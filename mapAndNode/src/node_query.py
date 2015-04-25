#!/usr/bin/python
'''
        This script provide API on the node information file for:
        1.finding the nearest neighbor for a given query point
        2.transfering the list of id to a list of gps infomation
'''

from data_preprocess import nodeInfoPath

NodeList = {}

def find_neighbor_node(lng, lat):
        '''
                input:a pair of longtitude and latitude
                return: id of the nearest block center node
        '''
        min_dis = None
        neighbor = None

        #read and compre the query to the existing cener points
        for line in open(nodeInfoPath):
                info = line.split(':')
                id = int(info[0])
                info = info[1].split()
                clng = float(info[0])
                clat = float(info[1])
                calt = float(info[2])
                dln = abs(clng - lng)
                dla = abs(clat - lat)
                md = min(dln, dla)

                if min_dis is None or md < min_dis:
                        min_dis = md
                        neighbor = id
        return neighbor

def query_gps_list(id_list):
        '''
                input: a list of id, id is string
                output: 'lng lat alt;lng lat alt;...'
        '''
        #read the existing node info and output gps
        result = []
        for line in open(nodeInfoPath):
                info = line.strip().split(':')
                if info[0] in id_list:
                        result.append(info[1])
        return ';'.join(result)


#print find_neighbor_node(0, 52) 
#print query_gps_list(['66642', '66620', '73819','67690'])

