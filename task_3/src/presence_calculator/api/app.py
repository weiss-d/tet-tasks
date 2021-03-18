"""
Task 3
WEB API
"""
import logging
from typing import Dict, List

import waitress
from flask import Flask, jsonify, request
from presence_calculator import calculator


def _validate_input(presence_dict: Dict[str, List[int]]) -> bool:
    """Проверка корректности входного словаря, получаемого из JSON-данных запроса.

    Parameters
    ----------
    presence_dict : Dict[str, List[int]]
        Входной словарь.

    Returns
    -------
    bool
        Подтверждение корректности.

    """
    if not all((key in presence_dict.keys() for key in ("lesson", "pupil", "tutor"))):
        return False
    if not all((isinstance(value, list) for value in presence_dict.values())):
        return False

    for timing_list in presence_dict.values():
        if len(timing_list) % 2:
            return False

        for start, end in calculator.pairwise(timing_list):
            if not isinstance(start, int) or not isinstance(end, int):
                return False
            if start < 0 or end < 0 or end < start:
                return False

    return True


# Настройка логирования

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(message)s",
    datefmt="%d-%m-%y %H:%M:%S",
)
LOG_STING = "Request from %s, Data: %s, Status: %s, Response: %s"


# Flask app

app = Flask(__name__)


@app.route("/appearance", methods=["POST"])
def appearance():
    """Ожидается POST-запрос, содержащий в теле JSON-данные в формате:
        {
          "lesson": [...],
          "pupil": [...],
          "tutor": [...]
        }
    В случае успеха возвращает JSON:
        {"appearance": <результат>}
    В случае некорректности входных данных:
        {"error": "Input data is invalid."}
    """
    if _validate_input(request.json):
        response_dict = {"appearance": calculator.appearance(request.json)}
        app.logger.info(
            LOG_STING,
            request.remote_addr,
            request.data[:1000],
            "OK",
            str(response_dict),
        )
        return jsonify(response_dict)

    response_dict = {"error": "Input data is invalid."}
    app.logger.info(
        LOG_STING, request.remote_addr, request.data[:1000], "ERROR", str(response_dict)
    )
    return (jsonify(response_dict), 422)


if __name__ == "__main__":
    waitress.serve(app, listen="*:5000")
