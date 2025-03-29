#
# @lc app=leetcode id=20 lang=python3
#
# [20] Valid Parentheses
#

# @lc code=start
class Solution:
    def isValid(self, s: str) -> bool:
        lookup = {
            ')':'(',
            ']':'[',
            '}':'{'
        }
        stack = []
        for c in s:
            if c in lookup:
                if not stack or stack.pop() != lookup.get(c):
                    return False
            else:
                stack.append(c)
        return len(stack) == 0
        
# @lc code=end

