import task_01
from functools import reduce

s = task_01.input_list()

# 4.1
summ = 0
for i in s:
    summ += i
print(f"4.1 For: {summ}")

summ = reduce(lambda x, y: x + y, s, 0)
print(f"4.1 Reduce: {summ}")

# 4.2
minn = s[0]
for i in s:
    if minn > i:
        minn = s
print(f"4.2 For: {minn}")

minn = reduce(lambda x, y: x if x < y else y, s)
print(f"4.2 Reduce: {minn}")

# 4.3
composition = 1
for i in s:
    composition *= i
print(f"4.3 For: {composition}")

composition = reduce(lambda x, y: x * y, s, 1)
print(f"4.3 Reduce: {composition}")

# 4.4
factorial = reduce(lambda x, y: x * y, range(1, 6), 1)
print(factorial)


# 4.5
def my_reduce(func, sequence, initial=None):
    x = 0 if initial is None else initial

    for k in sequence:
        x = func(x, k)
    return x


print(my_reduce(lambda x, y: x + y, [1, 2, 3], 5))
