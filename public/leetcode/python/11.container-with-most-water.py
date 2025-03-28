#
# @lc app=leetcode id=11 lang=python
#
# [11] Container With Most Water
#

# @lc code=start
class Solution(object):
    def maxArea(self, height):
        """
        :type height: List[int]
        :rtype: int
        """
        l = 0
        r = len(height) - 1
        max_area = 0
        while l < r:
            h = min(height[l], height[r])
            w = r - l
            max_area = max(max_area, h * w)
            if height[l] > height[r]:
                r -= 1
            else:
                l += 1
        return max_area
        # left = 0
        # right = len(height) - 1
        # max_area = 0
        # while left < right:
        #     current = min(height[left], height[right]) * (right - left)
        #     max_area = max(current, max_area)
        #     if height[left] > height[right]:
        #         right -= 1
        #     else:
        #         left += 1
        # return max_area
# @lc code=end

