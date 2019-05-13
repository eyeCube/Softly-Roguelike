'''
    entities.py

    Jacob Wharton
'''


#import esper

from const import *
import rogue as rog
import components as cmp


##import rogue as rog
##import dice
##from colors import COLORS as COL



diplomacy={
    #Factions:
    #(Rogue,Citizens,Deprived,Elite,Watch,Abominations,)
    FACT_ROGUE      : (1,1,1,0,0,0,),
    FACT_CITIZENS   : (1,1,0,0,0,0,),
    FACT_DEPRIVED   : (1,0,1,0,0,0,),
    FACT_ELITE      : (0,1,0,1,1,0,),
    FACT_WATCH      : (0,1,0,1,1,0,),
    FACT_MONSTERS   : (0,0,0,0,0,1,),
}




bestiary={
    # Column names in more detail:
    # Lo qi, Hi qi, Attack, Damage, Dodge, Armor, Speed, Move Speed, Attack Speed, Carrying Capacity, Mass, Gold.
    
#Type,  Name,                   (Lo\ Hi\ At\Dm\DV\AV\Spd\Msp\Asp\FIR\BIO\ELC\SIGT\HEAR\CARRY\KG\$$\),   FLAGS,

'@' : ('human',                 (20, 20, 5, 2, 2, 0, 100,100,100, 10, 10, 10, 20, 100, 60,  65, 500, ),(CANEAT,),),
'a' : ('abomination',           (16, 8,  0, 4, -8,2, 100,90, 110, 40, 50, 25, 6,  0,   30,  80, 0,  ),(),),
'b' : ('bug-eyed business guy', (20, 30, 5, 2, 2, 0, 150,120,100, 10, 10, 0,  25, 100, 90,  60, 500, ),(CANEAT,),),
'B' : ('butcher',               (50, 20, 5, 6, -4,0, 100,100,100,  0, 25, 25, 10, 100, 90,  130,300, ),(CANEAT,),),
'L' : ('raving lunatic',        (12, 25, 3, 2, 2, 0, 100,100,100,  0, 15, 30, 10, 0,   60,  50, 0, ),(),), #BABBLES,
'r' : ('ravaged',               (4,  1,  1, 2, -8,-1,100,80, 70,   0,  0, 0,  10, 0,   15,  35, 0,  ),(RAVAGED,),),
'R' : ('orctepus',              (15, 5,  6, 2,-12,0, 100,80, 145,  0, 60, 0,  8,  0,   120, 100,0,  ),(CANEAT,),),
's' : ('slithera',              (6,  15, 10,4, -4,0, 100,33, 150,  0, 20, 5,  5,  0,   35,  30, 0, ),(CANEAT,),),
'U' : ('obese scrupula',        (20, 2,  4, 8,-16,3, 100,50, 90,   0, 55, 50, 10, 0,   85,  140,100,  ),(),),
'V' : ('ash vampire',           (50, 80, 8, 5, 8, 0, 100,120,100, 10, 75, 5,  5,  200, 60,  30, 1000,  ),(MEAN,NVISION,),),
'w' : ('dire wolf',             (12, 3,  12,5, 8, 0, 100,225,115, 15, 15, 10, 15, 0,   20,  50, 0,  ),(RAVAGED,),),
'W' : ('whipmaster',            (24, 10, 5, 5, 4, 2, 100,80, 100, 25, 60, 15, 15, 0,   75,  75, 1000, ),(MEAN,NVISION,),),
'z' : ('zombie',                (8,  1,  0, 3,-12,-1,50, 40, 100,  5, 25, 15, 5,  0,   30,  45, 0,  ),(MEAN,),),


}

