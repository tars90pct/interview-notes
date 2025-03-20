#
# @lc app=leetcode id=968 lang=python3
#
# [968] Binary Tree Cameras
#

# @lc code=start
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def minCameraCover(self, root: Optional[TreeNode]) -> int:
        result = [0]
        # 2 covered
        # 1 camera
        # 0 not covered
        def postorder(root, result):
            if root is None:
                return 2
            lv = postorder(root.left, result)
            rv = postorder(root.right, result)
            if lv == 2 and rv == 2:
                return 0

            elif lv == 0 or rv == 0:
                result[0] += 1
                return 1
            else:
                return 2
        if postorder(root, result) == 0:
            result[0] += 1

        return result[0]
# @lc code=end

