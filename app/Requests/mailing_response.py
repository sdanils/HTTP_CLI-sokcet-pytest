import json

class Mailing_response:
    def __init__(self, binary_data: bytes, code_response_: str, body_response_: dict, date_response_: str, status_response_: str):
        self.response_bytes: bytes  = binary_data
        self.code_response: int = int(code_response_)
        self.body_response: dict = body_response_
        self.date_response: str = date_response_
        self.status_response: str = status_response_

    @staticmethod        
    def to_bytes(self) -> bytes:
        return None

    @staticmethod        
    def from_bytes(binary_data: bytes) -> 'Mailing_response':
        response_str = binary_data.decode("utf-8")
        headers, body =  response_str.split("\r\n\r\n")

        headers = headers.split(" ")
        date_response = "".join(headers[4:10])
        code_response = headers[1]
        status_response = headers[2]
        
        try:
            json_body: dict = json.loads(body)
        except json.JSONDecodeError:
            print("Ошибка: прочитать ответ")

        new_response = Mailing_response(binary_data, code_response, json_body, date_response, status_response)
        return new_response