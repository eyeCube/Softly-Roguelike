'''
    game.py
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
'''

import os
import tcod as libtcod
import time
import textwrap

from const      import *
import rogue as rog
import components as cmp
import ai
import colors
import misc
import player
import debug
import entities
#define
timer = debug.Timer()


        # Function definitions #

        
def play(pc, pcAct):
    '''
        primary gameplay loop
    '''
    
    world = rog.world()
    
    #timer.reset() #DEBUG TESTING. USED WITH timer.print()
    
##    rog.release_souls() #handled by esper now
    

        #-------------------#
        #   NPC turn        #
        #-------------------#
    
    pcActor = world.component_for_entity(pc, cmp.Actor)
    if pcActor.ap <= 0:
        rog.turn_pass()
        #beginning of turn /right after player turn.
        rog.Rogue.run_beginTurn_managers(pc)
        # process
        world.process()
        #end of turn
        rog.Rogue.run_endTurn_managers(pc)
        return
    
        #-------------------#
        #   player turn     #
        #-------------------#

    rog.pc_listen_sights()
    rog.pc_listen_sounds()
    rog.clear_listeners()
    
    rog.game_update()
    #timer.print() #DEBUG TESTING. SHOWS TIME ELAPSED SINCE RESET.
    
    player.commands(pc, pcAct)
    player.commands_pages(pc, pcAct)
# end def

    

        # Class definitions #


class GlobalSettings:
    '''
        ALERT: modifies global values.
        references settings.txt
            - creates settings.txt if it does not exist
    '''

    settingsDir = os.path.join(os.path.curdir,os.path.pardir,"settings")
    settingsFileName="settings.txt"
    settingsFile = os.path.join(settingsDir,settingsFileName)
    
    _errorSettingsCorrupted="ERROR: Settings file '{f}' corrupted. (a) Fix the syntax error, OR (b) delete '{f}' and restart the game to reset to default settings.".format(f=settingsFileName)
    _alertSettingsNotFound="ALERT: Settings file '{}' not found. Creating file from defaults...".format(settingsFileName)
    _settingsCreated="Settings file '{}' created.".format(settingsFileName)
    
    # Used for writing a new settings file from default settings #
    
    DEFAULTS = {
        "WINDOW WIDTH"      : 80,
        "WINDOW HEIGHT"     : 50,
        "TILESET"           : "tileset_12x16.png",
        "RENDERER"          : libtcod.RENDERER_SDL,
        "FPS MAX"           : 60,
        "SHOW FPS"          : 0,
        "HIGHLIGHT PC"      : 0,
        "HIGHLIGHT COLOR"   : "TRUEBLUE",
        "SLEEP TIME"        : 1,
        "COLORED STRINGS"   : "ATK,trueblue;DV,red",
    }

    COMMENTS = {
        "RENDERER"      : '''Renderer 0, 1, or 2; 2 is slowest, but most compatible.
0 - GLSL
1 - OPENGL
2 - SDL''',
        "#WHITE"        : "Colors. RGB Values 0-255. Feel free to change the values!",
    }

    ##
    
    def __init__(self):
        self.file = GlobalSettings.settingsFile
        # settings vars
        # will be overwritten when settings file is read
        self.renderer = 0
        self.window_width = 0
        self.window_height = 0
        self.fpsmax = 0
        self.showfps = False
        self.highlightPC = False
        self.highlightColor = ""
        self.tileset = ""
        self.colors={}
        self.sleep_time=0
        self._colored_strings=[]
        
    def apply(self):
        '''
            must call read() first
        '''
        try:
            self._apply()
        except:
            print(GlobalSettings._errorSettingsCorrupted)
            raise
        
    def read(self):
        '''
            read data from settings.txt
        '''
        self.colors={}
        try:
            with open(self.file, 'r') as file:
                for line in file:
                    self.lastLine=line
                    if misc.file_is_line_comment(line):
                        continue
                    self._parse_line(line)
            print("Settings loaded from '{}'".format(self.file) )

        except FileNotFoundError:
            print(GlobalSettings._alertSettingsNotFound)
            self._write_defaults()
            print(GlobalSettings._settingsCreated)
            self.read()
        except:
            print(GlobalSettings._errorSettingsCorrupted)
            print("Last line read from '{}': {}".format(self.file, self.lastLine))
            raise

    def _apply(self):       # apply settings globally
        '''
            apply the settings read from settings.txt
            # some settings do not get applied here
            # but are instead accessed by other objects
        '''        
        # window settings #
        libtcod.console_set_custom_font(self.tileset,
            libtcod.FONT_TYPE_GREYSCALE |
            libtcod.FONT_LAYOUT_ASCII_INROW, TILES_PER_ROW,TILES_PER_COL)
        libtcod.console_init_root(self.window_width,self.window_height,
                                  GAME_TITLE, False, renderer=self.renderer)
        libtcod.sys_set_fps(self.fpsmax)
        
        # colors #
        for k,v in self.colors.items():
            colors.COLORS.update({k:v})
