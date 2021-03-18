import json

import pytest
from presence_calculator.api import app


@pytest.fixture
def client():
    app.app.config["TESTING"] = True

    with app.app.test_client() as client:
        yield client


def test_api_request_normal_cases(client, timing_data_normal):
    response = client.post("/appearance", json=timing_data_normal["timing_dict"])
    assert response.status_code == 200
    assert json.loads(response.data) == {
        "appearance": timing_data_normal["estimated_output"]
    }


def test_api_request_invalid_input(client, timing_data_invalid):
    response = client.post("/appearance", json=timing_data_invalid["timing_dict"])
    assert response.status_code == 422
    assert timing_data_invalid["error_message"] in json.loads(response.data)["error"]
