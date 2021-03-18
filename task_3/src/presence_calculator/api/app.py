"""
Task 3
WEB API
"""
import logging
from typing import Dict, List

import waitress
from flask import Flask, jsonify, request
from presence_calculator import calculator
from pydantic import BaseModel, ValidationError, validator


class TimingData(BaseModel):
    """Валидация словаря таймингов, получаемого по API."""

    lesson: List[int]
    pupil: List[int]
    tutor: List[int]

    @validator("*")
    def check_for_pairs(cls, timing_list):
        """Проверка чётности длины списков."""
        if len(timing_list) % 2:
            raise ValueError("Timing list has unpaired items")
        return timing_list

    @validator("*", each_item=True)
    def check_time_correctness(cls, time_value):
        """Все тайминги должны быть положительными."""
        if time_value < 0:
            raise ValueError("Timing list has incorrect timestamp")
        return time_value

    @validator("*")
    def check_interval_correctness(cls, timing_list):
        """Начало интервала не должно быть больше конца интервала."""
        for start, end in calculator.pairwise(timing_list):
            if start > end:
                raise ValueError("Timing list has incorrect interval")
        return timing_list


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
        {"appearance": результат}
    В случае некорректности входных данных:
        {"error": "описание_ошибки"}
    """
    response_dict: Dict
    response_status: int

    try:
        timing_data = TimingData.parse_obj(request.json)
        response_dict = {"appearance": calculator.appearance(timing_data.dict())}
        response_status = 200
    except (ValidationError, ValueError) as error:
        response_dict = {"error": str(error)}
        response_status = 422

    app.logger.info(
        LOG_STING,
        request.remote_addr,
        request.data[:1000],
        response_status,
        str(response_dict),
    )

    return (jsonify(response_dict), response_status)


if __name__ == "__main__":
    waitress.serve(app, listen="*:5000")
