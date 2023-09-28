# Task 1
summ = 0
for i in range(0, 101):
    summ += i
print(f"1: {summ}")

# Task 2
summ = 0
for i in range(100, 1001):
    summ += i
print(f"2: {summ}")

# Task 3
summ = 0
for i in range(100, 1001, 2):
    summ += i
print(f"3: {summ}")

# Task 4
factorial = 1
for i in range(1, 11):
    factorial *= i
print(f"4: {factorial}")

# Task 5
answer = 2
for i in range(9):
    answer *= 2
print(f"5: {answer}")

# Task 6
summ = 0
i = 1
while summ < 1000:
    summ += i
    i += 1
i -= 1
print(f"6: summ = {summ}, last number = {i}")
