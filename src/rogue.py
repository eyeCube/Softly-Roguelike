'''
    rogue.py
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

    This file glues everything together.
'''

import esper
import tcod as libtcod
import math

from const import *
from colors import COLORS as COL
import components as cmp
import processors as proc
import orangio  as IO
import action
import debug
import dice
import entities
import game
import levelgen
import lights
import misc
import managers
import maths
import player
import tilemap


EQUIPABLE_CONSTS={
EQ_MAINHANDW: cmp.EquipableInHoldSlot,
EQ_OFFHANDW : cmp.EquipableInHoldSlot,
EQ_MAINHAND : cmp.EquipableInHandSlot,
EQ_OFFHAND  : cmp.EquipableInHandSlot,
EQ_MAINARM  : cmp.EquipableInArmSlot,
EQ_OFFARM   : cmp.EquipableInArmSlot,
EQ_MAINLEG  : cmp.EquipableInLegSlot,
EQ_OFFLEG   : cmp.EquipableInLegSlot,
EQ_MAINFOOT : cmp.EquipableInFootSlot,
EQ_OFFFOOT  : cmp.EquipableInFootSlot,
EQ_FRONT    : cmp.EquipableInFrontSlot,
EQ_BACK     : cmp.EquipableInBackSlot,
EQ_CORE     : cmp.EquipableInCoreSlot,
EQ_HIPS     : cmp.EquipableInHipsSlot,
EQ_MAINHEAD : cmp.EquipableInHeadSlot,
EQ_MAINFACE : cmp.EquipableInFaceSlot,
EQ_MAINNECK : cmp.EquipableInNeckSlot,
EQ_MAINEYES : cmp.EquipableInEyesSlot,
EQ_MAINEARS : cmp.EquipableInEarsSlot,
EQ_AMMO     : cmp.EquipableInAmmoSlot,
    }


    #----------------#
    # global objects #
    #----------------#
            
class Rogue:
    occupations={}
    et_managers={} #end of turn managers
    bt_managers={} #beginning of turn managers
    c_managers={} #const managers
    manager = None # current active game state manager
    manager_listeners = [] #
    fov_maps = []
    # boolean flags
    allow_warning_msp = True    # for warning prompt for very slow move speed
    
    @classmethod
    def run_endTurn_managers(cls, pc):
        for v in cls.et_managers.values():
            v.run(pc)
    @classmethod
    def run_beginTurn_managers(cls, pc):
        for v in cls.bt_managers.values():
            v.run(pc)

    
##    @classmethod
##    def create_fov_maps(cls):
##        cls.fov_maps.append(cls.map.fov_map)
    @classmethod
    def create_settings(cls): # later controllers might depend on settings
        cls.settings = game.GlobalSettings()
        cls.settings.read() # go ahead and read/apply settings
        cls.settings.apply()
    @classmethod
    def create_world(cls):      cls.world = esper.World()
    @classmethod
    def create_controller(cls): cls.ctrl = game.Controller()
    @classmethod
    def create_window(cls):
        cls.window = game.Window(
            cls.settings.window_width, cls.settings.window_height
            )
    @classmethod
    def create_consoles(cls):
        cls.con = game.Console(window_w(),window_h())
    @classmethod
    def create_data(cls):       cls.data = game.GameData()
    @classmethod
    def create_map(cls, w, h):
        cls.map = tilemap.TileMap(w,h)
    @classmethod
    def create_clock(cls):      cls.clock = game.Clock()
    @classmethod
    def create_updater(cls):    cls.update = game.Update()
    @classmethod
    def create_view(cls):       cls.view = game.View(view_port_w(),view_port_h(), ROOMW,ROOMH)
    @classmethod
    def create_log(cls):        cls.log = game.MessageLog()
    @classmethod
    def create_savedGame(cls):  cls.savedGame = game.SavedGame()
    @classmethod
    def create_player(cls, sx,sy):
        cls.pc = player.chargen(sx, sy)
    @classmethod
    def create_processors(cls):
        #Processor class, priority (higher = processed first)
        cls.world.add_processor(proc.MetersProcessor(), 101)
        cls.world.add_processor(proc.StatusProcessor(), 100)
        cls.world.add_processor(proc.UpkeepProcessor(), 93)
        cls.world.add_processor(proc.FluidProcessor(), 92)
        cls.world.add_processor(proc.FireProcessor(), 91)
        cls.world.add_processor(proc.TimersProcessor(), 90)
            # AI function and queued actions processor
        cls.world.add_processor(proc.ActorsProcessor(), 50)
    
    @classmethod
    def create_perturn_managers(cls):
        '''
            constant, per-turn managers, ran each turn
        '''
        #ran at beginning of turn
            # (No managers run at beginning of turn currently.)
            
        #ran at end of turn (before player turn -- player turn is the very final thing to occur on any given turn)
            # None
            # Why were sights and sounds here? Bad idea.
    
    @classmethod
    def create_const_managers(cls):
        '''
            constant managers, manually ran
        '''
        cls.c_managers.update({'sights' : managers.Manager_SightsSeen()})
        cls.c_managers.update({'sounds' : managers.Manager_SoundsHeard()})
        cls.c_managers.update({'events' : managers.Manager_Events()})
        cls.c_managers.update({'lights' : managers.Manager_Lights()})
        cls.c_managers.update({'fov' : managers.Manager_FOV()})


    # EXPIRED: Environment class
#/Rogue

# global return values. Functions can modify this as an additional
#  "return" value list.
class Return:
    values=None
def globalreturn(*args): Return.values = args
def fetchglobalreturn():
    ret=Return.values
    Return.values=None
    return ret

# global warning flags
def allow_warning_msp():
    return Rogue.allow_warning_msp
def reset_warning_msp():
    Rogue.allow_warning_msp = True
def expire_warning_msp():
    Rogue.allow_warning_msp = False

    #----------------#
    #   Functions    #
    #----------------#

# global objects
def settings():     return Rogue.settings

# ECS
def get_slots(obj): # should only be used if absolutely necessary...
   return set(getattr(obj, '__slots__', set()))

# world
def world():    return Rogue.world

# player
def pc():       return Rogue.pc
def is_pc(ent): return (ent==Rogue.pc)

# saved game
def playableJobs():
    return entities.getJobs().items() #Rogue.savedGame.playableJobs

