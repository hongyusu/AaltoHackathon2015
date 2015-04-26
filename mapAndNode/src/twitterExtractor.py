'''
        Downloaded from https://github.com/uwescience/datasci_course_materials/blob/master/assignment1/twitterstream.py
'''
import oauth2 as oauth
from key import api_key, api_secret, access_token_key, access_token_secret
import urllib2 as urllib
from os import path
import json

#See assignment1.html instructions or README for how to get these credentials
_debug = 0

oauth_token    = oauth.Token(key=access_token_key, secret=access_token_secret)
oauth_consumer = oauth.Consumer(key=api_key, secret=api_secret)

signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()

http_method = "GET"


http_handler  = urllib.HTTPHandler(debuglevel=_debug)
https_handler = urllib.HTTPSHandler(debuglevel=_debug)

def twitterreq(url, method, parameters):
        '''
        Construct, sign, open and read a twitter request
        using the credentials from another key.py.
        '''

        req = oauth.Request.from_consumer_and_token(oauth_consumer,
                token=oauth_token,
                http_method=http_method,
                http_url=url, 
                parameters=parameters)

        req.sign_request(signature_method_hmac_sha1, oauth_consumer, oauth_token)

        headers = req.to_header()
        if http_method == "POST":
                encoded_post_data = req.to_postdata()
        else:
                encoded_post_data = None
                url = req.to_url()


        #1:another option to get response from request with a singed url
        '''
        res = ""
        try:
                res = getResponseFromUrl(url)
        except:
                print 'error'
                pass

        if res != "":
                res = res.read()
        return res

        ''' 
        #second option
        opener = urllib.OpenerDirector()
        opener.add_handler(http_handler)
        opener.add_handler(https_handler)
        response = opener.open(url, encoded_post_data)
        if response:
                return response.read()
        else:
                return ""
def getResponseFromUrl(url):
        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.104 Safari/537.36'
        req = urllib.Request(url, None, {'User-Agent':user_agent})
        response = urllib.urlopen(req)
        return response

def extractText(res):
        js = json.loads(res)
        textStr = ""
        try:
              textStr = ';'.join([feed['text'] for feed in js['statuses']])
        except:
                pass
        return textStr

def fetchTwitters(lng, lat):
        global rad
        url='https://api.twitter.com/1.1/search/tweets.json'
        parameters = {'q':'','geocode':'%s,%s,%smi'%(lat, lng, rad), 'type':'mixed, recent', 'lang':'en'}
        response = twitterreq(url, "GET", parameters)
        return response

def nodesTwitters(fileName, resultFileName):
        dataPath =  '../result/'
        resultPath = path.join(dataPath, resultFileName)
        with open(resultPath, 'w') as rp:
                for line in  open(path.join(dataPath, fileName)):
                        info = line.split(':')
                        id = info[0]
                        info = info[1].split()
                        lng = info[0]
                        lat = info[1]
                        res = fetchTwitters(lng, lat)
                        if res != "":
                                res = res.encode('utf-8')
                                rp.write('%s:   %s\n'%(id, res))

def routeTwitters(routeIndex):
        dataPath = '../../RouteEngine/workout_%s.gps'%routeIndex
        resultPath = '../result/routeEngine_workout_%s_twitter.txt'%routeIndex
        with open(resultPath, 'w') as rp:
                node_id = 1
                for line in open(dataPath):
                        lng, lat = line.split()[0:2]
                        if node_id > 0:#just in case for the limits of request
                                res = fetchTwitters(lng, lat)
                                if res != "":
                                        res = res.encode('utf-8')
                                        rp.write('%s:   %s\n'%(node_id, res))
                        node_id += 1

def twitterAnalysis(routeIndex):
        dataPath = '../result/routeEngine_workout_%s_twitter.txt'%routeIndex
        nodePath = '../../RouteEngine/workout_%s.gps'%routeIndex
        nodeAndTwitterFile = '../result/routeEngine_workout_%s_tnames.json'%routeIndex
        nodeId = 1
        nodes = {}
        for line in open(nodePath):
                d = {}
                lng, lat = line.strip('\n').split()
                d.update({'lng':float(lng), 'lat':float(lat)})
                nodes.update({str(nodeId):d})
                nodeId += 1

        for line in open(dataPath):
                node_id, tstr = line.strip('\n').split(':   ')
                nameList = []
                jtweets = json.loads(tstr)
                s = ""
                text = ""
                name = ""
                for tweet in jtweets['statuses']:
                        try:
                                text = tweet['text']
                        except:
                                pass
                        if 'http://' not in text:
                                name = tweet['user']['name'].strip('\n')
                                break
                nodes[node_id].update({'user':name, 'tweet':text.replace('\n', '')})
        results = [ nodes[node] for node in nodes]
        result = [results[10], results[50], results[100]]
        with open(nodeAndTwitterFile, 'w') as ntf:
                json.dump(result, ntf)
                        
                

if __name__ == '__main__':
        global rad
        rad = 20#unit mile
        '''
        locations = ['London,England', 'New_York,NY', 'Prague,Czech_Rep.', 'Bangkok,Thailand', 'Sao_Paulo,Brazil', 'Fukuoka,Japan']
        locations = ['New_York,NY']
        suffix = 20
        for i in range(1):
                suf = locations[i]
                resultFname = 'twitter_%s%d_%dm.txt'%(suf, suffix, rad)
                nodesTwitters('node_info%s%d.txt'%(suf, suffix), resultFname)
        '''
        routeInd = ['58446.','5690']
        route = routeInd[1]
        routeTwitters(route)
        twitterAnalysis(route)
