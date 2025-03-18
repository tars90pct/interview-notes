#
# @lc app=leetcode id=376 lang=python3
#
# [376] Wiggle Subsequence
#

# @lc code=start
from typing import List

class Solution:
    def wiggleMaxLength(self, nums: List[int]) -> int:
        if len(nums) <= 1:
            return len(nums)
        prev = 0
        curr = 0
        result = 1
        for i in range(len(nums) - 1):
            curr = nums[i + 1] - nums[i]
            if curr * prev <= 0 and curr != 0:
                result += 1
                prev = curr
        return result
# @lc code=end

