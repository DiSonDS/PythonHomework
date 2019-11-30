input_list1 = ['This', 'is', 'test', 'list']
input_list2 = [1, 2, 3, 4]
input_list3 = [1]


def get_pairs(input_list):
    return list(zip(input_list, input_list[1:]))


print(get_pairs(input_list1))
print(get_pairs(input_list2))
print(get_pairs(input_list3))
