# Написать функцию xor_cipher, принимающая 2 аргумента: строку, которую нужно зашифровать, и
# ключ шифрования (целое число), которая возвращает строку, зашифрованную путем применения функции XOR (^)
# над символами строки с ключом. Написать также функцию xor_uncipher, которая по зашифрованной строке и
# ключу восстанавливает исходную строку. Подсказка: см. функции ord и chr.

def xor_cipher(string: str, key: int) -> str:
    return ''.join([chr(ord(i) ^ key) for i in string])


my_string = xor_cipher("Hello world!", 2)
print(my_string)

my_string = xor_cipher(my_string, 2)
print(my_string)

