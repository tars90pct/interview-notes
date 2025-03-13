#
# @lc app=leetcode id=101 lang=python
#
# [101] Symmetric Tree
#

# @lc code=start
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
from collections import deque

class Solution(object):
    def isSymmetric(self, root):
        """
        :type root: Optional[TreeNode]
        :rtype: bool
        """
        return self.isSymmetriciIeratively(root)
        # return self.compare(root.left, root.right)
    
    def compare(self, left, right):
        if left is None and right is None:
            return True
        elif left is None or right is None:
            return False
        elif left.val != right.val:
            return False
        
        outside = self.compare(left.left, right.right)
        inside = self.compare(left.right, right.left)
        return outside and inside

    def isSymmetriciIeratively(self, root):
        """
        :type root: Optional[TreeNode]
        :rtype: bool
        """
        queue = deque([root])
        while queue:
            level = []
            for _ in range(len(queue)):
                node = queue.popleft()
                level.append(node)
                if node is None:
                    continue
                queue.append(node.left)
                queue.append(node.right)
            if level:
                mid = len(level) // 2
                left = 0
                while left <= mid:
                    right = len(level) - left - 1
                    ln = level[left]
                    rn = level[right]
                    left +=1 
                    if not ln and not rn:
                        continue
                    elif ln and rn:
                        if ln.val != rn.val:
                            return False
                        else:
                            continue
                    else:
                        return False
        return True
        
# @lc code=end

