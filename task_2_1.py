test_string = '''this '' is "test" string'''


def replacer(string):
    return string.translate(string.maketrans({"'": "\"", "\"": "'"}))


print(replacer(test_string))
