# Binary Trees

<!-- level:beginner -->

## 🟢 Beginner Level — Binary Trees

<!-- examples:start -->
### 🌱 Simple Example
A **binary tree** is a data structure where each node has at most **two children** — a left and a right child.

Example structure:

```
   A
  / \
 B   C
```

This means **A** is the root, and **B** and **C** are its children.
<!-- examples:end -->

<!-- practice:start -->
### ✏️ Practice Problems
1. Identify the root of a binary tree.
2. Draw a binary tree with 3 nodes.
3. Explain the difference between root and leaf.
<!-- practice:end -->

<!-- visuals:start -->
### 🖼️ Visual Diagram
```
        5
       / \
      3   7
```
This tree shows 5 as the root, with two children: 3 (left) and 7 (right).
<!-- visuals:end -->

<!-- steps:start -->
### 🪜 Step-by-Step Explanation
1. A tree starts with a **root** node.  
2. Nodes can have **left** and/or **right** children.  
3. Nodes with no children are **leaf nodes**.
4. All nodes are connected via **edges**.
<!-- steps:end -->

<!-- code_python:start -->
### 🐍 Basic Python Code
```python
class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

root = Node(10)
root.left = Node(5)
root.right = Node(15)
```
<!-- code_python:end -->

<!-- testcases:start -->
### 🧪 Test Cases
| Input Operation | Tree State |
|-----------------|------------|
| Insert 10       | 10         |
| Insert 5        | 10 → 5     |
| Insert 15       | 10 → 5, 15 |
<!-- testcases:end -->

<!-- complexity:start -->
### ⏱️ Complexity (Easy Terms)
- Access: O(h) → *height of tree*
- Insert: O(h)
- Search: O(h)
For simple trees, h is small.
<!-- complexity:end -->

<!-- summary:start -->
### 📘 Summary
Binary Trees are structures with:
- A root node
- Up to two children per node
- Common in searching and hierarchical data
<!-- summary:end -->

<!-- analogies:start -->
### 🧠 Analogy
Think of a **family tree**, but each parent can have only **two children**.
<!-- analogies:end -->

<!-- pitfalls:start -->
### ⚠️ Pitfalls
- Forgetting to assign `None` for missing children
- Confusing left and right children while drawing
<!-- pitfalls:end -->

<!-- challenge:start -->
### 💪 Challenge Problem
Build a binary tree with height 3 and print all leaf nodes.
<!-- challenge:end -->

<!-- gif:start -->
### 🎬 GIF Walkthrough
(No GIF provided yet)
<!-- gif:end -->

<!-- postquiz:start -->
### 📋 Quick Post‑Read Quiz
1. What is the maximum number of children a node can have?  
2. What is a leaf node?  
3. Which node is at the top of the tree?
<!-- postquiz:end -->

---

<!-- level:intermediate -->

## 🟡 Intermediate Level — Binary Trees & Traversals

<!-- examples:start -->
### 🌿 Example
Given this tree:

```
      8
     / \
    3   10
   / \
  1   6
```

**Inorder Traversal Result:** 1, 3, 6, 8, 10
<!-- examples:end -->

<!-- practice:start -->
### ✏️ Practice Problems
1. Perform preorder traversal on a given tree.  
2. Perform postorder traversal on a tree of height 3.  
3. Identify leaf nodes in a given structure.
<!-- practice:end -->

<!-- visuals:start -->
### 🧭 Traversal Visual
```
Inorder:   Left → Root → Right  
Preorder:  Root → Left → Right  
Postorder: Left → Right → Root
```
<!-- visuals:end -->

<!-- steps:start -->
### 🪜 Step‑by‑Step Traversal
1. Visit left subtree  
2. Visit node  
3. Visit right subtree  
This pattern ensures sorted output in BST.
<!-- steps:end -->

<!-- code_python:start -->
### 🐍 Python Code (Inorder Traversal)
```python
def inorder(node):
    if not node:
        return
    inorder(node.left)
    print(node.value, end=" ")
    inorder(node.right)
```
<!-- code_python:end -->

