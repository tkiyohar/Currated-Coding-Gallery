import pip
import subprocess
packagecheck = subprocess.run('py -m pip list', capture_output=True)
packagecheck = packagecheck.stdout.decode("utf-8")
if "PyAutoGUI" not in packagecheck: 
  subprocess.run('py -m pip install PyAutoGUI')
if "keyboard" not in packagecheck: 
  subprocess.run('py -m pip install keyboard')

import pyautogui
import keyboard
import time
import webbrowser

print("SorBa_2.0 is running... press the \"0\" key to quit.")
width, height = pyautogui.size()
x, y = 640/2560*width, 1200/1600*height
spanishdict = False

while True:
  if keyboard.is_pressed('shift'):
    x, y = pyautogui.position()
    time.sleep(0.3)
    pyautogui.click(clicks=2)
    pyautogui.hotkey('ctrl', 'c')
    pyautogui.click(1583/2560*width, 1295/1600*height)
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.press('tab')
    time.sleep(0.3)
    pyautogui.press('pagedown')
  elif keyboard.is_pressed('1'):
    pyautogui.press('backspace')
    pyautogui.click(2195/2560*width, 1200/1600*height)
    pyautogui.press('tab')
    time.sleep(0.3)
    pyautogui.press('pagedown')
    pyautogui.moveTo(x, y)
  elif keyboard.is_pressed('2'):
    pyautogui.press('backspace')
    pyautogui.click(2195/2560*width, 1245/1600*height)
    pyautogui.press('tab')
    time.sleep(0.3)
    pyautogui.press('pagedown')
    pyautogui.moveTo(x, y)
  elif keyboard.is_pressed('3'):
    pyautogui.press('backspace')
    pyautogui.click(2195/2560*width, 1290/1600*height)
    pyautogui.press('tab')
    time.sleep(0.3)
    pyautogui.press('pagedown')
    pyautogui.moveTo(x, y)
  elif keyboard.is_pressed('capslock'):
    pyautogui.moveTo(1320/2560*width, 1290/1600*height)
    pyautogui.click(1320/2560*width, 1290/1600*height)
    time.sleep(0.15)
    pyautogui.click(1583/2560*width, 1295/1600*height)
    pyautogui.press('capslock')
    pyautogui.press('tab')
    pyautogui.press('tab')
    time.sleep(0.3)
    pyautogui.press('pagedown')
    time.sleep(0.15)
    pyautogui.click(1400/2560*width, 1192/1600*height)
    pyautogui.click(1583/2560*width, 1295/1600*height)
    time.sleep(0.3)
    pyautogui.press('pagedown')
    pyautogui.moveTo(x, y)
  elif keyboard.is_pressed('tab'):
    time.sleep(0.4)
    pyautogui.press('pagedown')
  elif keyboard.is_pressed('4'):
    if spanishdict == False:
      pyautogui.press('backspace')
      pyautogui.moveTo(1320/2560*width, 1290/1600*height)
      pyautogui.click(1320/2560*width, 1290/1600*height)
      time.sleep(0.15)
      pyautogui.click(1583/2560*width, 1295/1600*height, clicks=2)
      pyautogui.hotkey('ctrl', 'c')
      pyautogui.moveTo(1320/2560*width, 1290/1600*height)
      pyautogui.click(1320/2560*width, 1290/1600*height)
      time.sleep(0.15)
      pyautogui.click(270/2560*width, 24/1600*height)
      pyautogui.hotkey('ctrl', 'v')
      pyautogui.press('enter')
      time.sleep(0.3)
      pyautogui.click(2330/2560*width, 1290/1600*height)
      spanishdict = True
      pyautogui.press('pagedown')
    elif spanishdict == True:
      pyautogui.press('backspace')
      pyautogui.click(80/2560*width, 24/1600*height)
      pyautogui.click(2330/2560*width, 1290/1600*height)
      time.sleep(0.3)
      pyautogui.press('pagedown')
      pyautogui.moveTo(x, y)
      spanishdict = False
  elif keyboard.is_pressed('0'):
    pyautogui.press('backspace')
    break
  else:
    pass