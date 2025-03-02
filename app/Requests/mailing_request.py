from json import dumps
import get_config as gc
import socket
from Requests.mailing_response import Mailing_response
from Requests.func_convert import Func_convert
import base64

class Mailing_request:
    def __init__(self, data: dict):
        self.json_data: dict = data

        config = gc.get_config() 
        self.host: str = config['server']['host']
        self.port: int = config['server']['port']
        self.path: str = config['requests_path']['post']
        self.auth_token: str = f"{config['user']['name']}:{config['user']['password']}"

        self.socket: socket.socket = None
    
    def to_bytes(self) -> bytes:
        auth_bytes = self.auth_token.encode('utf-8')
        auth_base64 = base64.b64encode(auth_bytes).decode('utf-8')
        str_data = dumps(self.json_data)
        encoded_data = str_data.encode('utf-8')

        request_line = (f"POST {self.path} HTTP/1.1\r\n" + 
            f"Host: {self.host}\r\n" + 
            f"Authorization: Basic {auth_base64}\r\n" +
            "Content-Type: application/json\r\n" +
            f"Content-Length: {len(encoded_data)}\r\n" + 
            "Connection: close\r\n" +  
            "\r\n"  
        )
        http_request = request_line.encode('utf-8') + encoded_data

        return http_request

    def read_response(self) -> bytes:
        response_bytes = b''

        try:
            while True:
                chunk = self.socket.recv(256)
                if not chunk:
                    break
                response_bytes += chunk
        except socket.error as e:
            print(f"Ошибка сети. {e}")

        return response_bytes

    def make_request(self) -> Mailing_response:        
        http_request = self.to_bytes()
        response_bytes = None

        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            self.socket.sendall(http_request)

            response_bytes = self.read_response()
        except socket.error as e:
            print(f"Ошибка сокета: {e}")
        finally:
            self.socket.close()

        if not response_bytes:
            return None

        response = Mailing_response.from_bytes(response_bytes)
        return response
    
    @staticmethod
    def from_bytes(binary_data: bytes) -> 'Mailing_request':
        dict_data: dict = Func_convert.from_bytes_data(binary_data)
        headers, body = dict_data.values() 

        headers = headers.split(" ")    
        path = headers[1]

        config = gc.get_config()
        if config["request_path"]["post"] != path:
            print("Неизвестый запрос")
            return None

        new_request = Mailing_request(body)
        return new_request

