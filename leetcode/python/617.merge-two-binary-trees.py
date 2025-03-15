#
# @lc app=leetcode id=617 lang=python3
#
# [617] Merge Two Binary Trees
#

# @lc code=start
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def mergeTrees(self, root1: Optional[TreeNode], root2: Optional[TreeNode]) -> Optional[TreeNode]:
        if not root1 and not root2:
            return None
        val = 0
        root_1_left = None
        root_1_right = None
        root_2_left = None
        root_2_right = None
        if root1:
            root_1_left = root1.left
            root_1_right = root1.right
            val += root1.val
        if root2:
            root_2_left = root2.left
            root_2_right = root2.right
            val += root2.val
        root = TreeNode(val)
        root.left = self.mergeTrees(root_1_left, root_2_left)
        root.right = self.mergeTrees(root_1_right, root_2_right)
        return root
        

# @lc code=end

