def get_number(matrix: list) -> int:
    return sum(matrix[0])


def check_strings(matrix: list, number: int) -> bool:
    for string in matrix:
        if sum(string) != number:
            return False
    return True


def check_rows(matrix: list, number: int) -> bool:
    for j in range(len(matrix)):
        if number != sum([matrix[k][j] for k in range(len(matrix))]):
            return False
    return True


def check_diagonals(matrix: list, number: int) -> bool:
    length = len(matrix)

    # Principal diagonal
    if number != sum([matrix[i][i] for i in range(length)]):
        return False

    # Secondary diagonal
    if number != sum([matrix[i][-1 - i] for i in range(length)]):
        return False

    return True


def is_magic_square(matrix: list) -> bool:
    number = get_number(matrix)

    if check_diagonals(matrix, number) is False:
        return False

    return check_strings(matrix, number) and check_rows(matrix, number)


if __name__ == "__main__":
    n = int(input("Enter size of matrix: "))

    my_matrix = []
    for i in range(0, n):
        my_matrix.append([int(x) for x in input(f"Enter {i+1} string: ").split()])

    print(is_magic_square(my_matrix))
