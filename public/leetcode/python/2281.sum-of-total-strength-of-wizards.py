#
# @lc app=leetcode id=2281 lang=python3
#
# [2281] Sum of Total Strength of Wizards
#

# @lc code=start
from itertools import accumulate
from typing import List


class Solution:
    def totalStrength(self, strength: List[int]) -> int:
        ans = 0 
        stack = []
        prefix = list(accumulate(accumulate(strength), initial=0))
        for i, x in enumerate(strength + [0]): 
            while stack and stack[-1][1] >= x: 
                mid = stack.pop()[0]
                lo = stack[-1][0] if stack else -1 
                left = prefix[mid] - prefix[max(lo, 0)]
                right = prefix[i] - prefix[mid]
                ans = (ans + strength[mid]*(right*(mid-lo) - left*(i-mid))) % 1_000_000_007
            stack.append((i, x))
        return ans 
# @lc code=end
Solution().totalStrength([1,3,1,2])
