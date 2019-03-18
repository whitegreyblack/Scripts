'''Insertion Sort
Performance Worst  : O(n^2) comparisons, swaps
Performance Best   : O(n^2) comparisons, O(1) swaps
Performance Average: O(n^2) comparisons, swaps
Space Worst Case   : O(n) total, O(1) auxillary
'''
import random
import utility

def insertion_sort(numbers):

    current = 1
    while current < len(numbers):
        temp = current
        while temp > 0 and numbers[temp-1] > numbers[temp]:
            numbers[temp], numbers[temp-1] = numbers[temp-1], numbers[temp]
            temp -= 1
        current += 1
    return numbers

def main() -> None:
    numbers = utility.squares(n=1000, randomized=True)
    print(f"Sorting a randomly generated shuffled list of squares from 1-9.")
    print(f"Numbers before sorting: {numbers}")
    insertion_sort(numbers)
    print(f"Numbers after sorting: {numbers}")

if __name__ == "__main__":
    main()
