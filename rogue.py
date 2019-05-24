'''
    rogue.py
    Part of Softly Into the Night, a roguelike by Jacob Wharton.
    Copyright 2019.

    This file glues everything together.
'''

import esper
import libtcodpy as libtcod
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
import levels
import lights
import misc
import managers
import maths
import player
import tilemap


#----------------#
# global objects #
#----------------#

class Rogue:
    occupations={}
    et_managers={} #end of turn managers
    bt_managers={} #beginning of turn managers
    c_managers={} #const managers
##    manager = None # current active game state manager
    
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
    def create_consoles(cls):   cls.con = game.Console(window_w(),window_h())
    @classmethod
    def create_data(cls):       cls.data = game.GameData()
    @classmethod
    def create_map(cls):        cls.map = tilemap.Tilemap()
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
##        cls.world.add_processor(proc.ActionQueueProcessor(), 100)
        cls.world.add_processor(proc.StatusProcessor(), 11)
        cls.world.add_processor(proc.MetersProcessor(), 10)
        cls.world.add_processor(proc.FluidProcessor(), 2)
        cls.world.add_processor(proc.FireProcessor(), 1)
        cls.world.add_processor(proc.FOVProcessor(), 0)
##    @classmethod # TODO : implement this fxn
##    def create_managers(cls):
##        cls.et_managers.update()
##    @classmethod
##    def create_environment(cls):cls.environ = game.Environment()

        '''

    # constant managers, ran each turn
def create_perturn_managers():
    #end of turn (end of monster's turn)
    Ref.et_managers.update({'fire'      : managers.Manager_Fires()})
    Ref.et_managers.update({'fluids'    : managers.Manager_Fluids()})
    #beginning of turn (beginning of monster's turn)
    Ref.bt_managers.update({'timers'    : managers.Manager_Timers()})
    Ref.bt_managers.update({'status'    : managers.Manager_Status()})
    Ref.bt_managers.update({'meters'    : managers.Manager_Meters()})
    
    # constant managers, manually ran
def create_const_managers():
    Ref.c_managers.update({'fov'        : managers.Manager_FOV()})
    Ref.c_managers.update({'events'     : managers.Manager_Events()})
    Ref.c_managers.update({'sights'     : managers.Manager_SightsSeen()})
    Ref.c_managers.update({'sounds'     : managers.Manager_SoundsHeard()})
    Ref.c_managers.update({'actionQueue': managers.Manager_ActionQueue()})

'''

# world
def world():    return Rogue.world

# player
def pc():       return Rogue.pc

# saved game
def playableJobs():
    return Rogue.savedGame.playableJobs

# log
def logNewEntry():      Rogue.log.drawNew()
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

# clock
def turn_pass():        Rogue.clock.turn_pass()
def get_turn():         return Rogue.clock.turn

# view
def view_nudge(dx,dy):      Rogue.view.nudge(dx,dy)
def view_nudge_towards(obj):Rogue.view.follow(obj)
def view_center(obj):       Rogue.view.center(obj.x, obj.y)
def view_center_player():   Rogue.view.center(Rogue.pc.x, Rogue.pc.y)
def view_center_coords(x,y):Rogue.view.center(x,y)
def view_x():       return  Rogue.view.x
def view_y():       return  Rogue.view.y
def view_w():       return  Rogue.view.w
def view_h():       return  Rogue.view.h
def view_max_x():   return  ROOMW - Rogue.view.w #constraints on view panning
def view_max_y():   return  ROOMH - Rogue.view.h
def fixedViewMode_toggle(): Rogue.view.fixed_mode_toggle()

# map
def map():          return Rogue.map
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
def map_generate(Map,level): levels.generate(Map,level)
def identify_symbol_at(x,y):
    asci = libtcod.console_get_char(0, getx(x),gety(y))
    char = "{} ".format(chr(asci)) if (asci < 128 and not asci==32) else ""
    desc="__IDENTIFY UNIMPLEMENTED__" #IDENTIFIER.get(asci,"???")
    return "{}{}".format(char, desc)
def grid_remove(ent): #kill thing
    Rogue.map.remove_thing(ent)
def grid_insert(ent): #add thing
    Rogue.map.add_thing(ent)
