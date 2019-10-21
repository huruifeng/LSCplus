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

    SR_list_base = {}
    SR_list_HC = {}

    crt_list_indel = {}
    

    for SR in SRs:
        SR_info = SR.split("\t")

        SR_name = SR_info[0].split("_")[0]
        SR_rpt = int(SR_info[0].split("_")[1])

        pos = int(SR_info[1])-1

        if pos<start_pt:
            start_pt = pos

        SR_mis = SR_info[2][:-1]
        
        SR_seq = SR_info[3]
        SR_idx = SR_info[4]

        SR_idx_vec = SR_idx.split(',')

        if SR_name[0] == '-':
            SR_idx_vec = SR_idx_vec[::-1]
    
        L_SR_seq = len(SR_seq)

        j = 0
        while j < L_SR_seq:
            if j+pos in SR_list_base:
                SR_list_base[j+pos].extend([SR_seq[j]]*SR_rpt)
                SR_list_HC[j+pos].extend([SR_idx_vec[j]]*SR_rpt)
            else:
                SR_list_base[j+pos]=[]
                SR_list_base[j+pos].extend([SR_seq[j]]*SR_rpt)
                
                SR_list_HC[j+pos]=[]
                SR_list_HC[j+pos].extend([SR_idx_vec[j]]*SR_rpt)
            j += 1

        temp_SR_end = pos+L_SR_seq

        if SR_end < temp_SR_end:
            SR_end = temp_SR_end
        
       
        mis_type_ls = re.findall('\+|-', SR_mis)
        mis_pos_ls = re.findall('\w+', SR_mis)

        j = 0
        for tp in mis_type_ls:
            x = int(mis_pos_ls[j*2])
            if x in crt_list_indel:
                crt_list_indel[x].extend([tp+mis_pos_ls[2*j+1]]*SR_rpt)
            else:
                crt_list_indel[x]=[]
                crt_list_indel[x].extend([tp+mis_pos_ls[2*j+1]]*SR_rpt)
            j += 1

    ################################
    
    end_pt = max(SR_end,L_LR_seq)

    corrected_seq_full=""
    corrected_seq=""
    temp_str=""
    k = 0
    i = 0
    LR_seq = list(LR_seq)
    
    while k < end_pt :
        if i in crt_list_indel:
            ##ll = len(crt_list_indel[i])-1
            ##x_random = random.randint(0,ll)
            ll = len(crt_list_indel[i])
            x_random = 0
            x_max=0
            x_i=0        
            while x_random < ll:
                temp_str_random = crt_list_indel[i][x_random]
                x_count = crt_list_indel[i].count(temp_str_random)

                if x_count*100.00/ll >= SCF:
                    x_i = x_random
                    break

                if x_count > x_max:
                    x_max = x_count
                    x_i = x_random

                x_random += 1

            temp_str_random = crt_list_indel[i][x_i]
            l = int(temp_str_random[1:])
            if temp_str_random[0]=='+':
                del crt_list_indel[i]
                i -= l
                end_pt += l

            if temp_str_random[0]=='-':
                del crt_list_indel[i]
                i += l
        
        if k in SR_list_HC:
            ##ll = len(SR_list_HC[k])-1
            ##x_random = random.randint(0,ll)
            ll = len(SR_list_HC[k])
            x_random = 0
            x_max=0
            x_i=0        
            while x_random < ll:
                x_base=SR_list_base[k][x_random]
                x_count = SR_list_base[k].count(x_base)

                if x_count*100.00/ll >= SCF:
                    x_i = x_random
                    break

                if x_count > x_max:
                    x_max = x_count
                    x_i = x_random

                x_random += 1
            
            x_repeat = int(SR_list_HC[k][x_i])
            x_base=SR_list_base[k][x_i]

            temp_str=x_base*x_repeat
            corrected_seq_full += temp_str
            corrected_seq += temp_str

            k += 1
            i += 1
            
        elif i < L_LR_seq:
            x_repeat = int(LR_HC[i])
            temp_str=LR_seq[i]*x_repeat
            corrected_seq_full += temp_str

            if k >= start_pt and k < SR_end:
                corrected_seq += temp_str

            i += 1
            if i > k and (i in SR_list_HC):
                k = i
            
        else:
            break
       
    #break    
    corrected_full_file.write(">"+LR_name+"\n"+corrected_seq_full+"\n")
    corrected_file.write(">"+LR_name+"\n"+corrected_seq+"\n")

map_file.close()           
corrected_full_file.close()
corrected_file.close()       

        









































        
     
    
