def my_decorator(func):
    def wrapper(value):
        print(f"Функция получила на вход значение {value}")
        result = func(value)
        print(f"Результат функции: {result}")
        return result

    return wrapper


@my_decorator
def my_func(x):
    return x ** 2


y = my_func(3)
print(f'y = {y}')
