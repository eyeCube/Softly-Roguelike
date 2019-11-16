'''
    debug.py
    Softly Into the Night, a sci-fi/Lovecraftian roguelike
    Copyright (C) 2019 Jacob Wharton.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>
'''


import time

import rogue as rog




class Debugger():
    _last_command = ""
    @classmethod
    def set_last_command(cls,val):
        cls._last_command=val
    @classmethod
    def get_last_command(cls):
        return cls._last_command



class Timer():
    def __init__(self):
        self.reset()
        self.rr = []
    def reset(self):
        self.tt = time.time()
    def print(self):
        tr = time.time()-self.tt
        if tr > 0.001:
            self.rr.append(tr)
            tot=0
            for r in self.rr:
                tot+=r
            tot/=len(self.rr)
            print(tr,tot)



def printr(func):
    def wrapper(*args,**kwargs):
        print(func.__name__)
        func(*args,**kwargs)
    return wrapper



def cmd_prompt(G, L):
    
    print("Enter command below.\nFor a full list of commands, type /? and strike the enter key.")
    hlp='''-----------------------------------------------------------------
Command Line Help

- Preceed non-code commands with a forward slash ( / ).
- Do not include quotes when typing commands.

Commands:
'r','return':   exit shell and resume game.
'q','quit':     close program.

Writing code:
$ for a new line.'''
    
    while True:
        try:
            _str = input(">>")
            
            spaces=0
            for c in _str:
                if c == ' ':
                    spaces += 1
            _str=_str[spaces:]
            
            # built-in commands
            if _str[0] == '/': 
                _str=_str[1:]
                if _str == "?": print(hlp); continue
                elif (_str == 'return' or _str == 'r'): return
                elif (_str == 'quit' or _str == 'q'): rog.end(); return
            
            # parse new lines from '#' symbols
            new = []
            for i in _str:
                if i == '$': new.append('\n')
                else: new.append(i)
            _str = ''.join(new)
            
            # execute code
            exec(_str, G, L)
            Debugger.set_last_command(_str)
            print("Done.")
            
        except Exception as e:
            print(e)

def execute_last_cmd(G, L):
    try:
        exec(Debugger.get_last_command(), G, L)
        print("Done.")
    except Exception as e:
        print(e)

