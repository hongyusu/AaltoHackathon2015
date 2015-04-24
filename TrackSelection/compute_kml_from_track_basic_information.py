



h1 = open('kml_head.txt').read()
t1 = open('kml_tail.txt').read()

h2 = open('place_head.txt').read()
t2 = open('place_tail.txt').read()

kmlfile=''
kmlfile+=h1
ind = 0
for line in open('file_first_gps.txt'):
  ind = ind + 1
  words = line.strip().split(' ')
  kmlfile=kmlfile+h2+words[1]+','+words[2]+t2
  if ind == 1000:
    break

kmlfile = kmlfile + t1
print kmlfile