def grid_lights_insert(obj):    Rogue.map.grid_lights[obj.x][obj.y].append(obj)
def grid_lights_remove(obj):    Rogue.map.grid_lights[obj.x][obj.y].remove(obj)
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
def end():                  Rogue.control.end()
def game_state():           return Rogue.control.state
def game_is_running():      return Rogue.control.isRunning
def game_set_state(state="normal"):
    print("$---Game State changed from {} to {}".format(game_state(), state))
    Rogue.control.set_state(state)
def game_resume_state():    return Rogue.control.resume_state
def set_resume_state(state):Rogue.control.set_resume_state(state)

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
    con = Ref.Map.render_gameArea(pc, view_x(),view_y(),view_w(),view_h() )
    #libtcod.console_clear(con_game())
    libtcod.console_clear(con_game())
    libtcod.console_blit(con, view_x(),view_y(),view_w(),view_h(),
                         con_game(), view_port_x(),view_port_y())
#@debug.printr
def render_hud(pc) :
    con = misc.render_hud(hud_w(),hud_h(), pc, get_turn(), d_level() )
    libtcod.console_blit(con,0,0,0,0, con_game(),hud_x(),hud_y())
#@debug.printr
def blit_to_final(con,xs,ys, xdest=0,ydest=0): # window-sized blit to final
    libtcod.console_blit(con, xs,ys,window_w(),window_h(),
                         con_final(), xdest,ydest)
#@debug.printr
def alert(text=""):    # message that doesn't go into history
    dbox(msgs_x(),msgs_y(),msgs_w(),msgs_h(),text,wrap=False,border=None,con=con_final())
    refresh()




#-------------#
# "Fun"ctions #
#-------------#

# tilemap
def thingat(x,y):       return Rogue.map.thingat(x,y) #Thing object
def thingsat(x,y):      return Rogue.map.thingsat(x,y) #list
def inanat(x,y):        return Rogue.map.inanat(x,y) #inanimate Thing at
def monat (x,y):        return Rogue.map.monat(x,y) #monster at
def solidat(x,y):       return Rogue.map.solidat(x,y) #solid Thing at
def wallat(x,y):        return (not Rogue.map.get_nrg_cost_enter(x,y) ) #tile wall
def fluidsat(x,y):      return Rogue.et_managers['fluids'].fluidsat(x,y) #list
def lightsat(x,y):      return Rogue.map.lightsat(x,y) #list
def fireat(x,y):        return Rogue.et_managers['fire'].fireat(x,y)

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

# component functions - better to call directly and save the function call overhead
def get(ent, component): #return an entity's component
    return Rogue.world.component_for_entity(ent, component)
def has(ent, component): #return whether entity has component
    return Rogue.world.has_component(ent, component)
def match(component):
    return Rogue.world.get_component(component)
def matchx(*components):
    return Rogue.world.get_components(components)
    return True
def copyflags(toEnt,fromEnt,copyStatusFlags=True): #use this to set an object's flags to that of another object.
    for flag in Rogue.world.component_for_entity(fromEnt, set):
        if (copyStatusFlags or not flag in STATUSFLAGS):
            make(toEnt, flag)
            
# entity functions
def setAP(ent, val):
    actor=world().component_for_entity(ent, cmp.Actor)
    actor.ap = val
def spendAP(ent, amt):
    actor=world().component_for_entity(ent, cmp.Actor)
    actor.ap = actor.ap - amt
# flags
def on(ent, flag):
    return flag in Rogue.world.component_for_entity(ent, set)
def make(ent, flag):
    Rogue.world.component_for_entity(ent, set).add(flag)
def makenot(ent, flag):
    Rogue.world.component_for_entity(ent, set).remove(flag)
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
def drop(ent,item,dx=0,dy=0):   #remove item from ent's inventory, place it
    take(ent,item)              #on ground nearby ent.
    itempos=Rogue.world.component_for_entity(item, cmp.Position)
    entpos=Rogue.world.component_for_entity(ent, cmp.Position)
    itempos.x=entpos.x + dx
    itempos.y=entpos.y + dy
    register_inanimate(item)
def givehp(ent,val=9999):
    stats = Rogue.world.component_for_entity(ent, cmp.BasicStats)
    stats.hp = min(stats.hpmax, stats.hp + val)
def givemp(ent,val=9999):
    stats = Rogue.world.component_for_entity(ent, cmp.BasicStats)
    stats.mp = min(stats.mpmax, stats.mp + val)
