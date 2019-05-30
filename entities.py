'''
    entities.py
    Part of Softly Into the Night, a roguelike by Jacob Wharton.
    Copyright 2019.
'''

import random

from const import *
from colors import COLORS as COL
import rogue as rog
import components as cmp
import action
import dice



# CONSTANTS #

NUMWPNSTATS = 3

FLSH = MAT_FLESH
VEGG = MAT_VEGGIE
FUNG = MAT_FUNGUS
LETH = MAT_LEATHER
CLTH = MAT_CLOTH
WOOD = MAT_WOOD
BONE = MAT_BONE
CARB = MAT_CARBON
PLAS = MAT_PLASTIC
METL = MAT_METAL
STON = MAT_STONE
DUST = MAT_DUST
GUNP = MAT_GUNPOWDER
ROPE = MAT_ROPE

NASTY= TASTE_NASTY
BITTR= TASTE_BITTER
SWEET= TASTE_SWEET
SALTY= TASTE_SALTY
SAVOR= TASTE_SAVORY

PH = ELEM_PHYS
FI = ELEM_FIRE
BI = ELEM_BIO
CH = ELEM_CHEM
EL = ELEM_ELEC
RA = ELEM_RADS

ARMR = T_ARMOR
HELM = T_HELMET
BACK = T_CLOAK

TSTO    = T_STONE
MEL     = T_MELEEWEAPON
OFF     = T_OFFHANDWEAP
ENER    = T_ENERGYWEAPON
HEVY    = T_HEAVYWEAPON
GUN     = T_GUN
BOW     = T_BOW
SLNG    = T_SLING
EXPL    = T_EXPLOSIVE

A_BULL = AMMO_BULLETS
A_CART = AMMO_CARTRIDGES
A_SHOT = AMMO_SHOT
A_SLING= AMMO_SLING
A_STONE= AMMO_STONES
A_ARRO = AMMO_ARROWS
A_ELEC = AMMO_ELEC
A_FLUID= AMMO_FLUIDS
A_OIL  = AMMO_OIL
A_HAZM = AMMO_HAZMATS
A_ACID = AMMO_ACID
A_CHEM = AMMO_CHEMS
A_ROCKT= AMMO_ROCKETS
A_GREN = AMMO_GRENADES
A_FLAM = AMMO_FLAMMABLE
A_ANY  = AMMO_ANYTHING




# FUNCTIONS #


# GEAR #
    #non-weapon gear
def get_gear_type(gData):           return gData[0]
def get_gear_value(gData):          return gData[1]
def get_gear_mass(gData):           return gData[2]
def get_gear_hpmax(gData):          return gData[3]
def get_gear_mat(gData):            return gData[4]
def get_gear_dfn(gData):            return gData[5][0]
def get_gear_arm(gData):            return gData[5][1]
def get_gear_msp(gData):            return gData[5][2]
def get_gear_sight(gData):          return gData[5][3]
def get_gear_resbio(gData):         return gData[5][4]
def get_gear_resfire(gData):        return gData[5][5]
def get_gear_reselec(gData):        return gData[5][6]
def get_gear_script(gData):         return gData[6]
    #weapons
def get_weapon_type(gData):         return gData[0]
def get_weapon_value(gData):        return gData[1]
def get_weapon_mass(gData):         return gData[2]
def get_weapon_hpmax(gData):        return gData[3]
def get_weapon_capacity(gData):     return gData[4]
def get_weapon_rt(gData):           return gData[5]
def get_weapon_jam(gData):          return gData[6]
def get_weapon_mat(gData):          return gData[7]
def get_weapon_range(gData):        return gData[7][0]
def get_weapon_atk(gData):          return gData[7][1]
def get_weapon_dmg(gData):          return gData[7][2]
def get_weapon_pow(gData):          return gData[7][3]
def get_weapon_dv(gData):           return gData[7][4]
def get_weapon_av(gData):           return gData[7][5]
def get_weapon_asp(gData):          return gData[7][6]
def get_weapon_msp(gData):          return gData[7][7]
def get_weapon_elem(gData):         return gData[7][8]
def get_weapon_ammo(gData):         return gData[8]
def get_weapon_flags(gData):        return gData[9]
def get_weapon_script(gData):       return gData[10]

# JOBS #
def getJobs():
    #returns dict of pairs (k,v) where k=ID v=charType
    ll={}
    for k,v in JOBS.items():
        ll.update({k: getChar(k)})
    return ll
def getChar(jobID) -> str:
    return JOBS[jobID][0]
def getName(jobID) -> str:
    return JOBS[jobID][1]
def getMass(jobID) -> int:
    return JOBS[jobID][2]
def getMoney(jobID) -> int:
    return JOBS[jobID][3]
def getClearance(jobID) -> int: #get security clearance level
    return JOBS[jobID][4]
def getKey(jobID) -> str:
    return JOBS[jobID][5]
def getStats(jobID) -> dict:
    return JOBS[jobID][6]
def getSkills(jobID) -> tuple:
    return JOBS[jobID][7]

    
# item scripts #

# gear #

def _cloak(tt):
    if not rog.has(tt, cmp.CanEquipInMainhandSlot):
        modDict = { cmp.CombatStats : {"atk":3,"dmg":1,"dfn":1,}, }
        rog.world().add_component(tt, cmp.CanEquipInMainhandSlot(modDict))
        
def _fireBlanket(tt):
    pass

def _nvisionGoggles(tt):
##    if rog.has(tt, cmp.Equipable):
##        equipable = rog.get(tt, cmp.Equipable)
##        equipable.statMods.update({})
    pass

def _earPlugs(tt):
    pass

# explosives #

def _molotov(tt):
    def deathFunc(ent):
        pos=rog.world().component_for_entity(ent, cmp.Position)
        diameter = 7
        radius = int(diameter/2)
        for i in range(diameter):
            for j in range(diameter):
                xx = pos.x + i - radius
                yy = pos.y + j - radius
                if not rog.in_range(pos.x,pos.y, xx,yy, radius):
                    continue
                rog.create_fluid(FL_NAPALM, xx,yy, dice.roll(3))
                rog.set_fire(xx,yy)
    tt.deathFunction = deathFunc
def _ied(tt):
    pass
def _fragBomb(tt):
    def deathFunc(ent):
        #explode
        pass
    rog.world().add_component(tt, cmp.DeathFunction(deathFunc))
def _fragMine(tt):
    pass

# ammo #

def _incendiary(tt):
    def deathFunc(ent):
        entn=rog.world().component_for_entity(ent, cmp.Name)
        pos=rog.world().component_for_entity(ent, cmp.Position)
        rog.set_fire(pos.x, pos.y)
        radius=1
        rog.explosion("{}{}".format(entn.title,entn.name), pos.x,pos.y, radius)
    rog.world().add_component(tt, cmp.DeathFunction(deathFunc))
def _paperCartridge(tt):
    #do not need to load with gunpowder
    pass



# food #

def _food_poison(ent):  #deceptively sweet but makes you sick
    rog.world().add_component(ent, cmp.Edible(
        func=_sick, sat=FOOD_RATION, taste=TASTE_SWEET
        ))
