import pyperclip
from pyautogui import *
import pyautogui
import time
import keyboard
import numpy as np
import win32api, win32con
import os
import signal
import psutil
import colorama as color
from russian_names import RussianNames
from shutil import copy2
import pyautogui, pyperclip
from keyboard import press_and_release

names = []


def beautiful_print(text):
    length = 70
    if len(text)%2:
        length+=1
    print(color.Fore.LIGHTMAGENTA_EX + ('{0:*^' + str(length) +'}').format(text))

def get_list_of_dirs():  # получили список папок
    path = 'D:\\work\\telegram\\аккаунты\\'
    global names
    names = [names for names in os.listdir(path)]
    return names



def click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

def image_click(image):
    '''Click on the image. Region is the whole screen.'''
    if not pyautogui.locateOnScreen(image, grayscale=True, confidence=0.9) == None:
        x_y = pyautogui.locateOnScreen(image, grayscale=True, confidence=0.9)
        click(x_y[0], x_y[1])
        return True
    else:
        time.sleep(0.1)
        image_click(image)

def image_wait_or_region(image1,image2,region):
    '''Wait at least one of two images. Region is the whole screen.'''
    if pyautogui.locateOnScreen(image1, region=region, grayscale=True, confidence=0.9) != None:
        return True
    elif pyautogui.locateOnScreen(image2, grayscale=True, region=region, confidence=0.9) != None:
        return True
    else:
        time.sleep(0.1)
        image_wait_or_region(image1,image2,region)

def image_wait_or(image1,image2):
    '''Wait at least one of two images. Region is the whole screen.'''
    if pyautogui.locateOnScreen(image1, grayscale=True, confidence=0.9) != None:
        return True
    elif pyautogui.locateOnScreen(image2, grayscale=True, confidence=0.9) != None:
        return True
    else:
        time.sleep(0.1)
        image_wait_or(image1,image2)

copy_paste = None

def copy_present(image):
    '''Copy text.'''
    global copy_paste
    if copy_paste == None:
        if pyautogui.locateOnScreen(image, grayscale=True, confidence=0.9) != None:
            x_y = pyautogui.locateOnScreen(image, grayscale=True, confidence=0.9)
            click(x_y[0], x_y[1])
            sleep(0.1)
            click(x_y[0], x_y[1])
            sleep(0.1)
            pyautogui.hotkey('ctrl', 'c')
            sleep(0.1)
            copy_paste = pyperclip.paste()
        else:
            time.sleep(0.1)


def image_click_region(image, region):
    '''Click on the image in a specific region'''
    while (keyboard.is_pressed('esc') == False):
        if pyautogui.locateOnScreen(image, region=region, grayscale=True, confidence=0.9) != None:
            x_y = pyautogui.locateOnScreen(image, region=region, grayscale=True, confidence=0.9)
            click(x_y[0], x_y[1])
            return True
        else:
            time.sleep(0.1)


def image_click_region_or(image1,image2, region):
    '''Click on the image in a specific region'''
    try:
        x_y = pyautogui.locateOnScreen(image1, region=region, grayscale=True, confidence=0.9)
        click(x_y[0], x_y[1])
    except:
        try:
            x_y = pyautogui.locateOnScreen(image2, region=region, grayscale=True, confidence=0.9)
            click(x_y[0], x_y[1])
        except:
            sleep(0.1)
            image_click_region_or(image1, image2, region)
    return True


def image_wait(image):
    '''Waiting the picture. Region is the whole screen.'''
    while (keyboard.is_pressed('esc') == False):
        if pyautogui.locateOnScreen(image, grayscale=True, confidence=0.9) != None:
            return True
        else:
            time.sleep(0.1)

def image_wait_region(image, region):
    '''Click on the image in the specific region'''
    if pyautogui.locateOnScreen(image, region=region, grayscale=True, confidence=0.9) != None:
        return True
    else:
        time.sleep(0.1)
        image_wait_region(image, region)

