# MCtimer
Game timer for Minecraft speed running

MCtimer is cross platform in game timer for use in Minecraft speed running. 

There are two timers, one in game(green) and real time(red).
The in game timer calculates the time directly from the json file in the stats folder. 
This file is only updated by Minecraft when the game is paused, during an auto-save, and when the credits roll.
That means that the timer is only updated when these events occur.

The real time timer is updated every second. It can be reset to 0 by left clicking, then left clicking again to start it again.
Both timers automatically reset when a new world is created.

This runs on Linux, MacOS, and Windows. Recomended python 3.6+
It may be required to install tkinter via `pip install python-tk`
This assumes that your Minecraft saves are in the default location, if yours is different, you will need to edit your path for your OS.

See https://github.com/bleach86/MCtimer/releases/tag/v1.0 for binary release. The binary release includes everything needed and requires nothing to be installed and no CMD or terminal. Just double click and go.

Run from cmd or terminal via `python mctimer.py` or `python3 mctimer.py`

For use with minecfaft 1.13+, use unmodified. For minecraft 1.7-1.12.2 comment out line #45 and uncomment line #46.

"THE BEER-WARE LICENSE" (Revision 42):
bleach86 wrote this file. As long as you retain this notice you can do whatever you want with this stuff. If we meet some day, and you think this stuff is worth it, you can buy me a beer in return
