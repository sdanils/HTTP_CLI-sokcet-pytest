import json
import get_config as gc
import socket

class Mailing_request:
    def __init__(self, data: dict):
        config = gc.get_config()
        data['login_client'] = config['user']['name']
        data['password_client'] = config['user']['password']

        self.json_data: str = json.dumps(data) 
        self.host: str = config['server']['host']
        self.port: str = config['server']['port']
        self.path: str = config['requests_path']['post']
    
    def to_bytes(self) -> bytes:
        encoded_data = self.json_data.encode('utf-8')
        request_line = f"POST {self.path} HTTP/1.1\r\n"
        headers = [
            f"Host: {self.host}\r\n",
            "Content-Type: application/json\r\n",
            f"Content-Length: {len(encoded_data)}\r\n",
            "Connection: close\r\n",  
            "\r\n"  
        ]
        http_request = request_line.encode('utf-8') + "".join(headers).encode('utf-8') + encoded_data

        return http_request

    def make_request(self):        
        http_request = self.to_bytes()

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #client_socket.connect((self.host, self.port))
        print(f"Подключено к {self.host}:{self.port}")
        #client_socket.sendall(http_request)
        #For test
        print("HTTP запрос отправлен:")
        print(http_request.decode('utf-8'))
    

    @staticmethod
    def from_bytes(binary_data: bytes) -> 'Mailing_request':
        return Mailing_request()