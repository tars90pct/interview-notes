#
# @lc app=leetcode id=150 lang=python3
#
# [150] Evaluate Reverse Polish Notation
#

# @lc code=start
from typing import List


class Solution:
    def evalRPN(self, tokens: List[str]) -> int:

        stack = []
        for t in tokens:
            if t == '+':
                r = stack.pop()
                l = stack.pop()
                stack.append(l + r)
            elif t == '-':
                r = stack.pop()
                l = stack.pop()
                stack.append(l - r)
            elif t == '*':
                r = stack.pop()
                l = stack.pop()
                stack.append(l * r)
            elif t == '/':
                r = stack.pop()
                l = stack.pop()
                stack.append(int(l / r))
            else:
                stack.append(int(t))
        return stack[-1]

# @lc code=end

Solution().evalRPN(["10","6","9","3","+","-11","*","/","*","17","+","5","+"]
)