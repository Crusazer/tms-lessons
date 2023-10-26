import csv


def get_person() -> tuple:
    first_name = input("Enter name: ")
    second_name = input("Enter surname: ")
    age = input("Enter your gender: ")
    return first_name, second_name, age


with open("file_07.csv", "w") as file:
    writer = csv.writer(file)
    writer.writerow(("Name", "Surname", "Gender"))
    writer.writerow(get_person())
