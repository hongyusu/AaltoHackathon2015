

import os
import re

endomondodir = '../Endomondo/'

def get_track_position():
  for file in os.listdir(endomondodir):
    for line in open(endomondodir+file):
      if not len(re.findall('lng',line)) == 0:
        line = re.sub('.*lng": ','', line)
        line = re.sub(',.*: ',' ',line)
        words = line.strip().split(' ')
        lng = words[0]
        lat = words[1]
        print file,lng,lat
        break
  pass

if __name__ == '__main__':
  get_track_position()
