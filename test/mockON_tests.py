#Тесты с включённым mock сервером
import pytest
import unittest.mock as um
from json import dumps

from add_path import add_path_f
add_path_f()

import Requests.mailing_request as m_request
import Requests.mailing_response as m_response

@pytest.mark.parametrize(
    "sender, recipient, message, expected_code",
    [
        ("+79091231212", "+79121223345", "Hello", 200),
        ("+79091231213", "9099009090", "Hi", 200),
        ("+79091231214", "+79121223347", "Error", 200), 
        ("+79091231215", "+79121223348", "Test", 200),
    ],
)

def test_request(sender, recipient, message, expected_code):
    data = {"sender":sender, "recipient": recipient, "message":message}
    request = m_request.Mailing_request(data)
    response: m_response.Mailing_response = request.make_request()

    assert response.code_response == expected_code

def test_request_w_Authorization():
    data = {"sender":"+79091231215", "recipient": "+79121223348", "message": "Test"}
    date_str = dumps(data)
    encoded_data = date_str.encode('utf-8')
    mock_to_bytes = ("POST /send_sms HTTP/1.1\r\nHost: localhost\r\nContent-Type: application/json\r\n" +
                    f"Content-Length: {len(encoded_data)}\r\nConnection: close\r\n\r\n")  
    mock_to_bytes = mock_to_bytes.encode('utf-8') + encoded_data

    with um.patch.object(m_request.Mailing_request, 'to_bytes', return_value=mock_to_bytes):
        request = m_request.Mailing_request(data)
        response: m_response.Mailing_response = request.make_request()

        assert response.code_response == 401