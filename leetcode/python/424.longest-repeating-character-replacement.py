#
# @lc app=leetcode id=424 lang=python3
#
# [424] Longest Repeating Character Replacement
#

# @lc code=start
class Solution:
    def characterReplacement(self, s: str, k: int) -> int:
        freq = {}
        l = 0
        result = 1
        for r in range(len(s)):
            freq[s[r]] = freq.get(s[r], 0) + 1
            max_freq = max(freq.values())
            current_len = r - l + 1
            if current_len - max_freq > k:
                freq[s[l]] -= 1
                l += 1
            result = max(result, r - l + 1)
        return result
# @lc code=end

