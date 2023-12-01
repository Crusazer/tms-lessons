import random
import copy


def bubble_sort(array: list) -> list:
    if not array:
        return []

    lst = copy.deepcopy(array)
    length = len(lst)
    for i in range(length):
        for j in range(1, length - i):
            if lst[j] < lst[j - 1]:
                lst[j - 1], lst[j] = lst[j], lst[j - 1]
    return lst


def insert_sort(array: list) -> list:
    lst = copy.deepcopy(array)
    length = len(lst)

    for i in range(1, length):
        temp = lst[i]

        # Find index to insert
        j = i
        while j > 0 and lst[j - 1] > temp:
            lst[j] = lst[j - 1]
            j -= 1
        lst[j] = temp
    return lst


def marge_sort(array: list) -> list:
    lst2 = array.copy()

    if len(lst2) > 1:
        mid = len(lst2) // 2
        left = lst2[:mid]
        right = lst2[mid:]

        left_piece = marge_sort(left)
        right_piece = marge_sort(right)

        marge_list = []
        i = 0
        j = 0

        while i < len(left_piece) and j < len(right_piece):
            if left_piece[i] < right_piece[j]:
                marge_list.append(left_piece[i])
                i += 1
            else:
                marge_list.append(right_piece[j])
                j += 1

        while i < len(left_piece):
            marge_list.append(left_piece[i])
            i += 1

        while j < len(right_piece):
            marge_list.append(right_piece[j])
            j += 1
        return marge_list
    return lst2


def quick_sort(lst: list) -> list:
    array = lst.copy()

    if len(array) < 2:
        return array
    else:
        pivot = array[random.randint(1, len(array)) - 1]
        less = []
        greater = []
        equal = []

        for i in array:
            if i < pivot:
                less.append(i)
            elif i == pivot:
                equal.append(i)
            else:
                greater.append(i)
        return quick_sort(less) + equal + quick_sort(greater)


def generate_list(n: int):
    return [random.randint(0, n ** 2) for _ in range(n)]


def test_case(sort_func: callable, n: int):
    lst = generate_list(n)
    copy_lst = copy.deepcopy(lst)
    sorted_lst = sort_func(lst)
    assert lst == copy_lst, 'Sort function must not change the original list'
    assert len(sorted_lst) == n
    assert all(sorted_lst[i] <= sorted_lst[i + 1]
               for i in range(len(sorted_lst) - 1)), \
        'List is not sorted'


def test_sort(sort_func: callable):
    test_case(sort_func, 0)
    test_case(sort_func, 1)
    test_case(sort_func, 2)
    test_case(sort_func, 10)
    test_case(sort_func, 100)
    test_case(sort_func, 1000)
    test_case(sort_func, 100000)


if __name__ == '__main__':
    test_sort(insert_sort)
