import get_config as gc
import re

def conversion_number(number: str) -> str:
    """Formats the number"""
    if(len(number) == 10):
        number = "+7" + number
    elif(len(number) == 11):
        number = "+7" + number[1:]

    return number

def read_number(role: str) -> str: 
    """
    Reads the entered number. Enables the correctness check.
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
            return "-" #Для тестов.
    
    number = conversion_number(number)
    return number