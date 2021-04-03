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

'''
    TODO: pickle to save state
    TODO: reproduceable pseudo random generator (state saved using pickle)
        https://stackoverflow.com/questions/5012560/how-to-query-seed-used-by-random-random
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
import random
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
    c_entities={} #const entities
    manager = None # current active game state manager
    manager_listeners = [] #
    fov_maps = []
    # boolean flags
    allow_warning_msp = True    # for warning prompt for very slow move speed
    _pause_menu_key_listener = False

    @classmethod
    def pause_menu_key_listener(cls):
        cls._pause_menu_key_listener = True
    @classmethod
    def resume_menu_key_listener(cls):
        cls._pause_menu_key_listener = False
    @classmethod
    def menu_key_listener_is_paused(cls):
        return cls._pause_menu_key_listener
    
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

    @classmethod
    def create_const_entities(cls):
        # stone wall
        _ent_stone_wall = cls.world.create_entity(
            cmp.Name("stone wall"),
            cmp.Form(mat=MAT_STONE, shape=SHAPE_WALL),
            cmp.Stats(hp=1000, arm=20, pro=24),
            )
        cls.c_entities.update({ENT_STONE_WALL : _ent_stone_wall})
    # end def
    
#/Rogue


    #----------------#
    #   Functions    #
    #----------------#

    # Rogue
def const_ent(ent): return Rogue.c_entities[ent]
def _ent_stone_wall(): return const_ent(ENT_STONE_WALL)

# global warning flags
def allow_warning_msp():
    return Rogue.allow_warning_msp
def reset_warning_msp():
    Rogue.allow_warning_msp = True
def expire_warning_msp():
    Rogue.allow_warning_msp = False
    

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
def fame():             return Rogue.data.fame()
def infamy():           return Rogue.data.infamy()
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
def get_time_ratio():   return (Rogue.clock.turn % 86400) / 86400
def get_time_of_day():
    thetime = get_time_ratio()
    for k,v in TIMES_OF_DAY.items():
        if thetime >= k:
            result = v[0]
    return result
def get_time_of_day_colloquial():
    thetime = get_time_ratio()
    for k,v in TIMES_OF_DAY.items():
        if thetime >= k:
            result = v[1]
    return result

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


    # global return values. Functions can modify this as an additional
        #  "return" value list.
class Return:
    values=None
def globalreturn(*args): Return.values = args
def fetchglobalreturn():
    ret=Return.values
    Return.values=None
    return ret


# BITWISE OPERATORS ON BYTES OBJECT / BYTEARRAY

def AND(abytes, bbytes):
    return bytes([a & b for a, b in zip(abytes[::-1], bbytes[::-1])][::-1])
def NAND(abytes, bbytes):
    return NOT(AND(abytes, bbytes)) # OR(NOT, NOT)
def OR(abytes, bbytes):
    return bytes([a | b for a, b in zip(abytes[::-1], bbytes[::-1])][::-1])
def NOR(abytes, bbytes):
    return NOT(OR(abytes, bbytes))
def XOR(abytes, bbytes):
    return bytes([a ^ b for a, b in zip(abytes[::-1], bbytes[::-1])][::-1])
def NOT(abytes): # just XOR w/ mask full of 1's
    return XOR(abytes, bytes([255 for _ in range(len(abytes))]))
def GETBYTES(abytes):
    for byte in abytes:
        yield byte


    #------------------------#
    # functions from modules #
    #------------------------#

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


# Identification functions

def identify_get_name(idtype):
    return IDENTIFICATION[idtype][0]
def identify_entity(ent, quality): # only PC can Identify things
    world=Rogue.world
    if world.has_component(ent, cmp.Identified):
        compo = world.component_for_entity(ent, cmp.Identified)
        compo.quality = max(0, compo.quality, quality)
    else:
        world.add_component(ent, cmp.Identified(quality))

# Name functions

def getMatName(mat): return MATERIALS[mat][0]
def getMatDT(mat): return MATERIALS[mat][1]
def getMatHardness(mat): return MATERIALS[mat][2]
def getMatPrice(mat, mass=MULT_MASS): # $/kg (default mass == 1kg)
    return around(mass/MULT_MASS * MATERIALS[mat][3]*MULT_VALUE)
def add_prefix(ent, prefix): # add a prefix to an entity
    if Rogue.world.has_component(ent, cmp.Prefixes):
        compo = Rogue.world.component_for_entity(ent, cmp.Prefixes)
        compo.prefixes.append(prefix)
    else:
        Rogue.world.add_component(ent, cmp.Prefixes(prefix))
# end def
def fullname(ent):
    '''
        # UNFINISHED!!!!! TEST REQUIRED!!!!!!!
        
        get the full name of entity ent with all prefixes, suffixes, etc.
         (but do not add the title)
        this depends on the level of identification the player has
         for the entity -- at anything less than max level ID, the actual
         name is not displayed, but a pseudonym which describes it in
         some vague fashion e.g. "club" instead of "metal cudgel"
    '''
    world=Rogue.world
    shapeOnly = False

    '''
    # TODO: before getting this working / tested, we need to
    # set up Identification properly using identify_entity(...)
    # whenever the PC interacts with or sees something
    
    if not world.has_component(ent, cmp.Identified):
        shapeOnly = True
    else:
        quality = world.component_for_entity(ent, cmp.Identified).quality

        if quality<=0:
            shapeOnly = True
            
        # LOW-LEVEL ID (type of thing) (identify basic type)
        elif quality==1:
            idtype = world.component_for_entity(ent, cmp.Identify).generic
            return "{} {}".format(UNID, identify_get_name(idtype))
        
        # LOW-LEVEL ID (+ MATERIAL) (identify make-up)
        elif quality==2: 
            idtype = world.component_for_entity(ent, cmp.Identify).generic
            if world.has_component(ent, cmp.MaterialPrefix):
                mat = world.component_for_entity(ent, cmp.Form).material
            return "{} {} {}".format(
                UNID, getMatName(mat), identify_get_name(idtype)
                )

        # IDEA: mid-level Identification: identify skill required,
        #  uses, etc. (identify the purpose of the item)

        else: # FULL IDENTIFICATION OF UNIQUE INSTANCE
            pass # continue with full identification
        
    if shapeOnly:
        # we can only identify it by its vague form
        shape = world.component_for_entity(ent, cmp.Form).shape
        return "{} {}".format(UNID, SHAPES[shape])
    '''
    
    # full identification #
    # if we made it this far, return a full name #

    name = world.component_for_entity(ent, cmp.Name).name

    # TEST
    print("called fullname on ent {}".format(name))
    
    if world.has_component(ent, cmp.MaterialPrefix):
        mat = world.component_for_entity(ent, cmp.Form).material
        name = "{} {}".format(getMatName(mat), name)
            
    if world.has_component(ent, cmp.Prefixes):
        compo = world.component_for_entity(ent, cmp.Prefixes)
        for prefix in compo.prefixes:
            name = "{} {}".format(PREFIXES[prefix], name)
            
    if world.has_component(ent, cmp.StatusRusted):
        compo = world.component_for_entity(ent, cmp.StatusRusted)
        for k,v in RUST_QUALITIES.items():
            if compo.quality == k:
                string = RUSTEDNESS[v][2] # TODO: test
                name = "{} {}".format(string, name)
                break
            
    if world.has_component(ent, cmp.StatusRotted):
        compo = world.component_for_entity(ent, cmp.StatusRotted)
        for k,v in ROT_QUALITIES.items():
            if compo.quality == k:
                string = ROTTEDNESS[v][2] # TODO: test
                name = "{} {}".format(string, name)
                break
            
    return name
# end def
def fullname_gear(ent):
    world=Rogue.world
    name = fullname(ent)
    if ( world.has_component(ent, cmp.Fitted)
         and Rogue.pc==world.component_for_entity(ent, cmp.Fitted).entity ):
        name = "fitted {}".format(name)
    return name
# end def


    # "Fun"ctions #

def ceil(f): return math.ceil(f)
def line(x1,y1,x2,y2):
    for tupl in misc.Bresenham2D(x1,y1,x2,y2):
        yield tupl
def in_range(x1,y1,x2,y2,Range):
    return (maths.dist(x1,y1, x2,y2) <= Range + .34)
def around(f): # round with an added constant to nudge values ~0.5 up to 1 (attempt to get past some rounding errors)
    return round(f + 0.00001)
def about(f1, f2): # return True if the two floating point values are very close to the same value
    return (abs(f1-f2) < 0.00001)
def slt(f1, f2): # significantly less than (buffer against floating point errors)
    return (f1 + 0.00001 < f2)
def sgt(f1, f2): # significantly greater than (buffer against floating point errors)
    return (f1 - 0.00001 > f2)
def sign(n):
    if n>0: return 1
    if n<0: return -1
    return 0
def numberplace(i): # convert integer to numbering position / numbering place / number position / number place
    imod10 = i % 10
    imod100 = i % 100
    if (imod100 < 11 or imod100 > 13): # except *11, *12, *13 which end in "th"
        if imod10==1: return "{}st".format(i) # e.g. 21st
        if imod10==2: return "{}nd".format(i) # e.g. 172nd
        if imod10==3: return "{}rd".format(i) # e.g. 3rd
    return "{}th".format(i) # e.g. 212th

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
def gettitle(ent):
    return TITLES[Rogue.world.component_for_entity(ent, cmp.Name).title]
def gettitlename(ent):
    compo = Rogue.world.component_for_entity(ent, cmp.Name)
    return "{}{}".format(TITLES[compo.title], compo.name)
def getinv(ent):
    return Rogue.world.component_for_entity(ent, cmp.Inventory).data
def get_value(ent):
    return Rogue.world.component_for_entity(ent, cmp.Form).value
def get_value_dollars(ent):
    return Rogue.world.component_for_entity(ent, cmp.Form).value//MULT_VALUE
def get_value_cents(ent):
    return Rogue.world.component_for_entity(ent, cmp.Form).value % MULT_VALUE
def get_personality(ent):
    return Rogue.world.component_for_entity(ent, cmp.Personality).personality
def get_disposition(ent):
    return Rogue.world.component_for_entity(ent, cmp.Disposition).disposition

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
def roomtemp(): return 22 #temporary

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

    
    #---------------------#
    # component functions #
    #---------------------#

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
    newMeters.fire = meters.fire
    newMeters.frost = meters.frost
    newMeters.rads = meters.rads
    newMeters.expo = meters.expo
##    newMeters.sick = meters.sick
##    newMeters.pain = meters.pain
##    newMeters.fear = meters.fear
##    newMeters.bleed = meters.bleed
##    newMeters.rust = meters.rust
##    newMeters.rot = meters.rot
##    newMeters.wet = meters.wet
    return newMeters

    #------------------#
    # entity functions #
    #------------------#

def entity_exists(ent):
    return ent in world._entities.keys()

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
def getmomentum(ent):
    if Rogue.world.has_component(ent, cmp.Momentum):
        return Rogue.world.component_for_entity(ent, cmp.Momentum)
    else:
        return None

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
    level = getskill(ent, skill)
    if level >= MAX_SKILL:
        return
    # trait bonuses
    if Rogue.world.has_component(ent, cmp.Talented):
        compo = Rogue.world.component_for_entity(ent, cmp.Talented)
        pts = pts * compo.talents.get(skill, 1)
    if Rogue.world.has_component(ent, cmp.FastLearner):
        pts = pts * FASTLEARNER_EXPMOD
    # intelligence bonus to experience
    pts += around( getms(ent,'int')//MULT_STATS*pts*ATT_INT_EXPBONUS )
    # diminishing returns on skill gainz
    pts = around( pts - level*EXP_DIMINISH_RATE )
    # points calculated; try to apply experience
    if pts > 0:
        make(ent,DIRTY_STATS)
        skills = Rogue.world.component_for_entity(ent, cmp.Skills)
        __train(ent, skills, skill, pts)
    # level up message
    if (Rogue.pc==ent and getskill(ent, skill) > level):
        msg("Level up {} to {}".format(
            get_skill_name(skill), getskill(ent, skill)))
# end def
def __train(ent, skills, skill, pts): # train one level at a time
    if getskill(ent, skill) >= MAX_SKILL:
        return
    exp = min(pts, EXP_LEVEL)
    skills.skills[skill] = skills.skills.get(skill, 0) + exp
    pts = pts - exp - EXP_DIMINISH_RATE
    if pts > 0:
        __train(ent, skills, skill, pts)
# end def
def forget(ent, skill, pts): # lose skill experience
    assert(Rogue.world.has_component(ent, cmp.Skills))
    skills = Rogue.world.component_for_entity(ent, cmp.Skills)
    skills.skills[skill] = max(0, skills.skills.get(skill, pts) - pts)
    make(ent,DIRTY_STATS)
# end def
def get_skill_skillpts(skill): return SKILLS[skill][0]
def get_skill_learnrate(skill): return SKILLS[skill][1]
def get_skill_name(skill): return SKILLS[skill][2]

# flags
        # bitwise flags
    # restricted to 8 flags (1 full byte)
    #   TODO: expand to be able to take more than 8 flags.
    # reason: bytes((flag,)) <- flag cannot exceed 255. Must
    #   potentially have multiple zeroed-out bytes in the bytes object...
    #   How can we do this?
def onb(bp, flag: int): 
    return bool(AND( bytes((flag,)), bp.flags ))
def makeb(bp, flag: int):
    bp.flags = OR( bytes((flag,)), bp.flags )
def makenotb(bp, flag: int):
    bp.flags = AND( bp.flags, NOT(bytes((flag,))) )
        # set flags
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
    
    grid_remove(item)
    Rogue.world.component_for_entity(ent, cmp.Inventory).data.append(item)
    Rogue.world.add_component(item, cmp.Carried(ent))
    Rogue.world.add_component(item, cmp.Child(ent))
# end def

def take(ent,item):
##    print("taken!")
    Rogue.world.component_for_entity(ent, cmp.Inventory).data.remove(item)
    Rogue.world.remove_component(item, cmp.Carried)
    Rogue.world.remove_component(item, cmp.Child)
    if Rogue.world.has_component(item, cmp.Equipped):
        Rogue.world.remove_component(item, cmp.Equipped)
    if Rogue.world.has_component(item, cmp.Held):
        Rogue.world.remove_component(item, cmp.Held)

def mutate(ent):
    # TODO: do mutation
    mutable = Rogue.world.component_for_entity(ent, cmp.Mutable)
    pos = getpos(ent)
    # TODO: message based on mutation (i.e. "{t}{n} grew an arm!") Is this dumb?
    event_sight(pos.x,pos.y,"{n} mutated!".format(n=gettitlename(ent)))

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

def nudge(ent,xd,yd):
    pos=Rogue.world.component_for_entity(ent, cmp.Position)
    x = pos.x + xd
    y = pos.y + yd
    if getmap().tilefree(x,y):
        port(ent, x, y)
        return True
    return False
def port(ent,x,y):
    ''' move thing to absolute location, update grid and FOV
        do not check for a free space before moving
    '''
    grid_remove(ent)
    if not Rogue.world.has_component(ent, cmp.Position):
        Rogue.world.add_component(ent, cmp.Position())
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
    if world.has_component(item, cmp.Position):
        world.remove_component(item, cmp.Position)
    
def drop(ent,item,dx=0,dy=0):   #remove item from ent's inventory, place it on ground nearby ent.
    world=Rogue.world
    make(ent, DIRTY_STATS)
    take(ent,item)
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
def capres(ent): # does not make stats dirty! Doing so is a huge glitch!
    modded = Rogue.world.component_for_entity(ent, cmp.ModdedStats)
    modded.resfire  = max(MIN_RES, modded.resfire)
    modded.rescold  = max(MIN_RES, modded.rescold)
    modded.resbio   = max(MIN_RES, modded.resbio)
    modded.reselec  = max(MIN_RES, modded.reselec)
    modded.resphys  = max(MIN_RES, modded.resphys)
    modded.respain  = max(MIN_RES, modded.respain)
    modded.resrust  = max(MIN_RES, modded.resrust)
    modded.resrot   = max(MIN_RES, modded.resrot)
    modded.reswet   = max(MIN_RES, modded.reswet)
    modded.resbleed = max(MIN_RES, modded.resbleed)
    modded.reslight = max(MIN_RES, modded.reslight)
    modded.ressound = max(MIN_RES, modded.ressound)


# these aren't tested, nor are they well thought-out
def knock(ent, amt, _dir): # apply force to an entity
    ''' apply amt force in direction _dir to entity ent '''
    mass = getms(ent, 'mass')
    bal = getms(ent, 'bal')
    effmass = mass * bal / BAL_MASS_MULT # effective mass
    dmg = amt // effmass
    stagger(ent, dmg)
    # knockback / pushing (TODO)
    # if force is sufficient to knockback (TODO: calculate (how to?))
##    push(ent, _dir, 1)
def stagger(ent, dmg): # reduce balance by dmg
    if Rogue.world.has_component(ent, cmp.StatusOffBalance):
        compo=Rogue.world.component_for_entity(ent, cmp.StatusOffBalance)
        dmg = dmg + compo.quality
    set_status(ent, cmp.StatusOffBalance(
        t = min(8, 1 + dmg//4), q=dmg) )
def push(ent, _dir, n=1):
    xd = _dir[0]
    yd = _dir[1]
    for ii in range(n):
        result = nudge(ent, xd,yd)
        if not result:
            return False
    return True
# end def

# identifying
##def map_generate(Map,level): levels.generate(Map,level) #OLD OBSELETE
def look_identify_at(x,y):
    if in_view(Rogue.pc,x,y): # TODO: finish implementation
        pass
    desc="__IDENTIFY UNIMPLEMENTED__" #IDENTIFIER.get(asci,"???")
    return "{}{}".format(char, desc)

def visibility(ent, sight, plight, camo, dist) -> int: # calculate visibility level
    '''
    Parameters:
        ent    : viewer
        sight  : vision stat of viewer
        plight : perceived light level
        camo   : camoflauge of the target to see
        dist   : distance from viewer to target

        TODO: test this function's output
            (function logic has been altered)
    '''
    _sx = 4 if on(ent, NVISION) else 1
    return int( math.log2(plight)*0.5 + ( 40+sight - (dice.roll(20)+camo+dist) )//20)
# end def

    
#damage hp
def damage(ent, dmg: int):
##    assert isinstance(dmg, int)
    if dmg <= 0: return
    make(ent,DIRTY_STATS)
    stats = Rogue.world.component_for_entity(ent, cmp.Stats)
    stats.hp -= dmg
    if stats.hp <= 0:
        kill(ent)
        return
    mat = Rogue.world.component_for_entity(ent, cmp.Form).material
    dt = getMatDT(mat)
    if dmg >= dt:
        kill(ent)
        return
# end def
def damage_phys(ent, dmg: int):
    if dmg <= 0: return
    resMult = 0.01*(100 - getms(ent, 'resphys'))     # resistance multiplier
    damage(ent, around(dmg*resMult))
# end def

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
    print('ent named {} exhausted.'.format(fullname(ent)))
    knockout(ent)

# sleepiness
def fatigue(ent, amt:int):
    if amt < 0: return
    make(ent,DIRTY_STATS)
    body = Rogue.world.component_for_entity(ent, cmp.Body)
    body.fatigue += amt

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

def collide(ent1, dmg1, ent2, dmg2, force):
    ''' collide two entities together with force force
        deal damage dmg1,dmg2 to ent1,ent2, respectively
    '''
    contact(ent1, ent2, force=force)
    damage(ent1, dmg1)
    damage(ent2, dmg2)
def contact(ent1,ent2,force=0): # touch two entities together
    world=Rogue.world
    mat1=world.component_for_entity(ent1, cmp.Form).material
    mat2=world.component_for_entity(ent1, cmp.Form).material
    mass1=getms(ent1, 'mass')
    mass2=getms(ent2, 'mass')
    hard1=getMatHardness(mat1)
    hard2=getMatHardness(mat2)
    gforce(ent1, force)
    gforce(ent2, force)
    if (hard1 > hard2):
        scratch(ent1, ent2, force)
    elif (hard2 > hard1):
        scratch(ent2, ent1, force)
# end def
def gforce(ent, force):
    pass
def scratch(ent1, ent2, force):
    pass
def calcwork(force):
    return force*2
def exercise(ent, bp, work: int):
    ''' exercise body part's muscle by amount work
        return True if muscle was not fatigued, else False
    '''
##    if bp.bone.status
    fatigue = work // (getms(ent, 'str')//MULT_STATS)
    if fatigue: bp.sp -= fatigue
    if bp.sp <= 0:
        bp.sp = 0
        return False # ran out of gas
    return True # still cookin' with gas

  
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

def get_power_level(ent):
    ''' get perceived strength / power level of an entity
        Assumes you can assess their stats
    '''
    level = 0
    # stat buffs
    level += getms(ent, 'idn')//4
    level += getms(ent, 'str')
    level += getms(ent, 'con')
    # fame / infamy raises perception of power
    level += fame()
    level -= infamy()
    # obvious damage to your person reduces perceived power level
    hpmax = getms(ent,'hpmax')
    hp = getms(ent,'hp')
    level -= (hpmax - hp)/hpmax * 20
    return level

def zombify(ent):
    kill(ent) # temporary
def explosion(name, x, y, radius):
    event_sight(x, y, "{n} explodes!".format(n=name))

def getid(ent): # get identification level of a given entity (from Player's perspective)
    if Rogue.world.has_component(ent, cmp.Identified):
        return Rogue.world.component_for_entity(ent, cmp.Identified).quality
    return 0
def getidchar(ent):
    return _getidchar(ent, getid(ent))
def _getidchar(ent, idlv):
    if idlv > 1:
        return world.component_for_entity(ent, cmp.Draw).char
    return '?'

# inreach | in reach | in_reach 
# Calculate if your target is within your reach (melee range).
# Instead of calculating with a slow* sqrt func, we access this cute grid:
_REACHGRIDQUAD=[ #0==origin
    [12,12,99,99,99,99,99,],
    [10,10,11,12,99,99,99,], # we only need 1 quadrant of the total
    [8, 8, 9, 10,11,99,99,], # grid to calculate if you are in reach.
    [6, 7, 7, 9, 10,12,99,],
    [4, 5, 6, 7, 9, 11,99,],
    [0, 3, 5, 7, 8, 10,12,],
    [0, 0, 4, 6, 8, 10,12,],
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
    world = Rogue.world
    if world.has_component(gear, cmp.Fitted):
        oldent = world.component_for_entity(gear, cmp.Fitted).entity
        if entity_exists(oldent):
            make(oldent, DIRTY_STATS)
    make(ent, DIRTY_STATS)
    world.add_component(gear, cmp.Fitted(ent))
    make(ent, DIRTY_STATS)

def _get_encsp(enc:int,encmax:int,spregen:int) -> int:
    ''' max SP modifier from encumberance % '''
    encrat = max(0, 1 - (enc / max(1,encmax)))
    return int(max(0, (SPREGEN_MIN + SPREGEN_D*(encrat**2)) * spregen))


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
    maxHearDist = volume * getms(ent,'hearing') / AVG_HEARING
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
    # initialize stats components
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

def create_monster(typ,x,y,color=None): #init from entities.py
    ''' create a monster from the bestiary and initialize it '''
    if monat(x,y):
        return None #tile is occupied by a creature already.
    if color:
        ent = entities.create_monster(typ,x,y,color)
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

# persons | people | things that speak | init speaker
def init_person(
    ent, personality=-1,
    getsAngry=True, getsAnnoyed=True, getsDiabetes=True,
    likesMen=False, likesWomen=False
    ):
    if personality==-1: personality = random.choice(MAIN_PERSONALITIES)
    Rogue.world.add_component(ent, cmp.Speaks())
    Rogue.world.add_component(ent, cmp.Personality(personality))
    Rogue.world.add_component(ent, cmp.Disposition())
    if getsAngry: Rogue.world.add_component(ent, cmp.GetsAngry())
    if getsAnnoyed: Rogue.world.add_component(ent, cmp.GetsAnnoyed())
    if getsDiabetes: Rogue.world.add_component(ent, cmp.GetsDiabetes())
    if likesMen: Rogue.world.add_component(ent, cmp.AttractedToMen())
    if likesWomen: Rogue.world.add_component(ent, cmp.AttractedToWomen())
    

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
    #  #Body  #
    #---------#

def getcoretype(plan): return CORETYPES.get(plan, CORETYPE_TORSO)
# randombp
class __randombp_G: # global storage
    total=0 # records total coverage
    #wrapper function to add to total coverage
def __randombp_cov( # add part to parts, add coverage to total
    parts:dict, bpdata:dict, biases:dict, metacov:int, bpm_const:int,
    bp_const:int, part:object
    ):
##    thiscov:int
    print("bpm: {}, bp: {}".format(bpm_const, bp_const))
    thiscov = bpdata[bpm_const][bp_const]/100*metacov + biases.get(part, 0)
    thiscov = max(1, around(thiscov))
    parts[part] = thiscov
    __randombp_G.total += thiscov
# end def
def randombp(body:cmp.Body, biases=None) -> object:
    ''' get a random body part from body body
        biases of form {BP_ instance : bonus_to_hit}
        Returns part
        ##tuple: (part_instance, instance_class,)
    '''
    __cov = __randombp_cov
    __G = __randombp_G
    __G.total=0
    parts={} # {part_instance : (chance,cls,),}
    bpdata=BPM_COVERAGE[body.plan]
    data=BODY_COVERAGE[body.plan]
    if not biases: biases={}
    
    # cores
    coretype=getcoretype(body.plan)
    if coretype==CORETYPE_TORSO:
        metacov = data[BPM_TORSO]
        __cov(parts,bpdata,biases,metacov,BPM_TORSO,BP_CORE,body.core.core)
        __cov(parts,bpdata,biases,metacov,BPM_TORSO,BP_HIPS,body.core.hips)
        __cov(parts,bpdata,biases,metacov,BPM_TORSO,BP_FRONT,body.core.front)
        __cov(parts,bpdata,biases,metacov,BPM_TORSO,BP_BACK,body.core.back)
    # end if
    
    # parts
    for cls,bpc in body.parts.items():
        if cls==cmp.BPC_Arms:
            for arm in bpc.arms:
                metacov=data[BPM_ARM]
                __cov(parts,bpdata,biases,metacov,BPM_ARM,BP_HAND,arm.hand)
                __cov(parts,bpdata,biases,metacov,BPM_ARM,BP_ARM,arm.arm)
        elif cls==cmp.BPC_Legs:
            for leg in bpc.legs:
                metacov=data[BPM_LEG]
                __cov(parts,bpdata,biases,metacov,BPM_LEG,BP_FOOT,leg.foot)
                __cov(parts,bpdata,biases,metacov,BPM_LEG,BP_LEG,leg.leg)
        elif cls==cmp.BPC_Heads:
            for head in bpc.heads:
                metacov=data[BPM_HEAD]
                __cov(parts,bpdata,biases,metacov,BPM_HEAD,BP_HEAD,head.head)
                __cov(parts,bpdata,biases,metacov,BPM_HEAD,BP_FACE,head.face)
                __cov(parts,bpdata,biases,metacov,BPM_HEAD,BP_EYES,head.eyes)
                __cov(parts,bpdata,biases,metacov,BPM_HEAD,BP_EARS,head.ears)
                __cov(parts,bpdata,biases,metacov,BPM_HEAD,BP_MOUTH,head.mouth)
                __cov(parts,bpdata,biases,metacov,BPM_HEAD,BP_NECK,head.neck)
    # end for
    
    # roll and select a part
    r = dice.roll(__G.total)
    last=0
    for part,chance in parts.items():
        if (r > last and r <= chance+last):
            return part
        last += chance
    raise Exception("randombp: failed to pick a body part")
# end def
# fit
def get_fit(ent, eq_type):
    ''' get the fit of a body part; assumes body part exists '''
    compo = _get_eq_compo(ent, eq_type)
    return compo.slot.fit # (doesn't get fit for held items...)
# grip
def get_grip(ent, eq_type):
    ''' UNFINISHED / UNTESTED / NOT WELL THOUGHT OUT
