#
# @lc app=leetcode id=23 lang=python3
#
# [23] Merge k Sorted Lists
#

from typing import List, Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

# @lc code=start
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        dummy = ListNode()
        current = dummy
        while True:
            index = None
            for i in range(len(lists)):
                if index is None and lists[i]:
                    index = i
                elif lists[i] is not None and index is not None:
                    if lists[i].val <= lists[index].val:
                        index = i
            if index is None:
                break
            else:
                node = lists[index]
                current.next = node
                current = current.next
                lists[index] = node.next
        return dummy.next
        
# @lc code=end
def create_linked_list(arr):
    """
    Creates a linked list from a given list.

    Args:
        arr: A list of integers.

    Returns:
        The head of the linked list, or None if the list is empty.
    """
    if not arr:
        return None

    head = ListNode(arr[0])
    current = head
    for i in range(1, len(arr)):
        current.next = ListNode(arr[i])
        current = current.next

    return head

Solution().mergeKLists([
    create_linked_list([1,4,5]),
    create_linked_list([1,3,4]),
    create_linked_list([2,6])])
