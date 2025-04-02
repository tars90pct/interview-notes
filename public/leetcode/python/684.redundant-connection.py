#
# @lc app=leetcode id=684 lang=python3
#
# [684] Redundant Connection
#

# @lc code=start
from typing import List


class Solution:
    def findRedundantConnection(self, edges: List[List[int]]) -> List[int]:
        root = [ i for i in range(len(edges) + 1)]
        def find(node):
            if node != root[node]:
                root[node] = find(root[node])
            return root[node]
        for edge in edges:
            root1 = find(edge[0])
            root2 = find(edge[1])
            if root1 != root2:
                root[root1] = root2
            else:
                return [edge[0], edge[1]]

        # root = list(range(len(edges) + 1))
        # def find(node):
        #     if node != root[node]:
        #         root[node] = find(root[node])
        #     return root[node]

        # for (node1, node2) in edges:
        #     root1 = find(node1)
        #     root2 = find(node2)
        #     if root1 != root2:
        #         root[root1] = root2
        #     else:
        #         return [node1, node2]
# @lc code=end

Solution().findRedundantConnection([[1,2],[1,3],[2,3]])