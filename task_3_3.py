test_string = "This is test string"


def count_letters(string):
    return {letter: string.count(letter) for letter in set(string)}


print(count_letters(test_string))
