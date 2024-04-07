def if_all_list_is_0(fence_heights:list) -> bool:

    for i in range(len(fence_heights)):
        if fence_heights[i] != 0:
            return False
    return True

def main():
    #code here
    num=0
    n = int(input())  
    fence_heights =[int(s) for s in input().split()] 
    if n == 1:
        print("1")
        return 
    le=len(fence_heights)
    while 1:
        begin=0
        end=0
        max_index=0
        max_length=0
        for i in range(le):
            if fence_heights[i]!=0:
                max_length=fence_heights[i]
                max_index=i
                begin=i
                j=i+1
                while j<le and fence_heights[j] != 0:
                    if fence_heights[j]>max_length:
                        max_length=fence_heights[j]
                        max_index=j
                    j+=1
                end=j
                break
            else:
                continue
        
        if begin==end-1:
            fence_heights[begin]=0
            num+=1
            if if_all_list_is_0(fence_heights):
                break
            else:
                continue
        
        if (end-begin)>=max_length:
            while begin!=end and begin<le:
                fence_heights[begin]-=1
                begin+=1
            num+=1
        else:
            fence_heights[max_index]=0

        
        if if_all_list_is_0(fence_heights):
            break


    print(num)
    
    pass


if __name__ == '__main__':
    main();