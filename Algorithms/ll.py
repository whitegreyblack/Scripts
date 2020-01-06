# ll.py

import random

from node import Node


def build(chars: list) -> object:
    head = None
    for cs in chars:
        if not head:
            head = Node(cs)
            continue
        n = head
        prev = None
        while n:
            prev = n
            n = n.next
        prev.next = Node(cs)
    return head

def to_string(head, joiner="") -> str:
    if has_cycle(head):
        return "Detected cycle: cannot iterate until cycle prevention is implemented"
    l = []
    n = head
    while n:
        l.append(n.data)
        n = n.next
    return joiner.join(l)

def get_mid_node(head: object) -> object:
    if not head:
        return
    slow, fast = head, head
    while fast and fast.next:
        fast = fast.next.next
        slow = slow.next
    return slow

""" `reversing a singly linked list`
LL(head):
 |
 V
+----------+    +----------+
| N1       |    | N2       |
| data: a  |    | data: b  |
| next: N2 | -> | next: N3 |
+----------+    +----------+

0. init prev             | prev = None
1. set head to curr      | curr = head 
1.a. loop                | while curr is not None
    2. save curr.next        | next = curr.next
    2. set curr.next to prev | curr.next = prev
    3. set prev to curr      | prev = curr
    4. set curr to next      | curr = next
"""

def reverse(head: object) -> object:
    prev = None
    curr = head
    while curr:
        # curr.data = curr.data[::-1]
        next = curr.next
        curr.next = prev
        prev = curr
        curr = next
    head = prev
    return head

def is_palindrome(head: object) -> bool:
    n = reverse(get_mid_node(head))
    m = head
    print(to_string(m), m)
    print(to_string(n), n)
    while n:
        if not m.data == n.data:
            return False
        m = m.next
        n = n.next
    return True

def has_cycle(head: object) -> bool:
    if head == None:
        return False

    fast = head.next
    slow = head

    while fast is not None and fast.next is not None and slow is not None:
        if fast == slow:
            return True
        fast = fast.next.next
        slow = slow.next
    return False

def sort_single(head: object) -> object:
    if not head:
        return head
    
    return head

if __name__ == "__main__":
    # head = build(('a', 'bc', 'd', 'ef', 'g'))
    # print(is_palindrome(head))
    # print("has cylce", has_cycle(head))
    # dead = build(('a', 'b', 'c', 'b', 'a'))
    # print(is_palindrome(dead))
    # mead = build(('a', 'b', 'c', 'c', 'b', 'a'))
    # print(is_palindrome(mead))
    # lead = reverse(build(('a', 'bc', 'd', 'ef', 'g')))
    # print(to_string(lead))

    # lead.next.next.next.next.next = lead.next
    # print(has_cycle(lead))
    # print(to_string(lead))

    numbers = [str(i) for i in range(10)]
    random.shuffle(numbers)
    head = build(numbers)
    print(to_string(head))
