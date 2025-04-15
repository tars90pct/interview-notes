#
# @lc app=leetcode id=2843 lang=python3
#
# [2843]   Count Symmetric Integers
#

# @lc code=start
class Solution:
    def countSymmetricIntegers(self, low: int, high: int) -> int:
        result = 0
        for i in range(low, high + 1):
            str_i = str(i)
            len_i = len(str_i)
            if len_i % 2 == 1:
                continue
            current = 0
            for j in range(len_i // 2):
                left = int(str_i[j])
                right = int(str_i[len_i - j - 1])
                current += left - right
            if current == 0:
                result += 1
        return result
# @lc code=end

Solution().countSymmetricIntegers(1200, 1230)