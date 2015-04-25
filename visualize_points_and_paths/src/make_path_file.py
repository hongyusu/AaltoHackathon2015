


h1 = open('../res/h1.txt').read()
h2 = '{"type": "Feature", "geometry": {"type":"LineString", "coordinates": [\n'
t2 = ']},\n}'
t1 = open('../res/t1.txt').read()

data = h1
data = data + h2
ind = 1
for line in open('../../TrackSelection/file_first_gps_london.txt'):
  ind = ind + 1
  words = line.strip().split(' ')
  entry = words[1]+','+words[2]
  data = data + '[' + entry + '],'
  if ind == 5:
    break

data = data + t2+t1
print data
  
