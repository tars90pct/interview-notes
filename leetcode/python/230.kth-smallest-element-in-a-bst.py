#
# @lc app=leetcode id=230 lang=python3
#
# [230] Kth Smallest Element in a BST
#

# @lc code=start
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def kthSmallest(self, root: Optional[TreeNode], k: int) -> int:
        result = -1
        def dfs(root):
            if root is None:
                return
            dfs(root.left)

            nonlocal k
            if k == 1:
                nonlocal result
                result = root.val
                k -= 1
                return
            else:
                k -= 1
            
            dfs(root.right)
        dfs(root)
        return result
# @lc code=end

