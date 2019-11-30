test_string = "This is test string      "


def my_split(string, char):
    start = 0
    new_list = []
    for i, symbol in enumerate(string):
        if symbol == char:
            new_list.append(string[start:i])
            start = i + 1
    new_list.append(string[start:])

    return new_list


print(my_split(test_string, " "))
print(test_string.split(" "))