def _food_morsel_savory(ent):
    rog.world().add_component(ent, cmp.Edible(
        func=None, sat=FOOD_MORSEL, taste=TASTE_SAVORY
        ))
def _food_morsel_bloody_nasty(ent):
    rog.world().add_component(ent, cmp.Edible(
        func=_bloody, sat=FOOD_MORSEL, taste=TASTE_NASTY
        ))
def _food_serving_savory(ent):
    rog.world().add_component(ent, cmp.Edible(
        func=None, sat=FOOD_SERVING, taste=TASTE_SAVORY
        ))
def _food_ration_savory(ent):
    rog.world().add_component(ent, cmp.Edible(
        func=None, sat=FOOD_RATION, taste=TASTE_SAVORY
        ))
def _food_meal_savory(ent):
    rog.world().add_component(ent, cmp.Edible(
        func=None, sat=FOOD_MEAL, taste=TASTE_SAVORY
        ))
def _food_bigMeal_savory(ent):
    rog.world().add_component(ent, cmp.Edible(
        func=None, sat=FOOD_BIGMEAL, taste=TASTE_SAVORY
        ))
def _food_cokenut(ent):
    def func(ent, eater):
        rog.poison(eater)
    rog.world().add_component(ent, cmp.Edible(
        func=func, sat=FOOD_MORSEL, taste=TASTE_BITTER
        ))
    rog.world().add_component(ent, cmp.Ingredient(ING_COKENUT))
def _food_sillyfruit(ent):
    def func(ent, eater):
        rog.confuse(eater)
    rog.world().add_component(ent, cmp.Edible(
        func=func, sat=FOOD_SERVING, taste=TASTE_SWEET
        ))

      
# effects #
    
def _wet(actor, n):
    if n>=10:
        rog.set_status(actor, WET)
def _oily(actor, n):
    if n>=10:
        rog.make(actor, OILY)
def _bloody(actor, n):
    if n>=10:
        rog.make(actor, BLOODY)
def _cough(actor, n):
    rog.cough(actor, n)
def _hydrate(actor, n):
    actor.hydration += n * WATER_HYDRATE
def _blood(actor, n):
    pass
def _acid(actor, n):
    rog.corrode(actor, n)
def _strongAcid(actor, n):
    rog.corrode(actor, n*3)
def _quaffAcid(actor, n):
    rog.corrode(actor, n*5)
def _quaffStrongAcid(actor, n):
    rog.corrode(actor, n*15)
def _sick(actor, n):
    rog.disease(actor, n)
def _drunk(actor, n):
    rog.intoxicate(actor, n)


# stuff #

def _wood(ent):
##    rog.make(ent, CANWET)
    pass
    
def _pot(ent): #metal pot
    rog.init_fluidContainer(ent, 200)
##    rog.make(tt, CANUSE)
##    tt.useFunctionPlayer = action.pot_pc
##    tt.useFunctionMonster = action.pot

def _clayPot(ent):
    rog.world().add_component(ent, cmp.FluidContainer(capacity=50))
    
def _gunpowder(ent):
    rog.world().add_component(ent, cmp.DiesInWater(func=None))

def _boxOfItems1(ent):
    rog.world().add_component(ent, cmp.Inventory(capacity=100))
    #newt=
    #rog.give(tt, newt)

def _safe(ent):
    world=rog.world()
    def funcPC(thing, actor):
        pass
    def funcNPC(thing, actor):
        pass
    world.add_component(ent, cmp.Interactable(funcPC,funcNPC))
    world.add_component(ent, cmp.Inventory(capacity=200))
    world.add_component(ent, cmp.Openable(isOpen=False,isLocked=True))
    
def _still(ent):
    world=rog.world()
    def funcPC(thing, actor):
        pass
    def funcNPC(thing, actor):
        pass
    world.add_component(ent, cmp.Interactable(funcPC,funcNPC))
    world.add_component(ent, cmp.FluidContainer(capacity=100))
    #...
    
def _dosimeter(tt):
    #use function two options: 1) toggles on/off. 2) displays a reading only when you use it.
    world=rog.world()
    def diesInWaterFunc(ent):
        world.delete_entity(ent)
    def funcDeath(ent):
        entn=world.component_for_entity(ent, cmp.Name)
        pos=world.component_for_entity(ent, cmp.Position)
        rog.explosion(entn.name, pos.x,pos.y, 1)
    def funcUsePC(self, ent): 
        pos=world.component_for_entity(ent, cmp.Position)
        reading = rog.radsat(pos.x,pos.y)
        rog.msg("The geiger counter reads '{} RADS'".format(reading))
        #could do, instead:
        # use turns it on, activates an observer.
        # updates when rad damage received by player. Adds rad value to dosimeter
        # when you use again, you can either read it or turn it off.
        rog.spendAP(ent, NRG_USE)
    def funcUseNPC(self, ent):
        rog.spendAP(ent, NRG_USE)
        pos=world.component_for_entity(ent, cmp.Position)
        rog.event_sight(pos.x,pos.y,"{t}{n} looks at a geiger counter.")
    statMods={cmp.CombatStats : {"rng":3,"atk":2,"dmg":1,},}
    world.add_component(ent, cmp.Usable(funcUsePC,funcUseNPC))
    world.add_component(ent, cmp.ReactsWithWater(diesInWaterFunc))
    world.add_component(ent, cmp.CanEquipInMainhandSlot(statMods))
    world.add_component(ent, cmp.DeathFunction(funcDeath))
    
def _towel(ent):
    world=rog.world()
    def funcPC(thing, actor):
        pass
    def funcNPC(thing, actor):
        pass
    statMods={cmp.BasisStats : {"rescold":20,},}
    world.add_component(ent, cmp.GetsWet(capacity=100))
    world.add_component(ent, cmp.Usable(funcPC,funcNPC))
    world.add_component(ent, cmp.CanEquipInBodySlot(statMods))
def _towel_wield(ent): #prepare a towel for wielding. Transforms it into a wielding item.
    statMods={cmp.CombatStats : {"atk":3, "dmg":1, "dfn":3,},}
    world.add_component(ent, cmp.CanEquipInMainhandSlot(statMods))
def _towel_wearOnHead(ent): #prepare a towel for headwear. Transforms it into head gear
    statMods={cmp.BasisStats : {"resbio":15,},}
    world.add_component(ent, cmp.CanEquipInHeadSlot(statMods))
    
def _torch(tt):
    rog.make(tt, CANEQUIP)
    tt.equipType=EQ_OFFHAND

def _extinguisher(tt):
    rog.make(tt, CANUSE)
##    tt.useFunctionPlayer = action.extinguisher_pc
##    tt.useFunctionMonster = action.extinguisher
    rog.makeEquip(tt, EQ_MAINHAND)
    tt.statMods = {"dmg":5, "asp":-33,}

def _lighter(tt):
    pass

def _grave(tt):
    rog.world().add_component(tt, cmp.Readable(random.choice(HISTORY_EPITAPHS)))



# creator functions #

