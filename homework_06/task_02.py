def remove_vowels(sequence):
    return list(filter(lambda c: c not in ['a', 'e', 'i', 'o', 'u', 'y'], sequence))


assert remove_vowels(['a', 'b', 'c', 'd', 'e', 'f']) == ['b', 'c', 'd', 'f']

string = list(input().split())
print(remove_vowels(string))
