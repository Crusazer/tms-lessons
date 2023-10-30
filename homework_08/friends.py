from person import Person

from functools import reduce


def get_oldest_person(friends: list[Person] | tuple[Person]):
    if friends:
        oldest_friend = reduce(lambda x, y: x if x.age > y.age else y, friends)
        oldest_friend.print_person_info()


def filter_male_person(friends: list[Person] | tuple[Person]):
    [friend.print_person_info() for friend in friends if friend.gender == "M"]


if __name__ == "__main__":
    my_friends = [
        Person("Max", 25, "M"),
        Person("Masha", 29, "F"),
        Person("Maria", 18, "F"),
        Person("Wadim", 35, "M"),
        Person("Sergey", 15, "M")
    ]

    # Print all my friends
    [friend.print_person_info() for friend in my_friends]

    # Print the oldest my friend
    print("The oldest Person: ")
    get_oldest_person(my_friends)

    # Print all my male friends
    print("male Persons: ")
    filter_male_person(my_friends)
