def check_types(func):
    def wrapper(x, y):
        if isinstance(x, int) and isinstance(y, int):
            return func(x, y)
        else:
            print("Expected int type")
            return None
    return wrapper


@check_types
def plus(x, y):
    return x + y


@check_types
def minus(x, y):
    return x - y


@check_types
def mult(x, y):
    return x * y


@check_types
def div(x, y):
    return x / y


print(plus(5, 1))
print(minus(0, "sdf"))
print(mult('dfg', 'wqe'))
print(div('sdf', 1))
