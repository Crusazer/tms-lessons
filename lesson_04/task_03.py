import random

secret_number = random.randint(1, 5)
user_number = int(input("Try to guess a number (1..5): "))
while user_number != secret_number:
    user_number = int(input("Wrong. Try again: "))

print("Right. Congratulations!")
