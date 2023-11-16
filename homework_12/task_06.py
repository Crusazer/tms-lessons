def generate_words(text: str) -> str:
    assert text is not str, "Function generate_words get only string, but got not string"
    words = text.split()
    for w in words:
        yield w


if __name__ == "__main__":
    text1 = "Мама мыла раму"
    for word in generate_words(text1):
        print(word)
