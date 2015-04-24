

import os
import re

endomondodir = '../Endomondo/'

def get_track_position():
  for file in os.listdir(endomondodir):
    for line in open(endomondodir+file):
      if not len(re.findall('lng',line)) == 0:
        re.sub('lng":')
        print line
    break
  pass

if __name__ == '__main__':
  print "hello world"
  get_track_position()