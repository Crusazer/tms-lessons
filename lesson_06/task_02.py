import task_01

s = task_01.input_list()

# 2.1
numbers = []
for i in s:
    numbers.append(i * 100)
print(f"2.1 For: {numbers}")

numbers = [i * 100 for i in s]
print(f"2.1 Generator: {numbers}")

numbers = list(map(lambda x: x * 100, s))
print(f"2.1 Map: {numbers}")

# 2.2
numbers = []
for i in s:
    numbers.append(str(i))
print(f"2.2 For: {numbers}")

numbers = [str(i) for i in s]
print(f"2.2 Generator: {numbers}")

numbers = list(map(str, s))
print(f"2.2 Map: {numbers}")

# 2.3
numbers = []
for i in s:
    numbers.append(round(i / 100))
print(f"2.3 For: {numbers}")

numbers = [round(i / 100) for i in s]
print(f"2.3 Generator: {numbers}")

numbers = list(map(lambda x: round(x / 100), s))
print(f"2.3 Lambda: {numbers}")


# 2.4
def my_map(func, lst):
    return [func(q) for q in lst]


# 2.5
def my_map_yield(func, lst):
    for w in lst:
        yield func(w)


numbers = my_map(lambda x: x * 10, s)
print(f"My map: {numbers}")

numbers = my_map_yield(lambda x: x * 10, s)
print(f"My map: {numbers}")
