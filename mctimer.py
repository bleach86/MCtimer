import atexit
import os
import sys
import platform
import json
import glob
import datetime
import time
import threading
import tkinter as tk
from pynput import mouse
from pathlib import Path
from playsound import playsound
from enum import Enum

import copy

#"THE BEER-WARE LICENSE" (Revision 42):
#bleach86 wrote this file. As long as you retain this notice you can do whatever you want with this stuff. 
#If we meet some day, and you think this stuff is worth it, you can buy me a beer in return




input_fil = Path("/Users/sharpieman20/MCtimer/MCtimer") / "input.txt"

# continuously read from input file every 10ms
# when you get a "reset timer" message, reset the timer
# 


# class Category:

#     def __init__():
#         self.actions = []
#         self.attempts = []

#         # convert actions to attempts


#     def read():


#     def write():


# class Actions(Enum):
#     CREATE_WORLD = 0
#     START = 1





# class Attempt:
stage = 0
ind = 0
time_count = 0

rsg = [
    ("World Created", True),
    ([
        "Savannah",
        "Desert",
        "Plains",
        "Other"
    ], False),
    ([
        "0-15",
        "15-30",
        "30-45",
        "45-60",
        "60-75",
        "75+"
    ], False),
    ([
        "Iron",
        "Logs",
        "Feathers",
        "Wool",
        "Gravel"
    ], True),
    ("Enter Nether", True),
    ("Find Fortress", True),
    ("Find Spawner", True),
    ("Exit Spawner", True),
    ("Exit Nether", True),
    ("Tower Build Start", True),
    ("Tower Build Finished", True),
    ("Tower Leave", True),
    ("Enter Stronghold", True),
    ("Enter End", True),
    ("Finish", True)
]

cur_stages = {}


json_file = 'mct_config.json'
with open(json_file) as json_file:
    data2 = json.load(json_file)
if data2['borderless'] == 'true':
     data2['borderless']
    
else:
    data2['borderless'] = False

running_path = Path.cwd()
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
# bg = BindGlobal(widget=window)
window.text = tk.StringVar()
window.text2 = tk.StringVar()
window.text3 = tk.StringVar()
window.text4 = tk.StringVar()
window.geometry("{}x{}".format(data2["width"], data2["height"]))
window.configure(bg='black')
rt = time.time()
old_version = False
did_change = False
count = 0
ig = 0
base = 0
program_time = 0
metronome_armed = False
metronome_running = False
metronome_active = False
metronome_beats = int(data2['metronome_beats'])
listener = None
metronome_time = 0
base_update = int(data2['base_update'])
rta_update = int(data2['rta_update']) * base_update
metronome_bpm = int(data2['metronome_bpm'])
metronome_interval = 0
if data2['auto_start'] == 'true':
    click1 = 1
    click2 = 1
else:
    click1 = 0
    click2 = 0

cur_fil = None
world_base_time = 0

