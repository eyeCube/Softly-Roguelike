'''
    rogue.py
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
EQ_MAINHAND : cmp.EquipableInHoldSlot,
EQ_OFFHAND  : cmp.EquipableInHoldSlot,
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
    
    @classmethod
    def run_endTurn_managers(cls, pc):
        for v in cls.et_managers.values():
            v.run(pc)
    @classmethod
    def run_beginTurn_managers(cls, pc):
        for v in cls.bt_managers.values():
            v.run(pc)
    
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
            # after all changes have been made
        cls.world.add_processor(proc.GUIProcessor(), 71)
            # AI function (entity turns)
        cls.world.add_processor(proc.ActorsProcessor(), 50)

    @classmethod
    def create_perturn_managers(cls):
        '''
            constant, per-turn managers, ran each turn
        '''
        #ran at beginning of turn
            # (No managers run at beginning of turn currently.)
            
        #ran at end of turn (before player turn -- player turn is the very final thing to occur on any given turn)
        cls.et_managers.update({'sounds' : managers.Manager_SoundsHeard()})
        cls.et_managers.update({'sights' : managers.Manager_SightsSeen()})
    
    @classmethod
    def create_const_managers(cls):
        '''
            constant managers, manually ran
        '''
##        cls.c_managers.update({'sights' : managers.Manager_SightsSeen()})
##        cls.c_managers.update({'sounds' : managers.Manager_SoundsHeard()})
        cls.c_managers.update({'events' : managers.Manager_Events()})
        cls.c_managers.update({'lights' : managers.Manager_Lights()})
        cls.c_managers.update({'fov' : managers.Manager_FOV()})
        
        
'''
WHAT DO WE DO WITH THESE MANAGERS????
    FOV and ActionQueue is now a processor.... Events?????
    Rogue.c_managers.update({'events'     : managers.Manager_Events()})

