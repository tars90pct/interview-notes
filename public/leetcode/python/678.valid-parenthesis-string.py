#
# @lc app=leetcode id=678 lang=python3
#
# [678] Valid Parenthesis String
#

# @lc code=start
class Solution:
    def checkValidString(self, s: str) -> bool:
        open = 0
        for c in s:
            if c == '(' or c == '*':
                open += 1
            else:
                if open == 0:
                    return False
                else:
                    open -= 1
        close = 0
        for i in range(len(s) - 1, -1, -1):
            if s[i] == ')' or s[i] == '*':
                close += 1
            else:
                if close == 0:
                    return False
                else:
                    close -= 1
        return True
# @lc code=end