#create a thing from STUFF; does not register thing
def create_stuff(ID, x, y):
    name,typ,mat,val,fgcol,hp,kg,solid,push,script = STUFF[ID]
    world = rog.world()
    if fgcol == "random":
        fgcol = random.choice(list(COL.keys()))
##    tt = thing.Thing(x,y, _type=typ,name=name,color=COL[fgcol])
##    tt.mass = kg
##    tt.material=mat
##    if lo: _hp(tt, lo)
##    tt.isSolid = solid
##    if push: rog.make(tt, CANPUSH)
##    #_applyResistancesFromMaterial(tt, mat)
##    return tt
    ent = world.create_entity(
        cmp.Name(name),
        cmp.Position(x,y),
        cmp.Draw(typ, fgcol=fgcol),
        cmp.Form(mass=kg, mat=mat, val=val),
        cmp.BasicStats(hp=hp,mp=hp),
        )
    if solid:
        rog.make(ent, ISSOLID)
    if push:
        rog.add_component(ent, cmp.Pushable())
    script(ent)
    return ent


#create a fluid
def create_fluid(x,y,ID,volume):
    ent = world.create_entity(cmp.Position(x,y),cmp.FluidContainer())
##    fluid.add(ID, volume)
    return ent


#non-weapon gear
#pass in the name of a gear item
#   quality = 0 to 1. Determines starting condition of the item
def create_gear(name,x,y,quality):
    world = rog.world()
    ent = world.create_entity()
    
    gData = GEAR[name]
    _type = get_gear_type(gData)
    value = get_gear_value(gData)
    mass = get_gear_mass(gData)
    hpmax = get_gear_hpmax(gData)
    material = get_gear_material(gData)
    dfn = get_gear_dfn(gData)
    arm = get_gear_arm(gData)
    msp = get_gear_msp(gData)
    sight = get_gear_sight(gData)
    resbio = get_gear_resbio(gData)
    resfire = get_gear_resfire(gData)
    reselec = get_gear_reselec(gData)
    resphys = get_gear_resphys(gData)
    script = get_gear_script(gData)

    fgcol = COL['accent']
    bgcol = COL['deep']
    
    world.add_component(ent, cmp.Name(name))
    world.add_component(ent, cmp.Position(x, y))
    world.add_component(ent, cmp.Draw(char=_type,fgcol=fgcol,bgcol=bgcol) )
    world.add_component(ent, cmp.Form(mass=mass, material=material, value=value))
    world.add_component(ent, cmp.BasicStats(
        hp=hpmax,mp=hpmax,
        resfire=resfire,resbio=resbio,reselec=reselec,resphys=resphys
        ) )

    #stat mod dictionaries
    #{component : {var : modf}}
    basicStatsDict = {}
    combatDict = {}
    sightDict = {}
    if resbio: basicStatsDict.update({"resbio":resbio})
    if resfire: basicStatsDict.update({"resfire":resfire})
    if reselec: basicStatsDict.update({"reselec":reselec})
    if resphys: basicStatsDict.update({"resphys":resphys})
    if dfn: combatDict.update({"dfn":dfn})
    if arm: combatDict.update({"arm":arm})
    if msp: combatDict.update({"msp":msp})
    if sight: sightDict.update({"sight":sight})
    modDict = {}
    if not basicStatsDict == {}: modDict.update({cmp.BasicStats : basicStatsDict})
    if not combatDict == {}: modDict.update({cmp.CombatStats : combatDict})
    if not sightDict == {}: modDict.update({cmp.SenseSight : sightDict})
        
    if _type == ARMR:
        world.add_component(ent, cmp.CanEquipInBodySlot(modDict))
    elif _type == HELM:
        world.add_component(ent, cmp.CanEquipInHeadSlot(modDict))
    elif _type == BACK:
        world.add_component(ent, cmp.CanEquipInBackSlot(modDict))
    
    #item resistances based on material??? How to do this?

    if script: script(ent)
    return ent
#


def create_weapon(name, x,y):
    world = rog.world()
    ent = world.create_entity()
    
    data = WEAPONS[name]
    _type       = get_weapon_type(data)
    value       = get_weapon_value(data)
    mass        = get_weapon_mass(data)
    hpmax       = get_weapon_hpmax(data)
    capacity    = get_weapon_capacity(data)
    reloadTime  = get_weapon_rt(data)
    jamChance   = get_weapon_jam(data)
    material    = get_weapon_mat(data)
    rng         = get_weapon_range(data)
    atk         = get_weapon_atk(data)
    dmg         = get_weapon_dmg(data)
    _pow        = get_weapon_pow(data)
    dfn         = get_weapon_dfn(data)
    arm         = get_weapon_arm(data)
    asp         = get_weapon_asp(data)
    msp         = get_weapon_msp(data)
    elem        = get_weapon_elem(data)
    ammo        = get_weapon_ammo(data)
    flags       = get_weapon_flags(data)
    script      = get_weapon_script(data)
    physDmg = dmg if elem == ELEM_PHYS else 0
    
    fgcol = COL['accent']
    bgcol = COL['deep']
    
    world.add_component(ent, cmp.Name(name))
    world.add_component(ent, cmp.Position(x, y))
    world.add_component(ent, cmp.Draw( char=_type, fgcol=fgcol, bgcol=bgcol ))
    world.add_component(ent, cmp.Form( mass=mass, material=material, value=value ))
    world.add_component(ent, cmp.BasicStats(
        hp=hpmax,mp=hpmax,
        #resfire=resfire,resbio=resbio,reselec=reselec,resphys=resphys
        ))

    ammoDict={}
    mainhandDict={}
    elementalDict={}
    if ammoType: ammoDict.update({'ammoType':ammoType})
    if capacity: ammoDict.update({'capacity':capacity})
    if reloadTime: ammoDict.update({'reloadTime':reloadTime})
    if jamChance: ammoDict.update({'jamChance':jamChance})
    if rng: mainhandDict.update({'rng':rng})
    if atk: mainhandDict.update({'atk':atk})
    if dmg: mainhandDict.update({'dmg':dmg})
    if _pow: mainhandDict.update({'pow':_pow})
    if dfn: mainhandDict.update({'dfn':dfn})
    if arm: mainhandDict.update({'arm':arm})
    if asp: mainhandDict.update({'asp':asp})
    if msp: mainhandDict.update({'msp':msp})
    if elem: elementalDict.update({'element':elem})

    modDict={}
    if not ammoDict == {}: modDict.update({cmp.Ammo : ammoDict})
    if not mainhandDict == {}: modDict.update({cmp.CombatStats : mainhandDict})
    world.add_component(ent, cmp.CanEquipInMainhand(modDict))
    if not elementalDict == {}: world.add_component(ent, cmp.ElementalDamage(elementalDict))
    
    for flag in flags:
        rog.make(ent, flag)

    if script: script(weap)
    return weap


