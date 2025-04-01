#
# @lc app=leetcode id=124 lang=python3
#
# [124] Binary Tree Maximum Path Sum
#

# @lc code=start
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def maxPathSum(self, root: Optional[TreeNode]) -> int:
        result = root.val
        def dfs(root):
            if root is None:
                return 0
            left = max(dfs(root.left), 0)
            right = max(dfs(root.right), 0)
            nonlocal result
            result = max(
                result, 
                left + right + root.val
                )
            return root.val + max(left, right)
        dfs(root)
        return result
# @lc code=end