def get_time():

    global last_amount
    global old_version
    global amount2
    global ig
    global did_change

    # print("-------------------------")

    if data2['1.7+'] == 'false':
        try:
            global cur_fil
            global world_base_time
            mc_dir = Path(directory).parent

            stats_dir = mc_dir / "stats"

            os.chdir(stats_dir)

            json_file = glob.glob('*.dat')

            stats_file = json_file[0]

            amount = 0

            with open(stats_file) as timer_file:
                # print(timer_file)
                data = json.load(timer_file)
                for item in data["stats-change"]:
                    if "1100" in item:
                        amount = item["1100"]

            # print(amount)

            latest = max([os.path.join(directory,d) for d in os.listdir(directory)], key=os.path.getmtime)

            # print(latest)

            if latest != cur_fil:
                cur_fil = latest
                world_base_time = amount
                # print("world base time now {}".format(world_base_time))

            # print(amount)

            amount2 = float(amount - world_base_time) / 20

            # print(amount2)
            run_time = str(datetime.timedelta(seconds=amount2, milliseconds=0.5))

            # print(run_time)

            if last_amount == amount:
                ig = 0
                return run_time[:-3]
            else:
                did_change = True
                # print(latest + "\nTime: " + run_time)
                last_amount = amount
                ig = 0
                return run_time[:-3]
        except:
            ig = 1
            return '0:00:00.000'
    else:
        try:
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
    rta_font_size = data2['rta_font_size']
    igt_font_size = data2['igt_font_size']
    font_modifiers = data2['font_modifiers']
    rta_font = (font_name, rta_font_size, font_modifiers)
    igt_font = (font_name, igt_font_size, font_modifiers)
    greeting = tk.Label(fg=data2['rta_color'], bg=data2['bg_color'], font=rta_font, textvariable=window.text)
    greeting.pack()
    if data2['show_igt'] == 'true':
        greeting2 = tk.Label(fg=data2['igt_color'], bg=data2['bg_color'], font=igt_font, textvariable=window.text2)
        greeting2.pack()

    if data2['use_counter'] == 'true':
        greeting3 = tk.Label(fg=data2['counter_color'], bg=data2['bg_color'], font=rta_font, textvariable=window.text3)
        greeting3.pack()
        # bg.gbind(data2['increment'], on_increment_counter)
        # greeting.after(0, update_count)
    if data2['use_splits'] == 'true':
        split_font_size = data2['split_font_size']
        split_font = (font_name, split_font_size, font_modifiers)
        greeting4 = tk.Label(fg=data2['split_color'], bg=data2['bg_color'], font=split_font, textvariable=window.text4)
        greeting4.pack()
        # bg.gbind(data2['cycle'], cycle)
        # bg.gbind(data2['split'], split)
        # bg.gbind(data2['skip'], skip)
        reset_split()
        # greeting.after(0, update_count)
    # bg.gbind(data2['pause'], on_press)
    # bg.gbind(data2['reset_start'], on_press2)
    
    # if data2['enable_metronome'] == 'true':
    #     bg.gbind(data2['arm_metronome'], arm_metronome)
        # bg.gbind(data2['start_metronome'], start_metronome)
    
    # bg.gbind(data2['exit'], clicked3)


    # bg.bind(data2['start_metronome'], start_metronome)
    ''' this works for the window detecting right click '''
    # window.bind(data2['start_metronome'], start_metronome)
    #window.bind("<Button-1>", clicked)
    #window.bind("<Button-3>", clicked2)
    greeting.after(0, tick_time)
    greeting.after(0, update_time2)
    window.title("MCtimer")
    window.attributes('-topmost', True)
    window.overrideredirect(data2['borderless'])
    window.geometry(data2['window_pos'])
    window.mainloop()

def update_time():
    global rt
    global program_time
    

    # do_metronome_action()

    if click1 == 1:
        window.text.set(real_time())
    elif click1 == 0:
        # rt = time.time()
        diff = amount2 - base
        rtc = str(datetime.timedelta(seconds=diff))
        diff_txt = rtc[:-3]
        # print(diff_txt)
        window.text.set(diff_txt)
        # print(base)
    if click2 == 0:
        rt = time.time()
        window.text.set("0:00:00.000")
    # window.after(int(data2['rta_update'])/10, update_time)

def tick_time():
    global time_count
    global metronome_armed

    time_count += 1
    update_time()
    if metronome_armed or time_count % 20 == 0:
        check_input()
    window.after(rta_update, tick_time)
    

def check_input():
    txt = input_fil.read_text()
    input_fil.write_text("")

    global metronome_armed

    # print(txt)

    if "start_metronome" in txt:
        print(data2['enable_metronome'])
        if data2['enable_metronome'] == 'true':
            start_metronome(None)
    if "arm_metronome" in txt:
        metronome_armed = True
    if "pause_timer" in txt:
        left_click()
    if "start_timer" in txt:
        right_click()


def update_time2():
    window.text2.set(get_time())
    window.after(1000, update_time2)

def update_count():
    count_str = str(count)
    text_str = ""
    for i in range(0, int(NUM_CHARS/2)):
        text_str += " "
    text_str += count_str
    for i in range(0, int(NUM_CHARS/2)):
        text_str += " "
    window.text3.set(text_str)
    window.after(rta_update, update_count)

# def update_split()

def on_press(event):
    left_click()

def on_press2(event):
    right_click()

def update_split():
    global stage
    text_str = cur_stages[stage][0]
    if type(text_str) == type([]):
        text_str = text_str[ind]
    window.text4.set(text_str)

def reset_split():
    global ind, stage, cur_stages
    ind = 0
    stage = 0
    cur_stages = copy.deepcopy(rsg)
    update_split()

def cycle(event):
    global ind, stage
    ind += 1
    item = cur_stages[stage]
    if type(item[0]) == type([]):
        if ind == len(item[0]):
            ind = 0
    else:
        ind = 0
    update_split()

def split(event):
    global stage, ind
    item = cur_stages[stage]
    if item[1]:
        if type(item[0]) == type([]):
            item[0].remove(item[0][ind])
            if len(item[0]) == 0:
                stage += 1
            ind = 0
            update_split()
            return
    stage += 1
    ind = 0
    update_split()


def skip(event):
    global stage
    stage += 1
    update_split()


