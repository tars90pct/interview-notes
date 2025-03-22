#
# @lc app=leetcode id=337 lang=python3
#
# [337] House Robber III
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
    def rob(self, root: Optional[TreeNode]) -> int:
        memory = {}
        def rob_root(root):
            if root is None:
                return 0
            if root.left is None and root.right is None:
                return root.val
            
            if memory.get(root) is not None:
                return memory.get(root)
            
            val1 = root.val
            if root.left:
                val1 += rob_root(root.left.right) + rob_root(root.left.left)
            if root.right:
                val1 += rob_root(root.right.right) + rob_root(root.right.left)
            
            val2 = rob_root(root.left) + rob_root(root.right)
            memory[root] = max(val1, val2)
            return memory[root]
        return rob_root(root)
        
# @lc code=end

