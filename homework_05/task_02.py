def generate_natural_cubes(n: int) -> list:
    if n < 1:
        return []
    return [i ** 3 for i in range(1, n + 1)]


assert generate_natural_cubes(2) == [1, 8]         # Test 1
assert generate_natural_cubes(0) == []             # Test 2
assert generate_natural_cubes(-3) == []            # Test 3
assert generate_natural_cubes(3) == [1, 8, 27]     # Test 4

