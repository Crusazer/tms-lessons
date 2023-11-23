import sqlite3
from random import randint


def get_random_digits(count: int):
    """ Returns a string of the specified length """
    return str(randint(10 ** (count - 1), 10 ** count - 1))


class BankAccount:
    def __init__(self, card_holder, money=0.0, card_number=None, account_number=None):
        self.card_holder = card_holder
        self.money = money
        self.card_number = card_number if card_number else get_random_digits(10)
        self.account_number = account_number if account_number else str(get_random_digits(20))


def save_accounts(accounts: list[BankAccount], file_name: str):
    """ Save accounts to database"""
    with sqlite3.connect(file_name) as connection:
        """ Create table if note exist"""
        connection.execute("""CREATE TABLE IF NOT EXISTS accounts(
        card_holder VARCHAR(100),
        money FLOAT,
        card_number INTEGER,
        account_number VARCHAR(20) PRIMARY KEY);""")

        execute_string_for_update = f"""UPDATE accounts SET card_holder=?, money=?, card_number=?, account_number=? 
                            WHERE account_number=?"""
        execute_string_for_insert = """INSERT OR IGNORE INTO accounts (card_holder, money, card_number, account_number)
            VALUES (?, ?, ?, ?)"""

        for account in accounts:
            cursor = connection.execute(execute_string_for_update, (
                account.card_holder, account.money, account.card_number, account.account_number,
                account.account_number))

            cursor = connection.execute(execute_string_for_insert, (
                account.card_holder, account.money, account.card_number, account.account_number))

        # Save changes
        connection.commit()


def load_accounts(file_name: str) -> dict[str, BankAccount]:
    try:
        with sqlite3.connect(file_name) as connection:
            cursor = connection.execute("""SELECT * FROM accounts""")
            accounts = cursor.fetchall()
            return {account[3]: BankAccount(*account) for account in accounts} if accounts else {}

    except sqlite3.OperationalError:
        return {}


class Bank:
    def __init__(self, bank_accounts: dict[str, BankAccount] = None):
        self.__bank_accounts: dict[str, BankAccount] = bank_accounts if bank_accounts else {}

    def open_account(self, card_holder: str) -> BankAccount:
        """ Create a new account """
        account = BankAccount(card_holder)
        self.__bank_accounts[account.account_number] = account
        return account

    def __get_account(self, account_number: str) -> BankAccount | None:
        """ Return account if exist else return None"""
        return self.__bank_accounts.get(account_number)

    def get_all_bank_accounts(self) -> list[BankAccount]:
        """ Return all accounts in the bank """
        return list(self.__bank_accounts.values())

    def add_money(self, account_number: str, money: float | int):
        """ Add money to the bank account """
        if account := self.__get_account(account_number):
            account.money += money

    def transfer_money(self, from_account_number: str, to_account_number: str, money: float | int):
        """ Transfer money from account to other account """
        sender: BankAccount = self.__get_account(from_account_number)
        receiver: BankAccount = self.__get_account(to_account_number)

        if sender and receiver:
            sender.money -= money
            receiver.money += money

    def external_transfer(self, from_account_number: str, to_external_number: str, money: float | int):
        """ transfer money to other Bank """
        account = self.__get_account(from_account_number)
        account.money -= money
        print(f"Банк перевёл {money}$ с вашего счёта {from_account_number} на внешний счёт {to_external_number}")


class Controller:
    def __init__(self, data_file_name: str):
        self.data_file_name = data_file_name
        self.bank = Bank(load_accounts(data_file_name))

    def run(self):
        print("Здравствуйте, наш банк открылся!")
        while True:
            print(f"Выберите действие:\n"
                  f"0. Завершить программу\n"
                  f"1. Открыть новый счёт\n"
                  f"2. Просмотреть открытые счета\n"
                  f"3. Положить деньги на счёт\n"
                  f"4. Перевести деньги между счетами\n"
                  f"5. Совершить платёж")

            choice = int(input())

            match choice:
                # Завершить программу
                case 0:
                    save_accounts(self.bank.get_all_bank_accounts(), self.data_file_name)
                    print("До свидания")
                    return
                # Открыть новый счёт
                case 1:
                    card_holder = input("Введите держателя карты: ")
                    account = self.bank.open_account(card_holder)
                    print(f"Счёт {account.account_number} создан")
                # Посмотреть открытые счета
                case 2:
                    accounts = self.bank.get_all_bank_accounts()
                    for acc in accounts:
                        print(f"Счёт: {acc.account_number}\n"
                              f"   Остаток на счету: {acc.money}\n"
                              f"   Номер карты: {acc.card_number}\n"
                              f"   Держатель карты: {acc.card_holder}")
                # Положить деньги на счёт
                case 3:
                    number = input("Введите номер счёта: ")
                    money = float(input("Введите сумму денег: "))
                    self.bank.add_money(number, money)
                    print(f"Счёт пополнен на сумму {money}$")
                # Перевести деньги между счетами
                case 4:
                    from_curd_number = input("Введите номер счёта отправителя: ")
                    to_curd_number = input("Введите номер счёта получателя: ")
                    money = float(input("Введите сумму денег: "))
                    self.bank.transfer_money(from_curd_number, to_curd_number, money)
                    print(f"Деньги в сумму {money} переведены со счёта {from_curd_number} на счёт {to_curd_number}")
                # Совершить платёж
                case 5:
                    from_curd_number = input("Введите номер счёта отправителя: ")
                    external = input("Введите номер внешнего счета: ")
                    money = float(input("Введите сумму денег: "))
                    self.bank.external_transfer(from_curd_number, external, money)
                    print(f"Платёж на сумму {money} совершён!")


if __name__ == '__main__':
    controller = Controller("accounts.db")
    controller.run()
