#
# @lc app=leetcode id=45 lang=python3
#
# [45] Jump Game II
#

# @lc code=start
class Solution:
    def jump(self, nums: List[int]) -> int:
        if len(nums) <= 1:
            return 0
        next_distance = 0
        cover = 0
        result = 0
        for i in range(len(nums)):
            next_distance = max(next_distance, nums[i] + i)
            if next_distance >= len(nums) - 1:
                return result + 1
            if i == cover:
                result += 1
                cover = next_distance
        return result
# @lc code=end

