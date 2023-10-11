lst_numbers = list(map(int, input("Enter numbers separation space: ").split()))

max_numbers = lst_numbers[0]
for i in lst_numbers:
    if i > max_numbers:
        max_numbers = i

print(max_numbers)