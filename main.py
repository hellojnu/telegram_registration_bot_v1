import pytesseract
from pyautogui import *
from os import startfile
import functions as func
import api as api
import pyautogui
from data import path_to_telegram_exe, path_to_created_accounts




if __name__ == "__main__":
    func.beautiful_print(" tg_reger_v1 ")
    # account_count = input('how many accounts do you want to create?: ')
    account_count = 1
    service = 'sms-activate'
    for i in range(0, account_count):
        startfile(path_to_telegram_exe)
        func.image_click('start_messagin.png') # жмём Start Messaging
        func.image_wait('settin.png') # ждём настроек, чтобы проверить на QR-code
        sleep(1)
        if func.image_wait_once('using_phone_number.png'): # проверка на QR-code
            func.image_click('using_phone_number.png')
        func.image_wait('ready_for_input_number.png') # форма ввода номера
        func.key_press('tab') # переход на код страны
        sleep(0.5)
        func.key_press('delete') # удаление кода
        if float(api.get_balance(service))<4:
            print('top up balance!')
            break
        # методом проб и ошибок, юзаю 3 страны:
        # рашка с билайном, украина и вьетнам, хаха
        # ru = 0, ua = 1, vt = 10
        country = api.get_workable_country(service)
        #запрос api номера