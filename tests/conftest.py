import os
import json
import pytest


@pytest.fixture(scope='session')
def json_data():
    dir = os.path.dirname(os.path.abspath(__file__))
    json_file_path = os.path.join(dir, 'data', 'test_report.json')
    with open(json_file_path) as data:
        d = json.load(data)
        data.close()
    return d

