'''
    orangIO
    (Orange I/O)
        An input/output extension for tcod Python
    
    Softly Into the Night, a sci-fi/Lovecraftian roguelike
    Copyright (C) 2020 Jacob Wharton.

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

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Alpha: This module is currently in Alpha mode
        It is usable but not very user-friendly,
        and has a lot of dependencies.

    This extension to tcod allows you to easily do:
        - key commands with any combination of Shift, Ctrl, and Alt
        - text input with blinking cursor
        - "waiting" for a certain input

    How to use this module:

    Call init_keyBindings during the initialization of your game.
    Use the key_get* wrapper functions to interface with the keyboard input.
    The handle_mousekeys function is the function that allows commands
        with any combination of Ctrl, Shift and Alt.
        - To use this function in your game,
            modify COMMANDS and key_bindings.txt defaults.
    Call the get_raw_input wrapper function to
        wrap the tcod key and mouse objects in a tuple.
    key_bindings.txt
        To edit key bindings, refer to the comments on key_bindings.txt
        To change the directory of key_bindings.txt, change the variable
            "file_keyBindings"

    Example use for key combo inputs:
    
        # get input #
        pcInput=IO.get_raw_input()
        pcAct=IO.handle_mousekeys(pcInput).items()
        
        # process commands #
        for act,arg in pcAct:
            if act == "lclick":
                mousex,mousey,z = arg #unpack command arguments
                #...
            if act == "move":
                dx,dy,dz = arg #unpack command arguments
                #...
        
    
'''


import os
import tcod
import time
import textwrap

from const import *
import managers   
import maths
import word



    #colors
WHITE=tcod.Color(255,255,255)
BLACK=tcod.Color(0,0,0)

    #global key and mouse handlers for all objects in OrangIO
key = tcod.Key()
mouse = tcod.Mouse()

#this value is the number of alternate key codes for each command.
    #the number of key codes for each command in key_bindings.txt
    #MUST MATCH THIS VALUE.
NUM_ALT_CMDS = 3


#directory of "key_bindings.txt"
file_keyBindings=os.path.join(
    os.path.curdir,os.path.pardir,"settings","key_bindings.txt")

'''###
#key_bindings.txt
    #This is the backup key bindings file

    #To add a new command into the game, add it into the key_bindings.txt
    #defaults below. Add Shift+ or Ctrl+ or Alt+ or any combo thereof.
    #Delete the key_bindings.txt file from the game's directory to
    #have the game recreate it using the defaults.
    #   - Do not use spaces.
    #   - To use special keys, including spacebar:
            refer to the TEXT_TO_KEY dict.
    #   - Take note of the placement you put the command into the text file.
    #Put that command into the dict COMMANDS in the SAME ORDER that you put
    #it into key_bindings.
    #   - Put the command into player.commands or player.const_commands.
    #       (If using this as a third party module, simply run
    #       handle_mousekeys and check that the result == the desired command)
    
#if you add new commands you must add new key bindings for those commands.
#key bindings begin on a new line,
    #and consist of any combination of the following:
        #Ctrl+
        #Shift+
        #Alt+
    #followed by a key constant as defined in TEXT_TO_KEY
        #or a letter/number/symbol on the keyboard.
    #ALERT: To get the ? key:
        #do the key combination Shift+/ instead of ?
        #IN GENERAL, only use the lowercase keys and indicate Shift+
        #in order to indicate that the uppercase character should be used.
        #Example: to make a command respond to the command ">",
            #the command must be written as Shift+.
            #(shift+ period key)
    #Note: NumPad is not currently supported. NumPad must be OFF during play.
    #Note: commands are not case-sensitive.
###'''

