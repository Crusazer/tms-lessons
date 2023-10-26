import json

person = {"first_name": "Max", "seconds_name": "Gotovchikov", "age": 25}

with open("file_03.json", "w") as file:
    json.dump(person, file)
