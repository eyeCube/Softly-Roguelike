'''
    entities.py
    Softly Into the Night, a sci-fi/Lovecraftian roguelike
    Copyright (C) 2020 Jacob Wharton.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>
'''

import random

from const import *
from colors import COLORS as COL
import rogue as rog
import components as cmp
import action
import ai
import dice



# CONSTANTS #

NUMWPNSTATS = 3


FLSH = MAT_FLESH
LETH = MAT_LEATHER
BOIL = MAT_BLEATHER
CLTH = MAT_CLOTH
WOOD = MAT_WOOD
BONE = MAT_BONE
CARB = MAT_CARBON
TARP = MAT_TARP
PLAS = MAT_PLASTIC
METL = MAT_METAL
STON = MAT_STONE
DUST = MAT_DUST
ROPE = MAT_ROPE
CLAY = MAT_CLAY
CERA = MAT_CERAMIC
GLAS = MAT_GLASS
RUBB = MAT_RUBBER
QRTZ = MAT_QUARTZ
OIL  = MAT_OIL
##VEGG = MAT_VEGGIE
##FUNG = MAT_FUNGUS

PH = ELEM_PHYS
FI = ELEM_FIRE
BI = ELEM_BIO
CH = ELEM_CHEM
EL = ELEM_ELEC
RA = ELEM_RADS

ARMR = T_ARMOR
HELM = T_HEADWEAR
BACK = T_CLOAK

M_MAG = IMOD_MAGAZINE
M_PSC = IMOD_PISTOLSCOPE
M_RSC = IMOD_RIFLESCOPE
M_SSC = IMOD_SHOTGUNSCOPE
M_STR = IMOD_STRAP
M_STO = IMOD_STOCK
M_LAS = IMOD_LASER
M_BAY = IMOD_BAYONET
M_BIP = IMOD_BIPOD
M_FLA = IMOD_FLASHLIGHT
M_SUP = IMOD_SUPPRESSOR
M_GRE = IMOD_GRENADELAUNCHER

A_BULL = AMMO_BULLETS
A_BALL = AMMO_CANNONBALLS
A_PCAP = AMMO_PERCUSSIONCAPS
A_PC   = AMMO_PAPERCARTRIDGES
A_SPEAR= AMMO_SPEARS
A_AIR  = AMMO_AIRGUN
A_22LR = AMMO_22LR
A_9MM  = AMMO_9MM
A_357  = AMMO_357
A_10MM = AMMO_10MM
A_45   = AMMO_45ACP
A_44S  = AMMO_44SPL
A_44M  = AMMO_44MAG
A_30   = AMMO_30CARBINE
A_556  = AMMO_556
A_762  = AMMO_762
A_308  = AMMO_308
A_3006 = AMMO_3006
A_300  = AMMO_300
A_50   = AMMO_50BMG
A_2GA = AMMO_2GA
A_3GA = AMMO_3GA
A_4GA = AMMO_4GA
A_6GA = AMMO_6GA
A_8GA = AMMO_8GA
A_10GA = AMMO_10GA
A_12GA = AMMO_12GA
A_WARO = AMMO_WARARROWS
A_ARRO = AMMO_ARROWS
A_BOLT = AMMO_BOLTS
A_ELEC = AMMO_ELEC
A_FLUID= AMMO_FLUIDS
A_OIL  = AMMO_OIL
A_HAZM = AMMO_HAZMATS
A_ACID = AMMO_ACID
A_CHEM = AMMO_CHEMS
A_ROCKT= AMMO_ROCKETS
A_GREN = AMMO_GRENADES
A_FLAM = AMMO_FLAMMABLE
A_DART = AMMO_DARTS
A_ANY  = AMMO_ANYTHING
A_SLNG = AMMO_SLING

# skill data - simplifications
SKL_ENDOVEREND  = SKL_THROWING
SKL_PITCHING    = SKL_THROWING
SKL_SPINNING    = SKL_THROWING
SKL_TIPFIRST    = SKL_THROWING

# body plans
HUMAN   = BODYPLAN_HUMANOID
INSECT  = BODYPLAN_INSECTOID
FLEGS   = BODYPLAN_4LEGGED
EARMS   = BODYPLAN_8ARMS
CUSTOM  = BODYPLAN_CUSTOM

# colors of materials
C_CLAY = 'silver'
C_CERA = 'accent'
C_CLTH = 'white'
C_STON = 'gray'
C_PLAS = 'offwhite'
C_WOOD = 'brown'
C_BONE = 'bone'
C_METL = 'metal'
C_STEL = 'puremetal'
C_LETH = 'tan'
C_FLSH = 'red'
C_TARP = 'blue'
C_BOIL = 'dkbrown'
C_GLAS = 'truegreen'
C_RUBB = 'magenta'
C_DUST = 'ltgray'
C_SAND = 'ltbrown'
C_DIRT = 'brown'
C_CARB = 'graypurple'
C_ROPE = 'tan'
C_ELEC = 'lime' # electronics
C_QRTZ = 'crystal'

#types of materials
RAWM = T_RAWMAT
SCRP = T_SCRAP
SHRD = T_SHARD
STIK = T_STICK
PRCL = T_PARCEL
PIEC = T_PIECE
CHNK = T_CHUNK
SLAB = T_SLAB
CUBO = T_CUBOID
CUBE = T_CUBE



# FUNCTIONS #


# GEAR #
    #armor/headwear/facewear/eyewear (share most of these)
#$$$$$, KG,   Dur, AP,   Mat, (DV, AV, Pro,Enc,FIR,ICE,BIO,ELE,PHS,BLD),B,C,H,script
def get_gear_value(gData):          return gData[0]
def get_gear_mass(gData):           return gData[1]
def get_gear_hpmax(gData):          return gData[2]
def get_gear_apCost(gData):         return gData[3] # AP cost to put on/ take off
def get_gear_mat(gData):            return gData[4]
def get_gear_strReq(gData):         return gData[5]
##def get_gear_strReq(gData):         return gData[5] # could base StrReq on encumberance...?
def get_gear_dv(gData):             return gData[6][0]
def get_gear_av(gData):             return gData[6][1]
def get_gear_pro(gData):            return gData[6][2]
def get_gear_enc(gData):            return gData[6][3]
def get_gear_resfire(gData):        return gData[6][4]
def get_gear_rescold(gData):        return gData[6][5]
def get_gear_resbio(gData):         return gData[6][6]
def get_gear_reselec(gData):        return gData[6][7]
def get_gear_resphys(gData):        return gData[6][8]
def get_gear_resbleed(gData):       return gData[6][9]
def get_gear_reslight(gData):       return gData[6][10]
def get_gear_ressound(gData):       return gData[6][11]
def get_gear_sight(gData):          return gData[6][12]
##def get_gear_bal(gData):            return gData[6][13] # TODO: make balance a relevant stat, add it to all gear
def get_gear_script(gData):         return gData[7]
def get_gear_idtype(gData):         return gData[8]
    # armor only
def get_armor_coversBack(gData):    return gData[7][0] 
def get_armor_coversCore(gData):    return gData[7][1]
def get_armor_coversHips(gData):    return gData[7][2]
def get_armor_coversArms(gData):    return gData[7][3]
def get_armor_script(gData):        return gData[8]
def get_armor_idtype(gData):        return gData[9]
    # legwear
def get_legwear_coversBoth(gData):  return gData[7]
def get_legwear_script(gData):      return gData[8]
def get_legwear_idtype(gData):      return gData[9]
    # eyewear
def get_eyewear_script(gData):      return gData[7]
def get_eyewear_idtype(gData):      return gData[8]
    # facewear
def get_facewear_eyes(gData):       return gData[7] # covers eyes?
def get_facewear_script(gData):     return gData[8]
def get_facewear_idtype(gData):     return gData[8]
    # headwear
def get_headwear_face(gData):       return gData[7] # covers face?
def get_headwear_eyes(gData):       return gData[8] # covers eyes?
def get_headwear_ears(gData):       return gData[9] # covers ears?
def get_headwear_neck(gData):       return gData[10] # covers neck?
def get_headwear_script(gData):     return gData[11]
def get_headwear_idtype(gData):     return gData[12]
    #weapons
def get_weapon_value(gData):        return gData[0]
def get_weapon_mass(gData):         return gData[1]
def get_weapon_hpmax(gData):        return gData[2]
def get_weapon_mat(gData):          return gData[3]
def get_weapon_strReq(gData):       return gData[4]
def get_weapon_dexReq(gData):       return gData[5]
def get_weapon_atk(gData):          return gData[6][0]
def get_weapon_dmg(gData):          return gData[6][1]
def get_weapon_pen(gData):          return gData[6][2]
def get_weapon_dv(gData):           return gData[6][3]
def get_weapon_av(gData):           return gData[6][4]
def get_weapon_pro(gData):          return gData[6][5]
def get_weapon_asp(gData):          return gData[6][6]
def get_weapon_enc(gData):          return gData[6][7]
def get_weapon_gra(gData):          return gData[6][8]
def get_weapon_ctr(gData):          return gData[6][9]
def get_weapon_staminacost(gData):  return gData[6][10]
def get_weapon_reach(gData):        return gData[6][11]
def get_weapon_force(gData):        return gData[6][12] # knockback / knockdown / off-balance / stagger
def get_weapon_bal(gData):          return gData[6][13] # how much balance the weapon gives you
def get_weapon_grip(gData):         return gData[6][14]
def get_weapon_skill(gData):        return gData[7]
def get_weapon_script(gData):       return gData[8]
def get_weapon_idtype(gData):       return gData[9]
    # ranged weapons
def get_ranged_ammotype(name):  return RANGEDWEAPONS[name][0]
def get_ranged_value(name):     return RANGEDWEAPONS[name][1]
def get_ranged_kg(name):        return RANGEDWEAPONS[name][2]
def get_ranged_hp(name):        return RANGEDWEAPONS[name][3]
def get_ranged_mat(name):       return RANGEDWEAPONS[name][4]
def get_ranged_strReq(name):    return RANGEDWEAPONS[name][5]
def get_ranged_dexReq(name):    return RANGEDWEAPONS[name][6]
def get_ranged_capacity(name):  return RANGEDWEAPONS[name][7][0]
def get_ranged_nShots(name):    return RANGEDWEAPONS[name][7][1]
def get_ranged_reloadTime(name):return RANGEDWEAPONS[name][7][2]
def get_ranged_jamChance(name): return RANGEDWEAPONS[name][7][3]
def get_ranged_minRng(name):    return RANGEDWEAPONS[name][7][4]
def get_ranged_maxRng(name):    return RANGEDWEAPONS[name][7][5]
def get_ranged_ratk(name):      return RANGEDWEAPONS[name][7][6]
def get_ranged_rdmg(name):      return RANGEDWEAPONS[name][7][7]
def get_ranged_rpen(name):      return RANGEDWEAPONS[name][7][8]
def get_ranged_dfn(name):       return RANGEDWEAPONS[name][7][9]
def get_ranged_rasp(name):      return RANGEDWEAPONS[name][7][10]
def get_ranged_enc(name):       return RANGEDWEAPONS[name][7][11]
def get_ranged_force(name):     return RANGEDWEAPONS[name][7][12]
def get_ranged_skill(name):     return RANGEDWEAPONS[name][8]
def get_ranged_script(name):    return RANGEDWEAPONS[name][9]
def get_ranged_idtype(name):    return RANGEDWEAPONS[name][10]

# JOBS #
def getJobs():
    #returns dict of pairs (k,v) where k=ID v=charType
    ll={}
    for k,v in JOBS.items():
        ll.update({k: getJobChar(k)})
    return ll
def getJobChar(jobID) -> str:
    return JOBS[jobID][0]
def getJobName(jobID) -> str:
    return JOBS[jobID][1]
def getJobMass(jobID) -> int:
    return JOBS[jobID][2]
def getJobMoney(jobID) -> int:
    return JOBS[jobID][3]
def getJobClearance(jobID) -> int: #get security clearance level
    return JOBS[jobID][4]
def getJobKey(jobID) -> str:
    return JOBS[jobID][5]
def getJobStats(jobID) -> dict:
    return JOBS[jobID][6]
def getJobSkills(jobID) -> tuple:
    return JOBS[jobID][7]

# MONSTERS
def getMonName(_char):      return BESTIARY[_char][0]
def getMonKG(_char):        return BESTIARY[_char][1]
def getMonCM(_char):        return BESTIARY[_char][2]
def getMonMat(_char):       return BESTIARY[_char][3]
def getMonBodyPlan(_char):  return BESTIARY[_char][4]
def getMonFlags(_char):     return BESTIARY[_char][5]
def getMonScript(_char):    return BESTIARY[_char][6]
def getMonID(_char):        return BESTIARY[_char][7]
def getMonStats(_char):     return BESTIARY[_char][8]
#name, KG, bodyplan, (FLAGS), script, {Stat Dict},







    #-----------------------------------#
    #           item scripts            #
    #-----------------------------------#




    # GENERIC SCRIPTS

def _coversBothLegs(item):
    rog.world().component_for_entity(item, cmp.EquipableInLegSlot).coversBoth=True

def _length(item, cm):
    rog.world().component_for_entity(item, cmp.Form).length = cm

def _clothes(item):
    rog.world().add_component(item, cmp.Clothes)

def _mod(item, _typ, mods):
    for k,v in mods.items():
        if k in MULTSTATS:
            mods[k] = mods[k] * MULT_STATS
    rog.world().add_component(item, cmp.Mod(_typ, mods))
    
def _getDefaultAP(mass): # weapon AP cost to wield
    mass=mass//MULT_MASS
    if mass <= 0.5:
        ap = NRG_WIELDSMALL
    elif mass <= 1:
        ap = NRG_WIELD
    elif mass <= 2:
        ap = NRG_WIELDLARGE
    elif mass <= 3:
        ap = NRG_WIELDXLARGE
    else:
        ap = NRG_WIELDCUMBERSOME
    return ap
def _getDefaultSP(mass): # weapon SP cost to strike
    mass=mass//MULT_MASS
    return rog.ceil(mass*12)

def _weapon(item, acc=0,dmg=0,pen=0,dv=0,av=0,pro=0,asp=0,enc=1,
            reach=0,spcost=None,twoh=False,skill=None):
    world=rog.world()
    dmod={}
    if acc !=0: dmod['acc'] = int(acc*MULT_STATS)
    if dmg !=0: dmod['dmg'] = int(dmg*MULT_STATS)
    if pen !=0: dmod['pen'] = int(pen*MULT_STATS)
    if dv !=0: dmod['dv'] = int(dv*MULT_STATS)
    if av !=0: dmod['av'] = int(av*MULT_STATS)
    if pro !=0: dmod['pro'] = int(pro*MULT_STATS)
    if asp !=0: dmod['asp'] = int(asp)
    if reach !=0: dmod['reach'] = int(reach*MULT_STATS)
    world.add_component(item, cmp.Encumberance(enc))
    
    # get extra values from existing parameters
    wieldAP=NRG_WIELD # temporary (get from weapon mass?)
    if not spcost:
        spcost = int(8 * rog.getms(item, 'mass')//MULT_MASS) # TEST THIS
    
    # equipable in hold slot -- update component or add new component
    if world.has_component(item, cmp.EquipableInHoldSlot):
        # update existing component
        existing=world.component_for_entity(item, cmp.EquipableInHoldSlot)
        for k, v in existing.mods.items():
            dmod = dmod.get(k, 0) + v
        existing.mods = dmod
    else:
        # create new component
        world.add_component(item, cmp.EquipableInHoldSlot(
            wieldAP, spcost, dmod))
    #
    if twoh: rog.make(item, TWOHANDS)
    if skill: world.add_component(item, cmp.WeaponSkill(skill))

def _canThrow(item, func=None, rng=0,acc=0,dmg=0,pen=0,asp=0,
              skill=None, ap=None, sp=None, strReq=0, dexReq=0):
    if rng <= 0: return
    world=rog.world()
    world.add_component(item, cmp.Throwable(func))
    # holdable component - get or create if none already exists
    if world.has_component(item, cmp.EquipableInHoldSlot):
        equipable=world.component_for_entity(item, cmp.EquipableInHoldSlot)
    else:
        stats=world.component_for_entity(item, cmp.Stats) # this shouldn't be a problem, right..??
        if ap is None:
            ap = _getDefaultAP(stats.mass)
        if sp is None:
            sp = _getDefaultSP(stats.mass)
        equipable=cmp.EquipableInHoldSlot(ap, sp, {}, strReq=strReq, dexReq=dexReq)
        world.add_component(item, equipable)
    # throwing stats mods
    if rng!=0: equipable.mods['trng']=rng
    if acc!=0: equipable.mods['tatk']=acc*MULT_STATS
    if dmg!=0: equipable.mods['tdmg']=dmg*MULT_STATS
    if pen!=0: equipable.mods['tpen']=pen*MULT_STATS
    if asp!=0: equipable.mods['tasp']=asp
##    if skill:
##

def _addRes(item, resfire=0,resbio=0,reselec=0,resphys=0,resrust=0,resrot=0,reswet=0,resdirt=0):
    stats=rog.world().component_for_entity(item, cmp.Stats)
    if resfire: stats.resfire = resfire
    if resbio: stats.resbio = resbio
    if reselec: stats.reselec = reselec
    if resphys: stats.resphys = resphys
    if resrust: stats.resrust = resrust
    if resrot: stats.resrot = resrot
    if reswet: stats.reswet = reswet
    if resdirt: stats.resdirt = resdirt

    
def _elementalRanged(item, elem, amt):
    world=rog.world()
    if world.has_component(item, cmp.ElementalDamageRanged):
        # combine the elemental damage dictionaries
        compo = world.component_for_entity(item, cmp.ElementalDamageRanged)
        compo.elements[elem] = amt + compo.elements.get(elem, 0)
    else:
        world.add_component(item, cmp.ElementalDamageRanged({elem : amt}))
def _elementalMelee(item, elem, amt):
    world=rog.world()
    if world.has_component(item, cmp.ElementalDamageMelee):
        # combine the elemental damage dictionaries
        compo = world.component_for_entity(item, cmp.ElementalDamageMelee)
        compo.elements[elem] = amt + compo.elements.get(elem, 0)
    else:
        world.add_component(item, cmp.ElementalDamageMelee({elem : amt}))
    
    
# effects #
    
def _wet(actor, n):
    pass
##    if n>=10:
##        rog.set_status(actor, WET)
def _oily(actor, n):
    pass
##    if n>=10:
##        rog.make(actor, OILY)
def _bloody(actor, n):
    pass
##    if n>=10:
##        rog.make(actor, BLOODY)
def _cough(actor, n):
    rog.cough(actor, n)
def _hydrate(actor, n):
    actor.hydration += n * WATER_HYDRATE
def _quaffBlood(actor, n):
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


def _melee_bleed(item, amt):
    if not amt: return
    _elementalMelee(item, ELEM_BLEED, amt)
def _melee_pain(item, amt):
    if not amt: return
    _elementalMelee(item, ELEM_PAIN, amt)
def _bonusToFlesh(item, bonus):
    if bonus > 0:
        rog.world().add_component(item, cmp.BonusToFlesh(bonus))
def _bonusToArmor(item, bonus):
    if bonus > 0:
        rog.world().add_component(item, cmp.BonusToArmor(bonus))
def _amputate(item, value):
    if value > 0:
        rog.world().add_component(item, cmp.HacksOffLimbs(value))

def _spikes(item):
    rog.world().add_component(item, cmp.DamageTypeMelee(DMGTYPE_SPIKES))
def _spuds(item):
    rog.world().add_component(item, cmp.DamageTypeMelee(DMGTYPE_SPUDS))

    # /



    # gear #

def _cloak(tt):
    if not rog.has(tt, cmp.EquipableInHoldSlot):
        modDict = {"atk":3,"dfn":1,"pro":0.5,}
        rog.world().add_component(tt, cmp.EquipableInHoldSlot(NRG_WIELD,modDict))
        
def _fireBlanket(tt):
    pass

def _nvisionGoggles(tt):
##    if rog.has(tt, cmp.Equipable):
##        equipable = rog.get(tt, cmp.Equipable)
##        equipable.statMods.update({})
    pass

def _earPlugs(tt):
    pass

def _runningShoe(item):
    compo = rog.world().component_for_entity(item, cmp.EquipableInFootSlot)
    compo.mods['msp'] = 5



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

def _percussionCap(tt):
    pass
def _sCannonBall(tt):
    _canThrow(tt, acc=-5, rng=6, dmg=-1, skill=SKL_PITCHING)
def _mCannonBall(tt):
    _canThrow(tt, acc=-5, rng=6, dmg=-1, skill=SKL_PITCHING)
def _sBullet(tt):
    _canThrow(tt, acc=-6, rng=5, dmg=1)
def _mBullet(tt):
    _canThrow(tt, acc=-6, rng=3, dmg=1)
def _minnieBall(tt):
    _canThrow(tt, acc=-6, rng=3, dmg=1)
def _mCartridge(tt):
    _canThrow(tt, acc=-5, rng=5)
def _mCartridgeLarge(tt):
    _canThrow(tt, acc=5, rng=9, dmg=2)
def _shell(tt):
    _canThrow(tt, acc=0, rng=6, dmg=1)
def _incendiary(tt):
    def deathFunc(ent):
        entn=rog.world().component_for_entity(ent, cmp.Name)
        pos=rog.world().component_for_entity(ent, cmp.Position)
        rog.set_fire(pos.x, pos.y)
        radius=1
        rog.explosion("{}{}".format(TITLES[entn.title],entn.name), pos.x,pos.y, radius)
    rog.world().add_component(tt, cmp.DeathFunction(deathFunc))
def _paperCartridge(tt):
    _canThrow(tt, acc=0, rng=7, dmg=1, skill=SKL_PITCHING)



# food #

##def _food_poison(ent):  #deceptively sweet but makes you sick
##    rog.world().add_component(ent, cmp.Edible(
##        func=_sick, sat=FOOD_RATION, taste=TASTE_SWEET, FOOD_RATION_NRG
##        ))
def _food_morsel_savory(ent):
    rog.world().add_component(ent, cmp.Edible(
        func=None, sat=FOOD_MORSEL, taste=TASTE_SAVORY, ap=FOOD_MORSEL_NRG
        ))
def _food_morsel_bitter(ent):
    rog.world().add_component(ent, cmp.Edible(
        func=None, sat=FOOD_MORSEL, taste=TASTE_BITTER, ap=FOOD_MORSEL_NRG
        ))
def _food_morsel_sweet(ent):
    rog.world().add_component(ent, cmp.Edible(
        func=None, sat=FOOD_MORSEL, taste=TASTE_SWEET, ap=FOOD_MORSEL_NRG
        ))
def _food_morsel_bloody_nasty(ent):
    rog.world().add_component(ent, cmp.Edible(
        func=_bloody, sat=FOOD_MORSEL, taste=TASTE_NASTY, ap=FOOD_MORSEL_NRG
        ))
def _food_serving_savory(ent):
    rog.world().add_component(ent, cmp.Edible(
        func=None, sat=FOOD_SERVING, taste=TASTE_SAVORY, ap=FOOD_SERVING_NRG
        ))
def _food_ration_savory(ent):
    rog.world().add_component(ent, cmp.Edible(
        func=None, sat=FOOD_RATION, taste=TASTE_SAVORY, ap=FOOD_RATION_NRG
        ))
def _food_meal_gamble(ent):
    ran=random.random(10)
    if ran < 2:
        rog.world().add_component(ent, cmp.Edible(
            func=None, sat=FOOD_MEAL, taste=TASTE_SAVORY, ap=FOOD_MEAL_NRG
            ))
    elif ran < 4:
        rog.world().add_component(ent, cmp.Edible(
            func=None, sat=FOOD_MEAL, taste=TASTE_BITTER, ap=FOOD_MEAL_NRG
            ))
    elif ran < 6:
        rog.world().add_component(ent, cmp.Edible(
            func=None, sat=FOOD_MEAL, taste=TASTE_SWEET, ap=FOOD_MEAL_NRG
            ))
    elif ran < 8:
        rog.world().add_component(ent, cmp.Edible(
            func=None, sat=FOOD_MEAL, taste=TASTE_NASTY, ap=FOOD_MEAL_NRG
            ))
    else:
        rog.world().add_component(ent, cmp.Edible(
            func=None, sat=FOOD_MEAL, taste=TASTE_ACIDIC, ap=FOOD_MEAL_NRG
            ))
def _food_meal_savory(ent):
    rog.world().add_component(ent, cmp.Edible(
        func=None, sat=FOOD_MEAL, taste=TASTE_SAVORY, ap=FOOD_MEAL_NRG
        ))
def _food_bigMeal_savory(ent):
    rog.world().add_component(ent, cmp.Edible(
        func=None, sat=FOOD_BIGMEAL, taste=TASTE_SAVORY, ap=FOOD_BIGMEAL_NRG
        ))
def _food_cokenut(ent):
    def func(ent, eater):
        rog.poison(eater)
    rog.world().add_component(ent, cmp.Edible(
        func=func, sat=FOOD_MORSEL, taste=TASTE_BITTER, ap=FOOD_MORSEL_NRG
        ))
    rog.world().add_component(ent, cmp.Ingredient(ING_COKENUT))
def _food_sillyfruit(ent):
    def func(ent, eater):
        rog.confuse(eater)
    rog.world().add_component(ent, cmp.Edible(
        func=func, sat=FOOD_SERVING, taste=TASTE_SWEET, ap=FOOD_SERVING_NRG
        ))


# stuff #

def _solarPanel(ent):
    rog.make(ent, TWOHANDS)
    _canThrow(ent, rng=3, acc=-5, dmg=1)
def _skeleton(ent):
    rog.world().add_component(ent, cmp.Harvestable(
        500,
        {'bone':2, 'bone, small':16, 'skull':1,
         'piece of bone':1, 'parcel of bone':8, 'scrap bone':16,},
        {}
        ))
def _campfire(ent):
    pass
def _foliage(ent):
    pass

def _pot(ent): #metal pot
    rog.init_fluidContainer(ent, 200)
##    rog.make(tt, CANUSE)
##    tt.useFunctionPlayer = action.pot_pc
##    tt.useFunctionMonster = action.pot

def _clayPot(ent):
    pass
def _ceramicPot(ent):
    rog.world().add_component(ent, cmp.FluidContainer(capacity=50))
    _canThrow(ent, rng=4, acc=5, dmg=4, pen=2)
def _clayPotLarge(ent):
    pass
def _ceramicPotLarge(ent):
    rog.world().add_component(ent, cmp.FluidContainer(capacity=1000))
    
def _gunpowder(ent):
    rog.world().add_component(ent, cmp.DiesInWater(func=None))
def _blackPowder(ent):
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
    #components
    _canThrow(ent, rng=4)
    _weapon(ent, atk=1, dmg=1, asp=-6)
    world.add_component(ent, cmp.Usable(funcUsePC,funcUseNPC))
    world.add_component(ent, cmp.ReactsWithWater(diesInWaterFunc))
    world.add_component(ent, cmp.DeathFunction(funcDeath))
    
def _towel(ent):
    world=rog.world()
    def funcPC(thing, actor):
        pass
    def funcNPC(thing, actor):
        pass
    world.add_component(ent, cmp.GetsWet(capacity=100))
    world.add_component(ent, cmp.Usable(funcPC,funcNPC))
##    statMods={cmp.BasisStats : {"rescold":20,},} # THat's not a resistance stat yet. Dunno if we should add it...
##    world.add_component(ent, cmp.EquipableInAboutSlot(300,statMods))
    statMods={"dfn":1,"arm":1,"pro":1,} # if wet, gives double as much stats. How to handle this?
    world.add_component(ent, cmp.EquipableInHoldSlot(NRG_WIELD,statMods))
def _towel_wield(ent): #prepare a towel for wielding. Transforms it into a wielding item.
    statMods={"atk":3, "dmg":1, "dfn":3,}
    world.add_component(ent, cmp.EquipableInHoldSlot(NRG_WIELD,statMods))
def _towel_wearOnHead(ent): #prepare a towel for headwear. Transforms it into head gear
    statMods={"resbio":15,}
    world.add_component(ent, cmp.EquipableInHeadSlot(300,statMods))
    
def _torch(tt):
    pass # TODO: do components!!!!
##    rog.make(tt, CANEQUIP)
##    tt.equipType=EQ_OFFHAND
def _torchLarge(tt):
    pass # TODO: do components!!!!

def _extinguisher(tt):
    pass
##    rog.make(tt, CANUSE) # USE COMPONENTS!!
##    tt.useFunctionPlayer = action.extinguisher_pc
##    tt.useFunctionMonster = action.extinguisher
##    rog.makeEquip(tt, EQ_MAINHAND)

def _lighter(tt):
    pass

def _grave(tt):
    rog.world().add_component(tt, cmp.Readable(random.choice(HISTORY_EPITAPHS)))

def _meatFlower(item):
    rog.world().add_component(item, cmp.Harvestable(
        300,
        {'parcel of flesh' : 1},
        {cmp.Tool_Chop : 1}
        ))


    # monsters
def _whipmaster(ent):
    rog.setskill(ent, SKL_BULLWHIPS, 50)


    # raw mats
def _parcel(item): # TODO: hook up all standard rawmat scripts to these functions to give them the right glyph...
    rog.world().component_for_entity(item, cmp.Draw).char = T_PARCEL
    _length(item, 5)
def _shard(item):
    rog.world().component_for_entity(item, cmp.Draw).char = T_SHARD
    _length(item, 10)
def _piece(item):
    rog.world().component_for_entity(item, cmp.Draw).char = T_PIECE
    _length(item, 10)
def _chunk(item):
    rog.world().component_for_entity(item, cmp.Draw).char = T_CHUNK
    _length(item, 22)
def _slab(item):
    rog.world().component_for_entity(item, cmp.Draw).char = T_SLAB
    _length(item, 33)
def _cuboid(item):
    rog.world().component_for_entity(item, cmp.Draw).char = T_CUBOID
    _length(item, 33)
def _cube(item):
    rog.world().component_for_entity(item, cmp.Draw).char = T_CUBE
def _rawMat(item): # TODO: replace w/ more specialized functions except for those that don't fit any others
    rog.world().component_for_entity(item, cmp.Draw).char = T_RAWMAT
def _particles(item):
    rog.world().component_for_entity(item, cmp.Draw).char = T_RAWMAT
    _canThrow( item, rng=3, acc=6, dmg=1)
def _trinket(item):
    _canThrow(item, rng=5, acc=0, dmg=0)
    
    # shards
def _shard(item, acc=-2, rng=5):
    _canThrow(item, acc=acc, rng=rng)
    rog.world().component_for_entity(item, cmp.Draw).char = T_RAWMAT
def _pShard(item):
    _melee_bleed(item, 0.25*BLEED_PLASTIC)
    rog.world().add_component(item, cmp.Tool_Cut(1))
    _weapon(item, acc=1,dmg=1,pen=1,asp=3)
    _shard(acc=-5, rng=3)
def _wShard(item):
    _melee_bleed(item, 0.25*BLEED_WOOD)
    _weapon(item, acc=1,dmg=2,pen=1,asp=6)
    _shard(-3, 5)
def _sShard(item):
    _melee_bleed(item, 0.25*BLEED_STONE)
    rog.world().add_component(item, cmp.Tool_Cut(2))
    rog.world().add_component(item, cmp.Tool_Chisel(1))
    _weapon(item, acc=1,dmg=3,pen=4,asp=0)
    _shard(1, 10)
def _bShard(item):
    _melee_bleed(item, 0.25*BLEED_BONE)
    rog.world().add_component(item, cmp.Tool_Cut(1))
    rog.world().add_component(item, cmp.Tool_Chisel(1))
    _weapon(item, acc=1,dmg=2,pen=3,asp=6)
    _shard(-1, 6)
def _mShard(item):
    _melee_bleed(item, 0.25*BLEED_METAL)
    rog.world().add_component(item, cmp.Tool_Cut(3))
    rog.world().add_component(item, cmp.Tool_Chisel(2))
    _weapon(item, acc=2,dmg=4,pen=5,asp=9)
    _shard(0, 6)
def _gShard(item):
    _melee_bleed(item, 0.25*BLEED_GLASS)
    rog.world().add_component(item, cmp.Tool_Cut(4))
    _weapon(item, acc=4,dmg=5,pen=2,asp=15)
    _shard(-2, 2)
def _cShard(item): #ceramic
    _melee_bleed(item, 0.25*BLEED_CERAMIC)
    rog.world().add_component(item, cmp.Tool_Cut(3))
    _weapon(item, acc=3,dmg=4,pen=1,asp=12)
    _shard(acc=-2, rng=5)

    # parcels
def _rParcel(item):
    _parcel(item)
    _canThrow(item, acc=0, rng=4, skill=SKL_PITCHING)
def _qParcel(item): # quartz
    _parcel(item)
    _weapon(item, acc=1,dmg=1,pen=1,asp=-12)
    _canThrow(item, acc=2, rng=8, dmg=1, skill=SKL_PITCHING)
def _pParcel(item):
    _parcel(item)
    _canThrow(item, acc=-2, rng=4, skill=SKL_PITCHING)
def _wParcel(item):
    _parcel(item)
    _canThrow(item, acc=2, rng=4, skill=SKL_PITCHING)
def _sParcel(item):
    _parcel(item)
    _weapon(item, acc=1,dmg=1,pen=1,asp=-15)
    _canThrow(item, acc=2, rng=8, dmg=1, skill=SKL_PITCHING)
def _bParcel(item):
    _parcel(item)
    _weapon(item, acc=-1,dmg=1,pen=1,asp=-15)
    _canThrow(item, acc=2, rng=6, skill=SKL_PITCHING)
def _gParcel(item):
    _parcel(item)
    _weapon(item, acc=1,dmg=1,pen=1,asp=-15)
    _canThrow(item, acc=2, rng=6, skill=SKL_PITCHING)
def _mParcel(item):
    _parcel(item)
    _weapon(item, acc=2,dmg=1,pen=2,asp=-15)
    _canThrow(item, acc=2, rng=8, skill=SKL_PITCHING)
def _tParcel(item): # tarp
    _parcel(item)
def _fParcel(item):
    _parcel(item)
    _canThrow(item, acc=0, rng=6, skill=SKL_PITCHING)
def _lParcel(item):
    _parcel(item)
    _canThrow(item, acc=0, rng=8, skill=SKL_PITCHING)
def _blParcel(item):
    _parcel(item)
    _weapon(item, acc=0,dmg=1,pen=0,asp=-15)
    _canThrow(item, acc=1, rng=10, skill=SKL_PITCHING)
def _clothParcel(item):
    _parcel(item)
def _clayParcel(item):
    _parcel(item)
    _canThrow(item, acc=2, rng=5)
def _ceramicParcel(item):
    _parcel(item)
    _weapon(item, acc=2,dmg=1,pen=1,asp=-21)
    _canThrow(item, acc=2, rng=10, dmg=2, skill=SKL_PITCHING)

    # pieces
def _rPiece(item):
    _piece(item)
    _canThrow(item, acc=0, rng=6)
def _qPiece(item): # quartz
    _piece(item)
    _weapon(item, acc=0,dmg=2,pen=3,asp=-24,enc=3)
    _canThrow(item, acc=0, rng=14, dmg=3, skill=SKL_PITCHING)
def _pPiece(item):
    _piece(item)
    _weapon(item, acc=-2,dmg=1,pen=0,asp=-30,enc=3)
    _canThrow(item, acc=0, rng=6)
def _wPiece(item):
    _piece(item)
    _weapon(item, acc=0,dmg=1,pen=1,asp=-21,enc=3)
    _canThrow(item, acc=0, rng=8)
def _sPiece(item):
    _piece(item)
    rog.world().add_component(item, cmp.Tool_Hammer(1))
    _weapon(item, acc=0,dmg=2,pen=3,asp=-27,enc=3)
    _canThrow(item, acc=0, rng=14, dmg=3, skill=SKL_PITCHING)
def _bPiece(item):
    _piece(item)
    _weapon(item, acc=0,dmg=1,pen=2,asp=-21,enc=3)
    _canThrow(item, acc=0, rng=10, skill=SKL_PITCHING)
def _gPiece(item):
    _piece(item)
    _weapon(item, acc=0,dmg=1,pen=2,asp=-21,enc=3)
    _canThrow(item, acc=0, rng=8)
def _mPiece(item):
    _piece(item)
    _weapon(item, acc=0,dmg=2,pen=3,asp=-21,enc=3)
    _canThrow(item, acc=0, rng=12, dmg=2, pen=1, skill=SKL_PITCHING)
def _tPiece(item): # tarp
    _piece(item)
def _fPiece(item):
    _piece(item)
    _weapon(item, acc=0,dmg=1,pen=0,asp=-39,enc=3)
    _canThrow(item, acc=0, rng=6)
def _lPiece(item):
    _piece(item)
    _weapon(item, acc=0,dmg=1,pen=1,asp=-33,enc=3)
    _canThrow(item, acc=0, rng=5)
def _blPiece(item):
    _piece(item)
    _weapon(item, acc=0,dmg=2,pen=1,asp=-27,enc=3)
    _canThrow(item, acc=0, rng=12, skill=SKL_PITCHING)
def _clothPiece(item):
    _piece(item)
    _canThrow(item, acc=-6, rng=3)
def _clayPiece(item):
    _piece(item)
    _canThrow(item, acc=0, rng=6)
def _ceramicPiece(item):
    _piece(item)
    _weapon(item, acc=0,dmg=3,pen=2,asp=-21,enc=3)
    _canThrow(item, acc=0, rng=10, dmg=2, skill=SKL_PITCHING)

    # chunks
def _rChunk(item): #rubber
    _chunk(item)
    rog.make(item, TWOHANDS)
    _weapon(item, acc=-6,dmg=1,pen=0,asp=-42,enc=9)
    _canThrow(item, acc=-6, rng=8)
def _lChunk(item): #leather
    _chunk(item)
    rog.make(item, TWOHANDS)
    _weapon(item, acc=-5,dmg=2,pen=1,asp=-33,enc=9)
    _canThrow(item, acc=-5, rng=8)
def _blChunk(item): #boiled leather
    _chunk(item)
    rog.make(item, TWOHANDS)
    _weapon(item, acc=-5,dmg=3,pen=2,asp=-30,enc=9)
    _canThrow(item, acc=-5, rng=10)
def _qChunk(item): #quartz
    _chunk(item)
    rog.make(item, TWOHANDS)
    _weapon(item, acc=-5,dmg=4,pen=3,asp=-36,enc=9)
    _canThrow(item, acc=-5, rng=12)
def _pChunk(item):
    _chunk(item)
    rog.make(item, TWOHANDS)
    _weapon(item, acc=-5,dmg=1,pen=0,asp=-36,enc=9)
    _canThrow(item, acc=-5, rng=6)
def _wChunk(item):
    _chunk(item)
    rog.make(item, TWOHANDS)
    _weapon(item, acc=-5,dmg=1,pen=1,asp=-30,enc=9)
    _canThrow(item, acc=-5, rng=8)
def _sChunk(item):
    _chunk(item)
    rog.make(item, TWOHANDS)
    _weapon(item, acc=-5,dmg=4,pen=3,asp=-36,enc=9)
    _canThrow(item, acc=-5, rng=12)
def _bChunk(item):
    _chunk(item)
    rog.make(item, TWOHANDS)
    _weapon(item, acc=-5,dmg=2,pen=2,asp=-30,enc=9)
    _canThrow(item, acc=-5, rng=10)
def _gChunk(item):
    _chunk(item)
    rog.make(item, TWOHANDS)
    _weapon(item, acc=-5,dmg=3,pen=2,asp=-30,enc=9)
    _canThrow(item, acc=-5, rng=8)
def _mChunk(item):
    _chunk(item)
    rog.make(item, TWOHANDS)
    _weapon(item, acc=-5,dmg=4,pen=3,asp=-30,enc=9)
    _canThrow(item, acc=-5, rng=14)
def _tarp(item):
    _chunk(item)
def _fChunk(item):
    _chunk(item)
    rog.make(item, TWOHANDS)
    _weapon(item, acc=-5,dmg=1,pen=0,asp=-48,enc=9)
    _canThrow(item, acc=-5, rng=6)
def _lChunk(item):
    _chunk(item)
    rog.make(item, TWOHANDS)
    _weapon(item, acc=-5,dmg=1,pen=1,asp=-39,enc=9)
    _canThrow(item, acc=-5, rng=5)
def _blChunk(item):
    _chunk(item)
    rog.make(item, TWOHANDS)
    _weapon(item, acc=-5,dmg=2,pen=1,asp=-36,enc=9)
    _canThrow(item, acc=-5, rng=8)
def _clothChunk(item):
    _chunk(item)
    _canThrow(item, acc=-15, rng=2)
def _clayChunk(item):
    _chunk(item)
    _canThrow(item, acc=-10, rng=3, dmg=1, pen=-1)
def _ceramicChunk(item):
    _chunk(item)
    rog.make(item, TWOHANDS)
    _weapon(item, acc=-5,dmg=4,pen=3,asp=-30,enc=9)
    _canThrow(item, acc=-5, rng=6)
    
    # slabs
def _pSlab(item):
    _slab(item)
def _wSlab(item):
    _slab(item)
    rog.world().add_component( item, cmp.Harvestable(
        4800,
        {'wooden plank':20},
        {cmp.Tool_Saw:4}
        ) )
def _fSlab(item):
    _slab(item)
def _bSlab(item):
    _slab(item)
def _sSlab(item):
    _slab(item)
def _mSlab(item):
    _slab(item)
def _gSlab(item):
    _slab(item)
def _ceramicSlab(item):
    _slab(item)
def _claySlab(item):
    _slab(item)
def _tarpLarge(item):
    _slab(item)
    
    # sticks, poles
def _pStick(item):
    rog.world().component_for_entity(item, cmp.Draw).char = T_MELEEWEAPON
    _weapon(item, acc=2,dmg=2,pen=1,dv=1,asp=-15,enc=4)
    _canThrow(item, acc=0, rng=10, skill=SKL_ENDOVEREND)
    _length(item, 100)
def _wStick(item):
    rog.world().component_for_entity(item, cmp.Draw).char = T_MELEEWEAPON
    _weapon(item, acc=2,dmg=2,pen=2,dv=1,asp=-21,enc=4)
    _canThrow(item, acc=0, rng=12, skill=SKL_ENDOVEREND)
    _length(item, 100)
def _mStick(item):
    rog.world().component_for_entity(item, cmp.Draw).char = T_MELEEWEAPON
    _weapon(item, acc=2,dmg=4,pen=4,dv=1,asp=-12,enc=4)
    _canThrow(item, acc=0, rng=14, skill=SKL_ENDOVEREND)
    _length(item, 100)
def _pPole(item):
    rog.world().component_for_entity(item, cmp.Draw).char = T_TWOHANDWEAP
    rog.make(item, TWOHANDS)
    _weapon(item, acc=5,dmg=4,pen=3,dv=1,av=1,pro=1,asp=6,enc=4)
    _canThrow(item, acc=0, rng=10, skill=SKL_TIPFIRST)
    _length(item, 200)
def _wPole(item):
    rog.world().component_for_entity(item, cmp.Draw).char = T_TWOHANDWEAP
    rog.make(item, TWOHANDS)
    _weapon(item, acc=5,dmg=5,pen=4,dv=1,av=1,pro=1,asp=12,enc=4)
    _canThrow(item, acc=0, rng=11, skill=SKL_TIPFIRST)
    _length(item, 200)
def _mPole(item):
    rog.world().component_for_entity(item, cmp.Draw).char = T_TWOHANDWEAP
    rog.make(item, TWOHANDS)
    _weapon(item, acc=5,dmg=6,pen=6,dv=1,av=1,pro=1,asp=18,enc=4)
    _canThrow(item, acc=0, rng=12, skill=SKL_TIPFIRST)
    _length(item, 200)

    # other raw mats
def _spoolString(item):
    _canThrow(item, acc=-6, rng=6, dmg=1, pen=-1, skill=SKL_PITCHING)
def _spoolFishingWire(item):
    _canThrow(item, acc=-6, rng=6, dmg=2, skill=SKL_PITCHING)
def _pBottle(item):
    _canThrow(item, acc=-2, rng=8, skill=SKL_ENDOVEREND)
    _length(item, 10)
def _gBottle(item):
    _canThrow(item, acc=2, rng=12, dmg=2, skill=SKL_ENDOVEREND)
    _weapon(item, acc=0,dmg=2,pen=1,asp=-12, skill=SKL_BLUDGEONS)
    _length(item, 10)
def _pPipe(item):
    _canThrow(item, acc=0, rng=8)
    _weapon(item, acc=0,asp=-15,enc=5)
    _length(item, 35)
def _dust(item):
    rog.world().component_for_entity(item, cmp.Draw).char = T_DUST
    _canThrow( item, rng=2, acc=5, dmg=1, pen=5, asp=-15,
              elem=ELEM_BIO, elemDmg=10 ) # blow dust in enemy's faces
##    rog.world().add_component(item, cmp.Usable(funcPC, funcNPC))
def _log(item):
    rog.world().add_component( item, cmp.Harvestable(
        4800,
        {'slab of wood':3},
        {cmp.Tool_Saw:4}
        ) )
def _plank(item):
    rog.make(item, TWOHANDS)
    _weapon(item, acc=3,dmg=3,pen=1,av=1,pro=1,asp=-51,enc=26)
    _canThrow(item, acc=-5, rng=3, skill=SKL_TIPFIRST)
    _length(item, 200)
def _skull(item):
    rog.world().add_component(item, cmp.Tool_Hammer(1))
    _weapon(item, acc=-2,dmg=2,pen=1,asp=-15,enc=15)
    _canThrow(item, acc=0, dmg=0, rng=8, skill=SKL_PITCHING)
def _bone(item):
    rog.world().add_component(item, cmp.Tool_Hammer(2))
    _weapon(item, acc=1,dmg=3,pen=3,asp=6,enc=2)
    _canThrow(item, acc=2, dmg=1, rng=12, skill=SKL_ENDOVEREND)
    _length(item, 50)
def _bBone(item):
    rog.world().add_component(item, cmp.Tool_Hammer(1))
    _weapon(item, acc=1,dmg=3,pen=4,asp=12,enc=2)
    _canThrow(item, acc=-3, rng=8, skill=SKL_ENDOVEREND)
    _length(item, 25)
def _boneLarge(item):
    rog.make(item, TWOHANDS)
    rog.world().add_component(item, cmp.Tool_Hammer(1))
    _weapon(item, acc=-4,dmg=6,pen=6,asp=-12,enc=10)
    _canThrow(item, acc=-5, rng=8)
    _length(item, 90)
def _boneSmall(item):
    _weapon(item, acc=-2,dmg=1,pen=1,asp=-6)
    _canThrow(item, acc=-1, rng=6)
    _length(item, 25)
def _mPipe(item):
    rog.world().add_component(item, cmp.Tool_Hammer(2))
    _weapon(item, acc=1,dmg=6,pen=5,asp=-45,enc=6)
    _canThrow(item, acc=-2, rng=6, dmg=-1, skill=SKL_ENDOVEREND)
    _length(item, 50)
def _mPipeBroken(item):
    _weapon(item, acc=1,dmg=4,pen=6,asp=-33,enc=6)
    _canThrow(item, acc=-5, rng=5, dmg=-1, skill=SKL_ENDOVEREND)
    _length(item, 30)
def _mBar(item):
    rog.make(item, TWOHANDS)
    rog.world().add_component(item, cmp.Tool_Hammer(1))
    _weapon(item, acc=-2,dmg=2,pen=2,asp=-60,enc=6)
    _canThrow(item, acc=0, dmg=1, rng=6)
    _length(item, 50)
def _razorBlade(item):
    _melee_bleed(item, 25)
    rog.world().add_component(item, cmp.Tool_Cut(7))
    _weapon(item, acc=0,dmg=3,pen=6,asp=-24,enc=2)
    _length(item, 5)
def _nail(item):
    _canThrow(item, acc=-10, dmg=-1, rng=3)
    _weapon(item, acc=-5,dmg=1,pen=2,asp=-66)
    _length(item, 3)
def _screw(item):
    _canThrow(item, acc=-10, dmg=-1, rng=3)
    _weapon(item, acc=-5,dmg=1,pen=1,asp=-66)
    _length(item, 2)
def _mWire(item):
    rog.make(item, TWOHANDS)
    _weapon(item, acc=-11,dmg=4,pen=3,asp=-45)
    _length(item, 100)
def _mCan(item):
    _canThrow(item, acc=-7, rng=3)
    _length(item, 10)
def _mNeedle(item):
    _canThrow(item, acc=-10, rng=2)
    _weapon(item, acc=-7,dmg=1,pen=5,asp=-66)
    _length(item, 5)
def _mTube(item):
    _canThrow(item, acc=0, rng=4, skill=SKL_ENDOVEREND)
    _weapon(item, acc=0,dmg=1,pen=0,asp=-51,enc=2)
    _length(item, 50)
def _bobbyPin(item):
    _canThrow(item, acc=-5, rng=2, dmg=-2)
    rog.world().add_component(item, cmp.Tool_LockPick(1))
    _length(item, 3)
def _lockPick(item):
    _canThrow(item, acc=-5, rng=3, dmg=-2)
    rog.world().add_component(item, cmp.Tool_LockPick(3))
    _length(item, 3)
def _key(item):
    _canThrow(item, acc=-5, rng=4, dmg=1)
    _length(item, 3)
def _magnetWeak(item):
    _canThrow(item, acc=-2, rng=4)
def _magnet(item):
    _canThrow(item, acc=-2, rng=6)
def _magnetStrong(item):
    _canThrow(item, acc=-2, rng=8, dmg=1, pen=-1)
def _cordage(item):
    rog.make(item, TWOHANDS)
    _weapon(item, acc=-5,dmg=2,pen=3,asp=-42)
    _canThrow(item, acc=0, rng=3, pen=-6, dmg=-2)
    _length(item, 100)
def _rope(item):
    rog.make(item, TWOHANDS)
    _weapon(item, acc=-5,dmg=3,pen=3,asp=-48,enc=6)
    _canThrow(item, acc=0, rng=2, pen=-3, dmg=-1)
    _length(item, 100)
def _cable(item):
    _length(item, 100)
def _chainLight(item):
    rog.make(item, TWOHANDS)
    _weapon(item, acc=-6,dmg=4,pen=4,asp=-48,enc=33)
    _length(item, 100)
def _chain(item):
    rog.make(item, TWOHANDS)
    _weapon(item, acc=-11,dmg=5,pen=3,asp=-60,enc=51)
    _length(item, 100)
def _chainHeavy(item):
    _length(item, 100)
def _magnifyingGlass(item):
    rog.world().add_component(item, cmp.Tool_Lens(2))
    rog.world().add_component(item, cmp.Tool_Identify(2))
    
    
##def _hammer(item, acc=0, rng=10, hammer=3):
##    rog.world().add_component(item, cmp.Tool_Hammer(hammer))
##    _canThrow(item, acc=acc, rng=rng)
def _hammer(item, hammer, acc=0, rng=10, cm=20):
    rog.world().add_component(item, cmp.Tool_Hammer(hammer))
    _canThrow(item, acc=acc, rng=rng, skill=SKL_ENDOVEREND)
    rog.world().add_component(item, cmp.WeaponSkill(SKL_HAMMERS))
    _length(item, cm)
def _1hammer(item):
    _hammer(item, 1, acc=-1, rng=12)
def _2hammer(item):
    _hammer(item, 2, acc=-1, rng=13)
def _3hammer(item):
    _hammer(item, 3, acc=-1, rng=15)
def _4hammer(item):
    _hammer(item, 4, acc=-1, rng=13)
def _5hammer(item):
    _hammer(item, 5, acc=-2, rng=10)
def _axe(item, chop=2, chisel=1, hammer=2, rng=10, cm=30):
    rog.world().add_component(item, cmp.Tool_Chop(chop))
    rog.world().add_component(item, cmp.Tool_Chisel(chisel))
    rog.world().add_component(item, cmp.Tool_Hammer(hammer))
    _canThrow(item, acc=-5, rng=rng, skill=SKL_ENDOVEREND)
    rog.world().add_component(item, cmp.WeaponSkill(SKL_AXES))
    _length(item, cm)
def _pAxe(item):
    _melee_bleed(item, 0.25*BLEED_PLASTIC)
    _axe(item, chop=2, chisel=1, rng=10)
def _wAxe(item):
    _melee_bleed(item, 0.25*BLEED_WOOD)
    _axe(item, chop=2, chisel=1, rng=10)
    rog.world().add_component(item, cmp.Tool_Cut(1))
def _bAxe(item):
    _melee_bleed(item, 0.25*BLEED_BONE)
    _axe(item, chop=3, chisel=1, rng=10)
    rog.world().add_component(item, cmp.Tool_Cut(1))
def _sAxe(item):
    _melee_bleed(item, 0.25*BLEED_STONE)
    _axe(item, chop=3, chisel=1, rng=10)
    rog.world().add_component(item, cmp.Tool_Cut(1))
def _mAxe(item):
    _melee_bleed(item, 0.25*BLEED_METAL)
    _axe(item, chop=4, chisel=2, hammer=3, rng=12)
    rog.world().add_component(item, cmp.Tool_Cut(2))
def _gAxe(item): # no glass tools can be used as chisels.
    _melee_bleed(item, 0.25*BLEED_GLASS)
    _axe(item, chop=1, chisel=0, rng=10)
    rog.world().add_component(item, cmp.Tool_Cut(6)) 
    # machetes
def _machete(item, machete, cut=1, acc=-2, rng=5, amputate=5, toFlesh=2, cm=50):
    _amputate(item, amputate)
    _bonusToFlesh(item, toFlesh)
    rog.world().add_component(item, cmp.Tool_Cut(cut))
    rog.world().add_component(item, cmp.Tool_Machete(machete))
    _canThrow(item, acc=acc, rng=rng, skill=SKL_TIPFIRST)
    rog.world().add_component(item, cmp.WeaponSkill(SKL_SWORDS))
    _length(item, cm)
def _pMachete(item):
    _melee_bleed(item, 1.5*BLEED_PLASTIC)
    _machete(item, 1, cut=1, acc=-2, rng=5, amputate=1, toFlesh=1, cm=40)
def _wMachete(item):
    _melee_bleed(item, 1.5*BLEED_WOOD)
    _machete(item, 2, cut=2, acc=-2, rng=6, amputate=2, toFlesh=2, cm=40)
def _bMachete(item):
    _melee_bleed(item, 1.5*BLEED_BONE)
    _machete(item, 2, cut=3, acc=-2, rng=8, amputate=5, toFlesh=3, cm=30)
def _mMachete(item):
    _melee_bleed(item, 1.5*BLEED_METAL)
    _machete(item, 3, cut=5, acc=-2, rng=10, amputate=10, toFlesh=4)
    # chisels
def _chisel(item, chisel, cm=5):
    rog.world().add_component(item, cmp.Tool_Chisel(chisel))
    _canThrow(item, acc=-5, rng=4)
    _length(item, cm)
def _3chisel(item):
    _chisel(item, 3)
def _4chisel(item):
    _chisel(item, 4)


    # weapons #

    # clubs
def _club(item, toArmor=3, hammer=1, acc=-3, rng=8, cm=40):
    _bonusToArmor(item, toArmor)
    rog.world().add_component(item, cmp.Tool_Hammer(hammer))
    _canThrow(item, acc=acc, rng=rng, skill=SKL_ENDOVEREND)
    _length(item, cm)
def _pClub(item):
    _club(item, toArmor=1, hammer=1, acc=-2, rng=8)
def _wClub(item):
    _club(item, toArmor=2, hammer=1, acc=-2, rng=8)
def _sClub(item):
    _club(item, toArmor=2, hammer=1, acc=-2, rng=8)
def _bClub(item):
    _club(item, toArmor=2, hammer=1, acc=-2, rng=8)
def _gClub(item):
    _club(item, toArmor=2, hammer=1, acc=-2, rng=8)
def _mClub(item):
    _club(item, toArmor=3, hammer=1, acc=-2, rng=8)
def _cClub(item):
    _club(item, toArmor=2, hammer=1, acc=-2, rng=8)
    # spiked clubs
def _spikedClub(item, toArmor=2, bleed=10, pain=10, rng=8, cm=40):
    _melee_pain(item, pain)
    _melee_bleed(item, bleed)
    _bonusToArmor(item, toArmor)
    _canThrow(item, acc=-2, rng=rng, skill=SKL_ENDOVEREND)
    _length(item, cm)
def _pSpikedClub(item):
    _spikedClub(item, toArmor=2, bleed=10, pain=20, rng=8)
def _wSpikedClub(item):
    _spikedClub(item, toArmor=3, bleed=20, pain=30, rng=8)
    # cudgels
def _cudgel(item, toArmor=2, hammer=2, acc=-3, rng=6, cm=40):
    _bonusToArmor(item, toArmor)
    rog.world().add_component(item, cmp.Tool_Hammer(hammer))
    _canThrow(item, acc=acc, rng=rng, skill=SKL_ENDOVEREND)
    _length(item, cm)
def _pCudgel(item):
    _cudgel(item, toArmor=2, hammer=2, acc=-3, rng=6)
def _wCudgel(item):
    _cudgel(item, toArmor=3, hammer=2, acc=-3, rng=7)
def _sCudgel(item):
    _cudgel(item, toArmor=3, hammer=2, acc=-3, rng=6)
def _bCudgel(item):
    _cudgel(item, toArmor=3, hammer=2, acc=-3, rng=8)
def _gCudgel(item):
    _cudgel(item, toArmor=2, hammer=2, acc=-3, rng=8)
def _mCudgel(item):
    _cudgel(item, toArmor=4, hammer=2, acc=-3, rng=8)
def _cCudgel(item):
    _cudgel(item, toArmor=2, hammer=2, acc=-3, rng=8)
    # warhammers
def _warhammer(item, acc=-2,rng=8, hammer=3, toArmor=4, cm=30):
    _bonusToArmor(item, toArmor)
    rog.world().add_component(item, cmp.Tool_Hammer(hammer))
    _canThrow(item, acc=acc, rng=rng, skill=SKL_ENDOVEREND)
    _length(item, cm)
def _pWarhammer(item):
    _warhammer(item, acc=-4, rng=6, hammer=3, toArmor=4)
def _wWarhammer(item):
    _warhammer(item, acc=-3, rng=8, hammer=3, toArmor=6)
def _bWarhammer(item):
    _warhammer(item, acc=-3, rng=9, hammer=3, toArmor=8)
def _sWarhammer(item):
    _warhammer(item, acc=-3, rng=7, hammer=3, toArmor=10)
def _mWarhammer(item):
    _warhammer(item, acc=-2, rng=10, hammer=4, toArmor=12)
    # morning stars
def _mMorningStar(item):
    _melee_pain(item, 40)
    _melee_bleed(item, 25)
    _canThrow(item, acc=-3, rng=7, skill=SKL_ENDOVEREND)
    _length(item, 50)
    _spikes(item)
    # maces
def _mace(item, toArmor=10, cm=40):
    _melee_pain(item, 10)
    _melee_bleed(item, 5)
    _bonusToArmor(item, toArmor)
    _canThrow(item, acc=-2, rng=8, skill=SKL_ENDOVEREND)
    _length(item, cm)
    _studs(item)
def _pMace(item):
    _mace(item, toArmor=1)
def _wMace(item):
    _mace(item, toArmor=2)
def _sMace(item):
    _mace(item, toArmor=3)
def _bMace(item):
    _mace(item, toArmor=3)
def _mMace(item):
    _mace(item, toArmor=4)
def _gMace(item):
    _mace(item, toArmor=0)
def _cMace(item):
    _mace(item, toArmor=1)
    # war axes
def _warAxe(item, chop=1, chisel=0, hammer=1, acc=-5, rng=10, amputate=5, bleed=5, cm=30):
    _amputate(item, amputate)
    _melee_bleed(item, bleed)
    _canThrow(item, acc=acc, rng=rng, skill=SKL_ENDOVEREND)
    _length(item, cm)
    rog.world().add_component(item, cmp.Tool_Chop(chop))
    rog.world().add_component(item, cmp.Tool_Hammer(hammer))
    if chisel:
        rog.world().add_component(item, cmp.Tool_Chisel(chisel))
def _pWarAxe(item):
    _warAxe(item, chop=1, chisel=1, hammer=1, acc=-5, rng=12,
            bleed=BLEED_PLASTIC, amputate=1)
def _wWarAxe(item):
    _warAxe(item, chop=1, chisel=1, hammer=2, acc=-5, rng=14,
            bleed=BLEED_WOOD, amputate=2)
def _bWarAxe(item):
    _warAxe(item, chop=2, chisel=1, hammer=2, acc=-5, rng=14,
            bleed=BLEED_BONE, amputate=3)
def _sWarAxe(item):
    _warAxe(item, chop=2, chisel=2, hammer=2, acc=-5, rng=14,
            bleed=BLEED_STONE, amputate=4)
def _mWarAxe(item):
    _warAxe(item, chop=3, chisel=3, hammer=3, acc=-5, rng=16,
            bleed=BLEED_METAL, amputate=5)
def _gWarAxe(item): # glass tools cannot be effective chisels, choppers, hammers, etc.
    rog.world().add_component(item, cmp.Tool_Hammer(1))
    _canThrow(item, chop=1, chisel=0, acc=-5, rng=12,
            bleed=BLEED_METAL, amputate=5)
    # tomahawks (basically a knife on a stick)
def _tomahawk(item, chop=1, acc=-5, rng=10, bleed=0, cm=25):
    _melee_bleed(item, bleed)
    rog.world().add_component(item, cmp.Tool_Chop(chop))
    _canThrow(item, acc=acc, rng=rng, skill=SKL_ENDOVEREND)
    _length(item, cm)
def _pTomahawk(item):
    _tomahawk(item, chop=1, acc=-2, rng=16, bleed=BLEED_PLASTIC)
def _wTomahawk(item):
    _tomahawk(item, chop=2, acc=-2, rng=18, bleed=BLEED_WOOD)
def _sTomahawk(item):
    _tomahawk(item, chop=3, acc=-2, rng=18, bleed=BLEED_STONE)
def _bTomahawk(item):
    _tomahawk(item, chop=3, acc=-2, rng=18, bleed=BLEED_BONE)
def _mTomahawk(item):
    _tomahawk(item, chop=4, acc=-2, rng=20, bleed=BLEED_METAL)
def _gTomahawk(item):
    _tomahawk(item, chop=2, acc=-2, rng=20, bleed=BLEED_GLASS)
def _cTomahawk(item):
    _tomahawk(item, chop=2, acc=-2, rng=20, bleed=BLEED_CERAMIC)
    # swords
def _pSword(item):
    _melee_bleed(item, BLEED_PLASTIC)
    rog.world().add_component(item, cmp.Tool_Cut(1))
    _canThrow(item, acc=-6, rng=4, skill=SKL_TIPFIRST)
    _length(item, 80)
def _wSword(item):
    _melee_bleed(item, BLEED_WOOD)
    rog.world().add_component(item, cmp.Tool_Cut(2))
    rog.world().add_component(item, cmp.Tool_Machete(1))
    _canThrow(item, acc=-6, rng=6, skill=SKL_TIPFIRST)
    _length(item, 60)
def _bSword(item):
    _melee_bleed(item, BLEED_BONE)
    rog.world().add_component(item, cmp.Tool_Cut(3))
    rog.world().add_component(item, cmp.Tool_Machete(1))
    _canThrow(item, acc=-6, rng=8, skill=SKL_TIPFIRST)
    _length(item, 40)
def _sSword(item):
    _melee_bleed(item, BLEED_STONE)
    rog.world().add_component(item, cmp.Tool_Cut(4))
    rog.world().add_component(item, cmp.Tool_Chisel(1))
    rog.world().add_component(item, cmp.Tool_Machete(1))
    _canThrow(item, acc=-6, rng=5, skill=SKL_TIPFIRST)
    _length(item, 30)
def _mSword(item):
    _melee_bleed(item, BLEED_METAL)
    rog.world().add_component(item, cmp.Tool_Cut(5))
    rog.world().add_component(item, cmp.Tool_Machete(2))
    rog.world().add_component(item, cmp.Tool_Chisel(2))
    rog.world().add_component(item, cmp.Tool_Chop(1))
    _canThrow(item, acc=-4, rng=10, skill=SKL_TIPFIRST)
    _length(item, 75)
def _dSword(item): #diamonite
    _melee_bleed(item, BLEED_DIAMONITE)
    _amputate(item, 5)
    rog.world().add_component(item, cmp.Tool_Cut(7))
    rog.world().add_component(item, cmp.Tool_Machete(2))
    rog.world().add_component(item, cmp.Tool_Chisel(2))
    rog.world().add_component(item, cmp.Tool_Chop(1))
    rog.world().add_component(item, cmp.Tool_Saw(1))
    _canThrow(item, acc=-4, rng=12, skill=SKL_TIPFIRST)
    _length(item, 65)
def _grSword(item): #graphene
    _melee_bleed(item, BLEED_GRAPHENE)
    _amputate(item, 10)
    rog.world().add_component(item, cmp.Tool_Cut(7))
    rog.world().add_component(item, cmp.Tool_Machete(3))
    rog.world().add_component(item, cmp.Tool_Chisel(3))
    rog.world().add_component(item, cmp.Tool_Chop(2))
    rog.world().add_component(item, cmp.Tool_Saw(2))
    _canThrow(item, acc=-4, rng=12, skill=SKL_TIPFIRST)
    _length(item, 85)
    # shivs
def _pShiv(item):
    _melee_bleed(item, BLEED_PLASTIC)
    rog.world().add_component(item, cmp.Tool_Cut(2))
    _canThrow(item, acc=-15, rng=4, dmg=-2, pen=-4, skill=SKL_ENDOVEREND)
    _length(item, 5)
def _wShiv(item):
    _melee_bleed(item, BLEED_WOOD)
    rog.world().add_component(item, cmp.Tool_Cut(3))
    rog.world().add_component(item, cmp.Tool_Chisel(1))
    _canThrow(item, acc=-12, rng=6, dmg=-1, pen=-4, skill=SKL_ENDOVEREND)
    _length(item, 5)
def _bShiv(item):
    _melee_bleed(item, BLEED_BONE)
    rog.world().add_component(item, cmp.Tool_Cut(3))
    rog.world().add_component(item, cmp.Tool_Chisel(1))
    _canThrow(item, acc=-12, rng=6, dmg=-1, pen=-4, skill=SKL_ENDOVEREND)
    _length(item, 5)
def _sShiv(item):
    _melee_bleed(item, BLEED_STONE)
    rog.world().add_component(item, cmp.Tool_Cut(4))
    rog.world().add_component(item, cmp.Tool_Chisel(2))
    _canThrow(item, acc=-12, rng=7, dmg=0, pen=-4, skill=SKL_ENDOVEREND)
    _length(item, 5)
def _gShiv(item):
    _melee_bleed(item, BLEED_GLASS)
    rog.world().add_component(item, cmp.Tool_Cut(6))
    _canThrow(item, acc=-10, rng=7, dmg=-2, pen=-4, skill=SKL_ENDOVEREND)
    _length(item, 5)
def _mShiv(item):
    _melee_bleed(item, BLEED_METAL)
    rog.world().add_component(item, cmp.Tool_Cut(5))
    rog.world().add_component(item, cmp.Tool_Chisel(3))
    _canThrow(item, acc=-10, rng=8, dmg=0, pen=-4, skill=SKL_ENDOVEREND)
    _length(item, 5)
def _cShiv(item):
    _melee_bleed(item, BLEED_CERAMIC)
    rog.world().add_component(item, cmp.Tool_Cut(7))
    _canThrow(item, acc=-10, rng=7, dmg=-2, pen=-4, skill=SKL_ENDOVEREND)
    _length(item, 5)
def _grShiv(item):
    _melee_bleed(item, BLEED_GRAPHENE)
    rog.world().add_component(item, cmp.Tool_Cut(8))
    rog.world().add_component(item, cmp.Tool_Chisel(3))
    rog.world().add_component(item, cmp.Tool_Saw(2))
    _canThrow(item, acc=-10, rng=8, dmg=0, pen=-4, skill=SKL_ENDOVEREND)
    _length(item, 5)
    # knives
def _pKnife(item):
    _melee_bleed(item, BLEED_PLASTIC)
    rog.world().add_component(item, cmp.Tool_Cut(3))
    rog.world().add_component(item, cmp.Tool_Chisel(1))
    _canThrow(item, acc=-10, rng=6, dmg=-1, pen=-4, skill=SKL_ENDOVEREND)
    _length(item, 10)
def _wKnife(item):
    _melee_bleed(item, BLEED_WOOD)
    rog.world().add_component(item, cmp.Tool_Cut(4))
    rog.world().add_component(item, cmp.Tool_Chisel(1))
    _canThrow(item, acc=-6, rng=8, dmg=-1, pen=-4, skill=SKL_ENDOVEREND)
    _length(item, 10)
def _bKnife(item):
    _melee_bleed(item, BLEED_BONE)
    rog.world().add_component(item, cmp.Tool_Cut(4))
    rog.world().add_component(item, cmp.Tool_Chisel(2))
    _canThrow(item, acc=-6, rng=10, dmg=-1, pen=-4, skill=SKL_ENDOVEREND)
    _length(item, 10)
def _sKnife(item):
    _melee_bleed(item, BLEED_STONE)
    rog.world().add_component(item, cmp.Tool_Cut(5))
    rog.world().add_component(item, cmp.Tool_Chisel(2))
    rog.world().add_component(item, cmp.Tool_Saw(1))
    _canThrow(item, acc=-6, rng=10, dmg=0, pen=-4, skill=SKL_ENDOVEREND)
    _length(item, 10)
def _mKnife(item):
    _melee_bleed(item, BLEED_METAL)
    rog.world().add_component(item, cmp.Tool_Cut(6))
    rog.world().add_component(item, cmp.Tool_Chisel(3))
    rog.world().add_component(item, cmp.Tool_Saw(1))
    _canThrow(item, acc=-4, rng=12, dmg=0, pen=-4, skill=SKL_ENDOVEREND)
    _length(item, 10)
def _gKnife(item):
    _melee_bleed(item, BLEED_GLASS)
    rog.world().add_component(item, cmp.Tool_Cut(7))
    _canThrow(item, acc=-4, rng=10, dmg=-3, pen=-4, skill=SKL_ENDOVEREND)
    _length(item, 10)
def _cKnife(item):
    _melee_bleed(item, BLEED_CERAMIC)
    rog.world().add_component(item, cmp.Tool_Cut(8))
    _canThrow(item, acc=-4, rng=10, dmg=-3, pen=-4, skill=SKL_ENDOVEREND)
    _length(item, 10)
def _grKnife(item):
    _melee_bleed(item, BLEED_GRAPHENE)
    rog.world().add_component(item, cmp.Tool_Cut(9))
    rog.world().add_component(item, cmp.Tool_Chisel(3))
    rog.world().add_component(item, cmp.Tool_Saw(2))
    _canThrow(item, acc=-5, rng=14, dmg=-4, pen=-6, skill=SKL_ENDOVEREND)
    _length(item, 10)
    # serrated knives
def _pSerrated(item):
    _melee_bleed(item, 2*BLEED_PLASTIC)
    _melee_pain(item, 10)
    rog.world().add_component(item, cmp.Tool_Cut(2))
    rog.world().add_component(item, cmp.Tool_Saw(1))
    _canThrow(item, acc=-10, rng=6, dmg=-2, pen=-4, skill=SKL_ENDOVEREND)
    _length(item, 10)
def _wSerrated(item):
    _melee_bleed(item, 2*BLEED_WOOD)
    _melee_pain(item, 20)
    rog.world().add_component(item, cmp.Tool_Cut(3))
    rog.world().add_component(item, cmp.Tool_Saw(1))
    _canThrow(item, acc=-6, rng=8, dmg=-2, pen=-4, skill=SKL_ENDOVEREND)
    _length(item, 10)
def _bSerrated(item):
    _melee_bleed(item, 2*BLEED_BONE)
    _melee_pain(item, 20)
    rog.world().add_component(item, cmp.Tool_Cut(3))
    rog.world().add_component(item, cmp.Tool_Saw(1))
    rog.world().add_component(item, cmp.Tool_Chisel(1))
    _canThrow(item, acc=-6, rng=10, dmg=-2, pen=-4, skill=SKL_ENDOVEREND)
    _length(item, 10)
def _sSerrated(item):
    _melee_bleed(item, 2*BLEED_STONE)
    _melee_pain(item, 20)
    rog.world().add_component(item, cmp.Tool_Cut(4))
    rog.world().add_component(item, cmp.Tool_Saw(2))
    rog.world().add_component(item, cmp.Tool_Chisel(1))
    _canThrow(item, acc=-6, rng=10, dmg=-2, pen=-4, skill=SKL_ENDOVEREND)
    _length(item, 10)
def _mSerrated(item):
    _melee_bleed(item, 2*BLEED_METAL)
    _melee_pain(item, 30)
    rog.world().add_component(item, cmp.Tool_Cut(5))
    rog.world().add_component(item, cmp.Tool_Chisel(2))
    rog.world().add_component(item, cmp.Tool_Saw(2))
    _canThrow(item, acc=-4, rng=12, dmg=-2, pen=-4, skill=SKL_ENDOVEREND)
    _length(item, 10)
def _gSerrated(item):
    _melee_bleed(item, 2*BLEED_GLASS)
    _melee_pain(item, 10)
    rog.world().add_component(item, cmp.Tool_Cut(6))
    rog.world().add_component(item, cmp.Tool_Saw(1))
    _canThrow(item, acc=-4, rng=10, dmg=-5, pen=-4, skill=SKL_ENDOVEREND)
    _length(item, 10)
    # war knives    # TO ADD: Counter ability
def _pWarKnife(item):
    _melee_bleed(item, BLEED_PLASTIC)
    rog.world().add_component(item, cmp.Tool_Cut(3))
    rog.world().add_component(item, cmp.Tool_Chisel(1))
    _canThrow(item, acc=-5,  rng=10, dmg=0, pen=-4, skill=SKL_ENDOVEREND)
    _length(item, 15)
def _wWarKnife(item):
    _melee_bleed(item, BLEED_WOOD)
    rog.world().add_component(item, cmp.Tool_Cut(4))
    rog.world().add_component(item, cmp.Tool_Chisel(1))
    _canThrow(item, acc=-5, rng=10, dmg=0, pen=-4, skill=SKL_ENDOVEREND)
    _length(item, 15)
def _bWarKnife(item):
    _melee_bleed(item, BLEED_BONE)
    rog.world().add_component(item, cmp.Tool_Cut(4))
    rog.world().add_component(item, cmp.Tool_Chisel(2))
    _canThrow(item, acc=-5, rng=12, dmg=0, pen=-4, skill=SKL_ENDOVEREND)
    _length(item, 15)
def _sWarKnife(item):
    _melee_bleed(item, BLEED_STONE)
    rog.world().add_component(item, cmp.Tool_Cut(5))
    rog.world().add_component(item, cmp.Tool_Chisel(2))
    rog.world().add_component(item, cmp.Tool_Saw(1))
    _canThrow(item, acc=-5, rng=12, dmg=1, pen=-4, skill=SKL_ENDOVEREND)
    _length(item, 15)
def _mWarKnife(item):
    _melee_bleed(item, BLEED_METAL)
    rog.world().add_component(item, cmp.Tool_Cut(6))
    rog.world().add_component(item, cmp.Tool_Chisel(3))
    rog.world().add_component(item, cmp.Tool_Saw(1))
    _canThrow(item, acc=-2, rng=14, dmg=1, pen=-4, skill=SKL_ENDOVEREND)
    _length(item, 15)
def _gWarKnife(item):
    _melee_bleed(item, BLEED_GLASS)
    rog.world().add_component(item, cmp.Tool_Cut(7))
    _canThrow(item, acc=-2, rng=12, dmg=-2, pen=-4, skill=SKL_ENDOVEREND)
    _length(item, 15)
def _cWarKnife(item):
    _melee_bleed(item, BLEED_CERAMIC)
    rog.world().add_component(item, cmp.Tool_Cut(8))
    _canThrow(item, acc=-2, rng=12, dmg=-2, pen=-4, skill=SKL_ENDOVEREND)
    _length(item, 15)
    # daggers
def _bDagger(item):
    _melee_bleed(item, BLEED_BONE)
    rog.world().add_component(item, cmp.Tool_Cut(4))
    rog.world().add_component(item, cmp.Tool_Chisel(2))
    _canThrow(item, acc=-2, rng=12, dmg=-2, pen=-16, skill=SKL_ENDOVEREND)
    _length(item, 20)
def _gDagger(item):
    _melee_bleed(item, BLEED_GLASS)
    rog.world().add_component(item, cmp.Tool_Cut(7))
    _canThrow(item, acc=-2, rng=14, dmg=-6, pen=-16, skill=SKL_ENDOVEREND)
    _length(item, 20)
def _mDagger(item):
    _melee_bleed(item, BLEED_METAL)
    rog.world().add_component(item, cmp.Tool_Cut(6))
    rog.world().add_component(item, cmp.Tool_Chisel(3))
    _canThrow(item, acc=-2, rng=15, dmg=-2, pen=-16, skill=SKL_ENDOVEREND)
    _length(item, 20)
def _rondelDagger(item):
    _melee_bleed(item, BLEED_STEEL)
    rog.world().add_component(item, cmp.Tool_Cut(7))
    _canThrow(item, acc=-5, rng=8, dmg=-4, pen=-24, skill=SKL_ENDOVEREND)
    _length(item, 20)
# javelins and shortspears do NOT have reach
def _javelin(item, acc=2,rng=32,dmg=2,pen=2,bleed=5):
    _melee_bleed(item, bleed)
    _canThrow(item, acc=acc, rng=rng, dmg=dmg, pen=pen, skill=SKL_TIPFIRST)
    _length(item, 100)
def _pJavelin(item):
    _javelin(item, acc=2, rng=26, dmg=2, pen=1, bleed=0.5*BLEED_PLASTIC)
    _length(item, 100)
def _wJavelin(item):
    _javelin(item, acc=3, rng=28, dmg=2, pen=2, bleed=0.5*BLEED_WOOD)
    _length(item, 100)
def _mJavelin(item):
    _javelin(item, acc=4, rng=30, dmg=2, pen=4, bleed=0.5*BLEED_METAL)
    _length(item, 90)
def _shortSpear(item, acc=2, rng=26, dmg=2, pen=1, cut=1, bleed=0, cm=80):
    _melee_bleed(item, bleed)
    rog.world().add_component(item, cmp.Tool_Cut(cut))
    _canThrow(item, acc=acc, rng=rng, dmg=dmg, pen=pen, skill=SKL_TIPFIRST)
    _length(item, cm)
def _pShortSpear(item):
    _shortSpear(item, acc=2,rng=24,dmg=2,pen=1,cut=1,bleed=BLEED_PLASTIC)
def _wShortSpear(item):
    _shortSpear(item, acc=2,rng=26,dmg=2,pen=1,cut=1,bleed=BLEED_WOOD)
def _bShortSpear(item):
    _shortSpear(item, acc=2,rng=26,dmg=2,pen=2,cut=2,bleed=BLEED_BONE)
def _sShortSpear(item):
    _shortSpear(item, acc=2,rng=24,dmg=2,pen=2,cut=3,bleed=BLEED_STONE)
def _gShortSpear(item):
    _shortSpear(item, acc=2,rng=28,dmg=2,pen=0,cut=5,bleed=BLEED_GLASS)
def _mShortSpear(item):
    _shortSpear(item, acc=2,rng=28,dmg=2,pen=3,cut=4,bleed=BLEED_METAL)
def _cShortSpear(item):
    _shortSpear(item, acc=2,rng=28,dmg=2,pen=0,cut=5,bleed=BLEED_CERAMIC)
    # shields
def _buckler(item):
    rog.world().add_component(item, cmp.Tool_Hammer(1))
    _canThrow(item, acc=0, rng=9, skill=SKL_SPINNING)
    _length(item, 8)
def _rotella(item):
    rog.world().add_component(item, cmp.Tool_Hammer(1))
    _canThrow(item, acc=-2, rng=7, skill=SKL_SPINNING)
    _length(item, 16)
def _shield(item):
    _canThrow(item, acc=-5, rng=5, skill=SKL_SPINNING)
    _length(item, 32)
def _scutum(item):
    _canThrow(item, acc=-10, rng=3, skill=SKL_THROWING)
    _length(item, 32)
def _towerShield(item):
    _canThrow(item, acc=-15, rng=2, skill=SKL_THROWING)
    _length(item, 32)
    # boomerangs
def _pBoomerang(item):
    _melee_bleed(item, 0.25*BLEED_PLASTIC)
    rog.world().add_component(item, cmp.Tool_Cut(1))
    _canThrow(item, acc=3, rng=32, dmg=3, pen=2, skill=SKL_SPINNING)
    _length(item, 50)
def _wBoomerang(item):
    _melee_bleed(item, 0.25*BLEED_WOOD)
    rog.world().add_component(item, cmp.Tool_Cut(2))
    _canThrow(item, acc=10, rng=50, dmg=3, pen=2, skill=SKL_SPINNING)
    _length(item, 45)
def _bBoomerang(item):
    _melee_bleed(item, 0.25*BLEED_BONE)
    rog.world().add_component(item, cmp.Tool_Cut(3))
    _canThrow(item, acc=6, rng=40, dmg=3, pen=2, skill=SKL_SPINNING)
    _length(item, 30)
def _gBoomerang(item):
    _melee_bleed(item, 0.25*BLEED_GLASS)
    rog.world().add_component(item, cmp.Tool_Cut(5))
    _canThrow(item, acc=6, rng=42, dmg=3, pen=2, skill=SKL_SPINNING)
    _length(item, 25)
def _mBoomerang(item):
    _melee_bleed(item, 0.25*BLEED_METAL)
    rog.world().add_component(item, cmp.Tool_Cut(4))
    _canThrow(item, acc=8, rng=46, dmg=3, pen=2, skill=SKL_SPINNING)
    _length(item, 20)
def _cBoomerang(item):
    _melee_bleed(item, 0.25*BLEED_CERAMIC)
    rog.world().add_component(item, cmp.Tool_Cut(5))
    _canThrow(item, acc=6, rng=36, dmg=3, pen=2, skill=SKL_SPINNING)
    _length(item, 20)
    # bayonets
def _pBayonet(item):
    _mod(item, MOD_BAYONET, {'atk':1,'dmg':2,'pen':2,})
    _melee_bleed(item, BLEED_PLASTIC)
    rog.world().add_component(item, cmp.Tool_Cut(2))
    rog.world().add_component(item, cmp.Tool_Chisel(1))
    _canThrow(item, acc=-9, rng=6, dmg=-3, pen=-4, skill=SKL_ENDOVEREND)
    _length(item, 20)
def _wBayonet(item):
    _mod(item, MOD_BAYONET, {'atk':1,'dmg':3,'pen':3,})
    _melee_bleed(item, BLEED_WOOD)
    rog.world().add_component(item, cmp.Tool_Cut(3))
    rog.world().add_component(item, cmp.Tool_Chisel(1))
    _canThrow(item, acc=-8, rng=8, dmg=-3, pen=-4, skill=SKL_ENDOVEREND)
    _length(item, 20)
def _bBayonet(item):
    _mod(item, MOD_BAYONET, {'atk':1,'dmg':5,'pen':6,})
    _melee_bleed(item, BLEED_BONE)
    rog.world().add_component(item, cmp.Tool_Cut(4))
    rog.world().add_component(item, cmp.Tool_Chisel(1))
    _canThrow(item, acc=-8, rng=6, dmg=-3, pen=-4, skill=SKL_ENDOVEREND)
    _length(item, 20)
def _sBayonet(item):
    _mod(item, MOD_BAYONET, {'atk':1,'dmg':3,'pen':4,})
    _melee_bleed(item, BLEED_STONE)
    rog.world().add_component(item, cmp.Tool_Cut(5))
    rog.world().add_component(item, cmp.Tool_Chisel(1))
    rog.world().add_component(item, cmp.Tool_Saw(1))
    _canThrow(item, acc=-8, rng=6, dmg=-3, pen=-4, skill=SKL_ENDOVEREND)
    _length(item, 20)
def _mBayonet(item):
    _mod(item, MOD_BAYONET, {'atk':2,'dmg':6,'pen':8,'reach':1,})
    _melee_bleed(item, BLEED_METAL)
    rog.world().add_component(item, cmp.Tool_Cut(6))
    rog.world().add_component(item, cmp.Tool_Chisel(2))
    rog.world().add_component(item, cmp.Tool_Saw(1))
    _canThrow(item, acc=-6, rng=8, dmg=-3, pen=-4, skill=SKL_ENDOVEREND)
    _length(item, 20)
def _gBayonet(item):
    _mod(item, MOD_BAYONET, {'atk':1,'dmg':12,'pen':2,})
    _melee_bleed(item, BLEED_GLASS)
    rog.world().add_component(item, cmp.Tool_Cut(7))
    _canThrow(item, acc=-6, rng=6, dmg=-5, pen=-4, skill=SKL_ENDOVEREND)
    _length(item, 20)
def _cBayonet(item):
    _mod(item, MOD_BAYONET, {'atk':2,'dmg':14,'pen':3,})
    _melee_bleed(item, BLEED_CERAMIC)
    rog.world().add_component(item, cmp.Tool_Cut(8))
    _canThrow(item, acc=-6, rng=6, dmg=-5, pen=-4, skill=SKL_ENDOVEREND)
    _length(item, 20)
    # misc weapons
def _baton(item):
    _canThrow(item, acc=0, rng=10, pen=-3, skill=SKL_ENDOVEREND)
    _length(item, 25)
def _butcherKnife(item):
    _bonusToFlesh(item, 6)
    _amputate(item, 3)
    _melee_bleed(item, 2*BLEED_STEEL)
    rog.world().add_component(item, cmp.Tool_Cut(6))
    rog.world().add_component(item, cmp.Tool_Chop(1))
    _canThrow(item, acc=-4, rng=12, pen=-5, skill=SKL_ENDOVEREND)
    _length(item, 15)
def _kukri(item):
    _bonusToFlesh(item, 6)
    _melee_bleed(item, 1.25*BLEED_STEEL)
    _addRes(item, resrust=50)
    rog.world().add_component(item, cmp.Tool_Cut(7))
    rog.world().add_component(item, cmp.Tool_Chop(4))
    rog.world().add_component(item, cmp.Tool_Chisel(2))
    rog.world().add_component(item, cmp.Tool_Saw(1))
    rog.world().add_component(item, cmp.Tool_Machete(1))
    _canThrow(item, acc=-2, rng=14, pen=-4, skill=SKL_ENDOVEREND)
    _length(item, 20)
def _messer(item):
    _bonusToFlesh(item, 4)
    _melee_bleed(item, 1.25*BLEED_STEEL)
    _amputate(item, 10)
    _addRes(item, resrust=10)
    rog.world().add_component(item, cmp.Tool_Cut(5))
    rog.world().add_component(item, cmp.Tool_Machete(3))
    rog.world().add_component(item, cmp.Tool_Chop(2))
    _canThrow(item, acc=-4, rng=12, pen=-5, skill=SKL_ENDOVEREND)
    _length(item, 65)
def _broadsword(item):
    _bonusToFlesh(item, 4)
    _melee_bleed(item, 1.25*BLEED_STEEL)
    _amputate(item, 15)
    _addRes(item, resrust=20)
    rog.world().add_component(item, cmp.Tool_Cut(4))
    rog.world().add_component(item, cmp.Tool_Chop(2))
    rog.world().add_component(item, cmp.Tool_Machete(2))
    _canThrow(item, acc=-2, rng=12, pen=-4, skill=SKL_ENDOVEREND)
    _length(item, 60)
def _falchion(item):
    _bonusToFlesh(item, 8)
    _melee_bleed(item, 2*BLEED_STEEL)
    _amputate(item, 33)
    _addRes(item, resrust=25)
    rog.world().add_component(item, cmp.Tool_Cut(5))
    rog.world().add_component(item, cmp.Tool_Chop(3))
    rog.world().add_component(item, cmp.Tool_Machete(3))
    _canThrow(item, acc=-2, rng=12, pen=-5, skill=SKL_ENDOVEREND)
    _length(item, 55)
def _armingSword(item):
    _bonusToFlesh(item, 2)
    _melee_bleed(item, 0.75*BLEED_STEEL)
    _amputate(item, 5)
    _addRes(item, resrust=50)
    rog.world().add_component(item, cmp.Tool_Cut(6))
    rog.world().add_component(item, cmp.Tool_Chop(1))
    rog.world().add_component(item, cmp.Tool_Machete(1))
    rog.world().add_component(item, cmp.Tool_Chisel(1))
    _canThrow(item, acc=-2, rng=15, pen=-4, skill=SKL_TIPFIRST)
    _length(item, 90)
def _sabre(item):
    _bonusToFlesh(item, 6)
    _melee_bleed(item, BLEED_STEEL)
    _amputate(item, 10)
    _addRes(item, resrust=20)
    rog.world().add_component(item, cmp.Tool_Cut(5))
    rog.world().add_component(item, cmp.Tool_Machete(2))
    rog.world().add_component(item, cmp.Tool_Chop(1))
    _canThrow(item, acc=-5, rng=10, pen=-4, skill=SKL_ENDOVEREND)
    _length(item, 70)
def _hanger(item):
    _bonusToFlesh(item, 4)
    _melee_bleed(item, BLEED_STEEL)
    _addRes(item, resrust=20)
    rog.world().add_component(item, cmp.Tool_Cut(5))
    rog.world().add_component(item, cmp.Tool_Machete(1))
    _canThrow(item, acc=-5, rng=8, pen=-4, skill=SKL_TIPFIRST)
    _length(item, 55)
def _leafSword(item):
    _melee_bleed(item, BLEED_METAL)
    rog.world().add_component(item, cmp.Tool_Cut(6))
    rog.world().add_component(item, cmp.Tool_Machete(1))
    rog.world().add_component(item, cmp.Tool_Chisel(2))
    rog.world().add_component(item, cmp.Tool_Chop(2))
    _canThrow(item, acc=-4, rng=10, skill=SKL_TIPFIRST)
    _length(item, 35)
def _cutlass(item):
    _bonusToFlesh(item, 6)
    _melee_bleed(item, 1.25*BLEED_STEEL)
    _amputate(item, 15)
    _addRes(item, resrust=20)
    rog.world().add_component(item, cmp.Tool_Cut(5))
    rog.world().add_component(item, cmp.Tool_Machete(1))
    rog.world().add_component(item, cmp.Tool_Chop(1))
    _canThrow(item, acc=-5, rng=8, pen=-4, skill=SKL_TIPFIRST)
    _length(item, 50)
def _curvedSword(item):
    _bonusToFlesh(item, 7)
    _melee_bleed(item, 1.5*BLEED_STEEL)
    _amputate(item, 10)
    _addRes(item, resrust=20)
    rog.world().add_component(item, cmp.Tool_Cut(5))
    rog.world().add_component(item, cmp.Tool_Machete(1))
    _canThrow(item, acc=-5, rng=8, pen=-4, skill=SKL_TIPFIRST)
    _length(item, 40)
def _rapier(item):
    _bonusToFlesh(item, 5)
    _melee_bleed(item, BLEED_STEEL)
    _addRes(item, resrust=50)
    rog.world().add_component(item, cmp.Tool_Cut(5))
    rog.world().add_component(item, cmp.Tool_Machete(1))
    rog.world().add_component(item, cmp.Tool_Chisel(1))
    _canThrow(item, acc=-5, rng=12, pen=-5, skill=SKL_TIPFIRST)
    _length(item, 95)
def _basketHiltedSword(item):
    _bonusToFlesh(item, 4)
    _melee_bleed(item, BLEED_STEEL)
    _amputate(item, 5)
    _addRes(item, resrust=50)
    rog.world().add_component(item, cmp.Tool_Cut(5))
    rog.world().add_component(item, cmp.Tool_Machete(1))
    rog.world().add_component(item, cmp.Tool_Chisel(1))
    _canThrow(item, acc=-5, rng=12, pen=-5, skill=SKL_TIPFIRST)
    _length(item, 80)
def _smallSword(item):
    _bonusToFlesh(item, 3)
    _melee_bleed(item, 0.5*BLEED_STEEL)
    _addRes(item, resrust=50)
    rog.world().add_component(item, cmp.Tool_Cut(3))
    _canThrow(item, acc=-5, rng=8, pen=-6, skill=SKL_TIPFIRST)
    _length(item, 40)
def _whip(item):
    pass
def _rubberBandWhip(item):
    pass
def _bullWhip(item):
    _melee_pain(item, 20)
def _heavyWhip(item):
    pass
def _pushDagger(item):
    _melee_bleed(item, 3*BLEED_METAL)
    rog.world().add_component(item, cmp.Tool_Cut(6))
    rog.world().add_component(item, cmp.Tool_Chisel(1))
    _length(item, 10)
def _crescentBlade(item):
    _melee_bleed(item, 1.5*BLEED_STEEL)
    rog.world().add_component(item, cmp.Tool_Cut(5))
    rog.world().add_component(item, cmp.Tool_Chop(1))
    _length(item, 9)
def _mThrowingKnife(item):
    _melee_bleed(item, BLEED_METAL)
    rog.world().add_component(item, cmp.Tool_Cut(6))
    rog.world().add_component(item, cmp.Tool_Chisel(2))
    _canThrow(item, acc=2, rng=20, dmg=-1, pen=-1, skill=SKL_TIPFIRST)
    _length(item, 6)
def _knuckles(item):
    pass
def _boxingWraps(item):
    pass

    
    # 2-handed weapons #

    # longswords
def _longSword(item):
    _melee_bleed(item, 1.25*BLEED_STEEL)
    _bonusToFlesh(item, 2)
    _amputate(item, 10)
    _addRes(item, resrust=50)
    rog.make(item, TWOHANDS)
    rog.world().add_component(item, cmp.Tool_Cut(2))
    rog.world().add_component(item, cmp.Tool_Chop(2))
    _canThrow(item, acc=-4, rng=10, skill=SKL_TIPFIRST)
    _length(item, 110)
def _katana(item):
    _melee_bleed(item, 2.5*BLEED_STEEL)
    _bonusToFlesh(item, 6)
    _amputate(item, 33)
    _addRes(item, resrust=50)
    rog.make(item, TWOHANDS)
    rog.world().add_component(item, cmp.Tool_Cut(2))
    rog.world().add_component(item, cmp.Tool_Chop(1))
    _canThrow(item, acc=-4, rng=10, skill=SKL_TIPFIRST)
    _length(item, 80)
def _estoc(item):
    _melee_bleed(item, 0.75*BLEED_STEEL)
    _addRes(item, resrust=50)
    rog.make(item, TWOHANDS)
    rog.world().add_component(item, cmp.Tool_Cut(2))
    _canThrow(item, acc=-4, rng=10, skill=SKL_TIPFIRST)
    _length(item, 120)
def _bastardSword(item): # one or two handed longsword
    _melee_bleed(item, 1.5*BLEED_STEEL)
    _amputate(item, 15)
    _addRes(item, resrust=50)
    rog.world().add_component(item, cmp.Tool_Cut(2))
    rog.world().add_component(item, cmp.Tool_Chop(3))
    _canThrow(item, acc=-2, rng=8, skill=SKL_TIPFIRST)
    _length(item, 90)
def _kriegsmesser(item):
    _melee_bleed(item, 2*BLEED_STEEL)
    _bonusToFlesh(item, 5)
    _amputate(item, 50)
    _addRes(item, resrust=50)
    rog.make(item, TWOHANDS)
    rog.world().add_component(item, cmp.Tool_Cut(2))
    rog.world().add_component(item, cmp.Tool_Machete(1))
    rog.world().add_component(item, cmp.Tool_Chop(3))
    _canThrow(item, acc=-5, rng=6, skill=SKL_ENDOVEREND)
    _length(item, 85)
    # greatswords
def _greatSword(item):
    _melee_bleed(item, 1.5*BLEED_STEEL)
    _bonusToFlesh(item, 4)
    _amputate(item, 50)
    _addRes(item, resrust=50)
    rog.make(item, TWOHANDS)
    rog.world().add_component(item, cmp.Tool_Cut(1))
    rog.world().add_component(item, cmp.Tool_Chop(1))
    _canThrow(item, acc=-5, rng=6, skill=SKL_TIPFIRST)
    _length(item, 210)
def _flamberge(item):
    _melee_bleed(item, 2.5*BLEED_STEEL)
    _bonusToFlesh(item, 8)
    _amputate(item, 66)
    _addRes(item, resrust=33)
    rog.make(item, TWOHANDS)
    rog.world().add_component(item, cmp.Tool_Cut(1))
    rog.world().add_component(item, cmp.Tool_Saw(1))
    rog.world().add_component(item, cmp.Tool_Chop(1))
    _canThrow(item, acc=-5, rng=6, skill=SKL_TIPFIRST)
    _length(item, 180)
def _executionerSword(item):
    _melee_bleed(item, 3*BLEED_METAL)
    _amputate(item, 100)
    _bonusToFlesh(item, 16)
    _addRes(item, resrust=33)
    rog.make(item, TWOHANDS)
    rog.world().add_component(item, cmp.Tool_Striker(1))
    _canThrow(item, acc=-15, rng=3, skill=SKL_THROWING)
    _length(item, 150)
    # staves
def _staff(item):
    rog.make(item, TWOHANDS)
    rog.world().add_component(item, cmp.Tool_Hammer(1))
    _canThrow(item, acc=-6, rng=10, skill=SKL_TIPFIRST)
    _length(item, 160)
def _longstaff(item):
    rog.make(item, TWOHANDS)
    rog.world().add_component(item, cmp.Tool_Hammer(1))
    _canThrow(item, acc=-5, rng=15, skill=SKL_TIPFIRST)
    _length(item, 320)
    # spears
def _spear(item, cut=3, hammer=1, chisel=0, acc=0, rng=20, bleed=0, cm=235):
    _melee_bleed(item, bleed)
    rog.make(item, TWOHANDS)
    rog.world().add_component(item, cmp.Tool_Cut(cut))
    rog.world().add_component(item, cmp.Tool_Hammer(hammer))
    _canThrow(item, acc=acc, rng=rng, skill=SKL_TIPFIRST)
    _length(item, cm)
def _pSpear(item):
    _spear(item, cut=0, acc=1, rng=18, bleed=BLEED_PLASTIC)
def _wSpear(item):
    _spear(item, cut=1, acc=3, rng=20, bleed=BLEED_WOOD)
def _bSpear(item):
    _spear(item, cut=1, acc=3, rng=20, bleed=BLEED_BONE)
def _sSpear(item):
    _spear(item, cut=1, acc=2, rng=18, bleed=BLEED_STONE)
def _mSpear(item):
    _spear(item, cut=2, acc=4, rng=22, bleed=BLEED_METAL)
def _gSpear(item):
    _spear(item, cut=3, acc=4, rng=20, bleed=BLEED_GLASS)
def _cSpear(item):
    _spear(item, cut=3, acc=4, rng=22, bleed=BLEED_CERAMIC)
    # partizans
def _mPartizan(item):
    _spear(item, cut=5, acc=2, rng=18, bleed=1.5*BLEED_METAL)
    _amputate(item, 10)
    _length(item, 240)
    # naginatas
def _mNaginata(item):
    _spear(item, cut=6, acc=-2, rng=14, bleed=2*BLEED_METAL)
    rog.world().add_component(item, cmp.Tool_Chop(1))
    _bonusToFlesh(item, 12)
    _amputate(item, 66)
    _length(item, 250)
    # polehammers
def _poleHammer(item, toArmor=10, striker=1, bleed=3, cm=110):
    _bonusToArmor(item, toArmor)
    _melee_bleed(item, bleed)
    rog.make(item, TWOHANDS)
    rog.world().add_component(item, cmp.Tool_Hammer(1))
    rog.world().add_component(item, cmp.Tool_Striker(striker))
    _canThrow(item, acc=-8, rng=4, pen=-10, skill=SKL_TIPFIRST)
    _length(item, cm)
def _pPoleHammer(item):
    _poleHammer(item, toArmor=4, bleed=0)
def _wPoleHammer(item):
    _poleHammer(item, toArmor=6)
def _bPoleHammer(item):
    _poleHammer(item, toArmor=8)
def _sPoleHammer(item):
    _poleHammer(item, toArmor=10)
def _mPoleHammer(item):
    _poleHammer(item, toArmor=12, striker=2, bleed=6)
    _addRes(item, resrust=50)
    # poleaxes
def _poleAxe(item, bleed=20, toArmor=0, amputate=10, chop=1, cm=140):
    if chop: rog.world().add_component(item, cmp.Tool_Chop(chop))
    _melee_bleed(item, bleed)
    _bonusToArmor(item, toArmor)
    _amputate(item, amputate)
    rog.make(item, TWOHANDS)
    _canThrow(item, acc=-10, rng=4, pen=-12, skill=SKL_TIPFIRST)
    _length(item, cm)
def _mPoleAxe(item):
    _poleAxe(item, bleed=1.5*BLEED_METAL, toArmor=2, amputate=10, chop=1)
    _addRes(item, resrust=0)
    # bills
def _bill(item, bleed=20, rng=12, pen=-2, toFlesh=2, cm=200):
    _melee_bleed(item, bleed)
    _bonusToFlesh(item, toFlesh)
    rog.make(item, TWOHANDS)
    _canThrow(item, acc=-5, rng=rng, pen=pen, skill=SKL_TIPFIRST)
    _length(item, cm)
def _mBill(item):
    _bill(item, int(bleed=1.6667*BLEED_METAL), rng=12, pen=-2, toFlesh=4, cm=240)
    _addRes(item, resrust=0)
    # halberds
def _mHalberd(item):
    _melee_bleed(item, int(1.3334*BLEED_METAL))
    rog.world().add_component(item, cmp.Tool_Chop(1))
    _amputate(item, 10)
    rog.make(item, TWOHANDS)
    _canThrow(item, acc=-8, rng=8, pen=-4, skill=SKL_TIPFIRST)
    _addRes(item, resrust=0)
    _length(item, 245)
    # great axes
def _greatAxe(item, acc=-5,rng=5,dmg=-2,pen=-8,bleed=0, chop=1,hammer=1,striker=0,chisel=0,cut=1,amputate=5):
    _melee_bleed(item, bleed)
    _amputate(item, amputate)
    rog.make(item, TWOHANDS)
    if chop: rog.world().add_component(item, cmp.Tool_Chop(chop))
    if hammer: rog.world().add_component(item, cmp.Tool_Hammer(hammer))
    if striker: rog.world().add_component(item, cmp.Tool_Striker(striker))
    if chisel: rog.world().add_component(item, cmp.Tool_Chisel(chisel))
    if cut: rog.world().add_component(item, cmp.Tool_Chisel(cut))
    _canThrow(item, acc=acc, rng=rng, dmg=dmg, pen=pen, skill=SKL_ENDOVEREND)
    _length(item, 80)
def _pGreatAxe(item):
    _greatAxe(item, acc=-5, rng=5, dmg=-2, pen=-12, bleed=2*BLEED_PLASTIC,
              chop=1,hammer=1,striker=0,chisel=0,cut=2,amputate=5)
def _wGreatAxe(item):
    _greatAxe(item, acc=-5, rng=5, dmg=-2, pen=-10, bleed=2*BLEED_WOOD,
              chop=1,hammer=1,striker=0,chisel=0,cut=3,amputate=5)
def _bGreatAxe(item):
    _greatAxe(item, acc=-5, rng=5, dmg=-2, pen=-8, bleed=2*BLEED_BONE,
              chop=2,hammer=1,striker=0,chisel=0,cut=4,amputate=10)
def _sGreatAxe(item):
    _greatAxe(item, acc=-5, rng=5, dmg=-2, pen=-8, bleed=2*BLEED_STONE,
              chop=3,hammer=1,striker=0,chisel=0,cut=4,amputate=10)
def _mGreatAxe(item):
    _greatAxe(item, acc=-5, rng=5, dmg=-2, pen=-8, bleed=2*BLEED_METAL,
              chop=4,hammer=1,striker=1,chisel=1,cut=5,amputate=15)
    _addRes(item, resrust=0)
def _gGreatAxe(item):
    _greatAxe(item, acc=-5, rng=5, dmg=-2, pen=-12, bleed=2*BLEED_GLASS,
              chop=1,hammer=1,striker=0,chisel=0,cut=6,amputate=33)
def _cGreatAxe(item):
    _greatAxe(item, acc=-5, rng=5, dmg=-2, pen=-12, bleed=2*BLEED_CERAMIC,
              chop=1,hammer=1,striker=0,chisel=0,cut=6,amputate=33)
    # battleaxes
def _battleaxe(item, acc=-5, rng=5, dmg=-2, pen=-8, chop=1,chisel=0,hammer=1,striker=0,cut=1,amputate=5):
    _melee_bleed(item, bleed)
    _amputate(item, amputate)
    rog.make(item, TWOHANDS)
    rog.world().add_component(item, cmp.Tool_Chop(chop))
    rog.world().add_component(item, cmp.Tool_Chisel(chisel))
    rog.world().add_component(item, cmp.Tool_Hammer(hammer))
    rog.world().add_component(item, cmp.Tool_Striker(striker))
    rog.world().add_component(item, cmp.Tool_Cut(cut))
    _canThrow(item, acc=acc, rng=rng, dmg=dmg, pen=pen, skill=SKL_ENDOVEREND)
    _length(item, 140)
def _mBattleaxe(item):
    _battleaxe(item,chop=3,chisel=1,hammer=1,striker=1,cut=4,amputate=25)
    _addRes(item, resrust=0)
    # mallets
def _mallet(item, striker):
    _bonusToArmor(item, 4)
    rog.make(item, TWOHANDS)
    rog.world().add_component(item, cmp.Tool_Striker(striker))
    rog.world().add_component(item, cmp.Tool_Hammer(1))
    _canThrow(item, acc=-5, rng=6, dmg=-2, pen=-8, skill=SKL_ENDOVEREND)
    _length(item, 90)
def _1mallet(item):
    _mallet(item, 1)
def _2mallet(item):
    _mallet(item, 2)
    # great clubs
def _heavyClub(item):
    _bonusToArmor(item, 2)
    rog.make(item, TWOHANDS)
    _canThrow(item, acc=-5, rng=5, dmg=-2, pen=-4, skill=SKL_ENDOVEREND)
    _length(item, 80)
    # misc 2-h weapons
def _daneAxe(item): # light-weight battleaxe
    _melee_bleed(item, 2*BLEED_STEEL)
    rog.make(item, TWOHANDS)
    rog.world().add_component(item, cmp.Tool_Hammer(2))
    rog.world().add_component(item, cmp.Tool_Chop(2))
    rog.world().add_component(item, cmp.Tool_Cut(3))
    _canThrow(item, acc=-5, rng=8, dmg=-2, pen=-8, skill=SKL_ENDOVEREND)
    _addRes(item, resrust=33)
    _length(item, 120)

    # tools that double as weapons #

# misc
def _scalpel(item):
    rog.world().add_component(item, cmp.Tool_Cut(6))
    rog.world().add_component(item, cmp.Tool_Scalpel(3))
    _bonusToFlesh(item, 4)
    _bleed(item, BLEED_GLASS)
    _length(item, 10)
# scissors
def _scissors(item, cut=7):
    rog.world().add_component(item, cmp.Tool_Cut(cut))
    rog.world().add_component(item, cmp.Tool_Chisel(1))
    _length(item, 10)
def _wireCutter(item):
    rog.world().add_component(item, cmp.Tool_Cut(8))
    _length(item, 10)
# screwdrivers
def _screwdriver(item, screwdriver=3, drill=1, hammer=1):
    rog.world().add_component(item, cmp.Tool_Screwdriver(screwdriver))
    if drill: rog.world().add_component(item, cmp.Tool_Drill(drill))
    if hammer: rog.world().add_component(item, cmp.Tool_Hammer(hammer))
    _length(item, 10)
# pliers
def _pliers(item, pliers=2, hammer=2, tongs=1):
    rog.world().add_component(item, cmp.Tool_Pliers(2))
    if hammer: rog.world().add_component(item, cmp.Tool_Hammer(2))
    if tongs: rog.world().add_component(item, cmp.Tool_Tongs(1))
    _length(item, 10)
def _needleNosePliers(item):
    rog.world().add_component(item, cmp.Tool_Cut(8))
    rog.world().add_component(item, cmp.Tool_Pliers(3))
    rog.world().add_component(item, cmp.Tool_Tongs(1))
    _length(item, 10)
# shovels
def _shovel(item, dig=3, cut=0, hammer=0, saw=0):
    rog.make(item, TWOHANDS)
    rog.world().add_component(item, cmp.Tool_Dig(dig))
    if cut: rog.world().add_component(item, cmp.Tool_Cut(cut))
    if saw: rog.world().add_component(item, cmp.Tool_Saw(saw))
    if hammer: rog.world().add_component(item, cmp.Tool_Hammer(hammer))
    _canThrow(item, acc=-4, rng=8, dmg=-4, pen=-4, skill=SKL_TIPFIRST)
    _length(item, 125)
def _mShovel(item):
    _shovel(item, dig=4, cut=1, hammer=1)
# pickaxes
def _pickaxe(item, pickaxe=1, hammer=1):
    _bonusToArmor(item, 4)
    rog.make(item, TWOHANDS)
    rog.world().add_component(item, cmp.Tool_Pickaxe(pickaxe))
    if hammer: rog.world().add_component(item, cmp.Tool_Hammer(hammer))
    _canThrow(item, acc=-10, rng=3, dmg=-6, pen=-8, skill=SKL_ENDOVEREND)
    _length(item, 70)
def _mPickaxe(item):
    _pickaxe(item, pickaxe=2, hammer=1)
    

    

    # ranged weapons #

    # cannons / caplock guns etc.
def _handCannon(item):
    rog.make(item, TWOHANDS)
    _canThrow(item, acc=-15, rng=3, dmg=-8, pen=-4)
    _weapon(item, acc=-5, dmg=12, pen=6, asp=-60)
    _length(item, 40)
def _arquebus(item): # heavy weapons must be mounted or set on a rest in order to shoot.
    rog.make(item, TWOHANDS)
    _weapon(item, acc=-15, dmg=15, pen=1, asp=-97)
    _length(item, 105)
def _blowGun(item):
    _canThrow(item, acc=0, rng=6)
    _length(item, 10)
def _caplockPistol(item):
    rog.world().add_component(item, cmp.Tool_Hammer(2))
    _canThrow(item, acc=-2, rng=8)
    _weapon(item, acc=1, dmg=8, pen=10, asp=-33)
    _addRes(item, resrust=0)
    _length(item, 30)
def _musketoon(item): # modable w/ bayonet: dmg +6, pen +6
    rog.make(item, TWOHANDS)
    rog.world().add_component(item, cmp.Tool_Hammer(1))
    _canThrow(item, acc=-6, rng=6, dmg=-2)
    _weapon(item, acc=1, dmg=10, pen=10, asp=-42)
    _addRes(item, resrust=0)
    _length(item, 60)
def _musket(item): # modable w/ bayonet: dmg +6, pen +6 (reach???)
    rog.make(item, TWOHANDS)
    rog.world().add_component(item, cmp.Tool_Hammer(1))
    _canThrow(item, acc=-10, rng=6, dmg=-4)
    _weapon(item, acc=1, dmg=12, pen=9, asp=-51)
    _addRes(item, resrust=0)
    _length(item, 90)

    # shotguns
def _pipegun(item):
    # pipe gun is a gun made of a pipe. It is two pipes of different sizes,
    # and one slides into the other. No trigger is necessary, just load
    # a shell/slug into the back end, and slam down the front piece while
    # aiming the barrel at the target.
    rog.make(item, TWOHANDS)
    _canThrow(item, acc=-15, rng=9, dmg=-2, pen=-2)
    _weapon(item, acc=0, dmg=8, pen=8, asp=-51)
    _length(item, 50)
    def disassemblefunc(item):
        pass # create & return two parts of the pipe gun
        # the stock/handle/firing pin piece; and the secondary handle/barrel piece.
    _disassemblable(item, disassemblefunc)
def _12GAshotgun(item):
    rog.make(item, TWOHANDS)
    rog.world().add_component(item, cmp.Tool_Hammer(1))
    _canThrow(item, acc=-12, rng=6, dmg=-4, pen=-4)
    _weapon(item, acc=1, dmg=10, pen=8, asp=-42)
    _length(item, 50)
def _10GAshotgun(item):
    rog.make(item, TWOHANDS)
    rog.world().add_component(item, cmp.Tool_Hammer(1))
    _canThrow(item, acc=-14, rng=4, dmg=-5, pen=-6)
    _weapon(item, acc=1, dmg=11, pen=7, asp=-54)
    _length(item, 55)
def _8GAshotgun(item):
    rog.make(item, TWOHANDS)
    _canThrow(item, acc=-16, rng=3, dmg=-6, pen=-8)
    _weapon(item, acc=1, dmg=12, pen=6, asp=-63)
    _length(item, 60)
def _6GAshotgun(item):
    rog.make(item, TWOHANDS)
    _canThrow(item, acc=-18, rng=2, dmg=-7, pen=-10)
    _weapon(item, acc=0, dmg=13, pen=4, asp=-72)
    _length(item, 65)
def _4GAshotgun(item):
    rog.make(item, TWOHANDS)
    _canThrow(item, acc=-20, rng=2, dmg=-8, pen=-12)
    _weapon(item, acc=-2, dmg=14, pen=3, asp=-81)
    _length(item, 70)
def _3GAshotgun(item):
    rog.make(item, TWOHANDS)
    _weapon(item, acc=-4, dmg=14, pen=2, asp=-87)
    _length(item, 75)
def _2GAshotgun(item):
    rog.make(item, TWOHANDS)
    _weapon(item, acc=-6, dmg=15, pen=1, asp=-94)
    _length(item, 80)
def _combatShotgun(item):
    rog.make(item, TWOHANDS)
    rog.world().add_component(item, cmp.Tool_Hammer(1))
    _canThrow(item, acc=-10, rng=6, dmg=-2, pen=-4)
    _weapon(item, acc=1, dmg=12, pen=9, asp=-30)
    _length(item, 40)

    # SMGs
def _smg(item):
    rog.world().add_component(item, cmp.Tool_Hammer(1))
    _canThrow(item, acc=0, rng=6)
    _weapon(item, acc=1, dmg=6, pen=6, asp=-45)
    _length(item, 30)
def _smgSmall(item):
    rog.world().add_component(item, cmp.Tool_Hammer(1))
    _canThrow(item, acc=0, rng=6)
    _weapon(item, acc=1, dmg=5, pen=6, asp=-24)
    _length(item, 20)
def _smgLarge(item):
    rog.make(item, TWOHANDS)
    rog.world().add_component(item, cmp.Tool_Hammer(1))
    _canThrow(item, acc=0, rng=5)
    _weapon(item, acc=1, dmg=8, pen=6, asp=-36)
    _length(item, 35)
def _pistolSmall(item):
    rog.world().add_component(item, cmp.Tool_Hammer(1))
    _canThrow(item, acc=0, rng=10, dmg=-1)
    _weapon(item, acc=1, dmg=5, pen=6, asp=-12)
    _length(item, 10)
def _pistol(item):
    rog.world().add_component(item, cmp.Tool_Hammer(1))
    _canThrow(item, acc=0, rng=12)
    _weapon(item, acc=2, dmg=7, pen=9, asp=-18)
    _length(item, 15)
def _pistolLarge(item):
    rog.world().add_component(item, cmp.Tool_Hammer(1))
    _canThrow(item, acc=0, rng=10, dmg=1)
    _weapon(item, acc=2, dmg=8, pen=11, asp=-24)
    _length(item, 20)
def _liberator(item, dmg=6, pen=6, rng=12):
    rog.world().add_component(item, cmp.Tool_Hammer(1))
    _canThrow(item, acc=0, rng=rng)
    _weapon(item, acc=2, dmg=dmg, pen=pen, asp=-9)
    _length(item, 10)
def _pLiberator(item):
    _liberator(item, dmg=2, pen=3, rng=12)
def _mLiberator(item):
    _liberator(item, dmg=4, pen=6, rng=12)
##def _revolver(item):
##    _canThrow(item, acc=0, rng=10)
##    _weapon(item, acc=1, dmg=5, pen=3, asp=-18)

    # Rifles
def _rifleSmall(item):
    rog.make(item, TWOHANDS)
    rog.world().add_component(item, cmp.Tool_Hammer(1))
    _canThrow(item, acc=-5, rng=6, dmg=-4, pen=-2)
    _weapon(item, acc=0, dmg=8, pen=6, asp=-42)
    _length(item, 50)
def _rifle(item, cm=70):
    rog.make(item, TWOHANDS)
    _canThrow(item, acc=-5, rng=4, dmg=-4, pen=-4)
    _weapon(item, acc=-1, dmg=10, pen=8, asp=-51)
    _length(item, cm)
def _rifleLarge(item):
    rog.make(item, TWOHANDS)
    _canThrow(item, acc=-5, rng=4, dmg=-4, pen=-6)
    _weapon(item, acc=-2, dmg=12, pen=10, asp=-60)
    _length(item, 90)
def _rifleXLarge(item):
    rog.make(item, TWOHANDS)
    _weapon(item, acc=-4, dmg=14, pen=12, asp=-75)
    _length(item, 120)
def _rifle308(item):
    _rifle(item)
def _rifle3006(item):
    _rifle(item)
    compo=rog.world().component_for_entity(item, cmp.Shootable)
    compo.ammoTypes.add(AMMO_308)
def _autocarb(item):
    _rifleSmall(item)
    
    # slings
def _sling(item):
    _length(item, 110)
    _canThrow(item, acc=2, rng=3, dmg=-2, pen=-6)
    
    # bows
def _pBow(item):
    rog.make(item, TWOHANDS)
    _weapon(item, acc=-4,dmg=0,pen=0,asp=-21)
    _canThrow(item, acc=-4, rng=3, pen=-1)
    _length(item, 100)
def _smallBow(item):
    rog.make(item, TWOHANDS)
    _weapon(item, acc=-3,dmg=1,pen=0,asp=-21)
    _canThrow(item, acc=-2, rng=6, pen=-1)
    _length(item, 100)
def _wBow(item):
    rog.make(item, TWOHANDS)
    _weapon(item, acc=-2,dmg=1,pen=0,asp=-33)
    _canThrow(item, acc=-2, rng=4, pen=-1)
    _length(item, 100)
def _compositeBow(item):
    rog.make(item, TWOHANDS)
    _weapon(item, acc=-2,dmg=1,pen=0,asp=-33)
    _canThrow(item, acc=-2, rng=4, pen=-1)
    _length(item, 100)
    rog.world().component_for_entity(item, cmp.Stats).reswet -= 20 # composite bow is weaker to water than regular wooden bows
def _longbow(item):
    rog.make(item, TWOHANDS)
    _weapon(item, acc=-4,dmg=2,pen=0,asp=-45)
    _canThrow(item, acc=-4, rng=3, pen=-2)
    _length(item, 200)

    # crossbows
def _crossbow(item):
    rog.make(item, TWOHANDS)
    _weapon(item, acc=0,dmg=2,pen=1,asp=-36)
    _canThrow(item, acc=-4, rng=3, pen=-3)
    _length(item, 30)
def _arbalest(item):
    rog.make(item, TWOHANDS)
    _weapon(item, acc=-4,dmg=3,pen=3,asp=-75)
    _length(item, 50)

    # energy weapons
def _laserGun(item):
    _canThrow(item, acc=-2, rng=6, dmg=0)
    _weapon(item, acc=0, dmg=4, pen=6, asp=-45)
    _elementalRanged(item, ELEM_LIGHT, 400)
    _length(item, 20)
def _laserRifle(item):
    _canThrow(item, acc=-6, rng=3, dmg=-2)
    _weapon(item, acc=-2, dmg=6, pen=7, asp=-72)
    _elementalRanged(item, ELEM_LIGHT, 800)
    _length(item, 30)
def _maserGun(item): # heat ray
    _canThrow(item, acc=-2, rng=6, dmg=0)
    _weapon(item, acc=0, dmg=4, pen=6, asp=-45)
    _elementalRanged(item, ELEM_FIRE, 50)
    _length(item, 20)
def _cryoGun(item): # cold ray
    _canThrow(item, acc=-2, rng=6, dmg=0)
    _weapon(item, acc=0, dmg=4, pen=6, asp=-45)
    _elementalRanged(item, ELEM_COLD, 50)
    _length(item, 20)

    # LMGs
def _lmg(item):
    rog.make(item, TWOHANDS)
    _weapon(item, acc=-6, dmg=16, pen=9, asp=-75)
    _length(item, 100)

    # misc ranged
def _atlatl(item):
    rog.world().add_component(item, cmp.Tool_Hammer(2))
    _weapon(item, acc=2,dmg=1,pen=1,asp=-12)
    _canThrow(item, acc=0, rng=10, skill=SKL_ENDOVEREND)
    _length(item, 60)



    # headwear #
def _pCap(item):
    _canThrow(item, acc=0, rng=5, dmg=1, skill=SKL_SPINNING)
def _fCap(item):
    _canThrow(item, acc=0, rng=5, skill=SKL_SPINNING)
def _bCap(item):
    _canThrow(item, acc=0, rng=5, dmg=2, skill=SKL_SPINNING)
def _kCap(item):
    _canThrow(item, acc=0, rng=8, dmg=2, skill=SKL_SPINNING)
def _lCap(item):
    _canThrow(item, acc=0, rng=8, dmg=1, skill=SKL_SPINNING)
def _mCap(item):
    rog.world().add_component(item, cmp.Tool_Hammer(1))
    _canThrow(item, acc=0, rng=8, dmg=3, skill=SKL_SPINNING)
def _cCoif(item):
    _canThrow(item, acc=0, rng=3, skill=SKL_SPINNING)
def _mCoif(item):
    _canThrow(item, acc=0, rng=3, skill=SKL_SPINNING)
def _pHelm(item):
    _canThrow(item, acc=0, rng=5, skill=SKL_SPINNING)
def _bHelm(item):
    _canThrow(item, acc=0, rng=5, dmg=1, skill=SKL_SPINNING)
def _mHelm(item):
    rog.world().add_component(item, cmp.Tool_Hammer(1))
    _canThrow(item, acc=0, rng=6, dmg=1, skill=SKL_SPINNING)
def _grHelm(item): # graphene
    _canThrow(item, acc=0, rng=10, dmg=1, skill=SKL_SPINNING)
def _motorcycleHelm(item):
    _canThrow(item, acc=0, rng=8, skill=SKL_SPINNING)
def _mFullHelm(item):
    rog.world().add_component(item, cmp.Tool_Hammer(1))
    _canThrow(item, acc=0, rng=4, dmg=1, skill=SKL_SPINNING)
def _bioHelm(item):
    _canThrow(item, acc=0, rng=3, skill=SKL_SPINNING)
def _mBioHelm(item):
    rog.world().add_component(item, cmp.Tool_Hammer(1))
    _canThrow(item, acc=0, rng=3, dmg=1, skill=SKL_SPINNING)
    # face gear
def _bandana(item):
    pass
def _pMask(item):
    _canThrow(item, acc=0, rng=6, skill=SKL_SPINNING)
def _wMask(item):
    _canThrow(item, acc=0, rng=8, skill=SKL_SPINNING)
def _fMask(item):
    _canThrow(item, acc=0, rng=4, skill=SKL_SPINNING)
def _lMask(item):
    _canThrow(item, acc=0, rng=7, skill=SKL_SPINNING)
def _blMask(item):
    _canThrow(item, acc=0, rng=7, skill=SKL_SPINNING)
def _mMask(item):
    rog.world().add_component(item, cmp.Tool_Hammer(1))
    _canThrow(item, acc=0, rng=12, skill=SKL_SPINNING)
def _kMask(item):
    _canThrow(item, acc=0, rng=10, skill=SKL_SPINNING)
def _mRespirator(item):
    _canThrow(item, acc=0, rng=6, skill=SKL_SPINNING)
def _respirator(item):
    _canThrow(item, acc=0, rng=6, skill=SKL_SPINNING)
def _gasMask(item):
    _canThrow(item, acc=0, rng=4, skill=SKL_SPINNING)
def _plagueMask(item):
    _canThrow(item, acc=-5, rng=5, skill=SKL_THROWING)
    # eye gear
def _pGoggles(item):
    _canThrow(item, acc=0, rng=5, skill=SKL_SPINNING)
def _gGoggles(item):
    _canThrow(item, acc=0, rng=5, skill=SKL_SPINNING)
def _glasses(item):
    _canThrow(item, acc=0, rng=4, skill=SKL_SPINNING)

# leg armor
##def _pjs(item):
##    _coversBothLegs(item)


'''
    modification / transformation functions
'''

##def _trans_rust(item): 
### instead of a transform function, rust should just create a whole
### new object with the same name + rusted as a prefix, and it has
### no tool quality or equip ability / etc. ...
##    
##    rog.world().add_component(item, cmp.Rusted)
##    form=rog.world().component_for_entity(item, cmp.Form)
##    form.material=MAT_RUST
##    return True
def _apply_grease(item):
    rog.world().add_component(item, cmp.Greased())



    #------------------#
    # elemental damage #
    #------------------#


# METER-STATUSES ARE ALL REMOVED AT START OF UPDATE_STATS,
# AND ARE APPLIED DEPENDING ON WHAT LEVEL OF METERS YOU HAVE IN
# EACH ELEMENT...
# No need to check meters in a processor every turn or any shit like that
# Also, No need to set status in the following elemental damage functions.
# Note, This makes a distinction btn meters-statuses and statuses that are
#   not removed except in specific conditions.
#TODO:
#   **put set and remove status logic in _update_stats for most meter statuses
#     for those statuses, make the timer == -1 so they never expire.**
#   NEVER change meters directly -- change them through these functions
#   which will properly apply the DIRTYSTATS flag to the entity in question
#TODO: bleed works differently too: amount of bleeding and time
#  depends on how high the meter is.
# Actually, with this new system, we could easily have pretty much all
#  of the meters work in this kind of graduated way.
#NOT ALL STATUSES ARE HANDLED THIS WAY THOUGH::
#  Some statuses still work the old way, like those related to BIO res,
#    which all share the same resistance despite causing different effects.
#  This means for BIO, _update_stats does not care about BIO meter.
#  The BIO statuses remove themselves after the duration expires.


# TODO: ADD NEW ELEMENTAL TYPE FUNCTIONS!

#   TEMP METER
def burn(ent, amt, maxTemp):
    assert(amt > 0)
    res = max(-99, rog.getms(ent, 'resfire'))
    # TODO: wet resistance to fire. Put this logic in _update_stats
    # TODO: heat while wet reduces wetness, may create steam
##    if rog.on(obj, WET):    
##        rog.clear_status(obj,WET)    #wet things get dried
##        #steam=stuff.create("steam", obj.x, obj.y)
    dmg = amt*100/(res+100)
    meters = rog.world().component_for_entity(ent, cmp.Meters)
    if meters.temp < MAX_TEMP:
        meters.temp = min(MAX_TEMP, meters.temp + dmg)
        rog.make(ent, DIRTYSTATS)
    return dmg
def cool(ent, amt, minTemp):
    assert(amt > 0)
    res = max(-99, rog.getms(ent, 'rescold'))
    # TODO: wet resistance to cold. Put this logic in _update_stats
    dmg = amt*100/(res+100)
    meters = rog.world().component_for_entity(ent, cmp.Meters)
    if meters.temp > MIN_TEMP:
        meters.temp = max(MIN_TEMP, meters.temp - dmg)
        rog.make(ent, DIRTYSTATS)
    return dmg
##def normalizeTemperature(ent, roomTemp=0): # normalize to room temp
#TODO: fix to use cooldown and warmup (also make warmup func)
##    meters = rog.world().component_for_entity(ent, cmp.Meters)
##    meters.temp = meters.temp + rog.sign(roomTemp - meters.temp)
##    rog.make(ent, DIRTYSTATS)
##def cooldown(ent, amt, minTemp=0): # cool down to given temp e.g. room temp
##    assert(val > 0)
##    meters = rog.world().component_for_entity(ent, cmp.Meters)
##    if meters.temp > minTemp:
##        meters.temp = max(minTemp, meters.temp - val)
##        rog.make(ent, DIRTYSTATS)
    
#   PAIN METER
def hurt(ent, amt):
    assert(amt > 0)
    if rog.on(ent, IMMUNEPAIN): return 0
    res = max(-99, rog.getms(ent, 'respain'))
    dmg = amt*100/(res+100)
    meters = rog.world().component_for_entity(ent, cmp.Meters)
    if meters.pain < MAX_PAIN:
        meters.pain = min(MAX_PAIN, meters.pain + dmg)
        rog.make(ent, DIRTYSTATS)
    return dmg
def healhurt(ent, val):
    if rog.on(ent, IMMUNEPAIN): return
    assert(val > 0)
    meters = rog.world().component_for_entity(ent, cmp.Meters)
    if meters.pain > 0:
        meters.pain = max(0, meters.pain - val)
        rog.make(ent, DIRTYSTATS)

#   BLEED METER
def bleed(ent, amt):
    assert(amt > 0)
    if rog.on(ent, IMMUNEBLEED): return 0
    res = max(-99, rog.getms(ent, 'resbleed'))
    dmg = amt*100/(res+100)
    meters = rog.world().component_for_entity(ent, cmp.Meters)
    if meters.bleed < MAX_BLEED:
        meters.bleed = min(MAX_BLEED, meters.bleed + dmg)
        rog.make(ent, DIRTYSTATS)
    return dmg
def healbleed(ent, val):
    assert(val > 0)
    if rog.on(ent, IMMUNEBLEED): return
    meters = rog.world().component_for_entity(ent, cmp.Meters)
    if meters.bleed > 0:
        meters.bleed = max(0, meters.bleed - val)
        rog.make(ent, DIRTYSTATS)
        
#   SICK METER 
def disease(ent, amt):
    assert(amt > 0)
    if rog.on(ent, IMMUNEBIO): return 0
    res = max(-99, rog.getms(ent, 'resbio'))
    dmg = amt*100/(res+100)
    meters = rog.world().component_for_entity(ent, cmp.Meters)
    meters.sick += max(0, dmg )
    if meters.sick >= MAX_SICK:
        meters.sick = 0
        rog.set_status(ent, cmp.StatusSick)
        rog.make(ent, DIRTYSTATS)
    return dmg
def intoxicate(ent, amt):
    assert(amt > 0)
    if rog.on(ent, IMMUNEBIO): return 0
    res = max(-99, rog.getms(ent, 'resbio'))
    dmg = amt*100/(res+100)
    meters = rog.world().component_for_entity(ent, cmp.Meters)
    meters.sick += max(0, dmg )
    if meters.sick >= MAX_SICK:
        meters.sick = 0
        rog.set_status(ent, cmp.StatusDrunk)
        rog.make(ent, DIRTYSTATS)
    return dmg
def healsick(ent, val):
    assert(val > 0)
    if rog.on(ent, IMMUNEBIO): return
    meters = rog.world().component_for_entity(ent, cmp.Meters)
    if meters.sick > 0:
        meters.sick = max(0, meters.sick - val)
        rog.make(ent, DIRTYSTATS) # this is probably unnecessary since BIO statuses just run out of time. When they do run out of time though, DIRTYSTATS needs to be set!!
        
#   RADS METER
def irradiate(ent, amt):
    assert(amt > 0)
    if rog.on(ent, IMMUNEBIO): return 0
    res = max(-99, rog.getms(ent, 'resbio'))
    dmg = amt*100/(res+100)
    meters = rog.world().component_for_entity(ent, cmp.Meters)
    meters.rads += max(0, dmg )
    if meters.rads >= MAX_RADS:
        meters.rads = 0 # reset rads meter after mutation
        rog.mutate(ent)
        rog.make(ent, DIRTYSTATS)
    return dmg
def healrads(ent, val):
    assert(val > 0)
    if rog.on(ent, IMMUNEBIO): return
    meters = rog.world().component_for_entity(ent, cmp.Meters)
    if meters.rads > 0:
        meters.rads = max(0, meters.rads - val)
        rog.make(ent, DIRTYSTATS)
        
#   EXPOSURE METER
def exposure(ent, amt):
    assert(amt > 0)
    if rog.on(ent, IMMUNEBIO): return 0
    res = max(-99, rog.getms(ent, 'resbio'))
    #increase exposure meter
    dmg = amt*100/(res+100)
    meters = rog.world().component_for_entity(ent, cmp.Meters)
    meters.expo += max(0, dmg )
    if meters.expo >= MAX_EXPO:
        meters.expo = MAX_EXPO//2 #leave half exposure
        rog.damage(ent, CHEM_DAMAGE)  #instant damage when expo meter fills
        hurt(ent, CHEM_HURT)
        _random_chemical_effect(ent) #inflict chem status effect
        rog.make(ent, DIRTYSTATS)
    return dmg
def corrode(ent, amt): # acid
    assert(amt > 0)
    if rog.on(ent, IMMUNEBIO): return 0
    res = max(-99, rog.getms(ent, 'resbio'))
    dmg = amt*100/(res+100)
    meters = rog.world().component_for_entity(ent, cmp.Meters)
    meters.expo += max(0, dmg)
    if meters.expo >= MAX_EXPO:
        meters.expo = MAX_EXPO//2 #leave half exposure
        rog.set_status(ent, cmp.StatusAcid)
        rog.make(ent, DIRTYSTATS)
    return dmg
def cough(ent, amt): # throat irritation
    assert(amt > 0)
    if rog.on(ent, IMMUNEBIO): return 0
    res = max(-99, rog.getms(ent, 'resbio'))
    dmg = amt*100/(res+100)
    meters = rog.world().component_for_entity(ent, cmp.Meters)
    meters.expo += max(0, dmg)
    if meters.expo >= MAX_EXPO:
        meters.expo = MAX_EXPO//2 #leave half exposure
        rog.set_status(ent, cmp.StatusCough)
        rog.make(ent, DIRTYSTATS)
    return dmg
def vomit(ent, amt): # nausea
    assert(amt > 0)
    if rog.on(ent, IMMUNEBIO): return 0
    res = max(-99, rog.getms(ent, 'resbio'))
    dmg = amt*100/(res+100)
    meters = rog.world().component_for_entity(ent, cmp.Meters)
    meters.expo += max(0, dmg)
    if meters.expo >= MAX_EXPO:
        meters.expo = MAX_EXPO//2 #leave half exposure
        rog.set_status(ent, cmp.StatusVomit)
        rog.make(ent, DIRTYSTATS)
    return dmg
def irritate(ent, amt):
    assert(amt > 0)
    if rog.on(ent, IMMUNEBIO): return 0
    res = max(-99, rog.getms(ent, 'resbio'))
    dmg = amt*100/(res+100)
    meters = rog.world().component_for_entity(ent, cmp.Meters)
    meters.expo += max(0, dmg)
    if meters.expo >= MAX_EXPO:
        meters.expo = MAX_EXPO//2 #leave half exposure
        rog.set_status(ent, cmp.StatusIrritated)
        rog.make(ent, DIRTYSTATS)
    return dmg
def healexpo(ent, val):
    assert(val > 0)
    if rog.on(ent, IMMUNEBIO): return
    meters = rog.world().component_for_entity(ent, cmp.Meters)
    if meters.expo > 0:
        meters.expo = max(0, meters.expo - val)
        rog.make(ent, DIRTYSTATS)
        
#   WETNESS METER
def wet(ent, amt):
    assert(amt > 0)
    if rog.on(ent, IMMUNEWET): return 0
    world=rog.world()
    res = max(-99, rog.getms(ent, 'reswet'))
    dmg = amt*100/(res+100)
    meters = world.component_for_entity(ent, cmp.Meters)
    mat = world.component_for_entity(ent, cmp.Form).material
##    if world.has_component(ent, cmp.WetnessCapacity): ... # else get from material.
    max_wet = rog.getms(ent,'mass')/MULT_MASS * WETNESS_MAX_MATERIAL[mat]
    if meters.wet < max_wet:
        slough = amt + meters.wet - max_wet
        meters.wet = min(max_wet, meters.wet + dmg)
        rog.make(ent, DIRTYSTATS)
    if slough > 0: # IDEA: slough off excess water (how to do this intelligently without causing infinite recursion etc.?)
        rog.globalreturn(slough)
    # apply rust -- should this be in this function?
    return dmg
def healwet(ent, val):
    assert(val > 0)
    if rog.on(ent, IMMUNEWET): return
    meters = rog.world().component_for_entity(ent, cmp.Meters)
    if meters.wet > 0:
        meters.wet = max(0, meters.wet - val)
        rog.make(ent, DIRTYSTATS)
        
#   DIRTINESS METER
def dirty(ent, amt):
    assert(amt > 0)
    if rog.on(ent, IMMUNEWET): return 0
    res = max(-99, rog.getms(ent, 'reswet'))
    dmg = amt*100/(res+100)
    meters = rog.world().component_for_entity(ent, cmp.Meters)
    if meters.dirt < MAX_DIRT: # IDEA: slough off excess dirt
        meters.dirt = min(MAX_DIRT, meters.dirt + dmg)
        rog.make(ent, DIRTYSTATS)
    return dmg
def healdirt(ent, val):
    assert(val > 0)
    if rog.on(ent, IMMUNEWET): return
    meters = rog.world().component_for_entity(ent, cmp.Meters)
    if meters.dirt > 0:
        meters.dirt = max(0, meters.dirt - val)
        rog.make(ent, DIRTYSTATS)
        
#   RUST METER
def rust(ent, amt):
    assert(amt > 0)
    if rog.on(ent, IMMUNERUST): return 0
    res = max(-99, rog.getms(ent, 'resrust'))
    dmg = amt*100/(res+100)
    meters = rog.world().component_for_entity(ent, cmp.Meters)
    if meters.rust < MAX_RUST:
        meters.rust = min(MAX_RUST, meters.rust + dmg)
        rog.make(ent, DIRTYSTATS)
    return dmg
def healrust(ent, val):
    assert(val > 0)
    if rog.on(ent, IMMUNERUST): return
    meters = rog.world().component_for_entity(ent, cmp.Meters)
    if meters.rust > 0:
        meters.rust = max(0, meters.rust - val)
        rog.make(ent, DIRTYSTATS)
        
#   ROT METER
def rot(ent, amt):
    assert(amt > 0)
    if rog.on(ent, IMMUNEROT): return 0
    res = max(-99, rog.getms(ent, 'resrot'))
    dmg = amt*100/(res+100)
    meters = rog.world().component_for_entity(ent, cmp.Meters)
    if meters.rot < MAX_ROT:
        meters.rot = min(MAX_ROT, meters.rot + dmg)
        rog.make(ent, DIRTYSTATS)
    return dmg
def healrot(ent, val):
    assert(val > 0)
    if rog.on(ent, IMMUNERUST): return
    meters = rog.world().component_for_entity(ent, cmp.Meters)
    if meters.rot > 0:
        meters.rot = max(0, meters.rot - val)
        rog.make(ent, DIRTYSTATS)
        
        
#   NON-METER ELEMENTAL DAMAGE #

# elemental -> physical damage
def electrify(ent, amt):
    assert(amt > 0)
    res = max(-99, rog.getms(ent, 'reselec'))
    dmg = amt*100/(res+100) * 0.1 * MULT_STATS
    if dmg:
        rog.damage(ent, dmg)
        rog.sap(ent, dmg)
    if dmg >= (rog.getms(ent, 'hpmax')//3):
        paralyze(ent, 3) # paralysis from high damage
    rog.make(ent, DIRTYSTATS)
    return dmg
# 
def mutate(ent):
    if not rog.world().has_component(ent, cmp.Mutable):
        return False
    mutable = rog.world().component_for_entity(ent, cmp.Mutable)
    mutable.mutations += 1
    if mutable.mutations > 3:
        rog.kill(ent)
    return True
def paralyze(ent, dur):
    if not rog.world().has_component(ent, cmp.Creature):
        return False
    rog.set_status(ent, cmp.StatusParalyzed, dur)
    return True


    #-----------------------#
    #       # Stats #       #      #Stats#
    #-----------------------#

def rollstats(stats, DEV=3, HDEV=6, MDEV=0.05):
    stats.str+=int(MULT_STATS*(random.random()*DEV*2-DEV))
    stats.con+=int(MULT_STATS*(random.random()*DEV*2-DEV))
    stats.int+=int(MULT_STATS*(random.random()*DEV*2-DEV))
    stats.dex+=int(MULT_STATS*(random.random()*DEV*2-DEV))
    stats.agi+=int(MULT_STATS*(random.random()*DEV*2-DEV))
    stats.end+=int(MULT_STATS*(random.random()*DEV*2-DEV))
    stats.mass=int(stats.mass*(1 + random.random()*MDEV*2 - MDEV))
    stats.cm+=int(random.random()*HDEV*2-HDEV)

# ADD DICT MULTIPLIER FUNCTIONS (dadd)

# fitted bonus
def fittedBonus(world,ent,item,eqdadd):
    if ( world.has_component(item, cmp.Fitted)
         and ent==world.component_for_entity(item, cmp.Fitted).entity ):
        _apply_fittedBonus(eqdadd)
# armor skill bonus
def armor_skillBonus(world,item,eqdadd,armorSkill,unarmored,cov):
    if not world.has_component(item, cmp.Clothes):
        _apply_skillBonus_armor(eqdadd, armorSkill, cov)
    else: # unarmored combat skill used for "clothing" armor
        _apply_skillBonus_unarmored(eqdadd, unarmored, cov)
# get eqdadd (equip stat add mod dictionary)
def get_addmods(world,item,equipable):
    eqdadd={}
    for k,v in equipable.mods.items(): # collect add modifiers
        eqdadd.update({k:v})
    _getenc(eqdadd, item)
    return eqdadd

# apply any/all penalties necessary to gear
def apply_penalties_armor(eqdadd, item):
    _apply_durabilityPenalty_armor(eqdadd, item)
    _apply_rustPenalty_armor(eqdadd, item)
    _apply_rotPenalty_armor(eqdadd, item)
# apply any/all penalties necessary to weapon
def apply_penalties_weapon(eqdadd, item):
    _apply_durabilityPenalty_weapon(eqdadd, item)
    _apply_rustPenalty_weapon(eqdadd, item)
    _apply_rotPenalty_weapon(eqdadd, item)

#
def _add(dadd, modDict):
    for stat,val in modDict.items():
        if stat in MULTSTATS:
            val = val * MULT_STATS
        dadd[stat] = dadd.get(stat, 0) + val
def _mult(dmul, modDict):
    for stat,val in modDict.items():
        dmul[stat] = dmul.get(stat, 1) * val
def _apply_fittedBonus(dadd):
    dadd['enc']=dadd['enc']*FITTED_ENCMOD
def _getenc(dadd, item): # get Encumberance stat modifier from Encumberance component
    dadd['enc']=dadd.get('enc',0)+rog.getms(item,'mass')/MULT_MASS*rog.world().component_for_entity(
        item, cmp.Encumberance).value
def _apply_durabilityPenalty_weapon(dadd, item):
    hp = rog.getms(item, 'hp')
    hpMax = rog.getms(item, 'hpmax')
    modi = ( 1 - (hp / max(1,hpMax)) )**2
    modf = 1 - modi
    _2575 = (0.25 + 0.75*modf)
    _5050 = (0.5 + 0.5*modf)
    dadd['asp'] = dadd.get('asp',0) + DURMOD_ASP*modi
    dadd['atk'] = min( dadd.get('atk',0), dadd.get('atk',0) * _5050 )
    dadd['dmg'] = min( dadd.get('dmg',0), dadd.get('dmg',0) * _2575 )
    dadd['pen'] = min( dadd.get('pen',0), dadd.get('pen',0) * modf )
    dadd['pro'] = min( dadd.get('pro',0), dadd.get('pro',0) * modf )
    dadd['arm'] = min( dadd.get('arm',0), dadd.get('arm',0) * _2575 )
    dadd['dfn'] = min( dadd.get('dfn',0), dadd.get('dfn',0) * _5050 )
    dadd['ctr'] = min( dadd.get('ctr',0), dadd.get('ctr',0) * _5050 )
# end def
def _apply_rustPenalty_weapon(dadd, item): # TODO: test
    world=rog.world()
    if world.has_component(item, cmp.StatusRusted):
        rust = world.component_for_entity(item, cmp.StatusRusted).quality
        # get stat modifier for the quality of rustedness present
        modf = RUSTEDNESS[RUST_QUALITITES[rust]][0]
    else:
        modf = 1
    dadd['atk'] = min( dadd.get('atk',0), dadd.get('atk',0) * modf )
    dadd['dmg'] = min( dadd.get('dmg',0), dadd.get('dmg',0) * modf )
    dadd['pen'] = min( dadd.get('pen',0), dadd.get('pen',0) * modf )
    dadd['pro'] = min( dadd.get('pro',0), dadd.get('pro',0) * modf )
    dadd['arm'] = min( dadd.get('arm',0), dadd.get('arm',0) * modf )
    dadd['dfn'] = min( dadd.get('dfn',0), dadd.get('dfn',0) * modf )
    dadd['ctr'] = min( dadd.get('ctr',0), dadd.get('ctr',0) * modf )
# end def
def _apply_rotPenalty_weapon(dadd, item): # TODO: test
    world=rog.world()
    if world.has_component(item, cmp.StatusRotted):
        rust = world.component_for_entity(item, cmp.StatusRotted).quality
        # get stat modifier for the quality of rustedness present
        modf = ROTTEDNESS[ROT_QUALITITES[rust]][0]
    else:
        modf = 1
    dadd['atk'] = min( dadd.get('atk',0), dadd.get('atk',0) * modf )
    dadd['dmg'] = min( dadd.get('dmg',0), dadd.get('dmg',0) * modf )
    dadd['pen'] = min( dadd.get('pen',0), dadd.get('pen',0) * modf )
    dadd['pro'] = min( dadd.get('pro',0), dadd.get('pro',0) * modf )
    dadd['arm'] = min( dadd.get('arm',0), dadd.get('arm',0) * modf )
    dadd['dfn'] = min( dadd.get('dfn',0), dadd.get('dfn',0) * modf )
    dadd['ctr'] = min( dadd.get('ctr',0), dadd.get('ctr',0) * modf )
# end def
def _apply_skillBonus_weapon(dadd, skillLv, skill, enc=True):
    if skillLv <=0: return
    skillLv = min(skillLv, SKILL_MAXIMUM)
    sm = skillLv * SKILL_EFFECTIVENESS_MULTIPLIER
    # skill bonus can cut encumberance of gear item up to half. Only works up to max skill level.
    if enc: # only for weapons with encumberance values (not for unarmed combat)
        dadd['enc']=dadd['enc'] * (
            SKILL_MAXIMUM / (SKILL_MAXIMUM + skillLv*DEFAULT_SKLMOD_ENC) )
    # custom or default stat modifiers for specific skills
    dadd['atk']=dadd.get('atk',0) + MULT_STATS * sm * SKLMOD_ATK.get(skill,DEFAULT_SKLMOD_ATK)
    dadd['pen']=dadd.get('pen',0) + MULT_STATS * sm * SKLMOD_PEN.get(skill,DEFAULT_SKLMOD_PEN)
    dadd['dmg']=dadd.get('dmg',0) + MULT_STATS * sm * SKLMOD_DMG.get(skill,DEFAULT_SKLMOD_DMG)
    dadd['dfn']=dadd.get('dfn',0) + MULT_STATS * sm * SKLMOD_DFN.get(skill,DEFAULT_SKLMOD_DFN)
    dadd['pro']=dadd.get('pro',0) + MULT_STATS * sm * SKLMOD_PRO.get(skill,DEFAULT_SKLMOD_PRO)
    dadd['arm']=dadd.get('arm',0) + MULT_STATS * sm * SKLMOD_ARM.get(skill,DEFAULT_SKLMOD_ARM)
    dadd['asp']=dadd.get('asp',0) + sm * SKLMOD_ASP.get(skill,DEFAULT_SKLMOD_ASP)
    dadd['gra']=dadd.get('gra',0) + MULT_STATS * sm * SKLMOD_GRA.get(skill,DEFAULT_SKLMOD_GRA)
    dadd['ctr']=dadd.get('ctr',0) + MULT_STATS * sm * SKLMOD_CTR.get(skill,DEFAULT_SKLMOD_CTR)
# end def
def _apply_durabilityPenalty_armor(dadd, item):
    hp = rog.getms(item, 'hp')
    hpMax = rog.getms(item, 'hpmax')
    modf = 1 - ( 1 - (hp / max(1,hpMax)) )**2
    _2575 = (0.25 + 0.75*modf)
    _5050 = (0.5 + 0.5*modf)
    dadd['pro'] = min(dadd.get('pro',0), dadd.get('pro',0) * modf)
    dadd['arm'] = min(dadd.get('arm',0), dadd.get('arm',0) * _2575)
    dadd['dfn'] = min(dadd.get('dfn',0), dadd.get('dfn',0) * _5050)
# end def
def _apply_rustPenalty_armor(dadd, item): # TODO: test
    world=rog.world()
    if world.has_component(item, cmp.StatusRusted):
        rust = world.component_for_entity(item, cmp.StatusRusted).quality
        # get stat modifier for the quality of rustedness present
        modf = RUSTEDNESS[RUST_QUALITITES[rust]][0]
    else:
        modf = 1
    dadd['pro'] = min(dadd.get('pro',0), dadd.get('pro',0) * modf)
    dadd['arm'] = min(dadd.get('arm',0), dadd.get('arm',0) * modf)
    dadd['dfn'] = min(dadd.get('dfn',0), dadd.get('dfn',0) * modf)
# end def
def _apply_rotPenalty_armor(dadd, item): # TODO: test
    world=rog.world()
    if world.has_component(item, cmp.StatusRotted):
        rust = world.component_for_entity(item, cmp.StatusRotted).quality
        # get stat modifier for the quality of rustedness present
        modf = ROTTEDNESS[ROT_QUALITITES[rust]][0]
    else:
        modf = 1
    dadd['pro'] = min(dadd.get('pro',0), dadd.get('pro',0) * modf)
    dadd['arm'] = min(dadd.get('arm',0), dadd.get('arm',0) * modf)
    dadd['dfn'] = min(dadd.get('dfn',0), dadd.get('dfn',0) * modf)
# end def
def _apply_skillBonus_armor(dadd, skillLv, coverage_modf):
    if skillLv <=0: return
    sm = skillLv * SKILL_EFFECTIVENESS_MULTIPLIER * coverage_modf
    # skill bonus can cut encumberance of gear item up to half. 
    dadd['enc']=dadd['enc'] * (
        SKILL_MAXIMUM / (SKILL_MAXIMUM + skillLv*DEFAULT_SKLMOD_ENC) )
    dadd['pro']=dadd.get('pro',0) + MULT_STATS*SKLMOD_ARMOR_PRO*sm
    dadd['arm']=dadd.get('arm',0) + MULT_STATS*SKLMOD_ARMOR_AV*sm
    dadd['dfn']=dadd.get('dfn',0) + MULT_STATS*SKLMOD_ARMOR_DV*sm
# end def
def _apply_skillBonus_unarmored(dadd, skillLv, coverage_modf):
    if skillLv <=0: return
    sm = skillLv * SKILL_EFFECTIVENESS_MULTIPLIER * coverage_modf
    dadd['pro']=dadd.get('pro',0) + MULT_STATS*SKLMOD_UNARMORED_PRO*sm
    dadd['arm']=dadd.get('arm',0) + MULT_STATS*SKLMOD_UNARMORED_AV*sm
    dadd['dfn']=dadd.get('dfn',0) + MULT_STATS*SKLMOD_UNARMORED_DV*sm
# end def
##def _apply_mass(ent, item, dadd, equipable):
##    mass=rog.getms(item, 'mass')
##    dadd['mass'] = dadd.get('mass', 0) + mass
##    dadd['enc'] = dadd.get('enc', 0) + equipable.enc*mass/MULT_MASS
# end def

'''
    Body and Equipment
'''

class __EQ:
    def __init__(self, enc, strReq, dexReq, addMods, multMods, bptype=None):
        self.enc=enc
        self.strReq=strReq
        self.dexReq=dexReq
        self.addMods=addMods
        self.multMods=multMods
        self.bptype=bptype
class __BPS: # Body Part Stats
    def __init__(self, addMods, multMods, equip=None):
        self.addMods=addMods
        self.multMods=multMods
        self.equip=equip
    
# BPC

def _update_from_body_class(body, modded):
    bodymass=0
    bodymass += body.blood
    bodymass += body.hydration//MULT_HYD
    bodymass += body.bodyfat
    modded.mass += bodymass
    modded.height += body.height
    modded.rescold += body.bodyfat / MULT_MASS * FAT_RESCOLD
    modded.resfire += body.bodyfat / MULT_MASS * FAT_RESHEAT
    return bodymass

def _update_from_bpc_heads(lis, ent, bpc, armorSkill, unarmored):
    for bpm in bpc.heads: # for each head you possess,
        # head
        bps=_update_from_bp_head(ent, bpm.head, armorSkill, unarmored)
        lis.append(bps)
        # neck
        bps=_update_from_bp_neck(ent, bpm.neck, armorSkill, unarmored)
        lis.append(bps)
        # face
        bps=_update_from_bp_face(ent, bpm.face, armorSkill, unarmored)
        lis.append(bps)
        # eyes
        bps=_update_from_bp_eyes(ent, bpm.eyes, armorSkill, unarmored)
        lis.append(bps)
        # ears
        bps=_update_from_bp_ears(ent, bpm.ears, armorSkill, unarmored)
        lis.append(bps)
        # nose
        bps=_update_from_bp_nose(ent, bpm.nose, armorSkill, unarmored)
        lis.append(bps)
        # mouth
        bps=_update_from_bp_mouth(ent, bpm.mouth, armorSkill, unarmored)
        lis.append(bps)

def _update_from_bpc_legs(lis, ent, bpc, armorSkill, unarmored):
    for bpm in bpc.legs: # for each leg you possess,
        # foot
        bps=_update_from_bp_foot(ent, bpm.foot, armorSkill, unarmored)
        lis.append(bps)
        # leg
        bps=_update_from_bp_leg(ent, bpm.leg, armorSkill, unarmored)
        lis.append(bps)
# end def

def _update_from_bpc_arms(lis, ent, bpc, armorSkill, unarmored):
    i = 0
    for bpm in bpc.arms: # for each arm you possess,
        ismainhand = (i==0)
        i += 1
        
        # hand
        bps=_update_from_bp_hand(ent, bpm.hand, ismainhand)
        
        # check for two-handed bonus to 1-h weapons
        if ( ismainhand and bps.equip):
            if ( not rog.on(bpm.hand.held.item, TWOHANDS) and
                 not rog.off_arm(ent).hand.held.item ):
                bps.equip.addMods['atk'] = bps.equip.addMods.get(
                    'atk', 0 ) + MOD_2HANDBONUS_ATK*MULT_STATS
                bps.equip.addMods['pen'] = bps.equip.addMods.get(
                    'pen', 0 ) + MOD_2HANDBONUS_PEN*MULT_STATS
                bps.equip.addMods['dfn'] = bps.equip.addMods.get(
                    'dfn', 0 ) + MOD_2HANDBONUS_DFN*MULT_STATS
                bps.equip.addMods['arm'] = bps.equip.addMods.get(
                    'arm', 0 ) + MOD_2HANDBONUS_ARM*MULT_STATS
                bps.equip.addMods['pro'] = bps.equip.addMods.get(
                    'pro', 0 ) + MOD_2HANDBONUS_PRO*MULT_STATS
                bps.equip.addMods['asp'] = bps.equip.addMods.get(
                    'asp', 1 ) * MULT_2HANDBONUS_ASP
                bps.equip.addMods['dmg'] = bps.equip.addMods.get(
                    'dmg', 1 ) * MULT_2HANDBONUS_DMG
        #
        
        lis.append(bps)
        
        # arm
        bps=_update_from_bp_arm(ent, bpm.arm, armorSkill, unarmored)
        lis.append(bps)
# end def

# generic torso object with core, front (chest), back, and hips
def _update_from_bpc_torso(lis, ent, bpc, armorSkill, unarmored):
    # core
    bps=_update_from_bp_torsoCore(ent, bpc.core, armorSkill, unarmored)
    lis.append(bps)
    # front
    bps=_update_from_bp_torsoFront(ent, bpc.front, armorSkill, unarmored)
    lis.append(bps)
    # back
    bps=_update_from_bp_torsoBack(ent, bpc.back, armorSkill, unarmored)
    lis.append(bps)
    # hips
    bps=_update_from_bp_hips(ent, bpc.hips, armorSkill, unarmored)
    lis.append(bps)
    # heart, lungs (TODO)
# end def

# BP

# arm
def _update_from_bp_arm(ent, arm, armorSkill, unarmored):
    world = rog.world()
    dadd={}
    dmul={}
    eqdadd={}
    eqdmul={}
    
    cov = 0.15 # temporary (TODO: get from body plan...)
        
    # equipment
    if arm.slot.item:
        item=arm.slot.item
        equipable=world.component_for_entity(item, cmp.EquipableInArmSlot)
        
        eqdadd=get_addmods(world,item,equipable)
        
        armor_skillBonus(world,item,eqdadd,armorSkill,unarmored,cov)

        fittedBonus(world,ent,item,eqdadd)
        
        apply_penalties_armor(eqdadd, item)
        
        equip=__EQ(
            eqdadd['enc'], equipable.strReq, 0,
            eqdadd, eqdmul,
            BP_LIMB
            )
    else: # unarmored combat
        equip=None
        _apply_skillBonus_unarmored(dadd, unarmored, cov)
        
    # examine body part
    if arm.bone.status:
        _add(dadd, ADDMODS_BPP_ARM_BONESTATUS.get(arm.bone.status, {}))
    if arm.muscle.status:
        _add(dadd, ADDMODS_BPP_ARM_MUSCLESTATUS.get(arm.muscle.status, {}))
    if arm.skin.status:
        _add(dadd, ADDMODS_BPP_SKINSTATUS.get(arm.skin.status, {}))
    return __BPS(dadd,dmul, equip)
# end def

# hand
def _update_from_bp_hand(ent, hand, ismainhand=False):
    world = rog.world()
    dadd={}
    dmul={}
    eqdadd={}
    eqdmul={}

    skillsCompo=world.component_for_entity(ent, cmp.Skills)

    # equipment
    
    # TODO: gloves / gauntlets (hand armor)
    
    # held item (weapon)
    if hand.held.item:
        weapClass=None
        item=hand.held.item
        equipable=world.component_for_entity(item, cmp.EquipableInHoldSlot)
        
        eqdadd=get_addmods(world,item,equipable)
        
        # weapon skill bonus for item-weapons (armed combat)
        if world.has_component(item, cmp.WeaponSkill):
            weapClass=world.component_for_entity(item, cmp.WeaponSkill).skill
            skillLv = rog._getskill(skillsCompo.skills.get(weapClass, 0))
            if ismainhand:
                if skillLv:
                    _apply_skillBonus_weapon(eqdadd, skillLv, weapClass)
            else:
                if weapClass==SKL_SHIELDS:
                    _apply_skillBonus_weapon(eqdadd, skillLv, weapClass)
        
        fittedBonus(world,ent,item,eqdadd)
        
        # mainhand / offhand - specific stats
        if ismainhand:
            pass
        else: # offhand
            # offhand offensive penalty for offhand weapons
            eqdadd['reach'] = 0
            eqdadd['atk'] = 0
            eqdadd['dmg'] = 0
            eqdadd['pen'] = 0
            eqdadd['asp'] = 0
            eqdadd['gra'] = eqdadd.get('gra', 0) + OFFHAND_PENALTY_GRA
        # end if
        # offhand defensive penalty for offhand (non-shield) weapons
        #   AND for shields held in mainhand.
        offpenalty=False            
        if ( (not ismainhand and weapClass != SKL_SHIELDS) or
             (ismainhand and weapClass == SKL_SHIELDS) ):
            offpenalty=True
        if offpenalty:
            eqdadd['dfn'] = eqdadd.get('dfn', 0) * OFFHAND_PENALTY_DFNMOD
            eqdadd['arm'] = eqdadd.get('arm', 0) * OFFHAND_PENALTY_ARMMOD
            eqdadd['pro'] = eqdadd.get('pro', 0) * OFFHAND_PENALTY_PROMOD
        #
        
        
        # durability penalty multiplier for the stats
        apply_penalties_weapon(eqdadd, item)
        
        # armed wrestling still grants you some Gra, but significantly
        #   less than if you were unarmed.
        wreLv = rog._getskill(skillsCompo.skills.get(SKL_WRESTLING, 0))
        wreLv = wreLv // 3 # penalty to effective skill Lv
        if not ismainhand:
            wreLv = wreLv * 0.5 # penalty for offhand
        _apply_skillBonus_weapon(eqdadd, wreLv, SKL_WRESTLING, enc=False)
        
        equip=__EQ(
            eqdadd['enc'], equipable.strReq, equipable.dexReq,
            eqdadd, eqdmul,
            BP_HAND
            )
    #
    # unarmed combat
    else: 
        equip=None
        if ismainhand:
            # unarmed combat (hand-to-hand combat)
            boxLv = rog._getskill(skillsCompo.skills.get(SKL_BOXING, 0))
            _apply_skillBonus_weapon(dadd, boxLv, SKL_BOXING, enc=False)
            # wrestling unarmed
            wreLv = rog._getskill(skillsCompo.skills.get(SKL_WRESTLING, 0))
            wreLv = wreLv * 0.66666667 # most from mainhand, rest from offhand
            _apply_skillBonus_weapon(dadd, wreLv, SKL_WRESTLING, enc=False)
        else: # offhand
            # wrestling unarmed (offhand)
            wreLv = rog._getskill(skillsCompo.skills.get(SKL_WRESTLING, 0))
            wreLv = wreLv * 0.33333334
            _apply_skillBonus_weapon(dadd, wreLv, SKL_WRESTLING, enc=False)
    # end if
        
    # examine body part
    if hand.bone.status:
        _add(dadd, ADDMODS_BPP_HAND_BONESTATUS.get(hand.bone.status, {}))
    if hand.muscle.status:
        _add(dadd, ADDMODS_BPP_HAND_MUSCLESTATUS.get(hand.muscle.status, {}))
    if hand.skin.status:
        _add(dadd, ADDMODS_BPP_HAND_SKINSTATUS.get(hand.skin.status, {}))
    return __BPS(dadd,dmul, equip)
# end def

# leg
def _update_from_bp_leg(ent, leg, armorSkill, unarmored):
    world = rog.world()
    dadd={}
    dmul={}
    eqdadd={}
    eqdmul={}
    
    cov = 0.1 # temporary (TODO: get from body plan...)

    # equipment
    if leg.slot.item:
        item=leg.slot.item
        equipable=world.component_for_entity(item, cmp.EquipableInLegSlot)
        
        eqdadd=get_addmods(world,item,equipable)
        
        armor_skillBonus(world,item,eqdadd,armorSkill,unarmored,cov)

        fittedBonus(world,ent,item,eqdadd)
        
        apply_penalties_armor(eqdadd, item)
        
        equip=__EQ(
            eqdadd['enc'], equipable.strReq, 0,
            eqdadd, eqdmul,
            BP_LIMB
            )
                                
    else: # unarmored combat
        equip=None
        _apply_skillBonus_unarmored(dadd, unarmored, cov)
        
    # examine body part
    if leg.bone.status:
        _add(dadd, ADDMODS_BPP_LEG_BONESTATUS.get(leg.bone.status, {}))
        _mult(dmul, MULTMODS_BPP_LEG_BONESTATUS.get(leg.bone.status, {}))
    if leg.muscle.status:
        _add(dadd, ADDMODS_BPP_LEG_MUSCLESTATUS.get(leg.muscle.status, {}))
    if leg.skin.status:
        _add(dadd, ADDMODS_BPP_SKINSTATUS.get(leg.skin.status, {}))
    return __BPS(dadd,dmul, equip)
# end def

# foot
def _update_from_bp_foot(ent, foot, armorSkill, unarmored):
    world = rog.world()
    dadd={}
    dmul={}
    eqdadd={}
    eqdmul={}

    # equipment
    if foot.slot.item:
        item=foot.slot.item
        equipable=world.component_for_entity(item, cmp.EquipableInFootSlot)
        
        eqdadd=get_addmods(world,item,equipable)

        fittedBonus(world,ent,item,eqdadd)
        
        apply_penalties_armor(eqdadd, item)
        
        equip=__EQ(
            eqdadd['enc'], equipable.strReq, 0,
            eqdadd, eqdmul,
            BP_FOOT
            )
    else:
        equip=None
        
    # examine body part
    if foot.bone.status:
        _add(dadd, ADDMODS_BPP_LEG_BONESTATUS.get(foot.bone.status, {}))
        _mult(dmul, MULTMODS_BPP_LEG_BONESTATUS.get(foot.bone.status, {}))
    if foot.muscle.status:
        _add(dadd, ADDMODS_BPP_LEG_MUSCLESTATUS.get(foot.muscle.status, {}))
    if foot.skin.status:
        _add(dadd, ADDMODS_BPP_SKINSTATUS.get(foot.skin.status, {}))
    return __BPS(dadd,dmul, equip)
# end def

# head  
def _update_from_bp_head(ent, head, armorSkill, unarmored):
    world = rog.world()
    dadd={}
    dmul={}
    eqdadd={}
    eqdmul={}
    
    cov = 0.1 # temporary (TODO: get from body plan...)

    # equipment
    if head.slot.item:
        item=head.slot.item
        equipable=world.component_for_entity(item, cmp.EquipableInHeadSlot)
        
        eqdadd=get_addmods(world,item,equipable)
        
        # automatically convert the sight and hearing modifiers
        #  into multipliers for headwear, facewear, eye/earwear, etc.
        if 'sight' in eqdadd.keys(): # sense mod acts as multiplier not adder
            dmul['sight'] = eqdadd['sight']
            del eqdadd['sight']
        if 'hearing' in eqdadd.keys(): # sense mod acts as multiplier not adder
            dmul['hearing'] = eqdadd['hearing']
            del eqdadd['hearing']
        
        armor_skillBonus(world,item,eqdadd,armorSkill,unarmored,cov)

        fittedBonus(world,ent,item,eqdadd)
        
        apply_penalties_armor(eqdadd, item)
        
        equip=__EQ(
            eqdadd['enc'], equipable.strReq, 0,
            eqdadd, eqdmul,
            BP_HEAD
            )
                                
    else: # unarmored combat
        equip=None
        _apply_skillBonus_unarmored(dadd, unarmored, cov)
    
    # examine body part                
    if head.bone.status: # skull
        _add(dadd, ADDMODS_BPP_HEAD_BONESTATUS.get(head.bone.status, {}))
        _mult(dmul, MULTMODS_BPP_HEAD_BONESTATUS.get(head.bone.status, {}))
    if head.brain.status: # brain
        _add(dadd, ADDMODS_BPP_BRAINSTATUS.get(head.brain.status, {}))
        _mult(dmul, MULTMODS_BPP_BRAINSTATUS.get(head.brain.status, {}))
    if head.skin.status: # scalp
        _add(dadd, ADDMODS_BPP_SKINSTATUS.get(head.skin.status, {}))
    return __BPS(dadd,dmul, equip)
# end def

# face
def _update_from_bp_face(ent, face, armorSkill, unarmored):
    world = rog.world()
    dadd={}
    dmul={}
    eqdadd={}
    eqdmul={}

    # equipment
    if face.slot.item:
        item=face.slot.item
        equipable=world.component_for_entity(item, cmp.EquipableInFaceSlot)
        
        eqdadd=get_addmods(world,item,equipable)
        
        if 'sight' in eqdadd.keys(): # sense mod acts as multiplier not adder
            dmul['sight'] = eqdadd['sight']
            del eqdadd['sight']
        
        fittedBonus(world,ent,item,eqdadd)
        
        apply_penalties_armor(eqdadd, item)
        
        equip=__EQ(
            eqdadd['enc'], equipable.strReq, 0,
            eqdadd, eqdmul,
            BP_FACE
            )
    else:
        equip=None
        
    # examine body part
    if face.skin.status:
        _add(dadd, ADDMODS_BPP_FACE_SKINSTATUS.get(face.skin.status, {}))
    dadd['bea'] = dadd.get('bea', 0) + face.features.beauty
    dadd['idn']  = dadd.get('idn', 0) + face.features.scary
    return __BPS(dadd,dmul, equip)
# end def

# neck
def _update_from_bp_neck(ent, neck, armorSkill, unarmored):
    world = rog.world()
    dadd={}
    dmul={}
    eqdadd={}
    eqdmul={}

    # equipment
    if neck.slot.item:
        item=neck.slot.item
        equipable=world.component_for_entity(item, cmp.EquipableInNeckSlot)
        
        eqdadd=get_addmods(world,item,equipable)

        fittedBonus(world,ent,item,eqdadd)
        
        apply_penalties_armor(eqdadd, item)
        
        equip=__EQ(
            eqdadd['enc'], equipable.strReq, 0,
            eqdadd, eqdmul,
            BP_NECK
            )
    else:
        equip=None
        
    # examine body part
    if neck.skin.status:
        _add(dadd, ADDMODS_BPP_SKINSTATUS.get(neck.skin.status, {}))
    if neck.muscle.status:
        _add(dadd, ADDMODS_BPP_NECK_MUSCLESTATUS.get(neck.muscle.status, {}))
    if neck.bone.status:
        _add(dadd, ADDMODS_BPP_NECK_BONESTATUS.get(neck.bone.status, {}))
        _mult(dmul, MULTMODS_BPP_NECK_BONESTATUS.get(neck.bone.status, {}))
    return __BPS(dadd,dmul, equip)
# end def

# eyes
def _update_from_bp_eyes(ent, eyes, armorSkill, unarmored):
    world = rog.world()
    dadd={}
    dmul={}
    eqdadd={}
    eqdmul={}

    # equipment
    if eyes.slot.item:
        item=eyes.slot.item
        equipable=world.component_for_entity(item, cmp.EquipableInEyesSlot)
        
        eqdadd=get_addmods(world,item,equipable)
        
        if 'sight' in eqdadd.keys(): # sense mod acts as multiplier not adder
            dmul['sight'] = eqdadd['sight']
            del eqdadd['sight']
        
        fittedBonus(world,ent,item,eqdadd)
        
        apply_penalties_armor(eqdadd, item)
        
        equip=__EQ(
            eqdadd['enc'], equipable.strReq, 0,
            eqdadd, eqdmul,
            BP_EYES
            )
    else:
        equip=None
        
    # examine body part
    if eyes.open:
        dadd['sight'] = dadd.get('sight', 0) + eyes.visualSystem.quality
    return __BPS(dadd,dmul, equip)
# end def

# ears
def _update_from_bp_ears(ent, ears, armorSkill, unarmored):
    world = rog.world()
    dadd={}
    dmul={}
    eqdadd={}
    eqdmul={}
    # equipment (earplugs, earbuds, etc.)
    if ears.slot.item:
        item=ears.slot.item
        equipable=world.component_for_entity(item, cmp.EquipableInEarsSlot)
        
        eqdadd=get_addmods(world,item,equipable)
        
        if 'hearing' in eqdadd.keys(): # sense mod acts as multiplier not adder
            dmul['hearing'] = eqdadd['hearing']
            del eqdadd['hearing']
        
        fittedBonus(world,ent,item,eqdadd)
        
        apply_penalties_armor(eqdadd, item)
        
        equip=__EQ(
            eqdadd['enc'], equipable.strReq, 0,
            eqdadd, eqdmul,
            BP_EARS
            )
    else:
        equip=None
        
    # examine body part
    dadd['hearing'] = dadd.get('hearing', 0) + ears.auditorySystem.quality
    return __BPS(dadd,dmul, equip)
# end def

# nose
def _update_from_bp_nose(ent, nose, armorSkill, unarmored):
    dadd={}
    dmul={}
    eqdadd={}
    eqdmul={}
    # examine body part
    if nose.bone.status:
        _add(dadd, ADDMODS_BPP_FACE_BONESTATUS.get(mouth.bone.status, {}))
    return __BPS(dadd,dmul)
# end def

# mouth
def _update_from_bp_mouth(ent, mouth, armorSkill, unarmored):
    dadd={}
    dmul={}
    eqdadd={}
    eqdmul={}
    # examine body part
    if mouth.bone.status:
        _add(dadd, ADDMODS_BPP_FACE_BONESTATUS.get(mouth.bone.status, {}))
    if mouth.muscle.status:
        _add(dadd, ADDMODS_BPP_FACE_MUSCLESTATUS.get(mouth.muscle.status, {}))
    return __BPS(dadd,dmul)
# end def

# torso core
def _update_from_bp_torsoCore(ent, core, armorSkill, unarmored):
    world = rog.world()
    dadd={}
    dmul={}
    eqdadd={}
    eqdmul={}
    
    cov = 0.1 # temporary (TODO: get from body plan...)

    # equipment
    if core.slot.item:
        item=core.slot.item
        equipable=world.component_for_entity(item, cmp.EquipableInCoreSlot)
        
        eqdadd=get_addmods(world,item,equipable)
        
        armor_skillBonus(world,item,eqdadd,armorSkill,unarmored,cov)

        fittedBonus(world,ent,item,eqdadd)
        
        apply_penalties_armor(eqdadd, item)
        
        equip=__EQ(
            eqdadd['enc'], equipable.strReq, 0,
            eqdadd, eqdmul,
            BP_TORSO
            )
                                
    else: # unarmored combat
        equip=None
        _apply_skillBonus_unarmored(dadd, unarmored, cov)
             
    # examine body part
    if core.skin.status:
        _add(dadd, ADDMODS_BPP_SKINSTATUS.get(core.skin.status, {}))
    if core.muscle.status:
        _add(dadd, ADDMODS_BPP_TORSO_MUSCLESTATUS.get(core.muscle.status, {}))
    if core.guts.status:
        _add(dadd, ADDMODS_BPP_GUTSSTATUS.get(core.guts.status, {}))
    return __BPS(dadd,dmul, equip)
# end def

# torso front
def _update_from_bp_torsoFront(ent, front, armorSkill, unarmored):
    world = rog.world()
    dadd={}
    dmul={}
    eqdadd={}
    eqdmul={}
    
    cov = 0.1 # temporary (TODO: get from body plan...)
    cov += 0.1 * len(front.slot.covers)

    # equipment
    if front.slot.item:
        item=front.slot.item
        equipable=world.component_for_entity(item, cmp.EquipableInFrontSlot)
        
        eqdadd=get_addmods(world,item,equipable)
        
        armor_skillBonus(world,item,eqdadd,armorSkill,unarmored,cov)

        fittedBonus(world,ent,item,eqdadd)
        
        apply_penalties_armor(eqdadd, item)
        
        equip=__EQ(
            eqdadd['enc'], equipable.strReq, 0,
            eqdadd, eqdmul,
            BP_TORSO
            )
                                
    else: # unarmored combat
        equip=None
        _apply_skillBonus_unarmored(dadd, unarmored, cov)
             
    # examine body part
    if front.skin.status:
        _add(dadd, ADDMODS_BPP_SKINSTATUS.get(front.skin.status, {}))
    if front.muscle.status:
        _add(dadd, ADDMODS_BPP_TORSO_MUSCLESTATUS.get(front.muscle.status, {}))
    if front.bone.status:
        _add(dadd, ADDMODS_BPP_TORSO_BONESTATUS.get(front.bone.status, {}))
        _mult(dmul, MULTMODS_BPP_TORSO_BONESTATUS.get(front.bone.status, {}))
    return __BPS(dadd,dmul, equip)
# end def

# torso back
def _update_from_bp_torsoBack(ent, back, armorSkill, unarmored):
    world = rog.world()
    dadd={}
    dmul={}
    eqdadd={}
    eqdmul={}
    
    cov = 0.1 # temporary (TODO: get from body plan...)

    # equipment
    if back.slot.item:
        item=back.slot.item
        equipable=world.component_for_entity(item, cmp.EquipableInBackSlot)
        
        eqdadd=get_addmods(world,item,equipable)
        
        armor_skillBonus(world,item,eqdadd,armorSkill,unarmored,cov)

        fittedBonus(world,ent,item,eqdadd)
        
        apply_penalties_armor(eqdadd, item)
        
        equip=__EQ(
            eqdadd['enc'], equipable.strReq, 0,
            eqdadd, eqdmul,
            BP_TORSO
            )
                                
    else: # unarmored combat
        equip=None
        _apply_skillBonus_unarmored(dadd, unarmored, cov)
             
    # examine body part
    if back.skin.status:
        _add(dadd, ADDMODS_BPP_SKINSTATUS.get(back.skin.status, {}))
    if back.muscle.status:
        _add(dadd, ADDMODS_BPP_BACK_MUSCLESTATUS.get(back.muscle.status, {}))
    if back.bone.status:
        _add(dadd, ADDMODS_BPP_BACK_BONESTATUS.get(back.bone.status, {}))
        _mult(dmul, MULTMODS_BPP_BACK_BONESTATUS.get(back.bone.status, {}))
    return __BPS(dadd,dmul, equip)
# end def

# hips
def _update_from_bp_hips(ent, hips, armorSkill, unarmored):
    world = rog.world()
    dadd={}
    dmul={}
    eqdadd={}
    eqdmul={}
    
    cov = 0.1 # temporary (TODO: get from body plan...)

    # equipment
    if hips.slot.item:
        item=hips.slot.item
        equipable=world.component_for_entity(item, cmp.EquipableInHipsSlot)
        
        eqdadd=get_addmods(world,item,equipable)
        
        armor_skillBonus(world,item,eqdadd,armorSkill,unarmored,cov)

        fittedBonus(world,ent,item,eqdadd)
        
        apply_penalties_armor(eqdadd, item)
        
        equip=__EQ(
            eqdadd['enc'], equipable.strReq, 0,
            eqdadd, eqdmul,
            BP_TORSO
            )
                                
    else: # unarmored combat
        equip=None
        _apply_skillBonus_unarmored(dadd, unarmored, cov)
             
    # examine body part
    if hips.skin.status:
        _add(dadd, ADDMODS_BPP_SKINSTATUS.get(hips.skin.status, {}))
    if hips.muscle.status:
        _add(dadd, ADDMODS_BPP_TORSO_MUSCLESTATUS.get(hips.muscle.status, {}))
    if hips.bone.status:
        _add(dadd, ADDMODS_BPP_TORSO_BONESTATUS.get(hips.bone.status, {}))
        _mult(dmul, MULTMODS_BPP_TORSO_BONESTATUS.get(hips.bone.status, {}))
    return __BPS(dadd,dmul, equip)
# end def

# wing
def _update_from_bp_wing(ent, wing, armorSkill, unarmored):
    pass
# end def

# tail
def _update_from_bp_tail(ent, tail, armorSkill, unarmored):
    pass
# end def

# genitals
def _update_from_bp_genitals(ent, wing, armorSkill, unarmored):
    pass
# end def

# tentacle
def _update_from_bp_tentacle(ent, tentacle, armorSkill, unarmored):
    pass
# end def

# pseudopod
def _update_from_bp_pseudopod(ent, pseudopod, armorSkill, unarmored):
    pass
# end def

# ameboid
def _update_from_bp_ameboid(ent, ameboid, armorSkill, unarmored):
    pass
# end def

# appendage
def _update_from_bp_appendage(ent, appendage, armorSkill, unarmored):
    pass
# end def


'''
    Body functions
'''

def metabolism(ent, hunger: int, thirst=0) -> bool:
    '''
        burn calories
        filter water through kidneys (TO ALTER?)
            should you have to piss and shit in this game?
        
        DOES NOT:
            extract calories/water from food (stomach function does that)
        
        Parameters:
            hunger     calories to burn (not KiloCalories)
            thirst     thirst points to burn
        
        NOTE: No need for a processor to call this.
            Every action performed by any entity will call this function
            with the appropriate parameters for that action.
    '''
    assert(isinstance(hunger, int))
    
    body = rog.world().component_for_entity(ent, cmp.Body)
    meters = rog.world().component_for_entity(ent, cmp.Meters)

    status = rog.get_status(ent, cmp.StatusDehydrated)
    if status: # dehydration stops metabolic processes
        return False
    
    # hunger
    body.satiation -= hunger
    
    # thirst
    # add extra thirst from parameter, burn water equivalent to
    #  quantity of calories burned.
    thirst = 1 + int(thirst + hunger*METABOLISM_THIRST)
    body.hydration -= thirst
    
    # heat generation that is unaffected by heat res
    meters.temp += hunger * METABOLISM_HEAT

    return True
# end def


def starve(ent):
    body = rog.world().component_for_entity(ent, cmp.Body)
    if body.bodyfat > 0:
        # get calorie deficit from fat, and eat 10g of fat for 90 calories
        body.bodyfat = body.bodyfat - 0.01
        body.satiation += 90 # 9 (Kilo)Calories per g of fat, so 90 calories per 0.01g of fat.
    else:
        rog.set_status(ent, cmp.StatusEmaciated)

def dehydrate(ent):
    rog.damage(ent, 1)
    rog.sap(ent, 1)

##def wasteaway(body): handled by BodyProcessor
##    ''' consume muscle mass of the body for food '''
##    pass






'''
    # creator functions #
'''

#create a thing from STUFF; does not register thing
def create_stuff(name, x, y) -> int:
    typ,mat,val,fgcol,hp,kg,script,idtype = STUFF[name]
    world = rog.world()
    if fgcol == "random":
        fgcol = random.choice(list(COL.values()))
    else:
        fgcol = COL[fgcol]
    ent = world.create_entity(
        cmp.Name(name, title=TITLE_THE),
        cmp.Position(x,y),
        cmp.Draw(typ, fgcol=fgcol, bgcol=COL['deep']),
        cmp.Form( mat=mat, val=max(1, round(val*MULT_VALUE)) ),
        cmp.Stats(hp=hp*MULT_STATS, mass=round(kg*MULT_MASS)),
        cmp.Meters(),
        cmp.Flags(),
        cmp.Identify(idtype)
        )
    _setGenericData(ent, material=mat)
    _setGenericShape(ent, idtype)
    script(ent)
    return ent
#create a thing from RAWMATERIALS; does not register thing
def create_rawmat(name, x, y) -> int:
    typ,val,kg,hp,mat,fgcol,script,idtype = RAWMATERIALS[name]
    world = rog.world()
    if fgcol == "random":
        fgcol = random.choice(list(COL.values()))
    else:
        fgcol = COL[fgcol]
    ent = world.create_entity(
        cmp.Name(name, title=TITLE_THE),
        cmp.Position(x,y),
        cmp.Draw(typ, fgcol=fgcol, bgcol=COL['deep']),
        cmp.Form( mat=mat, val=max(1, round(val*MULT_VALUE)) ),
        cmp.Stats(hp=hp*MULT_STATS, mass=round(kg*MULT_MASS)),
        cmp.Meters(),
        cmp.Flags(),
        cmp.Identify(idtype)
        )
    _setGenericData(ent, material=mat)
    _setGenericShape(ent, idtype)
    script(ent)
    return ent


#create a fluid
def create_fluid(x,y,ID,volume) -> int:
    ent = world.create_entity(cmp.Position(x,y), cmp.Fluid(ID, volume))
    return ent


#-----------------#
# non-weapon gear #
#-----------------#

def _getGearStatsDict( ent,mass,resbio,resfire,rescold,reselec,
        resphys,resbleed,reslight,ressound,dfn,arm,pro,enc,sight ):
    #{var : modf}
    statsDict={'mass':mass}
    if resbio!=0: statsDict.update({"resbio":resbio})
    if resfire!=0: statsDict.update({"resfire":resfire})
    if rescold!=0: statsDict.update({"rescold":rescold})
    if reselec!=0: statsDict.update({"reselec":reselec})
    if resphys!=0: statsDict.update({"resphys":resphys})
    if resbleed!=0: statsDict.update({"resbleed":resbleed})
    if reslight!=0: statsDict.update({"reslight":reslight})
    if ressound!=0: statsDict.update({"ressound":ressound})
    if dfn!=0: statsDict.update({"dfn":dfn})
    if arm!=0: statsDict.update({"arm":arm})
    if pro!=0: statsDict.update({"pro":pro})
    if sight!=0: statsDict.update({"sight":sight})
    if enc==0: enc=1
    rog.world().add_component(ent, cmp.Encumberance(enc))
    return statsDict

#create_armor - create armor item on ARMOR table 
def create_armor(name,x,y,condition=1) -> int:
    '''
        # Parameters:
        #   name : string = name of item to create from the data table
        #   quality : float = 0 to 1. Determines starting HP of the item
    '''
    world = rog.world()
    ent = world.create_entity()
    
    gData = ARMOR[name]
    value = int(get_gear_value(gData)*MULT_VALUE)
    mass = round(get_gear_mass(gData)*MULT_MASS)
    hpmax = get_gear_hpmax(gData)
    apCost = get_gear_apCost(gData)
    material = get_gear_mat(gData)
    strReq = get_gear_strReq(gData)
    dfn = rog.around(get_gear_dv(gData)*MULT_STATS)
    arm = rog.around(get_gear_av(gData)*MULT_STATS)
    pro = rog.around(get_gear_pro(gData)*MULT_STATS)
    enc = get_gear_enc(gData)
    resbio = get_gear_resbio(gData)
    resfire = get_gear_resfire(gData)
    rescold = get_gear_rescold(gData)
    reselec = get_gear_reselec(gData)
    resphys = get_gear_resphys(gData)
    resbleed = get_gear_resbleed(gData)
    reslight = 0#get_gear_reslight(gData)
    ressound = 0#get_gear_ressound(gData)
    sight = 1#get_gear_sight(gData)
    back = get_armor_coversBack(gData)
    core = get_armor_coversCore(gData)
    hips = get_armor_coversHips(gData)
##    arms = get_armor_coversArms(gData)
    script = get_armor_script(gData)
    idtype = get_armor_idtype(gData)
    
    fgcol = COL['accent']
    bgcol = COL['deep']
    
    world.add_component(ent, cmp.Name(name, title=TITLE_THE))
    world.add_component(ent, cmp.Identify(idtype))
    world.add_component(ent, cmp.Position(x, y))
    world.add_component(ent, cmp.Draw(char=T_ARMOR,fgcol=fgcol,bgcol=bgcol) )
    world.add_component(ent, cmp.Form(mat=material, val=value))
    world.add_component(ent, cmp.Flags())
    world.add_component(ent, cmp.Meters())
    # stats component
    stats=cmp.Stats(
        hp=hpmax,mp=hpmax,mass=mass
        )
    stats.hp = rog.around(stats.hpmax * condition)
    world.add_component(ent, stats)
    
    _setGenericData(ent, material=material)
    _setGenericShape(ent, idtype)
    
    statsDict=_getGearStatsDict( ent,mass,resbio,resfire,rescold,reselec,
        resphys,resbleed,reslight,ressound,dfn,arm,pro,enc,sight )
    world.add_component(ent, cmp.EquipableInFrontSlot(
        apCost, statsDict, coversBack=back,coversCore=core,
        coversHips=hips, strReq=strReq) )
    
    if script: script(ent)
    return ent
#

#create head armor - create armor item on HEADWEAR table 
def create_headwear(name,x,y,condition=1) -> int:
    world = rog.world()
    ent = world.create_entity()
    
    gData = HEADWEAR[name]
    value = int(get_gear_value(gData)*MULT_VALUE)
    mass = round(get_gear_mass(gData)*MULT_MASS)
    hpmax = get_gear_hpmax(gData)
    apCost = get_gear_apCost(gData)
    material = get_gear_mat(gData)
    strReq = get_gear_strReq(gData)
    dfn = rog.around(get_gear_dv(gData)*MULT_STATS)
    arm = rog.around(get_gear_av(gData)*MULT_STATS)
    pro = rog.around(get_gear_pro(gData)*MULT_STATS)
    enc = get_gear_enc(gData)
    resbio = get_gear_resbio(gData)
    resfire = get_gear_resfire(gData)
    rescold = get_gear_rescold(gData)
    reselec = get_gear_reselec(gData)
    resphys = get_gear_resphys(gData)
    resbleed = get_gear_resbleed(gData)
    reslight = get_gear_reslight(gData)
    ressound = get_gear_ressound(gData)
    per = get_gear_sight(gData)
    neck = get_headwear_neck(gData)
    eyes = get_headwear_eyes(gData)
    ears = get_headwear_ears(gData)
    face = get_headwear_face(gData)
    script = get_headwear_script(gData)
    idtype = get_headwear_idtype(gData)
    
    fgcol = COL['accent']
    bgcol = COL['deep']
    
    world.add_component(ent, cmp.Name(name, title=TITLE_THE))
    world.add_component(ent, cmp.Identify(idtype))
    world.add_component(ent, cmp.Position(x, y))
    world.add_component(ent, cmp.Draw(char=T_HEADWEAR,fgcol=fgcol,bgcol=bgcol) )
    world.add_component(ent, cmp.Form(mat=material, val=value))
    world.add_component(ent, cmp.Flags())
    world.add_component(ent, cmp.Meters())
    # stats component
    stats=cmp.Stats(
        hp=hpmax,mp=hpmax,mass=mass
        )
    stats.hp = rog.around(stats.hpmax * condition)
    world.add_component(ent, stats)
    
    _setGenericData(ent, material=material)
    _setGenericShape(ent, idtype)
    
    statsDict=_getGearStatsDict( ent, mass,resbio,resfire,rescold,reselec,
        resphys,resbleed,reslight,ressound,dfn,arm,pro,enc,per )
    statsDict['hearing'] = statsDict['sight']
    world.add_component(ent, cmp.EquipableInHeadSlot(
        apCost, statsDict, coversNeck=neck,coversFace=face,
        coversEyes=eyes,coversEars=ears, strReq=strReq) )
    
    if script: script(ent)
    return ent
#

#create facewear - create armor item on FACEWEAR table 
def create_facewear(name,x,y,condition=1) -> int:
    world = rog.world()
    ent = world.create_entity()
    
    gData = ARMOR[name]
    value = int(get_gear_value(gData)*MULT_VALUE)
    mass = round(get_gear_mass(gData)*MULT_MASS)
    hpmax = get_gear_hpmax(gData)
    apCost = get_gear_apCost(gData)
    material = get_gear_mat(gData)
    strReq = get_gear_strReq(gData)
    dfn = rog.around(get_gear_dv(gData)*MULT_STATS)
    arm = rog.around(get_gear_av(gData)*MULT_STATS)
    pro = rog.around(get_gear_pro(gData)*MULT_STATS)
    enc = get_gear_enc(gData)
    resbio = get_gear_resbio(gData)
    resfire = get_gear_resfire(gData)
    rescold = get_gear_rescold(gData)
    reselec = get_gear_reselec(gData)
    resphys = get_gear_resphys(gData)
    resbleed = get_gear_resbleed(gData)
    reslight = get_gear_reslight(gData)
    ressound = get_gear_ressound(gData)
    sight = get_gear_sight(gData)
    eyes = get_facewear_eyes(gData)
    script = get_facewear_script(gData)
    idtype = get_facewear_idtype(gData)
    
    fgcol = COL['accent']
    bgcol = COL['deep']
    
    world.add_component(ent, cmp.Name(name, title=TITLE_THE))
    world.add_component(ent, cmp.Identify(idtype))
    world.add_component(ent, cmp.Position(x, y))
    world.add_component(ent, cmp.Draw(char=T_HEADWEAR,fgcol=fgcol,bgcol=bgcol) )
    world.add_component(ent, cmp.Form(mat=material, val=value))
    world.add_component(ent, cmp.Flags())
    world.add_component(ent, cmp.Meters())
    # stats component
    stats=cmp.Stats(
        hp=hpmax,mp=hpmax,mass=mass
        )
    stats.hp = rog.around(stats.hpmax * condition)
    world.add_component(ent, stats)
    
    _setGenericData(ent, material=material)
    _setGenericShape(ent, idtype)
    
    statsDict=_getGearStatsDict( ent, mass,resbio,resfire,rescold,reselec,
        resphys,resbleed,reslight,ressound,dfn,arm,pro,enc,sight )
    world.add_component(ent, cmp.EquipableInFaceSlot(
        apCost, statsDict, coversEyes=eyes, strReq=strReq) )
    
    if script: script(ent)
    return ent
#

#create armwear - create armor item on ARMARMOR table | arm armor
def create_armwear(name,x,y,condition=1) -> int:
    world = rog.world()
    ent = world.create_entity()
    
    gData = ARMARMOR[name]
    value = int(get_gear_value(gData)*MULT_VALUE)
    mass = round(get_gear_mass(gData)*MULT_MASS)
    hpmax = get_gear_hpmax(gData)
    apCost = get_gear_apCost(gData)
    material = get_gear_mat(gData)
    strReq = get_gear_strReq(gData)
    dfn = rog.around(get_gear_dv(gData)*MULT_STATS)
    arm = rog.around(get_gear_av(gData)*MULT_STATS)
    pro = rog.around(get_gear_pro(gData)*MULT_STATS)
    enc = get_gear_enc(gData)
    resbio = get_gear_resbio(gData)
    resfire = get_gear_resfire(gData)
    rescold = get_gear_rescold(gData)
    reselec = get_gear_reselec(gData)
    resphys = get_gear_resphys(gData)
    resbleed = get_gear_resbleed(gData)
    reslight = ressound = 0
    sight = 1
    script = get_gear_script(gData)
    idtype = get_gear_idtype(gData)
    
    fgcol = COL['accent']
    bgcol = COL['deep']
    
    world.add_component(ent, cmp.Name(name, title=TITLE_THE))
    world.add_component(ent, cmp.Identify(idtype))
    world.add_component(ent, cmp.Position(x, y))
    world.add_component(ent, cmp.Draw(char=T_ARMOR,fgcol=fgcol,bgcol=bgcol) )
    world.add_component(ent, cmp.Form(mat=material, val=value))
    world.add_component(ent, cmp.Flags())
    world.add_component(ent, cmp.Meters())
    # stats component
    stats=cmp.Stats(
        hp=hpmax,mp=hpmax,mass=mass
        )
    stats.hp = rog.around(stats.hpmax * condition)
    world.add_component(ent, stats)
    
    _setGenericData(ent, material=material)
    _setGenericShape(ent, idtype)
    
    statsDict=_getGearStatsDict( ent, mass,resbio,resfire,rescold,reselec,
        resphys,resbleed,reslight,ressound,dfn,arm,pro,enc,sight )
    world.add_component(ent, cmp.EquipableInArmSlot(
        apCost, statsDict, strReq=strReq))
    
    if script: script(ent)
    return ent
#

#create legging - create armor item on LEGARMOR table | leg armor
def create_legwear(name,x,y,condition=1) -> int:
    world = rog.world()
    ent = world.create_entity()
    
    gData = LEGARMOR[name]
    value = int(get_gear_value(gData)*MULT_VALUE)
    mass = round(get_gear_mass(gData)*MULT_MASS)
    hpmax = get_gear_hpmax(gData)
    apCost = get_gear_apCost(gData)
    material = get_gear_mat(gData)
    strReq = get_gear_strReq(gData)
    dfn = rog.around(get_gear_dv(gData)*MULT_STATS)
    arm = rog.around(get_gear_av(gData)*MULT_STATS)
    pro = rog.around(get_gear_pro(gData)*MULT_STATS)
    enc = get_gear_enc(gData)
    resbio = get_gear_resbio(gData)
    resfire = get_gear_resfire(gData)
    rescold = get_gear_rescold(gData)
    reselec = get_gear_reselec(gData)
    resphys = get_gear_resphys(gData)
    resbleed = get_gear_resbleed(gData)
    reslight = ressound = 0
    sight = 1
    coversBoth = get_legwear_coversBoth(gData)
    script = get_legwear_script(gData)
    idtype = get_legwear_idtype(gData)
    
    fgcol = COL['accent']
    bgcol = COL['deep']
    
    world.add_component(ent, cmp.Name(name, title=TITLE_THE))
    world.add_component(ent, cmp.Identify(idtype))
    world.add_component(ent, cmp.Position(x, y))
    world.add_component(ent, cmp.Draw(char=T_ARMOR,fgcol=fgcol,bgcol=bgcol) )
    world.add_component(ent, cmp.Form(mat=material, val=value))
    world.add_component(ent, cmp.Flags())
    world.add_component(ent, cmp.Meters())
    # stats component
    stats=cmp.Stats(
        hp=hpmax,mp=hpmax,mass=mass
        )
    stats.hp = rog.around(stats.hpmax * condition)
    world.add_component(ent, stats)
    
    _setGenericData(ent, material=material)
    _setGenericShape(ent, idtype)
    
    statsDict=_getGearStatsDict( ent, mass,resbio,resfire,rescold,reselec,
        resphys,resbleed,reslight,ressound,dfn,arm,pro,enc,sight )
    world.add_component(ent, cmp.EquipableInLegSlot(
        apCost, statsDict, strReq=strReq))
    if coversBoth:
        _coversBothLegs(ent)
    
    if script: script(ent)
    return ent
#

#create foot armor - create armor item on FOOTARMOR table 
def create_footwear(name,x,y,condition=1) -> int:
    world = rog.world()
    ent = world.create_entity()
    
    gData = FOOTARMOR[name]
    value = int(get_gear_value(gData)*MULT_VALUE)
    mass = round(get_gear_mass(gData)*MULT_MASS)
    hpmax = get_gear_hpmax(gData)
    apCost = get_gear_apCost(gData)
    material = get_gear_mat(gData)
    strReq = get_gear_strReq(gData)
    dfn = rog.around(get_gear_dv(gData)*MULT_STATS)
    arm = rog.around(get_gear_av(gData)*MULT_STATS)
    pro = rog.around(get_gear_pro(gData)*MULT_STATS)
    enc = get_gear_enc(gData)
    resbio = get_gear_resbio(gData)
    resfire = get_gear_resfire(gData)
    rescold = get_gear_rescold(gData)
    reselec = get_gear_reselec(gData)
    resphys = get_gear_resphys(gData)
    resbleed = get_gear_resbleed(gData)
    reslight = ressound = 0
    sight = 1
    script = get_gear_script(gData)
    idtype = get_gear_idtype(gData)
    
    fgcol = COL['accent']
    bgcol = COL['deep']
    
    world.add_component(ent, cmp.Name(name, title=TITLE_THE))
    world.add_component(ent, cmp.Identify(idtype))
    world.add_component(ent, cmp.Position(x, y))
    world.add_component(ent, cmp.Draw(char=T_ARMOR,fgcol=fgcol,bgcol=bgcol) )
    world.add_component(ent, cmp.Form(mat=material, val=value))
    world.add_component(ent, cmp.Flags())
    world.add_component(ent, cmp.Meters())
    # stats component
    stats=cmp.Stats(
        hp=hpmax,mp=hpmax,mass=mass
        )
    stats.hp = rog.around(stats.hpmax * condition)
    world.add_component(ent, stats)
    
    _setGenericData(ent, material=material)
    _setGenericShape(ent, idtype)
    
    statsDict=_getGearStatsDict( ent, mass,resbio,resfire,rescold,reselec,
        resphys,resbleed,reslight,ressound,dfn,arm,pro,enc,sight )
    world.add_component(ent, cmp.EquipableInFootSlot(
        apCost, statsDict, strReq=strReq))
    
    if script: script(ent)
    return ent
#

# weapons
def create_weapon(name, x,y, condition=1) -> int:
    world = rog.world()
    ent = world.create_entity()
    # get weapon data from table
    data = WEAPONS[name]
    _type       = T_MELEEWEAPON
    value       = int(get_weapon_value(data)*MULT_VALUE)
    mass        = int(get_weapon_mass(data)*MULT_MASS)
    hpmax       = get_weapon_hpmax(data)
    material    = get_weapon_mat(data)
    strReq      = get_weapon_strReq(data)
    dexReq      = get_weapon_dexReq(data)
    atk         = rog.around(get_weapon_atk(data)*MULT_STATS)
    dmg         = rog.around(get_weapon_dmg(data)*MULT_STATS)
    pen         = rog.around(get_weapon_pen(data)*MULT_STATS)
    dfn         = rog.around(get_weapon_dv(data)*MULT_STATS)
    arm         = rog.around(get_weapon_av(data)*MULT_STATS)
    pro         = rog.around(get_weapon_pro(data)*MULT_STATS)
    asp         = get_weapon_asp(data)
    enc         = get_weapon_enc(data)
    ctr         = rog.around(get_weapon_ctr(data)*MULT_STATS)
    gra         = rog.around(get_weapon_gra(data)*MULT_STATS)
    stamina_cost= get_weapon_staminacost(data)
    reach       = rog.around(get_weapon_reach(data)*MULT_STATS)
##    grp         = get_weapon_grip(data)
    skill       = get_weapon_skill(data)
    script      = get_weapon_script(data)
    idtype      = get_weapon_idtype(data)
    #
    # color
    fgcol = COL['accent'] #TODO: get color from somewhere else. Material?
    bgcol = COL['deep']
    # build entity
    world.add_component(ent, cmp.Name(name, title=TITLE_THE))
    world.add_component(ent, cmp.Identify(idtype))
    world.add_component(ent, cmp.Draw(char=_type,fgcol=fgcol,bgcol=bgcol))
    world.add_component(ent, cmp.Form(mat=material,val=value))
    world.add_component(ent, cmp.Position(x, y))    
    world.add_component(ent, cmp.Flags())
    world.add_component(ent, cmp.Meters())
    # stats component
    stats=cmp.Stats(
        hp=hpmax,mp=0,mass=mass
        )
    stats.hp = rog.around(stats.hpmax * condition)
    world.add_component(ent, stats)
    
    _setGenericData(ent, material=material)
    _setGenericShape(ent, idtype)
    
    # equipable
    modDict={'mass':mass} # equipable components need to have mass as a mod
    if not atk==0: modDict.update({'atk':atk})
    if not dmg==0: modDict.update({'dmg':dmg})
    if not pen==0: modDict.update({'pen':pen})
    if not dfn==0: modDict.update({'dfn':dfn})
    if not arm==0: modDict.update({'arm':arm})
    if not pro==0: modDict.update({'pro':pro})
    if not asp==0: modDict.update({'asp':asp})
    if not ctr==0: modDict.update({'ctr':ctr})
    if not gra==0: modDict.update({'gra':gra})
    if not reach==0: modDict.update({'reach':reach})
    if enc==0: enc=1
    world.add_component(ent, cmp.Encumberance(enc))
    world.add_component(ent, cmp.EquipableInHoldSlot(
        NRG_WIELD, stamina_cost, modDict, strReq=strReq, dexReq=dexReq) )
    if skill:
        world.add_component(ent,cmp.WeaponSkill(skill))
    # quality
    minGrind=-2
    maxGrind=MAXGRIND_FROM_MATERIAL[material]
    world.add_component(ent,cmp.Quality(0, minGrind, maxGrind))
    # script
    if script: script(ent)
    return ent
#

def create_ranged_weapon(name, x, y, condition=1) -> int:
    world = rog.world()
    ent = world.create_entity()
    
    # get data
    ammotype    = get_ranged_ammotype(name)
    value       = round(get_ranged_value(name)*MULT_VALUE)
    kg          = round(get_ranged_kg(name)*MULT_MASS)
    hpmax       = get_ranged_hp(name)
    material    = get_ranged_mat(name)
    strReq      = get_ranged_strReq(name)
    dexReq      = get_ranged_dexReq(name)
    capacity    = get_ranged_capacity(name)
    rTime       = get_ranged_reloadTime(name)
    nShots      = get_ranged_nShots(name)
    jam         = get_ranged_jamChance(name)
    minRng      = get_ranged_minRng(name)
    maxRng      = get_ranged_maxRng(name)
    rasp        = get_ranged_rasp(name)
    ratk        = int(get_ranged_ratk(name)*MULT_STATS)
    rdmg        = int(get_ranged_rdmg(name)*MULT_STATS)
    rpen        = int(get_ranged_rpen(name)*MULT_STATS)
    dfn         = int(get_ranged_dfn(name)*MULT_STATS)
    enc         = get_ranged_enc(name)
    force       = get_ranged_force(name)
    skill       = get_ranged_skill(name)
    script      = get_ranged_script(name)
    idtype      = get_ranged_idtype(gData)
    
    # AP cost to equip (TODO: get based on mass of weapon / weapon type?)
    wieldAP     = NRG_WIELD
    
    # function that runs when you shoot (TODO: get default based on weapon type)
    func        = None
    
    # color
    fgcol = COL['accent'] #TODO: get color from somewhere else. Material?
    bgcol = COL['deep']
    # build entity
    world.add_component(ent, cmp.Name(name, title=TITLE_THE))
    world.add_component(ent, cmp.Identify(idtype))
    world.add_component(ent, cmp.Position(x, y))
    world.add_component(ent, cmp.Draw(char=_type,fgcol=fgcol,bgcol=bgcol))
    world.add_component(ent, cmp.Form(mat=material,val=value))    
    world.add_component(ent, cmp.Flags())
    world.add_component(ent, cmp.Meters())
    # stats component
    stats=cmp.Stats(
        hp=hpmax,mp=0,mass=mass
        )
    stats.hp = rog.around(stats.hpmax * condition)
    world.add_component(ent, stats)
    
    _setGenericData(ent, material=material)
    _setGenericShape(ent, idtype)
    
    # equipable
    modDict={'mass':mass} # equipable components need to have mass as a mod
    if not dfn==0: modDict.update({'dfn':dfn})
    if not reach==0: modDict.update({'reach':reach})
    if not ratk==0: modDict.update({'ratk':ratk})
    if not rdmg==0: modDict.update({'rdmg':rdmg})
    if not rpen==0: modDict.update({'rpen':rpen})
    if not rasp==0: modDict.update({'rasp':rasp})
    if not minRng==0: modDict.update({'minRng':minRng})
    if not maxRng==0: modDict.update({'maxRng':maxRng})
    if enc==0: enc=1
    world.add_component(ent, cmp.Encumberance(enc))
    world.add_component(ent, cmp.Shootable(
        set((ammotype,)), cap=capacity, nshots=nShots,
        rtime=rTime, jam=jam, func=None) ) # TODO: func
    world.add_component(ent, cmp.EquipableInHoldSlot(
        wieldAP, stamina_cost, modDict, strReq=strReq, dexReq=dexReq) )
    if skill:
        world.add_component(ent,cmp.WeaponSkill(skill))
    # quality
    minGrind=-2
    maxGrind=MAXGRIND_FROM_MATERIAL[material]
    world.add_component(ent,cmp.Quality(0, minGrind, maxGrind))
    # script
    if script: script(ent)
    return ent
#

# monsters
def create_monster(_type, x, y, col=None, money=0) -> int:    
    if not col:
        col = COL['red']
    
    monData = BESTIARY[_type]
    name = getMonName(_type)
    kg = round(getMonKG(_type)*MULT_MASS)
    cm = getMonCM(_type)
    mat = getMonMat(_type)
    bodyplan = getMonBodyPlan(_type)
    flags = getMonFlags(_type)
    script = getMonScript(_type)
    stats = getMonStats(_type)
    idtype = getMonID(_type)
    
    sight=round(BASE_SIGHT*stats.get('sight',1))
    hear=round(BASE_HEARING*stats.get('hearing',1))
    
    female=False #temporary
    if bodyplan==BODYPLAN_HUMANOID:
        body, basekg = create_body_humanoid(kg, cm, female)

    # set body sight and hearing to the correct values
    # (TODO)
    
    
    stats=cmp.Stats(
        mass=basekg,
        encmax=BASE_ENCMAX+stats.get('encmax',0),
        hp=BASE_HP+stats.get('hp',0),
        mp=BASE_MP+stats.get('mp',0),
        mpregen=(BASE_MPREGEN+stats.get('mpregen',0))*MULT_STATS,
        reach=(BASE_REACH+stats.get('reach',0))*MULT_STATS,
        resfire=BASE_RESFIRE+stats.get('resfire',0),
        resbio=BASE_RESBIO+stats.get('resbio',0),
        reselec=BASE_RESELEC+stats.get('reselec',0),
        resphys=BASE_RESPHYS+stats.get('resphys',0),
        rescold=BASE_RESCOLD+stats.get('rescold',0),
        resbleed=BASE_RESBLEED+stats.get('resbleed',0),
        respain=BASE_RESPAIN+stats.get('respain',0),
        resrust=BASE_RESRUST+stats.get('resrust',0),
        resrot=BASE_RESROT+stats.get('resrot',0),
        reswet=BASE_RESWET+stats.get('reswet',0),
        reslight=BASE_RESLIGHT+stats.get('reslight',0),
        ressound=BASE_RESSOUND+stats.get('ressound',0),
        spd=BASE_SPD+stats.get('spd',0),
        asp=BASE_ASP+stats.get('asp',0),
        msp=BASE_MSP+stats.get('msp',0),
        _str=(BASE_STR+stats.get('str',0))*MULT_ATT,
        _con=(BASE_CON+stats.get('con',0))*MULT_ATT,
        _int=(BASE_INT+stats.get('int',0))*MULT_ATT,
        _dex=(BASE_DEX+stats.get('dex',0))*MULT_ATT,
        _agi=(BASE_AGI+stats.get('agi',0))*MULT_ATT,
        _end=(BASE_END+stats.get('end',0))*MULT_ATT,
        atk=(BASE_ATK+stats.get('atk',0))*MULT_STATS,
        dmg=(BASE_DMG+stats.get('dmg',0))*MULT_STATS,
        dfn=(BASE_DFN+stats.get('dv',0))*MULT_STATS,
        arm=(BASE_ARM+stats.get('av',0))*MULT_STATS,
        pen=(BASE_PEN+stats.get('pen',0))*MULT_STATS,
        pro=(BASE_PRO+stats.get('pro',0))*MULT_STATS,
        bal=(BASE_BAL+stats.get('bal',0))*MULT_STATS,
        ctr=(BASE_CTR+stats.get('ctr',0))*MULT_STATS,
        gra=(BASE_GRA+stats.get('gra',0))*MULT_STATS,
        courage=BASE_COURAGE+stats.get('cou',0),
        scary=BASE_SCARY+stats.get('idn',0),
        beauty=BASE_BEAUTY+stats.get('bea',0)
        )
##    rollstats(stats, DEV=3) # TODO: test this function
    
    #create entity
    ent = rog.world().create_entity(
        body,
        stats,
        cmp.AI(ai.stateless), #temporary
        cmp.Name(name),
        cmp.Identify(idtype),
        cmp.Draw(_type, col, COL['deep']),
        cmp.Position(x, y),
        cmp.Actor(),
        cmp.Form(mat, 0),
        cmp.Creature(faction=FACT_MONSTERS),
        cmp.Inventory(money=money),
        cmp.Skills(),
        cmp.Meters(),
        cmp.Flags(),
        cmp.Mutable(),
        cmp.Targetable(), # so it can be targeted by the player
        )
    if sight:
        rog.world().add_component(ent, cmp.SenseSight())
    if hear:
        rog.world().add_component(ent, cmp.SenseHearing())
    for flag in flags:
        rog.make(ent, flag)
    if script: script(ent)
    return ent


# conversion functions #

def convertTo_corpse(ent) -> int:
    '''
        TODO: change it so you don't delete the entity when you kill a creature,
        instead just call this to convert it to a corpse
    '''
    world = rog.world()
    name = world.component_for_entity(ent, cmp.Name)
    draw = world.component_for_entity(ent, cmp.Draw)
##    form = world.component_for_entity(ent, cmp.Form)
    bstats = world.component_for_entity(ent, cmp.Stats)
    name.name = "corpse of {}".format(name.name)
    draw.char = "%"
    bstats.hpmax = max(1, bstats.mass)
    bstats.hp = bstats.hpmax
    rog.make(ent, DIRTY_STATS)
    return ent

def create_ashes(ent) -> int:
    '''
        attempt to create ashes from the remains of an entity
        does not delete the entity
    '''
    world = rog.world()
    stats = world.component_for_entity(ent, cmp.Stats)
    if stats.mass < 10: return -1
    mass = round(stats.mass * 0.1) # mass must always be an integer for actual entities (only displayed as a float in-game and in-data for ease)
    name = world.component_for_entity(ent, cmp.Name)
    pos = world.component_for_entity(ent, cmp.Position)
    ashes=world.create_entity(
        cmp.Name("ashes of {}".format(name.name)),
        cmp.Draw(T_DUST, COL['ltgray'],COL['deep']),
        cmp.Position(pos.x, pos.y),
        cmp.Form(mass, MAT_DUST, 0),
        cmp.BasisStats(resfire=100,resbio=100,reselec=100)
        )
    return ent

def create_steel_weapon(itemName, x, y) -> int:
    '''
        create a metal weapon and modify its values/name to resemble steel
    '''
    world=rog.world()
    # create the weapon
    weap=create_weapon(itemName, x, y)
    # name
    compo=world.component_for_entity(weap, cmp.Name)
    if "metal " in compo.name:
        compo.name = "steel {}".format(compo.name[6:])
    else:
        compo.name = "steel {}".format(compo.name)
    # value and mass
    stats=world.component_for_entity(weap, cmp.Stats)
    form=world.component_for_entity(weap, cmp.Form)
    if form.material==MAT_METAL:
        form.value = 1 + round(form.value * 5.1)
        stats.mass = round(stats.mass * 0.95)
    else:
        form.value = 1 + round(form.value * 2.5)
    # equipable stats
    compo=world.component_for_entity(weap, cmp.EquipableInHoldSlot)
    pen=compo.mods['pen']
    compo.mods['dmg'] = round(compo.mods['dmg'] * 1.25)
    compo.mods['pen'] = max(pen + 1, round(pen * 1.2))
    # stats
    compo=world.component_for_entity(weap, cmp.Stats)
    compo.hpmax=compo.hpmax*1.5
    compo.hp=compo.hpmax
    compo.resrust=compo.resrust + 50
    return weap
#


# bodies #

def create_body_humanoid(mass=75, height=175, female=False, bodyfat=0.1):
    '''
        create a generic humanoid body with everything a basic body needs
            *does not add any values to components -- inits default vals
        
        Parameters:
            int mass    : intended total body mass in KG
            int height  : height in centimeters
            bool female : is the creature female?
            
        Returns: tuple of (body_component_object, base_mass,)
            where base_mass is the mass of the body except for
              the blood, fat, and water (the mass of which is added
              on the fly to calculate the total mass of the body).
    '''
    mass = int(mass * MULT_MASS)
    fat = mass*bodyfat
    body = cmp.Body(
        BODYPLAN_HUMANOID,
        cmp.BPC_Torso(),
        parts={
            cmp.BPC_Heads : cmp.BPC_Heads(cmp.BPM_Head()),
            cmp.BPC_Arms  : cmp.BPC_Arms(cmp.BPM_Arm(), cmp.BPM_Arm()),
            cmp.BPC_Legs  : cmp.BPC_Legs(cmp.BPM_Leg(), cmp.BPM_Leg()),
            },
        height=int(height),
        blood=int(mass*0.07), # 7% of body mass is blood
        fat=fat, # total fat mass in the body (floating point -- precision doesn't matter)
        hydration=int(MULT_HYD*mass*0.6), # TOTAL BODY MASS OF WATER != how close you are to dehydrating. At 90% this capacity you die of dehydration.
        satiation=int(mass*50), # how many calories (not KiloCalories) you have available at maximum satiation w/o resorting to burning fat / muscle
        sleep=86400 # 24h * 60m * 60s
        )
    # set some default values for the body parts
    head = body.parts[cmp.BPC_Heads].heads[0]
    head.eyes.visualSystem.quality = BASE_SIGHT
    head.ears.auditorySystem.quality = BASE_HEARING

    # calculate the base mass stat (mass remaining w/o body fluids/fat)
    left = mass - body.bodyfat - body.bloodMax - body.hydrationMax//MULT_HYD
    
    return (body, left,)
# end def


##def _setGenericName(ent, name):
##    generic=name
##    
##    if "plastic " in generic:
##        generic = generic[8:]
##    elif "wooden " in generic:
##        generic = generic[7:]
##    elif "bone " in generic:
##        generic = generic[5:]
##    elif "stone " in generic:
##        generic = generic[6:]
##    elif "metal " in generic:
##        generic = generic[6:]
##    elif "glass " in generic:
##        generic = generic[6:]
##    elif "ceramic " in generic:
##        generic = generic[8:]
##    elif "graphene " in generic:
##        generic = generic[9:]
##    elif "iron " in generic:
##        generic = generic[5:]
##    elif "steel " in generic:
##        generic = generic[6:]
##    elif "aluminum " in generic:
##        generic = generic[9:]
##    elif "platinum " in generic:
##        generic = generic[9:]
##    elif "titanium " in generic:
##        generic = generic[9:]
##    elif "silver " in generic:
##        generic = generic[7:]
##    elif "copper " in generic:
##        generic = generic[7:]
##    elif "gold " in generic:
##        generic = generic[5:]
##    
##    rog.world().add_component(ent, cmp.Identify(generic))

# generic shape based on its identification type
def _setGenericShape(ent, idtype):
    shape = IDENTIFICATION[idtype][1]
    rog.world().component_for_entity(ent, cmp.Form).shape = shape
    
# generic components that can be applied depending on entity's data
def _setGenericData(ent, material=0) -> int:
    stats=rog.world().component_for_entity(ent, cmp.Stats)
    # fuel
    fuelValue = FUEL_MULT * MAT_FUEL[material]
    if fuelValue:
        rog.world().add_component(ent, cmp.Fuel(fuelValue))
    # resistances,
    if material==MAT_METAL:
        stats.resrust=0
        stats.arm=6
        stats.pro=18
    elif material==MAT_STONE:
        stats.arm=4
        stats.pro=6
    elif material==MAT_BONE:
        stats.arm=2
        stats.pro=6
    elif material==MAT_GLASS:
        stats.arm=6
        stats.pro=6
    elif material==MAT_CARBON:
        stats.arm=2
        stats.pro=24
    elif material==MAT_LEATHER:
        stats.arm=1
        stats.pro=1
    elif material==MAT_BLEATHER:
        stats.arm=1
        stats.pro=3
    elif material==MAT_WOOD:
        stats.resrot=0
        stats.resfire=0
        stats.arm=1
        stats.pro=6
    elif material==MAT_CLOTH:
        stats.resfire=0
    elif material==MAT_PAPER:
        stats.resfire=-500
    elif material==MAT_OIL:
        stats.resfire=-100
    return ent
            



# FLUIDS #

    #TODO: implement fluids. These are the old functions.

##def getData(self, stat):    #get a particular stat about the fluid
##    return FLUIDS[self.name].__dict__[stat]
##
##def clear(self):            #completely remove all fluids from the tile
##    self.dic={}
##    self.size=0
##
##def add(self, name, quantity=1):
##    newQuant = self.dic.get(name, 0) + quantity
##    self.dic.update({name : newQuant})
##    self.size += quantity
##    
##    '''floodFill = False
##    if self.size + quantity > MAX_FLUID_IN_TILE:
##        quantity = MAX_FLUID_IN_TILE - self.size
##        floodFill = True #partial floodfill / mixing
##        #how should the fluids behave when you "inject" a new fluid into a full lake of water, etc.?
##        #regular floodfill will not cut it
##        #maybe just replace the current fluid with the new fluid to keep it simple.
##        '''
##
##    '''if floodFill:
##        #do flood fill algo.
##        #this is going to also have to run a cellular automata to distribute different types of fluids
##        return'''
##
##def removeType(self, name, quantity=1):
##    if self.size > 0:
##        curQuant = self.dic.get(name, 0)
##        newQuant = max(0, curQuant - quantity)
##        diff = curQuant - newQuant
##        if not diff:     #no fluid of that type to remove
##            return
##        self.size -= diff
##        if newQuant != 0:
##            self.dic.update({name : newQuant})
##        else:
##            #we've run out of this type of fluid
##            self.dic.remove(name)






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

##OLDmonsterdata={ #bestiary
##    # Column names in more detail:
##    # Lo qi, Hi qi, Attack, Damage, Dodge, Armor, Speed, Move Speed, Attack Speed, Carrying Capacity, Mass, Gold.
##    
###Type,  Name,                   (Lo\ Hi\ At\Dm\Pen\DV\AV\Pro\Spd\Msp\Asp\FIR\BIO\ELC\SIGT\HEAR\ENC\KG\ $$\),FLAGS,script,
##''' TODO: REMOVE
##'@' : ('human',                 (2,  20, 0, 0, 0,  10,0, 0,  100,100,0,   20, 20, 20, 20, 80,  0,  65, 96, ),(),None,),
##'a' : ('abomination',           (16, 8,  -2,4, 0,  -8,2, 2,  100,90, 110, 50, 50, 25, 6,  0,   0,  80, 0,  ),(),None,),
##'b' : ('bug-eyed business guy', (20, 30, 2, 2, 3,  2, 0, 0,  150,120,100, 50, 50, 20, 30, 80,  20, 60, 96, ),(),None,),
##'B' : ('butcher',               (40, 20, 2, 5, 2,  -4,1, 2,  100,100,100, 60, 50, 50, 10, 80,  0,  130,48, ),(),None,),
##'L' : ('raving lunatic',        (12, 25, 2, 3, 2,  2, 0, 0,  100,100,100, 25, 15, 30, 10, 0,   0,  50, 0, ),(),None,), #BABBLES,
##'r' : ('ravaged',               (4,  1,  -4,1, 0,  -8,-1,0,  100,80, 70,   0,  0, 0,  10, 0,   0,  35, 0,  ),(),None,),
##'R' : ('orctepus',              (15, 5,  4, 2, 8, -12,0, 0,  100,80, 145,  0, 80, 0,  15, 0,   20, 100,0,  ),(),None,),
##'s' : ('slithera',              (6,  15, 6, 3, 1,  -4,0, 0,  100,33, 150,  0, 50, 5,  5,  0,   0,  30, 0, ),(),None,),
##'U' : ('obese scrupula',        (20, 2,  0, 6, 2, -16,3, 6,  100,50, 90,  20, 65, 60, 10, 0,   40, 140,48,  ),(),None,),
##'V' : ('ash vampire',           (30, 80, 2, 3, 2,  8, 0, 0,  100,120,100, 10, 75, 5,  5,  200, 0,  30, 192,  ),(),None,),
##'w' : ('dire wolf',             (12, 3,  12,5, 0,  8, 0, 1,  100,225,115, 15, 15, 15, 15, 0,   0,  50, 0,  ),(),None,),
##'W' : ('whipmaster',            (50, 10, 6, 5, 4,  4, 2, 4,  100,80, 100, 25, 60, 10, 15, 0,   10, 75, 192, ),(),None,),
##'z' : ('zombie',                (8,  1,  -6,4, 0, -12,-1,0,  50, 40, 100, 10, 25, 55, 5,  0,   0,  45, 0,  ),(),None,),
##''':(), # TODO: REMOVE

BESTIARY={
#Type, name,            KG, CM,  Material,  plan,  (FLAGS), script, ID, {Stat Dict},
'h':('human',           70, 175, MAT_FLESH, HUMAN, (), None, ID_HUMANOID,
    {}, ),
'a':('abomination',     140,140, MAT_FLESH, FLEGS, (), None, ID_4LEGBEAST,
    {'str':4,'end':-8,'dex':-12,'int':-8,'con':4,'agi':-8,'msp':20,'resbio':50,'sight':0.25,'hearing':0,},),
'd':('dog',             60, 60,  MAT_FLESH, FLEGS, (MEAN,), None, ID_4LEGBEAST, # wolf build; to create a dog, make a wolf and make it non mean, and dull its sight, -2 Str, half the mass.
    {'str':2,'end':-2,'dex':-12,'int':-6,'con':-4,'agi':8,'msp':40,'sight':1,'hearing':2,}, ),
'L':('raving lunatic',  70, 165, MAT_FLESH, HUMAN, (MEAN,), None, ID_HUMANOID,
    {'str':6,'end':6,'int':-6,'dex':-6,'sight':-60,'resbio':40,'reselec':60,}, ),
'r':('ravaged',         35, 150, MAT_FLESH, HUMAN, (), None, ID_HUMANOID,
    {'str':-4,'end':-6,'dex':-2,'int':-6,'con':-4,'agi':-6,'sight':0.34,'hearing':0,}, ),
'R':('orctepus',        100,140, MAT_FLESH, EARMS, (IMMUNEWATER,), None, ID_8ARMS,
    {'str':6,'end':-6,'dex':-4,'int':-2,'con':4,'agi':-2,'sight':0.75,'hearing':0,'pen':6,'msp':-40,'resfire':-40,'rescold':-40,'reselec':-40,'resbio':60,}, ),
'U':('obese scrupula',  190,190, MAT_FLESH, HUMAN, (), None, ID_HUMANOID,
    {'str':4,'end':-10,'dex':-6,'int':-4,'con':12,'agi':-10,'sight':0.5,'hearing':0,}, ),
'W':('whipmaster',      85, 220, MAT_FLESH, HUMAN, (), _whipmaster, ID_HUMANOID,
    {'str':2,'end':-4,'dex':2,'int':-10,'con':6,'agi':4,'sight':1,'hearing':1,}, ),
'z':('zomb',            50, 160, MAT_FLESH, HUMAN, (), None, ID_HUMANOID,
    {'str':4,'end':-8,'dex':-4,'int':-10,'con':-8,'agi':-10,'sight':1,'hearing':0,}, ),
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



FOOD = {
# Columns:
#   $$$         cost
#   KG          mass
#   Mat         material
#   script      script to run to initialize values for the food item
#--Name-------------------$$$,  KG,   Mat,  script
"Corpse Button"         :(1,    0.03, FLSH, _food_morsel_bloody_nasty,),
"Hack Leaf"             :(1,    0.02, WOOD, _food_morsel_bitter,),
"Juniper Berry"         :(3,    0.01, FLSH, _food_morsel_sweet,),
"Coke Nut"              :(12,   0.02, WOOD, _food_cokenut,),
"Silly Fruit"           :(8,    0.04, FLSH, _food_sillyfruit,),
"Mole Rat Meat"         :(10,   0.15, FLSH, _food_ration_savory,),
"Dwarf Giant Cap"       :(25,   0.05, FLSH, _food_ration_savory,),
"Eel Meat"              :(20,   0.50, FLSH, _food_meal_savory,),
"Human Meat"            :(40,   1.00, FLSH, _food_meal_savory,),
"Infant Meat"           :(80,   0.50, FLSH, _food_meal_savory,),
"Giant Cap"             :(100,  0.35, FLSH, _food_meal_savory,),
"MRE"                   :(60,   1.0,  FLSH, _food_meal_gamble,),
    }

STUFF={
    
##extrastuff={ TODO: ADD THIS INTO STUFF
##"grinding stone"    :(500, 95.0,200, STON,(-20,5,  0,  0, 0, 0, 0,  120,),None,),
##"metal anvil, small":(580,  10.0,4000,METL,100,12,(-10,8,  0,  0, 0, 0, -33,60,),None,),
##"metal anvil"       :(2640, 50.0,9999,METL,500,12,(-15,16, 0,  0, 0, 0, -66,70,),None,),
##"metal anvil, large":(10300,200,36999,METL,2000,12,(-20,8,  0,  0, 0, 0, -99,80,),None,),
##
##    }
    # REMOVED: solid, pushable / push : this is now handled by scripts
    # misc mats / mixes of materials / complex objects / variable material objects
# name              :(type,material,value,color, HP, kg, script,)
"tinder"            :(T_MISC,WOOD,  0,   'accent',1,0.01,None,),
"solar panel"       :(T_DEVICE,GLAS,500, 'trueblue',40,2.0,_solarPanel,),
"skeleton"          :(T_CORPSE,BONE,100, 'bone',1,8.0,_skeleton,),
    # plastic
"plastic campfire"  :(T_FIREPIT,PLAS,10,'accent',800,6.5,_campfire,),
"lighter"           :(T_DEVICE,PLAS,60,  'random',2, 0.1,_lighter,),
"geiger counter"    :(T_DEVICE,PLAS,450, 'yellow',5,0.5, _dosimeter,),
    # wood
"foliage"           :(T_FOLIAGE,WOOD,1, 'green', 50,0.75,_foliage,),
"wooden campfire"   :(T_FIREPIT,WOOD,50,'brown', 1600,7.5,_campfire,),
"wooden crate"      :(T_BOX,  WOOD, 10,  'brown',200,50,  _boxOfItems1,),
"torch"             :(T_LIGHT,WOOD, 1,  'brown',20,1.1, _torch,),#torches need a component that makes them be able to burn taking damage on some separate health pool until that runs out at which point the thing actually catches "fire" and cannot be held any longer. Thus torches have low HP.
"torch, large"      :(T_LIGHT,WOOD, 5,  'brown',200,1.5,_torchLarge,),# torches are much heavier when you craft them yourself (unless you use a bone and oil instead of resin)
    # stone
"stone grave, large":(T_GRAVE,STON, 15, 'gray',300,300,_grave,),
    # metal
"fire extinguisher" :(T_DEVICE,METL,680, 'red',  8,8, _extinguisher,),
"metal safe, large" :(T_BOX,  METL, 1500,'metal', 2000,420,_safe,),
"metal still, large":(T_STILL,METL, 200,'metal', 5, 100,_still,),
"metal pot, large"  :(T_POT,  METL, 120,'metal', 800,100,_pot,),
    # flesh
"moss clump"        :(T_FOLIAGE,FLSH,1,'graygreen',10,0.35,None,),
"meat flower"       :(T_FOOD, FLSH, 3,   'pink', 10,2.5, _meatFlower,),
    # clay
"clay pot"          :(T_MISC, CLAY, 20, 'scarlet',1, 5, _clayPot,),
"clay pot, large"   :(T_POT,  CLAY, 250,'scarlet',1, 100, _clayPotLarge,),
    # ceramic
"ceramic pot"       :(T_MISC, CERA, 1,  'accent',1, 3, _ceramicPot,),
"ceramic pot, large":(T_POT,  CERA, 30, 'accent',10,75, _ceramicPotLarge,),
    # cloth
"towel"             :(T_TOWEL,CLTH, 50, 'accent',50,0.8,_towel,),
    # dust
"black powder"      :(T_DUST, DUST, 1,  'dkgray', 1, 0.02,_blackPowder,),
"gunpowder bag"     :(T_DUST, DUST, 5,  'silver', 1, 0.01,_gunpowder,),
"gunpowder grain"   :(T_DUST, DUST, 0,  'silver', 1, 0,   None,),#150 in one gunpowder bag
#THG.CLOAK
#THG.GENERATOR
##THG.TURRET      :("turret",           T_TURRET,METL,300, 'gray', 80, 55, False,False,_turret,),
##"foliage, dead"     :(T_FOLIAGE,WOOD,1, 'brown', 1, 0.05,False,_foliageDead,),
    }

FLUIDS = {
#attributes:
#   d       : density
#   v       : viscosity
#   kg      : mass
#   flamm   : flammable?
#   snuff   : snuffs out fires?
#  ID       : (type,   name,      color,          d,    v,    kg,  flamm,snuff,touch,quaff,
FL_SMOKE    : (T_GAS,  "smoke",   COL['white'],   0.05, 0.01, 0.01,False,False,None, _cough,),
FL_WATER    : (T_FLUID,"water",   COL['blue'],    1,    1,    0.1, False,True, _wet, _hydrate,),
FL_BLOOD    : (T_FLUID,"blood",   COL['red'],     1.1,  2,    0.12,False,True, _bloody,_quaffBlood,),
FL_ACID     : (T_FLUID,"acid",    COL['green'],   1.21, 0.6,  0.2, False,False,_acid,_quaffAcid,),
FL_STRONGACID:(T_FLUID,"strong acid",COL['bio'],  1.3,  0.9,  0.2, False,False,_strongAcid,_quaffStrongAcid,),
FL_OIL      : (T_FLUID,"oil",  COL['truepurple'], 0.9,  3,    0.3, True,False, _oily, _sick,),
FL_ALCOHOL  : (T_FLUID,"moonshine",COL['gold'],   1.2,  0.8,  0.15,True,False, _wet, _drunk,),
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
FL_STRONGACID:"acidic",
FL_OIL      : "oily",
FL_ALCOHOL  : "alcoholic",
    }



    # weapons #


AMMUNITION={
# Attributes:
#   type        ammo type
#   $$$, KG     value, mass
#   n           number shots
#   Acc, Atk, Dmg, Asp      Range, Attack, Damage, Attack Speed
    
     # arrows
# name                  : type,  $$$, KG, n, (Acc,Atk,Dmg,Asp,),script
##"hollow arrow"          :(A_ARRO,1,  0.02,1, (-8, 2,  0,  10,), None,),
##"wooden arrow"          :(A_ARRO,1,  0.03,1, (-4, 4,  1,  0,), None,),
##"fletched arrow"        :(A_ARRO,2,  0.03,1, (4,  8,  1,  0,), None,),
##"poisoned arrow"        :(A_ARRO,5,  0.03,1, (0,  6,  2,  0,), _poisonArrow,),
##"metal arrow"           :(A_ARRO,3,  0.04,1, (0,  6,  3,  0,), None,),
##"flight arrow"          :(A_ARRO,4,  0.05,1, (15, 5,  1,  0,), None,),
##"war arrow"             :(A_ARRO,6,  0.06,1, (10, 10, 5,  0,), None,),
##"obsidian arrow"        :(A_ARRO,8,  0.03,1, (2,  12, 6,  0,), None,),

    #TODO: add ceramic bullets, plastic, rubber bullets, etc.

    # TODO: convert all KG measurements to g (multiply by 1000)
        # Just do this when you create the objects.

    # TODO: when you create ammo, set its HP based on what type of ammo it is.

    # Range represents a multiplier modifier
    
    # stone
# name                  : type,  $$$, KG,  n,(Rng%,Acc,Dmg,Pen,Asp,),script
"percussion cap"        :(A_PCAP,1,  0.005,1,(0,   -99,-99,-99,30,),_percussionCap,),# required to shoot caplock guns. Can be fired by itself to make a loud noise/ frighten foes. NOTE: Should this be not in AMMO?
"stone cannonball"      :(A_BALL,3,  0.4,  1,(0.6, -5, -6, -6, 0,),_sCannonBall,),
"metal cannonball"      :(A_BALL,11, 0.2,  1,(0.9, 0,  0,  0,  0,),_mCannonBall,),
"stone bullet"          :(A_BULL,1,  0.05, 1,(0.7, -3, -2, -4, 0,),_sBullet,), # 12 gauge
"metal bullet"          :(A_BULL,6,  0.05, 1,(0.9, 0,  0,  0,  0,),_mBullet,),
"Minni ball"            :(A_BULL,7,  0.05, 1,(1.2, 5,  2,  2,  0,),_minnieBall,),
"cartridge, metal bullet":(A_PC, 4,  0.11, 1,(1.0, 0,  0,  0,  0,),_paperCartridge,),
".22 LR cartridge"      :(A_22LR,1,  0.003,1,(1.0, 0,  0,  0,  0,),_mCartridge,),# gunpowder could be expensive because it has to be imported, likewise casings are not cheap being hard to manfucature, so bullets are expensive shit in this world.
"9mm cartridge"         :(A_9MM, 1,  0.008,1,(1.0, 0,  0,  0,  0,),_mCartridge,),#.38 Spl 
".357 magnum cartridge" :(A_357, 3,  0.01, 1,(1.33,4,  5,  5,  -15,),_mCartridge,),#can also fire 9mm AKA .38Spl rounds
"10mm cartridge"        :(A_10MM,2,  0.017,1,(1.0, 0,  0,  0,  0,),_mCartridge,),
".45 ACP cartridge"     :(A_45,  2,  0.015,1,(1.0, 0,  0,  0,  0,),_mCartridge,),
".44 Spl cartridge"     :(A_44S, 5,  0.022,1,(1.5, 0,  0,  0,  0,),_mCartridge,),#can also fire 9mm AKA .38Spl rounds
".44 magnum cartridge"  :(A_44M, 7,  0.025,1,(2.0, 6,  3,  6,  -36,),_mCartridge,),#can also fire 9mm AKA .38Spl rounds
"5.56mm cartridge"      :(A_556, 2,  0.012,1,(1.0, 0,  0,  0,  0,),_mCartridge,),#.223 is similar. bullet itself is only 4g
".30 carbine cartridge" :(A_30,  2,  0.013,1,(1.0, 0,  0,  0,  0,),_mCartridge,),#7.62x33mm; M1 carbine
"7.62x39mm cartridge"   :(A_762, 3,  0.017,1,(1.5, 0,  0,  0,  0,),_mCartridge,),#7.62x39mm
".308 cartridge"        :(A_308, 4,  0.027,1,(2.0, 0,  0,  0,  0,),_mCartridge,),#7.62x51mm
".30-06 cartridge"      :(A_3006,5,  0.026,1,(2.5, 4,  2,  4,  -9,),_mCartridge,),#7.62x63mm
".300 magnum cartridge" :(A_300, 9,  0.031,1,(3.0, 6,  6,  8,  -24,),_mCartridge,),#7.62x67mm
".50 BMG cartridge"     :(A_50,  25, 0.115,1,(0,   0,  0,  0,  0,),_mCartridgeLarge,),
"12ga rubber shell"     :(A_12GA,1,  0.15, 5,(0.25,-8, -8, -6, -9,),_shell,),
"12ga rubber slug"      :(A_12GA,1,  0.15, 1,(0.6, -6, -12,-4, -9,),_shell,),
"12ga plastic shell"    :(A_12GA,1,  0.15, 5,(0.3, -8, -8, -6, -9,),_shell,),
"12ga plastic slug"     :(A_12GA,1,  0.15, 1,(0.75,-6, -12,-4, -9,),_shell,),
"12ga metal shell"      :(A_12GA,3,  0.08, 5,(0.67,-6, 7,  -3, 0,),_shell,),
"12ga metal slug"       :(A_12GA,3,  0.1,  1,(1,   0,  0,  0,  0,),_shell,),#slugs do less OVERALL damage, but the damage is spread out over 5 or so shots for the shells, meaning each individual shot does very little damage. Slugs also have better penetration.
"10ga metal shell"      :(A_10GA,3,  0.12, 5,(0.6, -8, 8,  -4, 0,),_shell,),
"10ga metal slug"       :(A_10GA,3,  0.15, 1,(1,   0,  0,  0,  0,),_shell,),

##"small stone bullet"    :(A_SB,  2,  0.1, 1, (2,  -8, 1,  3,  0,),_sBulletSmall,),# stone bullets are difficult to manufacture, especially small ones.
##"small metal bullet"    :(A_SB,  3,  0.05,1, (6,  -5, 3,  6,  0,),_mBulletSmall,),
     # cartridges
# name                  : type,  $$$, KG, n, (Rng,Acc,Dmg,Pen,Asp,),script
##"pistol cartridge"      :(A_CART,6,  0.02,1, (0,  2,  4,  0,), None,),
##"magnum cartridge"      :(A_CART,12, 0.03,1, (-2, 5,  7,  -33,), None,),
##"rifle cartridge"       :(A_CART,16, 0.04,1, (8,  8,  10, -15,), None,),
##"hollow-point cartridge":(A_CART,15, 0.03,1, (-5, -4, 12, -15,), None,),
##"incendiary cartridge"  :(A_CART,36, 0.04,1, (-2, 8,  16, -33,), _incendiary),
    }

GUNMODS={ # TODO: make all gun stats represent fully unmodded version -- 1 mag capacity unless has a built-in mag or revolver chamber.
##        Parameters:
##AMMO    ammo type (AMMO_ const)
##$$$$    cost
##KG      mass
##Enc     added encumberance when modded on. Multiplied by mass of the whole unit.
##Dur     max HP
##MAT     material
##type    mod type (IMOD_ const)
##mods    stat mods (and other modifiers?)

# TODO: when you modify a gun w/ a mod, convert special stats
    # (e.g. 'nshots') into modifications of the Shootable component
    # (how should we handle this???)
    # In other words, not all modifications are mods of the Stats compo.
    # IDEA: use base_ stats in Shootable component that represent unmodded
    # stats.
# magazines                     :(type, AMMO,  $$$, KG,   Enc,Dur,MAT, {mods}
"magazine, .22 LR, micro"       :(M_MAG,A_22LR,4,   0.05, 0.2,80, METL,{'nshots':10}),
"magazine, .22 LR, small"       :(M_MAG,A_22LR,6,   0.05, 0.3,80, METL,{'nshots':15}),
"magazine, .22 LR"              :(M_MAG,A_22LR,10,  0.08, 0.5,60, METL,{'nshots':25}),
"magazine, .22 LR, large"       :(M_MAG,A_22LR,15,  0.1,  0.6,50, METL,{'nshots':30}),
"magazine, .22 LR, drum"        :(M_MAG,A_22LR,50,  0.3,  2,  20, METL,{'nshots':75}),
"magazine, 9mm, small"          :(M_MAG,A_9MM, 25,  0.07, 0.2,100,METL,{'nshots':12}),
"magazine, 9mm"                 :(M_MAG,A_9MM, 30,  0.1,  0.4,75, METL,{'nshots':15}),
"magazine, 9mm, large"          :(M_MAG,A_9MM, 50,  0.2,  0.6,50, METL,{'nshots':30}),
"magazine, 9mm, drum"           :(M_MAG,A_9MM, 150, 0.5,  2,  20, METL,{'nshots':100}),
"magazine, 10mm, small"         :(M_MAG,A_10MM,35,  0.14, 0.2,120,METL,{'nshots':9}),
"magazine, 10mm"                :(M_MAG,A_10MM,40,  0.18, 0.3,80, METL,{'nshots':15}),
"magazine, 10mm, large"         :(M_MAG,A_10MM,60,  0.26, 0.6,60, METL,{'nshots':30}),
"magazine, 10mm, drum"          :(M_MAG,A_10MM,180, 0.6,  2,  20, METL,{'nshots':100}),
"magazine, .45 ACP, micro"      :(M_MAG,A_45,  45,  0.1,  0.2,150,METL,{'nshots':7}),
"magazine, .45 ACP, small"      :(M_MAG,A_45,  40,  0.15, 0.3,120,METL,{'nshots':12}),
"magazine, .45 ACP"             :(M_MAG,A_45,  60,  0.2,  0.6,90, METL,{'nshots':30}),
"magazine, .45 ACP, large"      :(M_MAG,A_45,  80,  0.3,  1.0,45, METL,{'nshots':50}),
"magazine, .45 ACP, drum"       :(M_MAG,A_45,  220, 0.66, 2.5,25, METL,{'nshots':100}),
"magazine, .30 carbine, small"  :(M_MAG,A_30,  45,  0.15, 0.3,150,METL,{'nshots':10}),
"magazine, .30 carbine"         :(M_MAG,A_30,  65,  0.2,  0.5,100,METL,{'nshots':15}),
"magazine, .30 carbine, large"  :(M_MAG,A_30,  110, 0.3,  0.7,50, METL,{'nshots':30}),
"magazine, 5.56x45mm, small"    :(M_MAG,A_556, 40,  0.08, 0.1,150,METL,{'nshots':5}),
"magazine, 5.56x45mm"           :(M_MAG,A_556, 60,  0.17, 0.4,100,METL,{'nshots':20}),
"magazine, 5.56x45mm, large"    :(M_MAG,A_556, 95,  0.3,  0.7,50, METL,{'nshots':35}),
"magazine, 5.56x45mm, drum"     :(M_MAG,A_556, 245, 0.8,  2,  30, METL,{'nshots':100}),
"magazine, 7.62x39mm, small"    :(M_MAG,A_762, 35,  0.1,  0.3,180,METL,{'nshots':15}),
"magazine, 7.62x39mm"           :(M_MAG,A_762, 70,  0.2,  0.5,120,METL,{'nshots':25}),
"magazine, 7.62x39mm, large"    :(M_MAG,A_762, 85,  0.25, 0.6,60, METL,{'nshots':30}),
"magazine, 7.62x39mm, drum"     :(M_MAG,A_762, 260, 0.9,  2,  35, METL,{'nshots':100}),
"magazine, .308, small"         :(M_MAG,A_308, 45,  0.06, 0.3,200,METL,{'nshots':4}),
"magazine, .308"                :(M_MAG,A_308, 80,  0.1,  0.5,130,METL,{'nshots':8}),
"magazine, .308, large"         :(M_MAG,A_308, 140, 0.16, 0.7,80, METL,{'nshots':16}),
"magazine, .30-06, small"       :(M_MAG,A_3006,50,  0.09, 0.3,220,METL,{'nshots':4}),
"magazine, .30-06"              :(M_MAG,A_3006,75,  0.12, 0.5,150,METL,{'nshots':6}),
"magazine, .30-06, large"       :(M_MAG,A_3006,150, 0.15, 0.7,100,METL,{'nshots':12}),
##"magazine, .300 magnum, small"  :
##"magazine, .300 magnum"         :
##"magazine, .300 magnum, large"  :
"magazine, .50 BMG, small"      :(M_MAG,A_50,  260, 0.25, 0.3,300,METL,{'nshots':4}),
"magazine, .50 BMG"             :(M_MAG,A_50,  320, 0.35, 0.6,200,METL,{'nshots':6}),
"magazine, .50 BMG, large"      :(M_MAG,A_50,  395, 0.5,  1,  100,METL,{'nshots':9}),
# scopes                        :(type, AMMO,  $$$, KG,   Enc,Dur,MAT, {mods}
"handgun scope, small"          :(M_PSC,None,  395, 0.3,  0.2,20, METL,{'sights':4,}),#scopes only apply their Atk bonus when you aim at an enemy that is sufficiently far away depending on the weapon type. So at melee range, scopes don't help at all.
"handgun scope"                 :(M_PSC,None,  525, 0.6,  0.4,15, METL,{'sights':8,}),
"rifle scope, small"            :(M_RSC,None,  510, 0.7,  0.6,15, METL,{'sights':4,}),
"rifle scope"                   :(M_RSC,None,  665, 1.1,  0.8,10, METL,{'sights':8,}),
"rifle scope, large"            :(M_RSC,None,  880, 1.5,  1,  5,  METL,{'sights':12,}),
# straps                        :(type, AMMO,  $$$, KG,   Enc,Dur,MAT, {mods}
"leather gun strap"             :(M_STR,None,  8,   0.2,  0,  20, LETH,{'enc':0.9,}),#enc multiplier
# stocks                        :(type, AMMO,  $$$, KG,   Enc,Dur,MAT, {mods}
"metal folding stock"           :(M_STO,None,  60,  0.6,  0.5,120,METL,{'atk':2,}),
"wooden stock"                  :(M_STO,None,  8,   0.8,  1,  80, WOOD,{'atk':3,}),
# bipods                        :(type, AMMO,  $$$, KG,   Enc,Dur,MAT, {mods}
"metal folding bipod"           :(M_BIP,None,  90,  0.55, 0.4,160,METL,{'prone':4,}),
# lights                        :(type, AMMO,  $$$, KG,   Enc,Dur,MAT, {mods}
"metal gun flashlight"          :(M_FLA,None,  22,  0.07, 0.1,30, METL,{}),#light is applied differently: adds a DirectedLight component; it automatically updates to face the direction of the wielder b/c of being a Child of the wielder.
# suppressors                   :(type, AMMO,  $$$, KG,   Enc,Dur,MAT, {mods}
"metal suppressor"              :(M_SUP,None,  625, 0.25, 0.2,75, METL,{'noise':0.2,}),
    }

RANGEDWEAPONS={
    # NOTE: Reload Time is based on the ammo type; reloading the magazine is handled differently (must eject the magazine and reload it, then put the magazine in the gun)
    # ARGUMENTS:
    #   Cp : ammo capacity
    #   Rt : reload time
    #   n : number of projectiles per shot
    #   ja : jam chance in 1/100ths of a percent (100 == 1%, 10000 == 100%)
    #   min, max : minimum / maximum range you can shoot without penalties
    #   accuracy, damage, penetration, Defense, Attack Spd, Move Spd,
    #   Enc: encumberance multiplier (* mass of the item)
    #   For: force multiplier when shooting (* mass of the projectile)

# caplock guns          :(AMMO,  $$$$, KG,  Dur,MAT, St,Dx,(Cp,n,Rt,  jam,Min,Max,Ac,Dm,Pe,DV, Asp,Enc,For,),TYPE,script,ID,
"caplock pistol"        :(A_BULL,90,   1.4, 60, METL,8, 4, (1, 1,900, 900,1,  6,  0, 6, 3, 0,  -18,2,  100,),SKL_CANNONS,_caplockPistol,ID_PISTOL,),
"caplock musketoon"     :(A_BULL,235,  3.8, 120,WOOD,12,3, (1, 1,1000,750,2,  14, 2, 11,4, -2, -39,6,  200,),SKL_CANNONS,_musketoon,ID_MUSKET,),
"caplock musket"        :(A_BULL,325,  5.15,180,WOOD,16,3, (1, 1,1100,600,3,  25, 4, 16,5, -4, -60,9,  400,),SKL_CANNONS,_musket,ID_MUSKET,),
"caplock arquebus"      :(A_BULL,450,  6.5, 240,WOOD,20,3, (1, 1,1200,500,4,  36, 5, 22,6, -6, -75,10, 800,),SKL_CANNONS,_musket,ID_MUSKET,),
# shotguns              :(AMMO,  $$$$, KG,  Dur,MAT, St,Dx,(Cp,n,Rt, jam,Min,Max,Ac,Dm,Pe,DV, Asp,Enc,For,),TYPE,script,ID,
"12ga pipegun"          :(A_12GA,85,   1.75,65, METL,14,1, (1, 1,300,500,1,  6, -6, 8, 0, -1, -36,5,  200,),SKL_SHOTGUNS,_pipegun,ID_PIPE,),#one of the shittiest guns imagineable.
"12ga shotgun"          :(A_12GA,450,  3.25,275,WOOD,12,2, (1, 1,100,50, 1,  16, 8, 18,6, -2, -24,6,  200,),SKL_SHOTGUNS,_12GAshotgun,ID_SHOTGUN,),# all single-capacity shotguns can be made to be double-barrel, adds +12% mass, +10% Enc, and +1 Capacity
"12ga combat shotgun"   :(A_12GA,6500, 3.45,750,METL,10,3, (7, 1,100,1,  2,  30, 10,24,9, -2, -15,4,  500,),SKL_SHOTGUNS,_combatShotgun,ID_SHOTGUN,),
"10ga shotgun"          :(A_10GA,520,  4.2, 350,WOOD,15,2, (1, 1,110,25, 1,  28, 7, 22,5, -3, -36,8,  350,),SKL_SHOTGUNS,_10GAshotgun,ID_SHOTGUN,),
"8ga shotgun"           :(A_8GA, 640,  5.5, 375,WOOD,18,2, (1, 1,120,12, 2,  26, 6, 26,4, -4, -48,9,  600,),SKL_SHOTGUNS,_8GAshotgun,ID_SHOTGUN,),
"6ga shotgun"           :(A_6GA, 745,  7.1, 400,WOOD,22,2, (1, 1,130,6,  2,  24, 5, 30,3, -6, -60,10, 1000,),SKL_SHOTGUNS,_6GAshotgun,ID_SHOTGUN,),
"6ga riot shotgun"      :(A_6GA, 675,  4.6, 320,PLAS,14,3, (7, 1,130,250,1,  22, 2, 24,2, -3, -45,6,  750,),SKL_SHOTGUNS,_10GAshotgun,ID_SHOTGUN,),# TODO: custom script
"4ga shotgun"           :(A_4GA, 850,  8.6, 425,WOOD,26,2, (1, 1,140,3,  3,  22, 4, 35,2, -8, -72,11, 1600,),SKL_SHOTGUNS,_4GAshotgun,ID_SHOTGUN,),
"3ga shotgun"           :(A_3GA, 980,  10.1,450,WOOD,31,2, (1, 1,150,2,  4,  20, 3, 40,1, -10,-84,12, 2400,),SKL_SHOTGUNS,_3GAshotgun,ID_SHOTGUN,),
"2ga shotgun"           :(A_2GA, 1100, 12.0,475,WOOD,36,2, (1, 1,160,1,  5,  18, 2, 50,0, -12,-96,13, 4000,),SKL_SHOTGUNS,_2GAshotgun,ID_SHOTGUN,),
    # pistols and revolvers (9mm, .45ACP, 10mm, .357 magnum, 22LR)
# name                  :(AMMO,  $$$$, KG,  Dur,MAT, St,Dx,(Cp,n,Rt, jam,Min,Max,Ac,Dm,Pe,DV, Asp,Enc,For,),TYPE,script,ID,
"pea shooter"           :(A_22LR,90,   0.8, 60, METL,1, 5, (1, 1,100,950,1,  8,  6, 1, 6, 0,  -30,2,  10,),SKL_PISTOLS,_pistolSmall,ID_PISTOL,),# double-barrel is a mod, adds .1KG and +1 Capacity
"derringer"             :(A_22LR,135,  0.7, 90, METL,2, 7, (1, 1,100,300,1,  12, 4, 2, 4, 0,  0,  1.5,20,),SKL_PISTOLS,_pistolSmall,ID_PISTOL,),# double-barrel is a mod, adds .1KG and +1 Capacity
"9mm revolver"          :(A_9MM, 740,  1.15,630,METL,10,8, (6, 1,100,200,1,  24, 6, 3, 12,0,  15, 2,  200,),SKL_PISTOLS,_pistol,ID_PISTOL,),#can use 9mm ammo only; 357 magnum revolver can use .357 OR 9mm ammo.
"9mm handgun"           :(A_9MM, 3750, 0.9, 520,METL,4, 5, (1, 1,100,50, 1,  46, 9, 4, 14,0,  45, 2,  100,),SKL_PISTOLS,_pistolSmall,ID_PISTOL,),
".357 magnum revolver"  :(A_357, 2075, 1.25,700,METL,13,7, (6, 1,100,100,1,  24, 4, 3, 11,0,  9,  2,  400,),SKL_PISTOLS,_pistol,ID_PISTOL,),
"10mm handgun"          :(A_10MM,4475, 1.2, 560,METL,6, 5, (1, 1,100,20, 1,  42, 8, 5, 13,0,  36, 2,  100,),SKL_PISTOLS,_pistol,ID_PISTOL,),
"plastic liberator"     :(A_45,  9,    0.5, 8,  PLAS,4, 4, (1, 1,200,999,1,  10, -2,0, 2, 0,  -12,2,  33,),SKL_PISTOLS,_pLiberator,ID_PISTOL,),
"metal liberator"       :(A_45,  95,   0.5, 50, METL,5, 4, (1, 1,200,666,1,  20, 1, 2, 5, 0,  -6, 2,  50,),SKL_PISTOLS,_mLiberator,ID_PISTOL,),
"autogun"               :(A_45,  3100, 1.1, 300,METL,4, 6, (1, 1,100,10, 1,  36, 4, 5, 10,0,  15, 2,  200,),SKL_PISTOLS,_pistol,ID_PISTOL,),
"cig sawyer"            :(A_45,  8750, 1.0, 420,METL,3, 6, (1, 1,100,10, 1,  50, 7, 6, 12,0,  24, 2,  150,),SKL_PISTOLS,_pistolSmall,ID_PISTOL,),
    # SMGs and machine pistols (9mm, 10mm, .45ACP)
# name                  :(AMMO,  $$$$, KG,  Dur,MAT, St,Dx,(Cp,n,Rt, jam,Min,Max,Ac,Dm,Pe,DV, Asp,Enc,For,),TYPE,script,ID,
"mech-9"                :(A_9MM, 260,  2.9, 90, METL,7, 10,(1, 3,100,450,1,  15,-2, 1, 6, -1, -6, 2,  30,),SKL_SMGS,_smg,ID_PISTOL,),#mac-10. Moddable w/ suppressor # made of stamped sheet metal.
"machine pistol"        :(A_9MM, 11200,0.95,560,METL,8, 12,(1, 4,100,50, 1,  24, 1, 3, 10,0,  -6, 2,  50,),SKL_SMGS,_pistolSmall,ID_PISTOL,),#beretta. Moddable w/ stock, suppressor
"UMP"                   :(A_9MM, 12960,1.7, 540,METL,5, 8, (1, 3,100,10, 1,  36, 5, 4, 13,-1, 0,  3,  100,),SKL_SMGS,_smgSmall,ID_SMG,),#moddable w/ scope, strap, laser, flashlight, suppressor
"10mm SMG"              :(A_10MM,18850,2.2, 520,METL,6, 5, (1, 3,100,20, 1,  30, 3, 5, 12,-1, 0,  4,  100,),SKL_SMGS,_smgSmall,ID_SMG,),#moddable w/ scope, strap, laser, flashlight, suppressor
"grease gun"            :(A_45,  450,  3.3, 120,METL,8, 5, (1, 3,100,300,1,  18, 0, 3, 5, -2, -9, 4,  200,),SKL_SMGS,_smg,ID_SMG,),#MODABLE TO SHOOT 9MM # made of stamped sheet metal. Named so b/c it looks like a mechanic's grease gun.
"tommy gun"             :(A_45,  1150, 4.0, 275,METL,10,5, (1, 5,100,150,1,  22, 4, 4, 7, -3, -9, 5,  250,),SKL_SMGS,_smgLarge,ID_SMG,),
"uzi"                   :(A_45,  13650,1.6, 440,METL,7, 10,(1, 3,100,20, 1,  28, 2, 6, 9, -1, 0,  2,  150,),SKL_SMGS,_smgSmall,ID_SMG,),#moddable w/ stock, laser, flashlight, suppressor, 
    # rifles, carbines, semi-auto and burst / full auto (22LR, 5.56x39mm, .30 carbine, .308, .30-06)
# name                  :(AMMO,  $$$$, KG,  Dur,MAT, St,Dx,(Cp,n,Rt, jam,Min,Max,Ac,Dm,Pe,DV, Asp,Enc,For,),TYPE,script,ID,
"pidgeon plinker"       :(A_22LR,240,  2.3, 110,WOOD,3, 3, (1, 1,100,50, 3,  50, 8, 3, 10,-1, -9, 5,  5,),SKL_RIFLES,_rifleSmall,ID_RIFLE,),#moddable w/ scope, strap, suppressor
"autocarb"              :(A_22LR,645,  2.6, 180,PLAS,4, 4, (1, 5,100,350,2,  30, 2, 2, 6, -1, -15,6,  5,),SKL_RIFLES,_autocarb,ID_RIFLE,),#integrally suppressed, not highly moddable
"storm rifle"           :(A_9MM, 1950, 2.75,110,METL,3, 3, (1, 1,100,50, 2,  55, 10,4, 20,-2, 30, 5,  30,),SKL_RIFLES,_rifleSmall,ID_RIFLE,),#ambidextrous; can also come chambered in 10mm or .45ACP
"flemington rifle"      :(A_556, 1320, 3.8, 500,WOOD,16,3, (1, 1,100,10, 4,  140,14,10,24,-3, -21,11, 200,),SKL_RIFLES,_rifleLarge,ID_RIFLE,),#moddable with scope, bayonet, 
"service rifle"         :(A_556, 4300, 3.1, 760,METL,10,5, (1, 1,100,1,  3,  120,12,12,22,-2, 15, 7,  30,),SKL_RIFLES,_rifle,ID_RIFLE,),#moddable with scope, suppressor, strap, lasers, flashlights, bayonet, bipod, 
"assault rifle"         :(A_556, 1480, 2.9, 425,METL,14,4, (1, 3,100,100,3,  50, 6, 7, 18,-2, -15,9,  30,),SKL_RIFLES,_rifle,ID_AUTORIFLE,),#moddable with scope, suppressor, strap, lasers, flashlights,
"bullpup rifle"         :(A_556, 3650, 3.5, 360,METL,7, 5, (1, 3,100,10, 2,  65, 6, 9, 20,-2, 6,  6,  30,),SKL_RIFLES,_rifleSmall,ID_AUTORIFLE,),#ambidextrous; modable with a scope, suppresor, strap,  lasers, flashlights, 
"battle rifle"          :(A_556, 7450, 3.3, 550,METL,12,4, (1, 4,100,10, 3,  75, 8, 12,24,-2, 0,  9,  30,),SKL_RIFLES,_rifle,ID_AUTORIFLE,),#m16 moddable with most things
"paratrooper carbine"   :(A_30,  1050, 2.0, 320,WOOD,5, 3, (1, 1,100,175,1,  45, 6, 10,16,-1, 15, 5,  100,),SKL_RIFLES,_rifleSmall,ID_RIFLE,),#Moddable w/ suppressor
"garand"                :(A_30,  880,  2.7, 730,WOOD,7, 3, (1, 1,100,100,2,  66, 6, 8, 16,-2, -6, 6,  100,),SKL_RIFLES,_rifleSmall,ID_RIFLE,),#M1 garand carbine. Moddable w/ scope, strap, bayonet, 
"tactical carbine"      :(A_30,  6620, 2.8, 950,METL,6, 5, (1, 1,100,10, 2,  90, 6, 10,22,-2, 24, 7,  100,),SKL_RIFLES,_rifleSmall,ID_RIFLE,),#moddable w/ most things
"skirmisher rifle"      :(A_762, 920,  2.3, 330,METL,5, 4, (1, 1,100,50, 2,  50, 8, 12,18,-2, 15, 6,  100,),SKL_RIFLES,_rifleSmall,ID_AUTORIFLE,),#ak47 (semi, no stock. Short barrel.) # moddable w/ stock, extended 7.62 barrel
"avtomat"               :(A_762, 1580, 2.6, 860,METL,8, 3, (1, 2,100,30, 2,  30, 4, 10,16,-2, 15, 7,  100,),SKL_RIFLES,_rifleSmall,ID_AUTORIFLE,),#ak47 (auto, no stock. Short barrel.) # moddable w/ stock, extended 7.62 barrel
"modular weapon system" :(A_762,17500, 3.0, 990,METL,7, 6, (1, 3,100,2,  2,  200,6, 12,18,-2, 0,  6,  50,),SKL_RIFLES,_rifleSmall,ID_AUTORIFLE,),#modable with anything you can think of, including grenade launcher, laser sight, scope, longer barrel, silencer, bipod, larger magazine (box of 100), flashlight, bayonet, etc. 
"big game rifle"        :(A_308, 4600, 3.2, 550,WOOD,14,3, (1, 1,130,10, 5,  160,12,15,22,-2, -36,12, 500,),SKL_RIFLES,_rifle308,ID_RIFLE,),#moddable with scope
"field rifle"           :(A_3006,6800, 4.1, 610,WOOD,18,4, (1, 1,150,1,  6,  250,10,18,28,-3, -45,12, 600,),SKL_RIFLES,_rifle3006,ID_RIFLE,),#moddable w/ scope
"anti-materiel rifle"   :(A_50, 165500,11.2,990,METL,30,6, (1, 1,200,0,  12, 500,8, 36,32,-9, -66,12, 2400,),SKL_RIFLES,_rifleXLarge,ID_RIFLE,),#moddable w/ scope
    # machine guns (large automatic weapons)
# name                  :(AMMO,  $$$$, KG,  Dur,MAT, St,Dx,(Cp,n,Rt, jam,Min,Max,Ac,Dm,Pe,DV, Asp,Enc,For,),TYPE,script,ID,
"SAW"                   :(A_556, 6200, 5.2, 700,METL,24,3, (1, 5,150,25, 2,  100,3, 10,20,-4, 0,  8,  100,),SKL_MACHINEGUNS,_lmg,ID_MACHINEGUN,),
"LMG"                   :(A_762, 8750, 7.2, 950,METL,32,3, (1, 5,150,10, 2,  120,0, 14,18,-6, 0,  8,  100,),SKL_MACHINEGUNS,_lmg,ID_MACHINEGUN,),
    # slings
# name                  :(AMMO,  $$$$, KG,  Dur,MAT, St,Dx,(Cp,n,Rt, jam,Min,Max,Ac,Dm,Pe,DV, Asp,Enc,For,),TYPE,script,ID,
"sling"                 :(A_SLNG,0.2,  0.02,3,  ROPE,8, 6, (1, 1,100,0,  3,  30, -2,4, 1, 0,  -30,1,  2,),SKL_SLINGS,_sling,ID_ROPE,),
"wooden slingshot"      :(A_SLNG,1.0,  0.4, 5,  WOOD,16,12,(1, 1,100,0,  2,  50, -2,4, 1, 0,  0,  1,  2,),SKL_SLINGS,_sling,ID_SLINGSHOT,),
    # bows
# name                  :(AMMO,  $$$$, KG,  Dur,MAT, St,Dx,(Cp,n,Rt, jam,Min,Max,Ac,Dm,Pe,DV, Asp,Enc,For,),TYPE,script,ID,
"plastic bow"           :(A_ARRO,1,    1.0, 15, PLAS,6, 5, (1, 1,20, 0,  1,  20, 2, 0, 0, 0,  -18,6,  1.5,),SKL_BOWS,_pBow,ID_BOW,),
"hunting bow"           :(A_ARRO,8,    0.8, 75, WOOD,12,8, (1, 1,10, 0,  1,  30, 4, 2, 2, 0,  0,  6,  2,),SKL_BOWS,_smallBow,ID_BOW,),
"short bow"             :(A_ARRO,24,   0.8, 250,WOOD,16,12,(1, 1,10, 0,  1,  20, 2, 4, 2, 0,  0,  6,  3,),SKL_BOWS,_smallBow,ID_BOW,),
   "wooden bow"         :(A_ARRO,12,   0.9, 80, WOOD,16,12,(1, 1,20, 0,  2,  40, 6, 4, 3, 0,  -12,9,  2.5,),SKL_BOWS,_wBow,ID_BOW,),
 "laminate bow"         :(A_ARRO,32,   1.0, 160,WOOD,16,12,(1, 1,20, 0,  2,  50, 8, 6, 4, 0,  -12,9,  5,),SKL_BOWS,_wBow,ID_BOW,),
"composite bow"         :(A_ARRO,85,   1.5, 320,BONE,18,10,(1, 1,20, 0,  2,  60, 10,8, 6, 0,  -12,9,  10,),SKL_BOWS,_compositeBow,ID_BOW,),
   "wooden longbow"     :(A_WARO,34,   1.8, 150,WOOD,20,8, (1, 1,50, 0,  3,  80, 6, 10,8, 0,  -51,15, 20,),SKL_BOWS,_longbow,ID_BOW,),
 "laminate longbow"     :(A_WARO,70,   1.95,200,WOOD,20,9, (1, 1,50, 0,  3,  90, 8, 10,7, 0,  -51,15, 25,),SKL_BOWS,_longbow,ID_BOW,),
"composite longbow"     :(A_WARO,125,  2.4, 275,WOOD,22,10,(1, 1,50, 0,  3,  100,10,12,9, 0,  -51,15, 35,),SKL_BOWS,_longbow,ID_BOW,),
   "wooden warbow"      :(A_WARO,55,   2.0, 300,WOOD,28,12,(1, 1,50, 0,  3,  100,8, 16,9, 0,  -66,15, 30,),SKL_BOWS,_longbow,ID_BOW,),
 "laminate warbow"      :(A_WARO,95,   2.4, 450,WOOD,28,13,(1, 1,50, 0,  3,  110,10,18,10,0,  -66,15, 35,),SKL_BOWS,_longbow,ID_BOW,),
"composite warbow"      :(A_WARO,160,  2.7, 525,WOOD,30,14,(1, 1,50, 0,  3,  120,12,20,12,0,  -66,15, 50,),SKL_BOWS,_longbow,ID_BOW,),
# HUGE variety in weight of bows (power) -- add a lot more types of bows. Also huge variety of arrows. Just like guns or any other weapons.
# distinction: bows vs. warbows. War bows have more damage, are slower, have higher strength requirements, more encumbering and durable, higher penetration etc.
# crossbows             :(AMMO,  $$$$, KG,  Dur,MAT, St,Dx,(Cp,n,Rt,  jam,Min,Max,Ac,Dm,Pe,DV, Asp,Enc,For,),TYPE,script,ID,
"wooden crossbow"       :(A_BOLT,40,   3.0, 180,WOOD,5, 2, (1, 1,400, 0,  2,  10, 10,6, 4, -3, 30, 15, 3,),SKL_CROSSBOWS,_crossbow,ID_CROSSBOW,),
"wooden arbalest"       :(A_ARRO,195,  9.5, 460,WOOD,10,2, (1, 1,1200,0,  3,  20, 12,24,16,-8, 0,  21, 6,),SKL_CROSSBOWS,_arbalest,ID_CROSSBOW,),
# chu ko nu / magazine fed crossbows!
# screw crossbow! Loaded by turning a screw. Small, light, weak cbows. Maybe stronger than hand span but takes a lot longer to reload. Fire small bolts (smaller than usual). Takes 30 secs to reload
# BELLY BOW! Crossbow that needs nothing but your own weight to load and can be loaded at varying strengths (draw lengths). Fires regular sized arrows but is a crossbow.
# hand span crossbow - can be cocked by hand with sufficient strength (all crossbow technically CAN but this requires more reasonable levels of strength)
#   latchet crossbow - can also be cocked by hand, requires less strength, but is weaker. Rapid to reload (5-10 secs).
# goat's foot lever - easiest besides hand span
#   take ~7-8 secs to reload (faster than musket reloading for SURE but not as long range as muskets)
# foot stirrup, belt hooks, stand up to cock
# crank / winch / windlass - most powerful crossbows, takes longest.
#   requires superhuman strength to cock by hand (not even Arnold Schwarzzenegger could do it)
# crossbows made of: steel or bone/horn/wood
#   bows and crossbows CAN shoot arrows larger than their arrow size but not smaller. Larger results in reduced accuracy.
# crossbow bolts vs arrows: bolts have heavier arrowheads, much shorter, do not have feathers usually but wood fletching (though they can have feathers just it's harder to do), may be thicker than standard war arrows.
# crossbows resistant to rust by having linen on the bow.
#   linen string (basically a rope, just use rope. Yes linen is better than cotton but let's imagine in this world all cloth is made of linen or some similar strong fiber.)
#       covered in wax to protect from water.

# misc                  :(AMMO,  $$$$, KG,  Dur,MAT, St,Dx,(Cp,n,Rt,  jam,Min,Max,Ac,Dm,Pe,DV, Asp,Enc,For,),TYPE,script,ID,
"hand cannon"           :(A_BALL,480,  8.75,900,METL,20,2, (1, 1,1200,100,3,  8,  2, 24,2, -6, -60,24, 1600,),SKL_CANNONS,_handCannon,ID_CANNON,),#grants +AV, Protection.
"war arquebus"          :(A_BALL,1060,12.25,800,METL,24,2, (1, 1,1500,20, 5,  32, 2, 30,9, -12,-96,18, 800,),SKL_HEAVY,_arquebus,ID_CANNON,),
"blowgun"               :(A_DART,2,    0.15,20, WOOD,1, 1, (1, 1,100, 0,  2,  16, 2, 2, 2, 0,  -30,1.5,0,),None,_blowGun,ID_BLOWGUN,),
"atlatl"                :(A_SPEAR,6,   0.5, 60, WOOD,3, 3, (1, 1,100, 0,  4,  20, 4, 4, 4, 0,  -30,5,  1.5,),SKL_TIPFIRST,_atlatl,ID_CLUB,),

# energy weapons        :(AMMO,  $$$$, KG,  Dur,MAT, St,Dx,(Cp,n,Rt, jam,Min,Max,Ac,Dm,Pe,DV, Asp,Enc,For,),TYPE,script,ID,
"laser gun"             :(A_ELEC,7550, 1.7, 20, METL,5, 10,(1, 1,100,0,  1,  400,20,0, 0, 0,  0,  3,  0,),SKL_ENERGY,_laserGun,ID_ENERGYWEAPON,),
"laser rifle"           :(A_ELEC,15400,2.7, 40, METL,9, 10,(1, 1,100,0,  1,  800,40,0, 0, 0,  0,  5,  0,),SKL_ENERGY,_laserRifle,ID_ENERGYWEAPON,),
##"particle gun"      :(A_ELEC,785000,6.5,990,METL,8, 6, (1, 1,0,  1,  999,20,32,32,-6, 0,  40, 10,),SKL_ENERGY,_particleGun),#grants +AV, Protection.

# TODO: make weapons moddable with magazine upgrade, then set their
#   DEFAULT ammo capacity to 1, but give them a magazine mod to give
#   them +12 or however much ammo can fit in the mag.
# *Weapons are sold with or without mods in the shop
#   so these mods should just be added on in REAL-TIME
#   thus the stats on weapons in the RANGEDWEAPONS TABLE will NOT
#   reflect the actual values of the weapons as they will appear in-game!
# TODO: add switch firing mode command, to swap between shooting
#   either 1 or n shots per attack.

# .44 magnum too similar to .45 ACP, and not as common so let's just drop it
##".44 magnum revolver":(A_44M,4345, 1.27,700,METL,(6, 1,30, 1,  20, 8, 6, 9, 0,  9,  0,),SKL_PISTOLS,_pistol),
##"compressed air gun":(A_AIR, 6,    0.15,20, WOOD,(1, 1,100, 16,2, 2, 2, 0,  -30,-60,),_blowGun),

    }

'''
    TODO: add ranged weapons + implement

    bows
    crossbows
    blowguns
    guns
    slingshots
    slings
    

'''

'''
    .45 ACP vs. 9mm: .45 ACP more damage, less penetration
    .308 vs. .30-06: basically the same. .30-06 has more pen, less dmg
        (slightly.) Also .308 is slightly more accurate/longer ranged.
    
'''

'''
materials
    wood     - low cost; medium weight, high acc, low damage and penetration
    stone    - low cost; heavy, low acc, med damage, low penetration
    bone     - med-low cost; medium weight, high acc, med damage and penetration. Low dur.
    glass    - high cost; light, high acc, highest damage. Lowest dur and penetration.
    metal    - highest cost; heavy, med acc, high damage, highest pen. Highest dur.
    flesh    - low cost; med-light, low stats. High protection.
    leather  - med-high cost; light, low dur. Med-low stats. Boiled leather is better but more expensive.
    carbon   - variable cost; very high resistances, variable stats.
    plastic  - variable cost; light, Weak to fire and bio, strong to elec, variable stats. Generally low dur and high cost.
Material tiers
    top tier:
        metal - very high dur and pen, high damage. Heavy.
        glass - very low dur and pen, highest damage. Light.
    middle tier:
        wood - light, low damage.
        stone - heavy, high damage.
        bone - middle ground. Medium weight, medium damage.
    bottom tier:
        plastic - very low dur, lowest pen, lowest damage. Lightest.
1-h weapon types
    bludgeons      - low cost; med-low acc, high dmg, lowest pen, slow. Also grants AV and protection.
    hammers        - med-low cost; low acc, med-high dmg and pen.
    axes           - med cost; very low acc, highest dmg, med speed
    knives         - med-low cost; fastest, highest pen. Lowest Msp penalty.
    swords         - med-high cost; highest DV, high pen. and acc. 
    javelins       - 
    shortspears    - 
    shields        - high cost; grants DV and/or AV and protection. Heaviest Msp penalty. Quite ineffective as a weapon.
    raw materials  - can be used as weapons in a pinch. Ineffectual compared to real weapons.
2-h weapons
    2-handed weapons have higher stats than 1-h, and often grant AV/DV/prot.
    Obviously they are heavier/more encumbering, but quicker, more accurate and powerful than 1-handed weapons.
    *longswords, battleaxes, and spears are like
    swords, axes, and javelins/shortspears, respectively, except 2-handed only.
'''

'''
    idea: weapon "grind" (PSO) SEE QUALITIES IN RECIPES...
        grinding gives +1 to dmg and pen, and +2 to acc
        to grind a weapon, you must have special grinding tools.
        maximum grind different depending on weapon type
            Grind maximum is higher for swords than clubs, for example.
'''


LIMBWEAPONS={
# name          :(At,Dm,Pe,Gr,DV,AV,Pr,Asp,Sta)
"flesh hand"    :(0, 0, 0, 0, 0, 0, 0, 0,  24,),
"bone claw"     :(2, 2, 2, -4,0, 0, 0, 12, 16,),
"cyborg hand"   :(2, 2, 2, 0, 1, 0, 1, 12, 20,),
"tentacle"      :(4, 0, 0, 4, 0, 0, 1, -30,28,),
"pseudopod"     :(-2,0, 0, 4, 0, 0, 0, -60,12,),
    }

WEAPONS={ #melee weapons, 1H, 2H and 1/2H

    # TODO:
        # give all weapons more defensive capability
        # skill in varying levels - how do?
        #   IDEA: when you have level 10 skill, you gain stats equal to those in the table.
        #       every 10 levels you gain is worth that same linear growth value for those stats.
        
    # IDEA: weapon class (skill type) affects various things in combat
        # bludgeons do increased damage to armored foes
        # swords do increased damage to unarmored foes

    # 1-handed weapons #

    # cudgels             $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,),TYPE,script,ID,
"plastic cudgel"        :(2,    1.4, 220, PLAS,10,2, (2,  2,  5,  0,  1,  1,  -15,5,  -5, 1,  18, 1,),SKL_BLUDGEONS,_pCudgel,ID_CLUB,),
"wooden cudgel"         :(13,   1.35,375, WOOD,10,2, (3,  4,  5,  0,  1,  1,  -9, 5,  -5, 1,  17, 1,),SKL_BLUDGEONS,_wCudgel,ID_CLUB,),
"stone cudgel"          :(10,   1.2, 340, WOOD,10,2, (3,  6,  6,  0,  1,  1,  -9, 5,  -5, 1,  15, 1,),SKL_BLUDGEONS,_sCudgel,ID_CLUB,),
"bone cudgel"           :(16,   1.3, 300, WOOD,10,2, (3,  5,  5,  0,  1,  1,  -9, 5,  -5, 1,  16, 1,),SKL_BLUDGEONS,_bCudgel,ID_CLUB,),
"glass cudgel"          :(18,   1.3, 10,  WOOD,10,3, (3,  9,  4,  0,  0,  0,  -6, 5,  -5, 1,  16, 1,),SKL_BLUDGEONS,_gCudgel,ID_CLUB,),
"metal cudgel"          :(32,   1.2, 650, WOOD,10,2, (3,  7,  7,  0,  1,  1,  -6, 5,  -5, 1,  15, 1,),SKL_BLUDGEONS,_mCudgel,ID_CLUB,),
    # clubs               $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,),TYPE,script,ID,
"plastic club"          :(2,    1.55,275, PLAS,13,2, (2,  3,  4,  0,  2,  1,  -21,6,  -5, 1,  20, 1,),SKL_BLUDGEONS,_pClub,ID_CLUB,),
"wooden club"           :(10,   1.45,420, WOOD,12,2, (3,  6,  5,  0,  2,  1,  -15,6,  -5, 1,  18, 1,),SKL_BLUDGEONS,_wClub,ID_CLUB,),
"stone club"            :(12,   1.3, 500, STON,11,2, (3,  7,  6,  0,  2,  1,  -12,5,  -5, 1,  18, 1,),SKL_BLUDGEONS,_sClub,ID_CLUB,),
"bone club"             :(22,   1.4, 365, BONE,12,2, (4,  7,  7,  0,  2,  1,  -12,5,  -5, 1,  18, 1,),SKL_BLUDGEONS,_bClub,ID_CLUB,),
"glass club"            :(32,   1.2, 3,   GLAS,10,3, (3,  10, 5,  0,  0,  0,  -9, 4,  -5, 1,  16, 1,),SKL_BLUDGEONS,_gClub,ID_CLUB,),
"metal club"            :(59,   1.15,950, METL,11,2, (3,  8,  8,  0,  1,  1,  -12,4,  -5, 1,  16, 1,),SKL_BLUDGEONS,_mClub,ID_CLUB,),
    # spiked clubs        $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,),TYPE,script,ID,
"plastic spiked club"   :(2,    1.6, 50,  PLAS,14,4, (1,  6,  5,  0,  2,  1,  -36,7,  -8, 1,  22, 1,),SKL_BLUDGEONS,_pSpikedClub,ID_MACE,),
"wooden spiked club"    :(10,   1.5, 120, WOOD,14,4, (2,  9,  6,  0,  2,  1,  -33,7,  -8, 1,  20, 1,),SKL_BLUDGEONS,_wSpikedClub,ID_MACE,),
    # maces               $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,),TYPE,script,ID,
"plastic mace"          :(2,    1.45,75,  PLAS,12,3, (2,  6,  5,  0,  1,  1,  -33,6,  -6, 1,  18, 1,),SKL_BLUDGEONS,_pMace,ID_MACE,),
"wooden mace"           :(20,   1.35,160, WOOD,12,3, (3,  9,  7,  0,  1,  1,  -27,6,  -6, 1,  16, 1,),SKL_BLUDGEONS,_wMace,ID_MACE,),
"stone mace"            :(24,   1.3, 220, WOOD,12,3, (3,  12, 8,  0,  1,  1,  -24,6,  -6, 1,  16, 1,),SKL_BLUDGEONS,_sMace,ID_MACE,),
"bone mace"             :(27,   1.3, 100, WOOD,12,3, (4,  10, 9,  0,  1,  1,  -24,6,  -6, 1,  16, 1,),SKL_BLUDGEONS,_bMace,ID_MACE,),
"glass mace"            :(65,   1.4, 5,   WOOD,12,4, (3,  24, 7,  0,  0,  0,  -30,5,  -6, 1,  14, 1,),SKL_BLUDGEONS,_gMace,ID_MACE,),
"metal mace"            :(72,   1.35,325, WOOD,12,3, (4,  14, 10, 0,  1,  1,  -27,5,  -6, 1,  16, 1,),SKL_BLUDGEONS,_mMace,ID_MACE,),
    # morning stars       $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,),TYPE,script,ID,
"metal morning star"    :(75,   1.25,240, METL,12,2, (4,  16, 12, 0,  1,  1,  -39,8,  -7, 1,  20, 1,),SKL_BLUDGEONS,_mMace,ID_MACE,),
    # warhammers          $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,),TYPE,script,ID,
"plastic warhammer"     :(2,    1.4, 190, PLAS,12,4, (1,  4,  10, 0,  0,  0,  -24,4,  -5, 1,  18, 1,),SKL_HAMMERS,_pWarhammer,ID_HAMMER,),
"wooden warhammer"      :(24,   1.35,280, WOOD,12,4, (2,  5,  13, 0,  0,  0,  -21,4,  -5, 1,  16, 1,),SKL_HAMMERS,_wWarhammer,ID_HAMMER,),
"stone warhammer"       :(18,   1.3, 200, WOOD,12,4, (2,  7,  15, 0,  0,  0,  -21,4,  -5, 1,  18, 1,),SKL_HAMMERS,_sWarhammer,ID_HAMMER,),
"bone warhammer"        :(28,   1.15,260, WOOD,10,4, (2,  6,  14, 0,  0,  0,  -15,4,  -5, 1,  16, 1,),SKL_HAMMERS,_bWarhammer,ID_HAMMER,),
"metal warhammer"       :(51,   1.25,500, WOOD,10,4, (2,  8,  16, 0,  0,  0,  -18,4,  -5, 1,  16, 1,),SKL_HAMMERS,_mWarhammer,ID_HAMMER,),
    # war axes            $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,),TYPE,script,ID,
"plastic war axe"       :(2,    1.35,60,  PLAS,11,5, (1,  8,  4,  1,  0,  0,  -12,5,  -2, 2,  18, 1,),SKL_AXES,_pWarAxe,ID_AXE,),
"wooden war axe"        :(26,   1.3, 90,  WOOD,11,5, (2,  10, 7,  1,  0,  0,  -9, 5,  -2, 2,  16, 1,),SKL_AXES,_wWarAxe,ID_AXE,),
"stone war axe"         :(22,   1.25,120, WOOD,11,5, (2,  12, 8,  1,  0,  0,  -15,5,  -2, 2,  18, 1,),SKL_AXES,_sWarAxe,ID_AXE,),
"bone war axe"          :(32,   1.25,180, WOOD,11,5, (2,  11, 9,  1,  0,  0,  -6, 5,  -2, 2,  16, 1,),SKL_AXES,_bWarAxe,ID_AXE,),
"metal war axe"         :(62,   1.2, 260, WOOD,11,5, (3,  14, 10, 1,  0,  0,  -12,5,  -2, 2,  15, 1,),SKL_AXES,_mWarAxe,ID_AXE,),
    # tomahawks           $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,),TYPE,script,ID,
"plastic tomahawk"      :(2,    1.1, 20,  PLAS,10,5, (1,  6,  7,  1,  0,  0,  -21,3,  -2, 3,  16, 1,),SKL_AXES,_pTomahawk,ID_AXE,),
"wooden tomahawk"       :(12,   0.9, 40,  WOOD,9, 6, (2,  7,  9,  1,  0,  0,  -18,3,  -2, 3,  15, 1,),SKL_AXES,_wTomahawk,ID_AXE,),
"stone tomahawk"        :(16,   1.1, 80,  WOOD,9, 5, (2,  9,  10, 1,  0,  0,  -24,3,  -2, 3,  16, 1,),SKL_AXES,_sTomahawk,ID_AXE,),
"bone tomahawk"         :(23,   0.95,60,  WOOD,8, 6, (2,  8,  11, 1,  0,  0,  -18,3,  -2, 3,  15, 1,),SKL_AXES,_bTomahawk,ID_AXE,),
"metal tomahawk"        :(40,   1.0, 120, WOOD,8, 6, (2,  11, 12, 1,  0,  0,  -21,3,  -2, 3,  14, 1,),SKL_AXES,_mTomahawk,ID_AXE,),
    # Shivs               $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,),TYPE,script,ID,
"plastic shiv"          :(0,    0.3, 15,  PLAS,2, 4, (2,  2,  7,  0,  0,  0,  42, 2,  -5, 1,  5,  0,),SKL_KNIVES,_pShiv,ID_KNIFE,),
"wooden shiv"           :(0,    0.3, 20,  WOOD,2, 4, (2,  3,  8,  0,  0,  0,  48, 2,  -5, 1,  4,  0,),SKL_KNIVES,_wShiv,ID_KNIFE,),
"stone shiv"            :(0,    0.25,40,  STON,2, 4, (3,  4,  9,  0,  0,  0,  45, 2,  -5, 1,  5,  0,),SKL_KNIVES,_sShiv,ID_KNIFE,),
"bone shiv"             :(0,    0.2, 35,  BONE,2, 4, (3,  4,  10, 0,  0,  0,  51, 2,  -5, 1,  4,  0,),SKL_KNIVES,_bShiv,ID_KNIFE,),
"glass shiv"            :(1,    0.15,3,   GLAS,2, 5, (5,  6,  8,  0,  0,  0,  63, 2,  -5, 1,  2,  0,),SKL_KNIVES,_gShiv,ID_KNIFE,),
"metal shiv"            :(6,    0.2, 50,  METL,2, 4, (4,  4,  12, 0,  0,  0,  54, 2,  -5, 1,  3,  0,),SKL_KNIVES,_mShiv,ID_KNIFE,),
"ceramic shiv"          :(2,    0.22,10,  CERA,2, 5, (5,  8,  9,  0,  0,  0,  60, 2,  -5, 1,  2,  0,),SKL_KNIVES,_cShiv,ID_KNIFE,),
    # knives              $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,),TYPE,script,ID,
"plastic knife"         :(0,    0.2, 35,  PLAS,2, 2, (3,  2,  10, 0,  0,  0,  48, 2,  -3, 2,  7,  0,),SKL_KNIVES,_pKnife,ID_KNIFE,),
"wooden knife"          :(2,    0.15,60,  WOOD,2, 2, (3,  3,  14, 0,  0,  0,  54, 2,  -3, 2,  5,  0,),SKL_KNIVES,_wKnife,ID_KNIFE,),
"stone knife"           :(6,    0.15,110, STON,2, 2, (4,  5,  16, 0,  0,  0,  51, 2,  -3, 2,  6,  0,),SKL_KNIVES,_sKnife,ID_KNIFE,),
"bone knife"            :(5,    0.12,90,  BONE,1, 3, (4,  5,  18, 0,  0,  0,  57, 2,  -3, 2,  5,  0,),SKL_KNIVES,_bKnife,ID_KNIFE,),
"glass knife"           :(12,   0.08,3,   GLAS,1, 5, (6,  8,  12, 0,  0,  0,  66, 2,  -3, 3,  3,  0,),SKL_KNIVES,_gKnife,ID_KNIFE,),
"metal knife"           :(14,   0.15,200, METL,1, 4, (5,  5,  20, 0,  0,  0,  60, 2,  -3, 3,  4,  0,),SKL_KNIVES,_mKnife,ID_KNIFE,),
"ceramic knife"         :(20,   0.12,15,  CERA,1, 5, (6,  10, 14, 0,  0,  0,  63, 2,  -3, 3,  3,  0,),SKL_KNIVES,_cKnife,ID_KNIFE,),
    # serrated knives     $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,),TYPE,script,ID,
"plastic serrated knife":(0,    0.18,15,  PLAS,2, 4, (2,  3,  8,  0,  0,  0,  24, 2,  -4, 1,  8,  0,),SKL_KNIVES,_pSerrated,ID_KNIFE,),
"wooden serrated knife" :(4,    0.13,35,  WOOD,2, 4, (2,  4,  11, 0,  0,  0,  30, 2,  -4, 1,  6,  0,),SKL_KNIVES,_wSerrated,ID_KNIFE,),
"stone serrated knife"  :(8,    0.13,60,  STON,2, 4, (3,  6,  12, 0,  0,  0,  27, 2,  -4, 1,  7,  0,),SKL_KNIVES,_sSerrated,ID_KNIFE,),
"bone serrated knife"   :(7,    0.1, 45,  BONE,2, 5, (3,  6,  13, 0,  0,  0,  33, 2,  -4, 1,  6,  0,),SKL_KNIVES,_bSerrated,ID_KNIFE,),
"metal serrated knife"  :(18,   0.13,100, METL,2, 6, (4,  7,  15, 0,  0,  0,  30, 2,  -4, 2,  5,  0,),SKL_KNIVES,_mSerrated,ID_KNIFE,),
    # war knives          $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,),TYPE,script,ID,
"plastic war knife"     :(1,    0.55,50,  PLAS,5, 6, (3,  3,  12, 1,  0,  0,  51, 2.5,-2, 5,  6,  0,),SKL_KNIVES,_pWarKnife,ID_KNIFE,),
"wooden war knife"      :(5,    0.45,80,  WOOD,4, 7, (4,  4,  16, 1,  0,  0,  57, 2.5,-2, 6,  5,  0,),SKL_KNIVES,_wWarKnife,ID_KNIFE,),
"bone war knife"        :(10,   0.5, 125, BONE,4, 8, (5,  6,  18, 1,  0,  0,  54, 2.5,-2, 7,  5,  0,),SKL_KNIVES,_bWarKnife,ID_KNIFE,),
"glass war knife"       :(28,   0.32,10,  GLAS,3, 9, (7,  10, 15, 0,  0,  0,  78, 2.5,-2, 6,  4,  0,),SKL_KNIVES,_gWarKnife,ID_KNIFE,),
"metal war knife"       :(26,   0.42,250, METL,4, 8, (6,  7,  20, 2,  0,  0,  69, 2.5,-2, 9,  4,  0,),SKL_KNIVES,_mWarKnife,ID_KNIFE,),
"ceramic war knife"     :(35,   0.35,20,  CERA,3, 9, (7,  11, 16, 0,  0,  0,  75, 2.5,-2, 7,  4,  0,),SKL_KNIVES,_cWarKnife,ID_KNIFE,),
    # daggers             $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,),TYPE,script,ID,
"bone dagger"           :(10,   0.35,115, BONE,3, 4, (4,  6,  21, 1,  0,  0,  69, 3,  -2, 5,  5,  0,),SKL_KNIVES,_bDagger,ID_DAGGER,),
"glass dagger"          :(28,   0.22,5,   GLAS,2, 7, (6,  12, 18, 1,  0,  0,  90, 3,  -2, 7,  4,  0,),SKL_KNIVES,_gDagger,ID_DAGGER,),
"metal dagger"          :(30,   0.3, 190, METL,3, 6, (5,  7,  24, 2,  0,  0,  75, 3,  -2, 6,  4,  0,),SKL_KNIVES,_mDagger,ID_DAGGER,),
"rondel dagger"         :(70,   0.4, 320, METL,4, 7, (4,  8,  28, 2,  0,  0,  54, 3,  -2, 6,  5,  0,),SKL_KNIVES,_rondelDagger,ID_DAGGER,),#STEEL
    # bayonets            $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,),TYPE,script,ID,
"plastic bayonet"       :(0,    0.45,40,  PLAS,5, 4, (2,  2,  10, 0,  0,  0,  36, 3,  -3, 2,  7,  0,),SKL_KNIVES,_pBayonet,ID_KNIFE,),
"wooden bayonet"        :(5,    0.4, 70,  WOOD,4, 4, (3,  3,  14, 0,  0,  0,  33, 3,  -3, 2,  6,  0,),SKL_KNIVES,_wBayonet,ID_KNIFE,),
"bone bayonet"          :(8,    0.3, 100, BONE,3, 4, (3,  5,  16, 0,  0,  0,  39, 3,  -3, 2,  5,  0,),SKL_KNIVES,_bBayonet,ID_KNIFE,),
"metal bayonet"         :(22,   0.35,225, METL,4, 5, (4,  5,  18, 0,  0,  0,  36, 3,  -3, 3,  6,  0,),SKL_KNIVES,_mBayonet,ID_KNIFE,),
    # javelins            $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,),TYPE,script,ID,
"plastic javelin"       :(1,    0.75,35,  PLAS,7, 2, (6,  4,  7,  0,  0,  0,  -24,9,  -6, 3,  12, 2,),SKL_JAVELINS,_pJavelin,ID_JAVELIN,),
"wooden javelin"        :(5,    0.7, 50,  WOOD,7, 2, (8,  6,  10, 0,  0,  0,  -27,9,  -6, 3,  10, 2,),SKL_JAVELINS,_wJavelin,ID_JAVELIN,),
"metal javelin"         :(32,   0.5, 200, METL,6, 3, (9,  8,  12, 0,  0,  0,  -18,9,  -6, 3,  8,  2,),SKL_JAVELINS,_mJavelin,ID_JAVELIN,),
    # shortspears         $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,),TYPE,script,ID,
"plastic shortspear"    :(1,    1.0, 15,  PLAS,12,1, (6,  5,  6,  0,  0,  0,  -12,9,  -8, 5,  12, 2.5,),SKL_JAVELINS,_pShortSpear,ID_JAVELIN,),
"wooden shortspear"     :(8,    1.05,30,  WOOD,12,1, (7,  7,  8,  0,  0,  0,  -12,9,  -8, 5,  12, 2.5,),SKL_JAVELINS,_wShortSpear,ID_JAVELIN,),
"stone shortspear"      :(8,    1.1, 65,  WOOD,13,1, (7,  9,  10, 0,  0,  0,  -15,9,  -8, 5,  12, 2.5,),SKL_JAVELINS,_sShortSpear,ID_JAVELIN,),
"bone shortspear"       :(15,   1.05,100, WOOD,12,2, (7,  8,  9,  0,  0,  0,  -12,9,  -8, 5,  12, 2.5,),SKL_JAVELINS,_bShortSpear,ID_JAVELIN,),
"glass shortspear"      :(25,   0.95,5,   WOOD,9, 3, (9,  12, 7,  0,  0,  0,  -9, 9,  -8, 5,  12, 2.5,),SKL_JAVELINS,_gShortSpear,ID_JAVELIN,),
"metal shortspear"      :(22,   1.05,135, WOOD,11,2, (8,  10, 12, 0,  0,  0,  -12,9,  -8, 5,  12, 2.5,),SKL_JAVELINS,_mShortSpear,ID_JAVELIN,),
"ceramic shortspear"    :(28,   0.95,10,  CERA,9, 3, (9,  14, 9,  0,  0,  0,  -9, 9,  -8, 5,  12, 2.5,),SKL_JAVELINS,_cShortSpear,ID_JAVELIN,),
    # boomerangs          $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,),TYPE,script,ID,
"plastic boomerang"     :(1,    0.7, 20,  PLAS,8, 2, (2,  2,  3,  0,  0,  0,  -15,7,  -6, 1,  14, 1,),SKL_BLUDGEONS,_pBoomerang,ID_BOOMERANG,),
"wooden boomerang"      :(4,    0.5, 30,  WOOD,7, 3, (3,  4,  5,  0,  0,  0,  -12,7,  -4, 1,  14, 1,),SKL_BLUDGEONS,_wBoomerang,ID_BOOMERANG,),
"bone boomerang"        :(5,    0.45,25,  BONE,6, 4, (3,  4,  5,  0,  0,  0,  -9, 4,  -4, 1,  12, 1,),SKL_BLUDGEONS,_bBoomerang,ID_BOOMERANG,),
"glass boomerang"       :(22,   0.5, 2,   GLAS,5, 6, (5,  7,  4,  0,  0,  0,  -9, 4,  -4, 1,  12, 1,),SKL_BLUDGEONS,_gBoomerang,ID_BOOMERANG,),
"metal boomerang"       :(25,   0.4, 90,  METL,5, 5, (4,  5,  6,  0,  0,  0,  -6, 4,  -4, 2,  12, 1,),SKL_BLUDGEONS,_mBoomerang,ID_BOOMERANG,),
"ceramic boomerang"     :(38,   0.4, 1,   CERA,5, 6, (5,  8,  4,  0,  0,  0,  -9, 4,  -3, 1,  12, 1,),SKL_BLUDGEONS,_cBoomerang,ID_BOOMERANG,),
    # bucklers            $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,),TYPE,script,ID,
"plastic buckler"       :(2,    1.7, 30,  PLAS,17,12,(1,  1,  1,  5,  1,  1,  -9, 4,  -3, 3,  16, 0.2,),SKL_SHIELDS,_buckler,ID_SHIELD,),
"wooden buckler"        :(12,   1.65,75,  WOOD,16,12,(1,  2,  3,  6,  1,  1,  -6, 4,  -3, 4,  16, 0.2,),SKL_SHIELDS,_buckler,ID_SHIELD,),
"bone buckler"          :(24,   1.4, 40,  BONE,14,12,(2,  3,  4,  6,  1,  1,  -3, 4,  -2, 5,  12, 0.2,),SKL_SHIELDS,_buckler,ID_SHIELD,),#made of one large bone sculpted into shape + some leather
"metal buckler"         :(90,   1.5, 150, METL,15,12,(2,  5,  5,  7,  2,  1,  -6, 4,  -3, 6,  16, 0.2,),SKL_SHIELDS,_buckler,ID_SHIELD,),
    # rotellas            $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,),TYPE,script,ID,
"plastic rotella"       :(4,    4.0, 50,  PLAS,24,8, (2,  2,  1,  5,  2,  2,  -33,6,  -6, 4,  32, 0.4,),SKL_SHIELDS,_rotella,ID_SHIELD,),
"wooden rotella"        :(24,   3.6, 115, WOOD,22,8, (3,  3,  2,  6,  2,  2,  -27,6,  -5, 6,  30, 0.4,),SKL_SHIELDS,_rotella,ID_SHIELD,),
"bone rotella"          :(49,   3.4, 75,  BONE,20,8, (3,  5,  3,  5,  2,  2,  -24,6,  -4, 6,  28, 0.4,),SKL_SHIELDS,_rotella,ID_SHIELD,),#made of one, two or three big pieces of bone glued together. The pieces of bone (esp. for 1 or 2-piece rotellas) are difficult to acquire and manufacture for shield use so this is a relatively expensive item.
"metal rotella"         :(175,  3.0, 240, METL,18,8, (3,  7,  4,  6,  3,  2,  -18,6,  -4, 7,  26, 0.4,),SKL_SHIELDS,_rotella,ID_SHIELD,), # one stamina cost for each 100g, +2 for being metal. - some percentage b/c shields are easy to attack with. Encumbering non-weapons should get *1.5 stamina cost or some shit. Auto-generated of course.
    # shields             $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,),TYPE,script,ID,
"wicker shield"         :(20,   4.2, 35,  WOOD,18,6, (1,  2,  0,  4,  2,  2,  -36,7,  -10,4,  44, 0.6,),SKL_SHIELDS,_shield,ID_SHIELD,),
"plastic shield"        :(7,    6.5, 80,  PLAS,22,6, (1,  3,  0,  3,  2,  3,  -54,7,  -12,5,  52, 0.6,),SKL_SHIELDS,_shield,ID_SHIELD,),
"wooden shield"         :(75,   5.25,180, WOOD,20,6, (3,  5,  1,  4,  3,  3,  -45,7,  -10,7,  44, 0.6,),SKL_SHIELDS,_shield,ID_SHIELD,),
"bone shield"           :(145,  6.2, 100, BONE,22,6, (2,  7,  2,  4,  4,  2,  -48,7,  -8, 7,  52, 0.6,),SKL_SHIELDS,_shield,ID_SHIELD,),
"boiled leather shield" :(190,  5.05,120, BOIL,20,6, (3,  4,  1,  5,  4,  3,  -42,7,  -12,6,  44, 0.6,),SKL_SHIELDS,_shield,ID_SHIELD,),
"metal shield"          :(380,  6.0, 360, METL,22,6, (2,  9,  3,  4,  5,  3,  -51,7,  -6, 8,  48, 0.6,),SKL_SHIELDS,_shield,ID_SHIELD,),
    # scutums             $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,),TYPE,script,ID,
"plastic scutum"        :(10,   9.8, 80,  PLAS,29,4, (-1, 2,  -6, 2,  3,  3,  -69,9,  -12,6,  76, 0.3,),SKL_SHIELDS,_scutum,ID_SHIELD,),
"wooden scutum"         :(120,  8.7, 180, WOOD,27,4, (1,  4,  -5, 3,  4,  3,  -57,9,  -10,7,  66, 0.3,),SKL_SHIELDS,_scutum,ID_SHIELD,),
"bone scutum"           :(255,  9.3, 100, BONE,28,4, (0,  5,  -2, 3,  5,  2,  -60,9,  -8, 8,  72, 0.3,),SKL_SHIELDS,_scutum,ID_SHIELD,),
"boiled leather scutum" :(305,  7.7, 120, BOIL,24,4, (1,  4,  -3, 4,  5,  3,  -54,9,  -12,8,  66, 0.3,),SKL_SHIELDS,_scutum,ID_SHIELD,),
"metal scutum"          :(495,  8.1, 360, METL,26,4, (0,  6,  -1, 3,  6,  3,  -63,9,  -6, 8,  72, 0.3,),SKL_SHIELDS,_scutum,ID_SHIELD,),
    # tower shields       $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,),TYPE,script,ID,
"plastic tower shield"  :(15,   13.5,140, PLAS,33,1, (-3, 2,  -12,-6, 4,  5,  -81,10, -32,7,  120,0.1,),SKL_SHIELDS,_towerShield,ID_SHIELD,),
"wooden tower shield"   :(165,  12.0,400, WOOD,31,1, (-2, 2,  -12,-5, 5,  6,  -72,10, -30,8,  100,0.1,),SKL_SHIELDS,_towerShield,ID_SHIELD,),
"bone tower shield"     :(360,  12.7,320, BONE,32,1, (-2, 3,  -6, -6, 6,  4,  -81,10, -28,9,  100,0.1,),SKL_SHIELDS,_towerShield,ID_SHIELD,),
"metal tower shield"    :(620,  10.8,800, METL,30,1, (-1, 4,  -6, -4, 8,  6,  -75,10, -24,9,  90, 0.1,),SKL_SHIELDS,_towerShield,ID_SHIELD,),
"riot shield"           :(1060, 8.2, 250, PLAS,24,1, (0,  2,  -9, -3, 7,  6,  -69,8,  -20,10, 70, 0.1,),SKL_SHIELDS,_towerShield,ID_SHIELD,),
    # whips / bullwhips   $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,),TYPE,script,ID,
"rubber flail"          :(2,    0.1, 3,   RUBB,1, 3, (-8, 3,  2,  0,  0,  0,  -51,3,  -1, 0,  1,  0,),None,_rubberBandWhip,ID_RUBBERBAND,),#2h only. This is a heavy metal ball attached to a rubber band like a primitive flail.
"rubber whip"           :(6,    0.3, 30,  RUBB,3, 5, (4,  1,  0,  0,  0,  0,  -15,2,  -10,1,  7,  1,),SKL_BLUDGEONS,_whip,ID_BATON,),
"plastic duel whip"     :(2,    1.6, 90,  PLAS,12,2, (2,  2,  2,  0,  0,  0,  -30,3,  -6, 1,  16, 1,),SKL_BLUDGEONS,_heavyWhip,ID_BATON,),
"leather duel whip"     :(75,   1.45,150, LETH,12,2, (2,  3,  4,  0,  0,  0,  -24,3,  -10,1,  20, 1,),SKL_BLUDGEONS,_heavyWhip,ID_BATON,),
"leather bullwhip"      :(40,   0.6, 60,  LETH,4, 16,(-5, 4,  2,  0,  0,  0,  -51,2.5,-5, 0,  5,  3,),SKL_BULLWHIPS,_bullWhip,ID_WHIP,),
"graphene bullwhip"     :(7500, 0.5, 1800,CARB,3, 20,(-2, 5,  5,  0,  0,  0,  -42,2.5,-5, 1,  4,  3,),SKL_BULLWHIPS,_bullWhip,ID_WHIP,),
    # swords              $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,),TYPE,script,ID,
"plastic sword"         :(2,    1.15,20,  PLAS,11,6, (4,  3,  6,  1,  0,  0,  15, 5,  -7, 3,  12, 1,),SKL_SWORDS,_pSword,ID_SWORD,),
"wooden sword"          :(22,   1.05,40,  WOOD,10,8, (6,  4,  9,  2,  0,  0,  24, 4,  -6, 4,  10, 1,),SKL_SWORDS,_wSword,ID_SWORD,),
"bone sword"            :(51,   0.75,60,  BONE,7, 10,(5,  5,  12, 1,  0,  0,  21, 3,  -5, 4,  8,  1,),SKL_SWORDS,_bSword,ID_SWORD,),
"metal sword"           :(65,   1.0, 120, METL,9, 12,(7,  6,  14, 2,  0,  0,  39, 4,  -4, 5,  10, 1,),SKL_SWORDS,_mSword,ID_SWORD,),
"diamonite sword"       :(2650, 0.9, 400, CARB,7, 15,(8,  9,  18, 3,  0,  0,  51, 4,  -4, 7,  8,  1,),SKL_SWORDS,_dSword,ID_SWORD,),
"graphene sword"        :(11500,0.8, 1200,CARB,5, 18,(9,  12, 22, 3,  0,  0,  60, 3,  -3, 12, 8,  2,),SKL_SWORDS,_grSword,ID_SWORD,),
    # other swords        $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,),TYPE,script,ID,
"gladius"               :(45,   0.7, 180, METL,6, 10,(6,  6,  13, 2,  0,  0,  42, 3,  -2, 2,  8,  1,),SKL_SWORDS,_leafSword,ID_SWORD,),
"hanger"                :(60,   0.8, 90,  METL,8, 8, (10, 4,  11, 4,  0,  0.5,54, 4,  -3, 4,  8,  1,),SKL_SWORDS,_hanger,ID_SWORD,),#POOR STEEL
"messer"                :(90,   1.4, 210, METL,12,6, (5,  6,  10, 3,  1,  1,  30, 6,  -4, 3,  14, 1.2,),SKL_SWORDS,_messer,ID_SWORD,),#POOR STEEL
"smallsword"            :(105,  0.4, 40,  METL,5, 13,(8,  3,  11, 4,  0,  0,  69, 3,  -6, 8,  4,  1,),SKL_SWORDS,_smallSword,ID_SWORD,),#STEEL
"curved sword"          :(120,  1.1, 80,  METL,8, 15,(7,  6,  7,  3,  0,  0,  54, 6,  -2, 6,  10, 0.8,),SKL_SWORDS,_curvedSword,ID_SWORD,),#POOR STEEL
"broadsword"            :(130,  1.3, 240, METL,12,7, (5,  8,  12, 2,  0,  0,  24, 6,  -5, 3,  14, 1,),SKL_SWORDS,_broadsword,ID_SWORD,),#POOR STEEL
"cutlass"               :(130,  1.35,450, METL,13,12,(6,  6,  10, 3,  0,  1,  39, 5,  -3, 6,  12, 1,),SKL_SWORDS,_cutlass,ID_SWORD,),#POOR STEEL, made entirely of metal (no wood)
"sabre"                 :(135,  1.25,200, METL,12,12,(8,  6,  9,  4,  0,  0.5,48, 6,  -4, 5,  12, 1.2,),SKL_SWORDS,_sabre,ID_SWORD,),#POOR STEEL
"falchion"              :(160,  1.4, 345, METL,14,10,(5,  8,  11, 1,  1,  0,  18, 6,  -5, 4,  14, 1,),SKL_SWORDS,_falchion,ID_SWORD,),#POOR STEEL
"arming sword"          :(235,  1.35,260, METL,12,14,(8,  7,  16, 2,  0,  0.5,42, 7,  -4, 5,  14, 1.8,),SKL_SWORDS,_armingSword,ID_SWORD,),#STEEL
"basket-hilted sword"   :(295,  1.45,220, METL,14,16,(9,  6,  12, 4,  1,  1.5,51, 7,  -6, 7,  14, 1.5,),SKL_SWORDS,_basketHiltedSword,ID_SWORD,),#STEEL
"rapier"                :(345,  1.5, 110, METL,16,16,(11, 5,  15, 4,  0,  1,  60, 8,  -7, 8,  18, 2.1,),SKL_SWORDS,_rapier,ID_SWORD,),#STEEL
    # other misc weapons  $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,),TYPE,script,ID,
    # knives
"kukri"                 :(70,   0.5, 90,  METL,5, 14,(4,  6,  8,  1,  0,  0,  51, 2.5,-3, 10, 6,  0.4,),SKL_KNIVES,_kukri,ID_KNIFE,),#POOR STEEL
"metal throwing knife"  :(8,    0.1, 20,  METL,1, 16,(5,  3,  16, 0,  0,  0,  54, 1.5,-8, 1,  4,  0.1,),SKL_KNIVES,_mThrowingKnife,ID_KNIFE,),
"metal butcher knife"   :(16,   0.3, 120, METL,3, 8, (2,  5,  3,  0,  0,  0,  12, 4,  -10,1,  8,  0.2,),SKL_KNIVES,_butcherKnife,ID_KNIFE,),
    # boxing weapons
"metal knuckles"        :(6,    0.1, 320, METL,2, 2, (2,  4,  4,  0,  0,  0,  18, 2,  -6, 0,  16, 0,),SKL_BOXING,_knuckles,ID_KNUCKLES,),
"metal spiked knuckles" :(14,   0.2, 150, METL,2, 2, (2,  5,  6,  0,  0,  0,  6,  3,  -8, 0,  24, 0,),SKL_BOXING,_knuckles,ID_KNUCKLES,),
"boxing wrap"           :(4,    0.25,20,  CLTH,2, 6, (2,  2,  1,  1,  0,  0,  33, 2,  -8, 2,  12, 0,),SKL_BOXING,_boxingWraps,ID_BANDAGE,),
    # bludgeons
"metal baton"           :(25,   0.5, 175, METL,4, 3, (4,  3,  5,  1,  0,  0,  9,  2,  -2, 3,  4,  0.5,),SKL_BLUDGEONS,_baton,ID_BATON,),
"metal bat"             :(35,   0.7, 220, METL,7, 1, (3,  6,  6,  0,  1,  0,  -6, 5,  -8, 1,  8,  0.5,),SKL_BLUDGEONS,_baton,ID_BATON,),
"wooden truncheon"      :(4,    0.85,250, WOOD,8, 2, (3,  5,  6,  1,  0,  0,  -3, 4,  -6, 2,  12, 1,),SKL_BLUDGEONS,_club,ID_BATON,),
"metal truncheon"       :(46,   0.75,500, METL,8, 3, (3,  7,  8,  1,  0,  0,  6,  4,  -4, 2,  10, 1,),SKL_BLUDGEONS,_club,ID_BATON,),
    # misc
"metal push dagger"     :(30,   0.3, 180, METL,3, 4, (3,  9,  15, 0,  0,  0,  90, 3,  -12,0,  12, 0.2,),SKL_PUSHDAGGERS,_pushDagger,ID_PUSHDAGGER,),
"crescent moon blade"   :(125,  0.3, 60,  METL,3, 14,(2,  4,  8,  1,  0,  0,  75, 6,  -4, 1,  4,  0.3,),None,_crescentBlade,ID_KNIFE,),
##"scissors katar"     :(25,   0.3, 180, METL,2,(3,  9,  15, 0,  0,  0,  90, 0,  -12,0,  4,),SKL_PUSHDAGGERS,_pushDagger,), 

    # 2-handed weapons #

# Some weapons can only be built with steel, like longswords, greatswords.
#   So these are expensive, and have no material designation.
    # longswords          $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,),TYPE,script,ID,
"bastard sword"         :(245,  1.55,300, METL,18,14,(4,  9,  12, 1,  1,  1,  15, 10, -5, 6,  24, 1.8,),SKL_LONGSWORDS,_bastardSword,ID_LONGSWORD,),#STEEL # weapon is a longsword but can be wielded in 1 hand (which it is by default due to the mechanics in this game (just by not having the TWOHANDS flag, it is a one-handed weapon that can be wielded with two hands alternatively.))
"longsword"             :(260,  1.6, 210, METL,10,12,(10, 12, 18, 5,  3,  3,  51, 10, -6, 12, 14, 2.2,),SKL_LONGSWORDS,_longSword,ID_LONGSWORD,),#STEEL
"kriegsmesser"          :(265,  1.8, 250, METL,14,8, (9,  14, 14, 2,  3,  3,  36, 12, -16,9,  18, 2,),SKL_LONGSWORDS,_kriegsmesser,ID_LONGSWORD,),#STEEL
"katana"                :(285,  1.45,80,  METL,8, 14,(11, 11, 16, 3,  2,  2,  45, 10, -12,14, 12, 1.6,),SKL_LONGSWORDS,_katana,ID_LONGSWORD,),#STEEL # VERY DIFFICULT TO FIND RECIPE FOR THIS/VERY DIFFICULT TO MAKE! SO VERY EXPENSIVE
"estoc"                 :(305,  1.65,100, METL,10,16,(12, 10, 20, 6,  1,  2,  60, 11, -12,16, 16, 2.4,),SKL_LONGSWORDS,_estoc,ID_LONGSWORD,),#STEEL
    # greatswords         $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,),TYPE,script,ID,
"greatsword"            :(540,  3.5, 450, METL,26,12,(9,  18, 15, 3,  3,  3,  -15,28, -6, 10, 32, 4,),SKL_GREATSWORDS,_greatSword,ID_GREATSWORD,),
"flamberge"             :(595,  3.3, 225, METL,24,14,(10, 16, 12, 2,  3,  3,  -12,28, -10,10, 26, 3.2,),SKL_GREATSWORDS,_flamberge,ID_GREATSWORD,),
    # short staves        $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,),TYPE,script,ID,
"plastic staff"         :(1.5,  1.5, 100, PLAS,11,10,(6,  5,  4,  2,  2,  2.5,66, 12, -7, 13, 13, 3,),SKL_STAVES,_staff,ID_STAFF,),
"wooden staff"          :(11,   1.3, 300, WOOD,9, 10,(7,  7,  6,  4,  4,  3,  75, 12, -5, 15, 12, 3,),SKL_STAVES,_staff,ID_STAFF,),
"bone staff"            :(20,   1.4, 200, WOOD,12,10,(5,  9,  7,  2,  4,  3,  51, 14, -3, 11, 18, 3,),SKL_STAVES,_staff,ID_STAFF,), # bone-headed staff (wooden staff with bone tip)
"metal staff"           :(30,   1.2, 250, WOOD,11,10,(6,  9,  8,  3,  4,  3,  66, 12, -5, 13, 15, 3,),SKL_STAVES,_staff,ID_STAFF,), # metal-headed staff (metal not tough enough to make a staff fully made of metal)
"steel staff"           :(142,  1.1, 500, METL,10,10,(8,  10, 9,  4,  3,  3,  81, 12, -5, 16, 11, 3,),SKL_STAVES,_staff,ID_STAFF,), # regular metal cannot make an entire staff shaft, but steel can.
    # longstaves          $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,),TYPE,script,ID,
"plastic longstaff"     :(3,    3.1, 150, PLAS,24,8, (9,  8,  6,  3,  2,  2,  54, 24, -18,5,  24, 6,),SKL_POLEARMS,_longstaff,ID_LONGSTAFF,),
"wooden longstaff"      :(24,   2.7, 400, WOOD,22,8, (10, 10, 8,  3,  4,  2.5,57, 24, -18,6,  22, 6,),SKL_POLEARMS,_longstaff,ID_LONGSTAFF,),
"steel longstaff"       :(88,   2.6, 500, METL,22,8, (11, 12, 10, 3,  3,  2.5,60, 24, -18,7,  20, 6,),SKL_POLEARMS,_longstaff,ID_LONGSTAFF,),
    # spears              $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,),TYPE,script,ID,
"plastic spear"         :(2,    2.1, 30,  PLAS,12,8, (8,  10, 10, 3,  2,  3,  51, 16, -12,8,  20, 4.1,),SKL_SPEARS,_pSpear,ID_SPEAR,),
"wooden spear"          :(20,   2.05,60,  WOOD,11,8, (10, 11, 12, 3,  3,  3,  48, 16, -12,9,  20, 4.1,),SKL_SPEARS,_wSpear,ID_SPEAR,),
"stone spear"           :(22,   2.15,100, WOOD,12,8, (9,  13, 13, 3,  3,  3,  42, 16, -12,9,  20, 4.1,),SKL_SPEARS,_bSpear,ID_SPEAR,),
"bone spear"            :(25,   2.05,150, WOOD,11,8, (10, 12, 14, 3,  3,  3,  45, 16, -12,10, 20, 4,),SKL_SPEARS,_sSpear,ID_SPEAR,),
"glass spear"           :(34,   1.9, 5,   WOOD,9, 12,(12, 22, 10, 3,  3,  3,  51, 16, -12,14, 18, 4,),SKL_SPEARS,_gSpear,ID_SPEAR,),
"metal spear"           :(32,   2.1, 200, WOOD,11,10,(11, 14, 16, 3,  3,  3,  45, 16, -12,12, 20, 4.2,),SKL_SPEARS,_mSpear,ID_SPEAR,),
"metal winged spear"    :(40,   2.15,300, WOOD,14,12,(10, 16, 15, 3,  3,  3.5,36, 16, -8, 12, 20, 4,),SKL_SPEARS,_mSpear,ID_SPEAR,),
"ceramic spear"         :(36,   1.95,10,  WOOD,9, 12,(12, 24, 12, 3,  3,  3,  48, 16, -12,14, 18, 4,),SKL_SPEARS,_cSpear,ID_SPEAR,),
    # partizans           $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,),TYPE,script,ID,
"metal partizan"        :(65,   2.2, 240, WOOD,14,6, (8,  18, 14, 2,  3,  3,  24, 20, -12,10, 22, 5,),SKL_SPEARS,_mPartizan,ID_SPEAR,),
    # naginatas           $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,),TYPE,script,ID,
"metal naginata"        :(80,   2.6, 120, WOOD,18,10,(9,  12, 13, 2,  3,  2,  15, 24, -14,8,  26, 5,),SKL_SPEARS,_mNaginata,ID_SPEAR,),
    # bills               $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,),TYPE,script,ID,
"metal bill"            :(110,  2.2, 80,  WOOD,16,14,(12, 14, 18, 2,  3,  2,  24, 28, -4, 10, 22, 4.5,),SKL_POLEARMS,_mBill,ID_POLEARM,),#requires some steel
    # halberds            $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,),TYPE,script,ID,
"metal halberd"         :(135,  2.25,280, WOOD,15,12,(8,  18, 20, 2,  3,  2,  9,  28, -6, 8,  22, 5.3,),SKL_POLEARMS,_mHalberd,ID_POLEARM,),
    # poleaxes            $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,),TYPE,script,ID,
"metal poleaxe"         :(150,  2.35,450, WOOD,14,13,(7,  22, 20, 2,  4,  2,  -15,12, -4, 6,  24, 3,),SKL_GREATAXES,_mPoleAxe,ID_GREATAXE,),
    # polehammers         $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,),TYPE,script,ID,
"plastic polehammer"    :(3,    2.7, 110, PLAS,18,9, (4,  11, 16, 1,  2,  2,  -27,12, -9, 3,  30, 2.5,),SKL_MALLETS,_pPoleHammer,ID_GREATHAMMER,),
"wooden polehammer"     :(18,   2.6, 200, WOOD,17,10,(5,  13, 16, 1,  3,  2,  -24,12, -9, 4,  28, 2.5,),SKL_MALLETS,_wPoleHammer,ID_GREATHAMMER,),
"metal polehammer"      :(105,  2.4, 675, WOOD,16,11,(6,  16, 24, 1,  3,  2,  -21,12, -9, 5,  26, 2.5,),SKL_MALLETS,_mPoleHammer,ID_GREATHAMMER,),
    # war mallets         $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,),TYPE,script,ID,
"plastic war mallet"    :(3,    2.4, 320, PLAS,16,3, (3,  11, 12, -1, 2,  2,  -45,14, -14,3,  28, 2,),SKL_MALLETS,_1mallet,ID_GREATHAMMER,),
"wooden war mallet"     :(19,   2.3, 600, WOOD,16,3, (4,  13, 13, -1, 3,  2,  -42,14, -14,4,  25, 2,),SKL_MALLETS,_1mallet,ID_GREATHAMMER,),
"stone war mallet"      :(22,   2.1, 400, WOOD,15,3, (5,  17, 14, 0,  3,  2,  -36,14, -14,4,  25, 2,),SKL_MALLETS,_1mallet,ID_GREATHAMMER,),
"bone war mallet"       :(25,   2.2, 500, WOOD,15,3, (4,  15, 15, 0,  3,  2,  -39,14, -14,5,  25, 2,),SKL_MALLETS,_1mallet,ID_GREATHAMMER,),
"metal war mallet"      :(72,   2.0, 950, WOOD,15,3, (5,  19, 16, 0,  4,  2,  -39,14, -14,6,  22, 2,),SKL_MALLETS,_2mallet,ID_GREATHAMMER,),
    # great clubs         $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,),TYPE,script,ID,
"plastic great club"    :(3,    2.7, 450, PLAS,26,2, (5,  11, 7,  -2, 2,  2,  -33,16, -26,2,  32, 1.4,),SKL_BLUDGEONS,_heavyClub,ID_GREATCLUB,),
"wooden great club"     :(18,   2.6, 1000,WOOD,24,2, (6,  15, 9,  -2, 3,  2,  -27,16, -26,3,  29, 1.4,),SKL_BLUDGEONS,_heavyClub,ID_GREATCLUB,),
"stone great club"      :(22,   2.5, 280, STON,26,2, (7,  19, 10, -2, 3,  2,  -24,16, -26,4,  29, 1.0,),SKL_BLUDGEONS,_heavyClub,ID_GREATCLUB,),
"bone great club"       :(13,   1.75,360, BONE,22,2, (8,  14, 9,  -1, 3,  2,  -15,16, -26,5,  26, 1.2,),SKL_BLUDGEONS,_heavyClub,ID_GREATCLUB,),
"metal great club"      :(95,   1.8, 1900,METL,24,2, (8,  21, 12, -1, 3,  2,  -18,16, -26,6,  26, 1.2,),SKL_BLUDGEONS,_heavyClub,ID_GREATCLUB,),
    # great axes          $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,),TYPE,script,ID,
"plastic great axe"     :(3,    2.2, 110, PLAS,14,8, (2,  14, 9,  1,  2,  2,  -27,16, -6, 3,  24, 2.5,),SKL_GREATAXES,_pGreatAxe,ID_GREATAXE,),
"wooden great axe"      :(22,   1.9, 210, WOOD,12,8, (3,  18, 10, 2,  3,  2,  -21,16, -6, 4,  23, 2.5,),SKL_GREATAXES,_wGreatAxe,ID_GREATAXE,),
"stone great axe"       :(15,   2.0, 230, WOOD,12,9, (3,  24, 12, 1,  3,  2,  -27,16, -6, 5,  23, 2.5,),SKL_GREATAXES,_sGreatAxe,ID_GREATAXE,),
"bone great axe"        :(34,   1.85,290, WOOD,12,9, (3,  22, 11, 2,  3,  2,  -21,16, -6, 6,  22, 2.5,),SKL_GREATAXES,_bGreatAxe,ID_GREATAXE,),
"glass great axe"       :(75,   1.65,10,  WOOD,12,11,(5,  32, 10, 2,  3,  2,  -12,16, -6, 7,  18, 2.5,),SKL_GREATAXES,_gGreatAxe,ID_GREATAXE,),
"metal great axe"       :(92,   1.8, 420, WOOD,12,10,(4,  28, 14, 2,  3,  2,  -24,16, -6, 8,  20, 2.5,),SKL_GREATAXES,_mGreatAxe,ID_GREATAXE,),
    # battleaxes          $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,),TYPE,script,ID,
    # misc 2-h weapons    $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,),TYPE,script,ID,
"dane axe"              :(275,  1.6, 300, WOOD,10,12,(6,  22, 12, 3,  3,  3,  6,  12, -2, 12, 16, 2,),SKL_GREATAXES,_daneAxe,ID_GREATAXE,),#STEEL and IRON
"executioner sword"     :(380,  3.1, 665, METL,28,4, (2,  20, 8,  0,  4,  1,  -45,22, -12,1,  32, 2.4,),SKL_LONGSWORDS,_executionerSword,ID_GREATSWORD,),#POOR STEEL

# TOOLS #

# misc                    $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,),TYPE,script,ID,
'scalpel'               :(30,   0.02,10,  METL,1, 10,(0,  3,  12, 0,  0,  0,  0,  2,  -9, 0,  4,  0,),SKL_MEDICINE,_scalpel,ID_SCALPEL,),
"sharpening stone"      :(10,   2.5, 200, STON,24,8, (0,  3,  3,  0,  0,  0,  -60,3,  -12,0,  24, 0,),None,_sChunk,ID_WHETSTONE,),
# scissors                $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,),TYPE,script,ID,
'scissors'              :(11,   0.16,140, METL,1, 8, (0,  4,  5,  0,  0,  0,  0,  2,  -9, 0,  8,  0,),None,_scissors,ID_SCISSORS,),
# pliers                  $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,),TYPE,script,ID,
'pliers'                :(24,   0.3, 650, METL,3, 6, (-2, 2,  4,  0,  0,  0,  -36,2,  -9, 0,  8,  0,),None,_pliers,ID_PLIERS,),
'needle-nose pliers'    :(32,   0.3, 500, METL,2, 6, (-2, 1,  3,  0,  0,  0,  -36,2,  -9, 0,  8,  0,),None,_needleNosePliers,ID_PLIERS,),
# screwdrivers            $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,),TYPE,script,ID,
'metal screwdriver'     :(16,   0.25,250, METL,3, 4, (0,  3,  4,  0,  0,  0,  0,  2,  -9, 0,  8,  0,),None,_screwdriver,ID_SCREWDRIVER,),
# shovels                 $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,),TYPE,script,ID,
"metal shovel"          :(45,   1.8, 400, WOOD,20,2, (-2, 10, 8,  0,  2,  1,  -60,12, -8, 0,  24, 2.6,),None,_mShovel,ID_SHOVEL,),
# pickaxes                $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,),TYPE,script,ID,
"metal pickaxe"         :(59,   1.4, 800, WOOD,16,6, (-8, 12, 14, 0,  2,  0.5,-84,14, -6, 0,  36, 1.4,),None,_mPickaxe,ID_PICKAXE,),
# hammers                 $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,),TYPE,script,ID,
"plastic hammer"        :(1.5,  1.4, 200, PLAS,14,2, (1,  3,  6,  0,  0,  0,  -15,4,  -10,0,  18, 1,),SKL_HAMMERS,_1hammer,ID_HAMMER,),
"wooden hammer"         :(12,   1.3, 260, WOOD,13,2, (1,  4,  7,  0,  0,  0,  -12,4,  -8, 0,  17, 1,),SKL_HAMMERS,_2hammer,ID_HAMMER,),
"stone hammer"          :(8,    1.2, 300, WOOD,12,4, (1,  5,  8,  0,  0,  0,  -12,4,  -8, 0,  16, 1,),SKL_HAMMERS,_2hammer,ID_HAMMER,),
"bone hammer"           :(16,   1.1, 350, WOOD,11,4, (1,  4,  9,  0,  0,  0,  -9, 4,  -6, 0,  16, 1,),SKL_HAMMERS,_2hammer,ID_HAMMER,),
"metal hammer"          :(44,   1.0, 500, WOOD,10,6, (2,  7,  11, 0,  0,  0,  -9, 4,  -4, 0,  15, 1,),SKL_HAMMERS,_3hammer,ID_HAMMER,),
"metal smithing hammer" :(95,   1.6, 990, METL,16,8, (2,  7,  11, 0,  0,  0,  -9, 4,  -10,0,  20, 1,),SKL_HAMMERS,_4hammer,ID_HAMMER,),
"fine metal hammer"     :(165,  2.0, 750, METL,20,10,(2,  8,  12, 0,  0,  0,  -51,4,  -12,0,  32, 1,),SKL_HAMMERS,_5hammer,ID_HAMMER,),
# axes                    $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,),TYPE,script,ID,
"plastic axe"           :(4,    1.9, 80,  PLAS,18,3, (0,  6,  4,  0,  0,  0,  -51,7,  -5, 0,  18, 1,),SKL_AXES,_pAxe,ID_AXE,),
"wooden axe"            :(22,   1.8, 120, WOOD,17,4, (0,  8,  5,  0,  0,  0,  -48,7,  -5, 0,  17, 1,),SKL_AXES,_wAxe,ID_AXE,),
"stone axe"             :(18,   1.75,200, WOOD,16,5, (0,  10, 6,  0,  0,  0,  -42,7,  -5, 0,  17, 1,),SKL_AXES,_sAxe,ID_AXE,),
"bone axe"              :(26,   1.85,160, WOOD,16,6, (0,  9,  6,  0,  0,  0,  -45,7,  -5, 0,  18, 1,),SKL_AXES,_bAxe,ID_AXE,),
"metal axe"             :(42,   1.7, 420, WOOD,15,8, (1,  12, 7,  0,  0,  0,  -36,7,  -5, 0,  16, 1,),SKL_AXES,_mAxe,ID_AXE,),
# machetes                $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,),TYPE,script,ID,
"plastic machete"       :(5,    1.8, 70,  PLAS,17,6, (2,  3,  3,  0,  0,  0,  3,  7,  -7, 0,  20, 1,),SKL_SWORDS,_pMachete,ID_MACHETE,),
"wooden machete"        :(13,   1.7, 90,  WOOD,16,7, (3,  4,  5,  0,  0,  0,  6,  7,  -7, 0,  18, 1,),SKL_SWORDS,_wMachete,ID_MACHETE,),
"bone machete"          :(16,   1.6, 60,  BONE,15,8, (3,  5,  7,  0,  0,  0,  9,  5,  -7, 0,  14, 1,),SKL_SWORDS,_bMachete,ID_MACHETE,),
"metal machete"         :(20,   1.5, 260, METL,14,9, (4,  6,  9,  1,  0,  0,  15, 5,  -7, 0,  14, 1,),SKL_SWORDS,_mMachete,ID_MACHETE,),
}
    

# armor #


##NECKWEAR={
###--Name-------------------$$$$$, KG,  Dur, Mat, (DV, AV, Pro,Vis,Enc,FIR,ICE,BIO,ELE,PHS,BLD),script
##"scarf"                 :(9,     0.5, 80,  CLTH,(0,  0,  0,  0,  0,  -12,12, 3,  0,  0,  0,),_scarf,),
##}

EYEWEAR={
#--Name-------------------$$$$$,KG,  Dur,AP,  Mat, S, (DV, AV, Pro,Enc,FIR,ICE,BIO,ELE,PHS,BLD,LGT,SND,Vis),script,ID,
"safety goggles"        :(15,   0.1, 12, 200, PLAS,0, (0,  0,  0.1,2,  0,  0,  21, 3,  0,  0,  200,0,  0.8,),_pGoggles,ID_SAFETYGOGGLES,),
"glasses"               :(7,    0.04,10, 100, GLAS,0, (0,  0,  0,  12, 0,  0,  9,  0,  0,  0,  50, 0,  0.9,),_glasses,ID_GLASSES,),
"sunglasses"            :(2,    0.06,3,  100, PLAS,0, (0,  0,  0,  12, 0,  0,  12, 0,  0,  0,  400,0,  0.666667,),_glasses,ID_SUNGLASSES,),
"laser goggles lv.1"    :(20,   0.04,6,  100, PLAS,0, (0,  0,  0,  6,  0,  0,  15, 0,  0,  0,  800,0,  0.5,),_glasses,ID_SUNGLASSES,),
"laser goggles lv.2"    :(105,  0.06,12, 100, PLAS,0, (0,  0,  0,  6,  0,  0,  12, 0,  0,  0, 1600,0,  0.3,),_glasses,ID_SUNGLASSES,),
"laser goggles lv.3"    :(260,  0.08,24, 100, PLAS,0, (0,  0,  0,  6,  0,  0,  12, 0,  0,  0, 3200,0,  0.2,),_glasses,ID_SUNGLASSES,),
}

FACEWEAR={
# Per : perception (vision AND hearing) (percentage modifier)
# E: covers eyes? bool (0 or 1)
    
#--Name-------------------$$$$$, KG,  Dur, AP,  Mat, S, (DV, AV, Pro,Enc,FIR,ICE,BIO,ELE,PHS,BLD,LGT,SND,Vis,)E,script,ID,
"flesh mask"            :(25,    0.9, 15,  200, FLSH,2, (0,  0.1,0.8,3,  0,  1,  12, 0,  0,  6,  10, 0,  0.9,),1,_fMask,ID_MASK,),# grants intimidation when you wear any armor but esp. if you wear flesh armor and the flesh face is the scariest of all
"bandana"               :(2,     0.05,10,  300, CLTH,0, (0,  0.0,0.1,1,  3,  0,  33, 0,  0,  0,  0,  0,  1,  ),0,_bandana,ID_RAG,),
"leather mask"          :(40,    0.8, 90,  200, LETH,2, (0,  0.6,1.2,3,  3,  1,  6,  6,  0,  3,  20, 0,  0.8,),1,_lMask,ID_MASK,),
"boiled leather mask"   :(62,    0.7, 150, 200, BOIL,2, (1,  1.0,1.6,3,  6,  1,  6,  9,  0,  3,  20, 0,  0.8,),1,_blMask,ID_MASK,),
"plastic mask"          :(1,     1.5, 30,  200, PLAS,4, (-1, 0.8,0.6,3,  -6, 0,  3,  3,  0,  0,  30, 0,  0.5,),1,_pMask,ID_MASK,),#"made of a translucent plastic, this mask allows the wearer to see through it while providing some protection.
"plastic respirator"    :(14,    1.4, 20,  400, PLAS,6, (-2, 0.8,0.7,6,  -6, 0,  51, 3,  0,  0,  30, 0,  0.5,),1,_respirator,ID_RESPIRATOR,),#mask with added breathing filter for added bio resistance.
"plastic bio mask"      :(25,    1.5, 15,  400, PLAS,8, (-2, 0.8,0.8,9,  3,  1,  90, 3,  0,  0,  30, 0,  0.5,),1,_respirator,ID_RESPIRATOR,),#respirator with a plastic or glass eye-covering for added bio resistance.
"plague mask"           :(95,    1.7, 60,  800, LETH,8, (-4, 0.8,1.0,12, 3,  3,  180,9,  0,  3,  50, 0,  0.2,),1,_plagueMask,ID_PLAGUEMASK,),
"gas mask"              :(1200,  2.5, 80,  400, PLAS,10,(-2, 0.5,1.8,6,  15, 3,  300,6,  1,  0,  50, 0,  0.5,),1,_gasMask,ID_GASMASK,),#a pre-apocalypse bio mask made of fire resistant material.
"kevlar mask"           :(2750,  0.5, 200, 200, PLAS,2, (2,  1.4,2.4,1,  3,  0,  6,  3,  3,  3,  20, 0,  0.8,),1,_kMask,ID_MASK,),
"wooden mask"           :(20,    0.8, 50,  200, WOOD,4, (0,  0.5,1.0,3,  -6, 0,  6,  0,  0,  0,  40, 0,  0.5,),1,_wMask,ID_MASK,),
"metal mask"            :(130,   0.7, 320, 300, METL,4, (0,  1.7,2.0,3,  -6, -1, 6,  -9, 0,  0,  50, 0,  0.5,),1,_mMask,ID_MASK,),
"metal respirator"      :(160,   1.7, 120, 400, METL,6, (-2, 1.7,2.0,6,  0,  -1, 60, 0,  1,  0,  50, 0,  0.5,),1,_mRespirator,ID_RESPIRATOR,),
"metal bio mask"        :(175,   1.8, 100, 400, METL,8, (-2, 1.7,2.0,9,  6,  2,  99, 0,  1,  0,  50, 0,  0.5,),1,_mRespirator,ID_RESPIRATOR,),#bio masks are respirators with a visor for eye protection
"metal welding mask"    :(85,    1.2, 150, 200, METL,8, (-2, 3.0,1.0,6,  -6, -6, 30, -12,0,  2,  400,0,  0.1,),1,_mHelm,ID_WELDINGMASK,),
}

HEADWEAR={
##    cap covers top of head only; low protection.
##    helmet covers up to: top and sides of head and neck
##    helm covers the whole head and face
##    globe helm is a full helm but it has a plastic face which
##      has a low vision penalty, at cost of reduced protection.
##    bio helm is like a globe helm with a respirator attached.

# Per : perception (vision AND hearing) (multiplier modifier)
# F: covers face? bool (0 or 1)
# E: covers eyes? bool (0 or 1)
# R: covers ears? bool (0 or 1)
# N: covers neck? bool (0 or 1)
#--Name-------------------$$$$$,KG,  Dur, AP,  Mat, S, (DV, AV,  Pro, Enc,FIR,ICE,BIO,ELE,PHS,BLD,LGT,SND,Vis,),F,E,R,N,script,ID,
"flesh cap"             :(6,    1.7, 20,  100, FLSH,6, (0,  0.5, 0.9, 3,  -6, 5,  0,  0,  0,  3,  0,  0,  1,  ),0,0,0,0,_fCap,ID_HELMET,),
"padded coif"           :(18,   1.2, 60,  200, CLTH,2, (0,  1.1, 1.9, 2,  -3, 3,  3,  0,  0,  3,  0,  20, 1,  ),0,0,1,0,_cCoif,ID_PADDEDCOIF,),
"thick padded coif"     :(32,   2.0, 120, 200, CLTH,6, (1,  2.2, 2.2, 2,  -6, 6,  6,  3,  3,  3,  0,  40, 1,  ),0,0,1,0,_cCoif,ID_PADDEDCOIF,),
"plastic cap"           :(2,    2.1, 90,  100, PLAS,6, (0,  1.9, 1.1, 3,  -9, 0,  0,  6,  0,  0,  0,  0,  1,  ),0,0,0,0,_pCap,ID_HELMET,),
"plastic helmet"        :(4,    3.2, 50,  200, PLAS,10,(-1, 2.0, 2.0, 4,  -12,2,  6,  9,  0,  0,  20, 10, 0.9,),0,0,1,0,_pHelm,ID_HELMET,),
"plastic helm"          :(12,   4.2, 80,  400, PLAS,12,(-2, 2.2, 3.0, 4,  -18,3,  12, 12, 0,  0,  50, 10, 0.5,),1,1,1,0,_pHelm,ID_HELMET,),
"plastic globe helm"    :(14,   3.7, 40,  800, PLAS,12,(-3, 1.6, 2.5, 5,  -24,5,  39, 18, 0,  0,  10, 10, 0.8,),1,1,1,0,_pHelm,ID_BIOHELM,),
"plastic bio helm"      :(30,   4.0, 20,  500, PLAS,14,(-4, 1.5, 2.5, 6,  -12,6,  78, 18, 0,  0,  10, 10, 0.8,),1,1,1,0,_bioHelm,ID_BIOHELM,), # may not fuck up your heat res that much but it can catch fire while on your face, which will definitely fuck you up pretty much regardless of your heat res.
"kevlar cap"            :(4550, 1.0, 300, 100, PLAS,4, (2,  3.0, 2.2, 1.5,3,  0,  0,  3,  5,  1,  0,  0,  1,  ),0,0,0,0,_kCap,ID_HELMET,),
"leather cap"           :(32,   2.0, 60,  100, LETH,4, (1,  1.6, 1.0, 2,  -6, 2,  0,  6,  0,  1,  0,  0,  1,  ),0,0,0,0,_lCap,ID_HELMET,),
"boiled leather cap"    :(46,   1.8, 120, 100, LETH,4, (1,  2.8, 1.2, 2,  -3, 2,  0,  9,  0,  1,  0,  0,  1,  ),0,0,0,0,_lCap,ID_HELMET,),
"skull cap"             :(26,   2.3, 110, 100, BONE,6, (-1, 3.2, 1.2, 3,  0,  1,  0,  6,  0,  0,  0,  0,  1,  ),0,0,0,0,_bCap,ID_HELMET,),
"bone helmet"           :(35,   2.8, 125, 300, BONE,8, (-2, 3.2, 2.0, 4,  3,  2,  3,  9,  0,  0,  10, 10, 0.9,),0,0,1,0,_bHelm,ID_HELMET,),
"pop tab mail coif"     :(65,   2.1, 175, 200, METL,6, (0,  3.5, 2.2, 3,  -3, 0,  3,  -6, 1,  3,  0,  20, 1,  ),0,0,1,0,_mCoif,ID_MAILCOIF,),
"metal mail coif"       :(220,  2.9, 315, 200, METL,8, (1,  4.1, 2.4, 3,  -3, 0,  3,  -6, 1,  3,  0,  20, 1,  ),0,0,1,0,_mCoif,ID_MAILCOIF,),
"metal cap"             :(145,  2.4, 650, 100, METL,8, (0,  5.0, 1.4, 3,  -6, -2, 0,  -6, 0,  1,  0,  0,  1,  ),0,0,0,0,_mCap,ID_HELMET,),
"metal blast cap"       :(385,  6.2, 900, 100, METL,22,(-4, 10,  2.0, 5,  -9, -15,0,  -9, 0,  1,  0,  100,0.9,),0,0,1,0,_mCap,ID_HELMET,),
"metal helmet"          :(255,  3.6, 420, 200, METL,12,(-1, 5.2, 3.2, 3,  -18,-3, 3,  -12,0,  2,  20, 0,  0.9,),0,0,1,0,_mHelm,ID_HELMET,),
"metal helm"            :(420,  4.5, 550, 400, METL,14,(-2, 5.5, 4.0, 4,  -24,-6, 6,  -15,3,  2,  50, 0,  0.5,),1,1,1,0,_mHelm,ID_HELM,),#can lower the visor for -2 protection, +1 DV, +3 FIR, Perception penalty cut to 1/4; 
"metal globe helm"      :(475,  4.0, 240, 800, METL,14,(-3, 4.5, 2.8, 5,  -36,0,  45, -9, 0,  2,  10, 0,  0.8,),1,1,1,0,_mHelm,ID_BIOHELM,),#"the globe hat has a see-through plastic visor that provides decent protection to vision ratio"
"metal bio helm"        :(400,  4.4, 200, 1000,METL,16,(-4, 4.3, 2.6, 6,  -24,2,  90, -6, 0,  2,  10, 0,  0.8,),1,1,1,0,_mBioHelm,ID_BIOHELM,),#"the globe hat has a see-through plastic visor that provides decent protection to vision ratio. This globe helm has an attached respirator for increased BIO and FIR resistance."
"metal full helm"       :(750,  5.0, 600, 1000,METL,18,(-6, 5.8, 5.2, 5,  -24,-9, 18, -18,3,  3,  100,0,  0.2,),1,1,1,1,_mFullHelm,ID_HELM,),#can lower the visor for -2 protection, +1 DV, +3 FIR, Perception penalty cut to 1/4; exchangeable/removable visor
"motorcycle helmet"     :(830,  1.0, 50,  300, PLAS,4, (1,  2.4, 3.5, 3,  -3, 3,  24, 9,  3,  1,  50, 30, 0.8,),1,1,1,0,_motorcycleHelm,ID_MOTORCYCLEHELM,),
"graphene helm"         :(18000,1.3, 560, 500, CARB,5, (2.5,8.0, 6.0, 1.5,18, 12, 36, 15, 3,  6,  50, 60, 0.8,),1,1,1,0,_grHelm,ID_MOTORCYCLEHELM,),
}
     
'''
armor type:
    shirt : typical thin clothing
        - basically not even armor, the worst protection
    coat : expensive high-coverage (protection) clothing
        - little step up from shirt, but very expensive for the armor value.
    vest : typical thick (high AV) clothing or low-coverage armor
        - little step up from shirt, or a light armor type
    gear : lamellar / scaled armor
        - low protection and resistances; low cost (medium Msp and DV penalty)
    armor : plated armor
        - medium protection and resistances; medium cost (heaviest Msp and DV penalty)
    mail shirt : ringmail
        - lightest, lowest dur, med-low AV, med-high prot.; med-low cost.  Also gives Phys res. (Like armor but weaker and lighter.)
    jacket : typical full-cover clothing or light armor
        - high protection and resistances; high cost (med Msp and DV penalty)
    suit : full body armor, highest coverage
        - highest protection and resistances; highest cost (lowest Msp and DV penalty). +Phys res.
'''
'''
    idea: function for creating mail-reinforced armor
        adds protection and armor
        adds mass, value
'''
# B - covers back?
# C - covers core?
# H - covers hips?
# A - covers arms?
ARMOR={
    # ceramics (ceramic armor is DIFFICULT to make)
#--Name-------------------$$$$$, KG,   Dur, AP,   Mat, S, (DV, AV, Pro,Enc,FIR,ICE,BIO,ELE,PHS,BLD),(B,C,H,A,),script,ID,
"ceramic armor"         :(2310,  12.25,20,  600,  CERA,12,(1,  15, 3,  2,  -15,0,  3,  3,  3,  9, ),(1,1,1,0,),None,ID_ARMOR,),
"ceramic gear"          :(3090,  13.6, 60,  2400, CERA,12,(2,  15, 5,  2,  -15,0,  6,  3,  3,  9, ),(1,1,1,0,),None,ID_GEAR,),# padded jacket interlaced with ceramic tiles, grants very good defense against one powerful blow before it shatters, rendering it useless to repeated assault.
    # cloth
#--Name-------------------$$$$$, KG,   Dur, AP,   Mat, S, (DV, AV, Pro,Enc,FIR,ICE,BIO,ELE,PHS,BLD),(B,C,H,A,),script,ID,
"t-shirt"               :(5,     0.15, 10,  100,  CLTH,0, (0,  0,  0,  5,  -9, 3,  3,  0,  0,  1, ),(0,0,0,0,),_clothes,ID_SHIRT,),
"hoody"                 :(14,    0.8,  30,  300,  CLTH,0, (0,  0,  1,  4,  -24,9,  6,  0,  0,  2, ),(0,0,0,0,),_clothes,ID_HOODY,),
"cloth vest"            :(19,    1.0,  40,  200,  CLTH,0, (1,  0,  1,  2,  -12,6,  3,  0,  0,  3, ),(1,0,0,0,),None,ID_VEST,),
"wool jacket"           :(69,    2.0,  160, 300,  CLTH,1, (1,  1,  3,  3,  -36,36, 6,  2,  0,  6, ),(1,1,0,0,),None,ID_JACKET,),
"padded vest"           :(28,    1.6,  120, 300,  CLTH,1 ,(2,  1,  2,  2,  -6, 12, 3,  1,  0,  3, ),(1,0,0,0,),None,ID_PADDEDSHIRT),
"padded jacket"         :(39,    2.1,  150, 600,  CLTH,2, (2,  2,  5,  2,  -12,18, 6,  3,  1,  12,),(1,1,0,0,),None,ID_PADDEDLONGSHIRT,),
"padded jack"           :(56,    3.1,  275, 700,  CLTH,2, (3,  3,  6,  2,  -21,24, 9,  6,  3,  15,),(1,1,0,0,),None,ID_PADDEDLONGSHIRT,),
"gambeson"              :(75,    4.1,  400, 800,  CLTH,3, (4,  4,  8,  2,  -30,30, 9,  12, 5,  18,),(1,1,0,0,),None,ID_PADDEDLONGSHIRT,),
    # flesh and fur
#--Name-------------------$$$$$, KG,   Dur, AP,   Mat, S, (DV, AV, Pro,Enc,FIR,ICE,BIO,ELE,PHS,BLD),(B,C,H,A,),script,ID,
"flesh armor"           :(75,    12.5, 80,  800,  FLSH,10,(1,  2,  5,  3.5,-6, 9,  6,  3,  0,  9, ),(1,1,1,0,),None,ID_ARMOR,),
"flesh suit"            :(110,   18.3, 50,  4000, FLSH,16,(2,  2,  8,  3.5,-12,21, 9,  3,  3,  15,),(1,1,1,1,),None,ID_SUIT,),
"fur coat"              :(95,    2.85, 25,  300,  FLSH,4, (-3, 0.6,2,  3.5,-42,60, 9,  9,  0,  0, ),(1,0,0,1,),None,ID_JACKET,),
"fur cuirass"           :(265,   15.85,115, 600,  FLSH,14,(0,  3,  5,  3,  -33,21, 9,  9,  0,  9, ),(1,1,0,0,),None,ID_CUIRASS,),
"fur suit"              :(475,   21.5, 60,  4000, FLSH,18,(-2, 3,  7,  4,  -51,75, 12, 15, 0,  15,),(1,1,1,1,),None,ID_FURSUIT,),#"no, not _that_ type of fur suit. ...ok, it basically is that type of fur suit. But it's not a sexual thing! At least, that wasn't it's original intended purpose, which was definitely combat and... ok, maybe it was a sexual thing. Oh, just get out of here, you weirdo! Just kidding, I wuv you UwU " 
    # leather and boiled leather
#--Name-------------------$$$$$, KG,   Dur, AP,   Mat, S, (DV, AV, Pro,Enc,FIR,ICE,BIO,ELE,PHS,BLD),(B,C,H,A,),script,ID,
"leather jacket"        :(100,   4.0,  40,  200,  LETH,4, (1,  1,  10, 3,  -12,15, 12, 15, 5,  8, ),(1,0,0,1,),None,ID_JACKET,),
"leather biker jacket"  :(220,   9.0,  90,  300,  LETH,8, (2,  2,  12, 3,  -21,30, 12, 18, 10, 15,),(1,0,0,1,),None,ID_JACKET,),
"boiled leather cuirass":(600,   22.5, 220, 1200, LETH,16,(2,  5,  4,  2,  -6, 15, 9,  33, 3,  5, ),(1,1,0,0,),None,ID_CUIRASS,),
"boiled leather gear"   :(660,   13.3, 260, 2000, LETH,12,(3,  4,  6,  2,  -9, 9,  9,  36, 3,  5, ),(1,1,1,0,),None,ID_GEAR,),
"cuir bouilli"          :(1025,  26.4, 410, 3200, LETH,18,(-2, 8,  7,  2.5,-36,51, 15, -6, 3,  21,),(1,1,1,0,),None,ID_CUIRASS,),
    # plastic
#--Name-------------------$$$$$, KG,   Dur, AP,   Mat, S, (DV, AV, Pro,Enc,FIR,ICE,BIO,ELE,PHS,BLD),(B,C,H,A,),script,ID,
"plastic cuirass"       :(43,    20.2, 100, 1200, PLAS,14,(-1, 4,  3,  2,  -30,3,  -6, 21, 0,  3, ),(1,1,0,0,),None,ID_CUIRASS,),
"plastic gear"          :(36,    13.5, 80,  2200, PLAS,10,(0,  3,  4,  2,  -45,3,  -9, 21, 0,  3, ),(1,1,1,0,),None,ID_GEAR,),
"disposable PPE"        :(25,    8.2,  10,  300,  PLAS,6, (-4, 0,  0,  4,  -12,6,  30, 9,  0,  0, ),(1,1,1,1,),None,ID_PPE,),
"hazard suit"           :(1120,  14.5, 25,  600,  PLAS,12,(-4, 1,  2,  3,  -30,15, 45, 12, 3,  0, ),(1,1,1,1,),None,ID_HAZARDSUIT,),# some items that cannot be easily crafted with modern (post-apocalypse) technology are very expensive, being rare.
"kevlar vest"           :(16200, 2.6,  275, 400,  PLAS,3, (4,  5,  10, 1.5,3,  3,  6,  6,  20, 5, ),(1,0,0,0,),None,ID_BULLETPROOFVEST,),
    # wood
#--Name-------------------$$$$$, KG,   Dur, AP,   Mat, S, (DV, AV, Pro,Enc,FIR,ICE,BIO,ELE,PHS,BLD),(B,C,H,A,),script,ID,
"wicker armor"          :(61,    12.3, 40,  1000, WOOD,10,(0,  2,  2,  2.5,-45,0,  3,  3,  0,  0, ),(1,1,1,0,),None,ID_ARMOR,),
"wooden gear"           :(115,   15.25,100, 2000, WOOD,12,(2,  3,  4,  2,  -30,3,  6,  6,  0,  3, ),(1,1,1,0,),None,ID_GEAR,),
    # bone
#--Name-------------------$$$$$, KG,   Dur, AP,   Mat, S, (DV, AV, Pro,Enc,FIR,ICE,BIO,ELE,PHS,BLD),(B,C,H,A,),script,ID,
"bone cuirass"          :(380,   25.3, 160, 1200, BONE,18,(0,  6,  3,  2,  3,  6,  15, 21, 0,  5, ),(1,1,0,0,),None,ID_CUIRASS,),
"bone gear"             :(100,   16.8, 240, 2400, BONE,14,(2,  4,  5,  2,  6,  6,  12, 18, 0,  5, ),(1,1,1,0,),None,ID_GEAR,),
    # metal
#--Name-------------------$$$$$, KG,   Dur, AP,   Mat, S, (DV, AV, Pro,Enc,FIR,ICE,BIO,ELE,PHS,BLD),(B,C,H,A,),script,ID,
"pop tab mail vest"     :(350,   12.3, 215, 800,  METL,12,(2,  6,  5,  2,  -3, 0,  9,  0,  3,  15,),(1,1,0,0,),None,ID_MAILSHIRT,),
"pop tab mail shirt"    :(415,   14.7, 265, 800,  METL,14,(2,  6,  7,  2,  -3, 3,  9,  -3, 3,  18,),(1,1,1,0,),None,ID_MAILLONGSHIRT,),
"metal mail vest"       :(745,   11.2, 350, 800,  METL,11,(2,  7,  6,  2,  -12,0,  9,  -3, 3,  15,),(1,1,0,0,),None,ID_MAILSHIRT,),
"metal mail shirt"      :(1020,  15.6, 400, 800,  METL,13,(3,  7,  8,  2,  -21,3,  9,  -6, 5,  18,),(1,1,1,0,),None,ID_MAILLONGSHIRT,),# todo: make this separable into its constituent parts (gambeson + mail shirt) OR should there be a separate slot for gambeson and mail?
"metal gear"            :(820,   14.4, 510, 2400, METL,12,(1,  8,  5,  2,  -30,-12,12, -12,3,  12,),(1,1,1,0,),None,ID_GEAR,),
"brigandine"            :(915,   13.5, 550, 1200, METL,12,(1,  9,  4,  2,  -27,3,  9,  -6, 3,  9, ),(1,1,0,0,),None,ID_GEAR,),
"metal cuirass"         :(1370,  22.9, 600, 1800, METL,16,(0,  12, 6,  2,  -30,-15,9,  -21,3,  12,),(1,1,0,0,),None,ID_CUIRASS,),
"metal blast plate"     :(2040,  34.0, 1290,2400, METL,28,(-3, 20, 4,  3,  -45,-30,9,  -33,5,  12,),(1,1,0,0,),None,ID_CUIRASS,),
    # carbon
#--Name-------------------$$$$$, KG,   Dur, AP,   Mat, S, (DV, AV, Pro,Enc,FIR,ICE,BIO,ELE,PHS,BLD),(B,C,H,A,),script,ID,
"graphene armor"        :(75000, 5.0,  750, 1200, CARB,6, (4,  20, 10, 1.5,30, 21, 36, 60, 3,  30,),(1,1,1,0,),None,ID_ARMOR,),
}

ARMARMOR={
#--Name-------------------$$$$$, KG,   Dur, AP,   Mat, S, (DV, AV, Pro,Enc,FIR,ICE,BIO,ELE,PHS,BLD),script,ID,
"wooden vambrace"       :(6,     0.8,  20,  200,  WOOD,9, (1,  0.1,0.2,4,  -9, 0,  0,  0,  0,  1,),None,ID_VAMBRACE,),
"leather vambrace"      :(15,    0.7,  60,  200,  LETH,7, (1,  0.2,0.3,2,  -3, 2,  0,  1,  0,  1,),None,ID_VAMBRACE,),
"metal vambrace"        :(70,    1.0,  200, 200,  METL,12,(1,  0.4,0.4,3,  -6, -2, 0,  -6, 0,  2,),None,ID_VAMBRACE,),
}

'''
leg armor | legwear
    b (both) - covers both legs?
'''
LEGARMOR={
#--Name-------------------$$$$$, KG,   Dur, AP,   Mat, S, (DV, AV, Pro,Enc,FIR,ICE,BIO,ELE,PHS,BLD),b,script,ID,
"pajamas"               :(5,     0.1,  5,   200,  CLTH,1, (0,  0,  0.1,14, -3, 0,  0,  0,  0,  0,),1,None,ID_PJS,),
"padded hose"           :(15,    0.8,  100, 300,  CLTH,4, (1,  0.2,0.8,3,  -6, 6,  1,  3,  0,  1,),0,None,ID_PADDEDLEGGING,),
"padded legging"        :(25,    1.4,  160, 300,  CLTH,6, (1,  0.3,1.0,4,  -9, 9,  2,  3,  0,  2,),0,None,ID_PADDEDLEGGING,),
"jeans"                 :(35,    0.4,  75,  400,  CLTH,3, (0,  0.1,1.0,5,  -12,6,  2,  3,  0,  1,),1,None,ID_PANTS,),
"wooden greave"         :(10,    1.6,  30,  200,  WOOD,7, (0,  0.1,0.4,8,  -9, 1,  0,  0,  0,  1,),0,None,ID_GREAVE,),
"leather greave"        :(20,    1.1,  75,  200,  LETH,8, (0,  0.2,0.5,6,  -3, 3,  0,  1,  0,  1,),0,None,ID_GREAVE,),
"metal greave"          :(95,    1.5,  300, 200,  METL,12,(0,  0.5,0.8,8,  -6, -3, 0,  -6, 0,  2,),0,None,ID_GREAVE,),
"metal mail legging"    :(85,    1.5,  250, 300,  METL,14,(1,  0.4,1.3,6.5,-9, 0,  0,  -3, 0,  2,),0,None,ID_MAILLEGGING,),
}

HANDARMOR={
#--Name-------------------$$$$$, KG,   Dur, AP,   Mat, S, (DV, AV, Pro,Enc,FIR,ICE,BIO,ELE,PHS,BLD),script,ID,
"leather glove"         :(5,     0.1,  40,  100,  LETH,2, (0,  0,  0.1,6,  -2, 2,  5,  1,  1,  1,),None,ID_GLOVE,),
"plastic gauntlet"      :(1,     0.45, 30,  200,  PLAS,6, (0,  0.1,0.2,7,  -5, 0,  5,  1,  2,  1,),None,ID_GAUNTLET,),
"metal gauntlet"        :(25,    0.4,  200, 200,  METL,6, (0,  0.2,0.4,8,  -3, 0,  5,  -1, 2,  1,),None,ID_GAUNTLET,),
}

FOOTARMOR={
#--Name-------------------$$$$$, KG,   Dur, AP,   Mat, S, (DV, AV, Pro,Enc,FIR,ICE,BIO,ELE,PHS,BLD),script,ID,
"running shoe"          :(65,    0.25, 75,  300,  LETH,4, (0.2,0,  0,  3,  -2, 2,  0,  3,  0,  0,),_runningShoe,ID_SHOE,),
"wooden sandal"         :(1,     0.15, 15,  100,  WOOD,5, (0,  0,  0,  18, 0,  0,  0,  0,  0,  0,),None,ID_SANDAL,),
"leather shoe"          :(3,     0.15, 60,  300,  LETH,4, (0,  0,  0.1,6,  -3, 3,  0,  1,  0,  1,),None,ID_SHOE,),
"leather boot"          :(7,     0.3,  125, 500,  LETH,7, (0,  0,  0.2,9,  -5, 5,  0,  2,  0,  1,),None,ID_BOOT,),
"metal boot"            :(20,    0.45, 150, 500,  LETH,9, (0,  0.1,0.5,12, -6, 3,  0,  2,  0,  1,),None,ID_BOOT,),
}

ABOUTARMOR={ # Actual Encumberance == encumberance * mass
#--Name-------------------$$$$$, KG,   Dur, AP,   Mat, S, (DV, AV, Pro,Enc,FIR,ICE,BIO,ELE,PHS,BLD),script,ID,
"cloak"                 :(160,   2.5,  90,  200,  CLTH,6, (1,  1.0,1.6,8,  -15,45, 0,  9,  6,  0,),_cloak,ID_CLOAK,),#gives water resistance; can be wielded as a weapon;
}




# raw materials

'''
progression of material mass (exponential growth):
    scrap -> parcel -> piece -> chunk -> slab -> cuboid -> cube
    strands come before scrap, walls come after cubes.
    Shards are also on the progression, between scrap and parcels.
    Generally each is 5 times more massive than the previous, except:
        - cuboids are 9 times more massive than slabs
        - cubes are 27 times more massive than cuboids
        - strands are 9 times smaller than scrap.
        - walls are 1m x 1m solid blocks, mass varies
    Cuboids and cubes and walls are increasingly very rare.
        the larger they are, the more rare.
        Some sizes of materials are very rare. Slabs of bone for instance.

Raw Mats are very common in crafting
    Cost of materials is based on whether it's fully recyclable
        Metal and glass can be melted down and reforged. 100% cost.
        Plastic, stone, bone, and wood, once cut to pieces, cannot be reformed.
            It is cheaper to buy small pieces since they have less functions.
        cloth and leather are more useful in large form but still useful small.
            Worth very slightly more when in large form.
        Flesh is cheaper to buy in bulk.
            Cutting flesh to pieces is a job that is rewarded.

'''
RAWMATERIALS={

# TODO: functions for creating these automatically
##"parcel of copper"      :(x3/5,   0.1, x0.5,  METL,C_METL,_mParcel,),
##"parcel of steel"       :(x5,  0.1, x2, METL,C_STEL,_mParcel,),
##"parcel of teal"        :(x20, 0.1, x4, METL,'teal',_mParcel,),
##"scrap steel"           :(3,   0.02,18,  METL,C_STEL,_particles,),

    # individual strands of material (tinyest pieces of material)
# name                    type,$$$$,KG,  Dur, Mat, Color,  script
"string"                :(RAWM,0,   0.0007,1, CLTH,C_CLTH,None,ID_STRING,),# string distinct from scrap cloth, it's a long 1m string whereas scrap cloth is a little patch of cloth.

    # Scrap, particles (tiny pieces of material)
# name                    type,$$$$,KG,  Dur, Mat, Color,  script, ID
"dust"                  :(RAWM,0,   0.008,1,  DUST,C_DUST,_dust,ID_POWDER,),# dust of non-specific kind
"sand"                  :(RAWM,0,   0.008,1,  DUST,C_SAND,_dust,ID_POWDER,),# quartz dust
"dirt"                  :(RAWM,0,   0.008,1,  DUST,C_DIRT,_dust,ID_PARTICLES,),
"quartz"                :(RAWM,0,   0.008,5,  QRTZ,C_QRTZ,_rawMat,ID_PARTICLES,),
"gravel"                :(RAWM,0,   0.008,15, STON,C_STON,_particles,ID_PARTICLES,), # particles can be thrown to cause blindness
"scrap clay"            :(SCRP,0,   0.06,10,  CLAY,C_CLAY,_rawMat,ID_CLAY,),
"scrap ceramic"         :(SCRP,0,   0.02,1,   CERA,C_CERA,_particles,ID_SCRAP,),
"scrap cloth"           :(SCRP,0.1, 0.008,1,  CLTH,C_CLTH,None,ID_RAG,),
"scrap plastic"         :(SCRP,0,   0.04,1,   PLAS,C_PLAS,_particles,ID_SCRAP,),
"scrap wood"            :(SCRP,0,   0.04,1,   WOOD,C_WOOD,_particles,ID_WOOD,),
"scrap bone"            :(SCRP,0.08,0.02,4,   BONE,C_BONE,_particles,ID_SCRAP,),
"scrap metal"           :(SCRP,1,   0.02,6,   METL,C_METL,_particles,ID_SCRAP,),
"scrap leather"         :(SCRP,0.4, 0.02,4,   LETH,C_LETH,_rawMat,ID_SCRAP,),
"scrap boiled leather"  :(SCRP,0.6, 0.02,12,  LETH,C_LETH,_rawMat,ID_SCRAP,),
"scrap flesh"           :(SCRP,0.2, 0.04,2,   FLSH,C_FLSH,_rawMat,ID_MEAT,),
"scrap RAM"             :(SCRP,1,   0.02,4,   QRTZ,C_ELEC,_rawMat,ID_SCRAPELECTRONICS,),

    # Parcels (small pieces of material, used as currency and for making fine tools)
    # DO NOT CHANGE THE NAMES OF THESE.
# name                    type,$$$$,KG,  Dur, Mat, Color, script, ID
"parcel of quartz"      :(PRCL,1,   0.2, 15,  QRTZ,C_QRTZ,_qParcel,ID_ROCK,),
"parcel of tarp"        :(PRCL,0.6, 0.06,15,  TARP,C_TARP,_tParcel,ID_TARP,),
"parcel of clay"        :(PRCL,0.2, 0.3, 15,  CLAY,C_CLAY,_clayParcel,ID_CLAY,),
"parcel of ceramic"     :(PRCL,0.2, 0.1, 1,   CERA,C_CERA,_ceramicParcel,ID_ROCK,),
"parcel of cloth"       :(PRCL,0.8, 0.04,10,  CLTH,C_CLTH,_clothParcel,ID_RAGS,),
"parcel of leather"     :(PRCL,2,   0.1, 20,  LETH,C_LETH,_lParcel,ID_SCRAP,),
"parcel of b.leather"   :(PRCL,3,   0.1, 40,  BOIL,C_BOIL,_blParcel,ID_SCRAP,),
"parcel of flesh"       :(PRCL,1,   0.2, 15,  FLSH,C_FLSH,_fParcel,ID_MEAT,),
"parcel of stone"       :(PRCL,0.2, 0.2, 50,  STON,C_STON,_sParcel,ID_ROCK,),
"parcel of plastic"     :(PRCL,0.2, 0.2, 30,  PLAS,C_PLAS,_pParcel,ID_SCRAP,),
"parcel of wood"        :(PRCL,1,   0.2, 40,  WOOD,C_WOOD,_wParcel,ID_WOOD,),
"parcel of bone"        :(PRCL,0.4, 0.1, 45,  BONE,C_BONE,_bParcel,ID_SCRAP,),
"parcel of glass"       :(PRCL,1,   0.04,2,   GLAS,C_GLAS,_gParcel,ID_SCRAP,),
"parcel of metal"       :(PRCL,5,   0.1, 80,  METL,C_METL,_mParcel,ID_SCRAP,),
"parcel of rubber"      :(PRCL,2,   0.1, 10,  RUBB,C_RUBB,_rParcel,ID_SCRAP,),

    # Pieces (medium size pieces of material, used for making tools, armor)
# name                    type,$$$$,KG,  Dur, Mat, Color, script, ID
"piece of quartz"       :(PIEC,5,   1.0, 60,  QRTZ,C_QRTZ,_qPiece,ID_ROCK,),
"piece of tarp"         :(PIEC,3,   0.3, 20,  TARP,C_TARP,_tPiece,ID_TARP,),
"piece of clay"         :(PIEC,1,   1.5, 30,  CLAY,C_CLAY,_clayPiece,ID_CLAY,),
"piece of ceramic"      :(PIEC,1,   0.5, 5,   CERA,C_CERA,_ceramicPiece,ID_ROCK,),
"piece of cloth"        :(PIEC,3,   0.2, 40,  CLTH,C_CLTH,_clothPiece,ID_CLOTH,),
"piece of leather"      :(PIEC,10,  0.5, 60,  LETH,C_LETH,_lPiece,ID_SCRAP,),
"piece of b.leather"    :(PIEC,15,  0.5, 120, BOIL,C_BOIL,_blPiece,ID_SCRAP,),
"piece of flesh"        :(PIEC,3,   1.0, 30,  FLSH,C_FLSH,_fPiece,ID_MEAT,),
"piece of stone"        :(PIEC,1,   1.0, 200, STON,C_STON,_sPiece,ID_ROCK,),
"piece of plastic"      :(PIEC,1,   1.0, 80,  PLAS,C_PLAS,_pPiece,ID_SCRAP,),
"piece of wood"         :(PIEC,5,   1.0, 150, WOOD,C_WOOD,_wPiece,ID_WOOD,),
"piece of bone"         :(PIEC,2,   0.5, 180, BONE,C_BONE,_bPiece,ID_BONE,),
"piece of glass"        :(PIEC,5,   0.2, 20,  GLAS,C_GLAS,_gPiece,ID_GLASS,),
"piece of metal"        :(PIEC,25,  0.5, 300, METL,C_METL,_mPiece,ID_SCRAP,),
"piece of rubber"       :(PIEC,10,  0.5, 200, RUBB,C_RUBB,_rPiece,ID_SCRAP,),

    # Chunks (large pieces of material, used for making weapons, armor)
# name                    type,$$$$,KG,  Dur, Mat, Color, script, ID
##"towel"                 :(20,  1.0, 120, CLTH,_towel,), # in STUFF, MOVE HERE
"tarp"                  :(CHNK,18,  1.5, 20,  TARP,C_TARP,_tarp,ID_TARP,),
"chunk of quartz"       :(CHNK,25,  5.0, 150, QRTZ,C_QRTZ,_qChunk,ID_CHUNK,),
"chunk of clay"         :(CHNK,4,   7.5, 350, CLAY,C_CLAY,_clayChunk,ID_CHUNK,),
"chunk of ceramic"      :(CHNK,3,   2.5, 10,  CERA,C_CERA,_ceramicChunk,ID_CHUNK,),
"chunk of cloth"        :(CHNK,15,  1.0, 160, CLTH,C_CLTH,_clothChunk,ID_CLOTH,),
"leather hide"          :(CHNK,60,  2.5, 120, LETH,C_LETH,_lChunk,ID_CHUNK,),
"boiled leather hide"   :(CHNK,75,  2.5, 240, BOIL,C_BOIL,_blChunk,ID_CHUNK,),
"chunk of flesh"        :(CHNK,12,  5.0, 100, FLSH,C_FLSH,_fChunk,ID_MEAT,),
"chunk of stone"        :(CHNK,6,   5.0, 400, STON,C_STON,_sChunk,ID_CHUNK,),
"chunk of plastic"      :(CHNK,5,   5.0, 250, PLAS,C_PLAS,_pChunk,ID_CHUNK,),
"chunk of wood"         :(CHNK,30,  5.0, 300, WOOD,C_WOOD,_wChunk,ID_CHUNK,),
"chunk of bone"         :(CHNK,10,  2.5, 350, BONE,C_BONE,_bChunk,ID_CHUNK,),
"chunk of glass"        :(CHNK,25,  1.0, 50,  GLAS,C_GLAS,_gChunk,ID_CHUNK,),
"chunk of metal"        :(CHNK,125, 2.5, 900, METL,C_METL,_mChunk,ID_CHUNK,),
"chunk of rubber"       :(CHNK,50,  2.5, 500, RUBB,C_RUBB,_rChunk,ID_CHUNK,),

    # Slabs (bricks of material, used for making large tools/weapons)
# name                    type,$$$$,KG,  Dur, Mat, Color, script, ID
##"slab of cloth"         :(100, 5.0, 120, CLTH,_rawMat,), #certain types of slabs are difficult to achieve
##"slab of leather"       :(400, 12.5,400, LETH,_rawMat,),
"tarp, large"           :(SLAB,95,  7.5, 20,  TARP,C_TARP,_tarpLarge,ID_TARP,),
"slab of clay"          :(SLAB,16,  37.5,2000,CLAY,C_CLAY,_claySlab,ID_SLAB,),
"slab of ceramic"       :(SLAB,15,  12.5,500, CERA,C_TARP,_ceramicSlab,ID_SLAB,),
"slab of flesh"         :(SLAB,100, 25.0,400, FLSH,C_FLSH,_fSlab,ID_SLAB,),
"slab of stone"         :(SLAB,40,  25.0,1200,STON,C_STON,_sSlab,ID_SLAB,),
"slab of plastic"       :(SLAB,25,  25.0,800, PLAS,C_PLAS,_pSlab,ID_SLAB,),
"slab of wood"          :(SLAB,180, 25.0,950, WOOD,C_WOOD,_wSlab,ID_SLAB,),
"slab of bone"          :(SLAB,100, 12.5,1050,BONE,C_BONE,_bSlab,ID_SLAB,),
"slab of glass"         :(SLAB,125, 5.0, 200, GLAS,C_GLAS,_gSlab,ID_SLAB,),
"slab of metal"         :(SLAB,600, 12.5,3000,METL,C_METL,_mSlab,ID_SLAB,),

    # Cuboids (solid 3D blocks, 9 times the mass of slabs)
# name                    type,$$$$,KG,  Dur, Mat, Color, script, ID
"cuboid of clay"        :(CUBO,100, 337, 5000,CLAY,C_CLAY,_cuboid,ID_CUBOID,),
"cuboid of flesh"       :(CUBO,800, 225, 3000,FLSH,C_FLSH,_cuboid,ID_CUBOID,),
"cuboid of stone"       :(CUBO,300, 225, 5000,STON,C_STON,_cuboid,ID_CUBOID,),
"cuboid of plastic"     :(CUBO,170, 225, 2000,PLAS,C_PLAS,_cuboid,ID_CUBOID,),
"cuboid of wood"        :(CUBO,950, 225, 5000,WOOD,C_WOOD,_cuboid,ID_CUBOID,),
"cuboid of bone"        :(CUBO,990, 112, 5000,BONE,C_BONE,_cuboid,ID_CUBOID,),
"cuboid of glass"       :(CUBO,850, 45,  2000,GLAS,C_GLAS,_cuboid,ID_CUBOID,),
"cuboid of metal"       :(CUBO,5000,112, 9000,METL,C_METL,_cuboid,ID_CUBOID,),

    # Cubes (27 times the mass of cuboids)
# name                    type,$$$$$$,KG,  Dur, Mat, script, ID
"cube of clay"          :(CUBE,2250,  9112,5000,CLAY,C_CLAY,_cube,ID_CUBE,),
"cube of flesh"         :(CUBE,20000, 6075,3000,FLSH,C_FLSH,_cube,ID_CUBE,),
"cube of stone"         :(CUBE,7500,  6075,5000,STON,C_STON,_cube,ID_CUBE,),
"cube of plastic"       :(CUBE,5500,  6075,2000,PLAS,C_PLAS,_cube,ID_CUBE,),
"cube of wood"          :(CUBE,20000, 6075,5000,WOOD,C_WOOD,_cube,ID_CUBE,),
"cube of bone"          :(CUBE,20000, 3037,5000,BONE,C_BONE,_cube,ID_CUBE,),
"cube of glass"         :(CUBE,10000, 1215,2000,GLAS,C_GLAS,_cube,ID_CUBE,),
"cube of metal"         :(CUBE,120000,3037,9000,METL,C_METL,_cube,ID_CUBE,),

    # Walls (1m x 1m x 3m massive solid blocks of material)
# name                    type,$$$$$$,KG,   Dur,  Mat, script, ID
"wall of clay"          :(219, 9999,  99999,99999,CLAY,C_CLAY,None,ID_CUBE,),
"wall of flesh"         :(219, 99999, 99999,99999,FLSH,C_FLSH,None,ID_CUBE,),
"wall of stone"         :(219, 9999,  99999,99999,STON,C_STON,None,ID_CUBE,),
"wall of plastic"       :(219, 9999,  99999,99999,PLAS,C_PLAS,None,ID_CUBE,),
"wall of wood"          :(219, 99999, 99999,99999,WOOD,C_WOOD,None,ID_CUBE,),
"wall of bone"          :(219, 99999, 99999,99999,BONE,C_BONE,None,ID_CUBE,),
"wall of glass"         :(219, 99999, 99999,99999,GLAS,C_GLAS,None,ID_CUBE,),
"wall of metal"         :(219, 999999,99999,99999,METL,C_METL,None,ID_CUBE,),

    # Shards (small and sharp pieces of material)
# name                    type,$$$$, Kg,  Dur, Mat, Color, script, ID
"shard of plastic"      :(SHRD,0,    0.18,3,   PLAS,C_PLAS,_pShard,ID_SHARD,),
"shard of ceramic"      :(SHRD,1,    0.12,1,   CERA,C_CERA,_cShard,ID_SHARD,),
"shard of wood"         :(SHRD,0.2,  0.18,10,  WOOD,C_WOOD,_wShard,ID_SHARD,),
"shard of stone"        :(SHRD,0.2,  0.18,15,  STON,C_STON,_sShard,ID_SHARD,),
"shard of bone"         :(SHRD,0.4,  0.08,20,  BONE,C_BONE,_bShard,ID_SHARD,),
"shard of glass"        :(SHRD,1,    0.05,2,   GLAS,C_GLAS,_gShard,ID_SHARD,),
"shard of metal"        :(SHRD,1,    0.1, 30,  METL,C_METL,_mShard,ID_SHARD,),

    # Sticks
# name                    type,$$$$, Kg,  Dur, Mat, Color, script, ID
"stick of plastic"      :(STIK,1,    1.0, 75,  PLAS,C_PLAS,_pStick,ID_STICK,),
"stick of wood"         :(STIK,5,    1.0, 150, WOOD,C_WOOD,_wStick,ID_STICK,), # wood is greenwood when you need it to be, and deadwood when you need it to be. Simplifies things.
"stick of metal"        :(STIK,50,   0.5, 500, METL,C_METL,_mStick,ID_STICK,),

    # Poles (long sticks, 2x the mass of sticks)
# name                    type,$$$$, Kg,  Dur, Mat, Color, script, ID
"pole of plastic"       :(STIK,2,    2.0, 150, PLAS,C_PLAS,_pPole,ID_POLE,),
"pole of wood"          :(STIK,10,   2.0, 225, WOOD,C_WOOD,_wPole,ID_POLE,),
"pole of metal"         :(STIK,100,  1.0, 600, METL,C_METL,_mPole,ID_POLE,),

    # Rings
# name                    type,$$$$, Kg,  Dur, Mat, Color, script, ID
"plastic ring"          :(RAWM,0,    0.01,10,  PLAS,C_PLAS,_rawMat,ID_RING,),
"wooden ring"           :(RAWM,1,    0.02,40,  WOOD,C_WOOD,_rawMat,ID_RING,),
"bone ring"             :(RAWM,1,    0.02,80,  BONE,C_BONE,_rawMat,ID_RING,),
"stone ring"            :(RAWM,1,    0.03,120, STON,C_STON,_rawMat,ID_RING,),
"glass ring"            :(RAWM,1,    0.01,10,  GLAS,C_GLAS,_rawMat,ID_RING,),
"metal ring"            :(RAWM,5,    0.02,300, METL,C_METL,_rawMat,ID_RING,),


    # Misc.
# name                    type,$$$$, Kg,  Dur, Mat, Color, script, ID
"turpentine"            :(RAWM,2,    0.75, 15, METL,'brown',None,ID_CONTAINER,),#_turpentine # super toxic
"acetone"               :(RAWM,1,    0.5,  15, METL,'white',None,ID_CONTAINER,),
"food-grade oil"        :(RAWM,5,    0.25, 15, METL,'white',None,ID_OIL,),
"oil"                   :(RAWM,1,    1.0,  15, METL,'white',None,ID_OIL,),
"grease"                :(RAWM,1,    1.0,  15, OIL, 'white',None,ID_GOOP,),
"rubbing alcohol"       :(RAWM,1,    0.5,  1,  PLAS,'white',None,ID_CONTAINER,),
"glue"                  :(RAWM,0,    0.001,1,  PLAS,'yellow',None,ID_GOOP,),
"gluestick"             :(RAWM,10,   0.1,  10, PLAS,'yellow',_trinket,ID_CONTAINER,),
"duct tape"             :(RAWM,0,    0.002,8,  PLAS,'gray',None,ID_TARP,),
"roll of duct tape"     :(RAWM,20,   1.0,  200,PLAS,'gray',_trinket,ID_ROLL,),
"battery, small"        :(RAWM,2,    0.05, 15, PLAS,'blue',_trinket,ID_BATTERY,),
"battery"               :(RAWM,5,    0.2,  25, PLAS,'blue',_trinket,ID_BATTERY,),


# name                    type,$$$$, Kg,  Dur, Mat, Color, script, ID
        # cloth
"spool of string"       :(RAWM,5,    0.3, 50,  CLTH,C_CLTH,_spoolString,ID_SPOOL,),# can unwind into hundreds of strings
        # carbon
"charcoal"              :(RAWM,1,    0.1, 5,   CARB,C_CARB,_rawMat,ID_ROCK,),# obtained by putting wood in a charcoal mound and cooking it for a long ass time (< 24 hours)
"coke"                  :(RAWM,1,    0.05,3,   CARB,C_CARB,_rawMat,ID_POWDER,),# used to smelt metal; can smelt rust back into metal, and create a weak steel that is stronger than normal metal. Obtained by cooking charcoal in airless environment for a long time (12-18 hours).
"powdered charcoal"     :(RAWM,1,    0.1, 1,   CARB,C_CARB,_dust,ID_POWDER,),
"activated carbon"      :(RAWM,3,    0.05,1,   CARB,C_CARB,_dust,ID_POWDER,),# filtration systems, antitoxin, antibiotic, odor absorbent. Needs powdered coal, calcium chloride and baking at 300C.
        # rubber
"rubber hose"           :(RAWM,3,    0.1, 15,  RUBB,C_RUBB,_rawMat,ID_TUBE,),
"rubber band"           :(RAWM,1,    0.02,10,  RUBB,C_RUBB,_rawMat,ID_RUBBERBAND,),
        # plastic
"plastic bottle"        :(RAWM,1,    0.05,5,   PLAS,C_PLAS,_pBottle,ID_BOTTLE,),
"plastic cup"           :(RAWM,1,    0.07,5,   PLAS,C_PLAS,_rawMat,ID_CUP,),
"plastic pipe"          :(RAWM,1,    1.0, 100, PLAS,C_PLAS,_pPipe,ID_PIPE,),
"plastic tube"          :(RAWM,1,    0.1, 20,  PLAS,C_PLAS,_rawMat,ID_TUBE,),
"insulated wire"        :(RAWM,6,    0.05,30,  PLAS,C_PLAS,_rawMat,ID_WIRE,),
"fishing wire"          :(RAWM,0,    0.003,5,  METL,C_PLAS,_rawMat,ID_WIRE,),
"spool of fishing wire" :(RAWM,150,  1.0, 100, METL,C_PLAS,_spoolFishingWire,ID_SPOOL,),# can unwind into hundreds of fishing wire
        # wood
"wooden plank"          :(RAWM,4,    1.25,80,  WOOD,C_WOOD,_plank,ID_PLANK,),#2H only
"twig"                  :(RAWM,0,    0.1, 4,   WOOD,C_WOOD,_rawMat,ID_STICK,),
"fibrous leaf"          :(RAWM,0,    0.2, 30,  WOOD,C_WOOD,_rawMat,ID_LEAF,),
"foliage"               :(RAWM,0,    0.3, 20,  WOOD,C_WOOD,_rawMat,ID_LEAF,),
"root"                  :(RAWM,1,    1.0, 100, WOOD,C_WOOD,_rawMat,ID_PLANT,),
"branch"                :(RAWM,1,    6.0, 800, WOOD,C_WOOD,_rawMat,ID_PLANT,),# becomes sticks of wood, sticks of wood, long, and foliage...
"log"                   :(T_LOG,92,  100, 1000,WOOD,C_WOOD,_log,ID_WOOD,),
        # bone
"skull"                 :(RAWM,5,    1.0, 80,  BONE,C_BONE,_skull,ID_BONE,),
"bone"                  :(RAWM,2,    0.25,120, BONE,C_BONE,_bone,ID_BONE,),
"bone, broken"          :(RAWM,1,    0.2, 30,  BONE,C_BONE,_bBone,ID_BONE,),
"bone, large"           :(RAWM,10,   2.0, 300, BONE,C_BONE,_boneLarge,ID_BONE,),#2H only
"bone, small"           :(RAWM,1,    0.1, 40,  BONE,C_BONE,_boneSmall,ID_BONE,),
        # glass
"magnifying glass"      :(RAWM,54,   0.1, 5,   GLAS,C_GLAS,_magnifyingGlass,ID_LENS,),
"glass bottle"          :(RAWM,5,    0.5, 1,   GLAS,C_GLAS,_gBottle,ID_BOTTLE,),
"glass tube"            :(RAWM,1,    0.01,1,   GLAS,C_GLAS,_rawMat,ID_GLASS,),
        # metal
    # springs
"spring, small"         :(RAWM,3,    0.02,2,   METL,C_METL,_rawMat,ID_SPRING,),
"spring"                :(RAWM,8,    0.1, 10,  METL,C_METL,_rawMat,ID_SPRING,),
"spring, large"         :(RAWM,55,   0.5, 50,  METL,C_METL,_rawMat,ID_SPRING,),
"spring, giant"         :(RAWM,275,  2.5, 250, METL,C_METL,_rawMat,ID_SPRING,),
"torsion spring, small" :(RAWM,6,    0.05,10,  METL,C_METL,_rawMat,ID_SPRING,),
"torsion spring"        :(RAWM,18,   0.2, 50,  METL,C_METL,_rawMat,ID_SPRING,),
"torsion spring, large" :(RAWM,160,  1.0, 250, METL,C_METL,_rawMat,ID_SPRING,),
    # chains
"chain link, small"     :(RAWM,0,    0.003,60, METL,C_METL,None,ID_CHAIN,),
"chain, small"          :(RAWM,25,   0.5, 75,  METL,C_METL,_chainLight,ID_CHAIN,),
"chain link"            :(RAWM,1,    0.01,125, METL,C_METL,None,ID_CHAIN,),
"chain"                 :(RAWM,50,   1.0, 150, METL,C_METL,_chain,ID_CHAIN,),
"chain link, large"     :(RAWM,2,    0.04,300, METL,C_METL,None,ID_CHAIN,),
"chain, large"          :(RAWM,100,  2.0, 350, METL,C_METL,_chainHeavy,ID_CHAIN,),
    # magnets
"magnet, small"         :(RAWM,6,    0.05,115, METL,C_METL,_magnetWeak,ID_SCRAP,),
"magnet"                :(RAWM,26,   0.2, 225, METL,C_METL,_magnet,ID_SCRAP,),
"magnet, large"         :(RAWM,166,  0.6, 335, METL,C_METL,_magnetStrong,ID_SCRAP,),
"magnet, rare-earth"    :(RAWM,320,  0.2, 80,  METL,C_METL,_magnet,ID_SCRAP,),
    # other metals
"brass rivet"           :(RAWM,0,    0.005,10, METL,C_METL,_rawMat,ID_SCRAP,),
"pop tab"               :(RAWM,0,    0.005,50, METL,C_METL,_rawMat,ID_SCRAP,),
"pop tab mail ring"     :(RAWM,0,    0.005,40, METL,C_METL,_rawMat,ID_SCRAP,),
"mail ring, riveted"    :(RAWM,1,    0.01,150, METL,C_METL,_rawMat,ID_SCRAP,),
"mail ring, welded"     :(RAWM,1,    0.01,150, METL,C_METL,_rawMat,ID_SCRAP,),
"paperclip"             :(RAWM,0,    0.001,8,  METL,C_METL,_rawMat,ID_SCRAP,),
"bobby pin"             :(RAWM,1,    0.01,25,  METL,C_METL,_bobbyPin,ID_SCRAP,),
"lock pick"             :(RAWM,3,    0.05,5,   METL,C_METL,_lockPick,ID_SCRAP,),
"needle"                :(RAWM,0,    0.001,15, METL,C_METL,_mNeedle,ID_SCRAP,),
"nail"                  :(RAWM,1,    0.02,60,  METL,C_METL,_nail,ID_SCRAP,),
"screw"                 :(RAWM,1,    0.02,120, METL,C_METL,_screw,ID_SCRAP,),
"razor blade"           :(RAWM,8,    0.02,2,   METL,C_METL,_razorBlade,ID_SCRAP,),
"metal screen"          :(RAWM,1,    0.05,5,   METL,C_METL,_rawMat,ID_SCRAP,),
"metal foil"            :(RAWM,1,    0.01,3,   METL,C_METL,_rawMat,ID_SCRAP,),
"metal can"             :(RAWM,5,    0.1, 25,  METL,C_METL,_mCan,ID_SCRAP,),
"metal wire"            :(RAWM,3,    0.04,15,  METL,C_METL,_mWire,ID_SCRAP,),
"metal key"             :(RAWM,6,    0.1, 350, METL,C_METL,_key,ID_SCRAP,),
"metal tube"            :(RAWM,6,    0.25,40,  METL,C_METL,_mTube,ID_TUBE,),
"metal pipe"            :(RAWM,50,   1.0, 500, METL,C_METL,_mPipe,ID_PIPE,),
"metal pipe, broken"    :(RAWM,30,   0.6, 250, METL,C_METL,_mPipeBroken,ID_PIPE,),
"metal bar"             :(RAWM,50,   1.0, 750, METL,C_METL,_mBar,ID_BAR,),# flat inch-thick brick of metal
"metal ingot"           :(RAWM,50,   1.0, 3000,METL,C_METL,_mPiece,ID_INGOT,),# flat inch-thick brick of metal
"metal sheet"           :(RAWM,136,  2.5, 50,  METL,C_METL,_mChunk,ID_SCRAP,),
        # ropes
"cordage"               :(RAWM,0.1,  0.006,5,  ROPE,C_ROPE,_cordage,ID_ROPE,),#2H only
"rope"                  :(RAWM,1,    0.05,30,  ROPE,C_ROPE,_rope,ID_ROPE,),#2H only; length of rope is simply how many items of rope you possess -- this is the simplest way to do this.
"cable"                 :(RAWM,3,    0.15,100, ROPE,C_ROPE,_cable,ID_ROPE,),#2H only

}


JOBS={
    # occupations the player can choose from when starting the game.
    # affects starting stats and gear/items.
    
    # KG, $$$: mass, money
    #Access keys:
    #S  level of security clearance
    #Keys:
        #J  janitor key : janitor's closets
        #K  politician's key : key to the city
        #P  pilot key : hangar access
        #L  lab tech key : lab access
    #stats: stat bonuses or nerfs (from BASE_ stats in const.py)
    #skills: major occupation skills that this character begins with
        # (the exact level is determined elsewhere)
    #items: items you start with
        #(itemName, dictionary, quantity)
            # where dictionary is the item table where the item can be found.
    
    
#ID                Char,Name         KG, $$$$,S|Key, stats, skills, items
CLS_ATHLETE     : ("a", "athlete",   80, 500, 0,'',
    {'con':2,'agi':4,'end':8,'int':-4,'msp':10,'bea':4,},
    (SKL_ATHLETE,),
    (
        ('running shoe', FOOTARMOR, 2,),
        ),
    ),
CLS_BOUNTYHUNTER : ("B", "bounty hunter",80, 2000, 0,'',
    {'con':2,'dex':4,'agi':4,'end':4,'str':2,'int':2,},
    (SKL_PISTOLS,SKL_RIFLES,SKL_SURVIVAL,SKL_BOXING,),
    (
        ('9mm revolver', RANGEDWEAPONS, 1,),
        ('9mm cartridge', AMMUNITION, 12,),
        ),
    ),
CLS_CHEMIST     : ("C", "chemist",   65, 2000,1,'L',
    {'int':8,'end':-2,'con':-2,'agi':-2,},
    (SKL_CHEMISTRY,),
    (
        ),
    ),
CLS_DEPRIVED    : ("d", "deprived",  50, 5,   0,'',
    {'sight':-5,'hearing':-20,'str':-2,'con':-2,'int':-2,'end':-2,'dex':-2,'agi':-2,'idn':16,'bea':-16,},
    (SKL_SURVIVAL,SKL_ASSEMBLY,),
    (
        ('wooden club', WEAPONS, 1,),
        ),
    ),
CLS_DOCTOR      : ("D", "doctor",    75, 2000,1,'',
    {'int':6,'dex':6,'end':-4,'agi':-4,'con':-4,},
    (SKL_MEDICINE,SKL_SURGERY,),
    (
        ('scalpel', WEAPONS, 1,),
        ),
    ),
CLS_JANITOR     : ("j", "janitor",   70, 100, 0,'J',
    {},
    (),
    (),
    ),
CLS_SOLDIER     : ("S", "soldier",    85, 1000,3,'',
    {'hearing':-40,'str':6,'con':6,'dex':2,'int':2,'end':6,'agi':2,'idn':8,},
    (SKL_PISTOLS,SKL_RIFLES,SKL_MACHINEGUNS,SKL_ARMOR,),
    (),
    ),
CLS_SECURITY    : ("O", "security",  80, 300, 5,'',
    {'dex':4,'con':4,'int':-4,'gra':2,'idn':8,},
    (SKL_BLUDGEONS,SKL_ENERGY,),
    (
        ('metal baton', WEAPONS, 1,),
        # taser?
        ),
    ),
CLS_PILOT       : ("p", "pilot",     70, 500, 0,'P',
    {'sight':40,'int':2,'dex':4,'agi':-4,'end':-2,},
    (SKL_PILOT,),
    (),
    ),
CLS_RIOTPOLICE  : ("P","riot police",85, 500, 2,'',
    {'str':4,'con':4,'dex':2,'end':2,'int':-2,'idn':16,},
    (SKL_BLUDGEONS,SKL_ENERGY,SKL_PISTOLS,SKL_SMGS,SKL_SHIELDS,SKL_ARMOR,),
    (
        ('riot shield', WEAPONS, 1,),
        ('metal truncheon', WEAPONS, 1,),
        ('6ga riot shotgun', RANGEDWEAPONS, 1,),
        ('6ga rubber slug', AMMUNITION, 4,),
        ('6ga rubber shell', AMMUNITION, 8,),
        ('6ga tear gas can', AMMUNITION, 2,),
        ),
    ),
CLS_PROGRAMMER  : ("q", "programmer",65, 2000,0,'',
    {'int':4,'agi':-2,'con':-2,},
    (SKL_COMPUTERS,),
    (
        ('hoody', ARMOR, 1,),
        ('pajamas', LEGARMOR, 1,),
        ),
    ),
CLS_POLITICIAN  : ("I", "politician",60,20000,4,'K',
    {'con':-2,'end':-4,'int':6,'bea':16,},
    (SKL_PERSUASION,),
    (),
    ),
CLS_SMUGGLER    : ("u", "smuggler",  75, 5000,0,'',
    {'con':2,'int':2,'dex':2,'agi':2,'encmax':10,},
    (SKL_PERSUASION,SKL_PISTOLS,),
    (),
    ),
CLS_TECHNICIAN  : ("T", "technician",65, 500, 1,'',
    {'int':2,'dex':2,'end':-2,'agi':-2,},
    (SKL_HARDWARE,),
    (),
    ),
CLS_THIEF       : ("t", "thief",     70, 5000,0,'',
    {'agi':6,'dex':4,'end':2,'con':-2,'encmax':30,},
    (SKL_STEALTH,SKL_LOCKPICK,SKL_KNIVES,),
    (),
    ),
CLS_WRESTLER    : ("w", "wrestler",  90, 300, 0,'',
    {'hearing':-20,'int':-2,'end':6,'str':6,'bal':5,'gra':2,},
    (SKL_WRESTLING,SKL_BOXING,SKL_UNARMORED,),
    (),
    ),
CLS_MONK        : ("m", "monk",     60, 100, 0,'',
    {'end':8,'str':-2,'dex':-2,'int':2,'con':-2,'agi':-4,'bal':5,'cou':32,},
    (SKL_STAVES,SKL_UNARMORED,),
    (),
    ),
}






















'''
def _create_human_head():
    partMeta = cmp.BPM_Head()
    partMeta.head.bone.material = MAT_BONE
    partMeta.head.skin.material = MAT_FLESH
    partMeta.neck.bone.material = MAT_BONE
    partMeta.neck.skin.material = MAT_FLESH
    partMeta.face.skin.material = MAT_FLESH
    partMeta.mouth.bone.material = MAT_BONE
    partMeta.mouth.teeth.material = MAT_BONE
    return partMeta
def _create_human_arm():
    partMeta = cmp.BPM_Arm()
    partMeta.arm.bone.material = MAT_BONE
    partMeta.arm.skin.material = MAT_FLESH
    partMeta.hand.bone.material = MAT_BONE
    partMeta.hand.skin.material = MAT_FLESH
    return partMeta
def _create_human_leg():
    partMeta = cmp.BPM_Leg()
    partMeta.leg.bone.material = MAT_BONE
    partMeta.leg.skin.material = MAT_FLESH
    partMeta.foot.bone.material = MAT_BONE
    partMeta.foot.skin.material = MAT_FLESH
    return partMeta'''


