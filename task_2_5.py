test_number = 3455767567568


def get_digits(number):
    return tuple([int(n) for n in str(number)])


print(get_digits(test_number))
