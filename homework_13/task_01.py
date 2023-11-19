import sqlite3
import re


class DataBase:
    """ A class for interacting with a database """

    def __init__(self, file_path: str):
        self.__connection = sqlite3.connect(file_path)
        self.__connection.execute("""CREATE TABLE IF NOT EXISTS contacts(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(50),
        number VARCHAR(20));""")

    def add_new_contact(self, contact: dict):
        self.__connection.execute("""INSERT INTO contacts (name, number) 
                                    VALUES(?, ?)""", (contact["name"], contact["phone_number"]))
        self.__connection.commit()

    def update_contact(self, contact: dict):
        self.__connection.execute("""UPDATE  contacts 
        SET number = ?
        WHERE name = ?;""", (contact["phone_number"], contact["name"]))
        self.__connection.commit()

    def get_all_contacts(self) -> tuple:
        cursor = self.__connection.execute("""SELECT name, number FROM contacts""")
        all_contacts = cursor.fetchall()
        return tuple({"name": i[0], "phone_number": i[1]} for i in all_contacts)

    def __del__(self):
        self.__connection.close()


class PhoneBook:
    def __init__(self, path_to_database: str):
        self.db = DataBase(path_to_database)

    @staticmethod
    def check_number(phone_number: str) -> bool:
        print(phone_number)
        regex = r"\+\d{3} \((29|25|33|44)\) \d{3}-\d{2}-\d{2}"
        return re.fullmatch(regex, phone_number) is not None

    def __get_contact_from_user(self) -> dict:
        name = input("Введите имя контакта: ")
        phone_number = input("Введите номер телефона в виде '+*** (**) ***-**-**': ")

        while self.check_number(phone_number) is False:
            phone_number = input(
                "Вы ввели некорректный номер телефона! Пример корректного номер: +375 (29) 111-11-11.\n"
                "Попробуйте снова: ")

        return {"name": name, "phone_number": phone_number}

    def __create_new_contact(self):
        contact = self.__get_contact_from_user()
        self.db.add_new_contact(contact)
        print("Новый контакт создан.\n")

    def __print__all_order_contacts(self):
        contacts = self.db.get_all_contacts()
        print("Ваш список контактов:\n")
        for contact in contacts:
            print(f"Имя: {contact['name']}\nНомер телефона: {contact['phone_number']}\n")

    def __update_contact_number(self):
        contact = self.__get_contact_from_user()
        self.db.update_contact(contact)
        print("Контакт обновлён.\n")

    def run(self):
        choice = None

        while True:
            print(f"Выберите действие:\n"
                  f"0. Выйти из программы\n"
                  f"1. Добавить новый контакт\n"
                  f"2. Вывести весь список контактов в алфавитном порядке.\n"
                  f"3. Обновить номер контакта\n")

            try:
                choice = int(input())
            except ValueError:
                print("Вы ввели некорректные данные, попробуйте снова!")

            match choice:
                # Завершить программу
                case 0:
                    print("До свидания")
                    return
                case 1:
                    # Создание нового контакта
                    self.__create_new_contact()
                case 2:
                    # Вывод на экран всех контактов из базы данных
                    self.__print__all_order_contacts()
                case 3:
                    # Обновление контакта в базе данных
                    self.__update_contact_number()


if __name__ == "__main__":
    book = PhoneBook("contacts.db")
    book.run()
