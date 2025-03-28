#
# @lc app=leetcode id=76 lang=python3
#
# [76] Minimum Window Substring
#

# @lc code=start
class Solution:
    def minWindow(self, s: str, t: str) -> str:
        if len(t) > len(s):
            return ""

        freq = {}
        for c in t:
            freq[c] = freq.get(c, 0) + 1
        remains = len(t)
        result = ""
        result_len = float('inf')
        l = 0

        for r in range(len(s)):
            if freq.get(s[r], 0) > 0:
                remains -= 1
            freq[s[r]] = freq.get(s[r], 0) - 1
            if remains == 0:
                while freq.get(s[l]) != 0:
                    freq[s[l]] += 1
                    l += 1
                if r - l + 1 < result_len:
                    result_len = r - l + 1
                    result = s[l:r+1]
                freq[s[l]] += 1
                remains += 1
                l += 1
        return result

# @lc code=end
Solution().minWindow("ADOBECODEBANC", "ABC")