'''

    # EXPIRED: Environment class
#/Rogue


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
def logNewEntry():
    Rogue.log.drawNew()
def msg(txt, col=None):
    if col is None: #default text color
        col=COL['white']
    Rogue.log.add(txt, str(get_turn()) )
def msg_clear():
    clr=libtcod.console_new(msgs_w(), msgs_h())
    libtcod.console_blit(clr, 0,0, msgs_w(),msgs_h(),  con_game(), 0,0)
    libtcod.console_delete(clr)

# game data
def dlvl():             return Rogue.data.dlvl() #current dungeon level of player
def level_up():         Rogue.data.dlvl_update(Rogue.data.dlvl() + 1)
def level_down():       Rogue.data.dlvl_update(Rogue.data.dlvl() - 1)
def level_set(lv):      Rogue.data.dlvl_update(lv)

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
def map(z = -99):
    # TODO: code for loading / unloading levels into the map
    if z == -99:
        z = dlvl()
    if dlvl() == z:
        return Rogue.map
    else:
        # unload current map from Rogue.map into the levels dict
        # load new map into Rogue.map from the levels dict
        # update dlvl
        level_set(z)
        return Rogue.map
def tile_get(x,y):          return Rogue.map.get_char(x,y)
def tile_change(x,y,char):
    updateNeeded=Rogue.map.tile_change(x,y,char)
    if updateNeeded:
        update_all_fovmaps()
def map_reset_lighting():   Rogue.map.grid_lighting_init()
def tile_lighten(x,y,value):Rogue.map.tile_lighten(x,y,value)
def tile_darken(x,y,value): Rogue.map.tile_darken(x,y,value)
def tile_set_light_value(x,y,value):Rogue.map.tile_set_light_value(x,y,value)
def get_light_value(x,y):   return Rogue.map.get_light_value(x,y)
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
        if world.has_component(ent, cmp.Name):
            entname="with name '{}'".format(
                world.component_for_entity(ent, cmp.Name).name)
        else:
            entname="<NO NAME>"
        # position
        if world.has_component(ent, cmp.Position):
            entposx=world.component_for_entity(ent, cmp.Position).x
            entposy=world.component_for_entity(ent, cmp.Position).y
        else:
            entposx = entposy = -1
        # message
        print("ERROR: rogue.py: function getms: entity {e} {n} at pos ({x},{y}) {err}".format(
            e=ent, n=entname, x=entposx, y=entposy, err=errorstring))
        raise ComponentException
# end def



    # "Fun"ctions #

def around(i): # round with an added constant to nudge values ~0.5 up to 1 (attempt to get past some rounding errors)
    return round(i + 0.00001)
def sign(n):
    if n>0: return 1
    if n<0: return -1
    return 0
# tilemap
def thingat(x,y):       return Rogue.map.thingat(x,y) #Thing object
def thingsat(x,y):      return Rogue.map.thingsat(x,y) #list
def inanat(x,y):        return Rogue.map.inanat(x,y) #inanimate Thing at
def monat (x,y):        return Rogue.map.monat(x,y) #monster at
def solidat(x,y):       return Rogue.map.solidat(x,y) #solid Thing at
def wallat(x,y):        return (not Rogue.map.get_nrg_cost_enter(x,y) ) #tile wall
def fluidsat(x,y):      return Rogue.et_managers['fluids'].fluidsat(x,y) #list
def lightsat(x,y):      return Rogue.map.lightsat(x,y) #list
def fireat(x,y):        return False #Rogue.et_managers['fire'].fireat(x,y)

def cost_enter(x,y):    return Rogue.map.get_nrg_cost_enter(x,y)
def cost_leave(x,y):    return Rogue.map.get_nrg_cost_leave(x,y)
def cost_move(xf,yf,xt,yt,data):
    return Rogue.map.path_get_cost_movement(xf,yf,xt,yt,data)

def is_in_grid_x(x):    return (x>=0 and x<ROOMW)
def is_in_grid_y(y):    return (y>=0 and y<ROOMH)
def is_in_grid(x,y):    return (x>=0 and x<ROOMW and y>=0 and y<ROOMH)
def in_range(x1,y1,x2,y2,Range):    return (maths.dist(x1,y1, x2,y2) <= Range + .34)

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
    # diminishing returns on skill gainz
    pts = pts - getskill(ent)*EXP_DIMINISH_RATE
    # train one level at a time
    if pts > 0:
        make(ent,DIRTY_STATS)
        skills = Rogue.world.component_for_entity(ent, cmp.Skills)
        __train(skills, skill, pts)
def __train(skills, skill, pts):
    if skills.skills[skill] >= MAX_LEVEL*EXP_LEVEL:
        skills.skills[skill] = MAX_LEVEL*EXP_LEVEL
        return
    skills.skills[skill] = skills.skills.get(skill, 0) + min(pts,EXP_LEVEL)
    pts = pts - EXP_LEVEL - EXP_DIMINISH_RATE
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
#

##def has_equip(obj,item):
##    return item in Rogue.world.component_for_entity(obj, )
def give(ent,item):
    if on(item,FIRE):
        burn(ent, FIRE_BURN)
        cooldown(item)
    Rogue.world.component_for_entity(ent, cmp.Inventory).data.append(item)
def take(ent,item):
    Rogue.world.component_for_entity(ent, cmp.Inventory).data.remove(item)
def mutate(ent):
    # TODO: do mutation
    mutable = Rogue.world.component_for_entity(ent, cmp.Mutable)
    pos = Rogue.world.component_for_entity(ent, cmp.Position)
    entn = Rogue.world.component_for_entity(ent, cmp.Name)
    # TODO: message based on mutation (i.e. "{t}{n} grew an arm!") Is this dumb?
    event_sight(pos.x,pos.y,"{t}{n} mutated!".format(t=entn.title,n=entn.name))
def has_sight(ent):
    if (Rogue.world.has_component(ent, cmp.SenseSight) and not on(ent,BLIND)):
        return True
    else:
        return False
def port(ent,x,y): # move thing to absolute location, update grid and FOV
    grid_remove(ent)
    pos = Rogue.world.component_for_entity(ent, cmp.Position)
    pos.x=x; pos.y=y;
    grid_insert(ent)
    update_fov(ent)
    if Rogue.world.has_component(ent, cmp.LightSource):
        compo = Rogue.world.component_for_entity(ent, cmp.LightSource)
        compo.light.reposition(x, y)
def drop(ent,item,dx=0,dy=0):   #remove item from ent's inventory, place it
    take(ent,item)              #on ground nearby ent.
    itempos=Rogue.world.component_for_entity(item, cmp.Position)
    entpos=Rogue.world.component_for_entity(ent, cmp.Position)
    itempos.x=entpos.x + dx
    itempos.y=entpos.y + dy
    grid_insert(ent)
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
    print('ent {} exhausted.'.format(ent))
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
# elemental damage
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
    #drop inventory
    if world.has_component(ent, cmp.Inventory):
        for tt in world.component_for_entity(ent, cmp.Inventory).data:
            drop(ent, tt)
    #creatures
    isCreature = world.has_component(ent, cmp.Creature)
    if isCreature:
        #create a corpse
        if dice.roll(100) < entities.corpse_recurrence_percent[_type]:
            create_corpse(ent)
    #inanimate things
    else:
        #burn to ashes
        if on(ent, FIRE):
            mat = world.component_for_entity(ent, cmp.Material).flag
            if (mat==MAT_FLESH
                or mat==MAT_WOOD
                or mat==MAT_FUNGUS
                or mat==MAT_VEGGIE
                or mat==MAT_LEATHER
                ):
                create_ashes(ent)
    #remove dead thing
    if Rogue.world.has_component(ent, cmp.Position):
        if isCreature:
            release_creature(ent)
        else:
            release_entity(ent)
def zombify(ent):
    kill(ent) # temporary
def explosion(name, x, y, radius):
    event_sight(x, y, "{n} explodes!".format(n=name))





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
def update_fov(ent):
    Rogue.c_managers['fov'].update(ent)
def run_fov_manager(ent):
    Rogue.c_managers['fov'].run(ent)
def update_pcfov():
    Rogue.c_managers['fov'].update(Rogue.pc)
def run_pcfov_manager():
    Rogue.c_managers['fov'].run(Rogue.pc)
    
def fov_init():  # normal type FOV map init
    #TODO: THIS CODE NEEDS TO BE UPDATED. ONLY MAKE AS MANY FOVMAPS AS NEEDED.
    fovMap=libtcod.map_new(ROOMW,ROOMH)
    libtcod.map_copy(Rogue.map.fov_map,fovMap)  # get properties from Map
    return fovMap
#@debug.printr
def fov_compute(ent):
    print("computing fov for ent {}".format(ent))
    pos = Rogue.world.component_for_entity(ent, cmp.Position)
    senseSight = Rogue.world.component_for_entity(ent, cmp.SenseSight)
    libtcod.map_compute_fov(
        senseSight.fov_map, pos.x, pos.y, getms(ent, 'sight'),
        light_walls = True, algo=libtcod.FOV_RESTRICTIVE
        )
def update_fovmap_property(fovmap, x,y, value):
    libtcod.map_set_properties( fovmap, x,y,value,True)
##def compute_fovs():     Rogue.c_managers['fov'].run()
# circular FOV function
def can_see(ent,x,y):
    world = Rogue.world
    if (get_light_value(x,y) == 0 and not on(ent,NVISION)):
        return False
    pos = world.component_for_entity(ent, cmp.Position)
    senseSight = world.component_for_entity(ent, cmp.SenseSight)
    return ( in_range(pos.x,pos.y, x,y, getms(ent, "sight")) #<- circle-ize
             and libtcod.map_is_in_fov(senseSight.fov_map,x,y) )
#copies Map 's fov data to all creatures - only do this when needed
#   also flag all creatures for updating their fov maps
def update_all_fovmaps():
    for ent, compo in Rogue.world.get_component(cmp.SenseSight):
        fovMap=compo.fov_map
        libtcod.map_copy(Rogue.map.fov_map, fovMap)
        update_fov(ent)
#******we should overhaul this FOV system!~*************
        #creatures share fov_maps. There are a few fov_maps
        #which have different properties like x-ray vision, etc.
        #the only fov_maps we have should all be unique. Would save time.
        #update_all_fovmaps only updates these unique maps.
        #this would probably be much better, I should do this for sure.



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
    grid_remove(ent) # precautionary ... this may be a bad place to have this
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

#  creature/monsters  #

def register_creature(ent):
    register_entity(ent)
def release_creature(ent):
    release_entity(ent)
    remove_listener_sights(ent)
    remove_listener_sounds(ent)

def create_monster(typ,x,y,col,mutate=3): #init from entities.py
    '''
        call this to create a monster from the bestiary

        TODO: figure out what to do to create monsters/creatures in general
            code for that is not complete...
    '''
    if monat(x,y):
        return None #tile is occupied by a creature already.
    ent = entities.create_monster(typ,x,y,col,mutate)
##    init_inventory(monst, monst.stats.get('carry')) # do this in create_monster
    givehp(ent)
    register_creature(ent)
    return monst

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

def init_inventory(ent, capacity):
    Rogue.world.add_component(ent, cmp.Inventory(capacity))



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




    #---------------------#
    #   Equipment / Body  #
    #---------------------#

def get_arm_length(bodyplan, height): #temporary solution to get arm length based on body type
    if bodyplan==BODYPLAN_HUMANOID:
        return around(height / 2.67)
def curebpp(bpp): #<flags> cure BPP status clear BPP status bpp_clear_status clear_bpp_status clear bpp status bpp clear status
    bpp.status = 0 # revert to normal status
def healbpp(bpp, bpptype, status): #<flags> heal BPP object
    pass #TODO
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
            bpp.status = SKINSTATUS_SKINNED
            return True
    
    # default
    if bpp.status >= status: 
        return False # don't overwrite lower priority statuses.
    # do exactly what the parameters intended
    bpp.status = status # just set the status
    return True
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

#equipping things
def equip(ent,item,equipType): # equip an item in 'equipType' slot
    '''
        equip ent with item in the slot designated by equipType const
        return tuple: (result, compo,)
            where result is a negative value for failure, or 1 for success
            and compo is None or the item's equipable component if success
        
