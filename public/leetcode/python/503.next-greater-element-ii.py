#
# @lc app=leetcode id=503 lang=python3
#
# [503] Next Greater Element II
#

# @lc code=start
from typing import List


class Solution:
    def nextGreaterElements(self, nums: List[int]) -> List[int]:
        result = [-1] * len(nums)
        stack = []
        for _ in range(2):
            for i in range(len(result)):
                while stack and stack[-1][1] < nums[i]:
                    (index, _) = stack.pop()
                    result[index] = nums[i]
                stack.append((i, nums[i]))
        return result
# @lc code=end

