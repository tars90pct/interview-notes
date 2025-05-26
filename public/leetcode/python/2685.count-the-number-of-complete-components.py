#
# @lc app=leetcode id=2685 lang=python3
#
# [2685] Count the Number of Complete Components
#

# @lc code=start
from collections import defaultdict
from typing import List


class Solution:
    def countCompleteComponents(self, n: int, edges: List[List[int]]) -> int:
        if n == 1:
            return 1
        root = [i for i in range(n)]
        def find(node):
            if node != root[node]:
                root[node] = find(root[node])
            return root[node]
        connection = defaultdict(list)
        for edge in edges:
            connection[edge[0]].append(edge[1])
            connection[edge[1]].append(edge[0])
            root1 = find(edge[0])
            root2 = find(edge[1])
            if root1 != root2:
                root[root1] = root2

        for i in range(len(root)):
            find(i)
        
        groups = defaultdict(int)
        for i in root:
            groups[i] += 1
        result = 0
        for group in groups.keys():
            node_len = groups[group] - 1
            if len(connection[group]) != node_len:
                continue
            result += 1
            for other in connection[group]:
                if len(connection[other]) != node_len:
                    result -= 1
                    break
        return result
        
        
# @lc code=end
Solution().countCompleteComponents(n = 6, edges = [[0,1],[0,2],[1,2],[3,4]])