''' TODO: refactor
def create_creature(name, typ, xs,ys, col):
    creat=Thing()
    creat.name          = name
    creat.type          = typ
    creat.mask          = typ
    creat.x             = xs
    creat.y             = ys
    creat.color         = col
    creat.material      = MAT_FLESH
    creat.isCreature    = True
    creat.mutations     = 0
    creat.gender        = dice.roll(2) - 1
    creat.fov_map       = rog.fov_init()
    creat.path          = rog.path_init_movement()
    return creat

def create_corpse(obj):
    corpse=Thing()
    corpse.name     = "corpse of {}".format(obj.name)
    corpse.type     = "%"
    corpse.mask     = corpse.type
    corpse.x        = obj.x
    corpse.y        = obj.y
    corpse.color    = obj.color
    corpse.material = obj.material
    corpse.stats.hpmax = int(obj.mass) + 1
    corpse.stats.resfire= obj.stats.resfire
    corpse.stats.resbio = obj.stats.resbio
    corpse.stats.reselec= obj.stats.reselec
    corpse.stats.temp   = obj.stats.temp
    #copy status effects?
    rog.copyflags(corpse, obj, copyStatusFlags=False)
    rog.givehp(corpse)
    return corpse

def create_ashes(obj):
    if obj.mass < 1: return
    ashes=Thing()
    ashes.name      = "ashes"
    ashes.type      = T_DUST
    ashes.mask      = ashes.type
    ashes.x         = obj.x
    ashes.y         = obj.y
    ashes.color     = COL['white']
    ashes.material  = MAT_DUST
    ashes.mass      = max(0.5, int(obj.mass/20))
    ashes.stats.resfire = 100
    ashes.stats.resbio  = 100
    ashes.stats.reselec = 100
    return ashes
'''





# ITEM DEFINITIONS #


# MONSTERS #


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

'@' : ('human',                 (20, 20, 5, 2, 2, 0, 100,100,100, 25, 25, 25, 20, 100, 60,  65, 500, ),(CANEAT,),),
'a' : ('abomination',           (16, 8,  0, 4, -8,2, 100,90, 110, 50, 50, 25, 6,  0,   30,  80, 0,  ),(),),
'b' : ('bug-eyed business guy', (20, 30, 5, 2, 2, 0, 150,120,100, 50, 50, 20, 30, 100, 90,  60, 500, ),(CANEAT,),),
'B' : ('butcher',               (50, 20, 5, 6, -4,0, 100,100,100, 60, 50, 50, 10, 100, 90,  130,300, ),(CANEAT,),),
'L' : ('raving lunatic',        (12, 25, 3, 2, 2, 0, 100,100,100, 25, 15, 30, 10, 0,   60,  50, 0, ),(),), #BABBLES,
'r' : ('ravaged',               (4,  1,  1, 2, -8,-1,100,80, 70,   0,  0, 0,  10, 0,   15,  35, 0,  ),(RAVAGED,),),
'R' : ('orctepus',              (15, 5,  6, 2,-12,0, 100,80, 145,  0, 80, 0,  8,  0,   120, 100,0,  ),(CANEAT,),),
's' : ('slithera',              (6,  15, 10,4, -4,0, 100,33, 150,  0, 50, 5,  5,  0,   35,  30, 0, ),(CANEAT,),),
'U' : ('obese scrupula',        (20, 2,  4, 8,-16,3, 100,50, 90,  20, 65, 60, 10, 0,   85,  140,100,  ),(),),
'V' : ('ash vampire',           (50, 80, 8, 5, 8, 0, 100,120,100, 10, 75, 5,  5,  200, 60,  30, 1000,  ),(MEAN,NVISION,),),
'w' : ('dire wolf',             (12, 3,  12,5, 8, 0, 100,225,115, 15, 15, 15, 15, 0,   20,  50, 0,  ),(RAVAGED,),),
'W' : ('whipmaster',            (24, 10, 5, 5, 4, 2, 100,80, 100, 25, 60, 10, 15, 0,   75,  75, 1000, ),(MEAN,NVISION,),),
'z' : ('zombie',                (8,  1,  0, 3,-12,-1,50, 40, 100, 10, 25, 55, 5,  0,   30,  45, 0,  ),(MEAN,),),


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


# GEAR #

''' #Columns:
    #   $$$$$   cost
    #   KG      mass
    #   Dur     durability
    #   Mat     material
    #   DV      Dodge Value
    #   AV      Armor Value
    #   Msp     Move Speed
    #   Vis     Vision
    #   FIR     Fire Resist
    #   BIO     Bio Resist
'''
GEAR = {
#--Name-------------------Type,$$$$$, KG,   Dur, Mat, (DV, AV, MSp, Vis,FIR,BIO,ELE,PHS), script
    #Back
"cloak"                 :(BACK,420,   6.0,  150, CLTH,( 4,  1, -3,  0,  10, 10, 0,  0,), _cloak,),
"fire blanket"          :(BACK,600,   12.4, 175, CLTH,(-4,  1, -9,  0,  150,33, 9,  0,), _fireBlanket,),
    #Armor
"t-shirt"               :(ARMR,40,    0.12, 50,  CLTH,( 1,  0,  0,  0,  -10,15, 0,  0,), None,),
"skin suit"             :(ARMR,450,   14.7, 90,  FLSH,( 2,  1, -6,  0,  0,  15, 3,  0,), None,),
"bone armor"            :(ARMR,790,   27.8, 475, BONE,(-4,  4, -18, 0,  15, 25, 0,  0,), None,),
"carb garb"             :(ARMR,860,   22.5, 600, CARB,(-2,  3, -12, 0,  10, 15, 6,  0,), None,),
"textile armor"         :(ARMR,950,   15.6, 125, CLTH,( 1,  2, -3,  0,  5,  40, 3,  0,), None,),
"boiled leather plate"  :(ARMR,2075,  12.5, 180, LETH,( 2,  3, -3,  0,  10, 25, 15, 0,), None,),
"riot gear"             :(ARMR,3490,  20.5, 500, CARB,(-1,  4, -12, 0,  25, 25, 25, 0,), None,),
"metal gear"            :(ARMR,9950,  27.5, 740, METL,(-3,  5, -18, 0,  -10,15, -25,0,), None,),
"full metal suit"       :(ARMR,12000, 35.1, 850, METL,(-4,  6, -21, 0,  -15,15, -50,0,), None,),
"graphene armor"        :(ARMR,58250, 16.5, 900, CARB,(-2,  5, -9,  0,  30, 50, 30, 0,), None,),
"bullet-proof armor"    :(ARMR,135000,12.8, 1000,CARB,( 0,  8, -3,  0,  5,  10, 0,  0,), None,),
"hazard suit"           :(ARMR,2445,  14.5, 75,  PLAS,(-8,  1, -24, 0,  15, 200,12, 0,), None,),
"disposable PPE"        :(ARMR,110,   9.25, 25,  PLAS,(-6,  0, -15, 0,  -25,100,3,  0,), None,),
"wetsuit"               :(ARMR,1600,  8.2,  50,  PLAS,(-1,  0, -6,  0,  50, 20, 21, 0,), None,),
"burn jacket"           :(ARMR,1965,  19.5, 150, CLTH,(-5,  2, -12, 0,  200 33, 15, 0,), None,),
"space suit"            :(ARMR,35490, 40.0, 50,  CARB,(-8,  2, -33, 0,  10, 100,6,  0,), None,),
    #Helmets
"bandana"               :(HELM,40,    0.1,  20,  CLTH,( 2,  0,  0,  0,  5,  10, 3,  0,), None,),
"skin mask"             :(HELM,180,   1.25, 10,  FLSH,( 1,  0,  0,  -1, 0,  5,  0,  0,), None,),
"wood mask"             :(HELM,10,    1.0,  30,  WOOD,( 0,  1,  0,  -5, -5, 5,  3,  0,), None,),
"skull helm"            :(HELM,750,   2.8,  115, BONE,(-2,  2, -6,  -3, 5,  5,  6,  0,), None,),
"motorcycle helmet"     :(HELM,1500,  0.75, 145, PLAS,( 0,  2,  0,  -3, 0,  5,  6,  0,), None,),
"metal helm"            :(HELM,8500,  3.0,  300, METL,(-3,  3, -6,  -10,0,  5,  -12,0,), None,),
"graphene mask"         :(HELM,21850, 0.8,  285, CARB,( 0,  2,  0,  -7, 5,  8,  9,  0,), None,),
"graphene helmet"       :(HELM,25450, 1.2,  310, CARB,(-1,  3, -3,  -7, 6,  10, 9,  0,), None,),
"kevlar hat"            :(HELM,89500, 1.5,  350, CARB,( 0,  4,  0,  0,  0,  0,  0,  0,), None,),
"respirator"            :(HELM,2490,  1.7,  25,  PLAS,(-1,  0, -3,  0,  13, 27, 3,  0,), None,),
"gas mask"              :(HELM,19450, 2.5,  30,  PLAS,(-1,  0, -6,  -1, 8,  36, 6,  0,), None,),
"space helmet"          :(HELM,21950, 3.5,  40,  CARB,(-3,  1, -12, -5, 10, 22, 6,  0,), None,),
#"night vision goggles"
#"ear plugs"
    }


