from collections import Counter
import copy
unique_lists_set = set()
ans=[]
def find_every_group(split_list:list,num_fama:int,fama_array:list):
    global ans
    ans_list=[0 for i in range(11451)] 
    ans_list[0]=1
    for i in range(num_fama):
        lis=[]
        n=0
        if i in split_list:
            continue
        else:
                       
            for j in range(1145): 
                if j in lis:
                    continue
                if ans_list[j]==1: 
                    if ans_list[j+fama_array[i]]==0:
                        ans_list[j+fama_array[i]]=1
                        lis.append(j+fama_array[i])
                        n+=1
    ans.append(n)

    


def dfs_to_search_different_list(num_split_fama:int,current_list:list,num_fama:int,fama_array:list):
    global unique_lists_set
    frozen_lst = frozenset(current_list)
    if len(current_list)==num_split_fama and frozen_lst not in unique_lists_set:
        
        
        unique_lists_set.add(frozen_lst)
        find_every_group(current_list,num_fama,fama_array)
        return

    for i in range(num_fama):
        if i in current_list:
            continue
        else:
            copy_list=copy.deepcopy(current_list)
            copy_list.append(i)
            dfs_to_search_different_list(num_split_fama,copy_list,num_fama,fama_array)
        

def main():
    #code here

    n,m=map(int,input().split())

    fama_array=[int(s) for s in input().split()]

    former_list=[]

    dfs_to_search_different_list(m,former_list,n,fama_array)

    print(sum(ans))


    


    
    pass


if __name__ == '__main__':
    main();