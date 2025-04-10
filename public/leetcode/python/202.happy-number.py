#
# @lc app=leetcode id=202 lang=python3
#
# [202] Happy Number
#

# @lc code=start
class Solution:
    def isHappy(self, n: int) -> bool:
        if n == 1:
            return True
        exists = set()
        def beHappy(num):
            result = 0
            for c in str(num):
                result += int(c) * int(c)
            return result
        while n not in exists:
            exists.add(n)
            n = beHappy(n)
            if n == 1:
                return True
        return False
            
# @lc code=end