##                #TODO: add special effects; light, etc. How to??
    '''
# init and failure checking #
    # first check that the entity can equip the item in the indicated slot.
    world = Rogue.world
    equipableConst = EQUIPABLE_CONSTS[equipType]
    eqcompo = _get_eq_compo(ent, equipType)
    holdtype=(equipType in cmp.BPS_HOLD) # holding type or armor type?
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
    
    # figure out what additional slots the equipment covers, if any
    def __cov(ent, clis, hlis, flis, eqtype, cls): # cover additional body part
        holdtype=(eqtype in cmp.BPS_HOLD)
        for _com in findbps(ent, cls):
            # held type or armor type?
            if holdtype: # holding type
                if _com.holding: # make sure you can't equip something if ...
                    flis.append(_com) # ... any required slots are occupied.
                else:
                    hlis.append(_com)
                    clslis.append(cls)
            else: # cover type
                if _com.covered: # make sure you can't equip something if ...
                    flis.append(_com) # ... any required slots are occupied.
                else:
                    clis.append(_com)
                    clslis.append(cls)
    # end def
    clis = [] # success list - covered
    hlis = [] # success list - holding
    flis = [] # failure list
    clslis = [] # covers list (class types)
    if ( equipType==EQ_MAINHAND and on(item, TWOHANDS) ):
        __cov(ent,clis,hlis,flis,equipType,cmp.BP_Hand) # Fixme: this covers ALL hands. 
    if equipType==EQ_FRONT:
        if equipable.coversBack:
            __cov(ent,clis,hlis,flis,equipType,cmp.BP_TorsoBack)
        if equipable.coversCore:
            __cov(ent,clis,hlis,flis,equipType,cmp.BP_TorsoCore)
        if equipable.coversHips:
            __cov(ent,clis,hlis,flis,equipType,cmp.BP_Hips)
    if equipType==EQ_MAINHEAD:
        if equipable.coversFace:
            __cov(ent,clis,hlis,flis,equipType,cmp.BP_Face)
        if equipable.coversNeck:
            __cov(ent,clis,hlis,flis,equipType,cmp.BP_Neck)
        if equipable.coversEyes:
            __cov(ent,clis,hlis,flis,equipType,cmp.BP_Eyes)
        if equipable.coversEars:
            __cov(ent,clis,hlis,flis,equipType,cmp.BP_Ears)
    if flis:
        return (-10, flis,) # failed to equip because the BPs in flis are already covered.
# /init #
    
        #-------------------------#
        # success! Equip the item #
        #-------------------------#
    
    # remove item from the map
    grid_remove(item)
    if world.has_component(item, cmp.Position):
        world.remove_component(item, cmp.Position)
    # make item a child of its equipper so it has equipper's position
    world.add_component(item, cmp.Child(ent)) # TODO: implement Child component

        # BUGGY CODE: FIXME! TODO: distinguish between covered and holding, for held items vs armor that covers the slot....
    # put it in the right slot -- is it a held item or a worn item?
    if (equipType==EQ_MAINHAND or equipType==EQ_OFFHAND):
        eqcompo.held.item = item # wielded / held
        eqcompo.holding = True # cover this BP
    else:
        eqcompo.slot.item = item # worn
        eqcompo.covered = True # cover this BP
        eqcompo.slot.covers = tuple(clslis)
    
    # cover the BPs
    for _com in clis:
        _com.covered=True
    for _com in hlis:
        _com.holding=True
    #
    
    make(ent, DIRTY_STATS)
    return (1,eqcompo,) # yey success
    
# end def

def deequip(ent,equipType):
    '''
        remove equipment from slot 'equipType'
        return the item that was equipped there
            or None if failed to de-equip
    '''
    compo = _get_eq_compo(ent, equipType)
    if not compo:
        return None
    
    item = compo.slot.item
    if not item: #nothing equipped here
        return None
    
        #-----------------#
        # remove the item #
        #-----------------#
        
    compo.slot.item = None
    compo.covered = False
    
    # covers
    def __uncov(ent, cls): # cover additional body part
        for compo in findbps(ent, cls):
            compo.covered = False
    if equipType==EQ_FRONT:
        if equipable.coversBack: __uncov(ent,cmp.BP_TorsoBack)
        if equipable.coversCore: __uncov(ent,cmp.BP_TorsoCore)
        if equipable.coversHips: __uncov(ent,cmp.BP_Hips)
    if equipType==EQ_MAINHEAD:
        if equipable.coversFace: __uncov(ent,cmp.BP_Face)
        if equipable.coversNeck: __uncov(ent,cmp.BP_Neck)
        if equipable.coversEyes: __uncov(ent,cmp.BP_Eyes)
        if equipable.coversEars: __uncov(ent,cmp.BP_Ears)    
    compo.slot.covers = ()
    
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

def create_body_humanoid(mass=70, height=175, female=False):
    return entities.create_body_humanoid(mass=mass, height=height, female=female)

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
def metabolism(ent, hunger, thirst=1): entities.metabolism(ent, hunger, thirst)
def stomach(ent): entities.stomach(ent)
def starve(ent): entities.starve(ent)
def dehydrate(ent): entities.dehydrate(ent)
        

    #--------------#
    #     Stats    #
    #--------------#
    
def get_encumberance_breakpoint(enc, encmax):
    erat = enc/max(1,encmax) # encumberance ratio
    if erat < 0.05:     # 0: 0 - 5%
        encbp = 0
    elif erat < 0.12:   # 1: 5 - 12%
        encbp = 1
    elif erat < 0.25:   # 2: 12 - 25%
        encbp = 2
    elif erat < 0.5:    # 3: 25 - 50%
        encbp = 3
    elif erat < 0.75:   # 4: 50 - 75%
        encbp = 4
    elif erat < 0.87:   # 5: 75 - 87%
        encbp = 5
    elif erat < 0.95:   # 6: 87 - 95%
        encbp = 6
    elif erat < 1:      # 7: 95 - 100%
        encbp = 7
    else:               # 8: 100% or greater
        encbp = 8
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
        entities._update_from_body_class(body, modded)
        
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
    # TODO


#~~~~~~~#------------~~~~~~~~~~~~~~~~~~~~~#~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
        # statuses that affect attributes #
        #---------------------------------#
        
    # pain
    if world.has_component(ent, cmp.StatusPain):
        modded.str = min(modded.str, modded.str * PAIN_STRMOD)
        modded.end = min(modded.end, modded.end * PAIN_ENDMOD)
        modded.con = min(modded.con, modded.con * PAIN_CONMOD)
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
            # Strength Requirement and penalties
            strd = bps.equip.strReq - modded.str//MULT_STATS
            if strd > 0:
                # Multiply gear's enc. by ratio based on missing STR
                modded.enc += bps.equip.enc * strd * 0.1
                modded.atk -= strd*INSUFF_STR_ATK_PENALTY*MULT_STATS
                modded.asp -= strd*INSUFF_STR_ASP_PENALTY
            # Dexterity Requirement and penalties
            dexd = bps.equip.dexReq - modded.dex//MULT_STATS
            if dexd > 0:
                modded.atk -= dexd*INSUFF_DEX_ATK_PENALTY*MULT_STATS
                modded.pen -= dexd*INSUFF_DEX_PEN_PENALTY*MULT_STATS
                modded.asp -= dexd*INSUFF_DEX_ASP_PENALTY
            #
    # end for
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

    #---------------------------------------------------------------#
    #       FINAL        MULTIPLIERS       BEGIN       HERE         #
    #---------------------------------------------------------------#
    
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
    
    # blind
    if world.has_component(ent, cmp.StatusBlind):
        modded.sight = modded.sight * BLIND_SIGHTMOD
    # deaf
    if world.has_component(ent, cmp.StatusDeaf):
        modded.hearing = modded.hearing * DEAF_HEARINGMOD
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
        modded.atk = modded.atk + COUGH_ATK
        modded.dfn = modded.dfn + COUGH_DFN
        
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
    
    # quality statuses #
    # have variable magnitude
        
    # drunk
    if world.has_component(ent, cmp.StatusDrunk):
        compo = world.component_for_entity(ent, cmp.StatusDrunk)
        modded.bal = modded.bal - compo.quality
    # off-balance staggered
    if world.has_component(ent, cmp.StatusOffBalance):
        compo = world.component_for_entity(ent, cmp.StatusOffBalance)
        modded.bal = modded.bal - compo.quality
        
    # crouched
    if world.has_component(ent, cmp.StatusBPos_Crouched):
##        modded.height = modded.height * CROUCHED_HEIGHTMOD
        modded.msp = modded.msp * CROUCHED_MSPMOD
        modded.atk = modded.atk + CROUCHED_ATK*MULT_STATS
        modded.dfn = modded.dfn + CROUCHED_DFN*MULT_STATS
    # seated
    if world.has_component(ent, cmp.StatusBPos_Seated):
##        modded.height = modded.height * SEATED_HEIGHTMOD
        modded.msp = modded.msp * SEATED_MSPMOD
        modded.atk = modded.atk + SEATED_ATK*MULT_STATS
        modded.dfn = modded.dfn + SEATED_DFN*MULT_STATS
    # supine
    if world.has_component(ent, cmp.StatusBPos_Supine):
##        modded.height = modded.height * SUPINE_HEIGHTMOD
        modded.msp = modded.msp * SUPINE_MSPMOD
        modded.atk = modded.atk + SUPINE_ATK*MULT_STATS
        modded.dfn = modded.dfn + SUPINE_DFN*MULT_STATS
    # prone
    if world.has_component(ent, cmp.StatusBPos_Prone):
##        modded.height = modded.height * PRONE_HEIGHTMOD
        modded.msp = modded.msp * PRONE_MSPMOD
        modded.atk = modded.atk + PRONE_ATK*MULT_STATS
        modded.dfn = modded.dfn + PRONE_DFN*MULT_STATS
    
    
    
#~~~~~~~#--------------------------#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
        # encumberance - stat mods #
        #--------------------------#

    # Things should avoid affecting attributes as much as possible.
    # Encumberance should not affect agility or any other attribute
    # because encumberance max is dependent on attributes.
    encpc = max(0, 1 - (modded.enc / max(1,modded.encmax)))
    modded.mpregen = modded.mpregen * (0.5 + 0.5*encpc)
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

def occupations(ent):
    return Rogue.occupations.get(ent, None)
def occupation_add(ent,turns,fxn,args,helpless):
    '''
        fxn: function to call each turn.
        args: arguments to pass into fxn
        turns: turns remaining in current occupation
        helpless: bool, whether ent can be interrupted
        interrupted: bool, whether ent has been interrupted in this action
    '''
    Rogue.occupations.update({ ent : (fxn,args,turns,helpless,False) })
def occupation_remove(ent):
    del Rogue.occupations[ent]
def occupation_elapse_turn(ent):
    fxn,args,turns,helpless,interrupted = Rogue.occupations[ent]
    if interrupted:
        Rogue.occupations.update({ ent : (fxn,args,turns - 1,helpless,interrupted) })
        return False    # interrupted occupation
    if turns:
        setAP(ent, 0)
        Rogue.occupations.update({ ent : (fxn,args,turns - 1,helpless,interrupted) })
    elif fxn is not None:
        fxn(ent, args)
    return True     # successfully continued occupation
    



    #----------------#
    #    lights      #
    #----------------#

def list_lights(): return list(Rogue.c_managers["lights"].lights.values())
def create_light(x,y, value, owner=None):
    light=lights.Light(x,y, value, owner)
    light.fov_map=fov_init()
    light.shine()
    lightID = Rogue.c_managers['lights'].add(light)
    if owner:
        if Rogue.world.has_component(owner, cmp.LightSource):
            compo = Rogue.world.component_for_entity(owner, cmp.LightSource)
            release_light(compo.lightID)
        Rogue.world.add_component(owner, cmp.LightSource(lightID, light))
    return lightID

def release_light(lightID):
    light = Rogue.c_managers['lights'].get(lightID)
    light.unshine()
    if light.owner:
        Rogue.world.remove_component(light.owner, cmp.LightSource)
    Rogue.c_managers['lights'].remove(lightID)



    #-------------#
    #   fires     #
    #-------------#

#fire tile flag is independent of the status effect of burning
def set_fire(x,y):
    Rogue.et_managers['fire'].add(x,y)
def douse(x,y): #put out a fire at a tile and cool down all things there
    if not Rogue.et_managers['fire'].fireat(x,y): return
    Rogue.et_managers['fire'].remove(x,y)
    for tt in thingsat(x,y):
        Rogue.bt_managers['status'].remove(tt, FIRE)
        cooldown(tt)



    #----------------#
    #    status      #
    #----------------#

#Status for being on fire separate from the fire entity and light entity.

def get_status(ent, statusCompo):
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
##def set_status_args(ent, status, *args): we might need this....?
##    '''
##        # ent       = Thing object to set the status for
##        # status    = status class (not an object instance)
##        # t         = duration (-1 is the default duration for that status)
##    '''
##    proc.Status.add(ent, status, args)
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

