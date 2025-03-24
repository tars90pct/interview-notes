#
# @lc app=leetcode id=496 lang=python3
#
# [496] Next Greater Element I
#

# @lc code=start
from typing import List


class Solution:
    def nextGreaterElement(self, nums1: List[int], nums2: List[int]) -> List[int]:
        result = [-1] * len(nums1)
        stack = []
        lookup = {nums1[i]:i for i in range(len(nums1))}
        for i in range(len(nums2)):
            while stack and nums2[i] > stack[-1]:
                index = lookup.get(stack[-1])
                if index is not None:
                    result[index] = nums2[i]
                stack.pop()
            stack.append(nums2[i])
        return result

# @lc code=end