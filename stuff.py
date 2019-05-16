'''
    stuff.py
    inanimate tts to populate the world
'''

from const import *
import rogue as rog
import thing
import dice
from colors import COLORS as COL



DUST = MAT_DUST
GUNP = MAT_GUNPOWDER
FLSH = MAT_FLESH
WOOD = MAT_WOOD
STON = MAT_STONE
METL = MAT_METAL
CLTH = MAT_CLOTH


#conversion functions:
# convert things into specific types of things by giving them certain data
def _edible(tt, nutrition, taste):
    rog.make(tt,EDIBLE)
    rog.taste=taste
    tt.nutrition=nutrition
    
def _food_poison(tt):
    _edible(tt, RATIONFOOD, TASTE_SWEET) #deceptively sweet
    rog.make(tt,SICK) #makes you sick when you eat it
def _food_ration_savory(tt):
    _edible(tt, FOOD_MORSEL, TASTE_SAVORY)
def _food_ration_savory(tt):
    _edible(tt, FOOD_RATION, TASTE_SAVORY)
def _food_serving_savory(tt):
    _edible(tt, FOOD_RATION*3, TASTE_SAVORY)
def _food_meal_savory(tt):
    _edible(tt, FOOD_RATION*9, TASTE_SAVORY)
def _food_bigMeal_savory(tt):
    _edible(tt, FOOD_RATION*18, TASTE_SAVORY)
    
def _wood(tt):
    rog.make(tt, CANWET)
    
def _pot(tt): #metal pot
    rog.init_fluidContainer(tt, 200)
##    rog.make(tt, CANUSE)
##    tt.useFunctionPlayer = action.pot_pc
##    tt.useFunctionMonster = action.pot

def _clayPot(tt):
    rog.make(tt, HOLDSFLUID)
    tt.capacity = 20
    
def _gunpowder(tt):
    rog.make(tt, WATERKILLS)

def _boxOfItems1(tt):
    rog.init_inventory(tt, 200)
    #newt=
    #rog.give(tt, newt)

def _safe(tt):
    rog.init_inventory(tt, 200)
    rog.make(tt, CANOPEN)
    rog.make(tt, INTERACT) #interact to lock or unlock
    
def _still(tt):
    rog.make(tt, HOLDSFLUID)
    rog.make(tt, INTERACT)
    #...
    
def _dosimeter(tt):
    #use function two options: 1) toggles on/off. 2) displays a reading only when you use it.
    rog.make(tt, WATERKILLS)
    rog.make(tt, CANUSE)
    rog.makeEquip(tt, EQ_MAINHAND)
    tt.statMods={"range":3, "atk":2, "dmg":1,}
    def funcPlayer(self, obj): 
        xx=obj.x
        yy=obj.y
        reading = rog.radsat(xx,yy)
        rog.msg("The geiger counter reads '{} RADS'".format(reading))
        #could do, instead:
        # use turns it on, activates an observer.
        # updates when rad damage received by player. Adds rad value to dosimeter
        # when you use again, you can either read it or turn it off.
        rog.drain(obj, 'nrg', NRG_USE)
    def funcMonster(self, obj):
        rog.drain(obj, 'nrg', NRG_USE)
        rog.event_sight(obj.x,obj.y,"{t}{n} looks at a geiger counter.")
    def funcDeath(self):
        rog.explosion(self.name, self.x,self.y, 1)
    tt.useFunctionPlayer = funcPlayer
    tt.useFunctionMonster = funcMonster
    tt.deathFunction = funcDeath
    
def _towel(tt):
    rog.make(tt, CANWET)
    rog.make(tt, CANUSE)
    rog.makeEquip(tt, EQ_BODY)
    tt.statMods={"rescold":20,}
    tt.useFunctionPlayer = action.towel_pc
    tt.useFunctionMonster = action.towel
def _towel_wield(tt): #prepare a towel for wielding. Transforms it into a wielding item.
    rog.makeEquip(tt, EQ_MAINHAND)
    tt.statMods={"atk":3, "dmg":2,}
