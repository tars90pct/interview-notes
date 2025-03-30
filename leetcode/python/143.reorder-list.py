#
# @lc app=leetcode id=143 lang=python
#
# [143] Reorder List
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
    def reorderList(self, head):
        """
        :type head: Optional[ListNode]
        :rtype: None Do not return anything, modify head in-place instead.
        # """

        # find mid
        fast = head
        slow = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        right_end = slow.next
        slow.next = None
        left = head

        def reverse(prev, curr):
            if curr is None:
                return prev
            temp = curr.next
            curr.next = prev
            return reverse(curr, temp)
        right = reverse(None, right_end)

        dummy = ListNode()
        current = dummy
        while left and right:
            current.next = left
            left = left.next
            current = current.next
            current.next = right
            right = right.next
            current = current.next
        
        if left:
            current.next = left
        if right:
            current.next = right
        
        return dummy.next

        # fast = head
        # slow = head

        # while fast and fast.next:
        #     fast = fast.next.next
        #     slow = slow.next

        # second = slow.next
        # slow.next = None
        # node = None

        # while second:
        #     temp = second.next
        #     second.next = node
        #     node = second
        #     second = temp

        # first = head
        # second = node

        # while second:
        #     temp1, temp2 = first.next, second.next
        #     first.next, second.next = second, temp1
        #     first, second = temp1, temp2

        
        
        
# @lc code=end

