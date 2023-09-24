number = int(input("Enter a number: "))

for i in range(3, number, 2):
    if number % i == 0:
        print(False)
        break
else:
    print(True)