<!-- testcases:start -->
### 🧪 Test Cases
Input Tree: [8,3,10,1,6]  
Output (Inorder): `1 3 6 8 10`
<!-- testcases:end -->

<!-- complexity:start -->
### ⏱️ Complexity
Traversals:
- Time: O(n)  
- Space: O(h) recursion depth
<!-- complexity:end -->

<!-- summary:start -->
### 📘 Summary
At intermediate level, user learns:
- Tree traversals
- Node relationships
- Sorted outputs via inorder (BST)
<!-- summary:end -->

<!-- analogies:start -->
### 🧠 Analogy
Traversal is like reading pages of a book in different orders.
<!-- analogies:end -->

<!-- pitfalls:start -->
### ⚠️ Pitfalls
- Forgetting base case (`if not node: return`)
- Incorrect left-right order → wrong output
<!-- pitfalls:end -->

<!-- challenge:start -->
### 💪 Challenge Problem
Write a function to count leaf nodes in a binary tree.
<!-- challenge:end -->

<!-- gif:start -->
### 🎬 GIF Walkthrough
(Not available)
<!-- gif:end -->

<!-- postquiz:start -->
### 📋 Quick Post-Read Quiz
1. What is the first node visited in preorder?  
2. Which traversal prints sorted output in BST?  
3. What does postorder visit last?
<!-- postquiz:end -->

---

<!-- level:advanced -->

## 🔴 Advanced Level — Balanced Trees & Height Analysis

<!-- examples:start -->
### 🌳 Example: Balanced Tree
```
        30
       /  \
     20    40
    / \    / \
   10 25  35 50
```
This is a **balanced tree** with equal subtree heights.
<!-- examples:end -->

<!-- practice:start -->
### ✏️ Practice Problems
1. Compute the height of a binary tree.  
2. Convert a sorted array to a height-balanced BST.  
3. Detect skewness in a tree.
<!-- practice:end -->

<!-- visuals:start -->
### 📊 Height Visualization
```
Height(left_subtree) = 2  
Height(right_subtree) = 2  
Tree is balanced.
```
<!-- visuals:end -->

<!-- steps:start -->
### 🪜 Steps: Height Calculation
1. Compute height(left)  
2. Compute height(right)  
3. Height = max(left, right) + 1  
4. Balanced if:  
   `abs(left - right) <= 1`
<!-- steps:end -->

<!-- code_python:start -->
```python
def height(node):
    if not node:
        return 0
    return max(height(node.left), height(node.right)) + 1

def is_balanced(node):
    if not node:
        return True
    left = height(node.left)
    right = height(node.right)
    return abs(left - right) <= 1 and is_balanced(node.left) and is_balanced(node.right)
```
<!-- code_python:end -->

<!-- testcases:start -->
### 🧪 Test Cases
1. Balanced tree → Output: True  
2. Skewed tree (every node right child) → Output: False
<!-- testcases:end -->

<!-- complexity:start -->
### ⏱️ Complexity
Naive balance check: O(n²)  
Optimized approach: O(n)
<!-- complexity:end -->

<!-- summary:start -->
### 📘 Summary
Advanced concepts include:
- Height-balanced trees  
- Height computation  
- Balance checking  
- Foundation for AVL & Red-Black Trees
<!-- summary:end -->

<!-- analogies:start -->
### 🧠 Analogy
A balanced tree is like a weighing scale — both sides must be almost equal.
<!-- analogies:end -->

<!-- pitfalls:start -->
### ⚠️ Pitfalls
- Recomputing height → causes O(n²)  
- Assuming balanced tree = perfect tree (not true)
<!-- pitfalls:end -->

<!-- challenge:start -->
### 💪 Challenge Problem
Implement optimized height + balance check in one recursion.
<!-- challenge:end -->

<!-- gif:start -->
### 🎬 GIF Walkthrough
(Not available)
<!-- gif:end -->

<!-- postquiz:start -->
### 📋 Quick Post-Read Quiz
1. What is the height of a leaf node?  
2. Define the balance condition.  
3. What is the height of an empty tree?
<!-- postquiz:end -->
