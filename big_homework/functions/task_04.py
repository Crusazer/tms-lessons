def compare(a , b) -> int:
    if a < b:
        return -1
    if a > b:
        return 1
    return 0


assert compare(100, 200) == -1
assert compare(200, 100) == 1
assert compare(10, 10) == 0
