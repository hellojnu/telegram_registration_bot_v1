import pytesseract
from pyautogui import *
from os import startfile
import functions as func
import api as api
import pyautogui
from russian_names import RussianNames
from shutil import copy2
import datetime
import os
import shutil
import os
from pyautogui import *
from os import startfile

import datetime
from api import api_keys, account_count, accessible_services
import colorama as color
import pyautogui as py

acc_services = accessible_services
#http://api2.5sim.net/stubs/handler_api.php

#http://api2.5sim.net/stubs/handler_api.php?api_key=de3f53ce486e412f9746ee8ce0f10e62&action=getBalance
#http://api2.5sim.net/stubs/handler_api.php?api_key=de3f53ce486e412f9746ee8ce0f10e62&action=setStatus&id=2629287&status=-1

api.get_balance(acc_services)
now = datetime.datetime.now().strftime("%H:%M:%S")
print(color.Fore.LIGHTRED_EX + f"[{now}] >> нет доступного баланса ни на одном из сервисов. пополните счёт и перезапустите скрипт.")
sys.exit()