def manager_sights_run():   Rogue.c_managers['sights'].run()
def manager_sounds_run():   Rogue.c_managers['sounds'].run()

# constant managers #

def register_timer(obj):    Rogue.bt_managers['timers'].add(obj)
def release_timer(obj):     Rogue.bt_managers['timers'].remove(obj)

# game state managers #

def get_active_manager():       return Rogue.manager
def close_active_manager():
    if Rogue.manager:
        Rogue.manager.close()
        Rogue.manager=None
def clear_active_manager():
    if Rogue.manager:
        Rogue.manager.set_result('exit')
        close_active_manager()

def routine_look(xs, ys):
    clear_active_manager()
    game_set_state("look")
    Rogue.manager=managers.Manager_Look(
        xs, ys, Rogue.view, Rogue.map.get_map_state())
    alert("Look where? (<hjklyubn>, mouse; <select> to confirm)")
    Rogue.view.fixed_mode_disable()

def routine_move_view():
    clear_active_manager()
    game_set_state("move view")
    Rogue.manager=managers.Manager_MoveView(
        Rogue.view, Rogue.map.get_map_state())
    alert("Direction? (<hjklyubn>; <select> to center view)")
    Rogue.view.fixed_mode_disable()

def routine_print_msgHistory():
    clear_active_manager()
    game_set_state("message history")
    width   = window_w()
    height  = window_h()
    strng   = Rogue.log.printall_get_wrapped_msgs()
    nlines  = 1 + strng.count('\n')
    hud1h   = 3
    hud2h   = 3
    scroll  = makeConBox(width,1000,strng)
    top     = makeConBox(width,hud1h,"message history")
    bottom  = makeConBox(width,hud2h,"<Up>, <Down>, <PgUp>, <PgDn>, <Home>, <End>; <select> to return")
    Rogue.manager = managers.Manager_PrintScroll( scroll,width,height, top,bottom, h1=hud1h,h2=hud2h,maxy=nlines)

