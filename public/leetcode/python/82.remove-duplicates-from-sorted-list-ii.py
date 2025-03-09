#
# @lc app=leetcode id=82 lang=python
#
# [82] Remove Duplicates from Sorted List II
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
    def deleteDuplicates(self, head):
        """
        :type head: Optional[ListNode]
        :rtype: Optional[ListNode]
        """
        dummy = ListNode()
        dummy.next = head
        prev = dummy
        curr = dummy.next
        while curr:
            while curr.next and curr.next.val == curr.val:
                curr = curr.next
            if prev.next == curr:
                prev = prev.next
                curr = curr.next
            else:
                curr = curr.next
                prev.next = curr
        return dummy.next
        # dummy = ListNode()
        # dummy.next = head
        # curr, prev = head, dummy
        # while curr:
        #     while curr.next and curr.val == curr.next.val:
        #         curr = curr.next
        #     if prev.next == curr:
        #         prev = prev.next
        #         curr = curr.next
        #     else:
        #         prev.next = curr.next
        #         curr = curr.next
        # return dummy.next
# @lc code=end

def list_to_linked_list(lst):
    if not lst:
        return None  # Empty list, return None

    head = ListNode(lst[0])  # Create the head node
    current = head

    for val in lst[1:]:  # Iterate through the rest of the list
        current.next = ListNode(val)
        current = current.next

    return head

Solution().deleteDuplicates(list_to_linked_list([1,2,3,3,4,4]))