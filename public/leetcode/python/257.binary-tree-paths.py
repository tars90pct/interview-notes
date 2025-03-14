#
# @lc app=leetcode id=257 lang=python3
#
# [257] Binary Tree Paths
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
from typing import List, Optional

class Solution:
    def binaryTreePaths(self, root: Optional[TreeNode]) -> List[str]:
        result = []
        def backtrack(path, result, root):
            if root is None:
                result.append(path)
                return result
            if not root.left and not root.right:
                path = path[:]
                path.append(str(root.val))
                result.append(path)
                return result
            for node in [root.left, root.right]:
                if node is None:
                    continue
                new_path = path[:]
                new_path.append(str(root.val))
                backtrack(new_path, result, node)
            return result
        result = []
        result = backtrack([], result, root)
        answer = []
        for path in result:
            answer.append("->".join(path))
        return answer
        
# @lc code=end

