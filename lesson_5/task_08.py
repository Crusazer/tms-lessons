# Напишите функцию my_round, аналог встроенной round (ссылка на документацию).
# Использование самой функции round запрещено.

def my_round(number, digits=0):
    fractional = (number * 10 ** digits) % 1
    new_number = int(number * 10 ** digits)
    if fractional >= 0.5:
        return (new_number + 1) / 10 ** digits
    return new_number / 10 ** digits


print(my_round(3.823456789, 6))
print(my_round(5.64432434234))
