# Напишите функцию get_natural_numbers, которое принимает целое число n и
# возвращает список натуральных чисел от 1 до n включительно. Используйте генераторы списков.

def get_natural_number(n: int):
    return [i for i in range(1, n + 1)]


print(get_natural_number(10))
