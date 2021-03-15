from typing import List, Union


def task(array: Union[List, str]) -> Union[int, None]:
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
    test_string = "111111111111111111111111100000000"
    print(f"Test string: {test_string}")
    print(f"Result: {task(test_string)}")
