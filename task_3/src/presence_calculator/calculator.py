"""
Модуль вычисления одновременного пребывания ученика и учителя на уроке.
Все границы временных интервалов имеют формат Unix Timestamp.
"""
from typing import Dict, Iterable, List, Tuple, TypeVar

T = TypeVar("T")


def pairwise(iterable: Iterable[T]) -> Iterable[Tuple[T, T]]:
    """Разбивает входной итерируемый элемент на пары:
    s -> (s0, s1), (s2, s3), (s4, s5), ...
    """
    a = iter(iterable)
    return zip(a, a)


def _trim_by_lesson(lesson_list: List[int], trimming_list: List[int]) -> List[int]:
    """Обрезает или удаляет временные интервалы, выходящие за границы урока.

    Parameters
    ----------
    lesson_list : List[int]
        Список с таймингами урока.
    trimming_list : List[int]
        Список с таймингами под обрезку.

    Returns
    -------
    List[int]
        Список с таймингами в границах урока.

    """
    output_list: list = []

    for start, end in pairwise(trimming_list):
        if start > lesson_list[1]:
            break
        if end < lesson_list[0]:
            continue
        if start < lesson_list[0]:
            start = lesson_list[0]
        if end > lesson_list[1]:
            end = lesson_list[1]
        output_list.append(start)
        output_list.append(end)

    return output_list


def _get_overlap_time(interval_1: Tuple[int, int], interval_2: Tuple[int, int]) -> int:
    """Возвращает длину перекрытия двух временных интервалов.

    Parameters
    ----------
    interval_1 : Tuple[int, int]
        Первый интервал.
    interval_2 : Tuple[int, int]
        Второй интервал.

    Returns
    -------
    int
        Перекрытие интервалов в секундах.

    """
    start: int = max(interval_1[0], interval_2[0])
    end: int = min(interval_1[1], interval_2[1])

    delta: int = end - start
    if delta > 0:
        return delta
    return 0


def appearance(presense_dict: Dict[str, List[int]]) -> int:
    """Возвращает время одновременного пребывания ученика и учителя на уроке.

    Parameters
    ----------
    presense_dict : Dict[str, List[int]]
        Словарь с таймингами урока, ученика и учителя.
        Формат:
            {
              'lesson': [...],
              'pupil': [...],
              'tutor': [...]
            }

    Returns
    -------
    int
        Время одновременного пребывания в секундах.

    """
    total_time: int = 0

    tutor_times: List[int] = _trim_by_lesson(
        presense_dict["lesson"], presense_dict["tutor"]
    )
    pupil_times: List[int] = _trim_by_lesson(
        presense_dict["lesson"], presense_dict["pupil"]
    )

    for tutor_interval in pairwise(tutor_times):
        for pupil_interval in pairwise(pupil_times):
            total_time += _get_overlap_time(tutor_interval, pupil_interval)

    return total_time
