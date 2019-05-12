'''
    components.py
'''

import esper



class Renderable:
    def __init__(self, char, color, bgcol):
        self.char=char
        self.color=color
        self.bgcol=bgcol
        
class Name:
    def __init__(self, name, title="the ", pronouns=("it","it","its",)):
        self.name = name
        self.title = title
        self.pronouns = pronouns

class Health:
    def __init__(self, hp, mp):
        self.hpmax=hp
        self.mpmax=mp
        self.hp=hp
        self.mp=mp

class Resistances:
    def __init__(self, fir=0, bio=0, elc=0, phs=0):
        self.fire=fir
        self.bio=bio
        self.elec=elc
        self.phys=phs

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
        self.ai=ai

class Mutable:
    def __init__(self):
        self.mutations=0

class Purse: #Money Container
    def __init__(self, purse=0): #, capacity=99999999
        self.purse=purse

class Seer:
    def __init__(self, sight=20):
        self.sight = sight
        self.fov_map = rog.init_fov_map(FOV_NORMAL)
        self.events = []

class Listener:
    def __init__(self, hearing=100):
        self.hearing = hearing
        self.events = []

class Skills:
    def __init__(self, *args):
        self.skills=set()
        for arg in args:
            self.skills.add(arg)

class CanEquipArmor:
    def __init__(self):
        self.slot=None

class CanEquipHats:
    def __init__(self):
        self.slot=None

class CanEquipBack:
    def __init__(self):
        self.slot=None

class CanEquipAmmo:
    def __init__(self):
        self.slot=None

class CanEquipWeapon:
    def __init__(self):
        self.slot=None

class CanEquipOffhand:
    def __init__(self):
        self.slot=None

class EquipSlot:
    def __init__(self, item=None, modID=None):
        self.item=item
        self.modID=modID

class CanBeEquipped:
    def __init__(self, equipType, statMods):
        self.equipType=equipType
        self.statMods=statMods

class Gun:
    def __init__(self, ammoType=0, capacity=1, reloadTime=1, jamChance=0):
        self.ammoType=ammoType
        self.capacity=capacity
        self.reloadTime=reloadTime
        self.jamChance=jamChance

class Food:
    def __init__(self, nutrition, taste, time=1):
        self.nutrition=nutrition
        self.taste=taste
        self.timeToConsume=time

class Use:
    def __init__(self, funcPC, funcNPC=None):
        self.funcPC=funcPC
        self.funcNPC=funcNPC

class FluidContainer:
    def __init__(self, capacity):
        self.capacity=capacity
        self.volume=0
        self.fluids={}

class Form:
    def __init__(self, mass): #, volume, shape
        self.mass=mass

class StatMods:
    def __init__(self, *args, **kwargs):
        self.mods=[]
        for arg in args:
            self.mods.append(arg)
        for k,w in kwargs:
            self.mods.append((k,w,))

class Stats:
    def __init__(self):
        self.base_atk=0
        self.atk=0
    @property
    def atk(self): return self._atk
    @atk.setter
    def atk(self, val):
        self._atk = max(0, val)
    @property
    def base_atk(self): return self._base_atk
    @base_atk.setter
    def base_atk(self, val):
        self._base_atk = max(0, val)
    























