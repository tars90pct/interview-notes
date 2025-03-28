#
# @lc app=leetcode id=721 lang=python3
#
# [721] Accounts Merge
#

# @lc code=start
class Solution:
    def accountsMerge(self, accounts: List[List[str]]) -> List[List[str]]:
        parent = {}
        def find(node):
            if node != parent.get(node):
                parent[node] = find(parent[node])
            return parent[node]
        def union(node1, node2):
            root1 = find(node1)
            root2 = find(node2)
            if root1 != root2:
                parent[root1] = root2
        for i in range(len(accounts)):
            for email in accounts[i][1:]:
                parent[email] = email
        for i in range(len(accounts)):
            root = accounts[i][1]
            for email in accounts[i][2:]:
                union(root, email)
        result = {}
        for i in range(len(accounts)):
            
# @lc code=end

