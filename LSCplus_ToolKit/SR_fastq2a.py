#!/usr/bin/python
import sys
import os

if len(sys.argv)>=2:
    in_filename = sys.argv[1]

else:
    print("Remove quality information and separate the reads from their names for performance reasons")
    print("usage: ./SR_fastq2a.py input_filename")
    print("or python SR_fastq2a.py input_filename")
    sys.exit(1)
    
###############################################################
#in_filename = 'SRR3372215.fastq'

f = open(in_filename,'r')
l = f.readline()

o = open("output_"+in_filename.split('.')[0]+".fasta",'w')
i = 0
while l:
    if l[0] !='@':
        print "Err: invalid SR fastq format"
        exit(1)
    #o.write('>'+l[1:])
    o.write('>SR_'+str(i)+'\n')
    i = i + 1
    l=f.readline()
    o.write(l)
    l=f.readline()
    l=f.readline()
    
    l=f.readline()
f.close()
o.close()
    
    
