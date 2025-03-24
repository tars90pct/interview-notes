#
# @lc app=leetcode id=42 lang=python3
#
# [42] Trapping Rain Water
#

# @lc code=start
from typing import List


class Solution:
    def trap(self, height: List[int]) -> int:
        stack = []
        result = 0
        for i in range(len(height)):
            while stack and height[i] > height[stack[-1]]:
                mid_index = stack.pop()
                if stack:
                    h = min(height[stack[-1]], height[i]) - height[mid_index]
                    w = i - stack[-1] - 1
                    result += h * w
            stack.append(i)
        return result
# @lc code=end


