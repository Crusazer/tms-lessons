# Напишите функцию list_sum, которая принимает на вход список и возвращает
# сумму элементов списка. Использование встроенной функции sum запрещено.

def list_sum(lst: list):
    summ = 0
    for i in lst:
        summ += i
    return summ


assert list_sum([1, 2, 3, 4, 5]) == 15
assert list_sum([1, -2, 3, -4, 5]) == 3
assert list_sum([1, 0, 0, 0]) == 1
