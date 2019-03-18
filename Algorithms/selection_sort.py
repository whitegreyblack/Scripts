# Selection Sort
#   Performance Worst   :- O(n**2)
#   Performance Best    :- O(n**2)
#   Performance Average :- O(n**2)

def selection_sort(nums):
    print(nums)
    for j in range(len(nums)):
        m = j
        for i in range(j+1, len(nums)):
            if nums[i] < nums[m]:
                m = i
        if m is not j:
            nums[j], nums[m] = nums[m], nums[j]
        print(nums)

selection_sort([9,4,2,42,1451,23313,2,5,6,3])
