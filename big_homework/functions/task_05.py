def filter_negative_numbers(numbers: list) -> list:
    return [x for x in numbers if x >= 0]


assert filter_negative_numbers([6, -5, 0, -1, 100]) == [6, 0, 100]

