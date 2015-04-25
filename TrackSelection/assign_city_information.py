


city2location = {}
for line in open('city_gps_refined.txt'):
  words = line.strip().split('___')
  city2location[words[0]] = (eval(words[1]),eval(words[2]))

delta = 0.00001*1000*30



fout = open('file_first_gps_city.txt','w')
for line in open('file_first_gps.txt'):
  words = line.strip().split(' ')
  y = eval(words[1])
  x = eval(words[2])
  city = ''
  for key in city2location.keys():
    if x>=city2location[key][0]-delta/2 and x<=city2location[key][0]+delta/2 and y>=city2location[key][1]-delta/2 and y<=city2location[key][1]+delta/2:
      if city=='':
        city = key
      else:
        city = city + "___" + key
  fout.write("%s %s\n" %(line.strip(),city))

fout.close()


