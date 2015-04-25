

import re
fout = open('city_gps_refined.txt','w')
fin = open('city_gps.txt')
for line in fin:
  line = line.strip()
  line = re.sub(' +\+','___+',line)
  line = re.sub(' +-','___-',line)
  words = line.split('___')
  fout.write("%s___%s___%s\n" %(re.sub(' *','',words[0]),words[1],re.sub(' .*','',words[2])) )
fin.close()
fout.close()