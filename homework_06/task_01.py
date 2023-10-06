def map_to_tuples(sequence):
    return [(i.upper(), i.lower()) for i in sequence]


def map_to_tuples2(sequence):
    return list(map(lambda x: (x.upper(), x.lower()), sequence))


string = list(input().split())
print(map_to_tuples(string))
print(map_to_tuples2(string))
