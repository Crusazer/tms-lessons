import random
import copy


def bubble(array: list) -> list:
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

        a = marge_sort(left)
        b = marge_sort(right)
        lst = []
        i = 0
        j = 0
        k = 0

        while i < len(a) and j < len(b):
            if a[i] < b[j]:
                lst[k] = a[i]
                i += 1
            else:
                lst[k] = b[j]
                j += 1
            k += 1

        while i < len(a):
            lst[k] = a[i]
            i += 1
            k += 1

        while j < len(b):
            lst[k] = b[j]
            j += 1
            k += 1
    return lst


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
    test_case(sort_func, 10000)


if __name__ == '__main__':
    #test_sort(mergeSort)
    print(marge_sort([5, 3, 2, 4, 1]))
