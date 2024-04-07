from collections import defaultdict
class Solution:
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        complement_map=defaultdict(list)
        for idx,num in enumerate(nums):
            complement=target-num
            if complement in complement_map:
                return [complement_map[complement][0],idx]
            complement_map[num].append(idx)

        return []
