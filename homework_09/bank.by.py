from functools import reduce
from random import randint


def get_random_digits(count: int):
    """ Returns a string of the specified length """
    return str(randint(10 ** (count - 1), 10 ** count - 1))


class BankAccount:
    def __init__(self, card_holder):
        self.card_holder = card_holder
        self.money = 0.0
        self.account_number = get_random_digits(20)
        self.curd_number = get_random_digits(10)


class Bank:
    def __init__(self):
        self.__bank_accounts: list[BankAccount] = []

    def open_account(self, card_holder: str) -> BankAccount:
        """ Create a new account """
        account = BankAccount(card_holder)
        self.__bank_accounts.append(account)
        return account

    def __get_account(self, account_number: str) -> BankAccount | None:
        """ Return account if exist else return None"""
        for account in self.__bank_accounts:
            if account_number == account.account_number:
                return account
        return None

    def get_all_bank_accounts(self) -> list[BankAccount]:
        """ Return all accounts in the bank """
        return self.__bank_accounts

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
    def __init__(self):
        self.bank = Bank()

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
                case 0:
                    print("До свидания")
                    return
                case 1:
                    card_holder = input("Введите держателя карты: ")
                    account = self.bank.open_account(card_holder)
                    print(f"Счёт {account.account_number} создан")
                case 2:
                    accounts = self.bank.get_all_bank_accounts()
                    for acc in accounts:
                        print(f"Счёт: {acc.account_number}\n"
                              f"   Остаток на счету: {acc.money}\n"
                              f"   Номер карты: {acc.curd_number}\n"
                              f"   Держатель карты: {acc.card_holder}")
                case 3:
                    number = input("Введите номер счёта: ")
                    money = float(input("Введите сумму денег: "))
                    self.bank.add_money(number, money)
                case 4:
                    from_curd_number = input("Введите номер счёта отправителя: ")
                    to_curd_number = input("Введите номер счёта получателя: ")
                    money = float(input("Введите сумму денег: "))
                    self.bank.transfer_money(from_curd_number, to_curd_number, money)
                case 5:
                    from_curd_number = input("Введите номер счёта отправителя: ")
                    external = input("Введите номер внешнего счета: ")
                    money = float(input("Введите сумму денег: "))
                    self.bank.external_transfer(from_curd_number, external, money)


if __name__ == '__main__':
    controller = Controller()
    controller.run()
