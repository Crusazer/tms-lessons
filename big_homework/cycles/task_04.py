lst_numbers = list(map(int, input("Enter numbers separation space: ").split()))

for i in lst_numbers:
    if i == 0:
        print("Yes")
        break
else:
    print("No")
