# merge_ll.py

"""Merge two sorted linked lists"""

from node import Node
from build_ll import build, string


def merge(a, b):
    """
        a - pointer to head of list a
        b - pointer to head of list b
    """
    # checks first elements since whichever is lower will be used
    # as the master linked list with a pointer saved to the first element.
    if a.data > b.data:
       a, b = b, a
    head = a
    # using only the lists themselves to save space
    # reorder the node pointers in-place
    # the first element in a is known to be smaller than b. set a.next.
    while a.next:
        if a.next.data > b.data:
            a.next, b = b, a.next
        a = a.next
    # add the rest of b to a. does not matter if b is empty or not.
    a.next = b
    return head

if __name__ == "__main__":
    a = build(1, 5, 7, 9)
    b = build(2, 4, 8, 12)

    v1 = string(a)
    v2 = string(b)
    print(v1, v2)
    assert v1 == "1579" and v2 == "24812"

    c = merge(a, b)
    v3 = string(c)
    print(v3) 
    assert v3 == "124578912"

