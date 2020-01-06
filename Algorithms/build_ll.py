# build_ll.py

"""
    Given an iterable argument build a linked list with a single element from
    the iterable as the data for each node.
"""

from node import Node

def build(*args):
    head = None
    last = None
    while True:
        data, *args = args
        if head is None:
            head = Node(data)
            last = head
        else:
            last.next = Node(data)
            last = last.next
        if not args:
            break
    return head

def string(head):
    curr = head
    data = []
    while curr:
        data.append(curr.data)
        curr = curr.next
    return ''.join(str(d) for d in data)

if __name__ == '__main__':
    ll = build(1, 2, 3, 4)
    value = string(ll)
    print(value)
    assert value == "1234"