WEAPONS = {
# Type              Weapon type
# $$$, KG, Dur      Value, mass, durability
# Cap               Ammo Capacity (for ranged weapons)
# Mat               Material
# Rn                Range/Accuracy (for ranged weapons or for throwing weapons),
# At,Dm,Pw          Attack, Damage (melee/throwing), Power (ranged weapon damage),
# DV,AV,            Dodge Value, Armor Value,
# Asp,Msp           Attack Speed, Move Speed,
# EL                Element (damage type)
# Ammo              Ammunition / Fuel required to use weapon
    
    # melee weapons / throwing weapons. Organized roughly by category of weapon
# Name     ##------- Type, $$$$, KG,  Dur, Cap,RT, Jam,Mat, (Rn,At,Dm,Pw, DV, AV, Asp,Msp,EL),Ammo,Flags,script
"stone"             :(TSTO,1,    0.25,50,  0,  0,  0,  STON,(10,2, 5, 0,  0,  0, -40, 0, PH,),None,(CRUSHES,), None,),
"stick"             :(MEL, 1,    0.6, 40,  0,  0,  0,  WOOD,(8, 4, 2, 0,  1,  0,  5, -3, PH,),None,(), None,),
"bone"              :(MEL, 1,    0.25,120, 0,  0,  0,  BONE,(8, 5, 4, 0,  2,  0,  5,  0, PH,),None,(CRUSHES,), None,),
"wooden plank"      :(MEL, 2,    1.2, 80,  0,  0,  0,  WOOD,(5, 5, 3, 0,  2,  0, -36,-6, PH,),None,(CRUSHES,), None,),
"fork"              :(MEL, 3,    0.05,65,  0,  0,  0,  METL,(3, 4, 1, 0,  0,  0,  10, 0, PH,),None,(STABS,), None,),
"throwing star"     :(MEL, 5,    0.1, 10,  0,  0,  0,  METL,(12,12,1, 0,  0,  0,  33, 0, PH,),None,(STABS,), None,),
"throwing dart"     :(MEL, 6,    0.2, 10,  0,  0,  0,  METL,(12,10,2, 0,  0,  0,  0,  0, PH,),None,(STABS,), None,),
"war frisbee"       :(MEL, 8,    0.4, 5,   0,  0,  0,  PLAS,(14,8, 4, 0,  0,  0, -10,-3, PH,),None,(CUTS,), None,),
"cudgel"            :(MEL, 3,    1.5, 520, 0,  0,  0,  WOOD,(5, 2, 9, 0,  0,  0, -33,-12,PH,),None,(CRUSHES,), None,),
"hammer"            :(MEL, 20,   1.15,550, 0,  0,  0,  WOOD,(8, 4, 11,0,  0,  0, -33,-9, PH,),None,(CRUSHES,), None,),
"flail"             :(MEL, 45,   1.5, 250, 0,  0,  0,  METL,(1, 2, 16,0,  -1, 0, -45,-9, PH,),None,(CRUSHES,), None,),
"baton"             :(MEL, 50,   0.75,330, 0,  0,  0,  PLAS,(5, 5, 3, 0,  2,  0,  15,-3, PH,),None,(CRUSHES,), None,),
"crowbar"           :(MEL, 66,   0.8, 750, 0,  0,  0,  METL,(5, 5, 10,0,  0,  0, -33,-3, PH,),None,(CRUSHES,), None,),
"stone axe"         :(MEL, 5,    1.55,40,  0,  0,  0,  WOOD,(6, 1, 11,0,  0,  0, -25,-9, PH,),None,(CHOPS,), None,),
"metal axe"         :(MEL, 25,   1.25,420, 0,  0,  0,  WOOD,(8, 3, 13,0,  0,  0, -25,-9, PH,),None,(CHOPS,CUTS,), None,),
"throwing axe"      :(MEL, 20,   0.8, 50,  0,  0,  0,  METL,(10,9, 9, 0,  0,  0, -20,-6, PH,),None,(CHOPS,CUTS,), None,),
"shortspear"        :(MEL, 8,    0.75,60,  0,  0,  0,  WOOD,(8, 9, 7, 0,  1,  0,  40,-9, PH,),None,(STABS,), None,),
"javelin"           :(MEL, 10,   0.5, 20,  0,  0,  0,  WOOD,(16,12,6, 0,  2,  0,  33,-9, PH,),None,(REACH,STABS,), None,),
"staff"             :(MEL, 15,   1.4, 220, 0,  0,  0,  WOOD,(8, 6, 6, 0,  3,  0,  33,-18,PH,),None,(REACH,), None,),
"wooden spear"      :(MEL, 18,   1.25,65,  0,  0,  0,  WOOD,(12,12,7, 0,  3,  0,  33,-18,PH,),None,(REACH,STABS,CUTS,), None,),
"bone spear"        :(MEL, 32,   1.1, 80,  0,  0,  0,  WOOD,(12,12,8, 0,  3,  0,  33,-18,PH,),None,(REACH,STABS,CUTS,), None,),
"metal spear"       :(MEL, 75,   1.3, 100, 0,  0,  0,  WOOD,(12,12,9, 0,  3,  0,  33,-18,PH,),None,(REACH,STABS,CUTS,), None,),
"wooden sword"      :(MEL, 52,   1.0, 60,  0,  0,  0,  WOOD,(5, 9, 3, 0,  4,  0,  20,-6, PH,),None,(CRUSHES,), None,),
"metal sword"       :(MEL, 360,  1.25,160, 0,  0,  0,  METL,(8, 15,8, 0,  5,  0,  25,-6, PH,),None,(CUTS,STABS,CHOPS,), None,),
"bone knife"        :(MEL, 22,   0.2, 30,  0,  0,  0,  BONE,(10,14,5, 0,  1,  0,  40, 0, PH,),None,(CUTS,STABS,), None,),
"pocket knife"      :(MEL, 95,   0.2, 75,  0,  0,  0,  METL,(10,14,5, 0,  1,  0,  40, 0, PH,),None,(CUTS,STABS,), None,),
"bayonet"           :(MEL, 175,  0.3, 80,  0,  0,  0,  METL,(10,14,5, 0,  3,  0,  40, 0, PH,),None,(CUTS,STABS,), None,),
"dagger"            :(MEL, 205,  0.4, 200, 0,  0,  0,  METL,(10,16,5, 0,  4,  0,  40, 0, PH,),None,(CUTS,STABS,), None,),
"scalpel"           :(MEL, 240,  0.05,10,  0,  0,  0,  METL,(1, 20,6, 0,  0,  0,  40, 0, PH,),None,(CUTS,STABS,), None,),
#chainsaw
#plasma sword

    # shields
# Name     ##------- Type, $$$$, KG,  Dur, Cap,RT, Jam,Mat, (Rn,At,Dm,Pw, DV, AV, Asp,Msp,EL),Ammo,Flags,script
"wooden shield"     :(OFF, 185,  5.3, 520, 0,  0,  0,  WOOD,(3, 0, 1, 0,  5,  3,  0, -18,PH,),None,(CRUSHES,), None,),
"metal shield"      :(OFF, 340,  7.5, 900, 0,  0,  0,  METL,(1, 0, 1, 0,  3,  5,  0, -24,PH,),None,(CRUSHES,), None,),
"riot shield"       :(OFF, 2250, 8.2, 450, 0,  0,  0,  PLAS,(1, 0, 0, 0,  2,  7,  0, -27,PH,),None,(CRUSHES,), None,),

    # ranged weapons
# Name     ##------- Type, $$$$, KG,  Dur, Cap,RT, Jam,Mat, (Rn,At,Dm,Pw, DV, AV, Asp,Msp,EL),Ammo,Flags,script
"sling"             :(SLNG,3,    0.05,30,  1,  1,  0,  ROPE,(20,10,-3,5,  0,  0, -33, 0,PH,),A_SLING,(), None,),
"hunting bow"       :(BOW, 30,   0.8, 35,  1,  1,  0,  WOOD,(16,6, -3,0,  0,  0, -10,-3,PH,),A_ARRO,(), None,),
"short bow"         :(BOW, 110,  1.1, 40,  1,  1,  0,  WOOD,(20,12,-3,2,  0,  0, -25,-6,PH,),A_ARRO,(), None,),
"longbow"           :(BOW, 160,  1.8, 45,  1,  1,  0,  WOOD,(36,16,-3,6,  0,  0, -33,-12,PH,),A_ARRO,(), None,),
"composite bow"     :(BOW, 325,  1.2, 50,  1,  1,  0,  BONE,(33,14,-3,4,  0,  0, -25,-6,PH,),A_ARRO,(), None,),

    # exposives
# Name     ##------- Type, $$$$, KG,  Dur, Cap,RT, Jam,Mat, (Rn,At,Dm,Pw, DV, AV, Asp,Msp,EL),Ammo,Flags,script
##"smoke bomb"        :(EXPL,50,   1.2, 1,   0,  0,  0,  METL,(8, 3, 2, 0,  0,  0,  0, 0, PH,),None,(), _molotov,),
##"flashbang"         :(EXPL,50,   1.2, 1,   0,  0,  0,  METL,(8, 3, 2, 0,  0,  0,  0, 0, PH,),None,(), _molotov,),
"molotov"           :(EXPL,50,   1.2, 1,   0,  0,  0,  METL,(8, 3, 2, 0,  0,  0,  0, 0, PH,),None,(), _molotov,),
"frag grenade"      :(EXPL,165,  0.8, 20,  0,  0,  0,  METL,(10,3, 2, 0,  0,  0,  0, 0, PH,),None,(), _fragBomb,),
"land mine"         :(EXPL,425,  4.0, 5,   0,  0,  0,  METL,(3, 0, 1, 0,  0,  0,  0, -12,PH,),None,(), _fragMine,),
##"remote-detonated bomb":(EXPL,75,   2.5, 3,   0,  0,  0,  METL,(8, 3, 1, 1,  -1, 0, -10,-6,PH,),None,(), _ied,),

    # heavy weapons
# Name     ##------- Type, $$$$, KG,  Dur, Cap,RT, Jam,Mat, (Rn,At,Dm,Pw, DV, AV, Asp,Msp,EL),Ammo,Flags,script
"spring cannon"     :(HEVY,360,  7.3, 75,  1,  4,  0,  METL,(8, 5, 1, 4,  -5, 0, -33,-21,PH,),A_ANY,(CRUSHES,), None,),
"MK-18 shitstormer" :(HEVY,1290, 2.5, 220, 100,3,  0,  PLAS,(7, 3, 1, 25, -4, 0,  0, -15,BI,),A_HAZM,(CRUSHES,), None,),
"raingun"           :(HEVY,2290, 2.85,175, 125,3,  0,  PLAS,(7, 5, 1, 40, -4, 0,  0, -18,CH,),A_ACID,(CRUSHES,), None,),
"supersoaker 9000"  :(HEVY,3750, 3.5, 100, 200,5,  0,  PLAS,(9, 5, 0, 3,  -4, 0,  10,-18,None,),A_FLUID,(CRUSHES,), None,),
"flamethrower"      :(HEVY,4800, 12.7,100, 300,8,  0,  METL,(5, 5, 1, 100,-4, 0,  33,-40,FI,),A_FLAM,(CRUSHES,), None,), #_flamethrower
#"napalm thrower"      :(HEVY,5800, 12.7,100, 300,8,  0,  METL,(5, 15,2, 100,-15,0,  33,-40,FI,),A_FLAM,(),), #_flamethrower
#"compressed air gun":(HEVY,215, 5.5,50, 1, 6,  0,  PLAS,(5, 15,2, 8,-15,0,  33,-40,PH,),A_FLAM,(),), #_flamethrower

    # guns
# Name     ##------- Type, $$$$, KG,  Dur, Cap,RT, Jam,Mat, (Rn,At,Dm,Pw, DV, AV, Asp,Msp,EL),Ammo,Flags,script
"hand cannon"       :(GUN, 145,  8.75,450, 1,  10, 15, METL,(5, 6, 4, 12, -4, 1, -50,-30,PH,),A_BULL,(CRUSHES,), None,),
"musket"            :(GUN, 975,  2.5, 120, 1,  8,  8,  WOOD,(8, 6, 4, 8,  -1, 0, -33,-12,PH,),A_BULL,(CRUSHES,), None,),
"flintlock pistol"  :(GUN, 1350, 1.3, 150, 1,  8,  12, WOOD,(10,6, 3, 1,   0, 0, -25,-3, PH,),A_BULL,(CRUSHES,), None,),
"revolver"          :(GUN, 3990, 1.1, 360, 6,  1,  8,  METL,(12,8, 3, 2,   0, 0, -15,-3, PH,),A_CART,(CRUSHES,), None,),
"rifle"             :(GUN, 4575, 2.2, 280, 1,  1,  8,  WOOD,(20,15,4, 6,  -1, 0, -33,-12,PH,),A_CART,(CRUSHES,), None,),
"repeater"          :(GUN, 13450,2.0, 300, 7,  1,  7,  WOOD,(20,13,4, 5,  -1, 0, -15,-9, PH,),A_CART,(CRUSHES,), None,),
"'03 Springfield"   :(GUN, 26900,2.5, 350, 5,  1,  6,  WOOD,(36,20,4, 10, -1, 0, -33,-12,PH,),A_CART,(CRUSHES,), None,),
"luger"             :(GUN, 55450,0.9, 210, 8,  1,  10, METL,(18,12,3, 4,   0, 0, -6, -3, PH,),A_CART,(CRUSHES,), None,),
"shotgun"           :(GUN, 2150, 2.0, 325, 1,  1,  8,  WOOD,(8, 8, 4, 4,  -1, 0, -33,-9, PH,),A_SHOT,(CRUSHES,), None,),
"dbl.barrel shotgun":(GUN, 6200, 2.8, 285, 2,  1,  8,  WOOD,(8, 8, 4, 4,  -1, 0, -33,-12,PH,),A_SHOT,(CRUSHES,), None,),

    # energy weapons
# Name     ##------- Type, $$$$, KG,  Dur, Cap,RT, Jam,Mat, (Rn,At,Dm,Pw, DV, AV, Asp,Msp,EL),Ammo,Flags,script
"battery gun"       :(ENER,3250, 4.20,175, 20, 1,  0,  PLAS,(2, 40,2, 70, -4,  0, -60,-24,EL,),A_ELEC,(),),
#"laser pointer"
#"beam rifle"
#"taser"
#"megaphone"
#"paralysis ray"

#"grenade launcher"  :(HEVY,45910,8.2, 200, 1,  3,  0,  METL,(12,5, 0, 4,  -15,0, -33,-30,PH,),A_GREN,(),),
}
#add extra weapons (variations)
##BAYONETS=("musket","rifle","shotgun","'03 Springfield",)
##for wpn in BAYONETS:
####    _stats = WEAPONS[wpn]
####    bayonetDmg = 4
####    _stats.update( {set_weapon_dmg() : get_weapon_dmg(WEAPONS[wpn]) + bayonetDmg} )
##    WEAPONS.update( {"{} with bayonet".format(wpn) : _stats} ))


