#
# @lc app=leetcode id=110 lang=python3
#
# [110] Balanced Binary Tree
#

# @lc code=start
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def isBalanced(self, root: Optional[TreeNode]) -> bool:
        result = True
        def get_height(root):
            if not root:
                return 0
            l = get_height(root.left)
            r = get_height(root.right)
            if abs(l - r) > 1:
                nonlocal result
                result = False
            return max(l, r) + 1
        get_height(root)
        return result
# @lc code=end

