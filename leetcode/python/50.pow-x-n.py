#
# @lc app=leetcode id=50 lang=python3
#
# [50] Pow(x, n)
#

# @lc code=start
class Solution:
    def myPow(self, x: float, n: int) -> float:
        def calc_power(x, n):
            if x == 0:
                return 0
            if x == 1:
                return 1
            if n == 0:
                return 1
            
            res = calc_power(x, n // 2)
            res = res * res

            if n % 2 == 1:
                return res * x
            
            return res
        ans = calc_power(x, abs(n))

        if n >= 0:
            return ans
        
        return 1 / ans 
# @lc code=end

