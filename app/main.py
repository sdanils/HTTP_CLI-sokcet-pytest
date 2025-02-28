import hashlib
import tomllib
from typing import Any
import sys
import re

def get_md5_hash(input_string: str) -> str:
    """
    Вычисляет MD5 хеш для входной строки.
    """
    encoded_string: bytes = input_string.encode('utf-8')
    md5_hash = hashlib.md5()
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

def conversion_number(number: str) -> str:
    if(len(number) == 10):
        number = "+7" + number
    elif(len(number) == 11):
        number = "+7" + number[1:]

    return number

def read_number(role: str) -> str: 
    """
    Читает введённый номер. Включает проверку на коррекстность.
    """
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
    
    number = conversion_number(number)

    return number

def check_data_mail(sender_number: str, kecipient_number: str, massage: str ) -> int:
    print(f"Телефон отправителя: {sender_number}\nТелефон получателя: {kecipient_number}\nСообщение: {massage}\nДанные корректы?(y/n)")
    if input() != 'y':
        return 0
    else:
        return 1

def read_data_mail() -> str:
    sender_number = read_number("Отправителя")
    if(sender_number == "-"):
        return 
    kecipient_number = read_number("Получателя")
    if(kecipient_number == "-"):
        return 
    massage = input("Введите сообщение: ")

    return sender_number, kecipient_number, massage

def creating_mailing() -> int:
    """
    Создает рассылку.
    """
    sender_number, kecipient_number, massage = read_data_mail()

    if check_data_mail(sender_number, kecipient_number, massage) == 0:
        return 0

    print("Сообщение создано.")
    
if __name__ == "__main__":
    result_login: int = login_verification()
    if(result_login == 0):
        sys.exit() 
    
    menu_operation()
    
    

     



  




