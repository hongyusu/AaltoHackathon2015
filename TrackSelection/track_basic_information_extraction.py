

import os
import re

endomondodir = '../Endomondo/'

def get_track_position():
  for file in os.listdir(endomondodir):
    sporttype = 'na'
    username = 'na'
    distance = 'na'
    for line in open(endomondodir+file):
      if not len(re.findall("'sport'",line)) == 0:
        words = line.strip().split(': ')
        sporttype = words[1]
      if not len(re.findall("'name'",line)) == 0:
        words = line.strip().split(': ')
        username = words[1]
      if not len(re.findall("'distance'",line)) == 0:
        words = line.strip().split(': ')
        distance = words[1]
      if not len(re.findall('"lng"',line)) == 0:
        line = re.sub('.*lng": ','', line)
        line = re.sub(',.*: ',' ',line)
        words = line.strip().split(' ')
        lng = words[0]
        lat = words[1]
        print file,lng,lat,sporttype,username,distance
        break
  pass

if __name__ == '__main__':
  get_track_position()
