from json import dumps
from Requests.func_convert import Func_convert
import log.logging as logging
import re

class Mailing_response:
    def __init__(self, binary_data: bytes, code_response_: str, body_response_: dict, date_response_: str, status_response_: str):
        self.response_bytes: bytes  = binary_data
        self.code_response: int = int(code_response_)
        self.body_response: dict = body_response_
        self.date_response: str = date_response_
        self.status_response: str = status_response_
       
    def to_bytes(self) -> bytes:
        """
        Форматирует обьект HTTP ответа в строку байт.
        """
        str_data = dumps(self.body_response)
        encoded_data = str_data.encode('utf-8')

        response_line = (f"HTTP/1.1 {self.code_response} {self.status_response}\r\n" + 
            f"Date: {self.date_response}\r\n" + 
            f"Server: ServerE\r\n" +
            "Content-type: application/json\r\n" +
            f"Content-Length: {len(encoded_data)}\r\n" + 
            "Connection: close\r\n" +  
            "\r\n"  
        )
        http_response = response_line.encode('utf-8') + encoded_data
        return http_response

    @staticmethod  
    def search_info(headers: str) -> str:
        """
        Достаёт из строки ответа сервера информацию.
        """
        headers = re.split(r"[ \r\n]", headers)
        code_response = headers[1]
        status_response = headers[2]

        for i, el_headers in enumerate(headers):
            if el_headers == "Date:":
                date_response = " ".join(headers[i+1:i+7])
                break
        
        return code_response, status_response, date_response

    @staticmethod        
    def from_bytes(binary_data: bytes) -> 'Mailing_response':
        """
        Форматирует строку байт в обьект класс. Обратная операция к to_bytes.
        """
        dict_data: dict = Func_convert.from_bytes_data(binary_data)
        headers, body = dict_data.values() 
        code_response, status_response, date_response = Mailing_response.search_info(headers)

        logging.create_error_log(body, status_response, code_response, date_response)

        new_response = Mailing_response(binary_data, code_response, body, date_response, status_response)
        return new_response