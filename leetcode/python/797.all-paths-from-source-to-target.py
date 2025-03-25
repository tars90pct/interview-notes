#
# @lc app=leetcode id=797 lang=python3
#
# [797] All Paths From Source to Target
#

# @lc code=start
from typing import List

class Solution:
    def allPathsSourceTarget(self, graph: List[List[int]]) -> List[List[int]]:
        def dfs(path, result, index):
            if index == len(graph) - 1:
                result.append(path[:])
                return
            
            for i in graph[index]:
                path.append(i)
                dfs(path, result, i)
                path.pop()
        result = []
        dfs([0], result, 0)
        return result
# @lc code=end

