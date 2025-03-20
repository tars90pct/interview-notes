基本操作：

- Insert(在current node後插入一個節點)

  ```
  temp = current.next
  current.next = target
  target.next = temp
  ```

- Delete(在current node後刪除一個節點)

  ```
  target = current.next
  next = None
  if target:
    next = target.next
  current.next = next
  target.next = None
  ```

- Iterate

  ```
  current = head
  while current:
    current = current.next
  ```

  或是

  ```
  def dfs(cur):
    if not cur:
      return None
    return dfs(cur.next)
  ```

- Reverse

  ```
  pre = None
  curr = head
  while curr.next:
    next = curr.next
    curr.next = pre
    pre = curr
    curr = next
  ```

  or

  ```
  def dfs(head, pre):
    if not head: return pre
    next = head.next
    head.next = pre
    dfs(next, head)
  ```

- Dummy head

  ```
  dummy = ListNode()
  dummy.next = head
  curr = head

  ... 一些操作

  return dummy.next
  ```

- 2 Pointers
  - 可以用來判斷是否有環
  - 找Linked list中點
  ```
  slow = head
  fast = head
  while fast and fast.next:
    slow = slow.next
    fast = fast.next.next
  ```
