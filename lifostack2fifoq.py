'''
Create a LIFO stack using only FIFO queues
I: 0 1 2 3 4 5
O: 5 4 3 2 1 0
'''

class Queue:
    def __init__(self):
        self.q = []
    
    def push(self, x):
        self.q.append(x)

    def pop(self):
        return self.q.pop(0)

    def top(self):
        return self.q[0]

    @property
    def empty(self):
        return not self.q

class Stack:
    def __init__(self):
        self.first = Queue()
        self.second = Queue()

    def push(self, x):
        if not self.first.q and not self.second.q:            
            self.first.push(x)
        elif self.first.q:
            self.first.push(x)
        else:
            self.second.push(x)
        print(self.first.q, self.second.q)

    def pop(self):
        if not self.first.q and not self.second.q:
            return
        elif not self.second.q:
            while len(self.first.q) != 1:
                self.second.push(self.first.pop())
            val = self.first.pop()
        else:
            while len(self.second.q) != 1:
                self.first.push(self.second.pop())
            val = self.second.pop()
        return val


if __name__ == "__main__":
    q = Queue()
    for i in range(5):
        q.push(i)
    for _ in range(5):
        print(q.pop())

    s = Stack()
    for i in range(5):
        s.push(i)
    for _ in range(4):
        print(s.pop())

    for i in range(5):
        s.push(i)
    for _ in range(5):
        print(s.pop())