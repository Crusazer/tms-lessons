def fib_loop(n: int) -> int:
    if n <= 1:
        return n
    a = [0] * (n + 1)
    a[1] = 1
    for i in range(2, n + 1):
        a[i] = a[i - 1] + a[i - 2]
    return a[n]


def fib_loop2(n: int) -> int:
    if n <= 1:
        return n

    first = 0
    second = 1
    for i in range(2, n + 1):
        first, second = second, first + second
    return second


def fib_rec(n: int) -> int:
    return n if n <= 1 else fib_rec(n - 1) + fib_rec(n - 2)


if __name__ == "__main__":
    print(fib_loop(1000))
    print(fib_loop2(1000))
