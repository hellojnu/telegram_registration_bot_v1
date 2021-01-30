import requests
import re
import time
from data import api_key
import functions as func
import datetime
import colorama as color

api_keys = func.read_config()[0]
accessible_services = list((api_keys.keys()))
account_count = int(func.read_config()[1])
final_result = []

def get_balance(service):
    global final_result
    for i in service:
        if i == "sms-activate":
            r = requests.get(r'https://sms-activate.ru/stubs/handler_api.php?api_key=$' + api_key[i] + '&action=getBalance')
        elif i == '5sim':
            r = requests.get(r'http://api2.5sim.net/stubs/handler_api.php?api_key=' + api_key[i] + '&action=getBalance')
        else:
            r = None
            print(f"don't know service like '{i}', sorry.")
        try:
            result = re.search(r'\d+.\d+',r.text)[0]
        except:
            result = re.search(r'\d+', r.text)[0]

        now = datetime.datetime.now().strftime("%H:%M:%S")

        if float(result)<20:
            print(color.Fore.LIGHTRED_EX + f"[{now}]-[{i}] >> balance: {result} ₽. top up the balance, please.")
        else:
            print(color.Fore.LIGHTGREEN_EX + f"[{now}]-[{i}] >> balance: {result} ₽.")
            final_result.append(i)
    return final_result

def get_number(accessible_services):
    while True:
        for i in accessible_services:
            if i == 'sms-activate':
                # response = buy_number('sms-activate', 2)
                # if response[0]:
                #     id = response[1]
                #     number = response[2]
                #     return id, number, 'sms-activate'
                response = buy_number('sms-activate', 1)
                if response[0]:
                    id = response[1]
                    number = response[2]
                    return id, number, 'sms-activate'
                response = buy_number('sms-activate', 10)
                if response[0]:
                    id = response[1]
                    number = response[2]
                    return id, number, 'sms-activate'
            elif i == '5sim':
                response = buy_number('5sim', 0)
                if response[0]:
                    id = response[1]
                    number = response[2]
                    return id, number, '5sim'
                response = buy_number('5sim', 1)
                if response[0]:
                    id = response[1]
                    number = response[2]
                    return id, number, '5sim'
        now = datetime.datetime.now().strftime("%H:%M:%S")
        print(color.Fore.LIGHTRED_EX +  f"[{now}] >> no available numbers. I'm going to sleep.")
        time.sleep(10)

def buy_number(service, country, operator = None):
    if country == 0:
        country_str = 'ru'
    elif country == 1:
        country_str = 'ua'
    elif country == 2:
        country_str = 'kz'
    else:
        country_str = 'vn'
    now = datetime.datetime.now().strftime("%H:%M:%S")
    if service == "sms-activate":
        ref = 'ref=902690'

        try:
            if operator==None:
                r = requests.get(r'https://sms-activate.ru/stubs/handler_api.php?api_key=$' + api_key[service] + f'&action=getNumber&service=$tg&{ref}&country={country}')
            else:
                r = requests.get(r'https://sms-activate.ru/stubs/handler_api.php?api_key=$' + api_key[service] + f'&action=getNumber&service=$tg&operator={operator}&{ref}&country={country}')
        except:
            print('bad api_key!')
            return False, 'bad api_key'

        if re.search('NO_NUMBER', r.text):
            print(color.Fore.LIGHTRED_EX +  f"[{now}]-[{service}] >> no available '{country_str}' number.")
            return False, 'no_numbers'
        elif re.search('NO_BALANCE',r.text):
            print(color.Fore.LIGHTRED_EX +  f'[{now}]-[{service}] >> top up balance, please.')
            #удалить сервис
            return False, 'no_balance'
        elif re.search('ACCESS_NUMBER',r.text):
            id = re.findall('\d+', r.text)[0]
            number = re.findall('\d+', r.text)[1]
            print(color.Fore.LIGHTGREEN_EX +  f"[{now}]-[{service}] >> ID: {id}, number: +{number}.")
            return True, id, number
    elif service == '5sim':
        if country == 0:
            country_5sim = 'ru_beeline'
        elif country == 1:
            country_5sim = 'ua'
        else:
            country_5sim = 'kazakhstan'
        try:
            r = requests.get(r'http://api2.5sim.net/stubs/handler_api.php?api_key=' + api_key[service] + f'&action=getNumber&country={country_5sim}&service=tg')
        except:
            print('bad api_key!')
            return False, 'bad api_key'
        if re.search('NO_NUMBER', r.text):
            print(color.Fore.LIGHTRED_EX +  f"[{now}]-[{service}] >> no available '{country_str}' number.")
            return False, 'no_numbers'
        elif re.search('NO_MEANS', r.text):
            print(color.Fore.LIGHTRED_EX +  f'[{now}]-[{service}] >> top up balance, please.')
            # удалить сервис
            return False, 'no_balance'
        elif re.search('BAD_KEY', r.text):
            print('bad api_key!')
            return False, 'bad_api_key'
        elif re.search('ACCESS_NUMBER',r.text):
            id = re.findall('\d+', r.text)[0]
            number = re.findall('\d+', r.text)[1]
            print(color.Fore.LIGHTGREEN_EX +  f"[{now}]-[{service}] >> ID: {id}, number: +{number}.")
            return True, id, number






        pass

