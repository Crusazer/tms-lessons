import csv

with open("file_07.csv", "r") as file:
    data = csv.reader(file, delimiter=',')
    j = 0
    for row in data:
        if j != 0:
            print(row[1], row[0], row[2])
        j += 1