# log
def get_time(turn):
    tt = turn + STARTING_TIME
    day = 1 + tt // 86400
    hour = (tt // 3600) % 24
    minute = (tt // 60) % 60
    second = tt % 60
    return "D{},{:02d}:{:02d}:{:02d}".format(day, hour, minute, second)
def logNewEntry():
    Rogue.log.drawNew()
def msg(txt, col=None):
    if col is None: #default text color
        col=COL['white']
    Rogue.log.add(txt, str(get_time(get_turn())) )
def msg_clear():
    clr=libtcod.console_new(msgs_w(), msgs_h())
    libtcod.console_blit(clr, 0,0, msgs_w(),msgs_h(),  con_game(), 0,0)
    libtcod.console_delete(clr)

# game data
def dlvl():             return Rogue.data.dlvl() #current dungeon level of player
def level_up():         Rogue.data.dlvl_update(Rogue.data.dlvl() + 1)
def level_down():       Rogue.data.dlvl_update(Rogue.data.dlvl() - 1)
def level_set(lv):
    # TODO: code for loading / unloading levels into the map
    # unload current map from Rogue.map into the levels dict
    # load new map into Rogue.map from the levels dict
    # update dlvl
    Rogue.data.dlvl_update(lv)

# clock
def turn_pass():        Rogue.clock.turn_pass()
def get_turn():         return Rogue.clock.turn

# view
def view_nudge(dx,dy):      Rogue.view.nudge(dx,dy)
def view_nudge_towards(ent):Rogue.view.follow(ent)
def view_center(ent):
    pos=Rogue.world.component_for_entity(ent, cmp.Position)
    Rogue.view.center(pos.x, pos.y)
def view_center_player():
    pos=Rogue.world.component_for_entity(Rogue.pc, cmp.Position)
    Rogue.view.center(pos.x, pos.y)
def view_center_coords(x,y):Rogue.view.center(x,y)
def view_x():       return  Rogue.view.x
def view_y():       return  Rogue.view.y
def view_w():       return  Rogue.view.w
def view_h():       return  Rogue.view.h
def view_max_x():   return  ROOMW - Rogue.view.w #constraints on view panning
def view_max_y():   return  ROOMH - Rogue.view.h
def fixedViewMode_toggle(): Rogue.view.fixed_mode_toggle()

# map
def getmap(z=None): # get TileMap obj for the corresponding dungeon level
    if z is None:
        z = dlvl()
    if z == dlvl():
        return Rogue.map
    else:
        level_set(z)
        return Rogue.map
def tile_get(x,y):          return Rogue.map.get_char(x,y)
def tile_height(x,y):       return Rogue.map.get_height(x,y)
def tile_change(x,y,char):
    updateNeeded=Rogue.map.tile_change(x,y,char)
    if updateNeeded:
        update_all_fovmaps()
def map_reset_lighting():   Rogue.map.grid_lighting_init()
def tile_lighten(x,y,value):Rogue.map.tile_lighten(x,y,value)
def tile_darken(x,y,value): Rogue.map.tile_darken(x,y,value)
def get_actual_light_value(x,y):
    return Rogue.map.get_light_value(x,y)
def get_perceived_light_value(x,y):
    return Rogue.map.get_perceived_light_value(x,y)
##def map_generate(Map,level): levels.generate(Map,level) #OLD OBSELETE
def identify_symbol_at(x,y):
    asci = libtcod.console_get_char(0, getx(x),gety(y))
    char = "{} ".format(chr(asci)) if (asci < 128 and not asci==32) else ""
    desc="__IDENTIFY UNIMPLEMENTED__" #IDENTIFIER.get(asci,"???")
    return "{}{}".format(char, desc)
def grid_remove(ent): #remove thing from grid of things
    return Rogue.map.remove_thing(ent)
def grid_insert(ent): #add thing to the grid of things
    return Rogue.map.add_thing(ent)
def grid_fluids_insert(obj):    Rogue.map.grid_fluids[obj.x][obj.y].append(obj)
def grid_fluids_remove(obj):    Rogue.map.grid_fluids[obj.x][obj.y].remove(obj)

# updater
def update_base():      Rogue.update.base()
#def update_pcfov():     Rogue.update.pcfov()
def update_game():      Rogue.update.game()
def update_msg():       Rogue.update.msg()
def update_hud():       Rogue.update.hud()
def update_final():     Rogue.update.final()
#apply all updates if applicable
def game_update():      Rogue.update.update()

# consoles
def con_game():             return Rogue.con.game
def con_final():            return Rogue.con.final

# controller
def end():                  Rogue.ctrl.end()
def game_state():           return Rogue.ctrl.state
def game_is_running():      return Rogue.ctrl.isRunning
def game_set_state(state="normal"):
    print("$---Game State changed from {} to {}".format(game_state(), state))
    Rogue.ctrl.set_state(state)
def game_resume_state():    return Rogue.ctrl.resume_state
def set_resume_state(state):Rogue.ctrl.set_resume_state(state)

# window
def window_w():         return Rogue.window.root.w
def window_h():         return Rogue.window.root.h
def view_port_x():      return Rogue.window.scene.x
def view_port_y():      return Rogue.window.scene.y
def view_port_w():      return Rogue.window.scene.w
def view_port_h():      return Rogue.window.scene.h
def hud_x():            return Rogue.window.hud.x
def hud_y():            return Rogue.window.hud.y
def hud_w():            return Rogue.window.hud.w
def hud_h():            return Rogue.window.hud.h
def msgs_x():           return Rogue.window.msgs.x
def msgs_y():           return Rogue.window.msgs.y
def msgs_w():           return Rogue.window.msgs.w
def msgs_h():           return Rogue.window.msgs.h
def set_hud_left():     Rogue.window.set_hud_left()
def set_hud_right():    Rogue.window.set_hud_right()

    # functions from modules #

# orangio

def init_keyBindings():
    IO.init_keyBindings()


# game

def dbox(x,y,w,h,text='', wrap=True,border=0,margin=0,con=-1,disp='poly'):
    '''
        x,y,w,h     location and size
        text        display string
        border      border style. None = No border
        wrap        whether to use automatic word wrapping
        margin      inside-the-box text padding on top and sides
        con         console on which to blit textbox, should never be 0
                        -1 (default) : draw to con_game()
        disp        display mode: 'poly','mono'
    '''
    if con==-1: con=con_game()
    misc.dbox(x,y,w,h,text, wrap=wrap,border=border,margin=margin,con=con,disp=disp)
    
def makeConBox(w,h,text):
    con = libtcod.console_new(w,h)
    dbox(0,0, w,h, text, con=con, wrap=False,disp='mono')
    return con




    # printing functions #

#@debug.printr
def refresh():  # final to root and flush
    libtcod.console_blit(con_final(), 0,0,window_w(),window_h(),  0, 0,0)
    libtcod.console_flush()
#@debug.printr
def render_gameArea(pc) :
    con = Rogue.map.render_gameArea(pc, view_x(),view_y(),view_w(),view_h() )
    libtcod.console_clear(con_game()) # WHY ARE WE DOING THIS?
    libtcod.console_blit(con, view_x(),view_y(),view_w(),view_h(),
                         con_game(), view_port_x(),view_port_y())
#@debug.printr
def render_hud(pc) :
    con = misc.render_hud(hud_w(),hud_h(), pc, get_turn(), dlvl() )
    libtcod.console_blit(con,0,0,0,0, con_game(),hud_x(),hud_y())
def clear_final():
    libtcod.console_clear(con_final())
#@debug.printr
def blit_to_final(con,xs,ys, xdest=0,ydest=0): # window-sized blit to final
    libtcod.console_blit(con, xs,ys,window_w(),window_h(),
                         con_final(), xdest,ydest)
#@debug.printr
def alert(text=""):    # message that doesn't go into history
    dbox(msgs_x(),msgs_y(),msgs_w(),msgs_h(),text,wrap=False,border=None,con=con_final())
    refresh()



# Error checking
class ComponentException(Exception):
    ''' raised when an entity lacks an expected component. '''
    pass

def asserte(ent, condition, errorstring=""): # "ASSERT Entity"
    ''' ASSERT condition condition satisifed, else raise error
        and print ID info about the Entity ent.'''
    if not condition:
        # name
        if Rogue.world.has_component(ent, cmp.Name):
            entname="with name '{}'".format(
                Rogue.world.component_for_entity(ent, cmp.Name).name)
        else:
            entname="<NO NAME>"
        # position
        if Rogue.world.has_component(ent, cmp.Position):
            entposx=Rogue.world.component_for_entity(ent, cmp.Position).x
            entposy=Rogue.world.component_for_entity(ent, cmp.Position).y
        else:
            entposx = entposy = -1
        # message
        print("ERROR: rogue.py: function getms: entity {e} {n} at pos ({x},{y}) {err}".format(
            e=ent, n=entname, x=entposx, y=entposy, err=errorstring))
        raise ComponentException
# end def


# Name functions

def identify(idtype): return IDENTIFICATION[idtype][0]
def fullname_gear(ent):
    world=Rogue.world
    fullname = world.component_for_entity(ent, cmp.Name).name
    if ( world.has_component(ent, cmp.Fitted)
         and Rogue.pc==world.component_for_entity(ent, cmp.Fitted).entity ):
        fullname = "fitted {}".format(fullname)
    return fullname
# end def
def fullname(ent):
    '''
        get the full name with any prefixes, suffixes, etc.
         (but do not add the title)
        this depends on the level of identification the player has
         for the entity -- at anything less than max level ID, the actual
         name is not displayed, but a pseudonym which describes it in
         some vague fashion e.g. "club" instead of "metal cudgel"
    '''
    world=Rogue.world
    fullname = world.component_for_entity(ent, cmp.Name).name
    
    if world.has_component(ent, cmp.Identified):
        quality = world.component_for_entity(ent, cmp.Identified).quality
        assert(quality>0)
        
        # LOW-LEVEL ID (type of thing) (identify basic type)
        if quality==1:
            idtype = world.component_for_entity(ent, cmp.Identify).generic
            fullname = "{} {}".format(UNID, identify(idtype))
            return fullname
        
        # LOW-LEVEL ID (+ MATERIAL) (identify make-up)
        elif quality==2: 
            idtype = world.component_for_entity(ent, cmp.Identify).generic
            mat = world.component_for_entity(ent, cmp.Form).material
            fullname = "{} {} {}".format(UNID, mat, identify(idtype))
            return fullname

        # IDEA: mid-level Identification: identify skill required,
        #  uses, etc. (identify the purpose of the item)

        elif quality==3: # FULL IDENTIFICATION OF UNIQUE INSTANCE
            pass # continue with full identification
        
    else: # SHAPE ONLY
        # we can only identify it by its vague form
        shape = world.component_for_entity(ent, cmp.Form).shape
        return "{} {}".format(UNID, SHAPES[shape])
    
    # full identification #
    
    if world.has_component(ent, cmp.Prefixes):
        compo = world.component_for_entity(ent, cmp.Prefixes)
        for string in compo.strings:
            fullname = "{} {}".format(string, fullname)
            
    if world.has_component(ent, cmp.StatusRusted):
        compo = world.component_for_entity(ent, cmp.StatusRusted)
        for k,v in RUST_QUALITIES.items():
            if compo.quality == k:
                string = RUSTEDNESS[v][2] # TODO: test
                fullname = "{} {}".format(string, fullname)
                break
            
    if world.has_component(ent, cmp.StatusRotted):
        compo = world.component_for_entity(ent, cmp.StatusRotted)
        for k,v in ROT_QUALITIES.items():
            if compo.quality == k:
                string = ROTTEDNESS[v][2] # TODO: test
                fullname = "{} {}".format(string, fullname)
                break
            
    return fullname
# end def


    # "Fun"ctions #

def ceil(i): return math.ceil(i)
def line(x1,y1,x2,y2):
    for tupl in misc.Bresenham2D(x1,y1,x2,y2):
        yield tupl
def in_range(x1,y1,x2,y2,Range):
    return (maths.dist(x1,y1, x2,y2) <= Range + .34)
def around(i): # round with an added constant to nudge values ~0.5 up to 1 (attempt to get past some rounding errors)
    return round(i + 0.00001)
def sign(n):
    if n>0: return 1
    if n<0: return -1
    return 0
def numberplace(i): # convert integer to numbering position / numbering place / number position / number place
    if i==1: return "1st"
    if i==2: return "2nd"
    if i==3: return "3rd"
    return "{}th".format(i)

# stat getters
def _getkg(value):      return value//MULT_MASS
def _getstat(value):    return value//MULT_STATS
def _getatt(value):     return value//MULT_ATT
def getkg(ent):         return _getmass(getms(ent, 'mass'))
def getstat(ent, stat): return _getstat(getms(ent, stat))
def getatt(ent, att):   return _getatt(getms(ent, att))

# component getters | parent / child functions
def getpos(ent):
    ''' # get parent position if applicable else self position
        Returns: Position component.
        Global Returns: whether or not the component belongs
            to a parent (True) or not (False)
    '''
    if Rogue.world.has_component(ent, cmp.Child):
        parent=Rogue.world.component_for_entity(ent, cmp.Child).parent
        globalreturn(True)
        return Rogue.world.component_for_entity(parent, cmp.Position)
    globalreturn(False)
    return Rogue.world.component_for_entity(ent, cmp.Position)
def getdir(ent):
    ''' # get parent direction if applicable else self direction
        Returns: Direction component.
        Global Returns: whether or not the component belongs
            to a parent (True) or not (False)
    '''
    if Rogue.world.has_component(ent, cmp.Child):
        parent=Rogue.world.component_for_entity(ent, cmp.Child).parent
        globalreturn(True)
        return Rogue.world.component_for_entity(parent, cmp.Direction)
    globalreturn(False)
    return Rogue.world.component_for_entity(ent, cmp.Direction)
def getname(ent):
    return Rogue.world.component_for_entity(ent, cmp.Name).name
    

# tilemap
def thingat(x,y):       return Rogue.map.thingat(x,y) #entity at
def thingsat(x,y):      return Rogue.map.thingsat(x,y) #list
def inanat(x,y):        return Rogue.map.inanat(x,y) #inanimate entity at
def monat (x,y):        return Rogue.map.monat(x,y) #monster at
def solidat(x,y):       return Rogue.map.solidat(x,y) #solid entity at
def wallat(x,y):        return (not Rogue.map.get_nrg_cost_enter(x,y) ) #tile wall
def fluidsat(x,y):      return Rogue.et_managers['fluids'].fluidsat(x,y) #list
def lightsat(x,y):      return Rogue.map.lightsat(x,y) #list
def fireat(x,y):        return False #Rogue.et_managers['fire'].fireat(x,y)
    # calculating cost to move across tiles
def cost_enter(x,y):    return Rogue.map.get_nrg_cost_enter(x,y)
def cost_leave(x,y):    return Rogue.map.get_nrg_cost_leave(x,y)
def cost_move(xf,yf,xt,yt,data):
    return Rogue.map.path_get_cost_movement(xf,yf,xt,yt,data)
    # checking for in bounds / out of bounds / outside of room boundary
def is_in_grid_x(x):    return (x>=0 and x<ROOMW)
def is_in_grid_y(y):    return (y>=0 and y<ROOMH)
def is_in_grid(x,y):    return (x>=0 and x<ROOMW and y>=0 and y<ROOMH)

# view
def getx(x):        return x + view_port_x() - view_x()
def gety(y):        return y + view_port_y() - view_y()
def mapx(x):        return x - view_port_x() + view_x()
def mapy(y):        return y - view_port_y() + view_y()

# terraforming
def dig(x,y):
    #dig a hole in the floor if no solids here
    #else dig the wall out
    #use rogue's tile_change func so we update all FOVmaps
    tile_change(x,y,FLOOR)
def singe(x,y): #burn tile
    if Rogue.map.get_char(x,y) == FUNGUS:
        tile_change(x,y,FLOOR)

def wind_force():
    return 0 # TEMPORARY, TODO: create wind processor
def wind_direction():
    return (1,0,) # TEMPORARY, TODO: create wind processor


    # component functions #

# NOTE: generally better to call directly and save the function call overhead
# Thus we should not really use these functions...

def get(ent, component): #return an entity's component
    return Rogue.world.component_for_entity(ent, component)
def has(ent, component): #return whether entity has component
    return Rogue.world.has_component(ent, component)
def match(component):
    return Rogue.world.get_component(component)
def matchx(*components):
    return Rogue.world.get_components(components)
    return True
def copyflags(toEnt,fromEnt): #use this to set an object's flags to that of another object.
    for flag in Rogue.world.component_for_entity(fromEnt, cmp.Flags).flags:
        make(toEnt, flag)

# duplicate component functions -- create copy(s) of a component
def dupCmpMeters(meters):
    newMeters = cmp.Meters()
    newMeters.temp = meters.temp
    newMeters.rads = meters.rads
    newMeters.sick = meters.sick
    newMeters.expo = meters.expo
    newMeters.pain = meters.pain
    newMeters.fear = meters.fear
    newMeters.bleed = meters.bleed
    newMeters.rust = meters.rust
    newMeters.rot = meters.rot
    newMeters.wet = meters.wet
    return newMeters


    # entity functions #

# getms: GET Modified Statistic (base stat + modifiers (permanent and conditional))
def getms(ent, _var): # NOTE: must set the DIRTY_STATS flag to true whenever any stats or stat modifiers change in any way! Otherwise the function will return an old value!
    world=Rogue.world
    asserte(ent,world.has_component(ent,cmp.ModdedStats),"has no ModdedStats component.")
    if on(ent, DIRTY_STATS): # dirty; re-calculate the stats first.
        makenot(ent, DIRTY_STATS) # make sure we don't get caught in infinite loop...
        modded=_update_stats(ent)
        return modded.__dict__[_var]
    return Rogue.world.component_for_entity(ent, cmp.ModdedStats).__dict__[_var]
def getbase(ent, _var): # get Base statistic
    return Rogue.world.component_for_entity(ent, cmp.Stats).__dict__[_var]
# SET Stat -- set stat stat to value val set base stat 
def sets(ent, stat, val):
    Rogue.world.component_for_entity(ent, cmp.Stats).__dict__[stat] = val
    make(ent, DIRTY_STATS)
# ALTer Stat -- change stat stat by val value
def alts(ent, stat, val):
    Rogue.world.component_for_entity(ent, cmp.Stats).__dict__[stat] += val
    make(ent, DIRTY_STATS)
def setAP(ent, val):
    actor=Rogue.world.component_for_entity(ent, cmp.Actor)
    actor.ap = val
def spendAP(ent, amt):
    actor=Rogue.world.component_for_entity(ent, cmp.Actor)
    actor.ap = actor.ap - amt

# skills
def getskill(ent, skill): # return skill level in a given skill
    assert(Rogue.world.has_component(ent, cmp.Skills))
    skills = Rogue.world.component_for_entity(ent, cmp.Skills)
    return _getskill(skills.skills.get(skill, 0))
def getskillxp(ent, skill): # return skill experience in a given skill
    assert(Rogue.world.has_component(ent, cmp.Skills))
    skills = Rogue.world.component_for_entity(ent, cmp.Skills)
    return skills.skills.get(skill, 0)
def _getskill(exp): return exp // EXP_LEVEL
def setskill(ent, skill, lvl): # set skill level
    assert(Rogue.world.has_component(ent, cmp.Skills))
    skills = Rogue.world.component_for_entity(ent, cmp.Skills)
    skills.skills[skill] = lvl*EXP_LEVEL
    make(ent,DIRTY_STATS)
def train(ent, skill, pts): # train (improve) skill
    if getskill(ent, skill) >= MAX_SKILL:
        return
    # trait bonuses
    if Rogue.world.has_component(ent, cmp.Talented):
        compo = Rogue.world.component_for_entity(ent, cmp.Talented)
        if compo.skill==skill:
            pts = pts * TALENTED_EXPMOD
    if Rogue.world.has_component(ent, cmp.FastLearner):
        pts = pts * FASTLEARNER_EXPMOD
    # intelligence bonus to experience
    pts += around( getms(ent,'int')*pts*EXP_INT_BONUS )
    # diminishing returns on skill gainz
    pts = around( pts - getskill(ent)*EXP_DIMINISH_RATE )
    # points calculated; try to apply experience
    if pts > 0:
        make(ent,DIRTY_STATS)
        skills = Rogue.world.component_for_entity(ent, cmp.Skills)
        __train(skills, skill, pts)
def __train(skills, skill, pts): # train one level at a time
    if getskill(ent, skill) >= MAX_SKILL:
        return
    exp = min(pts, EXP_LEVEL)
    skills.skills[skill] = skills.skills.get(skill, 0) + exp
    pts = pts - exp - EXP_DIMINISH_RATE
    if pts > 0:
        __train(ent, skill, pts)
def forget(ent, skill, pts): # lose skill experience
    assert(Rogue.world.has_component(ent, cmp.Skills))
    skills = Rogue.world.component_for_entity(ent, cmp.Skills)
    skills.skills[skill] = max(0, skills.skills.get(skill, pts) - pts)
    make(ent,DIRTY_STATS)

# flags
def on(ent, flag):
    return flag in Rogue.world.component_for_entity(ent, cmp.Flags).flags
def make(ent, flag):
    Rogue.world.component_for_entity(ent, cmp.Flags).flags.add(flag)
def makenot(ent, flag):
    Rogue.world.component_for_entity(ent, cmp.Flags).flags.remove(flag)
def makeimmune(ent, flag):
    make(ent, flag)
    if flag==IMMUNEBLEED:
        make(ent, DIRTYSTATS)
        clear_status(ent, cmp.StatusBleed)
    elif flag==IMMUNERUST:
        make(ent, DIRTYSTATS)
        clear_status(ent, cmp.StatusRusted)
    elif flag==IMMUNEROT:
        make(ent, DIRTYSTATS)
        clear_status(ent, cmp.StatusRotted)
    elif flag==IMMUNEPAIN:
        make(ent, DIRTYSTATS)
        clear_status(ent, cmp.StatusPain)
#

# inventory give/take items
def give(ent,item):
    assert(Rogue.world.has_component(item, cmp.Encumberance))
    
    if get_status(item, cmp.StatusBurn):
        burn(ent, FIRE_BURN)
        cooldown(item)
    
    Rogue.world.component_for_entity(ent, cmp.Inventory).data.append(item)
# end def

def take(ent,item):
    Rogue.world.component_for_entity(ent, cmp.Inventory).data.remove(item)

def mutate(ent):
    # TODO: do mutation
    mutable = Rogue.world.component_for_entity(ent, cmp.Mutable)
    pos = Rogue.world.component_for_entity(ent, cmp.Position)
    entn = Rogue.world.component_for_entity(ent, cmp.Name)
    # TODO: message based on mutation (i.e. "{t}{n} grew an arm!") Is this dumb?
    event_sight(pos.x,pos.y,"{t}{n} mutated!".format(
        t=TITLES[entn.title],n=entn.name))

def has_sight(ent):
    if (Rogue.world.has_component(ent, cmp.SenseSight) and not on(ent,BLIND)):
        return True
    else:
        return False
def has_hearing(ent):
    if (Rogue.world.has_component(ent, cmp.SenseHearing) and not on(ent,DEAF)):
        return True
    else:
        return False

def port(ent,x,y): # move thing to absolute location, update grid and FOV
    grid_remove(ent)
    pos = Rogue.world.component_for_entity(ent, cmp.Position)
    pos.x=x; pos.y=y;
    grid_insert(ent)
    update_fov(ent) # is this necessary? It was commented out, but AI seems to have no way to set the flag to update its FOV.
    if Rogue.world.has_component(ent, cmp.LightSource):
        compo = Rogue.world.component_for_entity(ent, cmp.LightSource)
        compo.light.reposition(x, y)

def pocket(ent, item):
    world=Rogue.world
    grid_remove(item)
    give(ent, item)
    spendAP(ent, NRG_POCKET)
    world.add_component(item, cmp.Child(ent)) # item is Child of Entity carrying the item
    if world.has_component(item, cmp.Position):
        world.remove_component(item, cmp.Position)
    
def drop(ent,item,dx=0,dy=0):   #remove item from ent's inventory, place it on ground nearby ent.
    world=Rogue.world
    make(ent, DIRTY_STATS)
    take(ent,item)
    world.remove_component(item, cmp.Child)
    entpos=world.component_for_entity(ent, cmp.Position)
    world.add_component(item, cmp.Position(entpos.x + dx, entpos.y + dy))
    grid_insert(item)

def givehp(ent,val=9999):
    stats = Rogue.world.component_for_entity(ent, cmp.Stats)
    stats.hp = min(getms(ent, 'hpmax'), stats.hp + val)
    make(ent,DIRTY_STATS)
def givemp(ent,val=9999):
    stats = Rogue.world.component_for_entity(ent, cmp.Stats)
    stats.mp = min(getms(ent, 'mpmax'), stats.mp + val)
    make(ent,DIRTY_STATS)
def caphp(ent): # does not make stats dirty! Doing so is a huge glitch!
    stats = Rogue.world.component_for_entity(ent, cmp.Stats)
    stats.hp = min(stats.hp, getms(ent,'hpmax'))
def capmp(ent): # does not make stats dirty! Doing so is a huge glitch!
    stats = Rogue.world.component_for_entity(ent, cmp.Stats)
    stats.mp = min(stats.mp, getms(ent,'mpmax'))


# these aren't tested, nor are they well thought-out
def knock(ent, amt): # apply force to an entity
    mass = getms(ent, 'mass')
    bal = getms(ent, 'bal')
    effmass = mass * bal / BAL_MASS_MULT # effective mass
    dmg = amt // effmass
    stagger(ent, dmg)
def stagger(ent, dmg): # reduce balance by dmg
    if Rogue.world.has_component(ent, cmp.StatusOffBalance):
        compo=Rogue.world.component_for_entity(ent, cmp.StatusOffBalance)
        dmg = dmg + compo.quality
    set_status(ent, cmp.StatusOffBalance(
        t = min(8, 1 + dmg//4), q=dmg) )

    
#damage hp
def damage(ent, dmg: int):
##    assert isinstance(dmg, int)
    if dmg <= 0: return
    make(ent,DIRTY_STATS)
    stats = Rogue.world.component_for_entity(ent, cmp.Stats)
    stats.hp -= dmg
    if stats.hp <= 0:
        kill(ent)
def damage_phys(ent, dmg: int):
    if dmg <= 0: return
    resMult = 0.01*(100 - getms(ent, 'resphys'))     # resistance multiplier
    damage(ent, around(dmg*resMult))

#damage mp (stamina)
def sap(ent, dmg: int, exhaustOnZero=True):
##    assert isinstance(dmg, int)
##    print('sapping ', dmg)
    if dmg < 0: return
    make(ent,DIRTY_STATS)
    stats = Rogue.world.component_for_entity(ent, cmp.Stats)
    stats.mp = int(stats.mp - dmg)
    if stats.mp <= 0:
        if exhaustOnZero:
            exhaust(ent) # TODO
        else:
            stats.mp = 0

def exhaust(ent):
    print('ent named {} exhausted.'.format(getname(ent)))
    kill(ent)

# satiation / hydration
def feed(ent, sat, hyd): # add satiation / hydration w/ Digest status
    if world.has_component(ent, cmp.StatusDigest):
        compo = Rogue.world.component_for_entity(ent, cmp.StatusDigest)
        compo.satiation += sat
        compo.hydration += hyd
    else:
        world.add_component(ent, cmp.StatusDigest(cald, hydd))
def sate(ent, pts):
    compo = Rogue.world.component_for_entity(ent, cmp.Body)
    compo.satiation = min(compo.satiation + pts, compo.satiationMax)
    #TODO: convert excess calories to fat(?) how/where should this be done?
def hydrate(ent, pts):
    compo = Rogue.world.component_for_entity(ent, cmp.Body)
    compo.hydration = min(compo.hydration + pts, compo.hydrationMax)

    #------------------#
    # elemental damage #
    #------------------#

# RECursively apply ELEMent to all items touching/held/carried by the entity
def recelem(ent, func, dmg, **kwargs):
    # apply to inventory items
    inv=Rogue.world.component_for_entity(ent, cmp.Inventory).data
##    invres=... # inventory resistance. Should backpack be a separate entity w/ its own inventory? Inventories combine into one?
    for item in inv:
        func(item, dmg, kwargs)
    # apply to the entity itself
    return func(ent, dmg, kwargs)
# INTENDED SYNTAX: (TODO: test to make sure this works before applying to all elements.)
def NEWburn(ent, dmg, maxTemp=999999):
    return recelem(ent, entities.burn, dmg, maxTemp=maxTemp)
        
        
def settemp(ent, temp):
    Rogue.world.component_for_entity(ent, cmp.Meters).temp = temp
def burn(ent, dmg, maxTemp=999999):
    return entities.burn(ent, dmg, maxTemp)
def cool(ent, dmg, minTemp=-300):
    return entities.burn(ent, dmg, minTemp)
def bleed(ent, dmg):
    return entities.bleed(ent, dmg)
def hurt(ent, dmg):
    return entities.hurt(ent, dmg)
def disease(ent, dmg):
    return entities.disease(ent, dmg)
def intoxicate(ent, dmg):
    return entities.intoxicate(ent, dmg)
def irradiate(ent, dmg):
    return entities.irradiate(ent, dmg)
def irritate(ent, dmg):
    return entities.irritate(ent, dmg)
def exposure(ent, dmg):
    return entities.exposure(ent, dmg)
def corrode(ent, dmg):
    return entities.corrode(ent, dmg)
def cough(ent, dmg):
    return entities.cough(ent, dmg)
def vomit(ent, dmg):
    return entities.vomit(ent, dmg)
def electrify(ent, dmg):
    return entities.electrify(ent, dmg)
def paralyze(ent, dur):
    return entities.paralyze(ent, dur)
def wet(ent, g):
    return entities.wet(ent, g)
def rot(ent, g):
    return entities.rot(ent, g)
def dirty(ent, g):
    return entities.dirty(ent, g)
def mutate(ent):
    return entities.mutate(ent)
    
def kill(ent): #remove a thing from the world
    if on(ent, DEAD): return
    world = Rogue.world
    _type = world.component_for_entity(ent, cmp.Draw).char
    if world.has_component(ent, cmp.DeathFunction): # call destroy function
        world.component_for_entity(ent, cmp.DeathFunction).func(ent)
    make(ent, DEAD)
    clear_status_all(ent)
    
    # handle any dependencies shared by this entity before removing it #
    
    # unequip entity if it's currently being worn / held as an equip
    if world.has_component(ent, cmp.Equipped):
        compo = world.component_for_entity(ent, cmp.Equipped)
        deequip(compo.owner, compo.equipType)
        
    # drop entity's equipped items if applicable
    if world.has_component(ent, cmp.Body):
        deequip_all(ent)
    
    # remove entity from inventory if it's being carried
    if world.has_component(ent, cmp.Carried):
        compo = world.component_for_entity(ent, cmp.Carried)
        drop(compo.owner, ent)
        
    # drop entity's inventory if it's carrying anything
    if world.has_component(ent, cmp.Inventory):
        for tt in world.component_for_entity(ent, cmp.Inventory).data:
            drop(ent, tt)
    
    # remains #
    
    # creatures
    isCreature = world.has_component(ent, cmp.Creature)
    if isCreature:
        # create a corpse
        if dice.roll(100) < entities.corpse_recurrence_percent[_type]:
            create_corpse(ent)
    # inanimate things
    else:
        # burn to ashes
        if get_status(ent, cmp.StatusBurn):
            mat = world.component_for_entity(ent, cmp.Form).material
            if (mat==MAT_FLESH
                or mat==MAT_WOOD
                or mat==MAT_FUNGUS
                or mat==MAT_VEGGIE
                or mat==MAT_LEATHER
                ):
                create_ashes(ent)
    # end if
    
    # cleanup #
    release_entity(ent) #remove dead thing
# end def

def zombify(ent):
    kill(ent) # temporary
def explosion(name, x, y, radius):
    event_sight(x, y, "{n} explodes!".format(n=name))

# inreach | in reach | in_reach 
# Calculate if your target is within your reach (melee range).
# Instead of calculating with a slow* sqrt func, we access this cute grid:
_REACHGRIDQUAD=[ #0==origin
    [12,12,99,99,99,99,99,],
    [10,10,11,12,99,99,99,], # we only need 1 quadrant of the total
    [8, 8, 9, 10,11,99,99,], # grid to calculate if you are in reach.
    [6, 7, 7, 9, 10,12,99,],
    [4, 5, 6, 7, 9, 11,99,],
    [2, 3, 5, 7, 8, 10,12,],
    [0, 2, 4, 6, 8, 10,12,],
]
#   *also gives me direct control over reach required for specific range.
def inreach(x1,y1, x2,y2, reach):
    ''' reach is the stat //MULT_STATS but not divided by 2 '''
    xd = abs(x2 - x1) # put the coordinates in the upper right quadrant ...
    yd = -abs(y2 - y1) # ... to match with the quadrant grid above
    if (xd > MAXREACH or yd < -MAXREACH): return False # max distance exceeded
    reachNeeded = _REACHGRIDQUAD[MAXREACH+yd][xd]
    if reach >= reachNeeded:
        return True
    return False
# end def
def dist(x1,y1,x2,y2): return misc.dist(x1,y1,x2,y2)
def fitgear(gear, ent):
    Rogue.world.add_component(gear, cmp.Fitted(ent))



    #----------------------#
    #        Events        #
    #----------------------#


def event_sight(x,y,text):
    if not text: return
    Rogue.c_managers['events'].add_sight(x,y,text)
def event_sound(x,y,data):
    if (not data): return
    volume,text1,text2=data
    Rogue.c_managers['events'].add_sound(x,y,text1,text2,volume)
# TODO: differentiate between 'events' and 'sights' / 'sounds' which are for PC entity only (right???)
def listen_sights(ent):     return  Rogue.c_managers['events'].get_sights(ent)
def add_listener_sights(ent):       Rogue.c_managers['events'].add_listener_sights(ent)
def remove_listener_sights(ent):    Rogue.c_managers['events'].remove_listener_sights(ent)
def clear_listen_events_sights(ent):Rogue.c_managers['events'].clear_sights(ent)
def listen_sounds(ent):     return  Rogue.c_managers['events'].get_sounds(ent)
def add_listener_sounds(ent):       Rogue.c_managers['events'].add_listener_sounds(ent)
def remove_listener_sounds(ent):    Rogue.c_managers['events'].remove_listener_sounds(ent)
def clear_listen_events_sounds(ent):Rogue.c_managers['events'].clear_sounds(ent)
def clear_listeners():              Rogue.c_managers['events'].clear()
    
##def listen_sights(ent):     return  Rogue.c_managers['sights'].get_sights(ent)
##def add_listener_sights(ent):       Rogue.c_managers['sights'].add_listener_sights(ent)
##def remove_listener_sights(ent):    Rogue.c_managers['sights'].remove_listener_sights(ent)
##def clear_listen_events_sights(ent):Rogue.c_managers['sights'].clear_sights(ent)
##def listen_sounds(ent):     return  Rogue.c_managers['sounds'].get_sounds(ent)
##def add_listener_sounds(ent):       Rogue.c_managers['sounds'].add_listener_sounds(ent)
##def remove_listener_sounds(ent):    Rogue.c_managers['sounds'].remove_listener_sounds(ent)
##def clear_listen_events_sounds(ent):Rogue.c_managers['sounds'].clear_sounds(ent)

def pc_listen_sights(): # these listener things for PC might need some serious work...
    pc=Rogue.pc
    lis=listen_sights(pc)
    if lis:
        for ev in lis:
            Rogue.c_managers['sights'].add(ev)
        manager_sights_run()
def pc_listen_sounds():
    pc=Rogue.pc
    lis=listen_sounds(pc)
    if lis:
        for ev in lis:
            Rogue.c_managers['sounds'].add(ev)
        manager_sounds_run()




    #----------------#
    #       FOV      #
    #----------------#

# TODO: test FOV for NPCs to make sure it works properly!!!
def getfovmap(mapID): return Rogue.map.fov_map# Rogue.fov_maps[mapID] #
def update_fov(ent):
    Rogue.c_managers['fov'].update(ent)
def run_fov_manager(ent):
    Rogue.c_managers['fov'].run(ent)
    
def _fov_init():  # normal type FOV map init -- just create the FOV map
    fovMap=libtcod.map_new(ROOMW,ROOMH)
    libtcod.map_copy(Rogue.map.fov_map,fovMap)  # get properties from Map
    return fovMap
def fov_init(ent):  # init fov for an entity
    if not Rogue.world.has_component(ent, cmp.SenseSight):
        return False
    compo=Rogue.world.component_for_entity(ent, cmp.SenseSight)
    compo.fovID=0 #_fov_init()
    return True
###@debug.printr
def fov_compute(ent):
##    print("computing fov for ent {}".format(ent))
    pos = Rogue.world.component_for_entity(ent, cmp.Position)
    senseSight = Rogue.world.component_for_entity(ent, cmp.SenseSight)
    sight = getms(ent, 'sight')
    getfovmap(senseSight.fovID).compute_fov(
        pos.x,pos.y, radius=sight, light_walls=True,
        algorithm=libtcod.FOV_RESTRICTIVE)
def update_fovmap_property(fovmap, x,y, value):
    libtcod.map_set_properties( fovmap, x,y,value,True)

# vision functions
def can_see(ent,x,y,sight=None): # circular FOV function
    run_fov_manager(ent) # compute entity's FOV if necessary
    world = Rogue.world
    light=get_perceived_light_value(x,y)
    if not on(ent,NVISION):
        light -= 3
    if light < 1:
        return False
##    if light >= BLINDING_LIGHT:
##        return False
    pos = world.component_for_entity(ent, cmp.Position)
    senseSight = world.component_for_entity(ent, cmp.SenseSight)
    if sight is None: sight=getms(ent, "sight")
    dist = int(maths.dist(pos.x,pos.y, x,y))
    if ( getfovmap(senseSight.fovID).fov[y][x] and dist <= sight ): # <- circle-ize
        globalreturn(dist,light)
        return True
    return False
#
def can_see_obj(ent, target,sight=None): # take heightmap into account
    h = HEIGHTMAP_GRADIENT * CM_PER_TILE
    world = Rogue.world
    
    # regular FOV algo
    if not can_see(ent,x,y,sight): # idea: instead of relying on this function,
        return False # implement whole FOV function using custom algos (no libtcod FOV)
    # (at least for exterior (outdoor) areas)
    #
    
    entpos = world.component_for_entity(ent, cmp.Position)
    targetpos = world.component_for_entity(target, cmp.Position)
    eyesh = (getms(ent, 'height') - 5) // h # - 5 is temporary; height of the viewer's eye-holes with respect to the ground
    targeth = (getms(target, 'height')*0.8333334) // h
    entz = tile_height(entpos.x, entpos.y) + eyesh
    targetz = tile_height(targetpos.x, targetpos.y) + targeth
    zz = targetz + targeth
    # cast thin-cover line to the target
    line = misc.Bresenham3D(
        entpos.x, entpos.y, entz + eyesh,
        targetpos.x, targetpos.y, zz
        )
    # look at heightmap for collisions
    for tile in line:
        x,y,z = tile
        if z < tile_height(x, y): # blocked by hill/cliff, etc.
            return False
    # end for
    return True # if we made it this far
#
#copies Map 's fov data to all creatures - only do this when needed
#   also flag all creatures for updating their fov maps
def update_all_fovmaps():
    for ent, compo in Rogue.world.get_component(cmp.SenseSight):
        update_fov(ent)
##        fovMap=compo.fov_map
##        libtcod.map_copy(Rogue.map.fov_map, fovMap)



    #----------------#
    #      Paths     #
    #----------------#

def can_hear(ent, x,y, volume):
    world = Rogue.world
    if ( on(ent,DEAD) or (not world.has_component(ent, cmp.SenseHearing)) ):
         return False
    pos = world.component_for_entity(ent, cmp.Position)
    senseHearing = world.component_for_entity(ent, cmp.SenseHearing)
    dist=maths.dist(pos.x, pos.y, x, y)
    maxHearDist = volume * senseHearing.hearing / AVG_HEARING
    if (pos.x == x and pos.y == y): return (0,0,maxHearDist,)
    if dist > maxHearDist: return False
    # calculate a path
    path=path_init_sound()
    path_compute(path, pos.x,pos.y, x,y)
    pathSize=libtcod.path_size(path)
    if dist >= 2:
        semifinal=libtcod.path_get(path, 0)
        xf,yf=semifinal
        dx=xf - pos.x
        dy=yf - pos.y
    else:
        dx=0
        dy=0
    path_destroy(path)
    loudness=(maxHearDist - pathSize - (pathSize - dist))
    if loudness > 0:
        return (dx,dy,loudness)

def path_init_movement():
    pathData=0
    return Rogue.map.path_new_movement(pathData)
def path_init_sound():
    pathData=0
    return Rogue.map.path_new_sound(pathData)
def path_compute(path, xfrom,yfrom, xto,yto):
    libtcod.path_compute(path, xfrom,yfrom, xto,yto)
def path_destroy(path):
    libtcod.path_delete(path)
def path_step(path):
    x,y=libtcod.path_walk(path, True)
    return x,y





    #----------------#
    #     Things     #
    #----------------#

def register_entity(ent): # NOTE!! this no longer adds to grid.
    create_moddedStats(ent) # is there a place this would belong better?
    make(ent,DIRTY_STATS)
def release_entity(ent):
    # do a bunch of precautionary stuff / remove entity from registers ...
    remove_listener_sights(ent) 
    remove_listener_sounds(ent)
    grid_remove(ent)
    # esper
    delete_entity(ent)
def delete_entity(ent):
    Rogue.world.delete_entity(ent)
def create_stuff(ID, x,y): # create & register an item from stuff list
    tt = entities.create_stuff(ID, x,y)
    register_entity(tt)
    return tt
def create_rawmat(ID, x,y): # create & register an item from raw materials
    tt = entities.create_rawmat(ID, x,y)
    register_entity(tt)
    return tt
def create_entity():
    return Rogue.world.create_entity()
##def create_entity_flagset(): # create an entity with a flagset
##    ent = Rogue.world.create_entity()
##    Rogue.world.add_component(ent, cmp.Flags) #flagset
##    return ent
def material_damage_threshold(mat):
    return MATERIALS[mat][1]

# harvesting
def breakitem(item, tool=None):
    ''' destroy an entity using tool; attempt to harvest it with tool
    '''
    harvest(item, tool, quality=0)
    kill(item)
def harvest(item, tool=None, quality=1):
    ''' attempt to harvest a Harvestable entity using tool
    Parameters:
        item:     the entity to harvest
        tool:     the entity that is being used to harvest the thing
        quality:  higher quality -> greater chance at successful harvest
    '''
    if Rogue.world.has_component(item, cmp.Harvestable):
        compo = Rogue.world.component_for_entity(item, cmp.Harvestable)
        return True
    return False



    #  creature/monsters  #

def create_monster(typ,x,y,col=None): #init from entities.py
    ''' create a monster from the bestiary and initialize it '''
    if monat(x,y):
        return None #tile is occupied by a creature already.
    if col:
        ent = entities.create_monster(typ,x,y,col)
    else:
        ent = entities.create_monster(typ,x,y)
    register_entity(ent)
    grid_insert(ent)
    givehp(ent)
    givemp(ent)
    fov_init(ent)
    update_fov(ent)
    return ent

def create_corpse(ent):
    corpse = entities.convertTo_corpse(ent)
##    register_entity(corpse)
    return corpse
def create_ashes(ent):
    ashes = entities.convertTo_ashes(ent)
##    register_entity(ashes)
    return ashes
def convert_to_creature(ent, job=None, faction=None, species=None):
    ''' try to give entity Creature component, return success '''
    pos = Rogue.world.component_for_entity(ent, cmp.Position)
    if monat(pos.x,pos.y):
        return False # already a creature in this spot.
    Rogue.world.add_component(ent, cmp.Creature(job, faction, species))
    return True

    

    #---------------#
    #   Inventory   #
    #---------------#

##def init_inventory(ent, capacity):
##    Rogue.world.add_component(ent, cmp.Inventory(capacity))



    #------------#
    #   Fluids   #
    #------------#

def create_fluid(name, x,y, volume):
    fluid = fluids.create_fluid(x,y,name,volume)
    register_fluid(fluid)

def port_fluid(fluid, xto, yto):
    grid_fluids_remove(fluid)
    pos = Rogue.world.component_for_entity(fluid, cmp.Position)
    pos.x = xto
    pos.y = yto
    grid_fluids_insert(fluid)
##def flow_fluid(fluid, xto, yto, amt): #fluids should be object instances?
##    grid_fluids_remove(fluid)
##    fluid.x=xto
##    fluid.y=yto
##    grid_fluids_insert(fluid)
    

def register_fluid(ent):
    grid_fluids_insert(ent)
##    list_add_fluid(ent)
def release_fluid(ent):
    grid_fluids_remove(ent)
##    list_remove_fluid(obj)
    
#fluid containers
def init_fluidContainer(ent, size):
    make(ent,HOLDSFLUID)
    Rogue.world.add_component(ent, cmp.FluidContainer(size))




    #---------#
    #   Body  #
    #---------#

def get_arm_length(bodyplan, height): #temporary solution to get arm length based on body type
    if bodyplan==BODYPLAN_HUMANOID:
        return around(height / 2.67)
def curebpp(bpp): #<flags> cure BPP status clear BPP status bpp_clear_status clear_bpp_status clear bpp status bpp clear status
    bpp.status = 0 # revert to normal status
def healbpp(bpp, bpptype, status): #<flags> heal BPP object
    pass #TODO
# damage body part piece (inflict status)
def damagebpp(bpp, bpptype, status): #<flags> damage BPP object inflict BPP status BPP set status set_bpp_status bpp_set_status bpp set status set bpp status
    '''
        * Try to inflict a status on a BPP (body part piece) object
            (A BPP is a sub-component of a BP (body part)
             such as a muscle, bone, etc.)
        * Possibly inflict a higher level status if the intended status
            and the current status are equal.
        * Do not overwrite higher-priority statuses (the higher the
            integer value of the status constant, the higher priority).
        
        # return whether the BPP was damaged
        # Parameters:
        #   bpp     : the BPP_ component to be damaged
        #   bpptype : BPP_ const
        #   status  : the status you want to set on the BPP --
        #               indicates the type of damage to be dealt
    '''
    # progressive damage:
    # two applications of same status => next status up in priority (if of the same type of damage)
    if bpptype == BPP_MUSCLE:
        if (status == MUSCLESTATUS_SORE and bpp.status == status ):
            bpp.status = MUSCLESTATUS_KNOTTED
            return True
        if (status == MUSCLESTATUS_KNOTTED and bpp.status == status ):
            bpp.status = MUSCLESTATUS_CONTUSION
            return True
        if (status == MUSCLESTATUS_CONTUSION and bpp.status == status ):
            bpp.status = MUSCLESTATUS_STRAINED
            return True
        if (status == MUSCLESTATUS_STRAINED and bpp.status == status ):
            bpp.status = MUSCLESTATUS_TORN
            return True
        if (status == MUSCLESTATUS_TORN and bpp.status == status ):
            bpp.status = MUSCLESTATUS_RIPPED
            return True
        if (status == MUSCLESTATUS_RIPPED and bpp.status == status ):
            bpp.status = MUSCLESTATUS_RUPTURED
            return True
        if (status == MUSCLESTATUS_RUPTURED and bpp.status == status ):
            bpp.status = MUSCLESTATUS_MANGLED
            return True
    elif bpptype == BPP_BONE:
        if (status == BONESTATUS_DAMAGED and bpp.status == status ):
            bpp.status = BONESTATUS_FRACTURED
            return True
        if (status == BONESTATUS_FRACTURED and bpp.status == status ):
            bpp.status = BONESTATUS_CRACKED
            return True
        if (status == BONESTATUS_CRACKED and bpp.status == status ):
            bpp.status = BONESTATUS_BROKEN
            return True
        if (status == BONESTATUS_BROKEN and bpp.status == status ):
            bpp.status = BONESTATUS_MULTIBREAKS
            return True
        if (status == BONESTATUS_MULTIBREAKS and bpp.status == status ):
            bpp.status = BONESTATUS_SHATTERED
            return True
        if (status == BONESTATUS_SHATTERED and bpp.status == status ):
            bpp.status = BONESTATUS_MUTILATED
            return True
    elif bpptype == BPP_SKIN:
        if (status == SKINSTATUS_RASH and bpp.status == status ):
            bpp.status = SKINSTATUS_BLISTER
            return True
        if (status == SKINSTATUS_BLISTER and bpp.status == status ):
            bpp.status = SKINSTATUS_SCRAPED
            return True
        if (status == SKINSTATUS_SCRAPED and bpp.status == status ):
            bpp.status = SKINSTATUS_MINORABRASION
            return True
        if (status == SKINSTATUS_MINORABRASION and bpp.status == status ):
            bpp.status = SKINSTATUS_MAJORABRASION
            return True
        if (status == SKINSTATUS_MAJORABRASION and bpp.status == status ):
            bpp.status = SKINSTATUS_SKINNED
            return True
        if (status == SKINSTATUS_SKINNED and bpp.status == status ):
            bpp.status = SKINSTATUS_FULLYSKINNED
            return True
        if (status == SKINSTATUS_FULLYSKINNED and bpp.status == status ):
            bpp.status = SKINSTATUS_MANGLED
            return True
        if (status == SKINSTATUS_BURNED and bpp.status == status ):
            bpp.status = SKINSTATUS_DEEPBURNED
            return True
        if (status == SKINSTATUS_DEEPBURNED and bpp.status == status ):
            bpp.status = SKINSTATUS_MANGLED
            return True
        if (status == SKINSTATUS_CUT and bpp.status == status ):
            bpp.status = SKINSTATUS_DEEPCUT
            return True
        if (status == SKINSTATUS_DEEPCUT and bpp.status == status ):
            bpp.status = SKINSTATUS_MULTIDEEPCUTS
            return True
        if (status == SKINSTATUS_MULTIDEEPCUTS and bpp.status == status ):
            bpp.status = SKINSTATUS_MANGLED
            return True
    
    # default
    if bpp.status >= status: 
        return False # don't overwrite lower priority statuses.
    # do exactly what the parameters intended
    bpp.status = status # just set the status
    return True
# end def

# damage body part (potentially call damagebpp multiple times)
def damagebp(bptarget, dmgtype, hitpp):
    '''
        bptarget   BP_ (Body Part) component object instance to damage
        dmgtype    DMGTYPE_ const
        hitpp      0 to 3: damage value -- how high of a priority of
                    status is inflicted? 3 is most severe, 0 least severe.
    '''
        
    # abrasions
    if dmgtype==DMGTYPE_ABRASION:
        cd=cmp.BP_BPPS[type(bptarget)]
        if BPP_SKIN in cd:
            damagebpp(
                bptarget.skin, BPP_SKIN, SKINSTATUSES_ABRASION[hitpp])
            # deep skin abrasions may result in muscle abrasion
            if ( BPP_MUSCLE in cd and
                 bptarget.skin.status >= SKINSTATUS_MAJORABRASION ):
                damagebpp(
                    bptarget.muscle, BPP_MUSCLE, MUSCLESTATUSES_ABRASION[hitpp])
    # burns
    elif dmgtype==DMGTYPE_BURN:
        cd=cmp.BP_BPPS[type(bptarget)]
        if BPP_SKIN in cd:
            damagebpp(
                bptarget.skin, BPP_SKIN, SKINSTATUSES_BURN[hitpp])
            # deep skin burns may result in muscle burns
            if ( BPP_MUSCLE in cd and
                 bptarget.skin.status >= SKINSTATUS_DEEPBURNED ):
                damagebpp(
                    bptarget.muscle, BPP_MUSCLE, MUSCLESTATUSES_BURN[hitpp])
    # lacerations
    elif dmgtype==DMGTYPE_CUT:
        cd=cmp.BP_BPPS[type(bptarget)]
        if BPP_SKIN in cd:
            damagebpp(
                bptarget.skin, BPP_SKIN, SKINSTATUSES_CUT[hitpp])
        if BPP_MUSCLE in cd:
            damagebpp(
                bptarget.muscle, BPP_MUSCLE, MUSCLESTATUSES_CUT[hitpp])
    # puncture wounds
    elif dmgtype==DMGTYPE_PIERCE:
        cd=cmp.BP_BPPS[type(bptarget)]
        if BPP_SKIN in cd:
            damagebpp(
                bptarget.skin, BPP_SKIN, SKINSTATUSES_PUNCTURE[hitpp])
        if BPP_MUSCLE in cd:

            damagebpp(
                bptarget.muscle, BPP_MUSCLE, MUSCLESTATUSES_PUNCTURE[hitpp])
        # organ damage is handled separately.
    # hacking / picking damage
    elif dmgtype==DMGTYPE_HACK:
        cd=cmp.BP_BPPS[type(bptarget)]
        if BPP_SKIN in cd:
            damagebpp(
                bptarget.skin, BPP_SKIN, SKINSTATUS_DEEPCUT)
        if BPP_MUSCLE in cd:
            damagebpp(
                bptarget.muscle, BPP_MUSCLE, MUSCLESTATUS_STRAINED)
        if BPP_BONE in cd:
            damagebpp(
                bptarget.bone, BPP_BONE, BONESTATUSES_BLUNT[hitpp])
    # blunt / crushing damage
    elif dmgtype==DMGTYPE_BLUNT:
        cd=cmp.BP_BPPS[type(bptarget)]
        if BPP_MUSCLE in cd:
            damagebpp(
                bptarget.muscle, BPP_MUSCLE, MUSCLESTATUSES_BLUNT[hitpp])
        if BPP_BONE in cd:
            damagebpp(
                bptarget.bone, BPP_BONE, BONESTATUSES_BLUNT[hitpp])
    # mace-like weapons
    elif dmgtype==DMGTYPE_SPUDS:            
        cd=cmp.BP_BPPS[type(bptarget)]
        if BPP_SKIN in cd:
            damagebpp(
                bptarget.skin, BPP_SKIN, SKINSTATUSES_SPUDS[hitpp])
        if BPP_MUSCLE in cd:
            damagebpp(
                bptarget.muscle, BPP_MUSCLE, MUSCLESTATUSES_BLUNT[hitpp])
        if BPP_BONE in cd:
            damagebpp(
                bptarget.bone, BPP_BONE, BONESTATUSES_BLUNT[hitpp])
    # morning-star like long-spiked weapons
    elif dmgtype==DMGTYPE_SPIKES:
        cd=cmp.BP_BPPS[type(bptarget)]
        if BPP_SKIN in cd:
            damagebpp(
                bptarget.skin, BPP_SKIN, SKINSTATUSES_SPIKES[hitpp])
        if BPP_MUSCLE in cd:
            damagebpp(
                bptarget.muscle, BPP_MUSCLE, MUSCLESTATUSES_BLUNT[hitpp])
        if BPP_BONE in cd:
            damagebpp(
                bptarget.bone, BPP_BONE, BONESTATUSES_BLUNT[hitpp])
# end def

def _get_eq_compo(ent, equipType): # equipType Const -> component
    compo = None
    
    # main hand
    if equipType==EQ_MAINHAND:
        compo = dominant_arm(ent).hand
    # main arm
    elif equipType==EQ_MAINARM:
        compo = dominant_arm(ent).arm
    # off hand
    elif equipType==EQ_OFFHAND:
        body = Rogue.world.component_for_entity(ent, cmp.Body)
        arm = body.parts[cmp.BPC_Arms].arms[1]
        if arm: compo = arm.hand
    # off arm
    elif equipType==EQ_OFFARM:
        body = Rogue.world.component_for_entity(ent, cmp.Body)
        arm = body.parts[cmp.BPC_Arms].arms[1]
        if arm: compo = arm.arm
    # main foot
    elif equipType==EQ_MAINFOOT:
        compo = dominant_leg(ent).foot
    # main leg
    elif equipType==EQ_MAINLEG:
        compo = dominant_leg(ent).leg
    # off foot
    elif equipType==EQ_OFFFOOT:
        body = Rogue.world.component_for_entity(ent, cmp.Body)
        leg = body.parts[cmp.BPC_Legs].legs[1]
        if leg: compo = leg.foot
    # off leg
    elif equipType==EQ_OFFLEG:
        body = Rogue.world.component_for_entity(ent, cmp.Body)
        leg = body.parts[cmp.BPC_Legs].legs[1]
        if leg: compo = leg.leg
    # head 1
    elif equipType==EQ_MAINHEAD:
        compo = dominant_head(ent).head
    # face 1
    elif equipType==EQ_MAINFACE:
        compo = dominant_head(ent).face
    # neck 1
    elif equipType==EQ_MAINNECK:
        compo = dominant_head(ent).neck
    # eyes 1
    elif equipType==EQ_MAINEYES:
        compo = dominant_head(ent).eyes
    # ears 1
    elif equipType==EQ_MAINEARS:
        compo = dominant_head(ent).ears
    # torso core
    elif equipType==EQ_CORE:
        compo = Rogue.world.component_for_entity(ent, cmp.Body).core.core
    # torso front chest
    elif equipType==EQ_FRONT:
        compo = Rogue.world.component_for_entity(ent, cmp.Body).core.front
    # torso back
    elif equipType==EQ_BACK:
        compo = Rogue.world.component_for_entity(ent, cmp.Body).core.back
    # torso hips
    elif equipType==EQ_HIPS:
        compo = Rogue.world.component_for_entity(ent, cmp.Body).core.hips
    return compo
#end def

# get body parts getbodyparts getbps findbodyparts find body parts
def findbps(ent, cls): # ent + cls -> list of BP component objects
    body = Rogue.world.component_for_entity(ent, cmp.Body)
    # TODO: body plans other than humanoid
##    if body.plan==BODYPLAN_HUMANOID:
    if cls is cmp.BP_TorsoCore:
        return (body.core.core,)
    if cls is cmp.BP_TorsoFront:
        return (body.core.front,)
    if cls is cmp.BP_TorsoBack:
        return (body.core.back,)
    if cls is cmp.BP_Hips:
        return (body.core.hips,)
    if cls is cmp.BP_Head:
        return (body.parts[cmp.BPC_Heads].heads[0].head,)
    if cls is cmp.BP_Face:
        return (body.parts[cmp.BPC_Heads].heads[0].face,)
    if cls is cmp.BP_Neck:
        return (body.parts[cmp.BPC_Heads].heads[0].neck,)
    if cls is cmp.BP_Eyes:
        return (body.parts[cmp.BPC_Heads].heads[0].eyes,)
    if cls is cmp.BP_Ears:
        return (body.parts[cmp.BPC_Heads].heads[0].ears,)
    if cls is cmp.BP_Nose:
        return (body.parts[cmp.BPC_Heads].heads[0].nose,)
    if cls is cmp.BP_Arm:
        return (body.parts[cmp.BPC_Arms].arms[0].arm,
                body.parts[cmp.BPC_Arms].arms[1].arm,)
    if cls is cmp.BP_Hand:
        return (body.parts[cmp.BPC_Arms].arms[0].hand,
                body.parts[cmp.BPC_Arms].arms[1].hand,)
    if cls is cmp.BP_Leg:
        return (body.parts[cmp.BPC_Legs].legs[0].leg,
                body.parts[cmp.BPC_Legs].legs[1].leg,)
    if cls is cmp.BP_Foot:
        return (body.parts[cmp.BPC_Legs].legs[0].foot,
                body.parts[cmp.BPC_Legs].legs[1].foot,)


    #-----------------#
    #    Equipment    #
    #-----------------#

def equip(ent,item,equipType): # equip an item in 'equipType' slot
    '''
        equip ent with item in the slot designated by equipType const
        (functions for held or worn items)
        return tuple: (result, compo,)
            where result is a negative value for failure, or 1 for success
            and compo is None or the item's equipable component if success
        
##                #TODO: add special effects; light, etc. How to??
            light: make the light a Child of the equipper
    '''
# init and failure checking #
    # first check that the entity can equip the item in the indicated slot.
    world = Rogue.world
    equipableConst = EQUIPABLE_CONSTS[equipType]
    eqcompo = _get_eq_compo(ent, equipType)
    holdtype=(equipType in cmp.EQ_BPS_HOLD) # holding type or armor type?
    if not world.has_component(item, equipableConst):
        return (-1,None,) # item can't be equipped in this slot
    if not eqcompo: # component selected. Does this component exist?
        return (-2,None,) # something weird happened
    if ( not holdtype and eqcompo.covered ):
        return (-3,None,) # already have something covering that slot
    if ( holdtype and eqcompo.holding ):
        return (-4,None,) # reject held item if already holding something
    if ( equipType==EQ_OFFHAND and on(item, TWOHANDS)):
        return (-5,None,) # reject 2-h weapons not equipped in mainhand.
    equipable = world.component_for_entity(item, equipableConst)
    
    # ensure body type indicates presence of this body part
    # (TODO)
##    if EQTYPES_TO_BODYPARTS[equipType] in BODYPLAN_BPS[body.plan]:
##        ...

    # coverage #
    
    # figure out what additional slots the equipment covers, if any
    def __cov(ent, clis, flis, eqtype, cls): # cover additional body part
        for _com in findbps(ent, cls): # temporary
            if _com.covered: # make sure you can't equip something if ...
                flis.append(_com) # ... any required slots are occupied.
            else:
                clis.append(_com)
    # end def
    clis = [] # success list - covered
    flis = [] # failure list
    
    # two hands
    # TODO : change logic so that you CAN wield 2-h weapon in 1-h
    # it's just that you get a big penalty for doing so.
##    if ( equipType==EQ_MAINHAND and on(item, TWOHANDS) ):
##        __cov(ent,clis,hlis,flis,equipType,cmp.BP_Hand) # Fixme: this covers ALL hands. 
    if equipType==EQ_FRONT:
        if equipable.coversBack: __cov(ent,clis,flis,equipType,cmp.BP_TorsoBack)
        if equipable.coversCore: __cov(ent,clis,flis,equipType,cmp.BP_TorsoCore)
        if equipable.coversHips: __cov(ent,clis,flis,equipType,cmp.BP_Hips)
    if equipType==EQ_MAINHEAD:
        if equipable.coversFace: __cov(ent,clis,flis,equipType,cmp.BP_Face)
        if equipable.coversNeck: __cov(ent,clis,flis,equipType,cmp.BP_Neck)
        if equipable.coversEyes: __cov(ent,clis,flis,equipType,cmp.BP_Eyes)
        if equipable.coversEars: __cov(ent,clis,flis,equipType,cmp.BP_Ears)
    if flis:
        return (-10, flis,) # failed to equip because the BPs in flis are already covered.
# /init #
    
        #-------------------------#
        # success! Equip the item #
        #-------------------------#
    
    # remove item from the map
    grid_remove(item)
    # indicate that the item is equipped using components
    world.add_component(item, cmp.Child(ent))
    world.add_component(item, cmp.Equipped(ent, equipType))
    
    # put it in the right slot (held or worn?)
    if holdtype: # held
        eqcompo.held.item = item
        eqcompo.holding = True # cover this BP
    else: # worn
        eqcompo.slot.item = item 
        eqcompo.covered = True # cover this BP

    if ( (equipType==EQ_MAINLEG or equipType==EQ_OFFLEG)
         and equipable.coversBoth
        ):
        # for now just cover all legs (TEMPORARY OBV.)
        for leg in findbps(ent, cmp.BP_Leg):
            clis.append(leg)
    
    # cover
    eqcompo.slot.covers = tuple(clis)
    # cover the BPs
    for _com in clis:
        _com.covered=True
    #
    
    make(ent, DIRTY_STATS)
    return (1,eqcompo,) # yey success
    
# end def

def deequip_all(ent): # TODO: test this (and thus all deequip funcs)
    body = Rogue.world.component_for_entity(ent, cmp.Body)
    
    # core
    if body.plan==BODYPLAN_HUMANOID:
        _deequipSlot(ent, body.slot)
        deequip(ent, EQ_FRONT)
        deequip(ent, EQ_BACK)
        deequip(ent, EQ_HIPS)
        deequip(ent, EQ_CORE)
    else:
        raise Exception # TODO: differentiate with different body types
    # parts
    for cls, part in body.parts.items():
        if type(part)==cmp.BPC_Arms:
            for arm in part.arms:
                _dewield(ent, arm.hand)
                _deequip(ent, arm.hand)
                _deequip(ent, arm.arm)
        elif type(part)==cmp.BPC_Legs:
            for leg in part.legs:
                _deequip(ent, leg.foot)
                _deequip(ent, leg.leg)
        elif type(part)==cmp.BPC_Heads:
            for head in part.heads:
                _deequip(ent, head.head)
                _deequip(ent, head.face)
                _deequip(ent, head.neck)
                _deequip(ent, head.eyes)
                _deequip(ent, head.ears)
    # end for
# end def
def deequip(ent,equipType):
    ''' remove worn equipment from slot 'equipType' (not held)
        return the item that was equipped there
            or None if failed to un-equip
    '''
    compo = _get_eq_compo(ent, equipType)
    if not compo:
        return None

    return _deequip(ent, compo)
# end def
def _deequip(ent, compo):
    ''' unequip the worn item in the component's wear slot (not held)
        consider coverage of other slots that may be affected
    '''
    # uncover the covered slot(s)
    for compo in compo.slot.covers:
        compo.covered = False
    compo.slot.covers = ()
    
    return _deequipSlot(ent, compo.slot)
# end def
def _deequipSlot(ent, slot):
    ''' unequip the worn item from equip slot slot (not held)
        unconcerned with coverage of other slots
    '''
    world=Rogue.world
    item = slot.item
    if not item: #nothing equipped here
        return None
    
    world.remove_component(item, cmp.Child)
    world.remove_component(item, cmp.Equipped)
    slot.item = None
    slot.covered = False
             
    make(ent, DIRTY_STATS)
    return item
# end def

def dewield(ent,equipType): # for held items only (not worn)
    compo = _get_eq_compo(ent, equipType)
    if not compo:
        return None
    return _dewield(ent, compo)
# end def
def _dewield(ent, compo):
    world=Rogue.world
    item = compo.held.item
    if not item: #nothing equipped here
        return None
    
    world.remove_component(item, cmp.Child)
    world.remove_component(item, cmp.Equipped)
    compo.held.item = None
    
    make(ent, DIRTY_STATS)
    return item
# end def

##    equipableConst = EQUIPABLE_CONSTS[equipType]
##    #TODO: remove any special effects; light, etc.
##    world.remove_component(item, cmp.Equipped)
##    effect_remove(slot.modID)
##    slot.modID = None

##    #put item back in the world # THIS SHOULD BE DONE BY ANOTHER FUNCTION
##    pos = world.component_for_entity(ent, cmp.Position)
##    world.add_component(item, cmp.Position(pos.x,pos.y))

# build equipment and place in the world
def _initThing(ent):
    register_entity(ent)
    grid_insert(ent)
    givehp(ent) #give random quality based on dlvl?
def create_weapon(name,x,y): #,quality=1
    ent=entities.create_weapon(name,x,y)
    _initThing(ent)
    return ent
def create_armor(name,x,y):
    ent=entities.create_armor(name,x,y)
    _initThing(ent)
    return ent
def create_legwear(name,x,y):
    ent=entities.create_legwear(name,x,y)
    _initThing(ent)
    return ent
def create_armwear(name,x,y):
    ent=entities.create_armwear(name,x,y)
    _initThing(ent)
    return ent
def create_footwear(name,x,y):
    ent=entities.create_footwear(name,x,y)
    _initThing(ent)
    return ent
def create_headwear(name,x,y):
    ent=entities.create_headwear(name,x,y)
    _initThing(ent)
    return ent
def create_neckwear(name,x,y):
    ent=entities.create_neckwear(name,x,y)
    _initThing(ent)
    return ent
def create_facewear(name,x,y):
    ent=entities.create_facewear(name,x,y)
    _initThing(ent)
    return ent
def create_eyewear(name,x,y):
    ent=entities.create_eyewear(name,x,y)
    _initThing(ent)
    return ent
def create_earwear(name,x,y):
    ent=entities.create_earwear(name,x,y)
    _initThing(ent)
    return ent

def create_body_humanoid(mass=70, height=175, female=False, bodyfat=None):
    if bodyfat:
        return entities.create_body_humanoid(
            mass=mass, height=height, female=female, bodyfat=bodyfat)
    else:
        return entities.create_body_humanoid(
            mass=mass, height=height, female=female)

def dominant_arm(ent): # get a BPM object (assumes you have the necessary components / parts)
    body = Rogue.world.component_for_entity(ent, cmp.Body)
    bpc = body.parts[cmp.BPC_Arms]
    return bpc.arms[0] # dominant is always in slot 0 as a rule
def dominant_leg(ent): # get a BPM object
    body = Rogue.world.component_for_entity(ent, cmp.Body)
    bpc = body.parts[cmp.BPC_Legs]
    return bpc.legs[0] # dominant is always in slot 0 as a rule
def dominant_head(ent): # get a BPM object
    body = Rogue.world.component_for_entity(ent, cmp.Body)
    bpc = body.parts[cmp.BPC_Heads]
    return bpc.heads[0] # dominant is always in slot 0 as a rule
def off_arm(ent): # get a BPM object (assumes you have the necessary components / parts)
    body = Rogue.world.component_for_entity(ent, cmp.Body)
    bpc = body.parts[cmp.BPC_Arms]
    return bpc.arms[1] # temporary
def off_leg(ent): # get a BPM object
    body = Rogue.world.component_for_entity(ent, cmp.Body)
    bpc = body.parts[cmp.BPC_Legs]
    return bpc.legs[1] # temporary

def homeostasis(ent): entities.homeostasis(ent)
def metabolism(ent, hunger, thirst=1): entities.metabolism(ent, hunger, thirst) # metabolize
def stomach(ent): entities.stomach(ent)
def starve(ent): entities.starve(ent)
def dehydrate(ent): entities.dehydrate(ent)
        

    #--------------#
    #     Stats    #
    #--------------#

def get_encumberance_breakpoint(enc, encmax):
    erat = enc/max(1,encmax) # encumberance ratio
    if erat < ENC_BP_1:   # 0: < 25%
        encbp = 0
    elif erat < ENC_BP_2:    # 1: 25 <= x < 50%
        encbp = 1
    elif erat < ENC_BP_3:   # 2: 50 <= x < 75%
        encbp = 2
    elif erat < ENC_BP_4:   # 3: 75 <= x < 85%
        encbp = 3
    elif erat < ENC_BP_5:   # 4: 85 <= x < 90%
        encbp = 4
    elif erat < ENC_BP_6:   # 5: 90 <= x < 95%
        encbp = 5
    elif erat < 1:      # 6: 95 <= x < 100%
        encbp = 6
    else:               # 7: 100% or greater
        encbp = 7
    return encbp

def _update_stats(ent): # PRIVATE, ONLY TO BE CALLED FROM getms(...)
    '''
        calculate modified stats
            building up from scratch (base stats)
            add any modifiers from equipment, status effects, etc.
        return the Modified Stats component
        after this is called, you can access the Modified Stats component
            and it will contain the right value, until something significant
            updates which would change the calculation, at which point the
            DIRTY_STATS flag for that entity must be set to True.
        NOTE: should not call this directly nor access modified stats
            component directly. Use the public interface "getms"
    '''
    # NOTE: apply all penalties (w/ limits, if applicable) AFTER bonuses.
        # this is to ensure you don't end up with MORE during a
        #   penalty application; as in the case the value was negative
    
# init #----------------------------------------------------------------#
    offhandItem = False
    bpdata=[]
    world=Rogue.world
    base=world.component_for_entity(ent, cmp.Stats)
    modded=world.component_for_entity(ent, cmp.ModdedStats)

    # skills
    if world.has_component(ent, cmp.Skills):
        skills = world.component_for_entity(ent, cmp.Skills)
        athlete = _getskill(skills.skills.get(SKL_ATHLETE,0)) # athletic skill Lv
        armorSkill = _getskill(skills.skills.get(SKL_ARMOR,0)) # armored skill value
        unarmored = _getskill(skills.skills.get(SKL_UNARMORED,0)) # unarmored skill
    else:
        skills=None
        athlete = 0
        armorSkill = 0
        unarmored = 0

    # RESET all modded stats to their base
    for k,v in base.__dict__.items():
        modded.__dict__[k] = v

    # init pseudo-stats (stats which have no base value)
    modded.tatk=modded.tdmg=modded.tpen=modded.tasp=modded.trng=0
    modded.ratk=modded.rdmg=modded.rpen=modded.rasp=modded.minrng=modded.maxrng=0
    
    # useful stats to keep track of
    basemass = base.mass / MULT_MASS
# /init #--------------------------------------------------------------#


#~~~~~~~#-------------------------#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
        # Get Body Data / Equips  #
        #  - Do not apply yet. -  #
        #-------------------------#
    
    if world.has_component(ent, cmp.Body):
        body=world.component_for_entity(ent, cmp.Body)
    else:
        body=None
    if body:
        keys = body.parts.keys()
        
        # body component top level vars
        bodymass = entities._update_from_body_class(body, modded)
        basemass = (base.mass + bodymass) / MULT_MASS
        # encumerance from your own body weight
        modded.enc += modded.mass//MULT_MASS
        
        # core
        if body.plan==BODYPLAN_HUMANOID:
            entities._update_from_bpc_torso(
                bpdata,
                ent, body.core,
                armorSkill, unarmored
                )
        
        # parts
        if cmp.BPC_Heads in keys:
            entities._update_from_bpc_heads(
                bpdata,
                ent, body.parts[cmp.BPC_Heads],
                armorSkill, unarmored
                )
        if cmp.BPC_Arms in keys:
            entities._update_from_bpc_arms(
                bpdata,
                ent, body.parts[cmp.BPC_Arms],
                armorSkill, unarmored
                )
        if cmp.BPC_Legs in keys:
            entities._update_from_bpc_legs(
                bpdata,
                ent, body.parts[cmp.BPC_Legs],
                armorSkill, unarmored
                )
        if cmp.BPC_Pseudopods in keys:
            entities._update_from_bpc_pseudopods(
                bpdata,
                ent, body.parts[cmp.BPC_Pseudopods],
                armorSkill, unarmored
                )
        if cmp.BPC_Wings in keys:
            entities._update_from_bpc_wings(
                bpdata,
                ent, body.parts[cmp.BPC_Wings],
                armorSkill, unarmored
                )
        if cmp.BPC_Tails in keys:
            entities._update_from_bpc_tails(
                bpdata,
                ent, body.parts[cmp.BPC_Tails],
                armorSkill, unarmored
                )
    # end if
            
            
#~~~~~~~#------------#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
        #   skills   #
        #------------#

    if athlete:
        modded.msp = modded.msp + athlete*SKL_ATHLETE_MSP*SKILL_EFFECTIVENESS_MULTIPLIER

            
#~~~~~~~#------------#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
        # inventory  #
        #------------#

    # add encumberance from all items in inventory
    if world.has_component(ent, cmp.Inventory): # TODO: test this
        inv=world.component_for_entity(ent, cmp.Inventory).data
        for item in inv:
            enc=world.component_for_entity(item, cmp.Encumberance).value
            mass = getms(item, 'mass')
            modded.enc += enc * (mass / MULT_MASS)
            modded.mass += mass
            
#~~~~~~~#--------#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
        # meters #
        #--------#
    
    if world.has_component(ent, cmp.Meters):
        meters=world.component_for_entity(ent, cmp.Meters)

        # Statuses
        
        # all statuses set here must also be unset here
        # all statuses set here must have timer == -1 (don't auto-expire)
        
        # temperature
##        if meters.temp > bodytemp

        # pain
        if not on(ent, IMMUNEPAIN):
            q=0
            for _q, dec in PAIN_QUALITIES.items():
                if meters.pain >= MAX_PAIN*dec:
                    q=_q
            if q:
                status=get_status(ent, cmp.StatusPain)
                if (status and status.quality != q):
                    clear_status(ent, cmp.StatusPain)
                set_status(ent, cmp.StatusPain, t=-1, q=q)
            else:
                clear_status(ent, cmp.StatusPain)
        
        # bleed
        if not on(ent, IMMUNEBLEED):
            q = meters.bleed // (0.5*basemass)
            if q:
                status=get_status(ent, cmp.StatusBleed)
                if (status and status.quality != q):
                    clear_status(ent, cmp.StatusBleed)
                set_status(ent, cmp.StatusBleed, t=-1, q=q)
            else:
                clear_status(ent, cmp.StatusBleed)
        
        # dirty
        q=0
        for _q, dec in DIRT_QUALITIES.items():
            if meters.dirt >= MAX_DIRT*dec:
                q=_q
        if q:
            status=get_status(ent, cmp.StatusDirty)
            if (status and status.quality != q):
                clear_status(ent, cmp.StatusDirty)
            set_status(ent, cmp.StatusDirty, t=-1, q=q)
        else:
            clear_status(ent, cmp.StatusDirty)
        
        # wet
        if not on(ent, IMMUNEWATER):
            q = meters.wet // (MULT_MASS//100) # every 10g (is this too many g?)
            if q:
                status=get_status(ent, cmp.StatusWet)
                if (status and status.quality != q):
                    clear_status(ent, cmp.StatusWet)
                set_status(ent, cmp.StatusWet, t=-1, q=q)
            else:
                clear_status(ent, cmp.StatusWet)
        
        # rust
            # TODO: rust status affecting stats
        q=0
        for _q, dec in RUST_QUALITIES.items():
            if meters.rust >= MAX_RUST*dec:
                q=_q
        if q:
            status=get_status(ent, cmp.StatusRusted)
            if (status and status.quality != q):
                clear_status(ent, cmp.StatusRusted)
            set_status(ent, cmp.StatusRusted, t=-1, q=q)
        else:
            clear_status(ent, cmp.StatusRusted)
        
        # rot
            # TODO: rot status affecting stats
        q=0
        for _q, dec in ROT_QUALITIES.items():
            if meters.rot >= MAX_ROT*dec:
                q=_q
        if q:
            status=get_status(ent, cmp.StatusRotted)
            if (status and status.quality != q):
                clear_status(ent, cmp.StatusRotted)
            set_status(ent, cmp.StatusRotted, t=-1, q=q)
        else:
            clear_status(ent, cmp.StatusRotted)
        
    
#~~~~~~~#------------~~~~~~~~~~~~~~~~~~~~~#~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
        # statuses that affect attributes #
        #---------------------------------#
        
    # pain
    if world.has_component(ent, cmp.StatusPain):
        # TODO
        if q==1:
            modded.str = min(modded.str, modded.str * PAIN_STRMOD)
            modded.end = min(modded.end, modded.end * PAIN_ENDMOD)
            modded.con = min(modded.con, modded.con * PAIN_CONMOD)
        elif q==2:
            modded.str = min(modded.str, modded.str * AGONY_STRMOD)
            modded.end = min(modded.end, modded.end * AGONY_ENDMOD)
            modded.con = min(modded.con, modded.con * AGONY_CONMOD)
        elif q==3:
            modded.str = min(modded.str, modded.str * EXCRU_STRMOD)
            modded.end = min(modded.end, modded.end * EXCRU_ENDMOD)
            modded.con = min(modded.con, modded.con * EXCRU_CONMOD)
            
    # sick
    if world.has_component(ent, cmp.StatusSick):
        modded.str = min(modded.str, modded.str * SICK_STRMOD)
        modded.end = min(modded.end, modded.end * SICK_ENDMOD)
        modded.con = min(modded.con, modded.con * SICK_CONMOD) 

    # frozen
    if world.has_component(ent, cmp.StatusFrozen):
        modded.int = min(modded.int, modded.int * FROZEN_INTMOD)
    # cold
    elif world.has_component(ent, cmp.StatusCold):
        modded.int = min(modded.int, modded.int * COLD_INTMOD)
    # chilly
    elif world.has_component(ent, cmp.StatusChilly):
        modded.int = min(modded.int, modded.int * CHILLY_INTMOD)

    # hazy
    if world.has_component(ent, cmp.StatusHazy):
        modded.int = min(modded.int, modded.int * HAZY_INTMOD)
        
    # hungry
    if world.has_component(ent, cmp.StatusHungry):
        modded.con = min(modded.con, modded.con * HUNGRY_CONMOD)
        modded.end = min(modded.end, modded.end * HUNGRY_ENDMOD)
    # Emaciated
    elif world.has_component(ent, cmp.StatusEmaciated):
        modded.con = min(modded.con, modded.con * EMACI_CONMOD)
        modded.end = min(modded.end, modded.end * EMACI_ENDMOD)
    # tired
    if world.has_component(ent, cmp.StatusTired):
        modded.int = min(modded.int, modded.int * TIRED_INTMOD)
        
    # crouched
    if world.has_component(ent, cmp.StatusBPos_Crouched):
        modded.agi = modded.agi * CROUCHED_AGIMOD
    # seated
    if world.has_component(ent, cmp.StatusBPos_Seated):
        modded.agi = modded.agi * SEATED_AGIMOD
    # supine
    if world.has_component(ent, cmp.StatusBPos_Supine):
        modded.agi = modded.agi * SUPINE_AGIMOD
    # prone
    if world.has_component(ent, cmp.StatusBPos_Prone):
        modded.agi = modded.agi * PRONE_AGIMOD
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#&&&&''''^^^^````....,,,,----OOOO&&&&''''^^^^````....,,,,----OOOO&&&&''#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#                                                                      #
# *** NOTE: ABSOLUTELY NOTHING BELOW HERE THAT MODIFIES ATTRIBUTES *** #
#                                                                      #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#&&&&''''^^^^````....,,,,----OOOO&&&&''''^^^^````....,,,,----OOOO&&&&''#
#~~~~~~~#------------#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
        # attributes #
        #------------#
        # Apply derived stat bonuses from attributes.
        # These are NOT multiplier modifiers; just add to stats.
    
    # Strength
    _str = modded.str//MULT_ATT
    if _str > 0: # negative attributes do not drain stats.
        modded.atk += _str * ATT_STR_ATK*MULT_STATS
        modded.dmg += _str * ATT_STR_DMG*MULT_STATS
        modded.arm += _str * ATT_STR_AV*MULT_STATS
        modded.gra += _str * ATT_STR_GRA*MULT_STATS
        modded.encmax += _str * ATT_STR_ENCMAX
        modded.idn += _str * ATT_STR_SCARY
        modded.trng += _str * ATT_STR_TRNG
    
    # Agility
    _agi = modded.agi//MULT_ATT
    if _agi > 0:
        modded.dfn += _agi * ATT_AGI_DV*MULT_STATS
        modded.pro += _agi * ATT_AGI_PRO*MULT_STATS
        modded.bal += _agi * ATT_AGI_BAL*MULT_STATS
        modded.msp += _agi * ATT_AGI_MSP
        modded.asp += _agi * ATT_AGI_ASP
    
    # Dexterity
    _dex = modded.dex//MULT_ATT
    if _dex > 0:
        modded.pen += _dex * ATT_DEX_PEN*MULT_STATS
        modded.atk += _dex * ATT_DEX_ATK*MULT_STATS
        modded.asp += _dex * ATT_DEX_ASP
        modded.rpen += _dex * ATT_DEX_RPEN*MULT_STATS
        modded.ratk += _dex * ATT_DEX_RATK*MULT_STATS
        modded.rasp += _dex * ATT_DEX_RASP
##        modded.maxrng += _dex * ATT_DEX_RNG
        modded.trng += _dex * ATT_DEX_TRNG
    # TODO: context-sensitive dex bonuses (crafting, any tasks with hands...) (Not in this function of course!!!!)
    
    # Endurance
    _end = modded.end//MULT_ATT
    if _end > 0:
        modded.hpmax += _end * ATT_END_HP
        modded.mpmax += _end * ATT_END_SP
        modded.mpregen += _end * ATT_END_SPREGEN*MULT_STATS
        modded.resfire += _end * ATT_END_RESHEAT
        modded.rescold += _end * ATT_END_RESCOLD
        modded.resphys += _end * ATT_END_RESPHYS
        modded.respain += _end * ATT_END_RESPAIN
        modded.resbio += _end * ATT_END_RESBIO
        modded.resbleed += _end * ATT_END_RESBLEED
    
    # Intelligence
    _int = modded.int//MULT_ATT
    if _int > 0:
        pass
    
    # Constitution
    _con = modded.con//MULT_ATT
    if _con > 0:
        modded.arm += _con * ATT_CON_AV*MULT_STATS
        modded.hpmax += _con * ATT_CON_HP
        modded.encmax += _con * ATT_CON_ENCMAX
        modded.reselec += _con * ATT_CON_RESELEC
        modded.resbleed += _con * ATT_CON_RESBLEED
        modded.respain += _con * ATT_CON_RESPAIN
        modded.resbio += _con * ATT_CON_RESBIO

    
#~~~~~~~~~~~#------------------------#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
            #   Equipment Add Mods   #
            #------------------------#
            # ** After Attributes have been calculated.
            # (b/c strReq/dexReq)
    
    # apply mods -- addMods
    for bps in bpdata:
        for k,v in bps.addMods.items():
            modded.__dict__[k] = v + modded.__dict__[k]
        if bps.equip:
            for k,v in bps.equip.addMods.items():
                modded.__dict__[k] = v + modded.__dict__[k]
            # Strength Requirement and penalties | insufficient strength penalty
            strd = bps.equip.strReq - modded.str//MULT_STATS
            if strd > 0:
                # Multiply gear's enc. by ratio based on missing STR
                modded.enc += bps.equip.enc * strd * 0.1
                modded.dfn -= strd*INSUFF_STR_DFN_PENALTY*MULT_STATS
                # for held items only, reduce offensive stats
                if (bps.equip.bptype in cmp.BP_BPS_HOLD):
                    modded.atk -= strd*INSUFF_STR_ATK_PENALTY*MULT_STATS
                    modded.pen -= strd*INSUFF_STR_PEN_PENALTY*MULT_STATS
                    modded.gra -= strd*INSUFF_STR_GRA_PENALTY*MULT_STATS
                    modded.asp -= strd*INSUFF_STR_ASP_PENALTY
            # Dexterity Requirement and penalties | insufficient dexterity penalty
            dexd = bps.equip.dexReq - modded.dex//MULT_STATS
            if dexd > 0:
                modded.dfn -= dexd*INSUFF_DEX_DFN_PENALTY*MULT_STATS
                # for held items only, reduce offensive stats
                if (bps.equip.bptype in cmp.BP_BPS_HOLD):
                    modded.atk -= dexd*INSUFF_DEX_ATK_PENALTY*MULT_STATS
                    modded.pen -= dexd*INSUFF_DEX_PEN_PENALTY*MULT_STATS
                    modded.gra -= dexd*INSUFF_DEX_GRA_PENALTY*MULT_STATS
                    modded.asp -= dexd*INSUFF_DEX_ASP_PENALTY
            #
    # end for
    
#~~~#---------------------------------------------------------------#~~~#
    #       FINAL        MULTIPLIERS       BEGIN       HERE         #
#~~~#---------------------------------------------------------------#~~~#
    
    #------------------------------------------------#
    #   Statuses that affect (non-attribute) stats   #
    #------------------------------------------------#
    
    # sick
    if world.has_component(ent, cmp.StatusSick):
        modded.respain = modded.respain + SICK_RESPAINMOD  
    
    # hot
    if world.has_component(ent, cmp.StatusHot):
        modded.mpregen  = modded.mpregen * HOT_SPREGENMOD
    
    # frozen
    if world.has_component(ent, cmp.StatusFrozen):
        modded.spd      = modded.spd        * FROZEN_SPDMOD
        modded.mpregen  = modded.mpregen    * FROZEN_SPREGENMOD
        modded.mp       = modded.mp         * FROZEN_STAMMOD
    # cold
    elif world.has_component(ent, cmp.StatusCold):
        modded.spd      = modded.spd        * COLD_SPDMOD
        modded.mpregen  = modded.mpregen    * COLD_SPREGENMOD
        modded.mpmax    = modded.mpmax      * COLD_STAMMOD
    # chilly
    elif world.has_component(ent, cmp.StatusChilly):
        modded.spd      = modded.spd        * CHILLY_SPDMOD
        modded.mpregen  = modded.mpregen    * CHILLY_SPREGENMOD
        modded.mpmax    = modded.mpmax      * CHILLY_STAMMOD
    
    # Disoriented
    if world.has_component(ent, cmp.StatusDisoriented):
        modded.sight    = modded.sight      * DISOR_SIGHTMOD
        modded.hearing  = modded.hearing    * DISOR_HEARINGMOD
    # hazy
    if world.has_component(ent, cmp.StatusHazy):
        modded.respain  = modded.respain    * HAZY_RESPAIN
        modded.hearing  = modded.hearing    * HAZY_SPREGENMOD
        modded.sight    = modded.sight      * HAZY_SIGHTMOD
    
    # irritated
    if world.has_component(ent, cmp.StatusIrritated):
        modded.sight    = modded.sight      * IRRIT_SIGHTMOD
        modded.hearing  = modded.hearing    * IRRIT_HEARINGMOD
        modded.respain  = modded.respain    + IRRIT_RESPAIN
        modded.resbleed = modded.resbleed   + IRRIT_RESBLEED
        modded.atk      = modded.atk        + IRRIT_ATK*MULT_STATS
        modded.dfn      = modded.dfn        + IRRIT_DFN*MULT_STATS
    # cough
    if world.has_component(ent, cmp.StatusCough):
        modded.atk = modded.atk + COUGH_ATK*MULT_STATS
        modded.dfn = modded.dfn + COUGH_DFN*MULT_STATS
        
    # paralyzed
    if world.has_component(ent, cmp.StatusParalyzed):
        modded.spd = modded.spd * PARAL_SPDMOD
        modded.atk = modded.atk + PARAL_ATK*MULT_STATS
        modded.dfn = modded.dfn + PARAL_DFN*MULT_STATS
        
    # slow
    if world.has_component(ent, cmp.StatusSlow):
        modded.spd = modded.spd * SLOW_SPDMOD 
    # haste
    if world.has_component(ent, cmp.StatusHaste):
        modded.spd = modded.spd * HASTE_SPDMOD
        
    # jog
    if world.has_component(ent, cmp.StatusJog):
        modded.msp = modded.msp * JOG_MSPMOD
    # run
    if world.has_component(ent, cmp.StatusRun):
        modded.msp = modded.msp * RUN_MSPMOD
    # sprint
    if world.has_component(ent, cmp.StatusSprint):
        modded.msp = modded.msp * SPRINT_MSPMOD
        
    # hungry
    if world.has_component(ent, cmp.StatusHungry):
        modded.mpregen = modded.mpregen * HUNGRY_SPREGENMOD
    # emaciated
    elif world.has_component(ent, cmp.StatusEmaciated):
        modded.mpregen = modded.mpregen * EMACI_SPREGENMOD
    # dehydrated
    if world.has_component(ent, cmp.StatusDehydrated):
        modded.resfire = modded.resfire + DEHYD_RESFIRE
        modded.respain = modded.respain + DEHYD_RESPAIN
        modded.mpregen = modded.mpregen * DEHYD_SPREGENMOD
    # tired
    if world.has_component(ent, cmp.StatusTired):
        modded.sight = modded.sight * TIRED_SIGHTMOD
        modded.mpregen = modded.mpregen * TIRED_SPREGENMOD
    # Full
    if world.has_component(ent, cmp.StatusFull):
        modded.mpregen = modded.mpregen * FULL_SPREGENMOD
    
#---# quality statuses #--------------------------------------------#
    # have variable magnitude
        
    # recoil
    if world.has_component(ent, cmp.StatusRecoil):
        status=world.component_for_entity(ent, cmp.StatusRecoil)
        modded.ratk = modded.ratk - status.quality*MULT_STATS
        # TODO: while recoiling, all actions except shooting again ...
        # ... cost extra AP to perform.
    # blinded
    if world.has_component(ent, cmp.StatusBlinded):
        status=world.component_for_entity(ent, cmp.StatusBlinded)
        modded.sight = around(modded.sight * status.quality / 100)
    # deafened
    if world.has_component(ent, cmp.StatusDeafened):
        status=world.component_for_entity(ent, cmp.StatusDeafened)
        modded.hearing = around(modded.hearing * status.quality / 100)
    # drunk
    if world.has_component(ent, cmp.StatusDrunk):
        compo = world.component_for_entity(ent, cmp.StatusDrunk)
        modded.int = modded.int - compo.quality*DRUNK_INT*MULT_STATS
        modded.bal = modded.bal - compo.quality*DRUNK_BAL*MULT_STATS
    # off-balance staggered
    if world.has_component(ent, cmp.StatusOffBalance):
        compo = world.component_for_entity(ent, cmp.StatusOffBalance)
        modded.bal = modded.bal - compo.quality*MULT_STATS
    
    # wet
    if world.has_component(ent, cmp.StatusWet):
        q=world.component_for_entity(ent, cmp.StatusWet).quality
        modded.resfire += q
        modded.rescold -= q
        modded.reselec -= q
        modded.resdirt -= q
        modded.resbio -= q
    
#---# body positions #-----------------------------------------------#
    
    # crouched
    if world.has_component(ent, cmp.StatusBPos_Crouched):
##        modded.height = modded.height * CROUCHED_HEIGHTMOD
        modded.msp = modded.msp * CROUCHED_MSPMOD
        modded.atk = modded.atk + CROUCHED_ATK*MULT_STATS
        modded.dfn = modded.dfn + CROUCHED_DFN*MULT_STATS
        modded.pen = modded.pen + CROUCHED_PEN*MULT_STATS
        modded.pro = modded.pro + CROUCHED_PRO*MULT_STATS
        modded.gra = modded.gra + CROUCHED_GRA*MULT_STATS
    # seated
    if world.has_component(ent, cmp.StatusBPos_Seated):
##        modded.height = modded.height * SEATED_HEIGHTMOD
        modded.msp = modded.msp * SEATED_MSPMOD
        modded.atk = modded.atk + SEATED_ATK*MULT_STATS
        modded.dfn = modded.dfn + SEATED_DFN*MULT_STATS
        modded.pen = modded.pen + SEATED_PEN*MULT_STATS
        modded.pro = modded.pro + SEATED_PRO*MULT_STATS
        modded.gra = modded.gra + SEATED_GRA*MULT_STATS
    # supine
    if world.has_component(ent, cmp.StatusBPos_Supine):
##        modded.height = modded.height * SUPINE_HEIGHTMOD
        modded.msp = modded.msp * SUPINE_MSPMOD
        modded.atk = modded.atk + SUPINE_ATK*MULT_STATS
        modded.dfn = modded.dfn + SUPINE_DFN*MULT_STATS
        modded.pen = modded.pen + SUPINE_PEN*MULT_STATS
        modded.pro = modded.pro + SUPINE_PRO*MULT_STATS
        modded.gra = modded.gra + SUPINE_GRA*MULT_STATS
    # prone
    if world.has_component(ent, cmp.StatusBPos_Prone):
##        modded.height = modded.height * PRONE_HEIGHTMOD
        modded.msp = modded.msp * PRONE_MSPMOD
        modded.atk = modded.atk + PRONE_ATK*MULT_STATS
        modded.dfn = modded.dfn + PRONE_DFN*MULT_STATS
        modded.pen = modded.pen + PRONE_PEN*MULT_STATS
        modded.pro = modded.pro + PRONE_PRO*MULT_STATS
        modded.gra = modded.gra + PRONE_GRA*MULT_STATS
    
    
    
#~~~~~~~#--------------------------#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
        # encumberance - stat mods #
        #--------------------------#

    # Things should avoid affecting attributes as much as possible.
    # Encumberance should not affect agility or any other attribute
    # because encumberance max is dependent on attributes.
    # Ratio of encumberance
    encpc = max(0, 1 - (modded.enc / max(1,modded.encmax)))
    # SP Regen acts differently -- no breakpoints.
    modded.mpregen = modded.mpregen * (0.5 + 1*encpc)
    # Breakpoint stats -- gotten from ENCUMBERANCE_MODIFIERS dict
    encbp = get_encumberance_breakpoint(modded.enc, modded.encmax)
    if encbp > 0:
        index = encbp - 1
        modded.asp = min(modded.asp,
            ENCUMBERANCE_MODIFIERS['asp'][index] * modded.asp)
        modded.msp = min(modded.msp,
            ENCUMBERANCE_MODIFIERS['msp'][index] * modded.msp)
        modded.atk = min(modded.atk,
            ENCUMBERANCE_MODIFIERS['atk'][index] * modded.atk)
        modded.dfn = min(modded.dfn,
            ENCUMBERANCE_MODIFIERS['dfn'][index] * modded.dfn)
        modded.pro = min(modded.pro,
            ENCUMBERANCE_MODIFIERS['pro'][index] * modded.pro)
        modded.gra = min(modded.gra,
            ENCUMBERANCE_MODIFIERS['gra'][index] * modded.gra)
        modded.bal = min(modded.bal,
            ENCUMBERANCE_MODIFIERS['bal'][index] * modded.bal)
    #
    
#~~~~~~~#--------------#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
        #   finalize   #
        #--------------#
    
    # final multipliers
    # apply mods -- mult mods
    for bps in bpdata:
        for k,v in bps.multMods.items():
            if modded.__dict__[k] > 0:
                modded.__dict__[k] = v * modded.__dict__[k]
        if bps.equip:
            for k,v in bps.equip.multMods.items():
                if modded.__dict__[k] > 0:
                    modded.__dict__[k] = v * modded.__dict__[k]
    
    # round values as the final step
    for k,v in modded.__dict__.items():
        modded.__dict__[k] = around(v)

    caphp(ent)
    capmp(ent)

##    print(" ** ~~~~ ran _update_stats.")

    # NOTE: resulting values can be negative, but this can be
    #   checked for, depending on the individual uses for each stat
    #   e.g. MSp cannot be below 1-5 or so for purposes of movement,
    #   Spd cannot be below 1, Dmg cannot be below 0,
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    assert(not on(ent, DIRTY_STATS)) # MUST NOT BE DIRTY OR ELSE A MAJOR PROBLEM EXISTS IN THE CODE. Before this is called, dirty_stats flag is removed. If it got reset during this function then we get infinite recursion of this expensive function.
    return modded
# end def


# create and initialize the ModdedStats component
def create_moddedStats(ent):
    world=Rogue.world
    modded=cmp.ModdedStats()
    base=world.component_for_entity(ent, cmp.Stats)
    for k in base.__dict__.keys():
        modded.__dict__.update({ k : 0 })
    world.add_component(ent, modded)
    make(ent, DIRTY_STATS)
    return modded






        
    #-------------#
    # occupations #
    #-------------#

# OBSELETE (?)
##def occupations(ent):
##    return Rogue.occupations.get(ent, None)
##def occupation_add(ent,turns,fxn,args,helpless):
##    '''
##        fxn: function to call each turn.
##        args: arguments to pass into fxn
##        turns: turns remaining in current occupation
##        helpless: bool, whether ent can be interrupted
##        interrupted: bool, whether ent has been interrupted in this action
##    '''
##    Rogue.occupations.update({ ent : (fxn,args,turns,helpless,False) })
##def occupation_remove(ent):
##    del Rogue.occupations[ent]
##def occupation_elapse_turn(ent):
##    fxn,args,turns,helpless,interrupted = Rogue.occupations[ent]
##    if interrupted:
##        Rogue.occupations.update({ ent : (fxn,args,turns - 1,helpless,interrupted) })
##        return False    # interrupted occupation
##    if turns:
##        setAP(ent, 0)
##        Rogue.occupations.update({ ent : (fxn,args,turns - 1,helpless,interrupted) })
##    elif fxn is not None:
##        fxn(ent, args)
##    return True     # successfully continued occupation
    



    #----------------#
    #    lights      #
    #----------------#

def list_lights(): return list(Rogue.c_managers["lights"].lights.values())
def create_light(x,y, value, owner=None): # value is range of the light.
    lumosity = value**lights.Light.LOGBASE
    light=lights.Light(x,y, lumosity, owner)
    light.fovID=0
    light.shine()
    lightID = Rogue.c_managers['lights'].add(light)
    if owner: # entity that has this Light object as a component
        # TODO: convert Light object / merge w/ LightSource compo, make functions global instead of member funcs (same for EnvLights) (low priority)
        if Rogue.world.has_component(owner, cmp.LightSource):
            compo = Rogue.world.component_for_entity(owner, cmp.LightSource)
            release_light(compo.lightID)
        Rogue.world.add_component(owner, cmp.LightSource(lightID, light))
    return lightID
def create_envlight(value, owner=None): # environment light
    light=lights.EnvLight(value, owner)
    light.shine()
    lightID = Rogue.c_managers['lights'].add_env(light)
    if owner:
        if Rogue.world.has_component(owner, cmp.LightSource):
            compo = Rogue.world.component_for_entity(owner, cmp.LightSource)
            release_envlight(compo.lightID)
        Rogue.world.add_component(owner, cmp.LightSource(lightID, light))
    return lightID

def release_light(lightID):
    light = Rogue.c_managers['lights'].get(lightID)
    light.unshine()
    if light.owner:
        Rogue.world.remove_component(light.owner, cmp.LightSource)
    Rogue.c_managers['lights'].remove(lightID)
def release_envlight(lightID):
    light = Rogue.c_managers['lights'].get_env(lightID)
    light.unshine()
    if light.owner:
        Rogue.world.remove_component(light.owner, cmp.LightSource)
    Rogue.c_managers['lights'].remove_env(lightID)



    #-------------#
    #   fires     #
    #-------------#

#fire tile flag is independent of the status effect of burning
def set_fire(x,y):
    Rogue.et_managers['fire'].add(x,y)
def douse(x,y): #put out a fire at a tile and cool down all things there
    if not Rogue.et_managers['fire'].fireat(x,y): return
    Rogue.et_managers['fire'].remove(x,y)
    for ent in thingsat(x,y):
        clear_status(ent, cmp.StatusBurn)
        cooldown(ent)



    #----------------#
    #    status      #
    #----------------#

#Status for being on fire separate from the fire entity and light entity.

def get_status(ent, statusCompo): #getstatus #status_get
    if Rogue.world.has_component(ent, statusCompo):
        return Rogue.world.component_for_entity(ent, statusCompo)
    else:
        return None
def set_status(ent, status, t=-1, q=None):
    '''
        # ent       = Thing object to set the status for
        # status    = status class (not an object instance)
        # t         = duration (-1 is the default duration for that status)
        # q         = quality (for specific statuses)
    '''
    proc.Status.add(ent, status, t, q)
def clear_status(ent, status):
    proc.Status.remove(ent, status)
def clear_status_all(ent):
    proc.Status.remove_all(ent)



    #-----------#
    #  actions  #
    #-----------#

def queue_action(ent, act):
    pass
    #Rogue.c_managers['actionQueue'].add(obj, act)






    #----------#
    # managers #
    #----------#

# manager listeners
class Manager_Listener: # listens for a result from a game state Manager.
    def alert(self, result): # after we get a result, purpose is finished.
        manager_listeners_remove(self) # delete the reference to self.
class Aim_Manager_Listener(Manager_Listener): # TODO: create instance of this class and add it using manager_listeners_add() when you press the Aim command.
    def __init__(self, shootfunc):
        self.shootfunc=shootfunc # function that runs when you select ...
                                 # ... to fire at a viable target.
    def alert(self, result):
        if type(result) is int:
            self.shootfunc(result)
        super(Aim_Manager_Listener, self).alert(result)

def manager_listeners_alert(result):
    for listener in manager_listeners():
        listener.alert(result)
def manager_listeners(): return Rogue.manager_listeners
def manager_listeners_add(obj): Rogue.manager_listeners.append(obj)
def manager_listeners_remove(obj): Rogue.manager_listeners.remove(obj)

# 

def Input(x,y, w=1,h=1, default='',mode='text',insert=False):
    return IO.Input(x,y,w=w,h=h,default=default,mode=mode,insert=insert)

# constant managers #

def manager_sights_run():   Rogue.c_managers['sights'].run()
def manager_sounds_run():   Rogue.c_managers['sounds'].run()

# per-turn managers #

def register_timer(obj):    Rogue.bt_managers['timers'].add(obj)
def release_timer(obj):     Rogue.bt_managers['timers'].remove(obj)

# game state managers #

def get_active_manager():       return Rogue.manager
def close_active_manager():
    if Rogue.manager:
        manager_listeners_alert(Rogue.manager.result)
        Rogue.manager.close()
        Rogue.manager=None
def clear_active_manager():
    if Rogue.manager:
        Rogue.manager.set_result('exit')
        close_active_manager()

def routine_look(xs, ys):
    clear_active_manager()
    game_set_state("manager") #look
    Rogue.manager=managers.Manager_Look(
        xs, ys, Rogue.view, Rogue.map.get_map_state())
    alert("Look where? (<hjklyubn>, mouse; <select> to confirm)")
    Rogue.view.fixed_mode_disable()

def routine_move_view():
    clear_active_manager()
    game_set_state("manager") #move view
    Rogue.manager=managers.Manager_MoveView(
        Rogue.view, Rogue.map.get_map_state(),
        "Direction? (<hjklyubn>; <select> to center; <Esc> to save position)")
    Rogue.view.fixed_mode_disable()
    
def aim_find_target(xs, ys, selectfunc):
    # selectfunc: the function that is ran when you select a valid target
    clear_active_manager()
    game_set_state("manager") #move view
    Rogue.manager=managers.Manager_AimFindTarget(
        xs, ys, Rogue.view, Rogue.map.get_map_state())
    Rogue.view.fixed_mode_disable()
    # listener -- handles the shooting
    listener = Aim_Manager_Listener(selectfunc)
    manager_listeners_add(listener)

# Manager_PrintScroll
def help():
    clear_active_manager()
    game_set_state("manager") # help
    width   = window_w()
    height  = window_h()
    strng   = IO.render_help()
    nlines  = 1 + strng.count('\n')
    hud1h   = 3
    hud2h   = 3
    scroll  = makeConBox(width,1000,strng)
    top     = makeConBox(width,hud1h,"help")
    bottom  = makeConBox(width,hud2h,"<Up>, <Down>, <PgUp>, <PgDn>, <Home>, <End>; <select> to return")
    Rogue.manager = managers.Manager_PrintScroll(
        scroll,width,height, top,bottom, h1=hud1h,h2=hud2h,maxy=nlines)
# end def
def routine_print_msgHistory():
    clear_active_manager()
    game_set_state("manager") #message history
    width   = window_w()
    height  = window_h()
    strng   = Rogue.log.printall_get_wrapped_msgs()
    nlines  = 1 + strng.count('\n')
    hud1h   = 3
    hud2h   = 3
    scroll  = makeConBox(width,1000,strng)
    top     = makeConBox(width,hud1h,"message history")
    bottom  = makeConBox(width,hud2h,"<Up>, <Down>, <PgUp>, <PgDn>, <Home>, <End>; <select> to return")
    Rogue.manager = managers.Manager_PrintScroll(
        scroll,width,height, top,bottom, h1=hud1h,h2=hud2h,maxy=nlines)
# end def
def routine_print_charPage():
    clear_active_manager()
    game_set_state("manager") #character page
    width   = window_w()
    height  = window_h()
    strng   = misc.render_charpage_string(width,height,pc(),get_turn(),dlvl())
    nlines  = 1 + strng.count('\n')
    hud1h   = 3
    hud2h   = 3
    scroll  = makeConBox(width,200,strng)
    top     = makeConBox(width,hud1h,"character data sheet")
    bottom  = makeConBox(width,hud2h,"<Up>, <Down>, <PgUp>, <PgDn>, <Home>, <End>; <select> to return")
    Rogue.manager = managers.Manager_PrintScroll(
        scroll,width,height, top,bottom, h1=hud1h,h2=hud2h,maxy=nlines)
# end def

#
# get direction
# player chooses a direction using key bindings or the mouse,
# returns a tuple or None
#
def get_direction():
    while True:
        pcAct=IO.handle_mousekeys(IO.get_raw_input()).items()
        for act,arg in pcAct:
            if (act=="context-dir" or act=="move"):
                return arg
            if act=="exit":
                alert("")
                return None
            if act=="select":
                return (0,0,0,)
            if act=="lclick":
                mousex,mousey,z=arg
                pc=Rogue.pc
                dx=mousex - getx(pc.x)
                dy=mousey - gety(pc.y)
                if (dx >= -1 and dx <= 1 and dy >= -1 and dy <= 1):
                    return (dx,dy,0,)
# end def
    
#prompt
# show a message and ask the player for input
# Arguments:
#   x,y:        top-left position of the prompt box
#   w,h:        width, height of the prompt dbox
#   maxw:       maximum length of the response the player can give
#   q:          question to display in the prompt dbox
#   default:    text that is the default response
#   mode:       'text' or 'wait'
#   insert:     whether to begin in Insert mode for the response
#   border:     border style of the dbox
def prompt(x,y, w,h, maxw=1, q='', default='',mode='text',insert=False,border=0):
    #libtcod.console_clear(con_final())
    dbox(x,y,w,h,text=q,
        wrap=True,border=border,con=con_final(),disp='mono')
    result=""
    while (result==""):
        refresh()
        if mode=="wait":
            xf=x+w-1
            yf=y+h-1
        elif mode=="text":
            xf=x
            yf=y+h
        result = Input(xf,yf,maxw,1,default=default,mode=mode,insert=insert)
    return result

#menu
#this menu freezes time until input given.
# Arguments:
#   autoItemize: create keys for your keysItems iterable automagically
#   keysItems can be an iterable or a dict.
#       **If a dict, autoItemize MUST be set to False
#       dict allows you to customize what buttons correspond to which options
def menu(name, x,y, keysItems, autoItemize=True):
    manager=managers.Manager_Menu(name, x,y, window_w(),window_h(), keysItems=keysItems, autoItemize=autoItemize)
    result=None
    while result is None:
        manager.run()
        result=manager.result
    manager.close()
    if result == ' ': return None
    return manager.result
    
def adjacent_directions(_dir):
    return ADJACENT_DIRECTIONS.get(_dir, ((0,0,0,),(0,0,0,),) )
    












        # commented out code below. #











        


'''
interesting = [] # possible targets
                checkdir = arg
                t = 0
                
                while True:
                    t += 1
                    
                    # check this tile
                    xd = checkdir[0]*t
                    yd = checkdir[1]*t
                    xx = pos.x + xd
                    yy = pos.y + yd
                    
                    # check we can see this tile
                    if (xd**2 + yd**2)**0.5 > sight:
                        break
                    
                    here = monat(xx,yy)
                    if here:
                        score = t
                        interesting.append( (here, score) )
                        
                    # check tiles in 2 lines spreading outward from this tile
                    for dir1, dir2 in adjacent_directions(checkdir):
                        g = 0
                        while t + g < sight:
                            pass
                        # end while
                    # end for
                # end while
                '''


# Skills
# might not use any skills at all
'''
i = 1
AXES        = i; i+=1;  # 
BLADES      = i; i+=1;  # swords and knives, shortblades
BLUNT       = i; i+=1;  # all blunt weapons, flails and quarterstaffs
MARKSMAN    = i; i+=1;  # bows, throwing, other ranged attacks
MEDS        = i; i+=1;  # medicine
REPAIR      = i; i+=1;  # repair armor, weapons,
SPEECH      = i; i+=1;  # and barter
SPELLS      = i; i+=1;  # spellcasting
STEALTH     = i; i+=1;  # 
TRAPS       = i; i+=1;  # find, set, and create traps

STATMODS_WRESTLING  ={'atk':4,'dfn':2,'dmg':1,'nrg':-3}
STATMODS_SWORDS     ={'atk':2,'dfn':2,'dmg':2,'nrg':-2}
STATMODS_DAGGERS    ={'atk':2,'dfn':2,'dmg':2,'nrg':-3}
STATMODS_AXES       ={'atk':2,'dmg':2,'nrg':-2}
STATMODS_CUDGELS    ={'atk':2,'dmg':2,'nrg':-2}
'''




##    #---------------#
##    #     Lists     #
##    #---------------#
##
##class Lists():
##    creatures   =[]     # living things
##    inanimates  =[]     # nonliving
##    lights      =[]
##    fluids      =[]
##    
##    @classmethod
##    def things(cls):
##        lis1=set(cls.creatures)
##        lis2=set(cls.inanimates)
##        return lis1.union(lis2)
##
### lists functions #
##
##def list_creatures():           return Lists.creatures
##def list_inanimates():          return Lists.inanimates
##def list_things():              return Lists.things()
##def list_lights():              return Lists.lights
##def list_fluids():              return Lists.fluids
##def list_add_creature(ent):     Lists.creatures.append(ent)
##def list_remove_creature(ent):  Lists.creatures.remove(ent)
##def list_add_inanimate(ent):    Lists.inanimates.append(ent)
##def list_remove_inanimate(ent): Lists.inanimates.remove(ent)
##def list_add_light(ent):        Lists.lights.append(ent)
##def list_remove_light(ent):     Lists.lights.remove(ent)
##def list_add_fluid(ent):        Lists.fluids.append(ent)
##def list_remove_fluid(ent):     Lists.fluids.remove(ent)
##

    #------------------------#
    # Stats Functions + vars #
    #------------------------#

# Stat mod Effects are handled entirely by components.

##class Effects:
##    effects={}
##    ID=0
##    # OLD IDEA: individually apply each mod in "mod" and divide / sort by entity, component and stat (variable of component)
##    # *** BETTER IDEA *** :
##     #  when durability of an equipped item drops below certain percentages,
##     #  (constants like 75%, 50%, and 25%, etc.)
##     #  it becomes unequipped and re-equipped, and when you equip
##     #  an item with those percentages of durability you receive
##     #  a penalty to stats that is implemented on-the-fly by
##     #  predetermined constants. THIS WOULD WORK WITH EXISTING SYSTEM.
##    @classmethod
##    def add(cls, ent, mod):
##        # add in new effect
##        Effects.ID+=1
##        Effects.effects.update({Effects.ID : (ent, mod,)})
##        # apply changes to stats
##        compo = Rogue.world.component_for_entity(ent, cmp.Stats)
##        for _var, _modf in mod.items():
##            entCompo.__dict__[_var] += _modf
##        return Effects.ID
##    @classmethod
##    def remove(cls, effID):
##        if not effID in Effects.effects.keys():
##            print("ERROR: failed to remove effect ID ",effID)
##            return False
##        # undo stat modifiers
##        ent,mod = Effects.effects[modID]
##        for compo, data in mod.items():
##            if not Rogue.world.has_component(ent, compo):
##                continue
##            entCompo = Rogue.world.component_for_entity(ent, compo)
##            for _var, _modf in data.items():
##                entCompo.__dict__[_var] -= _modf
##        # remove effect from dict
##        del Effects.effects[effID]
##        return True
####    @classmethod
####    def get(cls, ent, comp, stat):
####        base = Rogue.world.component_for_entity(ent, comp).__dict__[stat]
####        modBonus = Effects.modData.get()
##
##def effect_add(ent,mod):        # Stat mod create
##    effID=Effects.add(ent,mod)
##    return effID
##def effect_remove(modID):   # Stat mod delete
##    Effects.remove(modID)
##
