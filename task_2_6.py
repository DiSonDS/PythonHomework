test_string = "This is test \n string \t testes\nsetset"


def get_longest_word(string):
    words = string.split()
    return max(words, key=len)


print(get_longest_word(test_string))
