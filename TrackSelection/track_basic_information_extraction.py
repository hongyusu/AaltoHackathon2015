

import os
import re

endomondodir = '../Endomondo/'

def get_track_position():
  for file in os.listdir(endomondodir):
    sporttype = 'na'
    username = 'na'
    distance = 'na'
    datetime = 'na'
    avgspeed = 'na'
    maxspeed = 'na'
    calories = 'na'
    for line in open(endomondodir+file):
      if not len(re.findall("'sport'",line)) == 0:
        words = line.strip().split(': ')
        sporttype = words[1]
      if not len(re.findall("'calories'",line)) == 0:
        words = line.strip().split(': ')
        calories = words[1]
      if not len(re.findall("'avg. speed'",line)) == 0:
        words = line.strip().split(': ')
        avgspeed = words[1]
      if not len(re.findall("'max. speed'",line)) == 0:
        words = line.strip().split(': ')
        maxspeed = words[1]
      if not len(re.findall("'date-time'",line)) == 0:
        words = line.strip().split(': ')
        datetime = words[1]
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
        print file,lng,lat,sporttype,username,distance,datetime,avgspeed,maxspeed,calories
        break
  pass

if __name__ == '__main__':
  get_track_position()
