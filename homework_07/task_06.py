import csv

row1 = ("name", "surname", "gender")
row2 = ("Max", "Gotovchikov", "M")

with open("file_06.csv", "w") as file:
    writer = csv.writer(file, delimiter=',')
    writer.writerow(row1)
    writer.writerow(row2)
