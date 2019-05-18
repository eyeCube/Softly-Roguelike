'''
    rogue.py
    Part of Softly Into the Night, a roguelike by Jacob Wharton.
    Copyright 2019.
'''

import esper
import libtcodpy as libtcod
import math

from const      import *
import components as cmp
import orangio  as IO
import action
import debug
import dice
import fluids
import game
import items
import levels
import lights
import misc
import monsters
import managers
import maths
import player
import stuff
import thing
import tilemap
from colors import COLORS as COL


##
##class Ref():        # stores global references to objects
##    ctrl        = None  # global controller
##    con         = None  # consoles
##    data        = None
##    Map         = None
##    clock       = None
##    update      = None
##    settings    = None
##    view        = None
##    log         = None  # messages
##    pc          = None
##    environ     = None
##    manager     = None  # current active game state manager
##    savedGame   = None
##    et_managers = {}    # per turn managers that tick at end of each turn
##    bt_managers = {}    # per turn managers that tick at beginning of each turn
##    c_managers  = {}    # const managers, ran manually
##


class Rogue:
    @classmethod
    def create_world(cls):  cls.world = esper.World()
    @classmethod
    def create_map(cls):    cls.Map = tilemap.Tilemap()
    @classmethod
    def create_player(cls): cls.pc = player.chargen()

def world():    return Rogue.world
def pc():       return Rogue.pc




#-------------#
# "Fun"ctions #
#-------------#

# tilemap
def thingat(x,y):       return Rogue.Map.thingat(x,y) #Thing object
def thingsat(x,y):      return Rogue.Map.thingsat(x,y) #list
def inanat(x,y):        return Rogue.Map.inanat(x,y) #inanimate Thing at
def monat (x,y):        return Rogue.Map.monat(x,y) #monster at
def solidat(x,y):       return Rogue.Map.solidat(x,y) #solid Thing at
def wallat(x,y):        return (not Rogue.Map.get_nrg_cost_enter(x,y) ) #tile wall
def fluidsat(x,y):      return Rogue.et_managers['fluids'].fluidsat(x,y) #list
def lightsat(x,y):      return Rogue.Map.lightsat(x,y) #list
def fireat(x,y):        return Rogue.et_managers['fire'].fireat(x,y)

def cost_enter(x,y):    return Rogue.Map.get_nrg_cost_enter(x,y)
def cost_leave(x,y):    return Rogue.Map.get_nrg_cost_leave(x,y)
def cost_move(xf,yf,xt,yt,data):
    return Rogue.Map.path_get_cost_movement(xf,yf,xt,yt,data)

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
    if Rogue.Map.get_char(x,y) == FUNGUS:
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

