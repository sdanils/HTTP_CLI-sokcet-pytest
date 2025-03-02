import datetime as dt

def add_log(log: str) -> int:
    try:
        with open("logs.txt", "a") as file:
            file.write(log)
    except Exception as e:
        print(f"Произошла ошибка при записи лога: {e}")

def create_log(process: str, module: str, comment: str, date: dt.datetime = None, code_response: int = 0) -> str:
    if date == None:
        date = dt.datetime.now()
        date_str = date.strftime('%Y-%m-%d %H:%M:%S')

    log_str = date_str + " || " + process + " || " + module + " || " + comment + " || " + str(code_response) + "\n"
    add_log(log_str)
  



