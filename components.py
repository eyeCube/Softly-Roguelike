'''
    components.py
    Part of Softly Into the Night, a roguelike by Jacob Wharton.
    Copyright 2019.
'''


class Draw:
    def __init__(self, char, color, bgcol):
        self.char=char
        self.color=color
        self.bgcol=bgcol
        
class Name:
    def __init__(self, name: str, title="the ", pronouns=("it","it","its",)):
        self.name = name
        self.title = title
        self.pronouns = pronouns

class DeathFunction:
    def __init__(self, func):
        self.func=func

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

class Ammo:
    def __init__(self, ammoType=0, capacity=1, reloadTime=1, jamChance=0):
        self.ammoType=ammoType
        self.capacity=capacity
        self.reloadTime=reloadTime
        self.jamChance=jamChance
        
class EquipBody:
    def __init__(self):
        self.slot=None #(item, modID)
class EquipHead:
    def __init__(self):
        self.slot=None
class EquipBack:
    def __init__(self):
        self.slot=None
class EquipAmmo:
    def __init__(self):
        self.slot=None
class EquipMainhand:
    def __init__(self):
        self.slot=None
class EquipOffhand:
    def __init__(self):
        self.slot=None
        
class CanEquipInBodySlot:
    def __init__(self, mods): #{component : {var : modf}}
        self.mods=mods
class CanEquipInBackSlot:
    def __init__(self, mods): #{component : {var : modf}}
        self.mods=mods
class CanEquipInHeadSlot:
    def __init__(self, mods): #{component : {var : modf}}
        self.mods=mods
class CanEquipInMainhandSlot:
    def __init__(self, mods): #{component : {var : modf}}
        self.mods=mods
class CanEquipInOffhandSlot:
    def __init__(self, mods): #{component : {var : modf}}
        self.mods=mods
class CanEquipInAmmoSlot:
    def __init__(self, mods): #{component : {var : modf}}
        self.mods=mods

class Usable:
    def __init__(self, funcPC, funcNPC=None):
        self.funcPC=funcPC
        self.funcNPC=funcNPC
class Edible:
    def __init__(self, func, satiation, taste, time=1):
        self.func=func
        self.satiation=satiation
        self.taste=taste
        self.timeToConsume=time
class Quaffable:
    def __init__(self, func, hydration, taste, time=1):
        self.func=func
        self.hydration=hydration
        self.taste=taste
        self.timeToConsume=time
class Openable:
    def __init__(self, isOpen=False, isLocked=False):
        self.isOpen=isOpen
        self.isLocked=isLocked

class Form: #physical makeup of the object
    def __init__(self, mass=0, mat=0, val=0): #, volume, shape
        self.mass=mass
        self.material=mat
        self.value=val

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
class StatusBurning:
    def __init__(self, t=-1): #,dmg=1
        self.timer=t
        #self.dmg=dmg
class StatusCorroding:
    def __init__(self, t=8):
        self.timer=t
class StatusBlinded:
    def __init__(self, t=20):
        self.timer=t
class StatusDeafened:
    def __init__(self, t=150):
        self.timer=t
class StatusIrritated:
    def __init__(self, t=200):
        self.timer=t
class StatusParalyzed:
    def __init__(self, t=5):
        self.timer=t
class StatusVomiting:
    def __init__(self, t=50):
        self.timer=t
class StatusCoughing:
    def __init__(self, t=25):
        self.timer=t
class StatusSprinting:
    def __init__(self, t=10):
        self.timer=t
class StatusHasty:
    def __init__(self, t=25):
        self.timer=t
class StatusSlowed:
    def __init__(self, t=25):
        self.timer=t
class StatusWet:
    def __init__(self, t=100):
        self.timer=t
class StatusDrunk:
    def __init__(self, t=250):
        self.timer=t


























