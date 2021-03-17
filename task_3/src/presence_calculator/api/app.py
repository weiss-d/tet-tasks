import logging
from typing import Dict, List

import waitress
from flask import Flask, jsonify, request
from presence_calculator import calculator


def _validate_input(presense_dict: Dict[str, List[int]]) -> bool:
    if not all((key in presense_dict.keys() for key in ("lesson", "pupil", "tutor"))):
        return False
    if not all((isinstance(value, list) for value in presense_dict.values())):
        return False

    for timing_list in presense_dict.values():
        if len(timing_list) % 2:
            return False

        for start, end in calculator.pairwise(timing_list):
            if not isinstance(start, int) or not isinstance(end, int):
                return False
            if start < 0 or end < 0 or end < start:
                return False

    return True


logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(message)s",
    datefmt="%d-%m-%y %H:%M:%S",
)
LOG_STING = "Request from %s, Data: %s, Status: %s, Response: %s"

app = Flask(__name__)


@app.route("/appearance", methods=["POST"])
def appearance():
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
