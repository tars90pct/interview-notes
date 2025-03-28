#
# @lc app=leetcode id=125 lang=python3
#
# [125] Valid Palindrome
#

# @lc code=start
class Solution:
    def isPalindrome(self, s: str) -> bool:
        l = 0
        r = len(s) - 1
        while r >= l:
            while l < len(s) and not s[l].isalnum():
                l += 1
            
            while r >= 0 and not s[r].isalnum():
                r -= 1

            if r >= l and s[l].lower() != s[r].lower():
                return False

            r -= 1
            l += 1
        return True
# @lc code=end
Solution().isPalindrome("0p")

