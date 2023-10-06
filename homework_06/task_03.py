def remove_vowels(sequence):
    return list(filter(lambda c: c.lower() not in ['a', 'e', 'i', 'o', 'u', 'y'], sequence))


assert remove_vowels(['a', 'B', 'c', 'd', 'E', 'F']) == ['B', 'c', 'd', 'F']

string = list(input().split())
print(remove_vowels(string))
