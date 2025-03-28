#
# @lc app=leetcode id=399 lang=python3
#
# [399] Evaluate Division
#

# @lc code=start
from collections import deque
from typing import List

class Solution:
    def calcEquation(self, equations: List[List[str]], values: List[float], queries: List[List[str]]) -> List[float]:
        knwon_vars = {}
        for i in range(len(equations)):
            dividend, divisor = equations[i]
            knwon_vars[dividend] = {divisor: values[i]}
            knwon_vars[divisor] = {dividend: 1/values[i]}
        result = []
        for q in queries:
            dividend, divisor = q
            if dividend not in knwon_vars or divisor not in knwon_vars:
                result.append(-1)
            else:
                queue = deque([(dividend, 1)])
                visited = set()
                while queue:
                    for i in range(len(queue)):
                        node, result = queue.popleft()
                        if node == divisor:
                            return result
                        visited.add(node)
                        for key in knwon_vars[node]:
                            if key not in visited:
                                queue.append((key, result *knwon_vars[node][key]))
                return result
# @lc code=end