KEYBINDINGS_TEXT_DEFAULT = '''//file name: {filename}

//These are comments.
//  All empty lines, and all lines beginning with "//"
//  (without quotations), are considered to be comments
//  by the file reader, and are ignored.

//      --- Key Bindings Information ---

//In order to remove one binding, set it to: NONE 
//Bindings may begin with any combination of shift, ctrl,
//  and alt, followed by a plus (+) symbol:
//  "Shift+" OR "Ctrl+" OR "Alt+"
//Keypad numbers begin with "KP" e.g. "KP5"

//Example key bindings
//    (note bindings are case-insensitive):
//  CTRL+ALT+DELETE
//  shift+=
//  f
//  Ctrl+A
//  none
//  None
//  KP8

//The action bound to the last combo will function if and
//  only if the a button is pressed WHILE the Ctrl button
//  is being held, and neither Alt nor Shift are also being
//  pressed down; if the Alt button is also being held, for
//  instance, the input will be treated as "Ctrl+Alt+a",
//  which is different from "Ctrl+a".

//Note:
//  Left and right Ctrl are treated as the same.
//  Left and right Alt are treated as the same.
//  Left and right Shift are treated as the same.

//ALERT: NumLock is currently unsupported.
//  The numpad keys might not work as expected with NumLock on.
//  Keep NumLock off during play.

//---------\\
// Bindings |
//---------//

// display commands / help
Shift+/
NONE
NONE

// North
K
KP8
NONE

// West
H
KP4
NONE

// South
J
KP2
NONE

// East
L
KP6
NONE

// Northwest
Y
KP7
NONE

// Southwest
B
KP1
NONE

// Southeast
N
KP3
NONE

// Northeast
U
KP9
NONE

// Direct Towards Self
.
KP5
NONE

// up
Shift+,
NONE
NONE

// down
Shift+.
NONE
NONE

// context-sensitive action
SPACE
NONE
NONE

// target entity (+ target limbs) to fire / throw / attack
t
NONE
NONE

// move prompt
m
NONE
NONE

// attack prompt
x
NONE
NONE

// shoot ranged weapon
f
NONE
NONE

// throw item in dominant hand
shift+t
NONE
NONE

// get item (pickup & place in inventory)
g
,
NONE

// grab item (pickup item & hold in hand)
ctrl+,
NONE
NONE

// grapple (grab foe's limbs, etc.)
ctrl+g
NONE
NONE

// open/Close
o
NONE
NONE

// close
Shift+=
NONE
NONE

// open
-
NONE
NONE

// inventory
i
NONE
NONE

// abilities menu
Tab
NONE
NONE

// change body position or stance (crouch, stand, lie prone, etc.)
p
NONE
NONE

// change movement speed (walking, running, sprinting, etc.)
s
NONE
NONE

// speed up movement speed
Shift+s
NONE
NONE

// slow down movement speed
Ctrl+s
NONE
NONE

// examine or Look
/
Shift+L
NONE

// wait
w
Ctrl+t
NONE

// rest
r
NONE
NONE

// move view
v
NONE
NONE

// fixed view mode
Ctrl+v
NONE
NONE

// show player location (find player)
Ctrl+f
NONE
NONE

// show message history
Shift+h
NONE
NONE

// show character page
a
Shift+c
NONE

// quit game
Alt+q
NONE
NONE

//---------\\
//  MENUS   |
//---------//

// Menu Up
UP
NONE
NONE

// Menu Left
LEFT
NONE
NONE

// Menu Down
DOWN
NONE
NONE

// Menu Right
RIGHT
NONE
NONE

// Select
SPACE
ENTER
NONE

// Exit
ESCAPE
NONE
NONE

// Page Up
PAGEUP
NONE
NONE

// Page Down
PAGEDOWN
NONE
NONE

// Home
HOME
NONE
NONE

// End
END
NONE
NONE

// Delete
DELETE
NONE
NONE

// Insert
INSERT
NONE
NONE

// Backspace
BACKSPACE
NONE
NONE

//---------\\
// ADVANCED |
//---------//

// Shell / command prompt / console
Ctrl+`
NONE
NONE

// Execute last console command (during play)
Ctrl+Shift+`
NONE
NONE

// 

//
'''.format(filename=file_keyBindings)

