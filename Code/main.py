MAX_LEAF = 8

class Node:
    def __init__(self, left=None, right=None, value=None):
        self.left = left
        self.right = right
        self.value = value
        self.height = 1
        self.weight = 0
        self.recalc()

    def is_leaf(self):
        return self.value is not None

    def recalc(self):
        if self.is_leaf():
            self.weight = len(self.value)
            self.height = 1
        else:
            self.weight = total_length(self.left)
            self.height = 1 + max(total_height(self.left), total_height(self.right))

def total_length(node):
    if node is None:
        return 0
    if node.is_leaf():
        return len(node.value)
    return total_length(node.left) + total_length(node.right)

def total_height(node):
    if node is None:
        return 0
    if node.is_leaf():
        return 1
    return 1 + max(total_height(node.left), total_height(node.right))


def rotate_right(y):
    x = y.left
    new_y = Node(left=x.right, right=y.right, value=None)
    new_root = Node(left=x.left, right=new_y, value=None)
    return new_root

def rotate_left(x):
    y = x.right
    new_left = Node(left=x.left, right=y.left, value=None)
    new_root = Node(left=new_left, right=y.right, value=None)
    return new_root

def balance_node(node):
    if node is None or node.is_leaf():
        return node
    node = Node(left=node.left, right=node.right, value=None)
    balance = total_height(node.left) - total_height(node.right)
    if balance > 1:
        if total_height(node.left.left) < total_height(node.left.right):
            new_left = rotate_left(node.left)
            node = Node(left=new_left, right=node.right, value=None)
        return rotate_right(node)
    if balance < -1:
        if total_height(node.right.right) < total_height(node.right.left):
            new_right = rotate_right(node.right)
            node = Node(left=node.left, right=new_right, value=None)
        return rotate_left(node)
    return node

def concat_nodes(left_node, right_node):
    if left_node is None:
        return right_node
    if right_node is None:
        return left_node
    root = Node(left=left_node, right=right_node, value=None)
    return balance_node(root)

def build_rope_from_string(s):
    if s == "" or s is None:
        return None
    if len(s) <= MAX_LEAF:
        return Node(value=s)
    mid = len(s) // 2
    left = build_rope_from_string(s[:mid])
    right = build_rope_from_string(s[mid:])
    return concat_nodes(left, right)

def split_node(node, index):
    if node is None:
        return (None, None)
    if node.is_leaf():
        val = node.value
        if index <= 0:
            return (None, Node(value=val))
        if index >= len(val):
            return (Node(value=val), None)
        left_str = val[:index]
        right_str = val[index:]
        left_node = Node(value=left_str) if left_str else None
        right_node = Node(value=right_str) if right_str else None
        return (left_node, right_node)
    if index < node.weight:
        Lleft, Lright = split_node(node.left, index)
        new_right = concat_nodes(Lright, node.right)
        return (Lleft, new_right)
    elif index == node.weight:
        return (node.left, node.right)
    else:
        Rleft, Rright = split_node(node.right, index - node.weight)
        new_left = concat_nodes(node.left, Rleft)
        return (new_left, Rright)

def index_node(node, idx):
    if node is None:
        raise IndexError("index out of bounds")
    if node.is_leaf():
        if idx < 0 or idx >= len(node.value):
            raise IndexError("index out of bounds")
        return node.value[idx]
    if idx < node.weight:
        return index_node(node.left, idx)
    else:
        return index_node(node.right, idx - node.weight)


def insert_node(root, index, s):
    left_root, right_root = split_node(root, index)
    mid_root = build_rope_from_string(s) if s else None
    merged = concat_nodes(left_root, mid_root)
    merged = concat_nodes(merged, right_root)
    return merged

def delete_node(root, index, length):
    if length <= 0:
        return root
    left_root, rest = split_node(root, index)
    new_left, right_after = split_node(rest, length)
    return concat_nodes(left_root, right_after)

def print_structure(root):
    leaf_counter = {"v": 1}
    def print_leaves(node):
        if node is None:
            return
        if node.is_leaf():
            print(f"Leaf {leaf_counter['v']}: {node.value}")
            leaf_counter['v'] += 1
        else:
            print_leaves(node.left)
            print_leaves(node.right)
    print_leaves(root)

    node_counter = {"v": 1}
    def print_internals(node):
        if node is None:
            return
        if not node.is_leaf():
            node.recalc()
            print(f"Node {node_counter['v']}: {node.weight}")
            node_counter['v'] += 1
            print_internals(node.left)
            print_internals(node.right)
    print_internals(root)

    def collect_text(node):
        if node is None:
            return ""
        if node.is_leaf():
            return node.value
        return collect_text(node.left) + collect_text(node.right)
    print(collect_text(root))

class Rope:
    def __init__(self, s=""):
        self.root = build_rope_from_string(s) if s else None

    def concat(self, other):
        r = Rope()
        r.root = concat_nodes(self.root, other.root)
        return r

    def split(self, index):
        left_root, right_root = split_node(self.root, index)
        left_rope = Rope(); right_rope = Rope()
        left_rope.root = left_root; right_rope.root = right_root
        return (left_rope, right_rope)

    def index(self, idx):
        return index_node(self.root, idx)

    def insert(self, index, s):
        self.root = insert_node(self.root, index, s)

    def delete(self, index, length):
        self.root = delete_node(self.root, index, length)

    def print_structure(self):
        print_structure(self.root)

    def tostring(self):
        def collect(node):
            if node is None:
                return ""
            if node.is_leaf():
                return node.value
            return collect(node.left) + collect(node.right)
        return collect(self.root)

def main():
    s = input().rstrip("\n")
    line2 = input()
    line3 = input().strip()

    if " " in line2:
        idx_str, insert_text = line2.split(" ", 1)
    else:
        idx_str = line2.strip()
        insert_text = ""
    insert_idx = int(idx_str)
    del_idx, del_len = map(int, line3.split())

    rope = Rope(s)
    rope.print_structure()

    rope.insert(insert_idx, insert_text)
    rope.print_structure()

    rope.delete(del_idx, del_len)
    rope.print_structure()

if __name__ == "__main__":
    main()

