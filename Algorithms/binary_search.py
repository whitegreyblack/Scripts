'''Binary Search using list of squares
Performance Worst  : O(log n) 
Performance Best   : O(1)      
Performance Average: O(log n) 
Space Worst Case   : O(1)
'''
import click
import utility

def binary_search(numbers: list, number:int) -> bool:
    left, right = 0, len(numbers) - 1
    while left < right:
        middle = (left + right) // 2
        if numbers[middle] is number:
            return True
        elif numbers[middle] < number:
            left = middle + 1
        else:
            right = middle - 1
    return False

@click.command()
@click.argument('number', type=click.INT)
def main(number: int) -> None:
    numbers = utility.squares()
    print(f"Searching for {number} among a list of squares from 1-9.")
    print(f"This example uses a sorted data list.")
    found = binary_search(numbers, number)
    print(f"{number} was found: {found}")

if __name__ == "__main__":
    main()
