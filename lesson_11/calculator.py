class CalculationExitException(Exception):
    pass


def input_int_number() -> int:
    while True:
        try:
            return int(input("Введите целое число: "))
        except ValueError as e:
            print(f"Ошибка {e}\nПопробуйте снова")


def calculate(left: int, right: int, operation: str) -> float | int:
    match operation:
        case '+':
            return left + right
        case '-':
            return left - right
        case '*':
            return left * right
        case '/':
            return left / right
        case '!':
            raise CalculationExitException
        case _:
            raise ValueError(f"f'Неподдерживаемая операция: {operation}'")


def main():
    while True:
        try:
            a = input_int_number()
            b = input_int_number()
            operator = input("Введите операцию (введите ! для выхода из программы): ")
            print(calculate(a, b, operator))
        except ZeroDivisionError or ValueError as e:
            print(f"Ошибка {e},", end='\n\n')
        except CalculationExitException:
            print("Программа завершена успешно!")
            break


if __name__ == "__main__":
    main()
