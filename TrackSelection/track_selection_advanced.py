
import os

city2location = {}
for line in open('city_gps_refined.txt'):
  words = line.strip().split('___')
  city2location[words[0]] = (eval(words[1]),eval(words[2]))

delta = 0.00001*1000*30


for city in city2location.keys():
#for city in ['DenaliNatlPark,AK']:
  (x0,y0) = city2location[city]
  fout = open('./workout_by_city/file_first_gps_%s.txt' % city,'w')
  for line in open('file_first_gps.txt'):
    words = line.strip().split(' ')
    y = eval(words[1])
    x = eval(words[2])
    if x>=x0-delta/2 and x<=x0+delta/2 and y>=y0-delta/2 and y<=y0+delta/2:
      fout.write(line)
  fout.close()
  os.system('python compute_kml_from_track_basic_information.py ./workout_by_city/file_first_gps_%s.txt > ./workout_by_city/file_first_gps_%s.kml' % (city,city))
