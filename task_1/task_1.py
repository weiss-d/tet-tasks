"""
Task 1
"""
from typing import List, Tuple, Union


def task(array: Union[List, Tuple, str]) -> Union[int, None]:
    """Поиск индекса первого нуля в упорядоченной коллекции из последовательности единиц
    и следующей за ней последовательности нулей.

        >>> task("111111111111111111111111100000000")
        25

    Parameters
    ----------
    array : Union[List, Tuple, str]
        Входная коллекция.

    Returns
    -------
    Union[int, None]
        Индекс первого нуля, либо None при отсутствии строке нулей.

    """
    if int(array[-1]) == 1:
        return None
    if int(array[0]) == 0:
        return 0

    index_first: int = 0
    index_last: int = len(array) - 1

    while index_first <= index_last:
        middle: int = (index_first + index_last) // 2
        mid_value: int = int(array[middle])
        right_value: int = int(array[middle + 1])

        if mid_value == 1 and right_value == 0:
            return middle + 1

        if mid_value == 1:
            index_first = middle
        elif mid_value == 0:
            index_last = middle

    return None


if __name__ == "__main__":
    TEST_STRING = "111111111111111111111111100000000"
    print(f"Test string: {TEST_STRING}")
    print(f"Result: {task(TEST_STRING)}")
