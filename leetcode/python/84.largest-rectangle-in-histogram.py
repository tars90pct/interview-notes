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
                    result = max(result, (i - stack[-1] - 1) * heights[mid_index])
            stack.append(i)
        return result
        # heights.insert(0, 0)
        # heights.append(0)
        # stack = [0]
        # result = 0
        # for i in range(1, len(heights)):
        #     while stack and heights[i] < heights[stack[-1]]:
        #         mid_height = heights[stack[-1]]
        #         stack.pop()
        #         if stack:
        #             # area = width * height
        #             area = (i - stack[-1] - 1) * mid_height
        #             result = max(area, result)
        #     stack.append(i)
        # return result
# @lc code=end
