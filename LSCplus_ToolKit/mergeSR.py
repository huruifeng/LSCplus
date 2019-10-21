#!/usr/bin/python
import sys
import os

if len(sys.argv)>=3:
    file_x1 = sys.argv[1]
    file_x2 = sys.argv[2]

else:
    print("Remove useless line breaks, and separate the reads from their names for performance reasons")
    print("usage: ./mergeSR.py filename1 filename2")
    print("or python mergeSR.py filename1 filename2")
    sys.exit(1)

###############################################################
o = open('SR.fa','w')

i = 0

f = open(file_x1,'r')
l = f.readline()
while l:
    temp = l[1:]
    name = "SR_"+str(i)
    
    l=f.readline()
    ll = len(l)-1
	
    o.write('>'+name+'_'+str(ll))
    o.write('\n')
    o.write(l)

    i = i + 1
    
    l=f.readline()
f.close()

f = open(file_x2,'r')
l = f.readline()
while l:
    temp = l[1:]
    name = "SR_"+str(i)
    
    l=f.readline()
    ll = len(l)-1
	
    o.write('>'+name+'_'+str(ll))
    o.write('\n')
    o.write(l)

    i = i + 1
    
    l=f.readline()
f.close()

o.close()
#######################################################    
    
