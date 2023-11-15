def generate_squares(number: int):
    count = 1
    while count <= number:
        yield count ** 2
        count += 1


if __name__ == "__main__":
    for i in generate_squares(10):
        print(i)
    assert [1, 4, 9, 16, 25] == [i for i in generate_squares(5)]