

import re
import os


for keyword in ['London,England20','New_York,NY20','Prague,Czech_Rep.20','Amsterdam,Neth.20','Bangkok,Thailand20','Fukuoka,Japan20','Sao_Paulo,Brazil20']:


	fout = open('../res/point_%s.txt' % keyword, 'w')

	h1 = open('../res/h1.txt').read()
	h2 = '{"type": "Feature", "geometry": {"type":"Point", "coordinates": '
	t2 = '}\n},'
	t1 = open('../res/t1.txt').read()

	os.system("cat ../../mapAndNode/result/node_info%s.txt |sort -rnk5 > su_tmp" % keyword)
	data = h1 + '\n'
	ind = 0
	for line in open('su_tmp'):
		ind = ind + 1
		words = line.strip().split(' ')
		entry = h2 + "[%s,%s]" % (words[1],words[2]) + '},'
		entry = entry + '"properties":{"mag":' + words[4]+ '}},\n'
		data = data + entry
		if ind == 8000:
			break

	data = data + t1

	fout.write(data)  

	fout.close()
