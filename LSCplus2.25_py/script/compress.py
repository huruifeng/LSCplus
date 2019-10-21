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
MinNonN=40
MaxN=1
if len(sys.argv)>0:
    for opt in sys.argv[1:]:
        if opt[0]=='-':
            opt_ls = opt.split('=')
            if opt_ls[0]=="-MinNonN":
                MinNonN = int(opt_ls[1])
            elif opt_ls[0]=="-MaxN":
                MaxN = int(opt_ls[1])
    prefix = sys.argv[-1]
else:
    print("Perform homopoylmer compression on a fasta or fastq file and generate a cps (fasta) and idx file")
    print("usage: python compress.py [-MinNonN=39] [-MaxN=1] filetype inseq out_prefix")
    print("or ./compress.py [-MinNonN=39] [-MaxN=1] filetype inseq out_prefix")
    sys.exit(1)

################################################################################   

inseq=open("temp/SR.fa."+prefix,'r')
outseq=open("temp/SR.fa."+prefix+'.cps','w')
idx = open("temp/SR.fa."+prefix+'.idx','w')
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

