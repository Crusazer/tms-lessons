from functools import reduce


def my_join(sequence: str, sep: str):
    return reduce(lambda w, x: w + sep + x, sequence.split())


assert my_join("hello this is my string", '@') == "hello@this@is@my@string"

string = input()
separator = input()
print(my_join(string, separator))