get grip of entity ent for bp indicated by EQ_ const eq_type
    Grip is not a stat. To get grip of a grabbing appendage,
        look at the body part. If armor equipped, look at armor grip value
        which is a variable of the equipable component.
    Grip does not exist for non-grabbing body parts.
        (To get how well a non-grabbing body part's armor fits, use get_fit())
    '''
    
    # **TODO**:
    # FINISH IMPLEMENTATION
    #   DO NOT: factor in grip of the held item (calculated separately??)
    #   figure out in general how to handle grip/fit, and write it all down.
    # should we use _get_eq_compo here? No. We need to do different things w/ different BP types.
    
    body = Rogue.world.component_for_entity(ent, cmp.Body)
    # find which one we want to check (match correct body part to eq_type)
    if (eq_type >= EQ_MAINHAND and eq_type < EQ_MAINHAND + MAXARMS):
        for i in range(MAXARMS): # for all EQ_ consts following EQ_MAINHAND...
            if (eq_type==(i + EQ_MAINHAND) or eq_type==(i + EQ_MAINHANDW)):
                _strmod = getms(ent, 'str')//MULT_STATS * ATT_STR_GRIP
                _dexmod = getms(ent, 'dex')//MULT_STATS * ATT_DEX_GRIP
                return around( _strmod + _dexmod + get_grip_hand(
                    body.parts[ent,cmp.BPC_Arms].arms[i].hand ) )
    elif (eq_type >= EQ_MAINFOOT and eq_type < EQ_MAINFOOT + MAXLEGS):
        for i in range(MAXLEGS):
            if eq_type==(i + EQ_MAINFOOT):
                _kgmod = getms(ent, 'mass')//MULT_MASS * MASS_GRIP
                _agimod = getms(ent, 'agi')//MULT_STATS * ATT_AGI_GRIP
                return around( _kgmod + _agimod + get_grip_foot(
                    body.parts[ent,cmp.BPC_Legs].legs[i].foot ) )
# end def
def get_grip_hand(bp):
    return _get_grip_bp(bp, cmp.EquipableInHandSlot)
def get_grip_foot(bp):
    return _get_grip_bp(bp, cmp.EquipableInFootSlot)
def get_grip_misc(bp):
    return
def _get_grip_bp(bp, cls):
    if bp.slot.item:
        return Rogue.world.component_for_entity(bp.slot.item, cls).grip
    return bp.grip
#

# body part lengths
def get_arm_length(bodyplan, height): #temporary solution to get arm length based on body type
    if bodyplan==BODYPLAN_HUMANOID:
        return around(height / 2.66667)


# inflict injury / wound / damage body part
def wound(ent: int, woundtype: int, tier: int) -> bool:
    '''
        (Try to) inflict a wound status upon an entity
        Since only one wound of each wound type can exist on one entity,
        we will ignore any wounds that are less significant than any
        existing wounds of that type.

        Return whether the entity was significantly wounded (tier of 
        wound increased or new wound status applied)

        Tier of wound indicates the Status quality -- minimum == 1
    '''
    world=Rogue.world
    if tier <= 0:
        return False
    woundcls = cmp.WOUND_TYPE_TO_STATUS[woundtype] # get StatusWound class corresponding to the wound type
    degrees = WOUNDS[woundtype]['degrees']
    wounded = False
    if world.has_component(ent, woundcls):
        # edit existing Wound status
        compo = world.component_for_entity(ent, woundcls)
        # compound wounds
        # 2 wounds of same class and same tier == 1 higher tier wound
        if (compo.quality == tier and compo.quality < degrees):
            tier += 1
            compo.quality += 1
            wounded = True
        # upgrade existing wound to new tier level
        elif (compo.quality < tier):
            compo.quality = min(tier, degrees)
            wounded = True
        else:
            wounded = False # compo.quality > tier, so ignore the wound
    else:
        # create a new Wound status
        world.add_component(ent, woundcls(tier))
        wounded = True
    if wounded:
        print("wound type: ", WOUNDS[woundtype]['type'])
        print("wound tier: ", tier)
        pos = world.component_for_entity(ent, cmp.Position)
        event_sight(pos.x,pos.y,"{} wounded ({})".format(
            gettitlename(ent), WOUNDS[woundtype][tier]['name']
            ))
    return wounded
    
def __damagebp(ent, bptarget, damage) -> int:
    ''' just damage HP of BP, changing status if necessary '''
    if damage <= 0:
        return
    pos = Rogue.world.component_for_entity(ent, cmp.Position)
    bptarget.hp -= damage
    if bptarget.hp <= -20:
        if bptarget.status != BPSTATUS_AMPUTATED:
            # TODO: handle creation of limb object
            # and logic for handling an amputated body part
            #   (hint: cannot use that body part for ANYTHING)
            #   (use bp.status to determine if crippled/amputated etc.)
            bptarget.status = BPSTATUS_AMPUTATED
            event_sight(pos.x,pos.y, "{}'s {} is dismembered".format(
                gettitlename(ent), cmp.BPNAMES[type(bptarget)]
                ))
    elif bptarget.hp <= 0:
        bptarget.hp = 0 # padding for dismemberment
        if bptarget.status == BPSTATUS_NORMAL:
            bptarget.status = BPSTATUS_CRIPPLED
            event_sight(pos.x, pos.y, "{}'s {} is crippled".format(
                gettitlename(ent), cmp.BPNAMES[type(bptarget)]
                ))
def damagebp(ent:int, bptarget:int, dmg:int, dmgtype:int, tier:int):
    '''
        ent        entity who owns the bp being targeted
        bptarget   BP_ (Body Part) component object instance to damage
        dmgtype    DMGTYPE_ const
        tier       damage value -- how high of a priority of
                    status is inflicted? 1 is least severe, 9 most.
                       - Tier may be altered in case of effective weapon
                           pairing i.e. blunt vs. bony or cut vs. fleshy BP.

        Damage the body part and possibly inflict a wound
    '''
    
    woundtype = None
    brainDmg = 1
    organDmg = 1
    
    if dmgtype==DMGTYPE_ABRASION: # rash
        woundtype = WOUND_RASH
        brainDmg = 0
        organDmg = 0
        if bptarget.SOFT_TARGET: dmg = dmg*1.5
    elif dmgtype==DMGTYPE_BURN: # burn
        woundtype = WOUND_RASH
        brainDmg = 0
        organDmg = 0
        if bptarget.SOFT_TARGET: dmg = dmg*2
    elif dmgtype==DMGTYPE_CUT: # cut
        woundtype = WOUND_CUT
        brainDmg = 0
        if bptarget.SOFT_TARGET:
            tier += 1
            dmg = dmg*3
    elif dmgtype==DMGTYPE_PIERCE: # pierce
        woundtype = WOUND_PUNCTURE
        brainDmg = 0
        if bptarget.SOFT_TARGET:
            tier += 1
            dmg = dmg*4
    elif dmgtype==DMGTYPE_HACK: # hack - axes
        # hack damage is very wounding
        dmg = dmg*2 if bptarget.SOFT_TARGET else dmg*4
        tier += 1
        if dice.roll(6) % 2 == 0: # cut damage
            if bptarget.SOFT_TARGET: tier += 1
            woundtype = WOUND_CUT
        else: # bruise damage
            if not bptarget.SOFT_TARGET: tier += 2
            woundtype = WOUND_MUSCLE
    elif dmgtype==DMGTYPE_BLUNT:
        dmg = dmg*2 if bptarget.BONES else dmg*0.75
        woundtype = WOUND_MUSCLE
        if not bptarget.SOFT_TARGET: tier += 2
    elif dmgtype==DMGTYPE_SPIKES:
        dmg = dmg*1.5 if bptarget.BONES else dmg*1
        if dice.roll(6) % 2 == 0: # puncture damage
            if bptarget.SOFT_TARGET: tier += 1
            woundtype = WOUND_PUNCTURE
        else: # bruise damage
            if not bptarget.SOFT_TARGET: tier += 2
            woundtype = WOUND_MUSCLE
    elif dmgtype==DMGTYPE_GUNSHOT:
        if bptarget.SOFT_TARGET: dmg *= 2
        woundtype = WOUND_GUNSHOT

    # deal HP damage
    dmg *= BP_DAMAGE_MULTIPLIER
    __damagebp(ent, bptarget, around(dmg))

    # attempt generic wound
    wound(ent, woundtype, tier)
    
    # attempt to wound organs and/or brains
    if (organDmg and bptarget.HAS_ORGANS):
        wound(ent, WOUND_ORGAN, tier - dice.roll(3))
    if (brainDmg and bptarget.HAS_BRAINS):
        wound(ent, WOUND_BRAIN, tier - dice.roll(2))
# end def

def attackbp(
    attkr:int,dfndr:int,bptarget:int,weap:int,dmg:int,skill_type:int,dmgtype=-1
    ):
    ''' entity attkr attacks dfndr's bp bptarget with weapon weap
        using skill skill_type and damage type dmgtype if !=-1
        Possibly inflict wounding and BP damage '''
    world=Rogue.world
    dmgIndex = 0 # wound amount (tier)

    # TODO: add randomness to dmgIndex
    
    if dmgtype==-1: # get damage type
        if (weap and world.has_component(weap, cmp.DamageTypeMelee)): # custom?
            compo=world.component_for_entity(weap, cmp.DamageTypeMelee)
            dmgIndex += compo.types[dmgtype]
            dmgtype = compo.default
        else: # damage type based on skill of the weapon by default
            if skill_type:
                dmgtype = DMGTYPES[skill_type]
                # increase wounding tier based on skill level
                skill_lv = getskill(attkr, skill_type)
                dmgIndex += 1 + math.floor(skill_lv*SKILL_LV_WOUND_MODIFIER)
            else: # no skill involved
                if weap: # default to blunt damage
                    dmgtype = DMGTYPE_BLUNT
                else: # use body damage type
                    if (attkr and world.has_component(attkr, cmp.DamageTypeMelee)):
                        compo=world.component_for_entity(attkr, cmp.DamageTypeMelee)
                        dmgtype = compo.default
                        dmgIndex += compo.types[dmgtype]
                    else: # default to blunt damage
                        dmgtype = DMGTYPE_BLUNT
    else: # force a damage type
        if (not weap or not world.has_component(weap, cmp.DamageTypeMelee)):
            dmgtype=DMGTYPE_BLUNT # default to blunt damage
        else: # make sure this weapon can use this damage type
            compo = world.component_for_entity(weap, cmp.DamageTypeMelee)
            if dmgtype in compo.types:
                dmgIndex += compo.types[dmgtype]
            else: # default to blunt damage
                dmgtype=DMGTYPE_BLUNT
            
    # end get damage type

    # increase damage index in cases of higher damage
    
    #  TESTING
    print("dmgIndex is ",dmgIndex)
    #
    
    # deal body damage
    # ent:int, bptarget:int, dmg:int, dmgtype:int, tier:int
    damagebp(dfndr, bptarget, dmg, dmgtype, dmgIndex)
    
# end if

# component getters / finders
def has_wearable_component(ent):
    ''' does entity have any "wearable" equipable components? '''
    for compo in cmp.WEARABLE_COMPONENTS:
        if Rogue.world.has_component(ent, compo):
            return True
    return False
def get_wearable_components(ent):
    ''' which "wearable" equipable components does the entity have? '''
    lis=set()
    for compo in cmp.WEARABLE_COMPONENTS.keys():
        if Rogue.world.has_component(ent, compo):
            lis.add(compo)
    return lis
def _get_eq_compo(ent, equipType):
    ''' from EQ_ const equipType, get entity's respective BP_ component '''
    body = Rogue.world.component_for_entity(ent, cmp.Body)
    
    #~~~# cores #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    # torso core
    if equipType==EQ_CORE:
        return body.core.core
    # torso front chest
    elif equipType==EQ_FRONT:
        return body.core.front
    # torso back
    elif equipType==EQ_BACK:
        return body.core.back
    # torso hips
    elif equipType==EQ_HIPS:
        return body.core.hips
    
    #~~~# peripherals #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    # arms
    for i in range(MAXARMS):
        # hands
        if (equipType==(i + EQ_MAINHAND) or equipType==(i + EQ_MAINHANDW)):
            arm = body.parts[cmp.BPC_Arms].arms[i]
            return arm.hand if arm else None
        # arms
        if equipType==(i + EQ_MAINARM):
            arm = body.parts[cmp.BPC_Arms].arms[i]
            return arm.arm if arm else None
    # legs
    for i in range(MAXLEGS):
        # feet
        if equipType==(i + EQ_MAINFOOT):
            leg = body.parts[cmp.BPC_Legs].legs[i]
            return leg.foot if leg else None
        # legs
        if equipType==(i + EQ_MAINLEG):
            leg = body.parts[cmp.BPC_Legs].legs[i]
            return leg.leg if leg else None
    # heads
    for i in range(MAXHEADS):
        # heads
        if equipType==(i + EQ_MAINHEAD):
            head = body.parts[cmp.BPC_Heads].heads[i]
            return head.head if head else None
        # faces
        if equipType==(i + EQ_MAINFACE):
            head = body.parts[cmp.BPC_Heads].heads[i]
            return head.face if head else None
        # necks
        if equipType==(i + EQ_MAINNECK):
            head = body.parts[cmp.BPC_Heads].heads[i]
            return head.neck if head else None
        # eyes
        if equipType==(i + EQ_MAINEYES):
            head = body.parts[cmp.BPC_Heads].heads[i]
            return head.eyes if head else None
        # ears
        if equipType==(i + EQ_MAINEARS):
            head = body.parts[cmp.BPC_Heads].heads[i]
            return head.ears if head else None
        # mouths
        if equipType==(i + EQ_MAINMOUTH):
            head = body.parts[cmp.BPC_Heads].heads[i]
            return head.mouth if head else None
    return None
#end def

# get body parts getbodyparts getbps findbodyparts find body parts
def findbps(ent, cls): # ent + cls -> list of BP component objects
    body = Rogue.world.component_for_entity(ent, cmp.Body)
    if cls is cmp.BP_TorsoCore:
        return (body.core.core,)
    if cls is cmp.BP_TorsoFront:
        return (body.core.front,)
    if cls is cmp.BP_TorsoBack:
        return (body.core.back,)
    if cls is cmp.BP_Hips:
        return (body.core.hips,)
    if cls is cmp.BP_Head:
        return tuple([(head.head if head else None) for head in body.parts[cmp.BPC_Heads].heads])
    if cls is cmp.BP_Face:
        return tuple([(head.face if head else None) for head in body.parts[cmp.BPC_Heads].heads])
    if cls is cmp.BP_Neck:
        return tuple([(head.neck if head else None) for head in body.parts[cmp.BPC_Heads].heads])
    if cls is cmp.BP_Eyes:
        return tuple([(head.eyes if head else None) for head in body.parts[cmp.BPC_Heads].heads])
    if cls is cmp.BP_Ears:
        return tuple([(head.ears if head else None) for head in body.parts[cmp.BPC_Heads].heads])
    if cls is cmp.BP_Nose:
        return tuple([(head.nose if head else None) for head in body.parts[cmp.BPC_Heads].heads])
    if cls is cmp.BP_Mouth:
        return tuple([(head.mouth if head else None) for head in body.parts[cmp.BPC_Heads].heads])
    if cls is cmp.BP_Arm:
        return tuple([(arm.arm if arm else None) for arm in body.parts[cmp.BPC_Arms].arms])
    if cls is cmp.BP_Hand:
        return tuple([(arm.hand if arm else None) for arm in body.parts[cmp.BPC_Arms].arms])
    if cls is cmp.BP_Leg:
        return tuple([(leg.leg if leg else None) for leg in body.parts[cmp.BPC_Legs].legs])
    if cls is cmp.BP_Foot:
        return tuple([(leg.foot if leg else None) for leg in body.parts[cmp.BPC_Legs].legs])
# end def

    #-----------------#
    #    Equipment    #
    #-----------------#

def list_equipment(ent):
    lis = []
    body = Rogue.world.component_for_entity(ent, cmp.Body)
    # core
    if body.plan==BODYPLAN_HUMANOID:
        lis.append(body.slot.item)
        lis.append(body.core.front.slot.item)
        lis.append(body.core.back.slot.item)
        lis.append(body.core.hips.slot.item)
        lis.append(body.core.core.slot.item)
    else:
        raise Exception # TODO: differentiate with different body types
    # parts
    for cls, part in body.parts.items():
        if type(part)==cmp.BPC_Arms:
            for arm in part.arms:
                lis.append(arm.hand.held.item)
                lis.append(arm.hand.slot.item)
                lis.append(arm.arm.slot.item)
        elif type(part)==cmp.BPC_Legs:
            for leg in part.legs:
                lis.append(leg.foot.slot.item)
                lis.append(leg.leg.slot.item)
        elif type(part)==cmp.BPC_Heads:
            for head in part.heads:
                lis.append(head.mouth.held.item)
                lis.append(head.head.slot.item)
                lis.append(head.face.slot.item)
                lis.append(head.neck.slot.item)
                lis.append(head.eyes.slot.item)
                lis.append(head.ears.slot.item)
    while None in lis:
        lis.remove(None)
    return lis

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
##    print("trying to equip {} to {}".format(fullname(item), fullname(ent)))
# init and failure checking #
    # first check that the entity can equip the item in the indicated slot.
    world = Rogue.world
    equipableConst = EQUIPABLE_CONSTS[equipType]
    eqcompo = _get_eq_compo(ent, equipType)
    holdtype=(equipType in cmp.EQ_BPS_HOLD) # holding type or armor type?

    if equipType==EQ_NONE:
        return (-100,None,) # NULL value for equip type
    if not world.has_component(item, equipableConst):
        return (-1,None,) # item can't be equipped in this slot
    if not eqcompo: # component selected. Does this component exist?
        return (-2,None,) # something weird happened
    if eqcompo.slot.covered:
        return (-3,None,) # already have something covering that slot
    if ( equipType==EQ_OFFHANDW and on(item, TWOHANDS)):
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
            if _com.slot.covered: # make sure you can't equip something if ...
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
        
##    print("successfully equipped {} to {}".format(fullname(item), fullname(ent)))

    # remove item from the map and from agent's inventory if applicable
    grid_remove(item)
    if item in getinv(ent):
        take(ent, item)
##        print("taken {} from {}".format(fullname(item), fullname(ent)))
    # indicate that the item is equipped using components
    world.add_component(item, cmp.Child(ent))
    if holdtype:
        world.add_component(item, cmp.Held(ent, equipType))
    else:
        world.add_component(item, cmp.Equipped(ent, equipType))
    if world.has_component(item, cmp.Fitted):
        fitted=world.component_for_entity(item, cmp.Fitted)
        if fitted.entity==ent:
            armorfit = FIT_ARMOR_MAX
            heldfit = FIT_HELD_MAX
        else:
            armorfit = 0
            diff = abs(fitted.height - getbase(ent,'height'))//2
            heldfit = 0.5*FIT_HELD_MAX - diff*(FIT_HELD_MAX/FIT_ARMOR_MAX)
    else:
        armorfit = 0
        heldfit = 0
    
    # put it in the right slot (held or worn?)
    if holdtype: # held
        eqcompo.held.item = item
        eqcompo.held.fit = heldfit
# todo: function that adds these values to get how well you're gripping something.
    else: # worn
        eqcompo.slot.item = item
        eqcompo.slot.fit = armorfit
    
    eqcompo.slot.covered = True # cover this BP
    
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
        _com.slot.covered=True
    #
    
    make(ent, DIRTY_STATS)
    return (1,equipable,) # yey success
    
# end def

def remove_equipment(ent, item):
    ''' dewield or deequip (context sensitive) '''
    world = Rogue.world
    if world.has_component(item, cmp.Equipped):
        equipType=world.component_for_entity(item,cmp.Equipped).equipType
        deequip(ent, equipType)
    elif world.has_component(item, cmp.Held):
        equipType=world.component_for_entity(item,cmp.Held).equipType
        dewield(ent, equipType)
        
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
                _dewield(ent, head.mouth)
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
    for cc in compo.slot.covers:
        cc.slot.covered = False
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
    slot.fit = 0
    give(ent, item) # put item in inventory
    
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
    world.remove_component(item, cmp.Held)
    compo.held.covered = False
    compo.held.item = None
    compo.held.fit = 0
    give(ent, item) # put item in inventory
    
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
def create_weapon(name,x,y,cond=1,mat=None):
    ent=entities.create_weapon(name,x,y,condition=cond,mat=mat)
    _initThing(ent)
    return ent
def create_armor(name,x,y,cond=1,mat=None):
    ent=entities.create_armor(name,x,y,condition=cond,mat=mat)
    _initThing(ent)
    return ent
def create_legwear(name,x,y,cond=1,mat=None):
    ent=entities.create_legwear(name,x,y,condition=cond,mat=mat)
    _initThing(ent)
    return ent
def create_armwear(name,x,y,cond=1,mat=None):
    ent=entities.create_armwear(name,x,y,condition=cond,mat=mat)
    _initThing(ent)
    return ent
def create_footwear(name,x,y,cond=1,mat=None):
    ent=entities.create_footwear(name,x,y,condition=cond,mat=mat)
    _initThing(ent)
    return ent
def create_headwear(name,x,y,cond=1,mat=None):
    ent=entities.create_headwear(name,x,y,condition=cond,mat=mat)
    _initThing(ent)
    return ent
def create_neckwear(name,x,y,cond=1,mat=None):
    ent=entities.create_neckwear(name,x,y,condition=cond,mat=mat)
    _initThing(ent)
    return ent
def create_facewear(name,x,y,cond=1,mat=None):
    ent=entities.create_facewear(name,x,y,condition=cond,mat=mat)
    _initThing(ent)
    return ent
def create_eyewear(name,x,y,cond=1,mat=None):
    ent=entities.create_eyewear(name,x,y,condition=cond,mat=mat)
    _initThing(ent)
    return ent
def create_earwear(name,x,y,cond=1,mat=None):
    ent=entities.create_earwear(name,x,y,condition=cond,mat=mat)
    _initThing(ent)
    return ent

def create_body_humanoid(kg=70, cm=175, female=False, bodyfat=None):
    if bodyfat:
        return entities.create_body_humanoid(
            kg=kg, cm=cm, female=female, bodyfat=bodyfat)
    else:
        return entities.create_body_humanoid(
            kg=kg, cm=cm, female=female)

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
        # prompt for item equipped in various body parts
def is_wielding_mainhand(ent) -> bool:
    marm = dominant_arm(ent)
    if (not marm or not marm.hand.held.item):
        return False
    return True

def homeostasis(ent): entities.homeostasis(ent)
def metabolism(ent, hunger, thirst=1): entities.metabolism(ent, hunger, thirst) # metabolize
def stomach(ent): entities.stomach(ent)
def starve(ent): entities.starve(ent)
def dehydrate(ent): entities.dehydrate(ent)

# ranged weapon management / reloading
def ranged_ammo_load(rweap:int, ammo_to_load:tuple):
    compo = Rogue.world.component_for_entity(rweap, cmp.Shootable)
    loaded = compo.ammo
    if len(loaded) >= compo.stats['capacity']:
        return False
    if not Rogue.world.has_component(rweap, cmp.Ammo):
        return False
    ammocompo = Rogue.world.component_for_entity(rweap, cmp.Ammo)
    if not ammocompo.type in compo.ammoTypes:
        return False
    loaded.append(ammo_to_load)
    return True
def ranged_action_auto(rweap:int):
    compo = Rogue.world.component_for_entity(rweap, cmp.Shootable)
    ammo = compo.ammo.pop(0)
    # create used cartridge
    return ammo
def ranged_action_bolt(rweap:int):
    compo = Rogue.world.component_for_entity(rweap, cmp.Shootable)
    ammo = compo.ammo[0]
    # replace ammo with a used cartridge
##    compo.ammo[0] = ...
    return ammo
def ranged_eject_ammo(rweap:int):
    pos = getpos(rweap)
    compo = Rogue.world.component_for_entity(rweap, cmp.Shootable)
    for ammo in compo.ammo:
        port(ammo, pos.x,pos.y)
    compo.ammo = []
def ranged_attach_mod(rweap:int, mod:int, mod_type:int):
    compo = Rogue.world.component_for_entity(rweap, cmp.Moddable)
    if not compo.mods.get(mod_type, None): return False
    compo.mods[mod_type] = mod # MOD_ const : mod_instance
    modcompo = Rogue.world.component_for_entity(rweap, cmp.Mod)
    for k,v in modcompo.mods.items():
        compo.stats[k] += v
    # special cases -- flashlights ? Suppressors ?
      # Should these be handled differently?
    return True
def ranged_remove_mod(rweap:int, mod:int, mod_type:int):
    compo = Rogue.world.component_for_entity(rweap, cmp.Moddable)
    if not compo.mods.get(mod_type, None): return None
    mod = compo.mods[mod_type]
    compo.mods[mod_type] = None
    modcompo = Rogue.world.component_for_entity(rweap, cmp.Mod)
    for k,v in modcompo.mods.items():
        compo.stats[k] -= v
    # special cases removal
    return mod

           

    #--------------#
    #     Stats    #
    #--------------#

# attributes
def att_str_mult_force(_str: int) -> float:
    return ATT_STR_FORCEMULT * _str # + 1

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

def _update_from_limbweapon(modded, wp_id):
    ''' add stats from LIMBWEAPONS dict '''
    data = entities.LIMBWEAPONS.get(wp_id, {})
    if not data: return
    modded.atk += entities.get_limbweapon_atk(data)
    modded.dmg += entities.get_limbweapon_dmg(data)
    modded.pen += entities.get_limbweapon_pen(data)
    modded.gra += entities.get_limbweapon_gra(data)
    modded.dfn += entities.get_limbweapon_dfn(data)
    modded.arm += entities.get_limbweapon_arm(data)
    modded.pro += entities.get_limbweapon_pro(data)
    modded.asp += entities.get_limbweapon_asp(data)
# end def
def _update_from_wield(modded, equip):
    ''' apply addMods from weapon item, modify stats based on
        any attribute insufficiencies. Wielded equipment only.
        equip: entities.__EQ instance
    '''
    for k,v in equip.addMods.items():
        modded.__dict__[k] = v + modded.__dict__[k]
    # Strength Requirement and penalties | insufficient strength penalty
    strd = equip.strReq - modded.str//MULT_STATS
    if strd > 0:
        # Multiply gear's enc. by ratio based on missing STR
        modded.enc += equip.enc * strd * 0.1
        modded.dfn -= strd*INSUFF_STR_DFN_PENALTY*MULT_STATS
        modded.arm -= strd*INSUFF_STR_ARM_PENALTY*MULT_STATS
        modded.pro -= strd*INSUFF_STR_PRO_PENALTY*MULT_STATS
        # weapon-specific stats
        modded.dmg -= strd*INSUFF_STR_DMG_PENALTY*MULT_STATS
        modded.atk -= strd*INSUFF_STR_ATK_PENALTY*MULT_STATS
        modded.pen -= strd*INSUFF_STR_PEN_PENALTY*MULT_STATS
        modded.gra -= strd*INSUFF_STR_GRA_PENALTY*MULT_STATS
        modded.asp -= strd*INSUFF_STR_ASP_PENALTY
        modded.tatk -= strd*INSUFF_STR_ATK_PENALTY*MULT_STATS
        modded.tpen -= strd*INSUFF_STR_PEN_PENALTY*MULT_STATS
        modded.tdmg -= strd*INSUFF_STR_DMG_PENALTY*MULT_STATS
        modded.trng = (1 - strd*INSUFF_STR_RNG_PENALTY)*modded.trng
    # Dexterity Requirement and penalties | insufficient dexterity penalty
    dexd = equip.dexReq - modded.dex//MULT_STATS
    if dexd > 0:
        modded.dfn -= dexd*INSUFF_DEX_DFN_PENALTY*MULT_STATS
        # weapon-specific stats
        modded.dmg -= dexd*INSUFF_DEX_DMG_PENALTY*MULT_STATS
        modded.atk -= dexd*INSUFF_DEX_ATK_PENALTY*MULT_STATS
        modded.pen -= dexd*INSUFF_DEX_PEN_PENALTY*MULT_STATS
        modded.gra -= dexd*INSUFF_DEX_GRA_PENALTY*MULT_STATS
        modded.asp -= dexd*INSUFF_DEX_ASP_PENALTY
        modded.tatk -= dexd*INSUFF_DEX_ATK_PENALTY*MULT_STATS
        modded.tpen -= dexd*INSUFF_DEX_PEN_PENALTY*MULT_STATS
        modded.tdmg -= dexd*INSUFF_DEX_DMG_PENALTY*MULT_STATS
        modded.trng = (1 - dexd*INSUFF_DEX_RNG_PENALTY)*modded.trng
# end def
def _update_from_armor(modded, equip):
    ''' apply addMods from non-weapon equipment item, modify stats
        based on strength insufficiency. (Dex doesn't affect worn armor.)
        equip: entities.__EQ instance
    '''
    for k,v in equip.addMods.items():
        modded.__dict__[k] = v + modded.__dict__[k]
    # Strength Requirement and penalties | insufficient strength penalty
    strd = equip.strReq - modded.str//MULT_STATS
    if strd > 0:
        # Multiply gear's enc. by ratio based on missing STR
        modded.enc += equip.enc * strd * 0.1
        modded.dfn -= strd*INSUFF_STR_DFN_PENALTY*MULT_STATS
        modded.arm -= strd*INSUFF_STR_ARM_PENALTY*MULT_STATS
        modded.pro -= strd*INSUFF_STR_PRO_PENALTY*MULT_STATS
# end def

def _update_stats(ent): # PRIVATE, ONLY TO BE CALLED FROM getms(...)
    ''' calculate modified stats (ModdedStats component)
            building up from scratch (base stats from Stats component)
            add any modifiers from equipment, status effects, etc.
        return the ModdedStats component
        after this is called, you can access the ModdedStats component
            and it will contain the right value, until something significant
            updates which would change the calculation, at which point the
            DIRTY_STATS flag for that entity must be set to True.
        NOTE: this and ModdedStats component are private.
            Use the public interface "getms" to access modified stats.
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
    # throwing stats
    modded.tatk=modded.tdmg=modded.tpen=modded.tasp=modded.trng=0
    # range stats
    modded.ratk=modded.rdmg=modded.rpen=modded.rasp=modded.minrng=modded.maxrng=0
    # resistances
    modded.insul=modded.respain=0
    modded.cou=modded.reswet=modded.resbleed=modded.resrust=modded.resrot=0
    
    
    # useful stats to keep track of
    basekg = base.mass / MULT_MASS
# /init #--------------------------------------------------------------#


#~~~~~~~#-------------------------#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
        # Get Body Data / Equips  #
        #  - Do not apply yet. -  #
        #-------------------------#
    
    if world.has_component(ent, cmp.Body):
        # body component top level vars
        body = world.component_for_entity(ent, cmp.Body)
        keys = body.parts.keys()
        # get stats from body component
        bodymass = entities._update_from_body_class(body, modded)
            # (modded mass now represents true body mass)
        basekg = modded.mass / MULT_MASS
        # add encumerance from your own body mass
        modded.enc += basekg
        
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
    if world.has_component(ent, cmp.Inventory):
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
        if (not on(ent, IMMUNEPAIN) and world.has_component(ent, cmp.FeelsPain)):
            compo = world.component_for_entity(ent, cmp.FeelsPain)
            q=0
            for _q, dec in PAIN_QUALITIES.items():
                if compo.pain >= MAX_PAIN*dec:
                    q=_q
            overwrite_status(ent, cmp.StatusPain, q=q)
        
        # bleed
        if (not on(ent, IMMUNEBLEED) and world.has_component(ent, cmp.Bleeds)):
            compo = world.component_for_entity(ent, cmp.Bleeds)
            q = compo.bleed // (0.5*basekg)
            overwrite_status(ent, cmp.StatusBleed, q=q)
        
        # dirty
        if world.has_component(ent, cmp.Dirties):
            compo = world.component_for_entity(ent, cmp.Dirties)
            q=0
            for _q, dec in DIRT_QUALITIES.items():
                if compo.dirt >= MAX_DIRT*dec:
                    q=_q
            overwrite_status(ent, cmp.StatusDirty, q=q)
        
        # wet
        if (not on(ent, IMMUNEWATER) and world.has_component(ent, cmp.Wets)):
            compo = world.component_for_entity(ent, cmp.Wets)
            q = compo.wet // (MULT_MASS//100) # every 10g (is this too many g?)
            overwrite_status(ent, cmp.StatusWet, q=q)
        
        # rust
            # TODO: rust status affecting stats
        if world.has_component(ent, cmp.Rusts):
            compo = world.component_for_entity(ent, cmp.Rusts)
            q=0
            for _q, dec in RUST_QUALITIES.items():
                if compo.rust >= MAX_RUST*dec:
                    q=_q
            overwrite_status(ent, cmp.StatusRusted, q=q)
        
        # rot
            # TODO: rot status affecting stats
        if world.has_component(ent, cmp.Rots):
            compo = world.component_for_entity(ent, cmp.Rots)
            q=0
            for _q, dec in ROT_QUALITIES.items():
                if compo.rot >= MAX_ROT*dec:
                    q=_q
            overwrite_status(ent, cmp.StatusRotted, q=q)

        # fear
        # sickness
    # end if


    
#~~~~~~~#------------~~~~~~~~~~~~~~~~~~~~~#~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
        # components  #
        #---------------------------------#




    
    
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

        # wounds #
        # These are general wounds that affect stats in a generic way.
        #   For specific injury to body parts / bones, see the section
        #   titled "Get Body Data / Equips"
    # rash wounds
    if world.has_component(ent, cmp.StatusWound_Rash):
        compo = world.component_for_entity(ent, cmp.StatusWound_Rash)
        data = WOUNDS[WOUND_RASH][compo.quality]
        modded.resbio += data.get('resbio',0)
        modded.respain += data.get('respain',0)
        modded.resbleed += data.get('resbleed',0)
        modded.resfire += data.get('resfire',0)
        modded.rescold += data.get('rescold',0)
    # burn wounds
    if world.has_component(ent, cmp.StatusWound_Burn):
        compo = world.component_for_entity(ent, cmp.StatusWound_Burn)
        data = WOUNDS[WOUND_BURN][compo.quality]
        modded.resbio += data.get('resbio',0)
        modded.respain += data.get('respain',0)
        modded.resbleed += data.get('resbleed',0)
        modded.resfire += data.get('resfire',0)
        modded.rescold += data.get('rescold',0)
        modded.str += data.get('str',0)*MULT_ATT
    # cut wounds
    if world.has_component(ent, cmp.StatusWound_Cut):
        compo = world.component_for_entity(ent, cmp.StatusWound_Cut)
        data = WOUNDS[WOUND_CUT][compo.quality]
        modded.resbio += data.get('resbio',0)
        modded.respain += data.get('respain',0)
        modded.resbleed += data.get('resbleed',0)
        modded.gra += data.get('gra',0)*MULT_STATS
    # puncture wounds
    if world.has_component(ent, cmp.StatusWound_Puncture):
        compo = world.component_for_entity(ent, cmp.StatusWound_Puncture)
        data = WOUNDS[WOUND_PUNCTURE][compo.quality]
        modded.resbio += data.get('resbio',0)
        modded.respain += data.get('respain',0)
        modded.resbleed += data.get('resbleed',0)
    # gunshot wounds
    if world.has_component(ent, cmp.StatusWound_Gunshot):
        compo = world.component_for_entity(ent, cmp.StatusWound_Gunshot)
        data = WOUNDS[WOUND_GUNSHOT][compo.quality]
        modded.resbio += data.get('resbio',0)
        modded.respain += data.get('respain',0)
        modded.resbleed += data.get('resbleed',0)
    # muscle wounds (bruises, strains, tears, etc.)
    if world.has_component(ent, cmp.StatusWound_Muscle):
        compo = world.component_for_entity(ent, cmp.StatusWound_Muscle)
        data = WOUNDS[WOUND_MUSCLE][compo.quality]
        modded.atk += data.get('atk',0)*MULT_STATS
        modded.dfn += data.get('dfn',0)*MULT_STATS
        modded.gra += data.get('gra',0)*MULT_STATS
        modded.respain += data.get('respain',0)
        modded.msp *= data.get('msp',0) # multipliers
        modded.asp *= data.get('asp',0)
        modded.str *= data.get('str',0)*MULT_ATT
    # organ wounds (internal organ damage or failure)
    if world.has_component(ent, cmp.StatusWound_Organ):
        compo = world.component_for_entity(ent, cmp.StatusWound_Organ)
        data = WOUNDS[WOUND_ORGAN][compo.quality]
        modded.end += data.get('end',0)*MULT_ATT
        modded.con += data.get('con',0)*MULT_ATT
        modded.respain += data.get('respain',0)
        modded.resbleed += data.get('resbleed',0)
    # brain injury / brain damage
    if world.has_component(ent, cmp.StatusWound_Brain):
        compo = world.component_for_entity(ent, cmp.StatusWound_Brain)
        data = WOUNDS[WOUND_BRAIN][compo.quality]
        modded.int *= data.get('int',0) # multipliers
        modded.bal *= data.get('bal',0)
        modded.agi *= data.get('agi',0)
        modded.dex *= data.get('dex',0)
    
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
        modded.cou += _con * ATT_CON_COURAGE

    
#~~~~~~~~~~~#------------------------#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
            #   Equipment Add Mods   #
            #------------------------#
            # ** After Attributes have been calculated.
            # (b/c strReq/dexReq)
    
    # apply mods -- addMods
    for bps in bpdata:
        # body part mod dict (other than equipment stat mods)
        for k,v in bps.addMods.items():
            modded.__dict__[k] = v + modded.__dict__[k]
        # equipment
        if bps.armor: # worn
            _update_from_armor(modded, bps.armor)
        if bps.wield: # held/weapon # TEST!
            _update_from_wield(modded, bps.wield)
        elif bps.limbweapon: # pseudo-weapon from BP # TEST!
            _update_from_limbweapon(modded, bps.limbweapon)
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
        
    # KO
    if world.has_component(ent, cmp.StatusKO):
        modded.spd = modded.spd * KO_SPDMOD
        
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
    # flanked
    if world.has_component(ent, cmp.StatusFlanked):
        status=world.component_for_entity(ent, cmp.StatusFlanked)
        modded.dfn = modded.dfn - compo.quality*MULT_STATS 
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
    
    
#~~~~~~~#--------------#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
        # encumberance #
        #--------------#
    
    #~
    # Things should avoid affecting attributes as much as possible.
    # Encumberance should not affect agility or any other attribute
    # because encumberance max is dependent on attributes.
    #~
    
    # Ratio of encumberance
    encpc = max(0, 1 - (modded.enc / max(1,modded.encmax)))
    # SP Regen acts differently -- inverse quadratic scaling relative to encumberance
    modded.mpregen = _get_encsp(modded.enc, modded.encmax, modded.mpregen)
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
        
#~~~~~~~#---------#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
        # fatigue #
        #---------#
    
    # having a low % of Stamina affects your derived stats.
    if modded.mp < modded.mpmax:
        fatigue_modf = 1 - modded.mp / modded.mpmax
        modded.dfn -= fatigue_modf * FATIGUE_PENALTY_DFN * MULT_STATS
        modded.gra -= fatigue_modf * FATIGUE_PENALTY_GRA * MULT_STATS
        modded.ctr -= fatigue_modf * FATIGUE_PENALTY_CTR * MULT_STATS
        modded.bal -= fatigue_modf * FATIGUE_PENALTY_BAL * MULT_STATS
        modded.pro -= fatigue_modf * FATIGUE_PENALTY_PRO * MULT_STATS
        modded.pen -= fatigue_modf * FATIGUE_PENALTY_PEN * MULT_STATS
        modded.tpen -= fatigue_modf * FATIGUE_PENALTY_TPEN * MULT_STATS
        modded.rpen -= fatigue_modf * FATIGUE_PENALTY_RPEN * MULT_STATS
        modded.atk -= fatigue_modf * FATIGUE_PENALTY_ATK * MULT_STATS
        modded.tatk -= fatigue_modf * FATIGUE_PENALTY_TATK * MULT_STATS
        modded.ratk -= fatigue_modf * FATIGUE_PENALTY_RATK * MULT_STATS
        modded.msp -= fatigue_modf * FATIGUE_PENALTY_MSP
        modded.asp -= fatigue_modf * FATIGUE_PENALTY_ASP
        modded.tasp -= fatigue_modf * FATIGUE_PENALTY_TASP
        modded.rasp -= fatigue_modf * FATIGUE_PENALTY_RASP
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
        if bps.armor:
            for k,v in bps.armor.multMods.items():
                if modded.__dict__[k] > 0:
                    modded.__dict__[k] = v * modded.__dict__[k]
        if bps.wield:
            for k,v in bps.wield.multMods.items():
                if modded.__dict__[k] > 0:
                    modded.__dict__[k] = v * modded.__dict__[k]
    
    # round values
    for k,v in modded.__dict__.items():
        modded.__dict__[k] = around(v)

    # cap values at their limits
    caphp(ent)
    capmp(ent)
    capres(ent)

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

def get_status(ent, statuscompo): #getstatus #status_get
    if Rogue.world.has_component(ent, statuscompo):
        return Rogue.world.component_for_entity(ent, statuscompo)
    else:
        return None
def set_status(ent, statuscompo, t=-1, q=None, target=None):
    '''
        # ent       = Thing object to set the status for
        # statuscompo   = status class (not an object instance)
        # t         = duration (-1 is the default duration for that status)
        # q         = quality (for specific statuses)
        # target    = entity target (for targeted statuses)
    '''
    proc.Status.add(ent, statuscompo, t, q, target)
def clear_status(ent, statuscompo):
    proc.Status.remove(ent, statuscompo)
def clear_status_all(ent):
    proc.Status.remove_all(ent)
def overwrite_status(ent, statuscompo, t=-1, q=1):
    ''' set or clear status depending on q / t
        overwrite existing status
    '''
    if (q and t!=0):
        status=get_status(ent, statuscompo)
        if status:
            clear_status(ent, statuscompo)
        set_status(ent, statuscompo, t=t, q=q)
    else:
        clear_status(ent, statuscompo)
def compound_status(ent, statuscompo, t=-1, q=1):
    ''' increment quality of a given status '''
    if (q and t!=0):
        status=get_status(ent, statuscompo)
        if status:
            nq = q + status.quality
            clear_status(ent, statuscompo)
        else:
            nq = q
        set_status(ent, statuscompo, t=t, q=nq)
# end def
  
    # non-elemental statuses #
    
    # standard statuses
def knockout(ent, t = 32):
    set_status(ent, cmp.StatusKO, t=t)
    # quality-based statuses
def flank(ent, q: int): # TODO: call this when you attack a creature
    compound_status(ent, cmp.StatusFlanked, q=q)
    
    # elemental damage #
    
# RECursively apply ELEMent to all items touching/held/carried by the entity
def recelem(ent, func, dmg, *args, **kwargs):
    # apply to inventory items
    inv=Rogue.world.component_for_entity(ent, cmp.Inventory).data
##    invres=... # inventory resistance. Should backpack be a separate entity w/ its own inventory? Inventories combine into one?
    for item in inv:
        func(item, dmg, *args, **kwargs)
    # apply to the entity itself
    return func(ent, dmg, *args, **kwargs)
# INTENDED SYNTAX: (TODO: test to make sure this works before applying to all elements.)
def NEWburn(ent, dmg, maxTemp=999999):
    return recelem(ent, entities.burn, dmg, maxTemp)

def settemp(ent, temp):
    Rogue.world.component_for_entity(ent, cmp.Meters).temp = temp
def burn(ent, dmg):
    return entities.burn(ent, dmg)
def frost(ent, dmg):
    return entities.cool(ent, dmg)
def ctemp(ent, dmg, minTemp=-300, maxTemp=999999):
    return entities.change_temp(ent, dmg, minTemp, maxTemp)
def bleed(ent, dmg):
    return entities.bleed(ent, dmg)
def scare(ent, dmg):
    return entities.scare(ent, dmg)
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

# pseudo-statuses

def anger(ent, offender, amt):
    compo = world.component_for_entity(ent, cmp.GetsAngry)
    compo.anger += amt
    if compo.anger >= MAX_ANGER:
        compo.anger = 0 # reset "meter"
        set_status(ent, cmp.StatusAngry, target=offender, t=64)

def taunt(ent:int):
    world.add_component(ent, cmp.Taunted())
    

    #-----------#
    #  actions  #
    #-----------#

def queue_action(ent, act):
    pass
    #Rogue.c_managers['actionQueue'].add(obj, act)




    #-----------#
    # Character #
    #-----------#

# gender name and pronouns
def get_gender_id(ent): # gender ID
    return Rogue.world.component_for_entity(ent, cmp.Gender).gender
def get_gender(ent): # gender name
    gender=Rogue.world.component_for_entity(ent, cmp.Gender).gender
    return _get_gender_name(gender)
def get_pronouns(ent): # gender pronouns
    gender=Rogue.world.component_for_entity(ent, cmp.Gender).gender
    return _get_pronouns(gender)
def get_pronoun_subject(ent): # "he, she", etc.
    return _get_pronoun_subject(get_pronouns(ent))
def get_pronoun_object(ent): # "him, her", etc.
    return _get_pronoun_object(get_pronouns(ent))
def get_pronoun_possessive(ent): # "his, her", etc.
    return _get_pronoun_possessive(get_pronouns(ent))
def get_pronoun_possessive2(ent): # "his, "hers", etc.
    return _get_pronoun_possessive2(get_pronouns(ent))
def get_pronoun_generic(ent): # "man, woman", etc.
    return _get_pronoun_generic(get_pronouns(ent))
def get_pronoun_polite(ent): # "sir, madam", etc.
    return _get_pronoun_polite(get_pronouns(ent))
def get_pronoun_informal(ent): # "guy, girl", etc.
    return _get_pronoun_informal(get_pronouns(ent))
def _get_pronoun_subject(pronouns): return pronouns[0]
def _get_pronoun_object(pronouns): return pronouns[1]
def _get_pronoun_possessive(pronouns): return pronouns[2]
def _get_pronoun_possessive2(pronouns): return pronouns[3]
def _get_pronoun_generic(pronouns): return pronouns[4]
def _get_pronoun_polite(pronouns): return pronouns[5]
def _get_pronoun_informal(pronouns): return pronouns[6]
def _get_gender_name(gender): return GENDERS[gender][0]
def _get_pronouns(gender): return GENDERS[gender][1]





    #----------#
    # managers #
    #----------#

# manager listeners
class Manager_Listener: # listens for a result from a game state Manager.
    def alert(self, result): # after we get a result, purpose is finished.
        manager_listeners_remove(self) # delete the reference to self.
class Aim_Manager_Listener(Manager_Listener):
    def __init__(self, world, caller, shootfunc, *args, **kwargs):
        self.world=world
        self.caller=caller      # entity who is calling the shootfunc
        self.shootfunc=shootfunc # function that runs when you select viable target
        self.arglist=args     # arguments for the shootfunc function
        self.kwarglist=kwargs # keyword arguments "
    def alert(self, result):
        if type(result) is int: # we have an entity target
##            print(self.arglist)
##            print(self.kwarglist)
            self.shootfunc(
                self.caller, result,
                *self.arglist, **self.kwarglist
                )
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
    
def aim_find_target(xs, ys, selectfunc, *args, **kwargs):
    # selectfunc: the function that is ran when you select a valid target
    clear_active_manager()
    game_set_state("manager") #move view
    Rogue.manager=managers.Manager_AimFindTarget(
        xs, ys, Rogue.view, Rogue.map.get_map_state())
    Rogue.view.fixed_mode_disable()
    # listener -- handles the shooting
    listener = Aim_Manager_Listener(
        world(), Rogue.pc, selectfunc, *args, **kwargs)
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
    strng   = misc.render_charpage_string(
        width, height, Rogue.pc, get_turn(), dlvl()
        )
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
def prompt(x,y, w,h, maxw=1, q='', default='',mode='text',insert=False,border=0,wrap=True):
    #libtcod.console_clear(con_final())
    dbox(x,y,w,h,text=q,
        wrap=wrap,border=border,con=con_final(),disp='mono')
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
    
def get_wear_type(ent, item): #TEST!
    '''
        using menus, get BP (e.g. hand 2) and convert into the actual component object
            to be used to equip entity item to entity ent, then get/return EQ_ const
        1. pick the category of equipping from possible equip types the item has
        2. for the entity ent (return e.g. a BP_Hand component)
            for each bp the entity ent has that matches the type chosen*,
                store "name #" where # is the bp index starting from 1.
                Increment the WEAR_TYPE of the matching component with i
                (the index) in order to get the appropriate EQ_ const value.
            *This works because the values are consecutive in const.py.
        return EQ_ const
    '''
    #
    # 1. choose a BP name (hand, head, leg, etc.)
    #   that matches a valid equippable type for item item
    _menu={}
    for equippableCompo in get_wearable_components(item):
        name = cmp.WEARABLE_COMPONENTS[equippableCompo]
        _menu[name] = equippableCompo
    if len(_menu.keys()) == 0: # cannot be equipped anywhere
        alert("This {} cannot be equipped.".format(fullname(item)))
        return EQ_NONE
    opt = menu("wear it where?", 0,0,_menu.keys())
    bpname = opt
    #
    # 2. get the BP object from list of BPs
    #   from entity ent that match the chosen name
    # TODO: handle "about" slot differently. Goes in Body slot. Just put an "if" statement.
    _menu={}
    i = 0
    bps = findbps(ent, cmp.BPNAMES_TO_CLASSES[bpname])
    for compo in bps:
        _menu["{} {}".format(bpname, i+1)] = compo.WEAR_TYPE + i
        i += 1
    if len(_menu.keys()) == 0: # cannot be equipped to entity
        alert("You cannot equip this {}.".format(fullname(item)))
        return EQ_NONE
    opt = menu("which {}?".format(bpname), 0,0,_menu.keys())
    result = _menu[opt]
    #
    return result
# end def










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
