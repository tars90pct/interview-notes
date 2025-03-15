#
# @lc app=leetcode id=98 lang=python3
#
# [98] Validate Binary Search Tree
#

# @lc code=start
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        def validate(left, right, root):
            if not root:
                return True
            if root.val > left and right > root.val:
                if not validate(left , root.val, root.left):
                    return False
                return validate(root.val , right, root.right)
            else:
                return False
        return validate(float("-inf"), float("inf"), root)
        
# @lc code=end

