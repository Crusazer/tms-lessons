from __future__ import annotations  # For annotation (point: Point) in class Point


class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def distance_to_zero(self) -> float:
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def distance_to_point(self, point: Point) -> float:
        return ((point.x - self.x) ** 2 + (point.y - self.y) ** 2) ** 0.5

    # def distance_to_point(self, point: Point) -> float:
    #    new_vector = Point(point.x - self.x, point.y - self.y)
    #    return new_vector.distance_to_zero()


p1 = Point(3, 4)
p2 = Point(3, 10)
p3 = Point(10, 10)

print('Distance between p1 and zero point:', p1.distance_to_zero())
print('Distance between p2 and zero point:', p2.distance_to_zero())
print('Distance between p3 and zero point:', p3.distance_to_zero())
print('Distance between p1 and p1:', p1.distance_to_point(p1))
print('Distance between p1 and p2:', p1.distance_to_point(p2))
print('Distance between p2 and p1:', p2.distance_to_point(p1))
print('Distance between p1 and p3:', p1.distance_to_point(p3))
print('Distance between p2 and p3:', p2.distance_to_point(p3))
