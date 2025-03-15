#
# @lc app=leetcode id=654 lang=python3
#
# [654] Maximum Binary Tree
#

# @lc code=start
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def constructMaximumBinaryTree(self, nums: List[int]) -> Optional[TreeNode]:
        if not nums:
            return None
        max_v = -1
        max_index = -1
        for i in range(len(nums)):
            if nums[i] > max_v:
                max_v = nums[i]
                max_index = i
        
        left = nums[:max_index]
        right = nums[max_index+1:]
        root = TreeNode(max_v)
        root.left = self.constructMaximumBinaryTree(left)
        root.right = self.constructMaximumBinaryTree(right)
        return root
        
# @lc code=end

