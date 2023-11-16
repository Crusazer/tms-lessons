import re


def is_float_number(text: str) -> bool:
    assert text is not str, "Function is_float_number got not string"
    regex = r"-?\d+\.\d+"
    return re.fullmatch(regex, text) is not None


if __name__ == "__main__":
    assert is_float_number("12.0") is True
    assert is_float_number("1.123123") is True
    assert is_float_number("12123.03456563") is True
    assert is_float_number("-23.03") is True

    assert is_float_number("12123") is False
    assert is_float_number("121_23") is False
    assert is_float_number(".03456563") is False
    assert is_float_number("12123.") is False
    assert is_float_number("12123.aa") is False
    assert is_float_number("aa.1231") is False
    assert is_float_number("1 123.1231") is False
