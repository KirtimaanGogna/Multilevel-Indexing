import random
import string

def random_string(string_length=3):
    letters=string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(string_length))

""" utility functions to generate dataset """
def generate_dataset(lis,n): # for 1lac elements
    TID_list = random.sample(range(50000,200001),n)
    for i in range(n):
        single_rec=[]
        single_rec.append(TID_list[i])
        single_rec.append(random.randint(0,50000)+1)
        single_rec.append(random_string())
        single_rec.append(random.randint(0,1500)+1)    
        lis.append(single_rec)
    return lis,TID_list
    
    
"""data file generates again and again , does overwriting """
def write_to_file(lis,file_name):
    with open(file_name,'w') as f:
        for record in lis:
            f.writelines(str(record))
            f.write("\n")
            