##            print("updating color {} with {}".format(k,v))
        # colored strings
        colors.colored_strings=[]
        for item in self._colored_strings:
            colors.colored_strings.append(item)
    
    def _parse_line(self,line):
        strng = self._parse_setting(line)
        line = line.upper()
        
        if "RENDERER" in line:
            self.renderer = int(strng)
        elif "WINDOW WIDTH" in line:
            self.window_width = int(strng)
        elif "WINDOW HEIGHT" in line:
            self.window_height = int(strng)
        elif "FPS MAX" in line:
            self.fpsmax = int(strng)
        elif "SHOW FPS" in line:
            self.showfps = bool(int(strng))
        elif "TILESET" in line:
            self.tileset = os.path.join(
                os.path.curdir,os.path.pardir,"tilesets",strng)
        elif "HIGHLIGHT PC" in line:
            self.highlightPC = bool(int(strng))
        elif "HIGHLIGHT COLOR" in line:
            self.highlightColor = strng.lower()
        elif "SLEEP TIME" in line:
            self.sleep_time = int(strng)
        elif "COLORED STRINGS" in line:
            self._colored_strings=[]
            elements = strng.split(";")
            for element in elements:
                if not element: continue
                self._colored_strings.append(element.split(","))
        elif "#" in line:           #<- all colors, and only colors, begin with '#'
            self._parse_color(line, strng)

    def _write_defaults(self):
        '''
            create new settings.txt file from defaults
        '''
        
        def write_line(file, k,v):
            comment=self.COMMENTS.get(k, None)
            if comment:
                comment=comment.replace('\n','\n// ')
                file.write('\n// {}\n'.format(comment))
            newline = "{:20s}= {}\n".format(k,v)
            file.write(newline)
            
        with open(self.file, 'w+') as file:
            file.write('// {}\n'.format(GlobalSettings.settingsFileName))
            for k,v in GlobalSettings.DEFAULTS.items():
                write_line(file, k,v)
        #   default Colors
            for k,v in colors.COLORS.items():   
                k="#" + k.upper()
                write_line(file, k,v)
            #write_line(file, "COLORED STRINGS", GlobalSettings.)
    
    def _parse_setting(self,line):
        pos= 1 + line.find("=")
        while line[pos]==' ': pos+=1
        return line[pos:-1]

    def _parse_color(self, line, strng):
        i=1
        while not (line[i] == " " or line[i] == "="):
            i += 1
        k=line[1:i]
        k=k.lower()                 #<- lowercase colors
        strng=strng.replace(' ','') # get rid of spaces
        lis=strng.split(',')
        r,g,b=lis
        self.colors.update({k:libtcod.Color(int(r),int(g),int(b))})
    

class Console:
    '''
        container for global tcod consoles
    '''
    def __init__(self,w,h):
        self.final   = libtcod.console_new(w,h) # final surface blitted to 0
        self.game    = libtcod.console_new(w,h) # intermediate surface, displays HUD, messages, and the game view


class Controller:
    '''
        state machine for game state
    '''
    def __init__(self):
        self.isRunning      = True
        self._state         = "normal"
        self._resume_state  = self._state
    
    def end(self):              self.isRunning=False
    def set_state(self,state):  self._state=state
    def set_resume_state(self,state):   self._resume_state=state
    
    @property
    def state(self):            return self._state
    @property
    def resume_state(self):     return self._resume_state



class Window:
    '''
        stores relative locations and sizes of
        rendering areas on the game window
    '''
    def __init__(self, w, h):
        # HUD
        HUD_W       = w
        HUD_H       = 2
        HUD_X       = 0
        HUD_Y       = h - HUD_H
        # Msgs
        MSGS_X      = 0
        MSGS_Y      = 0
        MSGS_W      = w
        MSGS_H      = 3
        # View
        VIEW_X      = 0
        VIEW_Y      = MSGS_H
        VIEW_W      = w
        VIEW_H      = h - HUD_H - MSGS_H
        
        self.root   = Box(0,0, w, h)
        self.hud    = Box( HUD_X, HUD_Y,  HUD_W, HUD_H)
        self.msgs   = Box(MSGS_X,MSGS_Y, MSGS_W,MSGS_H)
        self.scene  = Box(VIEW_X,VIEW_Y, VIEW_W,VIEW_H)

    def set_hud_left(self):
        self.hud.x = 0
        self.scene.x = self.hud.w
    def set_hud_right(self):
        self.hud.x = self.root.w - self.hud.w
        self.scene.x = 0
    def set_hud_visible(self,val):
        self.hud.visible = val

