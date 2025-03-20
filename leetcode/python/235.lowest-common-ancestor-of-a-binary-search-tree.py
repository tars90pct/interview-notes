#
# @lc app=leetcode id=235 lang=python3
#
# [235] Lowest Common Ancestor of a Binary Search Tree
#

# @lc code=start
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution:
    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        def dfs(root, p, q):
            if root is None:
                return None
            if root == q:
                return root
            if root == p:
                return root
            
            if p.val > root.val and q.val > root.val:
                return dfs(root.right, p, q)
            if p.val < root.val and q.val < root.val:
                return dfs(root.left, p, q)
            return root
        return dfs(root, p, q)
# @lc code=end

