#
# @lc app=leetcode id=27 lang=python
#
# [27] Remove Element
#

# @lc code=start
class Solution(object):
    def removeElement(self, nums, val):
        """
        :type nums: List[int]
        :type val: int
        :rtype: int
        """
        slow = 0
        for n in nums:
            if n == val:
                continue
            nums[slow] = n
            slow += 1
        return slow
# @lc code=end
Solution().removeElement([3,2,2,3]
,3)
