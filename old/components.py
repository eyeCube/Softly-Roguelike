'''
    components.py
    Part of Softly Into the Night, a roguelike by Jacob Wharton.
    Copyright 2019.
'''

class Observable:
    def __init__(self):
        self.observers=[]

class DeathFunction:
    def __init__(self, func):
        self.func=func

class Draw:
    def __init__(self, char, fgcol, bgcol):
        self.char=char
        self.fgcol=fgcol
        self.bgcol=bgcol
        
class Name:
    def __init__(self, name: str, title="the ", pronouns=("it","it","its",)):
        self.name = name
        self.title = title
        self.pronouns = pronouns

class Form: #physical makeup of the object
    def __init__(self, mass=0, mat=0, val=0): #, volume, shape
        self.mass=mass
        self.material=mat
        self.value=val

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Creature:
    def __init__(self, gender=None, job=None, faction=None):
        self.gender=gender
        self.job=job
        self.faction=faction

class AI:
    def __init__(self, ai=None):
        self.func=func

class Mutable:
    def __init__(self):
        self.mutations=0

class Purse: #Money Container
    def __init__(self, purse=0): #, capacity=99999999
        self.purse=purse

class SenseSight:
    def __init__(self, sight=20):
        self.sight = sight
        self.fov_map = rog.init_fov_map(FOV_NORMAL)
        self.events = []
class SenseSound:
    def __init__(self, hearing=100):
        self.hearing = hearing
        self.events = []

class Skills:
    def __init__(self, *args):
        self.skills=set()
        for arg in args:
            self.skills.add(arg)

##class Ammo:
##    def __init__(self, ammoType=0):
##        self.ammoType=ammoType
class UsesAmmo:
    def __init__(self, ammoType=0, capacity=1, reloadTime=1, jamChance=0):
        self.ammoType=ammoType
        self.capacity=capacity
        self.reloadTime=reloadTime
        self.jamChance=jamChance
        
class EquipBody: # can equip things in the body slot
    def __init__(self, item=None, modID=None):
        self.item=item
        self.modID=modID
class EquipHead:
    def __init__(self, item=None, modID=None):
        self.item=item
        self.modID=modID
class EquipBack:
    def __init__(self, item=None, modID=None):
        self.item=item
        self.modID=modID
class EquipAmmo:
    def __init__(self, item=None, modID=None):
        self.item=item
        self.modID=modID
class EquipMainhand:
    def __init__(self, item=None, modID=None):
        self.item=item
        self.modID=modID
class EquipOffhand:
    def __init__(self, item=None, modID=None):
        self.item=item
        self.modID=modID
        
class CanEquipInBodySlot: # can be equipped in the body slot
    def __init__(self, mods): #{component : {var : modf,}}
        self.mods=mods
class CanEquipInBackSlot:
    def __init__(self, mods): #{component : {var : modf,}}
        self.mods=mods
class CanEquipInHeadSlot:
    def __init__(self, mods): #{component : {var : modf,}}
        self.mods=mods
class CanEquipInMainhandSlot:
    def __init__(self, mods): #{component : {var : modf,}}
        self.mods=mods
class CanEquipInOffhandSlot:
    def __init__(self, mods): #{component : {var : modf,}}
        self.mods=mods
class CanEquipInAmmoSlot:
    def __init__(self, mods): #{component : {var : modf,}}
        self.mods=mods

class Usable: #usable from within actor's inventory
    def __init__(self, funcPC=None, funcNPC=None):
        self.funcPC=funcPC
        self.funcNPC=funcNPC
class Interactable: #usable while on the game grid
    def __init__(self, funcPC=None, funcNPC=None):
        self.funcPC=funcPC
        self.funcNPC=funcNPC
class Pushable:
    def __init__(self, slides=False):
        self.slides=slides
class Edible:
    def __init__(self, func=None, sat=0, taste=0, time=1):
        self.func=func
        self.satiation=satiation
        self.taste=taste
        self.timeToConsume=time
class Quaffable:
    def __init__(self, func=None, hydration=0, taste=0, time=1):
        self.func=func
        self.hydration=hydration
        self.taste=taste
        self.timeToConsume=time
class Openable:
    def __init__(self, isOpen=False, isLocked=False):
        self.isOpen=isOpen
        self.isLocked=isLocked
class Ingredient: #can be used in crafting, cooking, etc.
    def __init__(self, data):
        self.data=data
        
class ReactsWithWater:
    def __init__(self, func=None):
        self.func=func
class ReactsWithFire: # fire makes it boil, explode, etc.
    # IS this the best way to handle this? ...
    def __init__(self, func=None):
        self.func=func

class Inventory: #item container
    def __init__(self, capacity):
        self.capacity=capacity
        self.size=0
        self.data=[]

class FluidContainer:
    def __init__(self, capacity):
        self.capacity=capacity
        self.size=0
        self.data={}

