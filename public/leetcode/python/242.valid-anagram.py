#
# @lc app=leetcode id=242 lang=python3
#
# [242] Valid Anagram
#

# @lc code=start
class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        lookup = {}
        for i in range(len(s)):
            lookup[s[i]] = lookup.get(s[i], 0) + 1
        for i in range(len(t)):
            lookup[t[i]] = lookup.get(t[i], 0) - 1
            if lookup[t[i]] < 0:
                return False
        
        for v in lookup.values():
            if v != 0:
                return False
        return True
# @lc code=end
Solution().isAnagram("rat", "car")