AMMUNITION={
# Attributes:
#   type        ammo type
#   $$$, KG     value, mass
#   n           number shots
#   Acc, Atk, Dmg, Asp      Range, Attack, Damage, Attack Speed
# name                  : type,  $$$, KG, n, (Acc,Atk,Dmg,Asp,),script
##hollow arrows
"metal ball"            :(A_BULL,2,  0.1, 1, (-2, 0,  4,  0,), None,)
"Minni ball"            :(A_BULL,3,  0.1, 1, (0,  2,  6,  0,), None,)
"paper cartridge"       :(A_BULL,4,  0.15,1, (0,  2,  6,  0,), _paperCartridge,)
"shotgun shell"         :(A_SHOT,6,  0.1, 5, (-2, -5, 0,  0,), None,)
"shotgun slug"          :(A_SHOT,8,  0.1, 1, (0,  0,  15, -10,), None,)
"pistol cartridge"      :(A_CART,6,  0.02,1, (0,  2,  4,  0,), None,)
"magnum cartridge"      :(A_CART,16, 0.03,1, (-2, 5,  10, -33,), None,)
"rifle cartridge"       :(A_CART,15, 0.04,1, (10, 8,  7,  -15,), None,)
"hollow-point cartridge":(A_CART,12, 0.03,1, (-5, -4, 12, -15,), None,)
"incendiary cartridge"  :(A_CART,36, 0.04,1, (-2, 12, 16, -33,), _incendiary)
    }


