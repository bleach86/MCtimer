# MCtimer
Game timer for Minecraft speed running

MCtimer is cross platform in game timer for use in Minecraft speed running. 

There are two timers, one in game(green) and real time(red).
The in game timer calculates the time directly from the json file in the stats folder. 
This file is only updated by Minecraft when the game is paused, during an auto-save, and when the credits roll.
That means that the timer is only updated when these events occur.

The real time timer is updated every milisecond. It can be paused using a configurable hotkey or left-click, then it can be reset and started with a configurable hotkey or with right-click. And the timer can be closed using a configurable hotkey or middle-click.
The IGT timer automatically reset when a new world is created. And the RTA timer can also be set to autostart on world load.
The timer is also visible over full screen windows. The only one out there.

This runs on Linux, MacOS, and Windows. Recomended python 3.6+
If running mctimer.py directly.
It may be required to install tkinter via `pip install python-tk`
bindglobal is now a requirement `pip install bindglobal`
Run from cmd or terminal via `python mctimer.py` or `python3 mctimer.py`

See https://github.com/bleach86/MCtimer/releases/tag/v2.0 for executable release. The executable release includes everything needed and requires nothing to be installed and no CMD or terminal. Just double click and go.

mct_config.json needs to be in the same directory as either mctimer.py, or the executable for your OS.

**mct_confic.json explained**
pause -used to set the hotkey for pause
reset_start -used to set the hotkey for reset and start
exit -used to set hotkey to close the timer
auto_start -set to true to auto start rta timer on world load.(NOTE: the RTA timer need to be running before creating a new world for this to work properly. IE: if you pause the timer, you will need to reset then start before loading the next world) set to false for manual stop
bg_color -sets background color
igt_color -sets color of the igt
rta_color -set color of the rta
linux_saves -used to set path to saves directory on Linux
mac_saves -used to set the path to saves directory on MacOS
windows_saves -used to set path to saves directory on Windows. note the double '\\'
rta_update -sets the update frequence of the rta timer in miliseconds. If cpu usage is too high, increase the number. 1 is 1 milisecond, and 1000 is one second. 25 is a nice amount to lower cpu usage.
window_pos -sets where on screen the window is. +0+0 is top left corner. increase the first 0 to move right, and the second to move down.

On Windows you may need to use virtual keyboard codes for certain hotkeys. For instance <96> sets to numpad 0. [Virtual Keyboard codes list](https://help.mjtnet.com/article/262-virtual-key-codes)

"THE BEER-WARE LICENSE" (Revision 42):
bleach86 wrote this file. As long as you retain this notice you can do whatever you want with this stuff. If we meet some day, and you think this stuff is worth it, you can buy me a beer in return
