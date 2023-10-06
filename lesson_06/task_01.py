def input_list(prompt="", sep=' ', element_type=int):
    return list(map(element_type, input(prompt).split(sep)))


if __name__ == "__main__":
    print(input_list("Enter a string:"))
