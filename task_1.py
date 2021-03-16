def task(array):
    # Реализован бинарный поиск. Сложность алгоритма O(log n).
    left = -1
    right = len(array)
    while right - left > 1:
        middle = (right + left) // 2
        if array[middle] == '0':
            right = middle
        else:
            left = middle
    return right


print(task("111111111111111111111111100000000"))
