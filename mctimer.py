import os
import sys
import platform
import json
import glob
import datetime
import time
import tkinter as tk
from bindglobal import BindGlobal

#"THE BEER-WARE LICENSE" (Revision 42):
#bleach86 wrote this file. As long as you retain this notice you can do whatever you want with this stuff. 
#If we meet some day, and you think this stuff is worth it, you can buy me a beer in return

json_file = 'mct_config.json'
with open(json_file) as json_file:
    data2 = json.load(json_file)
    

system_type = platform.system()
if system_type == 'Linux':
    directory = os.path.expanduser(data2['linux_saves'])
elif system_type == 'Darwin':
    directory = os.path.expanduser(data2['mac_saves'])
elif system_type == 'Windows':
    directory = os.path.expanduser(data2['windows_saves'])
amount2 = 0
last_amount = 0
window = tk.Tk()
bg = BindGlobal(widget=window)
window.text = tk.StringVar()
window.text2 = tk.StringVar()
rt = time.time()
old_version = False
count = 0
if data2['auto_start'] == 'true':
    click1 = 1
    click2 = 1
else:
    click1 = 0
    click2 = 0

def get_time():

    try:
        global last_amount
        global old_version
        global amount2
        #time.sleep(0.1)
        latest = max([os.path.join(directory,d) for d in os.listdir(directory)], key=os.path.getmtime)
        
        if system_type == "Linux" or system_type == "Darwin":
            os.chdir(latest + '/stats/')
            
        else:
            os.chdir(latest + '\\stats\\')
        json_file = glob.glob('*.json')
        timer = json_file[0]
        
        with open(timer) as json_file:
            data = json.load(json_file)
            try:
                amount = data['stats']['minecraft:custom']['minecraft:play_one_minute']
            except:
                amount = data['stat.playOneMinute']
                old_version = True
            json_file.close()
            amount2 = float(amount) / 20
            run_time = str(datetime.timedelta(seconds=amount2, milliseconds=0.5))
    
            if last_amount == amount:
                return run_time[:-3]
            else:
                print(latest + "\nTime: " + run_time)
                last_amount = amount
                return run_time[:-3]
    except:
        return '0:00:00.000'

def window2():
    greeting = tk.Label(fg=data2['igt_color'], bg=data2['bg_color'], font="Arial 45 bold", textvariable=window.text)
    greeting.pack()
    greeting2 = tk.Label(fg=data2['rta_color'], bg=data2['bg_color'], font="Arial 45 bold", textvariable=window.text2)
    greeting2.pack()
    bg.gbind(data2['pause'], on_press)
    bg.gbind(data2['reset_start'], on_press2)
    bg.gbind(data2['exit'], clicked3)
    window.bind("<Button-1>", clicked)
    window.bind("<Button-3>", clicked2)
    greeting.after(0, update_time)
    window.title("MCtimer")
    window.attributes('-topmost', True)
    window.overrideredirect(True)
    window.geometry(data2['window_pos'])
    window.mainloop()

def update_time():
    global rt
    window.text.set(get_time())
    if click1 == 1:
        window.text2.set(real_time())
    elif click1 == 0:
        rt = time.time()
    if click2 == 0:
        rt = time.time()
        window.text2.set("0:00:00.000")
    window.after(data2['rta_update'], update_time)

def on_press(event):
    left_click()

def on_press2(event):
    right_click()

def clicked3(event):
    sys.exit(1)

def clicked2(event):
    right_click()

def clicked(event):
    left_click()

def left_click():
    global click1
    if click1 == 1:
        click1 = 0
    elif click1 == 0:
        click1 = 0

def right_click():
    global click1
    global click2
    if click2 == 1:
        click1 = 0
        click2 = 0
    elif click2 == 0:
        click2 = 1
        click1 = 1

def real_time():
    global rt
    global click1
    global click2
    global amount2
    global old_version
    global count
    if data2['auto_start'] == 'true':
        if get_time() == '0:00:00.000':
            rt = time.time()
            click1 = 1
            click2 = 1
            count = 0
            return '0:00:00.000'
        elif click1 == 1:
            if old_version == True and count == 0:
                rt = float(time.time()) - float(amount2)
                rtc = str(datetime.timedelta(seconds=rt))
                count = 1
                return rtc[:-3]
            else:
                rt2 = time.time()
                real_time = rt2 - rt
                rtc = str(datetime.timedelta(seconds=real_time))
                return rtc[:-3]
    else:
        if click1 == 1:
            rt2 = time.time()
            real_time = rt2 - rt
            rtc = str(datetime.timedelta(seconds=real_time))
            return rtc[:-3]

def main():
    window2()

main()
