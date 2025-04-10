#
# @lc app=leetcode id=66 lang=python3
#
# [66] Plus One
#

# @lc code=start
from typing import List


class Solution:
    def plusOne(self, digits: List[int]) -> List[int]:
        carry = 0
        start = len(digits) - 1
        while start >= 0:
            value = digits[start] + 1
            carry = value // 10
            value = value % 10
            digits[start] = value
            start -= 1
            if carry == 0:
                break
        if carry > 0:
            digits.insert(0, carry)
        return digits
        
# @lc code=end

