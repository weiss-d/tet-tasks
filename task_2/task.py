"""
Task 2:
    Получение алфавитного списка животных из Википедии.
"""

from itertools import groupby

import pymorphy2
import wikipediaapi

# Собираем список всех элементов категории "Животные_по_алфавиту"

wiki = wikipediaapi.Wikipedia("ru")

cm_page = wiki.page("Category:Животные_по_алфавиту")

# Здесь происходит циклическое обращение к API Wikipedia,
# чтобы преодолеть ограничение в 500 результатов на запрос.
# Может занять некоторое время.
cmembers = cm_page.categorymembers

# Список животных первой степени очистки:
# содержит полные названия видов и семейств на Рус. и Англ.
animals = [key for key in cmembers.keys() if "Категория" not in key]

# Анализ и нормализация списка

morph = pymorphy2.MorphAnalyzer()


def normalize_if_noun(any_word):
    """Возвращает нормальную форму существительных в именительном падеже.
    Для всех остельных слов (включая английские) возвращает None.
    """
    for pare_variant in morph.parse(any_word):
        # Отбираем только существительные в именительном падеже,
        # множественном или единственном числе. Кол-во вариантов ограничиваем по рейтингу.
        # Первый найденный вариант считаем правильным.
        if pare_variant.score >= 0.3 and {"NOUN", "nomn"} in pare_variant.tag:
            return pare_variant.normal_form
    return None


normal_animals = set()

for animal in animals:
    for word in animal.split():
        if noun := normalize_if_noun(word):
            normal_animals.add(noun)

# Список животных второй степени очистки:
# только существительные в именительном падеже и единственном числе
normal_animals_list = list(normal_animals)

# Разделяем по алфавиту

normal_animals_list.sort()

alphabet_groups = []

for key, group in groupby(normal_animals_list, lambda x: x[0]):
    alphabet_groups.append((key, list(group)))

# Подсчёт слов и запись в файлы

for group in alphabet_groups:  # type: ignore
    with open(f"животные_на_{group[0]}.txt", "w+") as file:  # type: ignore
        file.write("\n".join(group[1]))  # type: ignore
        print(f"В файл на букву '{group[0]}' записано {len(group[1])} названий.")  # type: ignore
