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
if data2['borderless'] == 'true':
     data2['borderless']
    
else:
    data2['borderless'] = False
    
NUM_CHARS = 11
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
did_change = False
stage = 0
count = 0
ig = 0
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
        global ig
        global did_change
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
                ig = 0
                return run_time[:-3]
            else:
                did_change = True
                print(latest + "\nTime: " + run_time)
                last_amount = amount
                ig = 0
                return run_time[:-3]
    except:
        ig = 1
        return '0:00:00.000'

def window2():
    font_name = data2['font_name']
    font_size = data2['font_size']
    font_modifiers = data2['font_modifiers']
    font = (font_name, font_size, font_modifiers)
    greeting = tk.Label(fg=data2['igt_color'], bg=data2['bg_color'], font=font, textvariable=window.text)
    greeting.pack()
    greeting2 = tk.Label(fg=data2['rta_color'], bg=data2['bg_color'], font=font, textvariable=window.text2)
    greeting2.pack()
    if data2['use_counter'] == 'true':
        greeting3 = tk.Label(fg=data2['counter_color'], bg=data2['bg_color'], font=font, textvariable=window.text3)
        greeting3.pack()
        bg.gbind(data2['increment'], on_increment_counter)
        greeting.after(0, update_count)
    bg.gbind(data2['pause'], on_press)
    bg.gbind(data2['reset_start'], on_press2)
    bg.gbind(data2['exit'], clicked3)
    #window.bind("<Button-1>", clicked)
    #window.bind("<Button-3>", clicked2)
    greeting.after(0, update_time)
    greeting.after(0, update_time2)
    window.title("MCtimer")
    window.attributes('-topmost', True)
    window.overrideredirect(data2['borderless'])
    window.geometry(data2['window_pos'])
    window.mainloop()

def update_time():
    global rt
    if click1 == 1:
        window.text2.set(real_time())
    elif click1 == 0:
        rt = time.time()
    if click2 == 0:
        rt = time.time()
        window.text2.set("0:00:00.000")
    window.after(data2['rta_update'], update_time)

def update_time2():
    window.text.set(get_time())
    window.after(1500, update_time2)

def update_count():
    count_str = str(count)
    text_str = ""
    for i in range(0, int(NUM_CHARS/2)):
        text_str += " "
    text_str += count_str
    for i in range(0, int(NUM_CHARS/2)):
        text_str += " "
    window.text3.set(text_str)
    window.after(data2['rta_update'], update_count)

def on_press(event):
    left_click()

def on_press2(event):
    right_click()

def on_increment_counter(event):
    increment_counter()

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
    global count
    global did_change
    count = 0
    did_change = True
    if click2 == 1:
        click1 = 0
        click2 = 0
    elif click2 == 0:
        click2 = 1
        click1 = 1

def increment_counter():
    global count
    count += 1

def real_time():
    global rt
    global click1
    global click2
    global amount2
    global old_version
    global stage
    global ig
    global did_change
    if data2['auto_adjust'] == 'true':
        if did_change:
            rt = float(time.time()) - float(amount2)
            did_change = False
    if data2['auto_start'] == 'true':
        if ig == 1:
            rt = time.time()
            click1 = 1
            click2 = 1
            stage = 0
            return '0:00:00.000'
        elif click1 == 1:
            if old_version == True and stage == 0:
                ig = 0
                rt = float(time.time()) - float(amount2)
                rtc = str(datetime.timedelta(seconds=rt))
                stage = 1
                return rtc[:-3]
            else:
                ig = 0
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
