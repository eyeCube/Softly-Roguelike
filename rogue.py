'''
    rogue.py

    Jacob Wharton
'''

import esper

import components as cmp
#import tilemap
#import player


class Rogue:
    @classmethod
    def create_world(cls):  cls.world = esper.World()
##    @classmethod
##    def create_map(cls):    cls.Map = tilemap.Tilemap()
##    @classmethod
##    def create_player(cls): cls.pc = player.chargen()

def world():    return Rogue.world
def pc():       return Rogue.pc

def on(obj, flag):
    return flag in Rogue.world.component_for_entity(obj, set)
def make(obj, flag):
    Rogue.world.component_for_entity(obj, set).add(flag)
def makenot(obj, flag):
    Rogue.world.component_for_entity(obj, set).remove(flag)

def thingsat(x,y):  return Rogue.Map.thingsat(x,y)

    
def kill(objID):
    world=Rogue.world
    if DEAD in world.component_for_entity(objID, set):
        return False
    if world.has_component(objID, cmp.DeathFunction): # call destroy function
        world.component_for_entity(objID, cmp.DeathFunction)()
    world.delete_entity(objID)
    return True

def get(objID, component): #return an entity's component
    return Rogue.world.component_for_entity(objID, component)
def has(objID, component): #return whether entity has component
    return Rogue.world.has_component(objID, component)



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
        cmp.Name(name), cmp.Position(x,y), cmp.TakesTurns(100),
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

