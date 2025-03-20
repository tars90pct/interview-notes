#
# @lc app=leetcode id=538 lang=python3
#
# [538] Convert BST to Greater Tree
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
class Solution:
    def convertBST(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        sum = 0
        def sol(root: TreeNode) -> TreeNode:
            nonlocal sum
            if root:
                sol(root.right)
                root.val += sum
                sum = root.val
                sol(root.left)
            return root
        return sol(root)
        
# @lc code=end

