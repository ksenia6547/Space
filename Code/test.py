from rope import *

def test_node_basic():
    n = Node(value="abcde")
    assert n.is_leaf()
    assert n.weight == 5
    assert n.height == 1
    print("PASSED")

def test_total_length_height():
    n1 = Node(value="abc")
    n2 = Node(value="defg")
    root = Node(left=n1, right=n2)
    assert total_length(root) == 7
    assert total_height(root) == 2
    print("PASSED")

def test_rotate_left_right():
    a = Node(value="a")
    b = Node(value="b")
    c = Node(value="c")
    left = Node(left=a, right=b)
    root = Node(left=left, right=c)

    rotated = rotate_right(root)
    assert rotated is not None
    assert total_length(rotated) == 3
    print("PASSED")

def test_balance_node():
    a = Node(value="aaa")
    b = Node(value="bbb")
    c = Node(value="ccc")
    root = Node(left=Node(left=a, right=b), right=c)
    balanced = balance_node(root)
    assert total_length(balanced) == 9
    print("PASSED")

def test_build_rope():
    s = "abcdefghij"
    rope = build_rope_from_string(s)
    assert total_length(rope) == len(s)
    print("PASSED")

def test_split_node():
    s = "abcdefgh"
    rope = build_rope_from_string(s)
    left, right = split_node(rope, 3)
    assert left is not None and right is not None
    assert total_length(left) + total_length(right) == len(s)
    print("PASSED")

def test_index_node():
    rope = build_rope_from_string("abcdef")
    assert index_node(rope, 0) == "a"
    assert index_node(rope, 5) == "f"
    try:
        index_node(rope, 6)
        assert False, "IndexError expected"
    except IndexError:
        pass
    print("PASSED")

def test_concat_nodes():
    a = build_rope_from_string("abc")
    b = build_rope_from_string("def")
    merged = concat_nodes(a, b)
    text = Rope()
    text.root = merged
    assert text.tostring() == "abcdef"
    print("PASSED")

def test_insert_node():
    rope = Rope("HelloWorld")
    rope.insert(5, "_")
    assert rope.tostring() == "Hello_World"
    rope.insert(0, "Start:")
    assert rope.tostring().startswith("Start:")
    print("PASSED")

def test_delete_node():
    rope = Rope("Hello_World")
    rope.delete(5, 1)
    assert rope.tostring() == "HelloWorld"
    rope.delete(0, 5)
    assert rope.tostring() == "World"
    print("PASSED")

def test_full():
    rope = Rope("This is text")
    rope.insert(4, "_not")
    rope.delete(0, 5)
    assert "not" in rope.tostring()
    print("PASSED")


if __name__ == "__main__":
    test_node_basic()
    test_total_length_height()
    test_rotate_left_right()
    test_balance_node()
    test_build_rope()
    test_split_node()
    test_index_node()
    test_concat_nodes()
    test_insert_node()
    test_delete_node()
    test_full()
    print("ALL TESTS PASSED")

