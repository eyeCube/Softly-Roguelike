'''
    rogue.py
    Part of Softly Into the Night, a roguelike by Jacob Wharton.
    Copyright 2019.
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
    def create_player(cls):     cls.pc = player.chargen()
    @classmethod
    def create_savedGame(cls):  cls.savedGame = game.SavedGame()
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


'''
#
# func textbox
#
# display text box with border and word wrapping
#
    Args:
    x,y,w,h     location and size
    text        display string
    border      border style. None = No border
    wrap        whether to use automatic word wrapping
    margin      inside-the-box text padding on top and sides
    con         console on which to blit textbox, should never be 0
                    -1 (default) : draw to con_game()
    disp        display mode: 'poly','mono'

'''
def dbox(x,y,w,h,text='', wrap=True,border=0,margin=0,con=-1,disp='poly'):
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
        if dice.roll(100) < monsters.corpse_recurrence_percent[_type]:
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
    print("registering {} at {},{}".format(name, pos.x, pos.y))
    grid_insert(ent)
def release_inanimate(ent):
    grid_remove(ent)


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
def release_creature(ent):
    release_thing(ent)
    remove_listener_sights(ent)
    remove_listener_sounds(ent)


    
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