def _towel_wield(tt): #prepare a towel for headwear. Transforms it into head gear
    rog.makeEquip(tt, EQ_HEAD)
    tt.statMods={"resbio":15,}
    
def _torch(tt):
    rog.make(tt, CANEQUIP)
    tt.equipType=EQ_OFFHAND

def _extinguisher(tt):
    rog.make(tt, CANUSE)
##    tt.useFunctionPlayer = action.extinguisher_pc
##    tt.useFunctionMonster = action.extinguisher
    rog.makeEquip(tt, EQ_MAINHAND)
    tt.statMods = {"dmg":5, "asp":-33,}
    
def _cloak(tt):
    rog.make(tt, CANEQUIP)
##    tt.equipType=EQ_OFFHAND
##    rog.make(tt, CANUSE)
##    tt.useFunctionPlayer = action.cloak_pc
##    tt.useFunctionMonster = action.cloak



STUFF={
#flag           : name                  type   material,color, HP, kg, solid,push?,script,
#THG.CLOAK
#THG.GENERATOR
THG.SAFE        :("safe",               T_BOX,  METL, 'metal', 2000,420,True,False,  _safe,),
THG.CHAINGUN    :("chaingun",           T_MGUN, METL,  'gray', 80, 55, False,False,_gunpowder,),
THG.GUNPOWDER   :("grain of gunpowder", T_DUST, GUNP,  'gray', 1, 0.01,False,False,_gunpowder,),
THG.GORE        :("hunk of flesh",      T_MEAL, FLSH, 'red',  1, 1,   False,False,_food_meal_savory,),
THG.LOG         :("log",                T_LOG,  WOOD, 'brown',1000,100,False,False,_wood,),
THG.WOOD        :("wood",               T_WOOD, WOOD, 'brown',200,5,   False,False,_wood,),
THG.BOX         :("crate",              T_BOX,  WOOD, 'brown',200,50,  True,True,  _boxOfItems1,),
THG.GRAVE       :("grave",              T_GRAVE,STON,'silver',300,300,True,False, None,),
THG.POT         :("pot",                T_POT,  METL,'metal', 800,100,True,True, _pot,),
THG.CLAYPOT     :("clay pot",           T_MISC, STON,'scarlet',10,5, False,False, _clayPot,),
THG.STILL       :("still",              T_STILL,METL,'metal', 5, 100,True,False, _still,),
THG.TORCH       :("torch",              T_TORCH,WOOD, 'brown',350,1.1, False,False,_torch,),
THG.DOSIMETER   :("geiger counter",     T_DEVICE,METL,'yellow',5,0.5, False,False,_dosimeter,),
THG.EXTINGUISHER:("fire extinguisher",  T_DEVICE,METL,'red',  8,8, False,False,_extinguisher,),
THG.TOWEL       :("towel",              T_TOWEL,CLTH,'accent', 10,0.8,False,False,_towel,),
    }


#create a thing from STUFF; does not register thing
def create(x,y,ID):
    name,typ,mat,fgcol,lo,kg,solid,push,script = STUFF[ID]
    tt = thing.Thing(x,y, _type=typ,name=name,color=COL[fgcol])
    tt.mass = kg
    tt.material=mat
    if lo: hp(tt, lo)
    tt.isSolid = solid
    if push: rog.make(tt, CANPUSH)
    #_applyResistancesFromMaterial(tt, mat)
    return tt



#quick functions for multiple types of objects:
def hp(tt, value): #give a Thing a specified amount of HP and fully heal them
    tt.stats.hpmax=value; rog.givehp(tt);
#give a random number of items to the inventory of Thing tt
    #func is a function to build the items
    #_min is minimum number of items possible to give
    #_max is maximum "
def giveRandom(tt, func, _min, _max):
    for ii in range((_min - 1) + dice.roll(_max - (_min - 1))):
        item = func()
        rog.give(tt, item)



