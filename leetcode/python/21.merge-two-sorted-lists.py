#
# @lc app=leetcode id=21 lang=python
#
# [21] Merge Two Sorted Lists
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
    def mergeTwoLists(self, list1, list2):
        """
        :type list1: Optional[ListNode]
        :type list2: Optional[ListNode]
        :rtype: Optional[ListNode]
        """
        dummy = ListNode()
        current  = dummy
        while (list1 != None and list2 != None):
            if list1.val < list2.val:
                current.next = list1
                current = current.next
                list1 = list1.next
            else:
                current.next = list2
                current = current.next
                list2 = list2.next
        while list1 != None:
            current.next = list1
            current = current.next
            list1 = list1.next
        while list2 != None:
            current.next = list2    
            current = current.next
            list2 = list2.next
        return dummy.next
        
# @lc code=end

