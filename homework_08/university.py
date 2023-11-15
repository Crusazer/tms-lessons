from student import Student


def calc_sum_scholarship(students: list[Student] | tuple[Student]) -> int:
    return sum(student.get_scholarship() for student in students)


def get_excellent_student_count(students: list[Student] | tuple[Student]) -> int:
    return sum(student.is_excellent() for student in students)


if __name__ == "__main__":
    students = [
        Student("Max", 9.2),
        Student("Alex", 6.3),
        Student("Wadim", 7.2),
        Student("Andrey", 3.8),
        Student("Denis", 9)
    ]

    print(f"The summ scholarship: {calc_sum_scholarship(students)}")
    print(f"Excellent_student_count: {get_excellent_student_count(students)}")