def routine_print_charPage():
    clear_active_manager()
    game_set_state("character page")
    width   = window_w()
    height  = window_h()
    strng   = misc.render_charpage_string(width,height,pc(),get_turn(),dlvl())
    nlines  = 1 + strng.count('\n')
    hud1h   = 3
    hud2h   = 3
    scroll  = makeConBox(width,200,strng)
    top     = makeConBox(width,hud1h,"character data sheet")
    bottom  = makeConBox(width,hud2h,"<Up>, <Down>, <PgUp>, <PgDn>, <Home>, <End>; <select> to return")
    Rogue.manager = managers.Manager_PrintScroll( scroll,width,height, top,bottom, h1=hud1h,h2=hud2h,maxy=nlines)

def Input(x,y, w=1,h=1, default='',mode='text',insert=False):
    return IO.Input(x,y,w=w,h=h,default=default,mode=mode,insert=insert)

def adjacent_directions(_dir):
    return ADJACENT_DIRECTIONS.get(_dir, ((0,0,0,),(0,0,0,),) )

#
# aim find target entity
# target entity using a dumb line traversing algorithm
# returns an entity or None
# TODO: move these to some other module
#
def aim_find_target():
    targeted = None
    pos = Rogue.world.component_for_entity(Rogue.pc, cmp.Position)
    while True:
        pcAct=IO.handle_mousekeys(IO.get_raw_input()).items()
        for act,arg in pcAct:
            
            if (act=="context-dir" or act=="move"):
                interesting = [] # possible targets
                checkdir = arg
                t = 0
                
                while t < sight:
                    t += 1
                    
                    # check this tile
                    xx = pos.x + checkdir[0]*t
                    yy = pos.y + checkdir[1]*t
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

                for ent, score in interesting:
                    if score < lowscore:
                        lowscore = score
                        targeted = ent
                # end for
            #                        
            elif act=="exit":
                alert("")
                return None
            elif act=="select":
                return targeted
            elif act=="lclick":
                mousex,mousey,z=arg
                pc=Rogue.pc
                dx=mousex - getx(pc.x)
                dy=mousey - gety(pc.y)
                if (dx >= -1 and dx <= 1 and dy >= -1 and dy <= 1):
                    return (dx,dy,0,)
            #
            
        # end for
    # end while
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
    
    

















        # commented out code below. #











        


    


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
