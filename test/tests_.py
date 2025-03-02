import pytest
import sys
import os
import base64
from json import dumps

current_dir = os.path.dirname(os.path.abspath(__file__))
module_dir = os.path.join(current_dir, '..', 'app')
sys.path.insert(0, module_dir)

import Requests.mailing_request as mr
import get_config as gc
from main import read_number 

def get_data_req() -> dict:
    return {"sender_number": "9009001221", "recipient_number": "9009001222", "massage": "Привет, ---!"}

def test_constructor_request():
    data = get_data_req()
    config = gc.get_config()
    new_request = mr.Mailing_request(data)

    assert new_request.json_data == data
    assert new_request.host == config['server']['host']
    assert new_request.port == config['server']['port']
    assert new_request.path == config['requests_path']['post']

@pytest.fixture
def mocked_input(monkeypatch):
    """Фикстура для перехвата input."""
    def fake_input(prompt):
        return fake_input.values.pop(0)
    fake_input.values = []
    monkeypatch.setattr('builtins.input', fake_input)
    return fake_input

@pytest.mark.parametrize(
    "user_inputs, expected_result",
    [
        (["100"], "-"),
        (["900"], "-"),
        (["+7900"], "-"),
        (["8900"], "-"),
        (["123 112 90 90"], "-"), 
        ([""], "-"), 
        (["1231232323"], "-"),
        (["900123231"], "-"),
        (["109009001212"], "-"),
        (["10 900 900 12 12"], "-"),
        (["+"], "-"), 
        (["."], "-"), 
        (["Привет мир!"], "-"),
        (["+79091238989"], "+79091238989"),
        (["89091238989"], "+79091238989"),
        (["+7 909 123 89 89"], "+79091238989"),
        (["+790912   38989"], "+79091238989"), 
        (["9091238989"], "+79091238989"), 
        (["79091238989"], "+79091238989"), 
    ],
)
    
def test_read_number(mocked_input, user_inputs, expected_result):
    """Тестирует my_function с разными входами."""
    mocked_input.values = user_inputs
    assert read_number("Test") == expected_result

def test_to_bytes():
    data = get_data_req()
    new_request = mr.Mailing_request(data)

    bytes_obj: bytes = new_request.to_bytes()

    config = gc.get_config()
    auth_bytes = f"{config['user']['name']}:{config['user']['password']}".encode('utf-8')
    auth_base64 = base64.b64encode(auth_bytes).decode('utf-8')
    str_data = dumps(data)
    encoded_data = str_data.encode('utf-8')

    request_line = (f"POST {config['requests_path']['post']} HTTP/1.1\r\n" + 
        f"Host: {config['server']['host']}\r\n" + 
        f"Authorization: Basic {auth_base64}\r\n" +
        "Content-Type: application/json\r\n" +
        f"Content-Length: {len(encoded_data)}\r\n" + 
        "Connection: close\r\n" +  
        "\r\n"  
    )
    http_request = request_line.encode('utf-8') + encoded_data

    assert bytes_obj == http_request


    





