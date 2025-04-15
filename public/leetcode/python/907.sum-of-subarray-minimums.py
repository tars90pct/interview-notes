#
# @lc app=leetcode id=907 lang=python3
#
# [907] Sum of Subarray Minimums
#

# @lc code=start
from typing import List


class Solution:
    def sumSubarrayMins(self, arr: List[int]) -> int:
        stack = []
        result = [0] * len(arr)
        for i in range(len(arr)):
            while stack and arr[stack[-1]] > arr[i]:
                stack.pop()
            j = stack[-1] if stack else -1
            result[i] = result[j] + (i - j) * arr[i]
            stack.append(i)
        return sum(result) % (10 ** 9 + 7)
# @lc code=end