def caphp (ent):
    stats = Rogue.world.component_for_entity(ent, cmp.BasicStats)
    stats.hp = min(stats.hp, stats.hpmax)
def capmp (ent):
    stats = Rogue.world.component_for_entity(ent, cmp.BasicStats)
    stats.mp = min(stats.mp, stats.mpmax)
#train skill
def train (ent,skill):
    skills = Rogue.world.component_for_entity(ent, cmp.Skills)
    skills.skills.add(skill) #({skill : max(SKILLMAX, skills.get(skill,0)+1) })
#damage hp
def hurt(ent, dmg: int):
##    assert isinstance(dmg, int)
    if dmg < 0: return
    stats = Rogue.world.component_for_entity(ent, cmp.BasicStats)
    stats.hp -= dmg
    if stats.hp <= 0:
        kill(ent)
#damage mp
def sap(ent, dmg: int):
##    assert isinstance(dmg, int)
    if dmg < 0: return
    stats = Rogue.world.component_for_entity(ent, cmp.BasicStats)
    stats.mp -= dmg
    if stats.mp <= 0:
        zombify(ent)
#deal fire damage
def burn(ent, dmg, maxTemp=FIRE_MAXTEMP):
    if on(ent, DEAD): return False
    if on(ent, WET):
        clear_status(ent, WET)
        #steam=create_fluid(ent.x, ent.y, "steam")
        return False
    stuff.burn(ent, dmg, maxTemp)
    return True
def cooldown(ent, temp=999):
    if on(ent, DEAD): return False
    stuff.cooldown(ent, temp)
#deal bio damage
def disease(ent, dmg):
    if on(ent, DEAD): return False
    stuff.disease(ent, dmg)      #sick damage
def exposure(ent, dmg):
    if on(ent, DEAD): return False
    stuff.exposure(ent, dmg)    #chem damage
def corrode(ent, dmg):
    if on(ent, DEAD): return False
    stuff.corrode(ent, dmg)      #acid damage
def irradiate(ent, dmg):
    if on(ent, DEAD): return False
    stuff.irradiate(ent, dmg)  #rad damage
def intoxicate(ent, dmg):
    if on(ent, DEAD): return False
    stuff.intoxicate(ent, dmg)#drunk damage
def cough(ent, dmg): #coughing fit status
    if on(ent, DEAD): return False
    stuff.cough(ent, dmg)
def vomit(ent, dmg): #vomiting fit status
    if on(ent, DEAD): return False
    stuff.vomit(ent, dmg)
#deal electric damage
def electrify(ent, dmg):
    if on(ent, DEAD): return False
    stuff.electrify(ent, dmg)
#paralyze
def paralyze(ent, turns):
    if on(ent, DEAD): return False
    stuff.paralyze(ent, turns)
#mutate
def mutate(ent):
    if on(ent, DEAD): return False
    stuff.mutate(ent)
def kill(ent): #remove a thing from the world
    if on(ent, DEAD): return
    world = Rogue.world
    _type = world.component_for_entity(ent, cmp.Draw).char
    if world.has_component(ent, cmp.DeathFunction): # call destroy function
        world.component_for_entity(ent, cmp.DeathFunction)(ent)
    make(ent, DEAD)
    clear_status_all(ent)
    #drop inventory
    if world.has_component(ent, cmp.Inventory):
        for tt in world.component_for_entity(ent, cmp.Inventory):
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
    if on(ent, ONGRID):
        if isCreature:
            release_creature(ent)
        else:
            release_inanimate(ent)
def zombify(ent):
    pass
def explosion(name, x, y, radius):
    event_sight(x, y, "{n} explodes!".format(n=name))



