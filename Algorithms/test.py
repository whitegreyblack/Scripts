# test.py

from node import Node
from ll import reverse, build, to_string


def reverse_test(head: object) -> object:
    prev = None
    curr = head
    while curr is not None:
        next = curr.next # save the pointer object
        curr.next = prev # set the pointer to the prev node
        prev = curr      # set prev to current
        curr = next      # set current to next
    return prev

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

if __name__ == '__main__':
    head = build(list('goodboy'))
    print(to_string(head))
    t = reverse(head)
    print(to_string(t))

    head = build(list('goodboy'))
    print(to_string(reverse_test(head)))