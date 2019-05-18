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

# constants

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
EXPL    = T_EXPLOSIVE

A_BULL = AMMO_BULLETS
A_BALL = AMMO_BALLS
A_SHOT = AMMO_SHOT
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


def _cloak(tt):
    if not rog.has(tt, cmp.CanEquipInMainhandSlot):
        modDict = { cmp.CombatStats : {"atk":3,"dmg":1,"dfn":1,}, }
        rog.world().add_component(tt, cmp.CanEquipInMainhandSlot(modDict))

def _nvisionGoggles(tt):
##    if rog.has(tt, cmp.Equipable):
##        equipable = rog.get(tt, cmp.Equipable)
##        equipable.statMods.update({})
    pass

def _earPlugs(tt):
    pass

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


#GEAR
    #Columns:
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
    #
GEAR = {
#--Name-----------------------Type,$$$$$, KG,   Dur, Mat, (DV, AV, MSp, Vis,FIR,BIO,ELE,PHS), script
    #Back
"cloak"                     :(BACK,420,   6.0,  150, CLTH,( 4,  1, -3,  0,  10, 10, 0,  0,), _cloak,),
    #Armor
"skin suit"                 :(ARMR,450,   14.7, 90,  FLSH,( 2,  1, -6,  0,  0,  10, 3,  0,), None,),
"bone armor"                :(ARMR,790,   27.8, 475, BONE,(-6,  5, -18, 0,  15, 10, 0,  0,), None,),
"cloth armor"               :(ARMR,950,   15.6, 125, CLTH,(-3,  2, -6,  0,  5,  5,  3,  0,), None,),
"carb garb"                 :(ARMR,1060,  22.5, 600, CARB,(-3,  3, -12, 0,  10, 10, 6,  0,), None,),
"boiled leather plate"      :(ARMR,1175,  12.5, 180, LETH,( 0,  3, -6,  0,  5,  5,  15, 0,), None,),
"riot gear"                 :(ARMR,3490,  20.5, 500, CARB,(-2,  5, -12, 0,  18, 15, 10, 0,), None,),
"metal gear"                :(ARMR,9950,  27.5, 740, METL,(-4,  7, -18, 0,  -5, 5,  -10,0,), None,),
"full metal suit"           :(ARMR,12000, 35.1, 850, METL,(-5,  10,-21, 0,  -10,10, -20,0,), None,),
"graphene armor"            :(ARMR,58250, 16.5, 900, CARB,(-2,  8, -9,  0,  14, 20, 30, 0,), None,),
"bullet-proof armor"        :(ARMR,135000,12.8, 1000,CARB,(-1,  12,-3,  0,  5,  5,  0,  0,), None,),
"space suit"                :(ARMR,36000, 40.0, 50,  CARB,(-15, 3, -33, 0,  10, 26, 6,  0,), None,),
"hazard suit"               :(ARMR,2445,  14.5, 75,  PLAS,(-12, 2, -24, 0,  5,  38, 12, 0,), None,),
"disposable PPE"            :(ARMR,110,   9.25, 25,  PLAS,(-9,  1, -15, 0,  -15,21, 3,  0,), None,),
"wetsuit"                   :(ARMR,1600,  8.2,  50,  PLAS,( 0,  0, -6,  0,  23, 5,  21, 0,), None,),
"fire blanket"              :(BACK,600,   12.4, 175, CLTH,(-3,  1, -9,  0,  36, 15, 9,  0,), None,),
"burn jacket"               :(ARMR,1965,  19.5, 150, CLTH,(-5,  2, -12, 0,  50, 15, 15, 0,), None,),
    #Helmets
"bandana"                   :(HELM,40,    0.1,  20,  CLTH,( 2,  0,  0,  0,  5,  10, 3,  0,), None,),
"skin mask"                 :(HELM,180,   1.25, 10,  FLSH,( 1,  0,  0,  -1, 0,  5,  0,  0,), None,),
"wood mask"                 :(HELM,10,    1.0,  30,  WOOD,(-1,  1, -3,  -5, -5, 5,  3,  0,), None,),
"skull helm"                :(HELM,750,   2.8,  115, BONE,(-3,  2, -9,  -3, 5,  5,  6,  0,), None,),
"motorcycle helmet"         :(HELM,1500,  0.75, 145, PLAS,(-1,  2, -3,  -3, 0,  5,  6,  0,), None,),
"metal mask"                :(HELM,6000,  2.2,  275, METL,(-3,  3, -6,  -7, 0,  5,  -6, 0,), None,),
"metal helm"                :(HELM,8500,  3.0,  300, METL,(-4,  4, -9,  -10,0,  5,  -12,0,), None,),
"graphene mask"             :(HELM,21850, 0.8,  285, CARB,(-2,  2, -3,  -7, 5,  8,  9,  0,), None,),
"graphene helmet"           :(HELM,25450, 1.2,  310, CARB,(-2,  3, -3,  -7, 6,  10, 9,  0,), None,),
"kevlar hat"                :(HELM,89500, 1.5,  350, CARB,(-2,  4, -3,  0,  0,  0,  0,  0,), None,),
"space helmet"              :(HELM,51950, 3.5,  40,  CARB,(-4,  1, -15, -5, 10, 22, 6,  0,), None,),
"gas mask"                  :(HELM,19450, 2.5,  30,  PLAS,(-3,  1, -6,  -1, 8,  36, 6,  0,), None,),
"respirator"                :(HELM,2490,  1.7,  25,  PLAS,(-3,  0, -6,  0,  13, 27, 3,  0,), None,),
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

    #Should melee damage be separated from ranged damage?
    #If you get claws and gain +2 dmg that should not affect gun damage.
    
           ##------- Type, $$$$, KG,  Dur, Cap,RT, Jam,Mat, (Rn,At,Dm,Pw, DV, AV, Asp,Msp,EL),Ammo,Flags,script
    # melee weapons
"stone"             :(TSTO,1,    0.35,50,  0,  0,  0,  STON,(10,3, 4, 0,  0,  0, -33, 0, PH,),None,(CRUSHES,), None,),
"stick"             :(MEL, 1,    0.6, 40,  0,  0,  0,  WOOD,(8, 2, 2, 0,  0,  0,  0, -6, PH,),None,(), None,),
"bone"              :(MEL, 1,    0.25,320, 0,  0,  0,  BONE,(8, 4, 4, 0,  0,  0,  0,  0, PH,),None,(CRUSHES,), None,),
"fork"              :(MEL, 2,    0.05,20,  0,  0,  0,  METL,(1, 3, 1, 0,  0,  0,  10, 0, PH,),None,(STABS,), None,),
"cudgel"            :(MEL, 2,    1.5, 550, 0,  0,  0,  WOOD,(5, 3, 9, 0,  -3, 0, -33,-15,PH,),None,(CRUSHES,), None,),
"war frisbee"       :(MEL, 3,    0.4, 5,   0,  0,  0,  PLAS,(12,4, 4, 0,  0,  0, -33,-3, PH,),None,(), None,),
"stone axe"         :(MEL, 5,    1.55,40,  0,  0,  0,  WOOD,(8, 5, 11,0,  -2, 0, -25,-15,PH,),None,(CHOPS,), None,),
"dart"              :(MEL, 6,    0.2, 15,  0,  0,  0,  METL,(14,8, 3, 0,  0,  0, -10, 0, PH,),None,(), None,),
"javelin"           :(MEL, 10,   0.5, 10,  0,  0,  0,  WOOD,(20,14,6, 0,  1,  0,  33,-9, PH,),None,(REACH,STABS,), None,),
"staff"             :(MEL, 15,   1.2, 260, 0,  0,  0,  WOOD,(10,9, 5, 0,  2,  0,  33,-18,PH,),None,(REACH,), None,),
"hammer"            :(MEL, 20,   1.15,650, 0,  0,  0,  METL,(8, 4, 12,0,  -1, 0, -33,-6, PH,),None,(CRUSHES,), None,),
"metal axe"         :(MEL, 25,   1.25,365, 0,  0,  0,  WOOD,(8, 5, 14,0,  -2, 0, -25,-12,PH,),None,(CHOPS,CUTS,), None,),
"spear"             :(MEL, 30,   1.5, 185, 0,  0,  0,  WOOD,(16,16,10,0,  2,  0,  33,-18,PH,),None,(REACH,STABS,CUTS,), None,),
"wooden sword"      :(MEL, 35,   1.2, 50,  0,  0,  0,  WOOD,(8, 7, 3, 0,  2,  0,  20,-6, PH,),None,(), None,),
"baton"             :(MEL, 55,   0.75,450, 0,  0,  0,  PLAS,(4, 6, 3, 0,  0,  0,  15,-3, PH,),None,(), None,),
"pocket knife"      :(MEL, 75,   0.2, 75,  0,  0,  0,  METL,(6, 8, 4, 0,  1,  0,  40, 0, PH,),None,(CUTS,STABS,), None,),
"crowbar"           :(MEL, 80,   0.8, 600, 0,  0,  0,  METL,(6, 8, 10,0,  0,  0, -33,-3, PH,),None,(CRUSHES,), None,),
"scalpel"           :(MEL, 95,   0.05,5,   0,  0,  0,  METL,(1, 16,6, 0,  0,  0,  33, 0, PH,),None,(CUTS,STABS,), None,),
"bayonet"           :(MEL, 110,  0.3, 100, 0,  0,  0,  METL,(10,10,5, 0,  2,  0,  40, 0, PH,),None,(CUTS,STABS,), None,),
"dagger"            :(MEL, 155,  0.4, 190, 0,  0,  0,  METL,(10,12,5, 0,  3,  0,  40, 0, PH,),None,(CUTS,STABS,), None,),
"metal sword"       :(MEL, 250,  1.25,220, 0,  0,  0,  METL,(8, 14,8, 0,  4,  0,  25,-6, PH,),None,(CUTS,STABS,CHOPS,), None,),
#chainsaw
#plasma sword
    # shields
"wooden shield"     :(OFF, 205,  5.3, 520, 0,  0,  0,  WOOD,(4, 0, 1, 0,  4,  3,  0, -21,PH,),None,(), None,),
"metal shield"      :(OFF, 540,  7.5, 900, 0,  0,  0,  METL,(1, 0, 2, 0,  3,  5,  0, -27,PH,),None,(), None,),
"riot shield"       :(OFF, 2250, 8.2, 450, 0,  0,  0,  PLAS,(1, 0, 1, 0,  1,  7,  0, -30,PH,),None,(), None,),
    # bows
"composite bow"     :(BOW, 125,  1.2, 50,  1,  1,  0,  BONE,(32,14,0, 4,  -1, 0, -10,-6,PH,),A_ARRO,(), None,),
"short bow"         :(BOW, 180,  1.1, 40,  1,  1,  0,  WOOD,(20,12,0, 2,  -1, 0, -10,-6,PH,),A_ARRO,(), None,),
"longbow"           :(BOW, 360,  1.8, 60,  1,  1,  0,  WOOD,(36,16,1, 6,  -2, 0, -20,-12,PH,),A_ARRO,(), None,),
    # exposives
"molotov"           :(EXPL,50,   1.2, 5,   0,  0,  0,  METL,(8, 3, 1, 1,  -1, 0, -10,-6,PH,),None,(), None,), #_molotov
"IED"               :(EXPL,75,   2.5, 5,   0,  0,  0,  METL,(8, 3, 1, 1,  -1, 0, -10,-6,PH,),None,(), None,), #_ied
"frag grenade"      :(EXPL,165,  0.8, 5,   0,  0,  0,  METL,(8, 3, 1, 1,  -1, 0, -10,-6,PH,),None,(), None,), #_fragBomb
"land mine"         :(EXPL,425,  5.0, 5,   0,  0,  0,  METL,(8, 3, 1, 1,  -1, 0, -10,-6,PH,),None,(), None,), #_fragMine
    # heavy weapons
"MK-18 shitstormer" :(HEVY,2090, 2.5, 220, 100,3,  0,  PLAS,(7, 3, 1, 25, -4, 0,  0, -15,BI,),A_HAZM,(), None,),
"raingun"           :(HEVY,2990, 2.85,175, 125,3,  0,  PLAS,(7, 5, 1, 40, -5, 0,  0, -18,CH,),A_ACID,(), None,),
"supersoaker 9000"  :(HEVY,3750, 3.5, 100, 200,5,  0,  PLAS,(9, 5, 0, 3,  -10,0,  10,-18,None,),A_FLUID,(), None,),
"spring cannon"     :(HEVY,1860, 7.3, 75,  1,  4,  0,  METL,(10,5, 0, 3,  -10,0, -33,-21,PH,),A_ANY,(), None,),
"flamethrower"      :(HEVY,5800, 12.7,100, 300,8,  0,  METL,(5, 15,2, 100,-15,0,  33,-40,FI,),A_FLAM,(), None,), #_flamethrower
#"napalm thrower"      :(HEVY,5800, 12.7,100, 300,8,  0,  METL,(5, 15,2, 100,-15,0,  33,-40,FI,),A_FLAM,(),), #_flamethrower
#"compressed air gun":(HEVY,5800, 12.7,100, 300,8,  0,  METL,(5, 15,2, 100,-15,0,  33,-40,FI,),A_FLAM,(),), #_flamethrower
    # guns
"hand cannon"       :(GUN, 145,  8.75,450, 1,  10, 15, METL,(8, 10,6, 8,  -15,1, -50,-30,PH,),A_BALL,(), None,),
"musket"            :(GUN, 975,  2.5, 120, 1,  8,  8,  WOOD,(14,8, 5, 6,  -3, 0, -33,-12,PH,),A_BALL,(), None,),
"flintlock pistol"  :(GUN, 1350, 1.3, 150, 1,  8,  12, WOOD,(10,6, 3, 0,   0, 0, -25,-3, PH,),A_BALL,(), None,),
"revolver"          :(GUN, 3990, 1.1, 360, 6,  1,  8,  METL,(15,8, 3, 3,   0, 0, -15,-3, PH,),A_BULL,(), None,),
"rifle"             :(GUN, 4575, 2.2, 280, 1,  1,  8,  WOOD,(36,12,5, 8,  -3, 0, -33,-12,PH,),A_BULL,(), None,),
"repeater"          :(GUN, 13450,2.0, 300, 7,  1,  7,  WOOD,(30,10,5, 8,  -3, 0, -15,-9, PH,),A_BULL,(), None,),
"'03 Springfield"   :(GUN, 26900,2.5, 350, 5,  1,  6,  WOOD,(60,16,5, 12, -3, 0, -33,-12,PH,),A_BULL,(), None,),
"luger"             :(GUN, 55450,0.9, 210, 8,  1,  10, METL,(18,12,3, 6,   0, 0, -6, -3, PH,),A_BULL,(), None,),
"shotgun"           :(GUN, 2150, 2.0, 325, 1,  1,  8,  WOOD,(12,6, 5, 2,  -2, 0, -33,-9, PH,),A_SHOT,(), None,),
"double barrel shotgun":(GUN,6200,2.8,285, 2,  1,  8,  WOOD,(12,6, 5, 2,  -3, 0, -33,-12,PH,),A_SHOT,(), None,),
    # energy weapons
"battery gun"       :(ENER,3250, 4.20,175, 20, 1,  0,  PLAS,(5, 40,2, 70, -7,  0, -60,-24,EL,),A_ELEC,(),),
                      
            ##------- Type, $$$$, KG,  Dur, Cap,RT,Jam,Mat, (Rn,At,Dm,Pw, DV, AV, Asp,Msp,ELEM),Ammo,{Misc.Mods},

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
"metal ball"            :(A_BALL,2,  0.1, 1, (-2, 0,  4,  0,), None,)
"Minni ball"            :(A_BALL,3,  0.1, 1, (0,  2,  6,  0,), None,)
"paper cartridge"       :(A_BALL,4,  0.15,1, (0,  2,  6,  0,), _paperCartridge,)
"birdshot shell"        :(A_SHOT,4,  0.1, 12,(-4, -9, 0,  0,), None,)
"shotgun shell"         :(A_SHOT,6,  0.1, 5, (-2, -5, 2,  0,), None,)
"shotgun slug"          :(A_SHOT,8,  0.1, 1, (0,  0,  10, -10,), None,)
"pistol cartridge"      :(A_BULL,6,  0.02,1, (0,  2,  3,  0,), None,)
"magnum cartridge"      :(A_BULL,16, 0.04,1, (-2, 4,  9,  -33,), None,)
"rifle cartridge"       :(A_BULL,15, 0.06,1, (5,  8,  6,  -15,), None,)
"hollow-point cartridge":(A_BULL,12, 0.04,1, (-5, -4, 12, -15,), None,)
"incendiary cartridge"  :(A_BULL,36, 0.08,1, (-2, 12, 12, -33,), _incendiary)
    }



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

    color = COL['accent']
    bgcol = COL['deep']
    
    world.add_component(ent, cmp.Name(name))
    world.add_component(ent, cmp.Position(x, y))
    world.add_component(ent, cmp.Draw(char=_type,color=color,bgcol=bgcol) )
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
    
    color = COL['accent']
    bgcol = COL['deep']
    
    world.add_component(ent, cmp.Name(name))
    world.add_component(ent, cmp.Position(x, y))
    world.add_component(ent, cmp.Draw( char=_type, color=color, bgcol=bgcol ))
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
#


