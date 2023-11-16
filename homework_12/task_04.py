class WordIterable:
    def __init__(self, text: str):
        assert text is not str, "Class WordIterable got not string"
        self.__words = text.split()
        self.__count = -1

    def __iter__(self):
        return self

    def __next__(self):
        self.__count += 1
        if self.__count == len(self.__words):
            raise StopIteration
        return self.__words[self.__count]


if __name__ == "__main__":
    string = "Мама мыла раму"
    for w in WordIterable(string):
        print(w)
