#
# @lc app=leetcode id=22 lang=python3
#
# [22] Generate Parentheses
#

# @lc code=start
from typing import List

class Solution:
    def generateParenthesis(self, n: int) -> List[str]:
        result = []
        def dfs(open, close, pattern):
            if open + close == 2*n:
                result.append(pattern)
                return
            
            if open < n:
                dfs(open + 1, close, pattern + "(")
            if close < open:
                dfs(open, close + 1, pattern + ")")
        dfs(0,0,"")
        return result
        
# @lc code=end

