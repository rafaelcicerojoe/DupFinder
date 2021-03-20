import time
import random
from pathlib import Path
from base import SMWinservice
import main

class SO(SMWinservice):
    _svc_name_ = "RmSvc_SO"
    _svc_display_name_ = "SO_Remover"
    _svc_description_ = "Funciona :)"
    
    def main(self):
        time.sleep(5)
        main.prog()
        time.sleep(15)
        main.prog()
        time.sleep(45)
        main.prog()


if __name__ == '__main__':
    SO.parse_command_line()

