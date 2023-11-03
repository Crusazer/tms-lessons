import json
from random import randint


def get_random_digits(count: int):
    """ Returns a string of the specified length """
    return str(randint(10 ** (count - 1), 10 ** count - 1))


class BankAccount:
    def __init__(self, card_holder, money=0.0, card_number=None, account_number=None):
        self.card_holder = card_holder
        self.money = money
        self.card_number = card_number if card_number else get_random_digits(10)
        self.account_number = account_number if account_number else get_random_digits(20)


def convert_bank_account_to_dict(account: BankAccount) -> dict:
    """ convert BankAccount to dict """
    return {
        "card_holder": account.card_holder,
        "money": account.money,
        "card_number": account.card_number,
        "account_number": account.account_number
    }


def save_accounts(accounts: list[BankAccount], file_name: str):
    """ Save accounts to json file """
    with open(file_name, 'w') as file:
        json.dump([convert_bank_account_to_dict(acc) for acc in accounts], file, indent=4)


def load_accounts(file_name: str) -> dict[str, BankAccount]:
    try:
        with open(file_name, 'r') as file:
            accounts = json.load(file)
            return {account["account_number"]: BankAccount(**account) for account in accounts}
    except FileNotFoundError:
        return {}


class Bank:
    def __init__(self, bank_accounts: dict[str, BankAccount] = None):
        self.__bank_accounts: dict[str, BankAccount] = bank_accounts if bank_accounts else []

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
    controller = Controller("data.json")
    controller.run()
