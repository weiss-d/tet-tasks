import json

import pytest
from presence_calculator.api import app


@pytest.fixture
def client():
    app.app.config["TESTING"] = True

    with app.app.test_client() as client:
        yield client


# Тесты валидации входных данных из запроса


def test_validate_input_correct(timing_data_normal):
    assert app._validate_input(timing_data_normal["timing_dict"])


def test_validate_input_correct_corner_cases(timing_data_corner):
    assert app._validate_input(timing_data_corner["timing_dict"])


def test_validate_input_invalid(timing_data_invalid):
    assert not app._validate_input(timing_data_invalid)


# Тесты API


def test_api_request_normal_cases(client, timing_data_normal):
    response = client.post("/appearance", json=timing_data_normal["timing_dict"])
    assert response.status_code == 200
    assert json.loads(response.data) == {
        "appearance": timing_data_normal["estimated_output"]
    }


def test_api_request_invalid_input(client, timing_data_invalid):
    response = client.post("/appearance", json=timing_data_invalid)
    assert response.status_code == 422
    assert json.loads(response.data) == {"error": "Input data is invalid."}
