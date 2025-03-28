#
# @lc app=leetcode id=3 lang=python3
#
# [3] Longest Substring Without Repeating Characters
#

# @lc code=start
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        lookup = set() # char -> index
        l = 0
        result = 0
        for i in range(len(s)):
            if s[i] not in lookup:
                result = max(result, i - l + 1)
                lookup.add(s[i])
            else:
                while l <= i and s[l] != s[i]:
                    lookup.remove(s[l])
                    l += 1
                l += 1
        return result
# @lc code=end

Solution().lengthOfLongestSubstring("pwwkew")