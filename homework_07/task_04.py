import json


def get_person() -> tuple:
    first_name = input("Enter first name: ")
    second_name = input("Enter second name: ")
    age = input("Enter age: ")
    return first_name, second_name, age


if __name__ == "__main__":
    person = get_person()
    with open("file_04.json", "w") as file:
        json.dump(person, file)
