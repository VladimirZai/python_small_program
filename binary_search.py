import time


def decorator(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time() - start
        print(f'Time for result: {end} s')
        return result
    return wrapper


@decorator
def binary_search(my_list, item):
    low = 0
    high = len(my_list) - 1

    while low <= high:
        mid = (low + high) // 2
        guess = my_list[mid]
        if guess == item:
            return mid
        if guess > item:
            high = mid - 1
        else:
            low = mid + 1
    return None


size = int(input("Enter size list: "))
my_list = list(range(1, size))
number = int(input("Enter number which want search: "))

print(binary_search(my_list, number))
