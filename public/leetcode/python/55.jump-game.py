#
# @lc app=leetcode id=55 lang=python3
#
# [55] Jump Game
#

# @lc code=start
class Solution:
    def canJump(self, nums: List[int]) -> bool:
        if len(nums) == 1:
            return True
        cover = 0
        for i in range(len(nums)):
            if i <= cover:
                cover = max(cover, i + nums[i])
                if cover >= len(nums) - 1:
                    return True
        return False

# @lc code=end

