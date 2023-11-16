import re


def is_date(date: str) -> bool:
    assert date is not str, "Function is_date got not string"
    regex = r"\d\d-\d\d-\d{4}"
    return re.fullmatch(regex, date) is not None


if __name__ == "__main__":
    assert is_date("12-12-2023") is True
    assert is_date("123-12-1234") is False
    assert is_date("12_12-1234") is False
    assert is_date("Aa-12-1234") is False
    assert is_date("12-12-1234123") is False
    assert is_date("1-12-1234") is False
    assert is_date("11-12-1234 123") is False