FOOD = {
# Columns:
#   $$$         cost
#   KG          mass
#   Mat         material
#   script      script to run to initialize values for the food item
#--Name-------------------$$$,  KG,   Mat,  script
"Corpse Button"         :(1,    0.03, FUNG, _food_morsel_bloody_nasty,),
"Hack Leaf"             :(1,    0.02, VEGG, _food_morsel_bitter,),
"Juniper Berry"         :(3,    0.01, VEGG, _food_morsel_sweet,),
"Coke Nut"              :(12,   0.02, WOOD, _food_cokenut,),
"Silly Fruit"           :(8,    0.04, VEGG, _food_sillyfruit,),
"Mole Rat Meat"         :(10,   0.15, FLSH, _food_ration_savory,),
"Dwarf Giant Cap"       :(25,   0.05, FUNG, _food_ration_savory,),
"Eel Meat"              :(20,   0.50, FLSH, _food_meal_savory,),
"Human Meat"            :(40,   1.00, FLSH, _food_meal_savory,),
"Infant Meat"           :(80,   0.50, FLSH, _food_meal_savory,),
"Giant Cap"             :(100,  0.35, FUNG, _food_meal_savory,),
"MRE"                   :(60,   1.0,  FUNG, _food_meal_gamble,),
    }

STUFF={
#flag           : name                  type,material,value,color, HP, kg, solid,push?,script,
#THG.CLOAK
#THG.GENERATOR
#THG.TINDER
THG.LIGHTER     :("disposable lighter", T_DEVICE,PLAS,650, 'random',2, 0.1,False,False, _lighter,),
THG.SAFE        :("safe",               T_BOX,  METL, 1500,'metal', 2000,420,True,False,  _safe,),
##THG.TURRET      :("turret",           T_TURRET,METL,300, 'gray', 80, 55, False,False,_turret,),
THG.GUNPOWDER   :("pinch of gunpowder", T_DUST, GUNP, 1,    'gray', 1, 0.01,False,False,_gunpowder,),
THG.GORE        :("hunk of flesh",      T_MEAL, FLSH, 0,    'red',  1, 1,   False,False,_food_meal_savory,),
THG.LOG         :("log",                T_LOG,  WOOD, 5,   'brown',1000,100,False,False,_wood,),
THG.WOOD        :("wood",               T_WOOD, WOOD, 1,   'brown',200,5,   False,False,_wood,),
THG.BOX         :("crate",              T_BOX,  WOOD, 10,  'brown',200,50,  True,True,  _boxOfItems1,),
THG.GRAVE       :("grave",              T_GRAVE,STON, 15, 'silver',300,300,True,False, _grave,),
THG.POT         :("metal pot",          T_POT,  METL, 120,'metal', 800,100,True,True, _pot,),
THG.CLAYPOT     :("clay pot",           T_MISC, STON, 20, 'scarlet',10,5, False,False, _clayPot,),
THG.STILL       :("still",              T_STILL,METL, 200,'metal', 5, 100,True,False, _still,),
THG.TORCH       :("torch",              T_TORCH,WOOD, 10, 'brown',350,1.1, False,False,_torch,),
THG.DOSIMETER   :("geiger counter",     T_DEVICE,METL,1350,'yellow',5,0.5, False,False,_dosimeter,),
THG.EXTINGUISHER:("fire extinguisher",  T_DEVICE,METL,680, 'red',  8,8, False,False,_extinguisher,),
THG.TOWEL       :("towel",              T_TOWEL,CLTH, 50, 'accent',10,0.8,False,False,_towel,),
    }