def loadin_wait_region(image, region):
    '''Click on the image in the specific region'''
    if pyautogui.locateOnScreen(image, region=region, grayscale=True, confidence=0.9) == None:
        return True
    else:
        time.sleep(0.1)
        loadin_wait_region(image, region)

def image_wait_once_or(image1, image2):
    '''Check, if the image is on the screen. Region is the whole screen.'''
    try:
        if pyautogui.locateOnScreen(image1, grayscale=True, confidence=0.9) != None:
            return True
    except:
        try:
            if pyautogui.locateOnScreen(image2, grayscale=True, confidence=0.9) != None:
                return True
        except:
            return False


def image_wait_once_region(image, region):
    '''Check, if the image is in the specific region.'''
    if pyautogui.locateOnScreen(image, region=region, grayscale=True, confidence=0.9) != None:
        return True
    else:
        return False

def image_wait_once(image):
    '''Check, if the image is in the specific region.'''
    if pyautogui.locateOnScreen(image, grayscale=True, confidence=0.9) != None:
        return True
    else:
        return False

def kill_telegram():
    for process in psutil.process_iter():
        if process.name() == 'Telegram.exe':
            os.kill(process.pid, signal.SIGTERM)


def paste(text: str):
    pyperclip.copy(text)
    press_and_release('ctrl + v')

def print_out(text: str, interval=0.0):
    buffer = pyperclip.paste()
    if not interval:
        paste(text)
    else:
        for char in text:
            paste(char)
            sleep(interval)
    pyperclip.copy(buffer)
    #
    # for i in text:
    #     pyautogui.typewrite(i)

def create_telegram_exe_and_person():
    try:
        person = RussianNames(patronymic=False, output_type='dict', count=1).get_batch()
        name = person[0]["name"]
        surname = person[0]["surname"]
        time = datetime.datetime.now().strftime("%H_%M_%S")
        os.makedirs('accounts' + f'\\{name}_{surname}_{time}')
        copy2('Telegram.exe', r'accounts' + f'\\{name}_{surname}_{time}')
        path = 'accounts' + f'\\{name}_{surname}_{time}'
        return path, name, surname
    except:
        pass

def read_config():
    api_keys = {}
    account_counter = 0
    with open('config.txt', 'r') as f:
        string = f.read().splitlines()
    for str in string:
        if re.match(r'sms-activate',str):
            key_t = re.search(r'".+"', str)[0]
            key = re.search(r'\w+', key_t)[0]
            if len(key) == 32:
                api_keys["sms-activate"] = key
        elif re.match(r'5sim',str):
            key_t = re.search(r'".+"', str)[0]
            key = re.search(r'\w+', key_t)[0]
            if len(key) == 32:
                api_keys["5sim"] = key
        elif re.match(r'account_counter', str):
            account_counter = re.search(r'\d+', str)[0]
    return api_keys, account_counter


def key_press(key):
    pyautogui.keyDown(key)
    sleep(np.random.uniform(0.01, 0.02))
    pyautogui.keyUp(key)


def get_docks():
    name = get_list_of_dirs()
    name_array = []
    i2 = 0
    for i1 in range(0, (len(name)) // 9): #получаю целые доки в 9 акков
        temp_list = []
        for i in name[i2:i2 + 9:]:
            #print(f'{name.index(i)+1}: ' + i)
            temp_list.append(i)
        name_array.append(temp_list)
        i2 += 9

    temp_list = []
    for i2 in range(i2, len(name)): #добиваю в последний док оставшиеся аккаунты
        temp_list.append(name[i2])

    name_array.append(temp_list)

    return name_array

def set_regions(i):
    x = 0
    y = 0
    w = 380
    h = 500

    if i<=4:
        for i1 in range(0,i):
            x+=380
    elif i>=5 and i<=8:
        x=0
        y=540
        for i1 in range(5,i):
            x+=380

    list = [x, y, w, h]
    return list

region = []

def get_regions():
    global region
    for i in range(0, 9):
        region += [set_regions(i)]


