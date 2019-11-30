import string as s

test_strings = ["this", "is", "test", "string"]
test_strings2 = ["qwer", "zxc", "tyu", "yuio"]


def test_3_1_1(*strings):
    set_list = [set(string) for string in strings]
    return set.intersection(*set_list)


def test_3_1_2(*strings):
    return set(''.join(strings))


def test_3_1_3(*strings):
    set_list = [set(string) for string in strings]
    characters = set()
    for i, string1 in enumerate(set_list):
        for string2 in set_list[i+1:]:
            if string1.intersection(string2):
                characters.update(string1.intersection(string2))

    return characters


def test_3_1_4(*strings):
    set_strings = set()
    alphabet = set(s.ascii_lowercase)
    for string in strings:
        set_strings.update(set(string))
    return alphabet.difference(set_strings)


print(test_3_1_1(*test_strings))
print(test_3_1_2(*test_strings))
print(test_3_1_3(*test_strings))
print(test_3_1_4(*test_strings))