JOBS = {
    # KG, $$$: mass, money
    #Access keys:
    #S  level of security clearance
    #Keys:
        #J  janitor's closets
        #C  computer closets
        #K  key to the city
        #P  hangar access
        #L  lab access
    #stats: additional stat bonuses or nerfs
    #skills: starting skills
#ID                Char,Name         KG, $$$$,S|Key--------stats---------------skills
CLS_ATHLETE     : ("A", "athlete",   70, 300, 0,'', {'msp':20,'dfn':4,'carry':15,},(SKL_ATHLET,),),
CLS_CHEMIST     : ("C", "chemist",   60, 500, 2,'L',{'hpmax':-5,'mpmax':5,},(SKL_CHEMIS,),),
CLS_DEPRIVED    : ("d", "deprived",  40, 0,   0,'', {'hpmax':-5,'mpmax':-5,'atk':-5,},(),),
CLS_ENGINEER    : ("E", "engineer",  60, 500, 0,'C',{'hpmax':5,'carry':10,},(SKL_ROBOTS,),),
CLS_JANITOR     : ("j", "janitor",   60, 100, 0,'J',{},(),),
CLS_SECURITY    : ("O", "security",  75, 300, 4,'', {'atk':3,},(SKL_ENERGY,),),
CLS_PILOT       : ("p", "pilot",     60, 500, 0,'P',{'sight':10,},(SKL_PILOT,),),
CLS_POLITICIAN  : ("I", "politician",60, 1000,3,'K',{'hpmax':-5,'mpmax':-5,},(SKL_PERSUA),),
CLS_RIOTPOLICE  : ("P", "police",    75, 300, 3,'', {'hpmax':5,'mpmax':-5,'atk':3,'asp':10,},(SKL_FIGHT,SKL_ENERGY,),),
CLS_SMUGGLER    : ("u", "smuggler",  60, 1000,0,'', {'hpmax':5,'carry':10,},(SKL_PERSUA,SKL_GUNS,),),
CLS_SOLDIER     : ("S", "soldier",   90, 300, 1,'', {'hpmax':10,'mpmax':-5,'atk':5,'asp':15,'msp':10,'carry':20,},(SKL_HEAVY,SKL_GUNS,),),
CLS_TECHNICIAN  : ("T", "technician",60, 500, 1,'', {'mpmax':5,},(SKL_COMPUT,),),
CLS_THIEF       : ("t", "thief",     60, 1000,0,'', {'mpmax':-5,'dfn':2,'msp':10,'carry':15,},(SKL_SNEAK,),),
    }

FLUIDS = {
#attributes:
#   d       : density
#   v       : viscosity
#   kg      : mass
#   flamm   : flammable?
#   snuff   : snuffs out fires?
#  ID       : (    type,   name,      color,          d,    v,    kg,  flamm,snuff,touch,quaff,
FL_SMOKE    : Data(T_GAS,  "smoke",   COL['white'],   0.05, 0.01, 0.01,False,False,None, _cough,),
FL_WATER    : Data(T_FLUID,"water",   COL['blue'],    1,    1,    0.1, False,True, _wet, _hydrate,),
FL_BLOOD    : Data(T_FLUID,"blood",   COL['red'],     1.1,  2,    0.12,False,True, _bloody,_blood,),
FL_ACID     : Data(T_FLUID,"acid",    COL['green'],   1.21, 0.6,  0.2, False,False,_acid,_quaffAcid,),
FL_STRONGACID:Data(T_FLUID,"strong acid",COL['bio'],  1.3,  0.9,  0.2, False,False,_strongAcid,_quaffStrongAcid,),
FL_OIL      : Data(T_FLUID,"oil",  COL['truepurple'], 0.9,  3,    0.3, True,False, _oily, _sick,),
FL_ALCOHOL  : Data(T_FLUID,"moonshine",COL['gold'],   1.2,  0.8,  0.15,True,False, _wet, _drunk,),
#FL_LAVA
#FL_HEALING
#FL_CONFU
#FL_DRUNK
#FL_BLIND
#FL_SLOW
#FL_IRRIT
#FL_SICK
    }
FLUID_COMBONAMES={
FL_SMOKE    : "smokey",
FL_WATER    : "watery",
FL_BLOOD    : "bloody",
FL_ACID     : "acidic",
FL_STRONGACID: "acidic",
FL_OIL      : "oily",
FL_ALCOHOL  : "alcoholic",
    }
















                    # commented out code below.








'''
"spring-blade"      :(MEL, 9660, 2.8, 150, CARB,(0, 0,  8, 22, -2,  0, -60,-15,PH,),A_ELEC,),
"buzz saw"          :(MEL, 7500, 3.5, 480, METL,(0, 0,  15,5,  -5,  0,  66,-18,PH,),A_ELEC,),
"plasma sword"      :(MEL, 84490,2.0, 250, METL,(0, 0,  11,100,-2,  0, -40,-12,FI,),A_OIL,),
'''
#"bayonet"   :(MEL, 150,  0.3, 180, 0,  0,  METL,(4, 9, 4, 0,  2,  0,  40, 0, PH,),None,(),),

#--Name-----------------------Type,Dlv,$$$$$, KG,   Dur, Mat, (DV, AV, MSp, Vis,FIR,BIO,ELE)
    #Back
#"cloak"                     :(BACK,1,  420,   6.0,  150, CLTH,( 4,  1, -3,  0,  10, 10, 0,), ),

'''
    Example weapon display:
 #stats nerfed because it's crude


          ,
         /|
       ./ |
       |` |
      ./  |
      |`  |
      /   |
      \`  |
      /   |
      \`  |
      /   |
      \`  |
      /   |
      \`  |
      |   |
      |...|
  o___|___|___o
  "---|   |---"
       bb#
       #bb
       ###
       bb#
       #bb
       \#/
 
    [/] crude bayonet
    0.3kg     $28
    wield in main hand:                  
        Lo        50 (90)        
        Hi        1 (1)
        Atk       4
        Dmg       2  (physical)
        DV        2
        Atk Spd   40

        
    
    Armor display:
    
    [{] lacquered police cloak
    5.7kg     $1460
    wear on back:
        Lo        180 (200)
        Hi        1 (1)
        AV        1
        DV        4
        Move Spd  -3
        Fire Res  10
        Bio Res   10
    
'''





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

