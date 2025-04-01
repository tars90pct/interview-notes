#
# @lc app=leetcode id=100 lang=python3
#
# [100] Same Tree
#

# @lc code=start
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
        if p is None and q is None:
            return True
        if p is not None and q is not None:
            if p.val != q.val:
                return False
            else:
                return self.isSameTree(p.left, q.left) and self.isSameTree(p.right, q.right)
        return False
        
        
# @lc code=end

