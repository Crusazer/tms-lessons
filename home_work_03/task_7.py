number = int(input("Enter a number: "))

if number == 1 or number % 2 == 0:
    print(False)
else:
    for i in range(3, number, 2):
        if number % i == 0:
            print(False)
            break
    else:
        print(True)