''' TODO: refactor

#----------------------#
#        Events        #
#----------------------#

def event_sight(x,y,text):
    if not text: return
    Ref.c_managers['events'].add_sight(x,y,text)
def event_sound(x,y,data):
    if (not data): return
    volume,text1,text2=data
    Ref.c_managers['events'].add_sound(x,y,text1,text2,volume)
def listen_sights(obj):     return  Ref.c_managers['events'].get_sights(obj)
def listen_sounds(obj):     return  Ref.c_managers['events'].get_sounds(obj)
def add_listener_sights(obj):       Ref.c_managers['events'].add_listener_sights(obj)
def add_listener_sounds(obj):       Ref.c_managers['events'].add_listener_sounds(obj)
def remove_listener_sights(obj):    Ref.c_managers['events'].remove_listener_sights(obj)
def remove_listener_sounds(obj):    Ref.c_managers['events'].remove_listener_sounds(obj)
def clear_listen_events_sights(obj):Ref.c_managers['events'].clear_sights(obj)
def clear_listen_events_sounds(obj):Ref.c_managers['events'].clear_sounds(obj)

def pc_listen_sights():
    pc=Ref.pc
    lis=listen_sights(pc)
    if lis:
        for ev in lis:
            Ref.c_managers['sights'].add(ev)
        manager_sights_run()
def pc_listen_sounds():
    pc=Ref.pc
    lis=listen_sounds(pc)
    if lis:
        for ev in lis:
            Ref.c_managers['sounds'].add(ev)
        manager_sounds_run()
def clear_listeners():      Ref.c_managers['events'].clear()


#------------------------#
# Stats Functions + vars #
#------------------------#

def effect_add(obj,mod):        # Stat mod create
    effID=thing.effect_add(obj,mod)
    return effID
def effect_remove(obj,modID):   # Stat mod delete
    thing.effect_remove(obj,modID)



#---------------#
#     Lists     #
#---------------#

class Lists():
    creatures   =[]     # living things
    inanimates  =[]     # nonliving
    lights      =[]
    fluids      =[]
    
    @classmethod
    def things(cls):
        lis1=set(cls.creatures)
        lis2=set(cls.inanimates)
        return lis1.union(lis2)

# lists functions #

def list_creatures():           return Lists.creatures
def list_inanimates():          return Lists.inanimates
def list_things():              return Lists.things()
def list_lights():              return Lists.lights
def list_fluids():              return Lists.fluids
def list_add_creature(obj):     Lists.creatures.append(obj)
def list_remove_creature(obj):  Lists.creatures.remove(obj)
def list_add_inanimate(obj):    Lists.inanimates.append(obj)
def list_remove_inanimate(obj): Lists.inanimates.remove(obj)
def list_add_light(obj):        Lists.lights.append(obj)
def list_remove_light(obj):     Lists.lights.remove(obj)
def list_add_fluid(obj):        Lists.fluids.append(obj)
def list_remove_fluid(obj):     Lists.fluids.remove(obj)




#----------------#
#       FOV      #
#----------------#

#THIS CODE NEEDS TO BE UPDATED. ONLY MAKE AS MANY FOVMAPS AS NEEDED.
def fov_init():  # normal type FOV map init
    fovMap=libtcod.map_new(ROOMW,ROOMH)
    libtcod.map_copy(Ref.Map.fov_map,fovMap)  # get properties from Map
    return fovMap
#@debug.printr
def fov_compute(obj):
    libtcod.map_compute_fov(
        obj.fov_map, obj.x,obj.y, obj.stats.get('sight'),
        light_walls = True, algo=libtcod.FOV_RESTRICTIVE)
def update_fovmap_property(fovmap, x,y, value): libtcod.map_set_properties( fovmap, x,y,value,True)
def compute_fovs():     Ref.c_managers['fov'].run()
def update_fov(obj):    Ref.c_managers['fov'].add(obj)
# circular FOV function
def can_see(obj,x,y):
    if (get_light_value(x,y) == 0 and not on(obj,NVISION)):
        return False
    return ( in_range(obj.x,obj.y, x,y, obj.stats.get('sight')) #<- circle-ize
             and libtcod.map_is_in_fov(obj.fov_map,x,y) )
#copies Map 's fov data to all creatures - only do this when needed
#   also flag all creatures for updating their fov maps
def update_all_fovmaps():
    for creat in list_creatures():
        if has_sight(creat):
            fovMap=creat.fov_map
            libtcod.map_copy(Ref.Map.fov_map,fovMap)
            update_fov(tt)
#******maybe we should overhaul this FOV system!~*************
        #creatures share fov_maps. There are a few fov_maps
        #which have different properties like x-ray vision, etc.
        #the only fov_maps we have should all be unique. Would save time.
        #update_all_fovmaps only updates these unique maps.
        #this would probably be much better, I should do this for sure.



#----------------#
#      Paths     #
#----------------#

def can_hear(obj, x,y, volume):
    if ( on(obj,DEAD) or on(obj,DEAF) or not obj.stats.get('hearing') ):
         return False
    dist=maths.dist(obj.x, obj.y, x, y)
    maxHearDist=volume*obj.stats.get('hearing')/AVG_HEARING
    if (obj.x == x and obj.y == y): return (0,0,maxHearDist,)
    if dist > maxHearDist: return False
    # calculate a path
    path=path_init_sound()
    path_compute(path, obj.x,obj.y, x,y)
    pathSize=libtcod.path_size(path)
    if dist >= 2:
        semifinal=libtcod.path_get(path, 0)
        xf,yf=semifinal
        dx=xf - obj.x
        dy=yf - obj.y
    else:
        dx=0
        dy=0
    path_destroy(path)
    loudness=(maxHearDist - pathSize - (pathSize - dist))
    if loudness > 0:
        return (dx,dy,loudness)

def path_init_movement():
    pathData=0
    return Ref.Map.path_new_movement(pathData)
def path_init_sound():
    pathData=0
    return Ref.Map.path_new_sound(pathData)
def path_destroy(path):     libtcod.path_delete(path)
def path_compute(path, xfrom,yfrom, xto,yto):
    libtcod.path_compute(path, xfrom,yfrom, xto,yto)
def path_step(path):
    x,y=libtcod.path_walk(path, True)
    return x,y
'''