class Box():
    def __init__(self,x,y,w,h):
        self.x=x;self.y=y; self.w=w;self.h=h;
        self.visible = True


class View:
    def __init__(self,w,h,roomw,roomh):
        self.x=0; self.y=0; self.w=w;self.h=h; self.roomw=roomw;self.roomh=roomh
        self.followSpd=10
        self._fixed_mode=False
    def fixed_mode_toggle(self):    self._fixed_mode=not self._fixed_mode
    def fixed_mode_disable(self):   self._fixed_mode=False
    def fixed_mode_enable(self):    self._fixed_mode=True
        
    def nudge(self,dx,dy):
        if self._fixed_mode: return
        self.x += dx; self.y += dy;
        #self.limit_pos()
    
    def follow(self,obj):
        if self._fixed_mode: return
        if obj.x > self.x + self.w*2/3 -1:      self.nudge(self.followSpd,0)
        elif obj.x <= self.x + self.w*1/3 -1:   self.nudge(-self.followSpd,0)
        if obj.y - self.y >= self.h*1/2 +5:
            self.nudge(0,int(self.followSpd/2))
        elif obj.y - self.y < self.h*1/2 -5:
            self.nudge(0,int(-self.followSpd/2))
        
    def limit_pos(self):
        self.x = min(self.x, self.roomw - self.w)
        self.y = min(self.y, self.roomh - self.h)
        self.x = max(self.x, 0)
        self.y = max(self.y, 0)

    def center(self,x,y):
        if self._fixed_mode: return
        self.x = x - int(self.w/2)
        self.y = y - int(self.h/2)
        #self.limit_pos()


class Clock:
    '''
        game time and turn tracker
    '''
    def __init__(self):
        self._turn      = 0
        self._gametime  = 0
        self._timestamp = time.time()
    def turn_pass(self):
        self._turn +=1
        self._gametime += (time.time() - self._timestamp)
    @property
    def turn(self):         return self._turn



class Update:
    '''
        track what consoles need updating
    '''
    
    i=0;
    #U_PCFOV     =i;i+=1;
    U_GAME      =i;i+=1;
    U_HUD       =i;i+=1;
    U_MSG       =i;i+=1;
    U_FINAL     =i;i+=1;
    U_BASE      =i;i+=1;
    def __init__(self):
        self.set_all_to_false() #init dict
    
    #def pcfov(self):
    #    self.updates.add(Update.U_PCFOV)
    def game(self):
##        print('setting game update to true')
        self.updates.update({Update.U_GAME : True})
        self.updates.update({Update.U_FINAL : True})
    def hud(self):
##        print('setting hud update to true')
        self.updates.update({Update.U_HUD : True})
    def msg(self):
##        print('setting msg update to true')
        self.updates.update({Update.U_MSG : True})
    def final(self):
##        print('setting final update to true')
        self.updates.update({Update.U_FINAL : True})
        self.updates.update({Update.U_BASE : True})
    def base(self):
##        print('setting base update to true')
        self.updates.update({Update.U_BASE : True})

    '''def activate_all_necessary_updates(self):
        if Update.U_GAME in self.updates :   self.final()
        if (self.updates['final']):   self.base()'''
    
    def get_updates(self):
        return self.updates.items()

    def set_all_to_false(self):
        self.updates = {
            Update.U_GAME   : False,
            Update.U_HUD    : False,
            Update.U_MSG    : False,
            Update.U_FINAL  : False,
            Update.U_BASE   : False,
            }

    def update(self):
        clearMsg = False
        #activate_all_necessary_updates()
        if self.updates[Update.U_GAME]:
            rog.render_gameArea(rog.pc());
##            print('updating game')
        if self.updates[Update.U_HUD]:
            rog.render_hud(rog.pc());
##            print('updating hud')
        if self.updates[Update.U_MSG]:
            rog.logNewEntry();
            clearMsg=True;
##            print('updating msg')
        if self.updates[Update.U_FINAL]:
            rog.blit_to_final( rog.con_game(),0,0);
##            print('updating final')
        if self.updates[Update.U_BASE]:
            rog.refresh();
##            print('updating base')
        if clearMsg:
            rog.msg_clear()
        self.set_all_to_false()
    


