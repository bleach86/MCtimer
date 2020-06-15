import os
import platform
import json
import glob
import datetime
import time
import tkinter as tk

system_type = platform.system()
if system_type == 'Linux':
    directory = os.path.expanduser('~/.minecraft/saves/')
elif system_type == 'Darwin':
    directory = os.path.expanduser('~/Library/Application Support/minecraft/saves/')
elif system_type == 'Windows':
    directory = os.path.expanduser('~\\AppData\\Roaming\\.minecraft\\saves\\')

last_amount = 0
window = tk.Tk()
window.text = tk.StringVar()
window.text2 = tk.StringVar()
rt = time.time()
click1 = 1

def get_time():

    try:
        global last_amount
        time.sleep(0.1)
        latest = max([os.path.join(directory,d) for d in os.listdir(directory)], key=os.path.getmtime)
        
        if system_type == "Linux" or system_type == "Darwin":
            os.chdir(latest + '/stats/')
            
        else:
            os.chdir(latest + '\\stats\\')
        json_file = glob.glob('*.json')
        timer = json_file[0]
        
        with open(timer) as json_file:
            data = json.load(json_file)
            amount = data['stats']['minecraft:custom']['minecraft:play_one_minute']
            #amount = data['stat.playOneMinute']
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
        pass

def window2():
    greeting = tk.Label(fg="lime", bg="black", font="Arial 45 bold", textvariable=window.text)
    greeting.pack()
    greeting2 = tk.Label(fg="red", bg="black", font="Arial 45 bold", textvariable=window.text2)
    greeting2.pack()
    window.bind("<Button-1>", clicked)
    greeting.after(0, update_time)
    window.title("MCtimer")
    window.attributes('-topmost', True)
    window.geometry("+0+0")
    window.mainloop()

def update_time():
    window.text.set(get_time())
    window.text2.set(real_time())
    window.after(1000, update_time)
    
def clicked(event):
    left_click()

def left_click():
    global click1
    if click1 == 1:
        click1 = 0
    elif click1 == 0:
        click1 = 1

def real_time():
    global rt
    global click1
    if get_time() == None:
        rt = time.time()
        click1 = 1
        return None
    elif click1 == 1:
        rt2 = time.time()
        real_time = rt2 - rt
        rtc = str(datetime.timedelta(seconds=real_time))
        return rtc[:-3]
        
    elif click1 == 0:
        rt = time.time()
        return "0:00:00.000"

def main():
    window2()

main()
