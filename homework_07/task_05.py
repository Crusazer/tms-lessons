import json

with open("file_04.json", "r") as file:
    person = json.load(file)
    print(person[1], person[0], person[2])
