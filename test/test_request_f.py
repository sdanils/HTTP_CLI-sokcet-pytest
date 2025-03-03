import pytest
import base64
from json import dumps
from add_path import add_path_f
add_path_f()

import Requests.mailing_request as mr
import get_config as gc

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

def test_from_byte_request():
    data = {"sender_number": "9009001221", "recipient_number": "9009001222", "massage": "Привет, ---!"}
    config = gc.get_config()
    new_request = mr.Mailing_request(data)

    byte_http = new_request.to_bytes()
    new_request_copy = mr.Mailing_request.from_bytes(byte_http)

    assert new_request.json_data == new_request_copy.json_data 
    assert new_request.host == new_request_copy.host 
    assert new_request.port == new_request_copy.port 
    assert new_request.path == new_request_copy.path 
    assert new_request.auth_token == new_request_copy.auth_token 

def test_to_bytes_request():
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


    
