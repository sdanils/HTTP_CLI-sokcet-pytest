from Requests.mailing_request import Mailing_request
from Requests.mailing_response import Mailing_response
import data_functions as df
import log.logging as logging

def creating_mailing() -> int:
    """
    Creates a mailing list.
    """
    sender_number, recipient_number, message = df.read_data_mail()
    if sender_number == '' or df.check_data_mail(sender_number, recipient_number, message) == 0:
        return 0

    dict_data = {"sender":sender_number, "recipient": recipient_number, "message":message}
    request = Mailing_request(dict_data)
    
    logging.create_log("create request", "creating_mailing", "Creating a mailing list")
    response = request.make_request()
    if not response:
        return 0
    
    print(f"Результат: Код запроса - {response.code_response}, Информация - {response.body_response}\n")  
    return 1  