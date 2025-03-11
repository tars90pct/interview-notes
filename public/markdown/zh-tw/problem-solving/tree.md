# Tree

樹的題目只有一個核心思想，就是樹的遍歷。其實樹的遍歷的本質就是去把樹裡邊的每個元素都訪問一遍。必須從root節點開始訪問，然後根據子節點指標訪問子節點，但是子節點有多個方向，所以又有了先訪問哪個的問題，這造成了不同的遍歷方式。

## Binary Tree遍歷

- 分為recursive和stack + while的做法
- 看起來很簡單但推薦至少做一下stack + while(特別是inorder)，實作上不太一樣
- recursive的做法只需要記得修改中間節點的順序
  - preorder: left, self, right
  - inorder: self, left, right,
  - postorder: left, right, self
- stack + while 要用通用模版的話有雙色標記法或是空指針法
  - 因為stack的關係，順序會跟上面不同（包含self)
  - preorder: right, left, self
  - inorder: right, self, left
  - postorder: self, right, left

## Binary Tree遍歷 (recursive)

注意result.append(root.val)的位置

```
result = []

def inorder(root):
    if not root:
        return []

    inorder(root.left)
    result.append(root.val)
    inorder(root.right)
    return result

def preorder(root):
    if not root:
        return []

    result.append(root.val)
    preorder(root.left)
    preorder(root.right)
    return result

def postorder(root):
    if not root:
        return []

    postorder(root.left)
    postorder(root.right)
    result.append(root.val)
    return result
```

## Binary Tree遍歷 (while-loop + stack 雙色標記法)

- 使用白灰兩色來標記nodes，新節點是白色，訪問過的是灰色
- stack = [(WHITE, root)]
- 如果遇到的node是白色，將其標為灰色，然後把**右，自己，左**node依照這個順序放入stack中 (inorder)
- 如果要實現不同的排序
  - preorder: right, left, self,
  - inorder: right, self, left,
  - postorder: self, right, left
- 如果遇到的node是灰色，就輸出他

```
def inorder(root) -> List[int]:
  WHITE = 0
  GRAY = 1
  res = []
    stack = [(WHITE, root)]
  while stack:
    color, node = stack.pop()
    if node is None: continue
    if color == WHITE:
      stack.append((WHITE, node.right))
      stack.append((GRAY, node))
      stack.append((WHITE, node.left))
    else:
      res.append(node.val)
  return res
```

## Binary Tree遍歷 (while-loop + stack None pointer)

注意stack.push(node);和stack.push(null)放置的位置

- preorder: right, left, self
- inorder: right, self, left
- postorder: self, right, left

```
def postorderTraversal(self, root: TreeNode) -> List[int]:
  result = []
  st = []
  if root:
      st.append(root)
  while st:
    node = st.pop()
    if node != None:
        st.append(node) #中
        st.append(None)

  if node.right: #右
      st.append(node.right)
  if node.left: #左
      st.append(node.left)
  else:
    node = st.pop()
    result.append(node.val)
  return result
```

## BFS(廣度優先)和DFS(深度優先)

- DFS template

```
const visited = {}
function dfs(i) {
	if (特定條件達成）{
		return ...
	}

	visited[i] = true
	for (j = i可達到的下個狀態) {
		if (!visited[j]) {
			dfs(j)
		}
	}
}
```

- BFS template:

```
const visited = {}
function bfs() {
	let q = new Queue()
	q.push(...初始狀態)
	while(q.length) {
		let i = q.pop()
        if (visited[i]) continue
        if (符合條件) return ...
		for (j = i可達到的下個狀態) {
			if (j 合法) {
				q.push(j)
			}
		}
    }
    return not found
}
```
