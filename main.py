from pyautogui import *
from os import startfile
import functions as func
import api as api
from data import service
import datetime

if __name__ == "__main__":
    func.beautiful_print(" tg_reger_v1 ")
    # account_count = input('how many accounts do you want to create?: ')
    account_count = 1

    at_least_one_positive_balance = False
    accessible_services = []
    for i in range(0, len(service)): # проверяем баланс на сервисах
        if float(api.get_balance(service[i]))<15:
            print(f"top up balance at '{service[i]}', please.")
        else:
            accessible_services.append(i)
            at_least_one_positive_balance = True

    if at_least_one_positive_balance:
        for i in range(0, account_count):
            path, name, surname = func.create_telegram_exe_and_person()
            startfile(path + '\\Telegram.exe')
            func.image_click('start_messagin.png') # жмём Start Messaging
            func.image_wait('settin.png') # ждём настроек, чтобы проверить на QR-code
            sleep(0.5)
            if func.image_wait_once('using_phone_number.png'): # проверка на QR-code
                func.image_click('using_phone_number.png')
            func.image_wait('ready_for_input_number.png') # форма ввода номера

            # методом проб и ошибок, юзаю 3 страны:
            # рашка с билайном, украина и вьетнам, хаха
            # ru = 0, ua = 1, vt = 10

            service_index = accessible_services[0]
            success_order = False
            while not success_order:
                actual_service = service[service_index]
                country = api.get_workable_country(actual_service)
                if country[1] == None: # если запрос с оператором
                    response = api.buy_number(actual_service, country[0], country[1])
                    if response[0]: # купили номер
                        func.key_press('tab')  # переход на код страны
                        sleep(0.1)
                        func.key_press('delete')  # удаление кода
                        sleep(0.1)
                        func.key_press('tab')  # переход на ввод номера
                        number = response[2]
                        id = response[1]
                        func.print_out(number)  # ввод номера в тг клиент
                        sleep(0.5)
                        func.image_click('next.png')
                        sleep(1)
                        if not func.image_wait_once('ok.png'):  # проверка на бан номера
                            func.image_wait('we_have_sent.png')  # ждём ввод смс
                            code = api.get_sms(id, actual_service)
                            if not code == False:
                                func.print_out(code)  # ввод кода
                                func.image_wait('your_info.png')  # ждём ввода имени и фамилии
                                func.print_out(name) # вводим имя
                                sleep(0.5)
                                func.key_press('tab')
                                sleep(0.5)
                                func.print_out(surname) # вводим фамилию
                                func.image_click('sign_up.png')
                                func.image_wait('menu.png')
                                time = datetime.datetime.now().strftime("%H:%M:%S")
                                print(f'account created at [{time}]: {number}, {name}, {surname}')
                                success_order = True
                            else:
                                print('err')
                                pass
                        else:
                            print('phone was banned. restart.')
                            func.image_click('ok.png')
                            func.image_wait('next.png')
                            sleep(0.5)
                            for i in range(0, 20):
                                func.key_press('backspace')  # удаляем старый номер, переход на новый цикл
                            sleep(0.5)
                            func.key_press('tab')
                else: # если запрос без оператора
                    response = api.buy_number(actual_service, country[0])
                    if response[0]:
                        number = response[2]
                        id = response[1]
                        func.print_out(number) # ввод номера в тг клиент
                        sleep(0.5)
                        func.image_click('next.png')
                        sleep(1)
                        if not func.image_wait_once('ok.png'): # проверка на бан номера
                            func.image_wait('we_have_sent.png') # ждём ввод смс
                            code = api.get_sms(id, actual_service)
                            if not code == False:
                                func.print_out(code) # ввод кода
                                func.image_wait('your_info.png') # ждём ввода имени и фамилии
                                func.print_out(name)
                                sleep(0.5)
                                func.key_press('tab')
                                sleep(0.5)
                                func.print_out(surname)
                                func.image_click('sign_up.png')
                                func.image_wait('menu.png')
                                time = datetime.datetime.now().strftime("%H:%M:%S")
                                print(f'account created at [{time}]: {number}, {name}, {surname}')
                                success_order = True
                            else:
                                print('err')
                                pass
                        else:
                            print('phone was banned. restart.')
                            func.image_click('ok.png')
                            func.image_wait('next.png')
                            sleep(0.5)
                            for i in range(0,20):
                                func.key_press('backspace') # удаляем старый номер, переход на новый цикл
                            sleep(0.5)
                            func.key_press('tab')
                    elif response[1] == 'no_numbers':
                        pass
                    elif response[1] == 'no_balance':
                        input(f"press enter when balance at '{service}'> 4₽.")


        #запрос api номера