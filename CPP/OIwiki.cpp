#include <iostream>
#include <vector>
#include <ranges> // 包含范围库
#include <algorithm>
#include <string.h>
#include<functional>
#include<numeric>
#include<cctype>

class Solution {
public:
    std::vector<std::vector<int>> threeSum(std::vector<int>& nums) {
        std::sort( nums.begin( ), nums.end( ), []( int a, int b )->bool {return a < b;} );
        std::vector<std::vector<int>> ans;
        int i = 0;
        while (i < nums.size( )) {
            if (i and nums[i] == nums[i - 1]) {
                i++;
                continue;
            }
            int left = i + 1;
            int right = nums.size( ) - 1;
            while (left < right) {
                while (left < right and nums[left] == nums[left - 1]) {
                    left++;
                }
                while(left<right and nums[right]==nums[right + 1]){
                    right--;
                }
                if (left >= right)break;
                
                int sum = nums[i] + nums[left] + nums[right];
                if (sum< 0) {
                    left++;
                }
                else if (sum > 0) {
                    right--;
                }
                else {
                    ans.push_back( { nums[i],nums[right],nums[left] } );
                    
                    left++, right--;
                }
            }
            i++;
        }
        return ans;
    }
};