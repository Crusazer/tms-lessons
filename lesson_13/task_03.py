import sqlite3


def get_all_people() -> list:
    with sqlite3.connect("sqlite.db") as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM user")
        return cur.fetchall()


def get_lest_age_people(age: int) -> list:
    with sqlite3.connect("sqlite.db") as conn:
        all_users = conn.execute("SELECT * FROM user WHERE age >= ? ORDER BY age", (age,))
        return all_users.fetchall()


if __name__ == "__main__":
    print(*get_all_people(), sep='\n')

    print("\n\n\n-----------------------------------------------------\n")

    choice_age = int(input("Enter age to find: "))
    print(*get_lest_age_people(choice_age),  sep='\n')
