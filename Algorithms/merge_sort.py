# merge_sort

import random


def sort(o: list):
    if len(o) < 2:
        return o
    m = len(o) // 2
    return merge(sort(o[:m]), 
                 sort(o[m:]))

def merge(l, r):
    n = []
    while l and r:
        if l[0] <= r[0]:
            n.append(l.pop(0))
        else:
            n.append(r.pop(0))
    if l:
        n += l
    if r:
        n += r
    return n

if __name__ == "__main__":
    numbers = [n for n in range(1_000)]
    random.shuffle(numbers)
    for i in sort(numbers):
        print(i)
