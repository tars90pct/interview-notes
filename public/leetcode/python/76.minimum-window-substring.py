#
# @lc app=leetcode id=76 lang=python3
#
# [76] Minimum Window Substring
#

# @lc code=start
from collections import defaultdict


class Solution:
    def minWindow(self, s: str, t: str) -> str:
        if len(s) < len(t):
            return ""
        if len(s) == len(t):
            if s == t:
                return s
        
        freq_t = defaultdict(int)
        for ch in t:
            freq_t[ch] += 1
        freq = defaultdict(int)
        def isValid():
            for key, value in freq_t.items():
                if value > freq[key]:
                    return False
            return True 

        l = 0
        result = ""
        for r in range(len(s)):
            freq[s[r]] += 1
            while isValid():
                temp = s[l:r+1]
                if result == "":
                    result = temp
                elif len(temp) < len(result):
                    result = temp
                freq[s[l]] -= 1
                l += 1
        return result

# @lc code=end
Solution().minWindow("abc", "cba")
