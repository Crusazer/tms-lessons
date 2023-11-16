import re


def generate_words(text: str) -> str:
    assert text is not str, "Function generate_words get only string, but got not string"
    regex = r"\b\w+\b"
    words = re.finditer(regex, text)
    for w in words:
        yield w[0]


if __name__ == "__main__":
    text1 = "Мама. мыла? раму!"
    for word in generate_words(text1):
        print(word)
