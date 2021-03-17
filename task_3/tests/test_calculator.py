import pytest
from presence_calculator import calculator

# Тесты вспомогательных функций


@pytest.mark.parametrize(
    "list_couple,estimated_output",
    [
        (
            (
                [500, 1500],
                [400, 800, 900, 1200, 1300, 1600],
            ),
            [500, 800, 900, 1200, 1300, 1500],
        ),
        (
            (
                [500, 1500],
                [400, 800, 900, 1200],
            ),
            [500, 800, 900, 1200],
        ),
        (
            (
                [500, 1500],
                [900, 1200, 1300, 1600],
            ),
            [900, 1200, 1300, 1500],
        ),
    ],
)
def test_trim_inervals_by_lesson_normal_cases(list_couple, estimated_output):
    assert (
        calculator._trim_by_lesson(list_couple[0], list_couple[1]) == estimated_output
    )


@pytest.mark.parametrize(
    "list_couple,estimated_output",
    [
        (
            (
                [500, 1500],
                [900, 1200],
            ),
            [900, 1200],
        ),
        (
            (
                [500, 1500],
                [400, 1600],
            ),
            [500, 1500],
        ),
        (
            (
                [500, 1500],
                [],
            ),
            [],
        ),
        (
            (
                [500, 500],
                [],
            ),
            [],
        ),
    ],
)
def test_trim_inervals_by_lesson_corner_cases(list_couple, estimated_output):
    assert (
        calculator._trim_by_lesson(list_couple[0], list_couple[1]) == estimated_output
    )


@pytest.mark.parametrize(
    "tuple_1,tuple_2,estimated_output",
    [
        ((100, 500), (300, 700), 200),
        ((300, 700), (100, 500), 200),
        ((100, 500), (100, 500), 400),
        ((100, 500), (200, 400), 200),
        ((100, 200), (300, 400), 0),
        ((100, 200), (200, 300), 0),
    ],
)
def test_overlap_time(tuple_1, tuple_2, estimated_output):
    assert calculator._get_overlap_time(tuple_1, tuple_2) == estimated_output


# Тесты главной функции


def test_appearance_normal_cases(timing_data_normal):
    assert (
        calculator.appearance(timing_data_normal["timing_dict"])
        == timing_data_normal["estimated_output"]
    )


def test_appearance_corner_cases(timing_data_corner):
    assert (
        calculator.appearance(timing_data_corner["timing_dict"])
        == timing_data_corner["estimated_output"]
    )