'''
# IMPORTANT!!
# Order of commands must match order in the key_bindings.txt file. #
'''
COMMANDS = {        # translate commands into actions

    'help'          : {'help': True}, # CHANGED ORDERING, TEST TO MAKE SURE IT STILL WORKS.
    'north'         : {'context-dir': (0, -1,  0,) },
    'west'          : {'context-dir': (-1, 0,  0,) },
    'south'         : {'context-dir': (0,  1,  0,) },
    'east'          : {'context-dir': (1,  0,  0,) },
    'northwest'     : {'context-dir': (-1, -1, 0,) },
    'southwest'     : {'context-dir': (-1, 1,  0,) },
    'southeast'     : {'context-dir': (1,  1,  0,) },
    'northeast'     : {'context-dir': (1, -1,  0,) },
    'self'          : {'context-dir': (0,  0,  0,) },
    'up'            : {'context-dir': (0,  0, -1,) },
    'down'          : {'context-dir': (0,  0,  1,) },
    'context'       : {'context': True},
    'target-prompt' : {'target-prompt': True},
    'move-prompt'   : {'move-prompt': True},
    'attack-prompt' : {'attack-prompt': True},
    'shoot-prompt'  : {'shoot-prompt': True},
    'throw-prompt'  : {'throw-prompt': True},
    'get-prompt'    : {'get-prompt': True},
    'grabitem-prompt':{'grabitem-prompt': True},
    'grapple-prompt': {'grapple-prompt': True},
    'openclose-prompt':{'openclose-prompt': True},
    'close-prompt'  : {'close-prompt': True},
    'open-prompt'   : {'open-prompt': True},
    'inventory'     : {'inventory': True},
    'abilities'     : {'abilities': True},
    'change-pos'    : {'change-pos': True},
    'change-msp'    : {'change-msp': True},
    'msp-up'        : {'msp-up': True},
    'msp-down'      : {'msp-down': True},
    'look'          : {'look': True},
    'wait'          : {'wait': True},
    'rest'          : {'rest': True},
    'move view'     : {'move view': True},
    'fixed view'    : {'fixed view': True},
    'find player'   : {'find player': True},
    'msg history'   : {'message history': True},
    'char page'     : {'character page': True},
    'quit'          : {'quit game': True},

    'menu-up'       : {'menu-nav': (0, -1,  0,) },
    'menu-left'     : {'menu-nav': (-1, 0,  0,) },
    'menu-down'     : {'menu-nav': (0,  1,  0,) },
    'menu-right'    : {'menu-nav': (1,  0,  0,) },
    'select'        : {'select': True},
    'exit'          : {'exit': True},
    'pgup'          : {'page up': True},
    'pgdn'          : {'page down': True},
    'home'          : {'home': True},
    'end'           : {'end': True},
    'delete'        : {'delete': True},
    'insert'        : {'insert': True},
    'backspace'     : {'backspace': True},
    
    'console'       : {'console': True},
    'last cmd'      : {'last cmd': True},
}

