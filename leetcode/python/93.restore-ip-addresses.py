#
# @lc app=leetcode id=93 lang=python3
#
# [93] Restore IP Addresses
#

# @lc code=start
from typing import List

class Solution:
    def restoreIpAddresses(self, s: str) -> List[str]:
        def is_valid_ip_digits(s: str):
            if not s:
                return False
            if s[0] == '0' and len(s) != 1:
                return False
            digits = int(s)
            return digits >= 0 and digits <= 255

        def backtracking(path, result, start):
            path_len = len(path)
            if path_len == 3:
                last = s[start:]
                if is_valid_ip_digits(last):
                    path.append(last)
                    result.append('.'.join(path))
                    path.pop()
                return
            for i in range(start, start + 3):
                end = i + 1
                left = s[start: end]
                if is_valid_ip_digits(left):
                    path.append(left)
                    backtracking(path, result, end)
                    path.pop()
        result = []
        backtracking([], result, 0)
        return result
        
# @lc code=end
Solution().restoreIpAddresses("0000")
