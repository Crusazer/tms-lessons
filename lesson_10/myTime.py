from __future__ import annotations  # For annotation (point: Point) in class Point


class MyTime:
    def __init__(self, seconds: float | int):
        self.seconds: float = seconds

    @property
    def hours(self) -> int:
        return int(self.seconds // 3600)

    @property
    def minutes(self) -> int:
        return int(self.seconds // 60) % 60

    def __mul__(self, other: int):
        assert isinstance(other, int), "You can only multiply by an integer!"
        return MyTime(self.seconds * other)

    def __truediv__(self, other: int):
        assert isinstance(other, int), "You can only div by an integer!"
        return MyTime(self.seconds / other)

    def __floordiv__(self, other: int):
        assert isinstance(other, int), "You can only multiply by an integer!"
        return MyTime(self.seconds // other)

    def __add__(self, other: MyTime):
        assert isinstance(other, MyTime), "You can only add by an integer or MyTime class!"
        return MyTime(self.seconds + other.seconds)

    def __sub__(self, other: MyTime):
        assert isinstance(other, MyTime), "You can only sub by an integer or MyTime class!"
        return MyTime(self.seconds - other.seconds)

    def __str__(self):
        return f"{self.seconds}s"

    def __eq__(self, other: MyTime) -> bool:
        assert isinstance(other, MyTime), "Only time can be compared"
        return self.seconds == other.seconds

    def __ne__(self, other: MyTime) -> bool:
        assert isinstance(other, MyTime), "Only time can be compared"
        return self.seconds != other.seconds

    def __lt__(self, other: MyTime) -> bool:
        assert isinstance(other, MyTime), "Only time can be compared"
        return self.seconds < other.seconds

    def __gt__(self, other: MyTime) -> bool:
        assert isinstance(other, MyTime), "Only time can be compared"
        return self.seconds > other.seconds

    def __le__(self, other: MyTime) -> bool:
        assert isinstance(other, MyTime), "Only time can be compared"
        return self.seconds <= other.seconds

    def __ge__(self, other: MyTime) -> bool:
        assert isinstance(other, MyTime), "Only time can be compared"
        return self.seconds >= other.seconds

    def get_formatted_str(self):
        return f"{self.hours:02}:{self.minutes:02}:{self.seconds % 60:04.1f}"


class MyTimeInterval:
    def __init__(self, start_seconds: MyTime | int, finish_seconds: MyTime | int):
        assert (isinstance(start_seconds, int | MyTime) and
                isinstance(finish_seconds, int | MyTime)), "Only int or MyTime"
        if isinstance(start_seconds, int) and isinstance(finish_seconds, int):
            self.start = MyTime(start_seconds)
            self.finish = MyTime(finish_seconds)
        elif isinstance(start_seconds, MyTime) and isinstance(finish_seconds, MyTime):
            self.start = start_seconds
            self.finish = finish_seconds

    def is_inside(self, time: MyTime) -> bool:
        assert isinstance(time, MyTime), "time_interval must been MyTime object"
        return self.start <= time <= self.finish

    def intersects(self, time_interval: MyTimeInterval) -> bool:
        assert isinstance(time_interval, MyTimeInterval), "time_interval must been MyTimeInterval object"
        return (self.is_inside(time_interval.start) or self.is_inside(time_interval.finish) or
                time_interval.is_inside(self.start) or time_interval.is_inside(self.finish))


if __name__ == "__main__":
    my_time_5 = MyTime(5)
    my_time_10 = MyTime(10)
    my_time_15 = MyTime(15)
    assert my_time_10 * 2 == MyTime(20)
    assert my_time_10 / 2 == my_time_5
    assert my_time_10 + my_time_5 == my_time_15
    assert my_time_10 - my_time_5 == my_time_5
    assert my_time_10 != my_time_5
    assert my_time_10 > my_time_5
    assert my_time_5 < my_time_10
    assert my_time_10 <= my_time_10
    assert my_time_10 >= my_time_10

    first = MyTimeInterval(MyTime(5), MyTime(10))
    second = MyTimeInterval(MyTime(7), MyTime(15))
    third = MyTimeInterval(MyTime(0), MyTime(5))
    assert first.intersects(second)
    assert first.intersects(third)
    assert first.intersects(MyTimeInterval(MyTime(50), MyTime(100))) is False

    time = MyTime(3724.5)
    assert time.hours == 1
    assert time.minutes == 2
    assert MyTime(10) * 2 == MyTime(20)
    assert MyTime(10) / 2 == MyTime(5)
    assert MyTime(2) + MyTime(2) == MyTime(4)
    assert MyTime(5) - MyTime(2) == MyTime(3)
    assert time.get_formatted_str() == '01:02:04.5'
    assert str(time) == '3724.5s'
    assert MyTime(10) < MyTime(11)
    assert MyTime(10) <= MyTime(11)
    assert MyTime(10) <= MyTime(10)
    assert MyTime(5) == MyTime(5)
    assert MyTime(5) != MyTime(3)
    assert MyTime(5) > MyTime(3)
    assert MyTime(5) >= MyTime(3)
    assert MyTime(5) >= MyTime(5)

    interval = MyTimeInterval(10, 20)
    assert interval.is_inside(MyTime(15))
    assert interval.is_inside(MyTime(10))
    assert interval.is_inside(MyTime(20))
    assert not interval.is_inside(MyTime(5))
    assert not interval.is_inside(MyTime(25))

    assert interval.intersects(MyTimeInterval(5, 15))
    assert interval.intersects(MyTimeInterval(5, 25))
    assert interval.intersects(MyTimeInterval(10, 25))
    assert interval.intersects(MyTimeInterval(11, 19))
    assert not interval.intersects(MyTimeInterval(0, 5))
    assert not interval.intersects(MyTimeInterval(25, 30))
