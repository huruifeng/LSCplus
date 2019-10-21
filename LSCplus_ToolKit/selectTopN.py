#!/usr/bin/python
import sys
import os

if len(sys.argv)>=4:
    in_filename = sys.argv[1]
    in_N = sys.argv[2]
    in_N = int(in_N)
    output_filename = sys.argv[3]

else:
    print("Remove quality information and separate the reads from their names for performance reasons")
    print("usage: ./selectTopN.py input_file N output_file")
    print("or python selectTopN.py input_file N output_file")
    sys.exit(1)

###############################################################

f = open(in_filename,'r')
l = f.readline()

o = open(output_filename,'w')

i = 0

while l:
    if l[0] =='@':
       pass
    else:
        record_x = l[:-1].split('\t')
        name = record_x[0]
        read = record_x[9]
        s = ">"+name+'\n'+ read + '\n'
        o.write(s)
        i = i + 1
	print i
    if i == in_N:
        break
    l=f.readline()

f.close()
o.close()
    
    
