number = int(input("Enter a number: "))

if number == 1 or number % 2 == 0:
    print(False)
else:
    for i in range(3, int(number ** 0.5) + 1, 2):
        if number % i == 0:
            print(False)
            break
    else:
        print(True)

# 9 ** 0.5 == 3, что приводило к range(3,3)
# Поэтому цикл пропускался и выполнялась ветка else
# То же самое и с числом 15. Корень которого обрезается до числа 3
