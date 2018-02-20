'''
Create a FIFO queue using only LIFO stacks
I: 0 1 2 3 4 5
O: 0 1 2 3 4 5
'''

class Stack:
    def __init__(self):
        self.stack = []

    def __str__(self):
        return f'{self.__class__.__name__}: {str(self.stack)}'

    @property
    def top(self):
        return self.stack[-1]

    def push(self, x):
        self.stack.append(x)

    def pop(self):
        return self.stack.pop(-1)

    def clear(self):
        self.stack = []

    @property
    def empty(self):
        return len(self.stack) == 0

class Queue:
    def __init__(self):
        self.first = Stack()
        self.second = Stack()

    @property
    def top(self):
        return self.first.stack[-1]

    def push(self, x):
        self.first.push(x)
    
    def pop(self):
        if self.first.empty and self.second.empty:
            return
        elif self.second.empty:
            while len(self.first.stack) != 1:
                self.second.push(self.first.stack.pop())
            value = self.first.stack.pop()
        else:
            while len(self.second.stack) != 1:
                self.first.push(self.first.stack.pop())
            value = self.first.stack.pop()

if __name__ == "__main__":
    q = Queue()
    for i in range(5):
        q.push(i)
    
    for i in range(5):
        print(q.pop())
