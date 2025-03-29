#
# @lc app=leetcode id=84 lang=python3
#
# [84] Largest Rectangle in Histogram
#

# @lc code=start
from typing import List


class Solution:
    def largestRectangleArea(self, heights: List[int]) -> int:
        heights.insert(0, 0)
        heights.append(0)
        stack = []
        result = 0
        for i in range(len(heights)):
            while stack and heights[stack[-1]] > heights[i]:
                mid_index = stack.pop()
                if stack:
                    result = max(result, heights[mid_index] * (i - stack[-1] - 1))
            stack.append(i)
        return result
# @lc code=end
# [0, 2,1,5,6,2,3, 0]
Solution().largestRectangleArea([2,1,5,6,2,3])