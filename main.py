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
            accessible_services.append(service[i])
            at_least_one_positive_balance = True


    if at_least_one_positive_balance:
        for i in range(0, account_count):
            path, name, surname = func.create_telegram_exe_and_person()
            startfile(path + '\\Telegram.exe')
            func.image_click(r'images\start_messagin.png') # жмём Start Messaging
            func.image_wait(r'images\settin.png') # ждём настроек, чтобы проверить на QR-code
            sleep(1)
            if func.image_wait_once(r'images\using_phone_number.png'): # проверка на QR-code
                func.image_click(r'images\using_phone_number.png')
            func.image_wait(r'images\ready_for_input_number.png') # форма ввода номера

            # методом проб и ошибок, юзаю 3 страны:
            # рашка с билайном, украина и вьетнам, хаха
            # ru = 0, ua = 1, vt = 10
            def input_tg_number(tab = True):
                result = api.get_number(accessible_services) # получаем номер из сервисов, где положительный баланс
                id = result[0]
                number = result[1]
                actual_service = result[2]

                if tab:
                    func.key_press('tab')  # переход на код страны
                    sleep(0.1)
                    func.key_press('delete')  # удаление кода
                    sleep(0.1)
                    func.key_press('tab')  # переход на ввод номера

                func.print_out(number)  # ввод номера в тг клиент
                sleep(0.5)
                func.image_click(r'images\next.png')
                sleep(1)

                if not func.image_wait_once(r'images\ok.png'):  # проверка на бан номера
                    func.image_wait(r'images\we_have_sent.png')  # ждём ввод смс

                    api.set_status_wait_sms(actual_service, id) # установка статуса "жду смс"

                    code = api.get_sms(actual_service, id)
                    if not code == False: # если код получили
                        clear_code = re.search(r'\d+', code)[0]
                        func.print_out(clear_code)  # ввод кода
                        func.image_wait(r'images\your_info.png')  # ждём ввода имени и фамилии
                        sleep(1)
                        func.print_out(name)  # вводим имя
                        sleep(0.5)
                        func.key_press('tab')
                        sleep(0.5)
                        func.print_out(surname)  # вводим фамилию
                        func.image_click(r'images\sign_up.png')
                        func.image_wait(r'images\menu.png')
                        time = datetime.datetime.now().strftime("%H:%M:%S")
                        api.confirm_order(actual_service, id)
                        print(f'account created at [{time}]: +{number}, {name} {surname}.')
                        func.kill_telegram()
                    else: # если код идёт больше минуты
                        api.cancel_order(actual_service, id)
                        print('phone was banned. restart.')
                        func.image_click(r'images\back.png')
                        sleep(0.5)
                        for i in range(0, 15):
                            func.key_press('backspace')  # удаляем старый номер, переход на новый цикл
                        sleep(0.5)
                        func.key_press('tab')
                        input_tg_number(False)

                else:
                    api.cancel_order(actual_service, id)
                    print('phone was banned. restart.')
                    func.image_click(r'images\ok.png')
                    func.image_wait(r'images\next.png')
                    sleep(0.5)
                    for i in range(0, 15):
                        func.key_press('backspace')  # удаляем старый номер, переход на новый цикл
                    sleep(0.5)
                    func.key_press('tab')
                    input_tg_number(False)


            input_tg_number()

            #service_index = accessible_services[0]
            #success_order = False

                    # elif response[1] == 'no_numbers':
                    #     pass
                    # elif response[1] == 'no_balance':
                    #     input(f"press enter when balance at '{service}'> 4₽.")


        #запрос api номера