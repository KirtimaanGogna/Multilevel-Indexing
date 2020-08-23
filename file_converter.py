# -*- coding: utf-8 -*-

def file_converter(file_name_input,file_name_output):
    with open(file_name_input,'r') as fin, open(file_name_output,'w') as fout:
        for line in fin:
            data_item = line.rstrip('\n').split(' ')
            data_item = [int(data_item[i]) if i!=2 else data_item[i] for i in range(len(data_item))]
            fout.write(str(data_item))
            fout.write('\n')