#-----------------------------------------------------------#
TEXT_TO_KEY = {     # translate text into key constants
    'none'      : -1,
    'kp0'       : tcod.KEY_KP0,
    'kp1'       : tcod.KEY_KP1,
    'kp2'       : tcod.KEY_KP2,
    'kp3'       : tcod.KEY_KP3,
    'kp4'       : tcod.KEY_KP4,
    'k5p'       : tcod.KEY_KP5,
    'kp6'       : tcod.KEY_KP6,
    'kp7'       : tcod.KEY_KP7,
    'kp8'       : tcod.KEY_KP8,
    'kp9'       : tcod.KEY_KP9,
    'up'        : tcod.KEY_UP,
    'down'      : tcod.KEY_DOWN,
    'right'     : tcod.KEY_RIGHT,
    'left'      : tcod.KEY_LEFT,
    'space'     : tcod.KEY_SPACE,
    'tab'       : tcod.KEY_TAB,
    'enter'     : tcod.KEY_ENTER,
    'escape'    : tcod.KEY_ESCAPE,
    'backspace' : tcod.KEY_BACKSPACE,
    'insert'    : tcod.KEY_INSERT,
    'delete'    : tcod.KEY_DELETE,
    'home'      : tcod.KEY_HOME,
    'end'       : tcod.KEY_END,
    'pagedown'  : tcod.KEY_PAGEDOWN,
    'pageup'    : tcod.KEY_PAGEUP,
    'f1'        : tcod.KEY_F1,
    'f2'        : tcod.KEY_F2,
    'f3'        : tcod.KEY_F3,
    'f4'        : tcod.KEY_F4,
    'f5'        : tcod.KEY_F5,
    'f6'        : tcod.KEY_F6,
    'f7'        : tcod.KEY_F7,
    'f8'        : tcod.KEY_F8,
    'f9'        : tcod.KEY_F9,
    'f10'       : tcod.KEY_F10,
    'f11'       : tcod.KEY_F11,
    'f12'       : tcod.KEY_F12,
}
VK_TO_CHAR = {      # translate key consants into a char
    tcod.KEY_KP0     : '0',
    tcod.KEY_KP1     : '1',
    tcod.KEY_KP2     : '2',
    tcod.KEY_KP3     : '3',
    tcod.KEY_KP4     : '4',
    tcod.KEY_KP5     : '5',
    tcod.KEY_KP6     : '6',
    tcod.KEY_KP7     : '7',
    tcod.KEY_KP8     : '8',
    tcod.KEY_KP9     : '9',
    tcod.KEY_KPDEC   : '.',
    
    tcod.KEY_UP          : chr(K_UP),
    tcod.KEY_DOWN        : chr(K_DOWN),
    tcod.KEY_RIGHT       : chr(K_RIGHT),
    tcod.KEY_LEFT        : chr(K_LEFT),
    tcod.KEY_BACKSPACE   : chr(K_BACKSPACE),
    tcod.KEY_DELETE      : chr(K_DELETE),
    tcod.KEY_INSERT      : chr(K_INSERT),
    tcod.KEY_PAGEUP      : chr(K_PAGEUP),
    tcod.KEY_PAGEDOWN    : chr(K_PAGEDOWN),
    tcod.KEY_HOME        : chr(K_HOME),
    tcod.KEY_END         : chr(K_END),
    tcod.KEY_ENTER       : chr(K_ENTER),
    tcod.KEY_KPENTER     : chr(K_ENTER),
    tcod.KEY_ESCAPE      : chr(K_ESCAPE),
}





#-----------#
#  classes  #
#-----------#


#
# cursor
#
    
class Cursor:
    
    def __init__(self,x=0,y=0,rate=0.3):
        self.set_pos(x,y)
        self.time_stamp = 0
        self.blink_time = rate
        
    def set_pos(self,x,y):  self._x = x; self._y = y;
    def draw(self,con=0):   console_invert_color(con,self.x,self.y)
        
    def blink(self):
        if time.time() - self.time_stamp > self.blink_time:
            self.blink_reset_timer_off()
            return True
        else: return False
        
    def blink_reset_timer_off(self):
        self.time_stamp = time.time()
    def blink_reset_timer_on(self):
        self.time_stamp = 0
        
    @property
    def x(self): return self._x
    @property
    def y(self): return self._y


#
# Text Input Manager
#
#

# Display user-entered text field with blinking cursor
# and handle all processes thereof.

# key bindings should NEVER affect input for this function.
# that got nasty real fast in Caves of Qud...

#---------------Args----------------#
# int x,y           location on screen
# int w,h           width and height of textbox
# string default    text that appears when textbox is created
# string mode       'text' or 'wait' :
#   - text mode: normal input mode, returns text when Enter key pressed
#   - wait mode: returns first accepted key press input
# bool insert       begin in "insert" mode?
#

