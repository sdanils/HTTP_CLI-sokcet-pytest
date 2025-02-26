import hashlib
import tomllib
from typing import Any
import sys
import re

def get_md5_hash(input_string: str) -> str:
    """
    Вычисляет MD5 хеш для входной строки.
    """
    #Кодирование строки в байты
    encoded_string: bytes = input_string.encode('utf-8')
    # Создание объекта MD5.
    md5_hash = hashlib.md5()
    # Обновление объекта хеша данными.
    md5_hash.update(encoded_string)
    hex_digest: str = md5_hash.hexdigest()
    return hex_digest

def get_config() -> dict[str, Any]:
    """
    Загружает данные конфигурации программы.
    """
    with open("config.toml", "rb") as f:
        config: dict[str, Any] = tomllib.load(f)
    return config
     
def login_verification() -> int:
    """
    Проверяет пользователя при запуске.
    """
    config: dict[str, Any] = get_config()

    password_str: str = input("Введите пароль: ")
    hash_password: str = get_md5_hash(password_str)
    #Проверка совпадения пароля
    if(config["user"]["password"] != hash_password):
        print("Нет доступа.")
        return 0
    else:
        return 1

def menu_operation() -> int:
    """
    Выводит меню выбора дейсвтий.
    """
    message_error: str = "Неверный формат ввода.\n"
    while(True):
        print("Для введите номер пункта.\n1.Создать рассылку.\n2.Выйти.")
        client_chose: str = input()
        try:
            chose = int(client_chose)
        except ValueError:
            print(message_error)
            
        if(chose == 1):
            creating_mailing()
        elif(chose == 2):
            sys.exit()
        else:
            print(message_error)

def read_number(role: str) -> str: 
    """
    Читает введённый номер. Включает проверку на коррекстность.
    """
    #Загрузка маски номера.
    mask = get_config()["mask_number"]["regular_expression"]
    pattern = r"" + mask

    while True: 
        number = input(f"Введите номер телефона {role}. Exit для выхода:")
        number = number.replace(" ", "")
        if(number == "Exit"):
            return "-"

        match = re.match(pattern, number)
        if(bool(match)):
            break
        else:
            print("Некорректный номер.")

    return number

def creating_mailing():
    """
    Создает рассылку.
    """
    sender_number = read_number("Отправителя")
    if(sender_number == "-"):
        return 
    кecipient_number = read_number("Получателя")
    if(кecipient_number == "-"):
        return 

    massage = input("Введите сообщение: ")

    print("Сообщение создано.")
    

if __name__ == "__main__":
    result_login: int = login_verification()
    if(result_login == 0):
        sys.exit() 
    
    menu_operation()
    
    

     



  




