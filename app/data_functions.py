import number_functions as nm

def check_data_mail(sender_number: str, kecipient_number: str, massage: str ) -> int:
    """ Data output for verification """
    print(f"Телефон отправителя: {sender_number}\nТелефон получателя: {kecipient_number}\nСообщение: {massage}\nДанные корректы?(y/n)")
    if input() != 'y':
        return 0
    else:
        return 1

def read_data_mail() -> list[str]:
    """ Reads data """
    sender_number = nm.read_number("Отправителя")
    if(sender_number == "-"):
        return '','',''
    recipient_number = nm.read_number("Получателя")
    if(recipient_number == "-"):
        return '','',''
    message = input("Введите сообщение: ")

    return sender_number, recipient_number, message