corpse_recurrence_percent={
    '@' : 100,
    'a' : 30,
    "A" : 100,
    'b' : 100,
    'B' : 100,
    "C" : 100,
    "d" : 100,
    "E" : 100,
    "I" : 100,
    "j" : 100,
    "O" : 100,
    "p" : 100,
    "P" : 100,
    'r' : 20,
    'R' : 75,
    'S' : 100,
    "t" : 100,
    "T" : 100,
    "u" : 100,
    'U' : 100,
    'V' : 100,
    'W' : 50,
    'z' : 20,
}




DUST = MAT_DUST
FLSH = MAT_FLESH
WOOD = MAT_WOOD
STON = MAT_STONE
METL = MAT_METAL
CLTH = MAT_CLOTH


'''

#scripts for making interactive stuff in the game
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

def _stone(eid):
    def func(self):
        for i in range(dice.roll(6)):
            rog.create_thing("dust", self.x, self.y)
    rog.world.component_add(eid, cmp.DeathFunction(func))
    
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
#flag           : name                  type    material,color, HP,kg, solid,push?, script,
#THG.CLOAK
#THG.GENERATOR
THG.SAFE        :("safe",               T_BOX,  METL, 'metal', 2000,420,True,False,  _safe,),
THG.CHAINGUN    :("chaingun",           T_MGUN, METL,  'gray', 80, 55, False,False,_gunpowder,),
THG.GUNPOWDER   :("gunpowder",          T_DUST, DUST,  'gray', 1, 0.1, False,False,_gunpowder,),
THG.GORE        :("hunk of flesh",      T_MEAL, FLSH, 'red',  1, 1,   False,False,_food_meal_savory,),
THG.LOG         :("log",                T_LOG,  WOOD, 'brown',800,100, False,False,_wood,),
THG.WOOD        :("wood",               T_WOOD, WOOD, 'brown',200,2,   False,False,_wood,),
THG.BOX         :("crate",              T_BOX,  WOOD, 'brown',200,50,  True,True,  _boxOfItems1,),
THG.GRAVE       :("grave",              T_GRAVE,STON,'silver',300,300,True,False, _stone,),
THG.POT         :("pot",                T_POT,  METL,'metal', 800,100,True,True, _pot,),
THG.CLAYPOT     :("clay pot",           T_MISC, STON,'scarlet',10,5, False,False, _clayPot,),
THG.STILL       :("still",              T_STILL,METL,'metal', 20, 100,True,False, _still,),
THG.TORCH       :("torch",              T_TORCH,WOOD, 'brown',500,1.1, False,False,_torch,),
THG.DOSIMETER   :("geiger counter",     T_DEVICE,METL,'yellow',1,0.5, False,False,_dosimeter,),
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







#
# Create monster based on current dungeon level
# plugging in values from the table of monsters (bestiary)
# this monster has no special attributes; has generic name
#
def create_monster(typ, pos):
    
    mon=rog.world().create_entity()
    
    # get generic monster attributes #
    
    monData = bestiary[typ]
    
    namestr = monData[0]
    hp,mp,atk,dmg,dfn,arm,spd,msp,asp,fir,bio,elc,vis,aud,inv,kg,val = monData[1]
    _pow=0
    
    job = namestr
    world.add_component(mon, cmp.Name(namestr))
    world.add_component(mon, cmp.Creature(gender=None, job=job, faction=None))
    stats = cmp.CombatStats(atk,dfn,dmg,_pow,)
    stats.hpmax=hp
    stats.mpmax=mp
    stats.atk=atk
    stats.dmg=dmg
    stats.dfn=dfn
    stats.arm=arm
    stats.spd=spd
    stats.msp=msp
    stats.asp=asp
    stats.resfire=fir
    stats.resbio=bio
    stats.reselec=elc
    world.add_component(mon, stats)
    #for flag in monData[i]:     rog.make(monst,flag) #flags
    #i+=1
    #for item in monData[i]:     rog.give(monst,item) #items
    
    #ai, mutations, color? should be handled elsewhere
    
    return monst
    
# end def


'''









'''# level up #
    levels = 1
    for i in range(levels): rog.level(monst)
    '''