class TextInputManager(managers.Manager): #Manager_Input | ManagerInput
    
    def __init__(self, x,y, w,h, default,mode,insert):
        
        # init
        self.console    = tcod.console_new(w, h)
        self.init_time  = time.time()
        
        self.x=x
        self.w=w
        self.y=y
        self.h=h
        self.mode=mode
        self.text=default
        self.default=default
        
        self.keyInput=''
        
        self.redraw_cursor  = True
        self.render_text    = True
        self.flush          = False
        
        self.key=key
        self.mouse=mouse
        
        self.cursor=Cursor()
        self.cursor.set_pos(x,y)
        self.insert_mode=insert #replace the character under the cursor or shift it aside?
        
        #ignore buffer
        get_raw_input()


    def set_result(self,val):
        if val == '': val=self.default
        if val == '': val='0'
        elif val == '\x1c': val='0'
        super(TextInputManager,self).set_result(val)
    
    def run(self):
        super(TextInputManager, self).run()
        
##        # manually close game #
##        if libtcod.console_is_window_closed():
##            #sys.exit() # no, there should be a custom exit func
        
        tcod.sys_sleep_milli(5)  #reduce CPU usage
        
        self.update()
        
        tcod.sys_check_for_event(    # check don't wait.
            tcod.EVENT_KEY
            | tcod.EVENT_MOUSE_PRESS     # we only want to know mouse press
            | tcod.EVENT_MOUSE_RELEASE,  # or release, NOT mouse move event.
            self.key, self.mouse)
        
        self.get_char()
        self.mouse_events()
        self.keyboard_events()
    
    def close(self):
        ##do not inherit
        tcod.console_delete(self.console)
    
    def update(self):
        
        self.flush=False
        
        if self.cursor.blink():
            self.redraw_cursor=True
            
        if self.render_text:
            self.update_render_text()
            self.redraw_cursor=True
            
        if self.redraw_cursor:
            self.cursor.draw()
            self.flush=True
            
        if self.flush:
            tcod.console_flush()

        #now we've updated, turn all update variables to False
        self.redraw_cursor  =False
        self.render_text    =False
        self.flush          =False

    def keyboard_events(self):
        
        if self.keyInput:

            if self.mode == "wait": self.set_result(self.keyInput)

            self.redraw_cursor=True
            self.cursor_blinkOn()

            if self.mode == "text":
                self.input_vk()
                self.input_text()

    def mouse_events(self):
        
        if self.mouse.lbutton_pressed:
            self.cursor_blinkOn()
            self.putCursor(self.mouse.cx - self.x)
            self.blit_console()
            self.flush=True


    def input_vk(self):
        
        if not tcod.console_is_key_pressed(self.key.vk):
            return

        cpos=self.cursor_pos
        ans=ord(self.keyInput)

        # returning a result
        if (ans == K_ENTER):    self.set_result(self.text)
        if (ans == K_ESCAPE):   self.set_result(self.default)

        # deleting
        if (ans == K_BACKSPACE) :
            self.render_text=True
            self.putCursor(cpos - 1)
            self.delete()
        elif (ans == K_DELETE) :
            self.render_text=True
            self.delete()
        # moving
        elif (ans == K_LEFT)    : self.move(cpos - 1)
        elif (ans == K_RIGHT)   : self.move(cpos + 1)
        
        # insert mode
        elif (ans == K_INSERT)  : self.insert_mode = not self.insert_mode


    def input_text(self):

        if not self.key.vk == tcod.KEY_TEXT:
            return
        
        ans=self.keyInput
        if self.cursor_pos < len(self.text): # insert or replace
            self.render_text=True
            first_half = self.text[:self.cursor_pos]
            second_half = self.text[self.insert_mode + self.cursor_pos:]
            self.text='{}{}{}'.format(first_half, ans, second_half)
        else:   # append
            self.text += ans
            self.put_next_char(ans)
            self.blit_console()
            self.flush=True

        # truncate
        if (len(self.text) > self.w):
            self.text = self.text[:self.w]
        
        # move cursor
        self.putCursor(self.cursor_pos + 1)
        #


    def move(self, new):
        tcod.console_set_char_foreground(
            0, self.x + self.cursor_pos, self.y, WHITE)
        tcod.console_set_char_background(
            0, self.x + self.cursor_pos, self.y, BLACK)
        self.flush=True
        self.putCursor(new)

    def update_render_text(self):
        tcod.console_clear(self.console)
        tcod.console_print_ex(
            self.console,0,0,
            tcod.BKGND_NONE,tcod.LEFT,
            self.text )
        self.blit_console()
    
    def get_char(self):
        reply=''
        if tcod.console_is_key_pressed(self.key.vk):
            reply = VK_TO_CHAR.get(self.key.vk, None)
        
        elif self.key.vk == tcod.KEY_TEXT:
            tx = self.key.text #.decode()
            if (ord(tx) >= 128 or tx == '%'):
                return ''    # Prevent problem-causing input
            else: reply=tx
        self.keyInput=reply

    def delete(self):
        self.text=self.text[:self.cursor_pos] + self.text[1+self.cursor_pos:]
        
    def put_next_char(self,new):
        tcod.console_put_char_ex(
            self.console, self.cursor_pos,0, new,
            WHITE,BLACK
        )
    def blit_console(self):
        tcod.console_blit(
            self.console,   0,0,self.w,self.h,
            0,      self.x,self.y
        )    
    '''def ignore_buffer(self):
        return (time.time() - self.init_time < .05)'''
    def putCursor(self,new):
        pos=maths.restrict( new, 0, min(self.w - 1, len(self.text)) )
        self.cursor.set_pos(self.x + pos, self.y)
    def cursor_blinkOn(self):   self.cursor.blink_reset_timer_on()
    
    @property
    def cursor_pos(self):   return self.cursor.x


