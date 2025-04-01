#
# @lc app=leetcode id=297 lang=python3
#
# [297] Serialize and Deserialize Binary Tree
#

class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

# @lc code=start
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

from collections import deque


class Codec:

    def serialize(self, root):
        """Encodes a tree to a single string.
        
        :type root: TreeNode
        :rtype: str
        """
        if not root:
            return "None"  # Edge case: if tree is empty
        
        q = [root]  # Queue for BFS traversal
        res = []  # List to store serialized values
        
        while q:
            node = q.pop(0)  # Process the next node
            
            if node:
                res.append(str(node.val))  # Store the node value
                q.append(node.left)  # Add left child to queue
                q.append(node.right)  # Add right child to queue
            else:
                res.append("None")  # Mark None for missing children
        
        return ','.join(res)
        

    def deserialize(self, data):
        """Decodes your encoded data to tree.
        
        :type data: str
        :rtype: TreeNode
        """
        if data == "None":
            return None  # Edge case: if the tree is empty
        
        # Convert string back to a list, handling "None" values
        data = list(map(lambda x: None if x == "None" else int(x), data.split(",")))
        
        # Initialize root node
        root = TreeNode(data[0])
        q = [root]  # Queue to store nodes to be processed
        i = 1  # Pointer to track position in the data list
        
        while q and i < len(data):
            node = q.pop(0)  # Get the next node to assign children
            
            # Process left child
            if data[i] is not None:
                node.left = TreeNode(data[i])
                q.append(node.left)  # Add left child to queue
            
            # Process right child
            if i + 1 < len(data) and data[i + 1] is not None:
                node.right = TreeNode(data[i + 1])
                q.append(node.right)  # Add right child to queue
            
            i += 2  # Move to the next pair of children
        
        return root
        

# Your Codec object will be instantiated and called as such:
# ser = Codec()
# deser = Codec()
# ans = deser.deserialize(ser.serialize(root))
# @lc code=end