def on_increment_counter(event):
    increment_counter()

def clicked3(event):
    sys.exit(1)

def clicked2(event):
    right_click()

def clicked(event):
    left_click()


def write_to_log(text):
    pass
    # log_dir = Path("/Users/sharpieman20/MCtimer/MCtimer/logs")
    # log_fil = log_dir / data2["current_section"]
    # log_fil.touch()
    # log_fil = log_fil.open("a")
    # log_fil.write(str(text)+"\n")

def left_click():
    global click1
    if click1 == 1:
        click1 = 0
    elif click1 == 0:
        click1 = 0
    # global base
    # write_to_log(str(amount2-base))
    
    # base = amount2

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
    # print(float(amount2))
    # print("hehe")
    global base
    write_to_log("reset {}".format(str(amount2-base)))
    
    base = amount2

def increment_counter():
    global count
    count += 1


''' METRONOME CODE '''


''' Metronome mouse listener '''

def exit_handler():
    global listener
    mouse.Listener.stop(listener)
    window.quit()
    

atexit.register(exit_handler)

def listen_for_right_click():

    def on_click(x, y, button, pressed):
        # print(button)

        if pressed:
            if pressed and button == mouse.Button.right:
                start_metronome(None)
                return False
                # mouse.Listener.stop(listener)
                # print("Right Click Detected (pressed)")

    
    with mouse.Listener(on_click=on_click) as listener:
        # listener.start()
        listener.join()

''' Sound playing code '''

def play_file_named(str_name):
    playsound((running_path / str_name).as_posix(), block = True)

def play_up_beep():
    play_file_named("MetronomeHit.mp3")

def play_normal_beep():
    play_file_named("MetronomeBase.mp3")

def play_metronome_preset():
    time.sleep(0.06)
    play_file_named("MetronomePreset.mp3")

''' Metronome functions '''

def arm_metronome(event):
    global metronome_armed
    global metronome_running

    if metronome_armed or metronome_running:
        return

    metronome_armed = True
    
    # x = threading.Thread(target=listen_for_right_click, daemon=True)
    # x.start()
    listen_for_right_click()
    
    print("armed and ready")

def start_metronome(event):

    run_metronome()

    # print(metronome_running)

    # arm_metronome = False

def run_metronome():
    global metronome_time
    global metronome_interval
    global metronome_running

    if data2['has_metronome_preset'] == 'true':
        play_metronome_preset()
        metronome_running = False
        return

    metronome_time = 0

    base_time = round(time.time()*1000)

    metronome_interval = int(100 * 60 / metronome_bpm)*10

    time.sleep(float(data2['beat_offset'])*metronome_interval/1000.0)
    # print(metronome_interval)555

    while metronome_running:
        start_time = round(time.time()*1000) - base_time
        do_metronome_action()
        end_time = round(time.time()*1000) - base_time
        elapsed = end_time - start_time
        time.sleep((metronome_interval - elapsed)/1000.0)
        # print("{} {} {}".format(start_time, end_time, ))
        metronome_time += metronome_interval

def do_metronome_action():
    global metronome_running
    global metronome_interval
    if not metronome_running:
        return
    
    # print(metronome_interval)
    # metronome_time = program_time - metronome_start_time
    if metronome_time >= metronome_interval * metronome_beats:
        metronome_running = False
        return
    # print(metronome_time)
    # print(metronome_interval)
    # print(time.time()*1000)
    if metronome_time % metronome_interval == 0:
        if (metronome_time % (metronome_interval*4)) == metronome_interval*3:
            # print("up beep")
            play_up_beep()
            # pass
        else:
            # print("normal beep")
            play_normal_beep()
            # pass

    # print(time.time()*1000)
    # print()

    

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
        # print(did_change)
        # print(base)
        if did_change:
            rt = float(time.time()) - float(amount2)
            if data2['allow_offset'] == 'true':
                rt += base
            did_change = False
    if data2['auto_start'] == 'true':
        if ig == 1:
            
            rt = time.time()
            click1 = 1
            click2 = 1
            stage = 0
            reset_split()
            return '0:00:00.000'
        elif click1 == 1:
            if old_version == True and stage == 0:
                ig = 0
                rt = float(time.time()) - float(amount2)
                rtc = str(datetime.timedelta(seconds=rt))
                stage = 1
                print("stop")
                return rtc[:-3]
            else:
                ig = 0
                rt2 = time.time()
                real_time = rt2 - rt
                rtc = str(datetime.timedelta(seconds=real_time))
                
                # rt = float(amount2) - float(base)
                # rtc = str(datetime.timedelta(seconds=rt))
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