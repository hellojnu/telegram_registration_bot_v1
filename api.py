import requests
import re
import time
from data import api_key
from main import accessible_services

def get_balance(service):
    if service == "sms-activate":
        r = requests.get(r'https://sms-activate.ru/stubs/handler_api.php?api_key=$' + api_key[service] + '&action=getBalance')
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

                    if len(accessible_services) == 1:
                        print(f"there is now free numbers at '{service}'. i'm waitin for number.")
                        printed = True
                    elif len(accessible_services) > 1:
                        print(f"there is now free numbers at '{service}'. try to use another service...")
                        # придумать переход
                time.sleep(3)

def buy_number(service, country, operator = None):
    ref = 'ref=902690'
    if service == "sms-activate":
        if operator==None:
            r = requests.get(r'https://sms-activate.ru/stubs/handler_api.php?api_key=$' + api_key[service] + f'&action=getNumber&service=$tg&{ref}&country=${country}')
        else:
            r = requests.get(r'https://sms-activate.ru/stubs/handler_api.php?api_key=$' + api_key[service] + f'&action=getNumber&service=$tg&operator={operator}&{ref}&country=${country}')
        if r.text=='NO_NUMBERS' or r.text=='NO_NUMBERS.':
            print('there is now available numbers.')
            return False, 'no_numbers'
        elif r.text=='NO_BALANCE' or r.text=='NO_BALANCE.':
            print('top up balance!')
            return False, 'no_balance'
        elif re.search('ACCESS_NUMBER',r.text):
            id = re.findall('\d+', r.text)[0]
            number = re.findall('\d+', r.text)[1]
            print(f'success: id #{id}; number #{number}.')
            return True, id, number

def get_sms(id, service):
    if service == 'sms-activate':
        r = requests.get(r'https://sms-activate.ru/stubs/handler_api.php?api_key=$' + api_key[service] + f'&action=getFullSms&id=${id}')
        print(r.text)
        if r.text=='STATUS_WAIT_CODE':
            time.sleep(1)
            get_sms(id, service)
        elif r.text=='STATUS_CANCEL':
            return False
        elif re.search(r'FULL_SMS', r.text):
            print("success: i got the sms.")
            return r.text
        else:
            return False
