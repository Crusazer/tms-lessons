import re


def is_car_number(number: str) -> bool:
    regex = r"\d{4}[A-Z]{2}-\d"
    return re.fullmatch(regex, number) is not None


def is_phone_number(phone_number: str) -> str:
    regex = r"\+\d{3} \((29|25|33|44)\) \d{3}-\d{2}-\d{2}"
    return re.fullmatch(regex, phone_number) is not None


if __name__ == "__main__":
    assert is_car_number("1234AZ-1") is True
    assert is_car_number("1AD4AZ-1") is False
    assert is_car_number("11111Z11") is False

    assert is_phone_number("+375 (44) 123-45-67") is True
    assert is_phone_number("+375 (24) 123-45-67") is False
    assert is_phone_number("+375 144) 123-45-67") is False
    assert is_phone_number("+375 (4) 123-45-67") is False
    assert is_phone_number("+375 (44)123-45-67") is False
    assert is_phone_number("+375 (44) 12A-45-67") is False