# STUFF #
#  ITEMS / INTERACTABLE DUNGEON FEATURES #

##
###quick functions for multiple types of objects:
##def _hp(tt, value): #give a Thing a specified amount of HP and fully heal them
##    tt.stats.hpmax=value; rog.givehp(tt);
###give a random number of items to the inventory of Thing tt
##    #func is a function to build the items
##    #_min is minimum number of items possible to give
##    #_max is maximum "
##def _giveRandom(tt, func, _min, _max):
##    for ii in range((_min - 1) + dice.roll(_max - (_min - 1))):
##        item = func()
##        rog.give(tt, item)
        
#conversion functions:
# convert things into specific types of things by giving them certain data

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
    world.add_component(ent, cmp.ReactsToWater(diesInWaterFunc))
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
    statMods={cmp.CombatStats : {"atk":3, "dmg":2, "dfn":2,},}
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
def create_item(x,y,ID):
    name,typ,mat,fgcol,lo,kg,solid,push,script = STUFF[ID]
    tt = thing.Thing(x,y, _type=typ,name=name,color=COL[fgcol])
    tt.mass = kg
    tt.material=mat
    if lo: _hp(tt, lo)
    tt.isSolid = solid
    if push: rog.make(tt, CANPUSH)
    #_applyResistancesFromMaterial(tt, mat)
    return tt


