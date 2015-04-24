

# 51.3, -0.5
# 51.3, 0.2
# 51.7, -0.5
# 51.7, -0.2


for line in open('file_first_gps.txt'):
  words = line.strip().split(' ')
  y = eval(words[1])
  x = eval(words[2])
  if x>=51.3 and x<=51.7 and y>=-0.5 and y<=0.2:
    print line,