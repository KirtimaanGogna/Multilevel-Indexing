import synthesizer
import simulated_secondary_memory
from file_converter import file_converter
from indexRecords import IndexRecords
import math

unsorted_TID_list = []  
index_records_list = [] # create level 0 reqd to use

def generate_data(lis_size,file_name):
    global unsorted_TID_list
    lis,TID_list = synthesizer.generate_dataset([],lis_size)  # incosistent line
    unsorted_TID_list = TID_list
    synthesizer.write_to_file(lis,file_name)

def create_level_0(gamma,alpha):
    global unsorted_TID_list
    if(len(unsorted_TID_list) == 0): # when generate dataset is not used
        with open('dataset.txt','r') as fin:
            for line in fin:
                line_modified = line[1:].rstrip(']\n').split(', ')
                line_modified = [int(line_modified[i]) if i!=2 else line_modified[i].strip("\'") for i in range(len(line_modified))]
                # one input obtained in list form, created from dataset.txt
                unsorted_TID_list.append(line_modified[0])
        
    file_num = 1
    j = 1
    for i in unsorted_TID_list:
        index_records_list.append(IndexRecords(TID=i,block_name=str(file_num) + ".txt"))
        if j == alpha:
            j = 0
            file_num = file_num + 1
        j = j + 1
    # index_records_list is ready
    j=1
    file_num = 1
    for i in sorted(index_records_list, key=lambda x: x.TID):
        
        file_name = "l0_" + str(file_num) + ".txt"
        if j == gamma:
            j =  0
            file_num = file_num + 1
        j = j + 1
        with open(file_name,'a') as f:
            f.write(str(i.TID) + " " + i.block_name + "\n")

"""
len(sorted_index_records)/gamma**level
"""
def multi_levels(gamma):
    sorted_index_records = sorted(index_records_list, key=lambda x: x.TID)
    level = 2
    n = int(math.ceil(len(sorted_index_records)/(gamma**level))) # no of blocks in any level
    flag = 0
    while n>=1:
        k = 1
        print("\nLevel change")
        #print(n)
        # Sasta Tareeka
        if n == 1:
            flag = flag + 1
        if flag == 2:
            break
        # Main Logic below
        for i in range(1,n + 1):# no of blocks in any level
            print("\nBlock Change")
            file_name = "l" + str(level - 1) + "_" + str(i) + ".txt"
            # perfect till here
            with open(file_name,'a') as f:
                for j in range(gamma):
                    index = ((i-1)*gamma+j)*(gamma**(level - 1))
                    print(index)
                    if(index>=len(sorted_index_records)):
                        break
                    f.write(str(sorted_index_records[index].TID) + " l" + str(level - 2) + "_" + str(k) + ".txt\n")
                    k = k + 1
        level = level + 1
        n = int(math.ceil(len(sorted_index_records)/(gamma**level))) # no of blocks in any level
        
def actual_access(X,Y,gamma):
    global index_records_list
    ans = 0
    disk = 0
    blocks = 0
    level_jump = math.ceil(math.log(len(index_records_list),gamma))
    sorted_index_records = sorted(index_records_list, key=lambda x: x.TID)
    for i in range(len(sorted_index_records)):
        if sorted_index_records[i].TID >= X and sorted_index_records[i].TID <= Y:
            disk = disk + 1
            if (i + 1) % gamma == 0:
                blocks = blocks + 1
        if sorted_index_records[i].TID > Y:
            break
            
    ans = level_jump + disk + blocks
    return ans
            
def naive_opt(alpha):
    i = 0
    with open('dataset.txt','r') as fin:
        for line in fin:
            i = i + 1
    return i/alpha

def naive(X,Y,alpha):
    i = 0
    ans = 0
    found = 0
    if(X>Y):
        X, Y = Y, X
    with open('dataset.txt','r') as fin:
        for line in fin:
            i = i + 1
            line_modified = line[1:].rstrip(']\n').split(', ')
            line_modified = [int(line_modified[i]) if i!=2 else line_modified[i].strip("\'") for i in range(len(line_modified))]
            # one input obtained in list form, created from dataset.txt
            if(line_modified[0]>=X and line_modified[0]<=Y):
                print(line)
                found = found + 1
                if found == X + Y - 1:
                    break
            if(i % alpha == 0):
                ans = ans + 1
    print("No of records retrieved:",found)
    return ans

def roundup(x,b):
    return int(math.ceil(x/b))*b

def rounddown(x,b):
    return int(math.floor(x/b))*b

