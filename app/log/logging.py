import datetime as dt

def add_log(log: str) -> int:
    try:
        with open("app\log\logs.txt", "a") as file:
            file.write(log)
    except Exception as e:
        print(f"Произошла ошибка при записи лога: {e}")

def create_log(process: str, module: str, comment: str, date: dt.datetime = None, code_response: int = 0) -> str:
    """ Creates a simple log """
    if date == None:
        date = dt.datetime.now()
        date_str = date.strftime("%a, %d %b %Y %H:%M:%S GMT")

    log_str = ( date_str + " || "
            + process + " || "
            + module + " || "
            + comment + " || "
            + str(code_response) + "\n")
    add_log(log_str)
  
def create_log_add_mailing(code_response: str, date_response: str, message_id: str):
    """ Creates a log when creating a mailing list """
    log_str = (date_response + " || "
            + "Created mailing" + " || "
            + "Mailing_response.from_bytes" + " || "
            + "succsesful creating" + " || "
            + code_response + " || "
            + message_id + "\n")
    add_log(log_str)

def create_log_error_response(code_response: str, date_response: str, error_server: str = None):
    """Creates a log when there is an error in the response from the server"""
    log_str = (date_response + " || "
            + "Created mailing" + " || "
            + "Mailing_response.from_bytes" + " || "
            + f"server response error. {error_server}" + " || "
            + code_response + "\n")
    add_log(log_str)

def create_response_log(body: dict, code_response: str, date_response: str):
    """Creates the log"""
    if code_response == "200":
        message_id = body['message_id']
        create_log_add_mailing(code_response, date_response, message_id)
    else:
        if body != None:
            create_log_error_response(code_response, date_response, body['error'])
        else:
            create_log_error_response(code_response, date_response)

