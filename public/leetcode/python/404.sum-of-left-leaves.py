#
# @lc app=leetcode id=404 lang=python3
#
# [404] Sum of Left Leaves
#

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

# @lc code=start
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
from typing import Optional


class Solution:
    def sumOfLeftLeaves(self, root: Optional[TreeNode]) -> int:
        def backtrack(isLeft, root):
            result = 0
            if not root.left and not root.right and isLeft:
                return root.val
            if root.left:
                result += backtrack(True, root.left)
            if root.right:
                result += backtrack(False, root.right)
            return result
        if not root.left and not root.right:
            return 0
        return backtrack(True, root)
        
# @lc code=end

