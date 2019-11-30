dict1 = {'a': 100, 'b': 200}
dict2 = {'a': 200, 'b': 300}
dict3 = {'a': 300, 'b': 100}


def combine_dicts(*dicts):
    new_dict = {}
    for d in dicts:
        for k, v in d.items():
            new_dict[k] = new_dict.get(k, 0) + v

    return new_dict


print(combine_dicts(dict1, dict2))
print(combine_dicts(dict1, dict2, dict3))
