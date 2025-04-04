#
# @lc app=leetcode id=213 lang=python3
#
# [213] House Robber II
#

# @lc code=start
from typing import List


class Solution:
    def rob(self, nums: List[int]) -> int:
        if len(nums) == 1:
            return nums[0]
        if len(nums) == 2:
            return max(nums[0], nums[1])
        rob1 = self.robRange(0, len(nums) - 2, nums)
        rob2 = self.robRange(1, len(nums) - 1, nums)
        return max(rob1, rob2)

    def robRange(self, l, r, nums) -> int:
        if r - l == 1:
            return max(nums[l], nums[r])
        prev = 0
        curr = 0
        for i in range(l, r + 1):
            temp = max(curr, prev + nums[i])
            prev = curr
            curr = temp
        return curr


        # if len(nums) == 1:
        #     return nums[0]
        # if len(nums) == 2:
        #     return max(nums[0], nums[1])
        
        # result1 = self.robRange(nums, 0, len(nums) - 2)
        # result2 = self.robRange(nums, 1, len(nums) - 1)
        # return max(result1, result2)

    # def robRange(self, nums: List[int], start: int, end: int) -> int:
    #     if start == end:
    #         return nums[start]
        
    #     prev = 0
    #     curr = 0
    #     for i in range(start, end + 1):
    #         temp = curr
    #         curr = max(prev + nums[i], curr)
    #         prev = temp
    #     return curr
        
# @lc code=end

