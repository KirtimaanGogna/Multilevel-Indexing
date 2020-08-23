# -*- coding: utf-8 -*-

def simulate_secondary_memory(file_name,alpha):
    with open(file_name,'r') as fin:
        last_line = fin.readlines()[-1]
        last_line = last_line[1:].rstrip(']\n').split(', ')
        fin.seek(0)
        i = 1
        j = 1
        for line in fin:
            
            line_modified = line[1:].rstrip(']\n').split(', ')
            line_modified = [int(line_modified[i]) if i!=2 else line_modified[i].strip("\'") for i in range(len(line_modified))]
            with open(str(j)+'.txt','a+') as fout:
                fout.write(str(line_modified))
                fout.write("\n")
                if i!=alpha:
                    i = i + 1
                else: # End of alpha reached
                    i = 1
                    j = j + 1
                    if(int(last_line[0]) != line_modified[0]):
                        fout.write(str(j)+'.txt\n')
                    else:
                        fout.write('#\n')