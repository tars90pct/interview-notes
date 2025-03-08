#
# @lc app=leetcode id=15 lang=python
#
# [15] 3Sum
#

# @lc code=start
class Solution(object):
    def threeSum(self, nums):
        result = []
        nums.sort()
        for i in range(len(nums)):
            if nums[i] > 0:
                break
            if i > 0 and nums[i - 1]  == nums[i]:
                continue

            left = i + 1
            right = len(nums) - 1
            while left < right:
                current = nums[i] + nums[left] + nums[right]
                if current > 0:
                    right -= 1
                elif current < 0:
                    left += 1
                else:
                    result.append([nums[i], nums[left], nums[right]])
                    while left < right and nums[left] == nums[left + 1]:
                        left += 1
                    while left < right and nums[right] == nums[right - 1]:
                        right -= 1
                    left +=1
                    right -= 1

        return result
# @lc code=end

Solution().threeSum([-1,0,1,2,-1,-4])