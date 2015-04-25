


h1 = open('../res/h1.txt').read()
h2 = open('../res/h2.txt').read()
t1 = open('../res/t1.txt').read()
t2 = open('../res/t2.txt').read()

data = h1
ind = 1
for line in open('../../TrackSelection/file_first_gps_london.txt'):
  ind = ind + 1
  words = line.strip().split(' ')
  entry = words[1]+','+words[2]
  data = data + h2 + entry + ']},"id":"' +"%s" % ind + '"},\n'

data = data + t1
print data
  
  