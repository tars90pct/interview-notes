#
# @lc app=leetcode id=112 lang=python3
#
# [112] Path Sum
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
    def hasPathSum(self, root: Optional[TreeNode], targetSum: int) -> bool:
        def backtracking(current, root):
            if not root.left and not root.right:
                return current + root.val == targetSum
            
            for node in [root.left, root.right]:
                if not node:
                    continue
                result = backtracking(current + root.val, node)
                if result:
                    return True
            return False
        if root is None:
            return False
        return backtracking(0, root)

# @lc code=end