#----------------#
#     Things     #
#----------------#

def create_thing():
    ent = Rogue.world.create_entity()
    Rogue.world.add_component(ent, set) #flagset
    return ent
def create_stuff(ID, x,y):
    tt = stuff.create(x,y, ID)
    register_inanimate(tt)
    return tt
def release_thing(ent):
    grid_remove(ent)
    Rogue.world.delete_entity(ent)
def register_inanimate(ent):
    name = Rogue.world.component_for_entity(ent, cmp.Name).name
    pos = Rogue.world.component_for_entity(ent, cmp.Position)
##    print("registering {} at {},{}".format(name, pos.x, pos.y))
    grid_insert(ent)
def release_inanimate(ent):
    grid_remove(ent)
    
##    list_add_inanimate(ent)
##    list_remove_inanimate(ent)

    
'''
#---------------#
#   Inventory   #
#---------------#

def init_inventory(obj, capacity):
    obj.inv=items.Inventory(capacity)



#------------#
#   Fluids   #
#------------#

def create_fluid(name, x,y, volume):
    fluid = fluids.create_fluid(x,y,name,volume)
    register_fluid(fluid)
'''
'''def port_fluid(fluid, xto, yto):
    grid_fluids_remove(fluid)
    fluid.x=xto
    fluid.y=yto
    grid_fluids_insert(fluid)
def flow_fluid(fluid, xto, yto, amt): #fluids should be object instances?
    grid_fluids_remove(fluid)
    fluid.x=xto
    fluid.y=yto
    grid_fluids_insert(fluid)
    '''
'''
def register_fluid(obj):
    grid_fluids_insert(obj)
    list_add_fluid(obj)
def release_fluid(obj):
    grid_fluids_remove(obj)
    list_remove_fluid(obj)
    
#fluid containers
def init_fluidContainer(obj, size):
    make(obj,HOLDSFLUID)
    obj.fluidContainer = fluids.FluidContainer(size)



#---------------#
#   Equipment   #
#---------------#

#equipping things
def equip(obj,item,equipType): # equip an item in 'equipType' slot
    slotName = thing.getSlotName(equipType)
    slot = obj.equip.__dict__[slotName]
    if not on(item,CANEQUIP): #can't be equipped
        return None
    if not item.equipType == equipType: #can't be wielded in mainhand
        return None
    if not slot.isEmpty(): #already wielding something
        return None
    #add special effects; light, etc.
    #add stat effects
    effID = effect_add(obj,item.statMods)
    #put item in slot
    slot.setSlot(item, effID)
    return effID
def deequip(obj,equipType): # remove equipment from slot 'equipType'
    slotName = thing.getSlotName(equipType)
    slot = obj.equip.__dict__[slotName]
    if slot.isEmpty(): #nothing equipped here
        return None
    #remove any special effects; light, etc.
    #remove stat effects
    effect_remove(obj, slot.getModID() )
    #remove item from slot
    item = slot.clear()
    return item

# build equipment and place in the world
def create_weapon(name,x,y):
    weap=gear.create_weapon(name,x,y)
    givehp(weap) #give random quality based on dlvl?
    register_inanimate(weap)
    return weap
def create_gear(name,x,y):
    obj=gear.create_gear(name,x,y)
    givehp(weap) #give random quality based on dlvl?
    register_inanimate(obj)
    return obj
'''
    