#--------------------------------------------------#




#-----------#
# functions #
#-----------#


#key functions
def key_getchar(k):
    '''
    # we add 256 here to differentiate character (text) codes from
    # special key codes, like NumLock, which happens to have the same
    # integer code (62) as > (greater than symbol), for example.
    '''
    return k + 256
def key_get_pressed():      # get both vk and text in one variable
    k = tcod.KEY_NONE
    if tcod.console_is_key_pressed(key.vk) : k = key.vk 
    if k == tcod.KEY_CHAR : k = key_getchar(key.c)
    return k
def key_get_special_combo(k):   # combine shift,ctrl,alt, and key press
    shift    =  key.shift
    ctrl     = (key.lctrl or key.rctrl)
    alt      = (key.lalt  or key.ralt )
    return (k, (shift, ctrl, alt,),)

# files #

#is line a "comment"? Return whether string line should be ignored.
def file_is_line_comment(line):
    return ((line[0]=='/' and line[1]=='/') or line[0]=='\n')

# tcod #

def color_invert(rgb):
    return tcod.Color(255-rgb[0],255-rgb[1],255-rgb[2])
def console_invert_color(con,x,y):
    col1 = tcod.console_get_char_foreground(con,x,y)
    col2 = tcod.console_get_char_background(con,x,y)
    tcod.console_set_char_foreground(con, x,y, color_invert(col1))
    tcod.console_set_char_background(con, x,y, color_invert(col2))

#
#
# get raw input
#
# checks for input
# returns key and mouse objects in a tuple
#
def get_raw_input():
    tcod.sys_sleep_milli(1)  # prevent from checking a billion times/second to reduce CPU usage

    # we use the check_for_event instead of the wait_for_event function
    # because wait_for_event causes lots of problems
    tcod.sys_check_for_event(
        tcod.EVENT_KEY
        | tcod.EVENT_MOUSE_PRESS     # we only want to know mouse press
        | tcod.EVENT_MOUSE_RELEASE,  # or release, NOT mouse move event.
        key, mouse)
    return (key,mouse,)
