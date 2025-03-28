#
# @lc app=leetcode id=167 lang=python3
#
# [167] Two Sum II - Input Array Is Sorted
#

# @lc code=start
from typing import List


class Solution:
    def twoSum(self, numbers: List[int], target: int) -> List[int]:
        l = 0
        r = len(numbers) - 1
        while l <= r:
            temp = numbers[l] + numbers[r]
            if temp == target:
                return [l + 1, r + 1]
            elif temp > target:
                r -= 1
            else:
                l += 1
        return []
        
# @lc code=end

