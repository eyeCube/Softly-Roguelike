'''
    gear.py

    Armor, helmets
    Functions for making gear items
'''


import random

from const import *
from colors import COLORS as COL
import rogue as rog
import thing
import action



NUMWPNSTATS = 3


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

FLSH = MAT_FLESH
LETH = MAT_LEATHER
CLTH = MAT_CLOTH
WOOD = MAT_WOOD
BONE = MAT_BONE
CARB = MAT_CARBON
PLAS = MAT_PLASTIC
METL = MAT_METAL
STON = MAT_STONE

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
        entn = rog.get(ent, cmp.Name)
        pos = rog.get(ent, cmp.Position)
        rog.set_fire(pos.x, pos.y)
        radius = 1
        rog.explosion("{}{}".format(entn.title,entn.name), pos.x,pos.y, radius)
    rog.world().add_component(tt, cmp.DeathFunction(deathFunc))
def _paperCartridge(tt):
    #do not need to load with gunpowder
    pass

def _molotov(tt):
    def func(self):
        diameter = 7
        radius = int(diameter/2)
        for i in range(diameter):
            for j in range(diameter):
                xx = self.x + i - radius
                yy = self.y + j - radius
                if not rog.in_range(self.x,self.y, xx,yy, radius):
                    continue
                rog.create_fluid(FL_NAPALM, xx,yy, dice.roll(3))
                rog.set_fire(xx,yy)
    tt.deathFunction = func


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
"carb garb"                 :(ARMR,1060,  22.5, 600, CARB,(-3,  3, -12, 0,  10, 10, 0,  0,), None,),
"boiled leather plate"      :(ARMR,1175,  12.5, 180, LETH,( 0,  3, -6,  0,  5,  5,  15, 0,), None,),
"riot gear"                 :(ARMR,3490,  20.5, 500, CARB,(-2,  5, -12, 0,  33, 25, 0,  0,), None,),
"metal gear"                :(ARMR,9950,  27.5, 740, METL,(-4,  7, -18, 0,  5,  5,  -10,0,), None,),
"full metal suit"           :(ARMR,12000, 35.1, 850, METL,(-5,  10,-21, 0,  5,  10, -20,0,), None,),
"graphene armor"            :(ARMR,58250, 16.5, 900, CARB,(-2,  8, -9,  0,  20, 20, 30, 0,), None,),
"bullet-proof armor"        :(ARMR,135000,12.8, 1000,CARB,(-1,  12,-3,  0,  5,  5,  0,  0,), None,),
"space suit"                :(ARMR,36000, 40.0, 50,  CARB,(-15, 3, -33, 0,  20, 40, 6,  0,), None,),
"hazard suit"               :(ARMR,2445,  14.5, 75,  PLAS,(-12, 2, -24, 0,  5,  50, 12, 0,), None,),
"disposable PPE"            :(ARMR,110,   9.25, 25,  PLAS,(-9,  1, -15, 0,  -15,30, 3,  0,), None,),
"wetsuit"                   :(ARMR,1600,  8.2,  50,  PLAS,( 0,  0, -6,  0,  33, 5,  21, 0,), None,),
"fire blanket"              :(BACK,600,   12.4, 175, CLTH,(-3,  1, -9,  0,  40, 15, 9,  0,), None,),
"burn jacket"               :(ARMR,1965,  19.5, 150, CLTH,(-5,  2, -12, 0,  55, 15, 15, 0,), None,),
    #Helmets
"bandana"                   :(HELM,40,    0.1,  20,  CLTH,( 2,  0,  0,  0,  5,  10, 3,  0,), None,),
"skin mask"                 :(HELM,180,   1.25, 10,  FLSH,( 1,  0,  0,  -1, 0,  5,  0,  0,), None,),
"wood mask"                 :(HELM,10,    1.0,  30,  WOOD,(-1,  1, -3,  -5, -5, 5,  3,  0,), None,),
"skull helm"                :(HELM,750,   2.8,  115, BONE,(-3,  2, -9,  -3, 5,  5,  6,  0,), None,),
"motorcycle helmet"         :(HELM,1500,  0.75, 145, PLAS,(-1,  2, -3,  -3, 0,  5,  6,  0,), None,),
"metal mask"                :(HELM,6000,  2.2,  275, METL,(-3,  3, -6,  -7, 0,  5,  -6, 0,), None,),
"metal helm"                :(HELM,8500,  3.0,  300, METL,(-4,  4, -9,  -10,0,  5,  -12,0,), None,),
"graphene mask"             :(HELM,21850, 0.8,  285, CARB,(-2,  2, -3,  -7, 10, 10, 9,  0,), None,),
"graphene helmet"           :(HELM,25450, 1.2,  310, CARB,(-2,  3, -3,  -7, 10, 10, 9,  0,), None,),
"kevlar hat"                :(HELM,89500, 1.5,  350, CARB,(-2,  4, -3,  0,  0,  0,  0,  0,), None,),
"space helmet"              :(HELM,51950, 3.5,  40,  CARB,(-4,  1, -15, -5, 15, 25, 6,  0,), None,),
"gas mask"                  :(HELM,19450, 2.5,  30,  PLAS,(-3,  1, -6,  -1, 10, 45, 6,  0,), None,),
"respirator"                :(HELM,2490,  1.7,  25,  PLAS,(-3,  0, -6,  0,  20, 30, 3,  0,), None,),
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









