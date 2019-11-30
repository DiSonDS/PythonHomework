test_string = "pythoniscool,isn'tit?"


def split_by_index(string, indexes):
    start = 0
    new_list = []
    max_i = len(string)
    for i in indexes:
        if i > max_i - 1 or i < 0:
            return ["No luck"]
        new_list.append(string[start:i])
        start = i
    new_list.append(string[start:])

    return new_list


print(split_by_index(test_string, [6, 8, 12, 13, 18]))
print(split_by_index(test_string, [-42]))
