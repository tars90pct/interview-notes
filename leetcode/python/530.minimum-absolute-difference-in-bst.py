#
# @lc app=leetcode id=530 lang=python3
#
# [530] Minimum Absolute Difference in BST
#

# @lc code=start
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def __init__(self):
        self.result = float('inf')
        self.pre = None

    def traversal(self, cur):
        if cur is None:
            return
        self.traversal(cur.left)  # 左
        if self.pre is not None:  # 中
            self.result = min(self.result, cur.val - self.pre.val)
        self.pre = cur  # 记录前一个
        self.traversal(cur.right)  # 右

    def getMinimumDifference(self, root):
        self.traversal(root)
        return self.result
        
# @lc code=end

