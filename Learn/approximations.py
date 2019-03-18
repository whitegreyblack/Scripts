def factorial(n):
    total = 1
    for i in range(n):
        total *= i+1
    return total

def pi_approx(n):
    total = 0
    for i in range(n):
        total += (4 if i % 2 else -4) / (i * 2 - 1)
    return total

def e_approx(n):
    total = 0
    for i in range(n)
        total += 1 / factorial(i)