#---------------------#
#  creature/monsters  #
#---------------------#

#register and release functions do not perform checks to ensure proper calling
#must ensure manually that you insert an object of type Thing
#if a creature already exists in the tile of obj's position,
#   then this function will produce errors.
#likewise make sure you do not try to release an entity
#   that was not first registered.
#Always call proper release that corresponds with the register function
#   in order to remove an object from the game.
def register_creature(ent):
    grid_insert(ent)
##    make(ent,ONGRID) # shouldn't be needed anymore.
##    list_add_creature(ent) # do we need a list of creatures still?
def release_creature(ent):
    release_thing(ent)
    remove_listener_sights(ent)
    remove_listener_sounds(ent)
##    list_remove_creature(ent)
##    makenot(ent,ONGRID)
#call this to create a monster from the bestiary
def create_monster(typ,x,y,col,mutate=3): #init from entities.py
    if monat(x,y):
        return None #tile is occupied by a creature already.
    monst = entities.create_monster(typ,x,y,col,mutate)
##    init_inventory(monst, monst.stats.get('carry')) # do this in create_monster
    givehp(monst)
    register_creature(monst)
    return monst 
#call this to build a creature from scratch, not using entities.py
#call create_monster instead if you want to use a template from the bestiary
#this function does not initialize all creature parameters
def create_creature(name, typ, x,y, col): #init basic creature stuff
    if monat(x,y):
        return None #tile is occupied by a creature already.
    creat = thing.create_creature(name,typ,x,y,col)
    register_creature(creat)
    return creat
def create_corpse(ent):
    corpse = entities.create_corpse(ent)
    register_inanimate(corpse)
    return corpse
def create_ashes(ent):
    ashes = entities.create_ashes(ent)
    register_inanimate(ashes)
    return ashes


    
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
    

'''

#----------------#
#    lights      #
#----------------#

def create_light(x,y, value, owner=None):
    light=lights.Light(x,y, value, owner)
    light.fov_map=fov_init()
    register_light(light)
    if owner:   #light follows owner if applicable
        owner.observer_add(light)
    return light

def register_light(light):
    light.shine()
    grid_lights_insert(light)
    list_add_light(light)
def release_light(light):
    light.unshine()
    if light.owner:
        light.owner.observer_remove(light)
    grid_lights_remove(light)
    list_remove_light(light)



#-------------#
#   fires     #
#-------------#

#fire tile flag is independent of the status effect of burning
def set_fire(x,y):
    Ref.et_managers['fire'].add(x,y)
def douse(x,y): #put out a fire at a tile and cool down all things there
    if not Ref.et_managers['fire'].fireat(x,y): return
    Ref.et_managers['fire'].remove(x,y)
    for tt in thingsat(x,y):
        Ref.bt_managers['status'].remove(tt, FIRE)
        cooldown(tt)



#----------------#
#    status      #
#----------------#

#Status for being on fire separate from the fire entity and light entity.

#set status effect
    # obj       = Thing object to set the status for
    # status    = ID of the status effect
    # t         = duration (-1 is the default duration for that status)
def set_status(obj, status, t=-1):
    Ref.bt_managers['status'].add(obj, status, t)
def clear_status(obj, status):
    Ref.bt_managers['status'].remove(obj, status)
def clear_status_all(obj):
    Ref.bt_managers['status'].remove_all(obj)



#-----------#
#  actions  #
#-----------#

def queue_action(obj, act):
    pass
    #Ref.c_managers['actionQueue'].add(obj, act)



#----------#
# managers #
#----------#

def managers_beginturn_run():
    for v in Ref.bt_managers.values():
        v.run()
def managers_endturn_run():
    for v in Ref.et_managers.values():
        v.run()
def manager_sights_run():   Ref.c_managers['sights'].run()
def manager_sounds_run():   Ref.c_managers['sounds'].run()

# constant managers #

def register_timer(obj):    Ref.bt_managers['timers'].add(obj)
def release_timer(obj):     Ref.bt_managers['timers'].remove(obj)

# game state managers #

def get_active_manager():       return Ref.manager
def close_active_manager():
    if Ref.manager:
        Ref.manager.close()
        Ref.manager=None
def clear_active_manager():
    if Ref.manager:
        Ref.manager.set_result('exit')
        close_active_manager()

def routine_look(xs, ys):
    clear_active_manager()
    game_set_state("look")
    Ref.manager=managers.Manager_Look(
        xs, ys, Ref.view, Ref.Map.get_map_state())
    alert("Look where? (<hjklyubn>, mouse; <select> to confirm)")
    Ref.view.fixed_mode_disable()

def routine_move_view():
    clear_active_manager()
    game_set_state("move view")
    Ref.manager=managers.Manager_MoveView(
        Ref.view, Ref.Map.get_map_state())
    alert("Direction? (<hjklyubn>; <select> to center view)")
    Ref.view.fixed_mode_disable()

def routine_print_msgHistory():
    clear_active_manager()
    game_set_state("message history")
    width   = window_w()
    height  = window_h()
    strng   = Ref.log.printall_get_wrapped_msgs()
    nlines  = 1 + strng.count('\n')
    hud1h   = 3
    hud2h   = 3
    scroll  = makeConBox(width,1000,strng)
    top     = makeConBox(width,hud1h,"Message History:")
    bottom  = makeConBox(width,hud2h,"<Up>, <Down>, <PgUp>, <PgDn>, <Home>, <End>; <select> to return")
    Ref.manager = managers.Manager_PrintScroll( scroll,width,height, top,bottom, h1=hud1h,h2=hud2h,maxy=nlines)

def Input(x,y, w=1,h=1, default='',mode='text',insert=False):
    return IO.Input(x,y,w=w,h=h,default=default,mode=mode,insert=insert)

def get_direction():
    return IO.get_direction()

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
    
    '''
















