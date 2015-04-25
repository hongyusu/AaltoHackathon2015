#!/usr/bin/python
import json
from math import ceil
from os import listdir, path
import sys
toolPath = '../../TrackSelection/'
sys.path.append(toolPath)
from haversine import haversine



resultPath = '../resulttmp'
nodeInfoPath = path.join(resultPath, 'node_infoLondon,England20.txt')#each line cotains:'id:lng lat alt'
mapInfoPath = path.join(resultPath, 'map_infoLondon,England20.txt')#each line contains:'id1 id2:distance', the distance of unit is meter.
partialRoutesFile = path.join(toolPath, 'workout_by_city/file_first_gps_London,England.txt')

def getLogger():
        import logging
        _log = logging.getLogger('route_parse.log')
        _log.setLevel(logging.ERROR)
        _log.addHandler(logging.StreamHandler())
        return _log

_log_file = getLogger()

#global variables
BlockSize = 0.0001*2#about 10 meters
NodeIndex = {}#'Node.lat,Node.lng':node_object
nodeNum = 0

def center(n):
        '''
                get the center node of each block according to the real lng and lat
        '''
        return (ceil(n/BlockSize) + 0.5)*BlockSize

class Node(object):
        '''
                The whole word is divided into a matrix of blocks of which each block is labeled by the center point with the lng and lat.
                Currently, alt is just the value of the first encounted node.
        '''
        def __init__(self, id, lng, lat, alt):
                self.id = id
                self.lng = lng
                self.lat = lat
                self.alt = alt
                self.next = []

        def nodeInfo(self):
                return "%d: %f %f %f\n"%(self.id, self.lng, self.lat, self.alt)

class Route(object):
        '''
                for generating node link list and a node list 
        '''
        head = None
        def __init__(self, info):
                self.generate_route(info)

        def generate_route(self, infoStr):
                global nodeNum
                global NodeIndex
                '''
                        update the whole node list and generate node link list
                '''

                parent_node = None
                cur_node = None

                infoList = json.loads(infoStr)
                for info in infoList:
                        alt = 0
                        lng = 0
                        lat = 0
                        try:
                                #print info['lng'], info['lat']
                                lng = center(info['lng'])
                                lat = center(info['lat'])
                                alt = info['values']['alt']  

                        except KeyError as e:
                                #_log_file.error("value missing:%s"%str(e)) 
                                pass

                        indexKey = "%f,%f"%(lng, lat)
                        #update whole node dic
                        try:
                                cur_node = NodeIndex[indexKey]
                        except KeyError:
                                cur_node = Node(nodeNum, lng, lat, alt)
                                NodeIndex.update({indexKey:cur_node})
                                nodeNum += 1

                        #update node link list
                        if parent_node is not None and parent_node.id != cur_node.id and cur_node not in parent_node.next and parent_node not in cur_node.next:
                                parent_node.next.append(cur_node)
                        else:
                                self.head = cur_node
                        parent_node = cur_node


def parseFile(filePath):
        with open(filePath) as f:
                routeInfo = f.readlines()[-1][10:-2]
                if routeInfo:
                        route = Route(routeInfo)
                        route.head.nodeInfo()

def writeNodeInfo():
        with open(nodeInfoPath, 'w') as nf:
                for indexKey, node in NodeIndex.items():
                        nf.write(node.nodeInfo())

def writeMap():
        with open(mapInfoPath, 'w') as mf:
                for indexKey, node in NodeIndex.items():
                        if len(node.next):
                                mf.writelines('\n'.join(['{0} {1} {2}'.format(node.id, neighbor.id, haversine(node.lng, node.lat, neighbor.lng, neighbor.lat)) for neighbor in node.next])+'\n')

def generateMap(dataPath):
        whole = 0#whole data or partial routes in file
        if whole:
                for file_name in listdir(dataPath):
                        parseFile(path.join(dataPath, file_name))
        else:
                for fstr in open(partialRoutesFile):
                        file_name=fstr.split()[0]
                        parseFile(path.join(dataPath, file_name))

sports = {}
def sportsCategory(dataPath):
        for fileName in listdir(dataPath):
                for line in open(path.join(dataPath, fileName)):
                        if line.startswith("'sport'"):
                                sport = line.replace("'","").split(': ')[1].strip('\n')
                                try:
                                        sports[sport][0] += 1
                                        sports[sport][1].append(fileName)
                                except:
                                        sports[sport] = [0, [fileName]]

        with open(path.join(resultPath, 'sports_stat.txt'), 'w') as result:
                result.writelines('\n'.join(["%s: %d %s"%(sport, count, ','.join(files)) for sport, [count, files] in sports.items()]))
                                        

                
if __name__ == "__main__":
        dataPath = '../../Endomondo/'
        #dataPath = '../../../Data/workouts_anonymized/'
        #parseFile(path.join(dataPath, 'workout_13014.txt'))
        generateMap(dataPath)
        writeNodeInfo()
        writeMap()
        #sportsCategory(dataPath)