sms_wait_count = 0

def get_sms(service, id):
    global sms_wait_count
    if sms_wait_count < 45:
        sms_wait_count += 1
        now = datetime.datetime.now().strftime("%H:%M:%S")
        if service == 'sms-activate':
            r = requests.get(r'https://sms-activate.ru/stubs/handler_api.php?api_key=$' + api_key[service] + f'&action=getFullSms&id=${id}')
            if re.search('STATUS_WAIT_CODE', r.text):
                time.sleep(1)
                return get_sms(service, id)
            elif re.search(r'FULL_SMS', r.text):


                sms_wait_count = 0
                return r.text

        elif service == '5sim':
            r = requests.get(r'http://api2.5sim.net/stubs/handler_api.php?api_key=' + api_key[service] + f'&action=getStatus&id={id}')
            if re.search('STATUS_WAIT_CODE', r.text):
                time.sleep(1)
                return get_sms(service, id)
            elif re.search(r'STATUS_OK', r.text):


                sms_wait_count = 0
                return r.text
    else:
        sms_wait_count = 0
        return False


def cancel_order(service, id):
    if service == 'sms-activate':
        r = requests.get(r'https://sms-activate.ru/stubs/handler_api.php?api_key=$' + api_key[service] + f'&action=setStatus&status=8&id=${id}')
        return r.text

    elif service == '5sim':
        r = requests.get(r'http://api2.5sim.net/stubs/handler_api.php?api_key=' + api_key[service] + f'&action=setStatus&id={id}&status=-1')
        return r.text

def confirm_order(service, id):
    if service == 'sms-activate':
        r = requests.get(r'https://sms-activate.ru/stubs/handler_api.php?api_key=$' + api_key[service] + f'&action=setStatus&status=6&id=${id}')
        return r.text

    elif service == '5sim':
        r = requests.get(r'http://api2.5sim.net/stubs/handler_api.php?api_key=' + api_key[service] + f'&action=setStatus&id={id}&status=6')
        return r.text

def set_status_wait_sms(service, id):
    if service == 'sms-activate':
        r = requests.get(r'https://sms-activate.ru/stubs/handler_api.php?api_key=$' + api_key[
            service] + f'&action=setStatus&status=1&id=${id}')
        return r.text

    elif service == '5sim':
        r = requests.get(r'http://api2.5sim.net/stubs/handler_api.php?api_key=' + api_key[
            service] + f'&action=setStatus&id={id}&status=1')
        return r.text