import json
import get_config as gc
import socket
from Requests.mailing_response import Mailing_response
import base64

class Mailing_request:
    def __init__(self, data: dict):
        self.json_data: str = json.dumps(data)

        config = gc.get_config() 
        self.host: str = config['server']['host']
        self.port: int = config['server']['port']
        self.path: str = config['requests_path']['post']
        self.auth_token: str = f"{config['user']['name']}:{config['user']['password']}"

        self.socket: socket.socket = None
    
    def to_bytes(self) -> bytes:
        auth_bytes = self.auth_token.encode('utf-8')
        auth_base64 = base64.b64encode(auth_bytes).decode('utf-8')
        encoded_data = self.json_data.encode('utf-8')

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

        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            self.socket.sendall(http_request)

            response_bytes = self.read_response()
        except socket.error as e:
            print(f"Ошибка сокета: {e}")
            self.close_socket()
        finally:
            self.socket.close()

        response = Mailing_response.from_bytes(response_bytes)
        return response

    def close_socket(self):
        self.socket.close()

    @staticmethod
    def from_bytes(binary_data: bytes) -> 'Mailing_request':
        return Mailing_request()