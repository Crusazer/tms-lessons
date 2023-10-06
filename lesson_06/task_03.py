import task_01

s = task_01.input_list()

# 3.1
numbers = []
for i in s:
    if i >= 0:
        numbers.append(i)
print(f"3.1 For: {numbers}")

numbers = [i for i in s if i >= 0]
print(f"3.1 Generator: {numbers}")

numbers = list(filter(lambda x: x >= 0, s))
print(f"3.1 Map: {numbers}")

# 3.2
numbers = []
for i in s:
    if i % 2 != 0:
        numbers.append(i)
print(f"3.2 For: {numbers}")

numbers = [i for i in s if i % 2 != 0]
print(f"3.2 Generator: {numbers}")

numbers = list(filter(lambda x: x % 2 != 0, s))
print(f"3.2 Map: {numbers}")

# 3.3
numbers = [0, 0, 0]
for i in s:
    if i > 0:
        numbers[0] += 1
    elif i == 0:
        numbers[1] += 1
    else:
        numbers[2] += 1
print(f"3.3 For: Positive: {numbers[0]} Zero: {numbers[1]} Negative{numbers[2]}")

numbers = [0, 0, 0]
numbers[0] = [i for i in s if i > 0]
numbers[1] = [i for i in s if i == 0]
numbers[2] = [i for i in s if i < 0]
print(f"3.3 Generator: Positive: {numbers[0]} Zero: {numbers[1]} Negative{numbers[2]}")

numbers = [0, 0, 0]
numbers[0] = filter(lambda x: x > 0, s)
numbers[1] = filter(lambda x: x == 0, s)
numbers[2] = filter(lambda x: x < 0)
print(f"3.3 Filter: Positive: {numbers[0]} Zero: {numbers[1]} Negative{numbers[2]}")


# 3.4
def my_filter(func, lst):
    return [i for i in lst if func(i)]


def my_filter_yield(func, lst):
    for q in lst:
        if func(q):
            yield q
