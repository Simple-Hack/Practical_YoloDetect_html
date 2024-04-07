#include<unordered_map>
#include<vector>
#include<iostream>
#include <list>

class Solution {
private:
    std::vector<int> Ret;
    std::unordered_map<int,std::list<int>>hashMap;
public:
    bool find_index_in_hashMap(int index,std::unordered_map<int,std::list<int>>hashMap){
        auto it=hashMap.find(index);
        if(it==hashMap.end())
            return false;
        return true;
    }

    std::vector<int> twoSum(std::vector<int>& nums, int target) {
        int length_num=nums.size();
        int index=0;
        for(;index<length_num;index++){

            int next=target-nums[index];
            if(find_index_in_hashMap(next,hashMap)){
                Ret.push_back(index);
                Ret.push_back(hashMap[next].front());

                return Ret;
            }
            hashMap[nums[index]].push_back(index);
        }
        return {};
    }
};