import get_config as gc
import sys
import re
import verification as ver
from RequestsData.mailing_request import Mailing_request

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
    mask = gc.get_config()["mask_number"]["regular_expression"]
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

    if(ver.login_verification() == 0):
        sys.exit() 

    dict_data = {"sender_number":sender_number, "kecipient_number": kecipient_number, "massage":massage}
    request = Mailing_request(dict_data)
    request.make_request()
    
    print("Сообщение создано.")
    
if __name__ == "__main__":
    result_login: int = ver.login_verification()
    if(result_login == 0):
        sys.exit() 
    
    menu_operation()
    
    

     



  




