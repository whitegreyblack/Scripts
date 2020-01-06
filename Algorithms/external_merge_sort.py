# external_merge_sort.py

import random

# creates a file that is 7_888_890 bytes or 7704 kb
def write_numbers_to_file(name='unsorted.txt', numbers=None):
    if not numbers:
        numbers = list(get_numbers(1_000))
    random.shuffle(numbers)
    with open(name, 'w') as f:
        for num in numbers:
            f.write(f'{num}\n')

def sort(size:int=1_024):
    '''Sorts using filesystem with a given max_buffer size'''
    ...

def get_numbers(size:int=1_000_000):
    '''Helper function'''
    for i in range(size):
        yield str(i)

if __name__ == '__main__':
    numbers = get_numbers(1_000)
    write_numbers_to_file()
    # assuming 1kb or 1024b we pull 64 numbers max per read
    # for size in range(1, 64 +1):
    with open('unsorted.txt', 'r') as f:
        dat = f.read(1024)
        data = dat.split('\n')
        print(dat, len(dat))
        print(len(data))
