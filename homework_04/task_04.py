import random

secret_number = random.randint(0, 100)
while True:
    user_guess = int(input("Try to guess a number (0, 100): "))
    if user_guess == secret_number:
        print("Congratulation!")
        break
    else:
        if user_guess > secret_number:
            print("Your number is bigger!")
        else:
            print("Your number is less!")

