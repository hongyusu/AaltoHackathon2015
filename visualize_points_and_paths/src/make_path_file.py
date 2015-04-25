

import re


for keyword in ['London,England10','London,England20','New_York,NY10','New_York,NY20']:


	fout = open('../res/path_%s.txt' % keyword, 'w')

	nodes = {}
	for line in open('../../mapAndNode/result/node_info%s.txt'%  keyword):
	  words = line.strip().split(' ')
	  nodes[re.sub(':','',words[0])] = (words[1],words[2])


	h1 = open('../res/h1.txt').read()
	h2 = '{"type": "Feature", "geometry": {"type":"LineString", "coordinates": ['
	t2 = ']}\n},'
	t1 = open('../res/t1.txt').read()

	data = h1 + '\n'
	ind = 0
	for line in open('../../mapAndNode/result/map_info%s.txt' % keyword):
	  ind = ind + 1
	  words = line.strip().split(" ")
	  entry = h2 + "[%s,%s],[%s,%s]" % (nodes[words[0]][0],nodes[words[0]][1],nodes[words[1]][0],nodes[words[1]][1]) + t2
	  data = data + entry
	  if ind==-20000:
	    break

	data = data + t1

	fout.write(data)  

	fout.close()
