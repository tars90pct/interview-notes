#
# @lc app=leetcode id=501 lang=python3
#
# [501] Find Mode in Binary Search Tree
#

# @lc code=start
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
from typing import Optional

class Solution:
    def findMode(self, root: Optional[TreeNode]) -> List[int]:
        counts = {}
        max_count = 0
        modes = []

        def inorder(node):
            if not node:
                return
            inorder(node.left)

            nonlocal max_count, modes

            counts[node.val] = 1 + counts.get(node.val, 0)
            
            if counts[node.val] > max_count:
                max_count = counts[node.val]
                modes = [node.val]
            elif counts[node.val] == max_count:
                modes.append(node.val)

            inorder(node.right)

        inorder(root)

        return modes
# @lc code=end

