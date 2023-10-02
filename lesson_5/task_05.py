# Напишите функцию is_palindrome, которая принимает на вход строку,
# и возвращает True если это палиндром, иначе False.

def is_palindrome(string):
    return string == string[::-1]


print(is_palindrome("asa"))
