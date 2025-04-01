#
# @lc app=leetcode id=572 lang=python3
#
# [572] Subtree of Another Tree
#

# @lc code=start
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def isSubtree(self, root: Optional[TreeNode], subRoot: Optional[TreeNode]) -> bool:
        def is_same_tree(p, q):
            if q is None and p is None:
                return True
            if p is not None and q is not None:
                if p.val != q.val:
                    return False
                return is_same_tree(p.left, q.left) and is_same_tree(p.right, q.right)
            return False
        
        if root is None and subRoot is None:
            return True
        if root is not None and subRoot is not None:
            if is_same_tree(root, subRoot):
                return True
            return self.isSubtree(root.left, subRoot) or self.isSubtree(root.right, subRoot)
        return False
        
# @lc code=end

