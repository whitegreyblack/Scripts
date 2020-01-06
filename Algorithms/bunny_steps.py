# a rabbit can hop one step or two steps at a time , given N steps how many combinations are possible

def fib(n):
    if n == 0 or n == 1:
        return 1
    return fib(n-1) + fib(n-2)

'''
1 -> [
    1
]
2 -> [
    1, 1
    2
]
3 -> [
    1, 1, 1
    1, 2
    2, 1
]
4 -> [
    1, 1, 1, 1
    1, 1, 2
    1, 2, 1
    2, 1, 1
    2, 2
]
5 -> [
    1, 1, 1, 1, 1
    1, 1, 1, 2
    1, 1, 2, 1
    1, 2, 1, 1
    2, 1, 1, 1
    1, 2, 2
    2, 1, 2
    2, 2, 1
]
'''


if __name__ == '__main__':
    for i in range(1, 6):
        print(fib(i))