import requests
import re
import time

api_key_sms_activate = 'api_key'

request_ex = r'https://sms-activate.ru/stubs/handler_api.php?api_key=$' + api_key_sms_activate

def get_balance(service):
    if service == "sms-activate":
        r = requests.get(request_ex + '&action=getBalance')
    else:
        r = None
        print("don't know any except sms-activate")
    try:
        result = re.search(r'\d+.\d+',r.text)
    except:
        result = re.search(r'\d+', r.text)
    print(f'balance: {result[0]} ₽.')
    return result[0]

def get_available_numbers(service, country, operator = None):
    if service=='sms-activate':
        if not operator == None:
            r = requests.get(request_ex + f'&action=getNumbersStatus&country=${country}&operator={operator}')
        else:
            r = requests.get(request_ex + f'&action=getNumbersStatus&country=${country}')
        if r.text == 'WRONG_OPERATOR.' or r.text == 'WRONG_OPERATOR':
            print(f'wrong operator "{operator}".')
        else:
            temp = r.text
            res = re.search(r'"tg_0": "\d+"', temp)
            res1 = re.search(r'"\d+"', res[0])
            return res1[0], country
        return '0'


def get_workable_country(service):
    key = 0
    if service == 'sms-activate':
        while key == 0:
            if not get_available_numbers(service, 0,'beeline')[0]=='0':
                country = get_available_numbers(service, 0)[1]
                print(f"found free number in {country}. startin' the creatin'.")
                key = 1
                return country
            elif not get_available_numbers(service, 1)[0]=='0':
                country = get_available_numbers(service, 1)[1]
                print(f"found free number in {country}. startin' the creatin'.")
                key = 1
                return country
            elif not get_available_numbers(service, 10)[0]=='0':
                country = get_available_numbers(service, 10)[1]
                print(f"found free number in {country}. startin' the creatin'.")
                key = 1
                return country
            else:
                print("there is now free numbers. i'm sleepin'.")
                time.sleep(10)
