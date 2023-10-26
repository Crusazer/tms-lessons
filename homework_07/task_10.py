import openpyxl


def get_person() -> tuple:
    first_name = input("Enter name: ")
    second_name = input("Enter surname: ")
    age = input("Enter your age: ")
    return first_name, second_name, age


wb = openpyxl.Workbook()

sheet = wb.active
sheet['A1'] = "Name"
sheet['B1'] = "Surname"
sheet['C1'] = "Age"

person = get_person()
sheet['A2'] = person[0]
sheet['B2'] = person[1]
sheet['C2'] = person[2]

wb.save("file_10.xlsx")
