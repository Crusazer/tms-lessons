my_dict = {'a': 1, 'b': 2, 'c': 3, 'd': 10, 'e': 1}

max_number = list(my_dict.values())[0]
max_key = list(my_dict.keys())[0]

for key, value in my_dict.items():
    if value > max_number:
        max_number = value
        max_key = key

print(max_key)
