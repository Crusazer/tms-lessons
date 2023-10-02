from typing import Dict, Any, Type


def get_longest_word(text: str) -> str:
    word = ""
    for i in list(text.split()):
        if len(i) > len(word):
            word = i
    return word


assert get_longest_word("get longest word") == "longest"               # Test 1
assert get_longest_word("") == ""                                      # Test 2
assert get_longest_word("My dog only eats special food") == "special"  # Test 3
assert get_longest_word("One") == "One"                                # Test 4
assert get_longest_word("hello this is a string with words and spaces and big big woooooooooord") == "woooooooooord"                                # Test 4