##def makeEquip(obj, component):
##    make(obj, CANEQUIP)
##    Rogue.world.add_component(obj, component)
###gain (improve) stat
##def gain (obj,stat,val=1,Max=999):
##    stats=obj.stats
##    setattr(stats, stat, min(Max, getattr(stats, stat) + val))
###drain (damage) stat
##def drain (obj,stat,val=1):
##    old = getattr(obj.stats,stat)
##    setattr(obj.stats,stat, old-val )
##    if (stat=='hpmax'): caphp(obj)
##    if (stat=='mpmax'): capmp(obj)

##def is_creature(obj):   return Rogue.world.component_for_entity(obj, Creature)
##def is_solid(obj):      return ISSOLID in Rogue.world.component_for_entity(obj, set)
##def on  (obj,flag):     return (flag in obj.flags)
##def make(obj,flag):     obj.flags.add(flag)
##def makenot(obj,flag):  obj.flags.remove(flag)
###set stat
##def setStat (obj,stat,val):
##    setattr(get(obj, cmp., stat, val)

'''
def getComp(objID, component):
    return Rogue.world.get_component(objID, component)

def hasComp(objID, component):
    return Rogue.world.has_component(objID, component)
    
def create_thing(name, x, y, char, color, bgcol):
    ent = Rogue.world.create_entity(set(), #flags set
        cmp.Name(name), cmp.Position(x,y),
        cmp.Draw(char, color, bgcol),
        cmp.BasicStats(),
        )
    return ent

def create_creature(name, x, y):
    ent = Rogue.world.create_entity(
        cmp.Draw(),
        cmp.Name(name), cmp.Position(x,y), cmp.Actor(100),
        cmp.BasicStats(), cmp.CombatStats(), cmp.Creature(),
        cmp.Purse(), cmp.Inventory(), cmp.Skills(), cmp.Form(),
        cmp.StatMods(), cmp.StatusEffects(), cmp.Mutable(), 
        cmp.EquipBody(), cmp.EquipAmmo(), cmp.EquipBack(),
        cmp.EquipMainhand(), cmp.EquipOffhand(), cmp.EquipHead(),
        )
    return ent
'''






'''
TEST

Rogue.create_world()
i=Rogue.world.create_entity(cmp.Position(1,1))
print(get(i, cmp.Position))
if has(i, cmp.Name):
    print(get(i, cmp.Name))
    '''





