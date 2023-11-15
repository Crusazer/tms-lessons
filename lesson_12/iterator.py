class SquaresIterable:
    def __init__(self, number: int):
        self.__count = number
        self.__current_count = 0

    def __iter__(self):
        return self

    def __next__(self):
        self.__current_count += 1
        if self.__current_count > self.__count:
            raise StopIteration
        return self.__current_count ** 2


if __name__ == "__main__":
    for i in SquaresIterable(10):
        print(i)
