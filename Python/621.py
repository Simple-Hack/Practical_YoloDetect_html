import numpy as np
class Solution:
    def secondGreaterElement(self, nums: list[int]) -> list[int]:
        ll=len(nums)
        my_list=[]
        now=nums
        i=0
        while i<ll:
            if_first=0
            if_second=0
            ii=i+1
            if ii >= ll :
                my_list.append(-1)
                i+=1
                if(i >= ll):
                    break
                continue
            while ii< ll:  
                if now[ii] > now[i]:
                    if_first=1
                    iii=ii+1
                    while iii<ll:
                        if now[iii] > now[i]:
                            if_second=1
                            my_list.append(nums[iii])
                            break
                        iii=iii+1
                if if_second==1:
                    break
                ii=ii+1
            if if_first==0 or if_second==0:
                my_list.append(-1)
            i=i+1
        l=len(my_list)
        s=0
        while s<l:
            print(my_list[s])
            s=s+1
        return my_list
nums=[2,4,0,9,6]
ni=Solution.secondGreaterElement(Solution,nums)
