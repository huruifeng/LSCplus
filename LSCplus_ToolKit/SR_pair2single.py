#!/usr/bin/python
import sys
import os

if len(sys.argv)>=2:
    in_filename = sys.argv[1]

else:
    print("usage: ./SR_pair2single.py input_filename")
    print("or python SR_pair2single.py input_filename")
    sys.exit(1)
    
###############################################################
#in_filename = 'SRR3372215.fastq'

f = open(in_filename,'r')
l = f.readline()

o = open("output_"+in_filename,'w')
i = 0
t = 0
while l:
    if l[0] !='>':
        print "Err: invalid SR fasta/fa format"
        exit(1)

    t = t % 2
    
    o.write('>SR_'+str(i)+"_"+str(t)+'\n')
    l=f.readline()
    o.write(l)
    t = t + 1
    
    o.write('>SR_'+str(i)+"_"+str(t)+'\n')
    l=f.readline()
    o.write(l)
    t = t + 1

    i = i+1
    l=f.readline()
    
f.close()
o.close()
    
    
