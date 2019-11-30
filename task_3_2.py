
def generate_squares(number):
    return {number: number ** 2 for number in range(1, number + 1)}


print(generate_squares(5))
