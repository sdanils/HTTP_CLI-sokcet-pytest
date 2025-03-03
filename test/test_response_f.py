import pytest
from add_path import add_path_f
add_path_f()

import Requests.mailing_response as mr

def test_to_bytes_response():
    response_str = 'HTTP/1.1 200 OK\r\nDate: Mon, 03 Mar 2025 07:26:15 GMT\r\nServer: ServerE\r\nContent-type: application/json\r\nContent-Length: 45\r\nConnection: close\r\n\r\n{"status": "success", "message_id": "123456"}'
    response_bytes = response_str.encode("utf-8")

    new_response = mr.Mailing_response.from_bytes(response_bytes)

    assert new_response.date_response == 'Mon, 03 Mar 2025 07:26:15 GMT'
    assert new_response.body_response == {'status': 'success', 'message_id': '123456'}
    assert new_response.code_response == 200
    assert new_response.status_response == "OK"

    new_response_bytes = new_response.to_bytes()
    assert new_response_bytes.decode("utf-8") == response_str