#!/usr/bin/python

import re
import random
import datetime
import sys

if len(sys.argv)>0:
    aa = sys.argv[-1]
    SCF = float(sys.argv[-2])
else:
    print "ERROR CODE: 1"
file_name = "temp/LR_SR.map."+aa

corrected_file = open(file_name+".corrected","w")
corrected_full_file = open(file_name+".corrected.full","w")

map_file = open(file_name,"r")
flag = 0
for map_line in map_file:
    map_line_ls = map_line.split("Q")

    LR_name = map_line_ls[0]
    LR_seq = list(map_line_ls[1])
    LR_idx = map_line_ls[2]

    L_LR_seq = len(LR_seq)

    LR_HC = LR_idx.split(",")

    SRs = map_line_ls[3].split(";")[:-1]

    start_pt = 10000
    end_pt = 0
    SR_end = 0

    SR_del_base = {}
    SR_del_HC = {}

    SR_ins_base = {}
    
    for SR in SRs:
        SR_info = SR.split("\t")

        SR_name = SR_info[0].split("_")[0]
        SR_rpt = int(SR_info[0].split("_")[1])
        
        pos = int(SR_info[1])-1

        if pos<start_pt:
            start_pt = pos

        SR_mis = SR_info[2][:-1]
    
        SR_seq_ls = list(SR_info[3])
        SR_idx_ls = SR_info[4].split(',')

        L_SR_seq = len(SR_seq_ls)

        SR_ins_ls = ['=']*L_SR_seq

        if SR_name[0] == '-':
            SR_idx_ls = SR_idx_ls[::-1]

        mis_pos_ls = {}
        
        mis_type_ls = re.findall('\+|-', SR_mis)# + or -
        mis_pos_seq = re.findall('\w+', SR_mis)#[pos1,seq1,pos2,seq2,....]

        
        for i in range(len(mis_type_ls)):
            mis_pos_ls[int(mis_pos_seq[i<<1])]=mis_type_ls[i]+mis_pos_seq[(i<<1)+1]

        mis_pos_sorted = mis_pos_ls.keys()
        
        mis_pos_sorted.sort()
        for k in mis_pos_sorted:

            mis_type = mis_pos_ls[k][0]
            l = len(mis_pos_ls[k])-1
            
            k -= 1
            if mis_type =='+':
                uncompress_str = ""
                for i in range(l):
                    uncompress_str += SR_seq_ls[k+i]*int(SR_idx_ls[k+i])

                del SR_seq_ls[k:k+l]
                del SR_idx_ls[k:k+l]
                del SR_ins_ls[k:k+l]
                SR_ins_ls[k] = uncompress_str
                
            elif mis_type == '-':
                
                SR_seq_ls.insert(k,'-')
                SR_idx_ls.insert(k,'0')
                SR_ins_ls.insert(k,'=')

        L_SR_seq = len(SR_seq_ls)
        temp_SR_end = pos+L_SR_seq

        if SR_end < temp_SR_end:
            SR_end = temp_SR_end

        j = 0
        while j < L_SR_seq:
            if j+pos in SR_del_base:
                SR_del_base[j+pos].extend([SR_seq_ls[j]]*SR_rpt)
                SR_del_HC[j+pos].extend([SR_idx_ls[j]]*SR_rpt)

                SR_ins_base[j+pos].extend([SR_ins_ls[j]]*SR_rpt)
            else:
                SR_del_base[j+pos]=[]
                SR_del_base[j+pos].extend([SR_seq_ls[j]]*SR_rpt)

                SR_del_HC[j+pos]=[]
                SR_del_HC[j+pos].extend([SR_idx_ls[j]]*SR_rpt)
                    
                SR_ins_base[j+pos]=[]
                SR_ins_base[j+pos].extend([SR_ins_ls[j]]*SR_rpt)
                
            j += 1

    ################################
    end_pt = max(SR_end,L_LR_seq)
 
    corrected_seq_full=""
    corrected_seq=""
    temp_str=""

    k = 0
    
    while k < end_pt:
        if k in SR_del_base:
           #####################################################
            ##ll = len(SR_del_base[k])-1
            ##x_random = random.randint(0,ll)
            ll = len(SR_del_base[k])
            x_random = 0
            x_max=0
            x_i=0        
            while x_random < ll:
                x_base=SR_del_base[k][x_random]
                x_count = SR_del_base[k].count(x_base)

                if x_count*100.00/ll >= SCF:
                    x_i = x_random
                    break

                if x_count > x_max:
                    x_max = x_count
                    x_i = x_random

                x_random += 1
            
            x_repeat = int(SR_del_HC[k][x_i])
            x_base=SR_del_base[k][x_i]

            temp_str=x_base*x_repeat
            #####################################################
          
            if SR_ins_base[k][x_i] != '=':
                temp_str=SR_ins_base[k][x_i]+temp_str    
            
            corrected_seq_full += temp_str
            corrected_seq += temp_str
        elif k < L_LR_seq:
            x_repeat = int(LR_HC[k])
            temp_str=LR_seq[k]*x_repeat
            corrected_seq_full += temp_str

            if k>=start_pt and k<SR_end:
                corrected_seq += temp_str    
            
        else:
            break
        
        k += 1

    corrected_full_file.write(">"+LR_name+"\n"+corrected_seq_full+"\n")
    corrected_file.write(">"+LR_name+"\n"+corrected_seq+"\n")

map_file.close()           
corrected_full_file.close()
corrected_file.close()    

        









































        
     
    
