#
# @lc app=leetcode id=455 lang=python3
#
# [455] Assign Cookies
#

# @lc code=start
from typing import List

class Solution:
    def findContentChildren(self, g: List[int], s: List[int]) -> int:
        g.sort()
        s.sort()
        cookie_index = len(s) - 1
        result = 0
        for i in range(len(g) - 1, -1, -1):
            if cookie_index >= 0 and s[cookie_index] >= g[i]:
                cookie_index -= 1
                result += 1
        return result
# @lc code=end

