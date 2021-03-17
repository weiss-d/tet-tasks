import pytest


# Normal cases
@pytest.fixture(
    params=[
        {
            "timing_dict": {
                "lesson": [500, 1500],
                "pupil": [600, 1000],
                "tutor": [900, 1300],
            },
            "estimated_output": 100,
        },
        {
            "timing_dict": {
                "lesson": [500, 1500],
                "pupil": [400, 1000],
                "tutor": [400, 600],
            },
            "estimated_output": 100,
        },
        {
            "timing_dict": {
                "lesson": [100, 2500],
                "pupil": [200, 500, 600, 900, 1300, 1600],
                "tutor": [400, 700, 1100, 1400, 1500, 1800],
            },
            "estimated_output": 400,
        },
    ]
)
def timing_data_normal(request):
    return request.param


# Corner cases
@pytest.fixture(
    params=[
        {
            "timing_dict": {
                "lesson": [500, 1500],
                "pupil": [],
                "tutor": [900, 1300],
            },
            "estimated_output": 0,
        },
        {
            "timing_dict": {
                "lesson": [500, 1500],
                "pupil": [550, 550],
                "tutor": [400, 600],
            },
            "estimated_output": 0,
        },
        {
            "timing_dict": {
                "lesson": [100, 500],
                "pupil": [200, 500],
                "tutor": [100, 200],
            },
            "estimated_output": 0,
        },
    ]
)
def timing_data_corner(request):
    return request.param
