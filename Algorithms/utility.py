'''Utility functions for sort and search functions'''

import random

def squares(n=9, randomized=False):
    numbers = [i * i for i in range(1, n)]
    if randomized:
        random.shuffle(numbers)
    return numbers
