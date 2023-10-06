# Напишите функцию filter_odd_numbers, которая принимает на вход список целых чисел и возвращает новый список,
# состоящий из элементов первоначального, но без нечётных чисел.

def filter_odd_numbers(numbers: list[int]):
    return [i for i in numbers if i % 2 != 0]


print(filter_odd_numbers([1, 2, 3, 4, 5, 6, 7]))
