#
# @lc app=leetcode id=133 lang=python3
#
# [133] Clone Graph
#

class Node:
    def __init__(self, val = 0, neighbors = None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []
# @lc code=start
"""
# Definition for a Node.
class Node:
    def __init__(self, val = 0, neighbors = None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []
"""

from typing import Optional
class Solution:
    def cloneGraph(self, node: Optional['Node']) -> Optional['Node']:
        if node is None:
            return None
        cache = {}
        def dfs(node):
            if node.val in cache:
                return cache[node.val]
            clone = Node(node.val)
            cache[node.val] = clone
            clone.neighbors = [dfs(n) for n in node.neighbors]
            return clone
        return dfs(node)
        
# @lc code=end

