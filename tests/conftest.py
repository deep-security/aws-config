import json
import jsonpickle
import os

from unittest.mock import MagicMock
from pytest import fixture


def load_json(file_path):
    dir_name = os.path.dirname(os.path.abspath(__file__))
    file_name = os.path.join(dir_name, file_path)
    with open(file_name) as f:
        data = json.load(f)
    return data


@fixture
def event():
    return load_json('resources/event.json')


@fixture
def event_policy():
    return load_json('resources/event_with_policy.json')


@fixture
def event_control():
    return load_json('resources/event_with_control.json')


@fixture
def config_response():
    return load_json('resources/config_response.json')


@fixture
def config_service(config_response):
    service = MagicMock()
    service.put_evaluations.return_value = config_response
    return service


@fixture
def computers(monkeypatch):
    data = load_json('resources/computers.json')
    computers = jsonpickle.decode(json.dumps(data))
    monkeypatch.setattr(computers, 'get', lambda: None)
    return computers


@fixture
def manager(computers):
    manager = MagicMock()
    manager._request.return_value = None
    manager.sign_in.return_value = None
    manager.sign_out.return_value = None
    manager.computers = computers
    return manager
