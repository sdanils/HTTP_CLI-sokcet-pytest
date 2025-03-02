import json

class Func_convert:
    @staticmethod
    def from_bytes_data(binary_data: bytes) -> dict:
        """
        Возвращает словарь с заголовками в str и телом ответа в dict
        """
        response_str = binary_data.decode("utf-8")
        headers, body =  response_str.split("\r\n\r\n")
        
        try:
            json_body: dict = json.loads(body)
        except json.JSONDecodeError:
            print("Ошибка чтения тела")  

        dict_data = {"headers": headers, "body": json_body}

        return dict_data
    