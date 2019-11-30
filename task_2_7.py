import math

test_numbers = [1, 3, 2, 6]


def foo(numbers):
    prod = math.prod(numbers)
    return [prod // number for number in numbers]


print(foo(test_numbers))
