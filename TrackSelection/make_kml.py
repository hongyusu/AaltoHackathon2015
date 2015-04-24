



h1 = open('kml_head.txt').read()
t1 = open('kml_tail.txt').read()

h2 = open('place_head.txt').read()
t2 = open('place_tail.txt').read()

kmlfile=''
kmlfile+=h1
for line in open('file_first_gps.txt'):
  words = line.strip().split(' ')
  kmlfile=kmlfile+h2+words[1]+','+words[2]+t2

kmlfile = kmlfile + t1
print kmlfile