# FOOD #


FOOD = {
'''
    Columns:
    #   $$$         cost
    #   KG          mass
    #   Mat         material
    #   script      script to run to initialize values for the food item
'''
#--Name-------------------$$$,  KG,   Mat,  script
"Corpse Button"         :(1,    0.03, FUNG, _food_morsel_bloody_nasty,),
"Hack Leaf"             :(1,    0.02, VEGG, BITTR,  1,   2,  0, 1,1,),
"Juniper Berry"         :(3,    0.01, VEGG, SWEET,  1,   1,  0, 0,0,),
"Coke Nut"              :(12,   0.02, WOOD, BITTR,  2,   2,  1, 1,1,),
"Silly Fruit"           :(8,    0.04, VEGG, SWEET,  3,   1,  0, 0,0,),
"Mole Rat Meat"         :(10,   0.15, FLSH, SAVOR,  4,   3,  0, 1,1,),
"Dwarf Giant Cap"       :(25,   0.05, FUNG, SAVOR,  6,   3,  0, 0,1,),
"Eel Meat"              :(20,   0.50, FLSH, SAVOR,  9,   1,  0, 0,1,),
"Human Meat"            :(40,   1.00, FLSH, SAVOR,  10,  4,  1, 1,1,),
"Infant Meat"           :(80,   0.50, FLSH, SAVOR,  12,  2,  0, 1,1,),
"Giant Cap"             :(100,  0.35, FUNG, SAVOR,  20,  6,  0, 0,1,),
    }


