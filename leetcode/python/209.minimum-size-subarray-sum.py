#
# @lc app=leetcode id=209 lang=python
#
# [209] Minimum Size Subarray Sum
#

# @lc code=start
class Solution(object):
    def minSubArrayLen(self, target, nums):
        """
        :type target: int
        :type nums: List[int]
        :rtype: int
        """
        min_size = 100001
        current_sum = 0
        left = 0
        for right in range(len(nums)):
            current_sum += nums[right]
            while current_sum >= target and right >= left:
                min_size = min(min_size, right - left + 1)
                current_sum -= nums[left]
                left += 1
        
        if min_size == 100001:
            return 0
        return min_size
        
# @lc code=end

