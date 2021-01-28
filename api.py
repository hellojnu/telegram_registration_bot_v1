import requests
import re
import time
from data import api_key


def get_balance(service):
    if service == "sms-activate":
        r = requests.get(r'https://sms-activate.ru/stubs/handler_api.php?api_key=$' + api_key[service] + '&action=getBalance')
    elif service == '5sim':
        r = requests.get(r'http://api2.5sim.net/stubs/handler_api.php?api_key=' + api_key[service] + '&action=getBalance')
    else:
        r = None
        print("don't know any except sms-activate")
    try:
        result = re.search(r'\d+.\d+',r.text)
    except:
        result = re.search(r'\d+', r.text)
    print(f"balance at '{service}': {result[0]} ₽.")
    return result[0]

def get_available_numbers(service, country, operator = None):
    if service=='sms-activate':
        if not operator == None:
            r = requests.get(r'https://sms-activate.ru/stubs/handler_api.php?api_key=$' + api_key[service] + f'&action=getNumbersStatus&country=${country}&operator={operator}')
        else:
            r = requests.get(r'https://sms-activate.ru/stubs/handler_api.php?api_key=$' + api_key[service] + f'&action=getNumbersStatus&country=${country}')
        if r.text == 'WRONG_OPERATOR.' or r.text == 'WRONG_OPERATOR':
            print(f'wrong operator "{operator}".')
        else:
            temp = r.text
            res = re.search(r'"tg_0": "0"', temp)
            if res:
                return '0', country
        return '0'


def get_workable_country(service):
    key = 0
    if service == 'sms-activate':
        printed = False
        while key == 0:
            if not get_available_numbers(service, 0,'beeline')[0]=='0':
                country = get_available_numbers(service, 0)[1]
                key = 1
                return country, 'beeline'
            elif not get_available_numbers(service, 1)[0]=='0':
                country = get_available_numbers(service, 1)[1]
                key = 1
                return country, None
            elif not get_available_numbers(service, 10)[0]=='0':
                country = get_available_numbers(service, 10)[1]
                key = 1
                return country, None
            else:
                if not printed:
                    print(f"there is now free numbers at '{service}'. i'm waitin for a number.")
                    printed = True
                    # if len(accessible_services) == 1:
                    #     print(f"there is now free numbers at '{service}'. i'm waitin for number.")
                    #     printed = True
                    # elif len(accessible_services) > 1:
                    #     print(f"there is now free numbers at '{service}'. try to use another service...")
                          # придумать переход
                time.sleep(3)


def get_number(accessible_services):
    while True:
        for i in accessible_services:
            if i == 'sms-activate':
                response = buy_number('sms-activate', 0, 'beeline')
                if response[0]:
                    id = response[1]
                    number = response[2]
                    return id, number, 'sms-activate'
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
        print("there are really no any numbers. sleepin'.")
        time.sleep(10)

def buy_number(service, country, operator = None):
    if service == "sms-activate":
        ref = 'ref=902690'

        try:
            if operator==None:
                r = requests.get(r'https://sms-activate.ru/stubs/handler_api.php?api_key=$' + api_key[service] + f'&action=getNumber&service=$tg&{ref}&country=${country}')
            else:
                r = requests.get(r'https://sms-activate.ru/stubs/handler_api.php?api_key=$' + api_key[service] + f'&action=getNumber&service=$tg&operator={operator}&{ref}&country=${country}')
        except:
            print('bad api_key!')
            return False, 'bad api_key'

        if re.search('NO_NUMBER', r.text):
            print(f'there is now available numbers at {service}: {country}.')
            return False, 'no_numbers'
        elif re.search('NO_BALANCE',r.text):
            print(f'top up balance at {service}!')
            return False, 'no_balance'
        elif re.search('ACCESS_NUMBER',r.text):
            id = re.findall('\d+', r.text)[0]
            number = re.findall('\d+', r.text)[1]
            print(f'success at {service}. id: {id}; number: {number}.')
            return True, id, number
    elif service == '5sim':
        if country == 0:
            country_5sim = 'ru_beeline'
        elif country == 1:
            country_5sim = 'ua'

        try:
            r = requests.get(r'http://api2.5sim.net/stubs/handler_api.php?api_key=' + api_key[service] + f'&action=getNumber&country={country}&service=tg')
        except:
            print('bad api_key!')
            return False, 'bad api_key'

        if re.search('NO_NUMBER', r.text):
            print(f'there is now available numbers at {service}: {country}.')
            return False, 'no_numbers'
        elif re.search('NO_MEANS', r.text):
            print(f'top up balance at {service}!')
            return False, 'no_balance'
        elif re.search('BAD_KEY', r.text):
            print('bad api_key!')
            return False, 'bad_api_key'
        elif re.search('ACCESS_NUMBER',r.text):
            id = re.findall('\d+', r.text)[0]
            number = re.findall('\d+', r.text)[1]
            print(f'success at {service}. id: {id}; number: {number}.')
            return True, id, number






        pass

sms_wait_count = 0

def get_sms(service, id):
    global sms_wait_count
    if sms_wait_count < 60:
        sms_wait_count += 1
        if service == 'sms-activate':
            r = requests.get(r'https://sms-activate.ru/stubs/handler_api.php?api_key=$' + api_key[service] + f'&action=getFullSms&id=${id}')
            if re.search('STATUS_WAIT_CODE', r.text):
                time.sleep(1)
                return get_sms(service, id)
            elif re.search(r'FULL_SMS', r.text):
                print("success: i got the sms.")
                sms_wait_count = 0
                return r.text

        elif service == '5sim':
            r = requests.get(r'http://api2.5sim.net/stubs/handler_api.php?api_key=' + api_key[service] + f'&action=getStatus&id={id}')
            if re.search('STATUS_WAIT_CODE', r.text):
                time.sleep(1)
                return get_sms(service, id)
            elif re.search(r'STATUS_OK', r.text):
                print("success: i got the sms.")
                sms_wait_count = 0
                return r.text
    else:
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