'''
    ##TESTING a* A star path
    while not libtcod.path_is_empty(path):
        x,y=path_step(path)
        if x is None:
            print('A* stuck')
            break
        libtcod.console_set_char_background(con_final(), getx(x),gety(y), COL['white'])
'''
'''
def msg_printall():
        # init manager
    width   = window_w()
    strng   = Ref.log.printall_get_wrapped_msgs()
    nlines  = 1 +strng.count('\n')
    hud1h   = 3
    hud2h   = 4
    scroll  = makeConBox(width,1000,strng)
    top     = makeConBox(width,hud1h,"Message History:")
    bottom  = makeConBox(width,hud2h,'....')
        # execute manager
    manager = managers.Manager_PrintScroll( scroll,top,bottom, h1=hud1h,h2=hud2h,maxy=nlines)
    
    while not manager.result:
        manager.run()
    manager.close()
#'''


'''def get_exp_req(level):     # experience required to level up at a certain level
    return (level+1)*20

def level(monst):           # level up
    monst.stats.lvl     += 1
    monst.stats.atk     += 1
    monst.stats.dfn     += 1
    monst.stats.dmg     += 1
    monst.stats.hpmax   += HP_PER
    monst.stats.mpmax   += MP_PER

def award_exp(monst,exp):
    monlv = monst.stats.lvl
    monst.stats.exp += max(0, exp - monlv)
    expreq = get_exp_req(monlv)
    if monst.stats.exp >= expreq:
        monst.exp -= expreq
        level(monst)
'''



'''from gamedata
room = [[]]    # Lists of saved room data
field = []     # List of objects in the current room


def room_save(index) :
    room[index] = []
    for obj in self.field:
        self.room[index].append(obj)


def room_load(self, index) :
    self.field = []
    for obj in self.room[index]:
        self.field.append(obj)


def create_map(self, width, height) :
    self.map = map_new(width, height)
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

'''
    con_box0 = Ref.log.printall_make_box0(width,strng)
    con_box1 = Ref.log.printall_make_box1(width,box1h)
    con_box2 = Ref.log.printall_make_box2(width,box2h)
    
    manager = managers.PrintScrollManager(con_box0,con_box1,con_box2)
    while True:
        reply=manager.run()
        if (reply==' ' or reply==chr(K_ESCAPE) or reply==chr(K_ENTER)):
            break
    
    width = window_w()
    height = window_h()
    box1h = 3
    box2h = 4
    box2y = window_h()-box2h
    strng = Ref.log.printall_get_wrapped_msgs()
    
    scrollspd       = 1
    pagescroll      = height -(box1h+box2h+2)
    maxy            = 1 + strng.count('\n')
    y = 0
    while True:
        blit_to_final(con_box0,0,y,0,box1h)
        blit_to_final(con_box1,0,0,0,0)
        blit_to_final(con_box2,0,0,0,box2y)
        refresh()
        
        reply=IO.Input(width-5,height-1,w=4,mode="wait",default="...")
        if   reply==chr(K_UP):       y = max(0,      y-scrollspd)
        elif reply==chr(K_DOWN):     y = min(maxy,   y+scrollspd)
        elif reply==chr(K_PAGEUP):   y = max(0,      y-int(pagescroll))
        elif reply==chr(K_PAGEDOWN): y = min(maxy,   y+int(pagescroll))
        elif reply==chr(K_HOME):     y = 0
        elif reply==chr(K_END):      y = max(0,      maxy-pagescroll)
        elif (reply==' ' or reply==chr(K_ESCAPE) or reply==chr(K_ENTER)):
            break
    
    update_final() # refresh screen when done
    libtcod.console_delete(con_box0)
    libtcod.console_delete(con_box1)
    libtcod.console_delete(con_box2)
'''

'''
def shield(obj,item): # equip an item in the offhand
    if not on(item,CANEQUIP): #can't be equipped
        return None
    if not item.equipType == EQ_OFFHAND: #can't be wielded in mainhand
        return None
    if not obj.equip.offHand.isEmpty(): #already wielding something
        return None 
    effID = effect_add(obj,item.statMods)
    obj.equip.offHand.setSlot(item, effID)
    return effID
def wearBody(obj,item): # put on body armor
    if not on(item,CANEQUIP): #can't be equipped
        return None
    if not item.equipType == EQ_BODY: #can't be worn on body
        return None
    if not obj.equip.body.isEmpty(): #already wearing something on body
        return None 
    effID = effect_add(obj,item.statMods)
    obj.equip.body.setSlot(item, effID)
    return effID'''