def get_theta(X,Y,bin_size):
    global unsorted_TID_list
    sorted_TID_list = sorted(unsorted_TID_list)
    dic = {}
    j = 0
    i = 40000
    while i <= 400000: # min hist and max hist X axis values
        dic[i] = 0
        i = i + bin_size
    
    i = 40000
    while i <= 400000 and j != len(sorted_TID_list): # min hist and max hist X axis values
        if(sorted_TID_list[j] >= i and sorted_TID_list[j] < i + bin_size):
            dic[i] = dic[i] + 1
            j = j + 1
            #print("s: {},i: {}, j: {}".format(sorted_TID_list[j],i,j))
        else:
            i = i + bin_size
    theta = 0
    theta = theta + (((roundup(X,bin_size) - X)/bin_size) * dic[roundup(X,bin_size)-bin_size])
    theta = theta + (((Y - rounddown(Y,bin_size))/bin_size) * dic[rounddown(Y,bin_size)])
    for i in range(roundup(X,bin_size),rounddown(Y,bin_size) - bin_size + 1,bin_size):
        theta = theta + dic[i]
    return theta
        
def multi_opt(X,Y,gamma,theta):
    global index_records_list
    if(len(index_records_list)==0):
        file_num = 1
        j = 1
        for i in unsorted_TID_list:
            index_records_list.append(IndexRecords(TID=i,block_name=str(file_num) + ".txt"))
            if j == alpha:
                j = 0
                file_num = file_num + 1
            j = j + 1
            
    height = math.ceil(math.log(len(index_records_list),gamma))
    return height + (theta/gamma) + 1 + theta
    
    
#%% INTERFACE        

alpha = int(input("\nEnter a block size: "))

while(1):
    print("\nEnter A Choice: ")
    print("1. Generate Data")
    print("2. File Converter")
    print("3. Simulate Secondary Memory (Mandatory)")
    print("4. Create Level 0 (Mandatory)")
    print("5. Create Multi levels (Mandatory)")
    print("6. Query Params (Mandatory)")
    print("7. Multilevel (Actual)")
    print("8. Naive Algorithm (Actual)")
    print("9. Naive Algorithm (Estimate)")
    print("10. Get theta")
    print("11. Multilevel (Estimate)")
    
    
    choice = int(input())
    
    if choice != 1:
        if(len(unsorted_TID_list) == 0): # when generate dataset is not used
            with open('dataset.txt','r') as fin:
                for line in fin:
                    line_modified = line[1:].rstrip(']\n').split(', ')
                    line_modified = [int(line_modified[i]) if i!=2 else line_modified[i].strip("\'") for i in range(len(line_modified))]
                    # one input obtained in list form, created from dataset.txt
                    unsorted_TID_list.append(line_modified[0])

    if choice == 1:
        total_index_records = int(input("\nEnter how number of records for 'dataset.txt': "))
        generate_data(total_index_records,'dataset.txt') #passing list size, file name
    elif choice == 2:
        file_converter(input("Enter file name for conversion: "),'dataset.txt')
    elif choice == 3:
        simulated_secondary_memory.simulate_secondary_memory('dataset.txt',alpha)
    elif choice == 4:
        gamma = int(input("\nEnter Gamma value: "))
        create_level_0(gamma,alpha)
    elif choice == 5:
        multi_levels(gamma)
    elif choice == 6:
        print("Enter X and Y for the query:")
        print("Select * From Transaction Where TID is between X and Y")
        X = int(input("X: "))
        Y = int(input("Y: "))
    elif choice == 7:
        print("Works after running option \"6. Query Params\" first!")
        print("Number of Disk access: {}".format(actual_access(X,Y,gamma)))
    elif choice == 8:
        print("Works after running option \"6. Query Params\" first!")
        print("No of disk access: {}".format(naive(X,Y,alpha)))
    elif choice == 9:
        print("Works after running option \"6. Query Params\" first!")
        print("Naive Optimizer estimate (disk access): {}".format(naive_opt(alpha)))
    elif choice == 10:
        print("Works after running option \"6. Query Params\" first!")
        bin_size = int(input("Enter Bin size of Histogram plot: "))
        theta = get_theta(X,Y, bin_size)
        print("Theta: {}".format(theta))
    elif choice == 11:
        print("Works after running option \"6. Query Params\" first!")
        print("Works after running option \"10. Get theta\" first!")
        print("Multilevel Optimizer estimate (disk access): {}".format(multi_opt(X,Y,gamma,theta)))