#
#
# handle_mousekeys
#
# convert keyboard and mouse input into player commands
# and return the command as a dict
#
def handle_mousekeys(keymouse):
    key,mouse=keymouse
    
    # Mouse #

    if mouse.lbutton_pressed:   return {'lclick': (mouse.cx,mouse.cy,0,) }
    if mouse.rbutton_pressed:   return {'rclick': (mouse.cx,mouse.cy,0,) }
    
    # Keys #
    
    k = key_get_pressed()
    combined = key_get_special_combo(k)
    
    return COMMANDS.get(bind.get(combined, None), {})

#Input
#wrapper function to get a simple input from the user
def Input(x,y, w=1,h=1, default='',mode='text',insert=False):
    manager=TextInputManager(x,y, w,h, default,mode,insert)
    result=None
    while not result:
        manager.run()
        result=manager.result
    manager.close()
    return result

#
# key bindings
#

bind={}
NO_KEY=(-1,(False,False,False,),) # NULL key constant

# init_keyBindings
# call during setup to initialize the keyboard controls
def init_keyBindings():
    try:
        _init_keyBindings()
    except FileNotFoundError:
        print("'key_bindings.txt' File Not Found. Creating new file from defaults...")
        _keyBindings_writeFromDefault()
        _init_keyBindings()

#
# *DO NOT CALL THIS FUNCTION*
# call init_keyBindings instead
# _init_keyBindings
# read from a file and put key binding info into dict bind.
#
def _init_keyBindings():
        
    global bind

    codes = []  # list of key codes 0-511 (0-255 and an additional 256
                # for special key inputs like NumPad digits)
    combin = [] # list of tuples (shift,ctrl,alt) for key combinations
                
    numCommands=0   #counter
    
    with open(file_keyBindings, 'r') as bindings:
        for line in bindings:
            if file_is_line_comment(line): continue #ignore comments

            #read this line as a command
            numCommands += 1
            
            #init
            line=word.remove_blankspace(line) #ignore white space
            line=line.lower() #not case-sensitive
            
            #NONE
            if "none" in line: #no key set, still need to put something in the list
                combin.append( (False,False,False,) )
                codes.append(   -1  ) # NULL key
                continue
            
            # Key combinations #
            
            delete=0
            if 'shift+' in line:
                delete+=6
                _shf = True
            else: _shf = False
            if 'ctrl+' in line:
                delete+=5
                _ctl = True
            else: _ctl = False
            if 'alt+' in line:
                delete+=4
                _alt = True
            else: _alt = False
            combinData=(_shf,_ctl,_alt,)
            if delete: line=line[delete:]
            
            if line[1] == '\n':     # character keys
                codeData=key_getchar(ord(line[0]))
            else:                   # special keys
                new = TEXT_TO_KEY.get(line[:-1],-1)
                codeData=new
            
            combin.append( combinData )
            codes.append(   codeData  )
        #
        
    print("Key bindings loaded from '{}'".format(file_keyBindings))
    
    n = NUM_ALT_CMDS
    # error checking
    if not ( numCommands == n*len(COMMANDS.keys()) ):
        print("number of commands: ", numCommands)
        print("number expected: ", n*len(COMMANDS.keys()))
        raise(Error_wrongNumberCommandsLoaded)
    # bind special combined key input to commands #
    try:
        for i,v in enumerate(COMMANDS.keys()):
            for j in range(n):
                index = i*n + j
                bind.update({ (codes[index], combin[index],) : v })
    except:
        raise(Error_wrongNumberCommandsLoaded)
#end def _init_keyBindings

def _keyBindings_writeFromDefault():
    try:
        with open(file_keyBindings,"w+") as file:
            file.write(KEYBINDINGS_TEXT_DEFAULT)
            print("'key_bindings.txt' Created.")
    except:
        print("FATAL ERROR! Failed to create key_bindings.txt")









