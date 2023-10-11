def simple_compare(a, b) -> bool:
    return a < b


assert simple_compare(1, 2) is True
assert simple_compare(2, 1) is False
assert simple_compare(1, 1) is False
