#
# @lc app=leetcode id=669 lang=python3
#
# [669] Trim a Binary Search Tree
#

# @lc code=start
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def trimBST(self, root: Optional[TreeNode], low: int, high: int) -> Optional[TreeNode]:
        if root is None:
            return None
        if root.val > high or root.val < low:
            if not root.left and not root.right:
                return None
            if root.val > high:
                return self.trimBST(root.left, low, high)
            if root.val < low:
                return self.trimBST(root.right, low, high)
            return root
        root.right = self.trimBST(root.right, low, high)
        root.left = self.trimBST(root.left, low, high)
        return root

        
# @lc code=end

