class Student:
    def __init__(self, full_name: str, agerage_mark: float):
        self.full_name = full_name
        self.agerage_mark = agerage_mark

    def get_scholarship(self):
        if self.agerage_mark < 6:
            return 60
        if self.agerage_mark < 8:
            return 80
        return 100

    def is_excellent(self):
        return self.agerage_mark >= 9
