#
# @lc app=leetcode id=738 lang=python3
#
# [738] Monotone Increasing Digits
#

# @lc code=start
class Solution:
    def monotoneIncreasingDigits(self, n: int) -> int:
        str_num = list(str(n))
        flag = len(str_num)

        for i in range(len(str_num) - 1, 0, -1):
            if str_num[i] < str_num[i-1]:
                flag = i
                str_num[i-1] = str(int(str_num[i - 1]) - 1)
        for i in range(flag, len(str_num)):
            str_num[i] = '9'
        
        return int(''.join(str_num))

        
# @lc code=end

