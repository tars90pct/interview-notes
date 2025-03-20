#
# @lc app=leetcode id=86 lang=python
#
# [86] Partition List
#

class ListNode(object):
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

# @lc code=start
# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution(object):
    def partition(self, head, x):
        """
        :type head: Optional[ListNode]
        :type x: int
        :rtype: Optional[ListNode]
        """
        dummy_l = ListNode()
        dummy_r = ListNode()
        left = dummy_l
        right = dummy_r
        curr = head
        while curr:
            if curr.val < x:
                left.next = curr
                left = left.next
            else:
                right.next = curr
                right = right.next
            curr = curr.next
        left.next = dummy_r.next
        right.next = None
        return dummy_l.next        
# @lc code=end

