#
# @lc app=leetcode id=560 lang=python
#
# [560] Subarray Sum Equals K
#

# @lc code=start
class Solution(object):
    def subarraySum(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """
        lookup = {0:1}
        current = 0
        result = 0
        for i, n in enumerate(nums):
            current += n
            pre = current - k
            if pre in lookup:
                result += lookup[pre]
            lookup[current] = lookup.get(current, 0) + 1
        return result        
# @lc code=end