class Actor: #participates in the game by gaining and spending action points
    def __init__(self, spd=1):
        self.ap=0 #action points (energy/potential to act)
        self.spd=spd #AP gained per turn

class BasicStats: #stats any thing is expected to have
    def __init__(self, hp=1, mp=1,
                 resfire=0,resbio=0,reselec=0,resphys=0):
        self.hpmax=hp
        self.hp=hp
        self.mpmax=mp
        self.mp=mp
        self.resfire=resfire    #resistances
        self.resbio=resbio
        self.reselec=reselec
        self.resphys=resphys
        self.temp=0             #meters
        self.rads=0
        self.sick=0
        self.expo=0
    
class CombatStats: #stats any fighter is expected to have
    def __init__(self, atk=0,dfn=0,dmg=0,arm=0,rng=0,_pow=0,asp=0,msp=0):
        self.atk=atk    #attack
        self.dfn=dfn    #DV
        self.dmg=dmg    #melee damage
        self.arm=arm    #AV
        self.rng=rng    #range
        self.pow=_pow   #ranged damage
        self.asp=asp    #atk spd
        self.msp=msp    #move spd

class ElementalDamage: #special elemental damage
    def __init__(self, element, dmg):
        self.element=element
        self.dmg=dmg
##class ElementalPower: #special elemental ranged damage
##    def __init__(self, element, dmg):
##        self.element=element
##        self.dmg=dmg

class StatMods:
    def __init__(self, *args, **kwargs):
        self.mods=[]
        for arg in args:
            self.mods.append(arg)
        for k,w in kwargs:
            self.mods.append((k,w,))

#status effects
    #owned by entities currently exhibiting status effect(s)
class StatusFire:
    def __init__(self, t=-1): #,dmg=1
        self.timer=t
##class StatusSmoldering:
##    def __init__(self, t=-1):
##        self.timer=t
class StatusAcid:
    def __init__(self, t=8):
        self.timer=t
class StatusBlind:
    def __init__(self, t=20):
        self.timer=t
class StatusDeaf:
    def __init__(self, t=150):
        self.timer=t
class StatusIrritated:
    def __init__(self, t=200):
        self.timer=t
class StatusParalyzed:
    def __init__(self, t=5):
        self.timer=t
class StatusVomit:
    def __init__(self, t=50):
        self.timer=t
class StatusCough:
    def __init__(self, t=25):
        self.timer=t
class StatusSprint:
    def __init__(self, t=10):
        self.timer=t
class StatusHaste:
    def __init__(self, t=25):
        self.timer=t
class StatusSlow:
    def __init__(self, t=25):
        self.timer=t
class StatusWet:
    def __init__(self, t=100):
        self.timer=t
class StatusDrunk:
    def __init__(self, t=250):
        self.timer=t


# GLOBAL LISTS OF COMPONENTS #

STATUSES = (
    StatusFire,
    StatusAcid,
    StatusBlind,
    StatusDeaf,
    StatusIrritated,
    StatusParalyzed,
    StatusVomit,
    StatusCough,
    StatusSprint,
    StatusHaste,
    StatusSlow,
    StatusWet,
    StatusDrunk,
    )























# TODO: make Fluid property into a component

##
##class Fluid:
##
##    def __init__(self, x,y):
##        super(Fluid, self).__init__(x, y)
##        self.dic={}
##        self.size=0 #total quantity of fluid in this tile
##
##    def getData(self, stat):    #get a particular stat about the fluid
##        return FLUIDS[self.name].__dict__[stat]
##    
##    def clear(self):            #completely remove all fluids from the tile
##        self.dic={}
##        self.size=0
##    
##    def add(self, name, quantity=1):
##        newQuant = self.dic.get(name, 0) + quantity
##        self.dic.update({name : newQuant})
##        self.size += quantity
##        
##        '''floodFill = False
##        if self.size + quantity > MAX_FLUID_IN_TILE:
##            quantity = MAX_FLUID_IN_TILE - self.size
##            floodFill = True #partial floodfill / mixing
##            #how should the fluids behave when you "inject" a new fluid into a full lake of water, etc.?
##            #regular floodfill will not cut it
##            #maybe just replace the current fluid with the new fluid to keep it simple.
##            '''
##
##        '''if floodFill:
##            #do flood fill algo.
##            #this is going to also have to run a cellular automata to distribute different types of fluids
##            return'''
##
##    def removeType(self, name, quantity=1):
##        if self.size > 0:
##            curQuant = self.dic.get(name, 0)
##            newQuant = max(0, curQuant - quantity)
##            diff = curQuant - newQuant
##            if not diff:     #no fluid of that type to remove
##                return
##            self.size -= diff
##            if newQuant != 0:
##                self.dic.update({name : newQuant})
##            else:
##                #we've run out of this type of fluid
##                self.dic.remove(name)


