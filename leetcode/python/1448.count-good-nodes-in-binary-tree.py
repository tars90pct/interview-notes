#
# @lc app=leetcode id=1448 lang=python3
#
# [1448] Count Good Nodes in Binary Tree
#

# @lc code=start
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def goodNodes(self, root: TreeNode) -> int:
        if not root:
            return 0
        result = 0
        def dfs(root, current):
            if root is None:
                return
            if root.val >= current:
                nonlocal result
                result += 1
            current = max(current, root.val)
            dfs(root.left, current)
            dfs(root.right, current)
        dfs(root, root.val)
        return result
# @lc code=end

