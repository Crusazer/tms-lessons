from __future__ import annotations
from math import gcd


class Rational:
    """ This class is a rational number. For example, 2/3 """

    def __init__(self, numerator: int, denominator: int):
        assert isinstance(numerator, int) and isinstance(denominator, int), "Arguments must be int"
        assert denominator != 0, "Denominator cannot be a zero"
        self.__numerator = numerator
        self.__denominator = denominator
        self.__normalise()

    @property
    def numerator(self) -> int:
        return self.__numerator

    @property
    def denominator(self) -> int:
        return self.__denominator

    def __normalise(self):
        """ Normalise a rational number. For example: 5 / -10 = -1 / 2"""
        greatest_common_divisor = gcd(self.__numerator, self.__denominator)
        self.__numerator //= greatest_common_divisor
        self.__denominator //= greatest_common_divisor

        # Only numerator can be lass then zero
        if self.__denominator < 0:
            self.__numerator *= -1
            self.__denominator *= -1

    def __str__(self) -> str:
        return f"{self.__numerator} / {self.__denominator}"

    def __mul__(self, other: Rational) -> Rational:
        assert isinstance(other, Rational), "Can only multiply by Rational"
        # When will call constructor number will be normalised
        return Rational(self.__numerator * other.__numerator, self.__denominator * other.__denominator)

    def __truediv__(self, other: Rational) -> Rational:
        assert isinstance(other, Rational), "Can only divide by Rational"
        return Rational(self.__numerator * other.__denominator, self.__denominator * other.__numerator)

    def __add__(self, other: Rational) -> Rational:
        assert isinstance(other, Rational), "Can only add by Rational"
        numerator = self.__numerator * other.__denominator + self.__denominator * other.__numerator
        denominator = self.__denominator * other.__denominator
        return Rational(numerator, denominator)

    def __sub__(self, other: Rational) -> Rational:
        assert isinstance(other, Rational), "Can only sub by Rational"
        numerator = self.__numerator * other.__denominator - self.__denominator * other.__numerator
        denominator = self.__denominator * other.__denominator
        return Rational(numerator, denominator)

    def __eq__(self, other: Rational) -> bool:
        """ All Rational number normalised therefor equal rational numbers have equal numerator and denominator"""
        assert isinstance(other, Rational), "Can only equal by Rational"
        return self.__numerator == other.__numerator and self.__denominator == other.__denominator

    def __ne__(self, other: Rational) -> bool:
        return not self == other

    def __lt__(self, other: Rational) -> bool:
        assert isinstance(other, Rational), "Only rational numbers can be compared"
        return self.__numerator * other.__denominator < self.__denominator * other.__numerator

    def __le__(self, other: Rational) -> bool:
        assert isinstance(other, Rational), "Only rational numbers can be compared"
        return self.__numerator * other.__denominator <= self.__denominator * other.__numerator

    def __gt__(self, other: Rational) -> bool:
        assert isinstance(other, Rational), "Only rational numbers can be compared"
        return self.__numerator * other.__denominator > self.__denominator * other.__numerator

    def __ge__(self, other: Rational) -> bool:
        assert isinstance(other, Rational), "Only rational numbers can be compared"
        return self.__numerator * other.__denominator >= self.__denominator * other.__numerator


if __name__ == '__main__':
    first = Rational(2, 5)
    second = Rational(2, 7)

    assert str(first) == "2 / 5"
    assert first / second == Rational(7, 5)
    assert first * second == Rational(4, 35)
    assert first + second == Rational(24, 35)
    assert first - second == Rational(4, 35)

    assert Rational(8, 32) == Rational(1, 4)
    assert Rational(9, 32) != Rational(1, 4)

    assert Rational(2, 7) < Rational(2, 5)
    assert Rational(2, 7) <= Rational(2, 5)
    assert Rational(2, 7) <= Rational(2, 7)

    assert Rational(2, 5) > Rational(2, 7)
    assert Rational(2, 5) >= Rational(2, 7)
    assert Rational(2, 7) >= Rational(2, 7)

    assert Rational(-1, -2) == Rational(1, 2)
    assert Rational(1, -2) == Rational(-1, 2)

    num1 = Rational(1, 4)
    num2 = Rational(3, 2)
    num4 = Rational(156, 100)
    num3 = Rational(1, 8)
    assert num1 * (num2 + num3) + num4 == Rational(1573, 800)
