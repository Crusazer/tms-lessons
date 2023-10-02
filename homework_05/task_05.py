def get_most_frequent_word(text: str) -> str:
    counter_words = {}
    for i in text.split():
        if i in counter_words:
            counter_words[i] += 1
        else:
            counter_words[i] = 0

    return max(counter_words, key=counter_words.get)


assert get_most_frequent_word("hello this is a string with words and spaces and "
                              "big big woooooooooord and and and") == "and"
assert get_most_frequent_word("a") == 'a'
