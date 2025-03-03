import sys
import verification_function as ver
import creating_mailing as cm

def menu_operation() -> int:
    """
    Displays the action selection menu.
    """
    message_error: str = "Неверный формат ввода.\n"
    while(True):
        print("Введите номер пункта.\n1.Создать рассылку.\n2.Выйти.")
        client_chose: str = input()
        try:
            chose = int(client_chose)
        except ValueError:
            print(message_error)
            
        if(chose == 1):
            cm.creating_mailing()
        elif(chose == 2):
            sys.exit()
        else:
            print(message_error)    
    
if __name__ == "__main__":
    if ver.login_verification() == 0:
        sys.exit() 
        
    menu_operation()
    
    

     



  




