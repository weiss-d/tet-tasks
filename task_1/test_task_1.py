import pytest

import task_1


def test_find_first_zero_index_generic_case():
    test_string = "11100"
    assert task_1.task(test_string) == 3


def test_find_first_zero_index_generic_case_different_iterable():
    test_list = [1, 1, 1, 0, 0]
    assert task_1.task(list(test_list)) == 3


@pytest.mark.parametrize(
    "test_string,estimated_output",
    [
        ("0000", 0),
        ("1111", None),
        ("110", 2),
        ("100", 1),
        ("10", 1),
    ],
)
def test_find_first_zero_corner_cases(test_string, estimated_output):
    assert task_1.task(test_string) == estimated_output
