# Linked List

Linked list 是一種線性資料結構，由多個節點（Node）透過**指標Pointer**連接而成。每個節點包含兩部分：

- 資料（Data）：儲存實際數值（如整數、字串、物件等）。
- 指標（Pointer）：指向下一個節點的記憶體位址。

定義如下：

```
interface Node<T> {
  val: T;    // 儲存泛型資料
  next: Node; // 指向下一個節點的參考
}
```

## Pattern

::TIPS
{{FILE|markdown/zh-tw/problem-solving/linked-list-pattern.md}}
::
