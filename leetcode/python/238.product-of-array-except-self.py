#
# @lc app=leetcode id=238 lang=python3
#
# [238] Product of Array Except Self
#

# @lc code=start
class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        non_zero_product = 1
        has_zero = False
        for n in nums:
            if n == 0:
                if has_zero == False:
                    has_zero = True
                    continue
                else:
                    non_zero_product = 0
            non_zero_product = non_zero_product * n
        result = []
        for i in nums:
            if i == 0:
                result.append(non_zero_product)
            elif has_zero:
                result.append(0)
            else:
                result.append(int(non_zero_product/i))
        return result
# @lc code=end

