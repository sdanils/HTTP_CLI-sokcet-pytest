import get_config as gc
import hashlib
from typing import Any
import os


def get_md5_hash(input_string: str) -> str:
    """
    Вычисляет MD5 хеш для входной строки.
    """
    encoded_string: bytes = input_string.encode('utf-8')
    md5_hash = hashlib.md5()
    md5_hash.update(encoded_string)
    hex_digest: str = md5_hash.hexdigest()
    return hex_digest

def login_verification() -> int:
    """
    Проверяет пользователя при запуске.
    """
    config: dict[str, Any] = gc.get_config()

    password_str: str = input("Введите пароль: ")
    os.system('cls')
    hash_password: str = get_md5_hash(password_str)
    
    if(config["user"]["password"] != hash_password):
        print("Нет доступа.")
        return 0
    else:
        return 1