# FLUIDS #

 # TODO : implement fluids.


class Data:
    '''
        Fluid data
        each type of fluid has 1 unique fluid data object.
    '''

    def __init__(self, x,y, t=T_FLUID, name=None,
                 color=None, material=None, d=1,v=1,kg=1,
                 burns=False, putsout=False):

        self._type=t
        self.name=name
        self.color=color
        self.material=material
        self.density=d
        self.viscosity=v
        self.mass=kg
        self.flammable=burns
        self.extinguish=putsout  #does it put out fires?
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


            
        
#effects
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

#create a fluid
def create_fluid(x,y,ID,volume):
    fluid = world.create_entity(cmp.Position(x,y),cmp.FluidContainer())
##    fluid.add(ID, volume)
    return fluid

        
##
##def simulate_flow():
###idea: if any fluid tiles contain more than the maximum allowed,
##    #always flow outward using flood fill if necessary.
##    for fluid in rog.list_fluids():
##        #simultaneous cellular automata
##        newMap = TileMap(self.w,self.h)
##        newMap.COPY(rog.map())
##        #define some functions to reduce duplicate code
##        def _doYourThing(x,y,num,nValues): # alter a tile or keep it the same based on input
##            if nValues[num]==-1:
##                newMap.tile_change(x,y,offChar)
##            elif nValues[num]==1:
##                newMap.tile_change(x,y,onChar)
##        for ii in range(iterations):
##            for x in range(self.w):
##                for y in range(self.h):
##                    num = newMap.countNeighbors(x,y, onChar)
##                    _doYourThing(x,y,num,nValues)
##        self.COPY(newMap)
##        










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

