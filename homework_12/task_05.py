import re


class WordIterable:
    __REGEX = r"\b\w+\b"

    def __init__(self, text: str):
        assert text is not str, "Class WordIterable got not string"
        self.__words = re.finditer(self.__REGEX, text)

    def __iter__(self):
        return self

    def __next__(self):
        return next(self.__words)[0]


if __name__ == "__main__":
    string = "Мама. мыла? раму!"
    for w in WordIterable(string):
        print(w)
