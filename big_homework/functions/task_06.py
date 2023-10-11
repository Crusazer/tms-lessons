def hello_world():
    print("Hello world!")


def my_sum(a, b):
    return a + b


def simple_compare(a, b) -> bool:
    return a < b


def compare(a , b) -> int:
    if a < b:
        return -1
    if a > b:
        return 1
    return 0


def filter_negative_numbers(numbers: list) -> list:
    return [x for x in numbers if x >= 0]


number_task = int(input("Enter the number of task: "))

if number_task == 1:
    hello_world()
elif number_task in (2, 3, 4):
    a = int(input("Enter first number: "))
    b = int(input("Enter second number: "))

    if number_task == 2:
        print(f"The sum of numbers: {my_sum(a, b)}")
    elif number_task == 3:
        print(f"Is first number less then second? Answer: {simple_compare(a, b)}")
    else:
        print(f"Is numbers equal? Answer: {compare(a, b)}")
else:
    my_list = list(map(int, input("Enter a list of numbers separated of a space: ").split()))
    print(f"List without negative numbers: {filter_negative_numbers(my_list)}")



