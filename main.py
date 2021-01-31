import shutil
import os
from pyautogui import *
from os import startfile
import functions as func
import api as api
import datetime
from api import api_keys, account_count, accessible_services
import colorama as color
import pyautogui as py
from keyboard import press_and_release

acc_services = accessible_services
ban_count = 0
if __name__ == "__main__":
    func.beautiful_print(" [TELEGRAM REGISTRATION BOT V1] ")
    if len(api_keys)>0 and account_count>0: # если есть хотя бы 1 api и число акков > 0
        accessible_services = api.get_balance(accessible_services)

        if len(accessible_services)>0: # если есть хотя бы 1 сервис с позитивным балансом
            def start_creating():

                for i in range(0, account_count):
                    path, name, surname = func.create_telegram_exe_and_person()
                    print(name, surname)
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
                        global ban_count
                        if len(accessible_services)>0:
                            result = api.get_number(accessible_services) # получаем номер из сервисов, где положительный баланс

                            if not result[0]:
                                accessible_services.remove(result[1])
                                input_tg_number()

                            id = result[0]
                            number = result[1]
                            actual_service = result[2]

                            if tab:
                                func.key_press('tab')  # переход на код страны
                                sleep(0.1)
                                func.key_press('delete')  # удаление кода
                                sleep(0.1)
                                func.key_press('tab')  # переход на ввод номера

                            func.print_out(number, 0.1)  # ввод номера в тг клиент
                            sleep(0.5)
                            func.image_click(r'images\next.png')
                            sleep(1)

                            if not func.image_wait_once_or(r'images\ok.png', r'images\too_many_tries.png'):  # проверка на бан номера или too many tries
                                func.image_wait_or(r'images\we_have_sent.png', r'images\already_registered.png')  # ждём ввод смс
                                already_registered = False
                                if func.image_wait_once(r'images\already_registered.png'):
                                    func.image_click(r'images\send_code_via_sms.png')
                                    already_registered = True
                                api.set_status_wait_sms(actual_service, id) # установка статуса "жду смс"

                                code = api.get_sms(actual_service, id)
                                if not code == False: # если код получили
                                    clear_code = re.search(r'\d+', code)[0]
                                    now = datetime.datetime.now().strftime("%H:%M:%S")
                                    print(color.Fore.LIGHTGREEN_EX + f"[{now}]-[{actual_service}] >> code: {clear_code}.")
                                    func.print_out(clear_code, 0.1)  # ввод кода
                                    if not already_registered:
                                        func.image_wait(r'images\your_info.png')  # ждём ввода имени и фамилии
                                        func.image_click(r'images\your_info.png')
                                        sleep(1)
                                        print(name, surname)
                                        func.print_out(name, 0.1)  # вводим имя ПАЧИМУ НЕ РАБОТАЕТ
                                        sleep(0.5)
                                        func.key_press('tab')
                                        sleep(0.5)
                                        func.print_out(surname, 0.1)  # вводим фамилию
                                        func.image_click(r'images\sign_up.png')
                                        func.image_wait(r'images\menu.png')
                                        now = datetime.datetime.now().strftime("%H:%M:%S")
                                        api.confirm_order(actual_service, id)
                                        print(color.Fore.LIGHTCYAN_EX + f"[{now}]-[{actual_service}] >> created account: +{number}, {name} {surname}.")
                                        func.kill_telegram()
                                        sleep(3)
                                        os.rename(path, 'accounts' + rf'\{number}')
                                    else:
                                        sleep(3)
                                        now = datetime.datetime.now().strftime("%H:%M:%S")
                                        api.confirm_order(actual_service, id)
                                        if func.image_wait_once(r'images\menu.png'):
                                            print(color.Fore.LIGHTBLUE_EX + f"[{now}]-[{actual_service}] >> logged in already created account: +{number}.")
                                            func.kill_telegram()
                                        else:
                                            print(color.Fore.LIGHTRED_EX + f"[{now}]-[{actual_service}] >> tried to log in already created account: +{number}, but the account has a 2FA password.")
                                            func.kill_telegram()
                                            shutil.rmtree(path)


                                else: # если код идёт больше минуты

                                    api.cancel_order(actual_service, id)
                                    now = datetime.datetime.now().strftime("%H:%M:%S")
                                    print(color.Fore.LIGHTRED_EX + f"[{now}]-[{actual_service}] >> +{number} was banned. ")
                                    func.image_click(r'images\back.png')
                                    func.image_wait(r'images\+.png')
                                    sleep(2)
                                    press_and_release('ctrl + a')  # удаляем старый номер, переход на новый цикл
                                    sleep(0.1)
                                    func.key_press('del')
                                    ban_count+=1
                                    if ban_count<=5:
                                        input_tg_number(False)
                                    else:
                                        ban_count=0
                                        accessible_services.remove(actual_service)
                            else:
                                now = datetime.datetime.now().strftime("%H:%M:%S")
                                if not func.image_wait_once(r'images\too_many_tries.png'):
                                    api.cancel_order(actual_service, id)

                                    print(color.Fore.LIGHTRED_EX + f"[{now}]-[{actual_service}] >> +{number} was banned. ")
                                    func.image_click(r'images\ok.png')
                                    func.image_wait(r'images\next.png')
                                    sleep(2)
                                    press_and_release('ctrl + a')  # удаляем старый номер, переход на новый цикл
                                    sleep(0.1)
                                    func.key_press('del')
                                    ban_count += 1
                                    if ban_count <= 5:
                                        input_tg_number(False)
                                    else:
                                        ban_count = 0
                                        accessible_services.remove(actual_service)
                                else:
                                    print(color.Fore.LIGHTRED_EX + f"[{now}] >> too many tries. I'm going to sleep about 10 minutes.")
                                    func.kill_telegram()
                                    shutil.rmtree(path)
                                    time.sleep(600)
                                    start_creating()
                        else:
                            now = datetime.datetime.now().strftime("%H:%M:%S")
                            if len(api.get_balance(acc_services))==0:

                                print(color.Fore.LIGHTRED_EX + f"[{now}] >> нет доступного баланса ни на одном из сервисов. пополните счёт и перезапустите скрипт.")
                                sys.exit()
                            else:
                                print(color.Fore.LIGHTRED_EX + f"[{now}] >> было слишком много банов номеров, я посплю минутку.")
                                sleep(60)
                                input_tg_number(False)

                    input_tg_number()
            start_creating()