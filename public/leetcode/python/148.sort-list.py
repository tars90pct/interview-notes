#
# @lc app=leetcode id=148 lang=python
#
# [148] Sort List
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
    def sortList(self, head):
        """
        :type head: Optional[ListNode]
        :rtype: Optional[ListNode]
        """
        if not head or not head.next:
            return head
        
        # find mid
        slow = head
        fast = head.next
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        
        left = head
        right = slow.next
        slow.next = None

        left = self.sortList(left)
        right = self.sortList(right)

        dummy = ListNode()
        curr = dummy
        while left and right:
            if left.val < right.val:
                curr.next = left
                left = left.next
                curr = curr.next
            else:
                curr.next = right
                right = right.next
                curr = curr.next
        
        curr.next = left or right
        
        return dummy.next

        # if not head or not head.next:
        #     return head

        # # Split the linked list into two halves using "slow and fast pointer" technique to find the midpoint of the linked list
        # slow, fast = head, head.next
        # while fast and fast.next:
        #     slow = slow.next
        #     fast = fast.next.next
        # # The midpoint of the linked list is slow.next
        # mid = slow.next
        # # Set slow.next to None to separate the left and right halves of the linked list
        # slow.next = None

        # # Recursively sort the left and right halves of the linked list
        # left = self.sortList(head)
        # right = self.sortList(mid)

        # # Merge the two sorted halves of the linked list
        # dummy = ListNode(0)
        # curr = dummy
        # while left and right:
        #     if left.val < right.val:
        #         curr.next = left
        #         left = left.next
        #     else:
        #         curr.next = right
        #         right = right.next
        #     curr = curr.next
        # curr.next = left or right

        # return dummy.next
# @lc code=end

