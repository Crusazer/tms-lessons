def generate_squares(*args: int) -> list:
    return [i ** 2 for i in args]


assert generate_squares(1, 2, 3) == [1, 4, 9]       # Test 1
assert generate_squares(-1, -2, -3) == [1, 4, 9]    # Test 2
assert generate_squares(2, 4, -5) == [4, 16, 25]    # Test 3
