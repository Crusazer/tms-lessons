import openpyxl

wb = openpyxl.Workbook()

sheet = wb.active
sheet['A1'] = "Name"
sheet['B1'] = "Surname"
sheet['C1'] = "Gender"
sheet['A2'] = "Max"
sheet['B2'] = "Gotovchikov"
sheet['C2'] = "M"

wb.save("file_09.xlsx")
