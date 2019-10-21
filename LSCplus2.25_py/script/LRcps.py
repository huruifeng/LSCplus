#!/usr/bin/python

import sys
import os
import datetime

t0 = datetime.datetime.now()
################################################################################
def compress(seq):
    # Return values
    cps_seq = seq[0] # Compressed sequence
    cps_idx=[]
    n_count = 0
    
    # Loop carry values
    repeat_count=0
    ref_s = seq[0]
    
    for s in seq:
        if not ref_s == s:
            if (ref_s == 'N'):
                n_count += 1
            cps_idx.append(str(repeat_count))
            cps_seq = cps_seq + s
            repeat_count=1
            ref_s = s
        else:
            repeat_count+=1
    if (ref_s == 'N'):
        n_count += 1

    cps_idx.append(str(repeat_count))
        
    return cps_seq, cps_idx, n_count      

################################################################################

MinNonN=39
MaxN=10000

################################################################################

inseq=open("temp/LR_NoTails.fa",'r')
outseq=open("temp/LR_NoTails.fa.cps",'w')
idx = open("temp/LR_NoTails.fa.idx",'w')
    
# Process all the entries, one per iteration
while(True):
    # Read in the readname
    line = inseq.readline()
    if (line == ""):
        break
    readname = line[:-1]
    
    # Read in the sequence
    line = inseq.readline()
    if (line == ""):
        break

    seq = line.strip().upper()
    
    # Compress, filter and output the sequence
    cps_seq, cps_idx, n_count = compress(seq)
    if len(cps_seq)-n_count>=MinNonN and n_count<=MaxN:
        outseq.write(readname+'\n' + cps_seq + '\n')
        idx.write(readname + "\t" + ','.join(cps_idx) + '\n')
   
inseq.close()
outseq.close()
idx.close()
print "finsish genome"

################################################################################

