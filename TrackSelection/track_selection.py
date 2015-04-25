

# 51.3, -0.5
# 51.3, 0.2
# 51.7, -0.5
# 51.7, -0.2


# city data is (lat,lng)
# raw data is (lng,lat)

import os

helsinki_gps = (+60.16660,+24.88330)
london_gps = (+51.50000,-0.11670)



delta = 0.00001*1000*30

for city in ['helsinki','london']:
  if city == 'helsinki':
    (x0,y0) = helsinki_gps
  if city == 'london':
    (x0,y0) = london_gps
  fout = open('file_first_gps_%s.txt' % city,'w')
  for line in open('file_first_gps.txt'):
    words = line.strip().split(' ')
    y = eval(words[1])
    x = eval(words[2])
    if x>=x0-delta/2 and x<=x0+delta/2 and y>=y0-delta/2 and y<=y0+delta/2:
      fout.write(line)
  fout.close()
  os.system('python compute_kml_from_track_basic_information.py file_first_gps_%s.txt > file_first_gps_%s.kml' % (city,city))