class MessageLog:
    def __init__(self):
        self.msgs               = []
        self.msg_newEntry       = True
    
    def print(self,index):
        #todo: pass colored indeces into dbox func. to allow colored messages
        x=rog.msgs_x(); y=rog.msgs_y();
        w=rog.msgs_w(); h=rog.msgs_h();
        rog.dbox(x,y,w,h,self.msgs[index], border=None,margin=0)

    #delineate; indicate that the next turn has begun,
        #so messages start on a new entry in the log
    def drawNew(self):
        self.msg_newEntry = True
        if self.msgs: self.print(-1)
        
    def capitalize(self, text): return text[0].upper() + text[1:]
    
    def msg_format_start(self, text, turn):
        return "[{}] {}".format(turn,text)
    
    def add(self, text, turn):
        if len(text) == 0: return False
        rog.update_msg()
        new=self.capitalize(text)
        if (self.msg_newEntry):
            self.msg_newEntry = False
            self.msgs.append( self.msg_format_start(new, turn) )
        else:
            self.msgs[-1] += " {}".format(new) # NOTE: was simply: += new
        
    def printall_get_wrapped_msgs(self):
        w = rog.msgs_w()
        return '\n'.join( textwrap.fill( msg, w-2) for msg in reversed(self.msgs) )
    #


class GameData:
    '''
        global game data about current play session
    '''
    def __init__(self):
        self._dlvl = 1
        self._fame = 0 
            # Increases chance of strangers already knowing who you are
            #   and potentially already carrying an opinion of you.
            #   High fame makes you more reliable for questing in the eyes
            #   of quest-giving NPCs.
            #   NPCs who already know you do not change their opinion of
            #   you if you gain fame after they have met you.
        self._infamy = 0
            # Like fame, but carries a negative connotation.
    def dlvl(self):     return self._dlvl
    def fame(self):     return self._fame
    def infamy(self):   return self._infamy
    def fame_inc(self,val=1):   self._fame += val
    def infamy_inc(self,val=1): self._infamy += val
    def dlvl_update(self, value): #returns whether change was successful
        if value < 0: return False
        if value >= MAXLEVEL: return False
        self._dlvl = value
        return True



class SavedGame:
    
    def __init__(self):
        self.create_defaultData()
        #global save data is progress shared across savegames
        def getGlobalSaveFile():
            fname="globalsavedata.sav"
            try:
                self.file=os.path.join(
                    os.path.curdir,os.path.pardir,"save",fname)
            except:
                with open(os.path.join(
                    os.path.curdir,os.path.pardir,"save",fname), 'w+') as file:
                    pass
                self.file=os.path.join(
                    os.path.curdir,os.path.pardir,"save",fname)
                self._write_defaults()
        if os.path.exists(os.path.join(
            os.path.curdir,os.path.pardir,"save")):
            getGlobalSaveFile()
        else:
            try:
                os.mkdir(os.path.join(
                    os.path.curdir,os.path.pardir,"save"), )
            except OSError:
                print("Failed to create directory './save'. Aborting...")
                rog.end()
                return
            print("Successfully created directory './save'.")
            getGlobalSaveFile()
        #init empty lists to fill later during loading
        self.playableJobs=[]

    #make the list containing the data that will be saved into globalsavedata
        #by default (this is the lowest progress state)
    def create_defaultData(self):
        self.DEFAULTS = []
        #add jobs
        self.DEFAULTS.append('jobs')
        for job in entities.getJobs().values(): #job chars
            self.DEFAULTS.append(job)

    #load the global saved data that's shared between games
    def loadSavedData(self):
        mode=''
        try:
            with open(self.file, 'r') as file:
                for line in file:
                    if 'jobs' in line:
                        mode='jobs'
                    elif mode=='jobs':
                        self.playableJobs.append(line[:-1])
        except FileNotFoundError:
            print("ALERT: file '{}' not found.".format(self.file))
            print("Creating file '{}'...".format(self.file))
            self._write_defaults()
            print("Initializing defaults from '{}'...".format(self.file))
            self.loadSavedData()
        except:
            print("ERROR: saved data corrupted. Delete the file '{}' in the game's directory, and restart the game to init saved data to defaults...".format(self.file))
            raise
            
    def write_defaults(self):
        with open(self.file, 'w+') as file:
            for item in self.DEFAULTS:
                file.write("{}\n".format(item))

    #load a game currently in progress
    def loadGame(self):
        pass





         # commented out code below.



##
##class Environment:
##    def __init__(self):
##        self._genocides     = []
##        self._tokill        = []
##    
##    def genocide(self,typ):     self._genocides.append(typ)
##    def kill(self,mon):         self._tokill.append(mon)
##    def release_souls(self): # unregister entities that have died
##        if self._tokill:
##            for mon in self._tokill:
##                rog.release_creature(mon)
##            self._tokill=[]


 # TODO: use pickle or other serializer rather than this nonsense.

