def is_year_leap(year: int) -> bool:
    if year < 1582:
        return False
    if year % 400 == 0:
        return True
    if year % 100 == 0:
        return False
    if year % 4 == 0:
        return True
    return False


assert is_year_leap(2032) is True   # Test 1
assert is_year_leap(1804) is True   # Test 2
assert is_year_leap(1721) is False  # Test 3
assert is_year_leap(1900) is False  # Test 4
assert is_year_leap(16) is False    # Test 5

# В 1582 году римский папа Григорий XIII провёл реформу календаря.
# Чтобы средний календарный год лучше соответствовал солнечному,
# было решено изменить правило високосных годов.
# https://ru.wikipedia.org/wiki/Високосный_год