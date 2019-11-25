'''
    const.py
    Softly Into the Night, a sci-fi/Lovecraftian roguelike
    Copyright (C) 2019 Jacob Wharton.

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


from enum import Flag, auto

import tcod as libtcod


#------------#
# Exceptions #
#------------#

class Error_wrongNumberCommandsLoaded(Exception):
#tried to load key commands from key_bindings
#but received the wrong number of commands.
    pass


#------------#
#  History   #
#------------#

HISTORY_EPITAPHS=( # Procedurally generated?
"here lies a mother, a father, a hermaphrodite, and a friend",
"he died doing who he loved",
"Richy ",
    )
HISTORY_ROADNAMES=(
"Any Witch Way",
"Roadkill Rd",
"Murder Dr",
"Raven Rider Rd",
"Avelyn Ave",
"Bullshit Blvd",
"",
    )



#-----------------------#
# Init Global Constants #
#-----------------------#

GAME_TITLE = "Softly Into the Night"

ROOMW       = 80            #max level size, width and height
ROOMH       = 50
MAXLEVEL    = 20            #deepest dungeon level
TILES_PER_ROW = 16          # Num tiles per row (size of the char sheet 
TILES_PER_COL = 16          # " per column         used for ASCII display)

CRAFT_CONSTRUCT_MULTIPLIER = 2  # construction time multiplier for all crafting recipes


#
# Engine Constants
#

# special character key inputs
K_ESCAPE    = 19
K_UP        = 24
K_DOWN      = 25
K_RIGHT     = 26
K_LEFT      = 27
K_ENTER     = 28
K_PAGEUP    = 30
K_PAGEDOWN  = 31
K_HOME      = 127
K_END       = 144
K_BACKSPACE = 174
K_DELETE    = 175
K_INSERT    = 254


#direction
DIRECTIONS={
    (-1,-1) : 'northwest',
    (1,-1)  : 'northeast',
    (0,-1)  : 'north',
    (-1,0)  : 'west',
    (0,0)   : 'self',
    (1,0)   : 'east',
    (-1,1)  : 'southwest',
    (0,1)   : 'south',
    (1,1)   : 'southeast',
}
DIRECTIONS_TERSE={
    (-1,-1) : 'NW',
    (1,-1)  : 'NE',
    (0,-1)  : 'N',
    (-1,0)  : 'W',
    (0,0)   : 'self',
    (1,0)   : 'E',
    (-1,1)  : 'SW',
    (0,1)   : 'S',
    (1,1)   : 'SE',
}
DIRECTION_FROM_INT={
    0   : (1,0,),
    1   : (1,-1,),
    2   : (0,-1,),
    3   : (-1,-1,),
    4   : (-1,0,),
    5   : (-1,1,),
    6   : (0,1,),
    7   : (1,1,),
    }
##DIRECTIONS_DIAGONAL=(
##    (-1,-1,),
##    (1,1,),
##    (-1,1,),
##    (1,-1,),
##    )
##DIRECTIONS_ORTHOGONAL=(
##    (0,-1,),
##    (0,1,),
##    (-1,0,),
##    (1,0,),
##    )


# titles
i=1;
TITLE_NONE          = i;i+=1;
TITLE_THE           = i;i+=1;
TITLE_MR            = i;i+=1;
TITLE_MRS           = i;i+=1;
TITLE_MS            = i;i+=1;
TITLE_SIR           = i;i+=1;
TITLE_THEHONORABLE  = i;i+=1;


# death types (sent to DeathFunction component to tell it how the thing died)
i=1;
DEATH_SHATTERED     = i;i+=1;
DEATH_STABBED       = i;i+=1;
DEATH_CUT           = i;i+=1;
DEATH_CRUSHED       = i;i+=1;
DEATH_MELTED        = i;i+=1; # SHOULD THESE BE HANDLED DIFFERENTLY?
DEATH_BURNED        = i;i+=1;
DEATH_RUSTED        = i;i+=1;
DEATH_ELECTROCUTED  = i;i+=1;





#
# Crafting Recipe Categories
#
i=1;
CRC_PLASTIC         = i;i+=1; # plasticraft (whittling, chiseling)
CRC_WOOD            = i;i+=1; # woodcraft (whittling, chiseling)
CRC_BONE            = i;i+=1; # bonecraft (whittling, chiseling)
CRC_STONE           = i;i+=1; # stonecraft (chiseling)
CRC_METAL           = i;i+=1; # metalcraft (forging)
CRC_GLASS           = i;i+=1; # glasscraft (chiseling)
CRC_GLASSBLOWING    = i;i+=1; # glass blowing, separate skill from glass chiseling
CRC_CLAY            = i;i+=1; # potter
CRC_LEATHER         = i;i+=1; # tanner
CRC_BOILEDLEATHER   = i;i+=1; # boiled leathercraft
CRC_RUBBER          = i;i+=1; # Joergcraft
CRC_CLOTH           = i;i+=1; # tailor
CRC_FLESH           = i;i+=1; # fleshcraft
CRC_ARMOR           = i;i+=1; # armor making
CRC_ASSEMBLY        = i;i+=1; # basic putting stuff together skills
CRC_SURVIVAL        = i;i+=1; # living off the land
CRC_SWORDS          = i;i+=1; # swordsmithing (parents: metalcraft)
CRC_GUNS            = i;i+=1; # gunsmithing (parents: wood, metalcraft)
CRC_BOWS            = i;i+=1; # 
CRC_ARROWS          = i;i+=1; # 
CRC_CARTRIDGES      = i;i+=1; # 



#
# Crafting Recipe Types (which table to access)
#
i=1;
CRT_WEAPONS         = i;i+=1;
CRT_ARMOR           = i;i+=1;
CRT_TOOLS           = i;i+=1;
CRT_STUFF           = i;i+=1;
CRT_RAWMATS         = i;i+=1;



#
# Flags
#

# Monster and item flags

i = 1
RAVAGED     = i; i+=1;  # Creature is starved: strong desire for food
THIEF       = i; i+=1;  # Creature desires gold / treasure and will steal it
MEAN        = i; i+=1;  # Creature is always hostile to rogues
DEAD        = i; i+=1;  # Is dead
FLYING      = i; i+=1;  # Is currently flying
IMMUNE      = i; i+=1;  # Immune to poison
REACH       = i; i+=1;  # Has long reach
NVISION     = i; i+=1;  # Has Night vision
INVIS       = i; i+=1;  # Is invisible
SEEINV      = i; i+=1;  # Can see invisible things
SEEXRAY     = i; i+=1;  # LOS not blocked by walls
TWOHANDS    = i; i+=1;  # 2-handed only (when wielded in hands)
ISSOLID     = i; i+=1;  # Is solid (cannot walk through it)
CANCOUNTER  = i; i+=1;  # Is able to counter-attack this turn
DIRTY_STATS = i; i+=1;  # dirty flag: needs updating stats


#
# Gameplay Constants
#

# global multipliers
# the displayed integer value in-game and in the code is the same
#   but in-engine, the actual value is always an integer.
MULT_VALUE          = 12    # 12 pence == 1 pound. multiplier for value of all things
MULT_MASS           = 1000  # 1 mass unit == 1 gram. multiplier for mass of all things (to make it stored as an integer by Python)
MULT_DMG_AV_HP      = 10    # finer scale for AV/dmg but only each 10 makes any difference. Shows up /10 without the decimal in-game and functions the same way by the mechanics.
MULT_PEN_PRO        = 10    # " (6.8 penetration functions as 6 pen, and displays as 6 in-game. Truncated decimal.)

# fire / ice
FIRE_THRESHOLD  = 70 # lowest temperature at which things may combust (should this be a np grid array that has different values for each tile depending on what kid of fuel is there? May be too complex but would add more functionality for e.g. high fuel objects that have a high flash point like explosives)
ENVIRONMENT_DELTA_HEAT = -0.1 # global change in heat each iteration of heat dispersion
HEATMIN         = -300 # minimum temperature
HEATMAX         = 16000 # maximum temperature
FREEZE_THRESHOLD= -30
FREEZE_DAMAGE   = 10  # damage dealt when you become frozen

#fluids
MAX_FLUID_IN_TILE   = 1000 * MULT_MASS


#misc
DUR_STATMODS={ # durability % affects stats (multipliers)
    # stm1: stat mod 1 affects:
        # Atk, Prot, Pen, 
    # stm2: stat mod 2 affects:
        # Dmg, AV, DV, 
# %  : (stm1, stm2)
0.90 : (0.92,0.961538,),
0.75 : (0.85,0.9,),
0.50 : (0.7, 0.8,),
0.25 : (0.5, 0.666667,),
0.10 : (0.3333333,0.5,),
    }
RUSTEDNESS={
# amt   - rustedness amount
# sm    - stat modifier
# vm    - value modifier (value cannot go below the cost of the raw mats)
#amt : (sm,  vm,  name mod)
40   : (1.0, 0.95,"rusting ",),
160  : (0.9, 0.8, "rusty ",),
333  : (0.75,0.5, "rusted ",),
667  : (0.5, 0.25,"badly rusted ",),
1000 : (0.25,0.1, "fully rusted ",),
    }
ROTTEDNESS={
# amt   - rot amount
# sm    - stat modifier
# vm    - value modifier
#amt : (sm,  vm,  name mod)
100  : (0.9, 0.75,"rotting ",),
333  : (0.7, 0.33,"rotted ",),
667  : (0.3, 0.1, "badly rotted ",),
1000 : (0.1, 0.01,"fully rotted ",),
    }


# base stats for player
BASE_RESFIRE    = 0
BASE_RESCOLD    = 0
BASE_RESBIO     = 0
BASE_RESPHYS    = 0
BASE_RESELEC    = 0
BASE_RESPAIN    = 0
BASE_RESBLEED   = 0
BASE_RESRUST    = 100
BASE_RESROT     = 100
BASE_RESWET     = 0
BASE_RESLIGHT   = 0
BASE_RESSOUND   = 0
BASE_COURAGE    = 24
BASE_SCARY      = 6
BASE_BAL        = 12
BASE_GRA        = 6
BASE_CTR        = 0
BASE_ATK        = 4
BASE_DMG        = 0
BASE_PEN        = 2
BASE_DFN        = 10
BASE_ARM        = 2
BASE_PRO        = 6
BASE_SPD        = 100
BASE_MSP        = 100
BASE_ASP        = 100
BASE_HP         = 20
BASE_MP         = 200
BASE_CARRY      = 0
BASE_STR        = 12
BASE_CON        = 12
BASE_INT        = 12
BASE_SIGHT      = 20 # TODO: set to 0, get all sight/hearing from body compo
BASE_HEARING    = 60

# attributes
ATT_INT_AUGMENTATIONS   = 0.5   # mental augmentation slots per int
ATT_INT_IDENTIFY        = 1     # identification ability per int
ATT_INT_SOCIAL          = 1     # social influence gained per int
ATT_CON_AUGMENTATIONS   = 0.5   # physical augmentation slots per con
ATT_CON_HP              = 2     # HP gained per con
ATT_CON_STAMINA         = 20    # stamina gained per con
ATT_CON_GEARCARRY       = 0.02  # reduction of Msp penalty for equipping gear
ATT_CON_CARRY           = 1000  # carrying capacity per con (g)
ATT_STR_CARRY           = 1000  # carrying capacity per str (g)
ATT_STR_HP              = 0.5   # HP gained per str
ATT_STR_DMG             = 0.4   # damage gained per strength unit applied
ATT_STR_ATK             = 0.2   # attack gained per strength unit applied
ATT_STR_PEN             = 0.3   # penetration gained per strength unit applied

##P_AUGS={ # physical augmentations
##PAUG_
##    }



# 1-h / 2-h constants
# attribute bonuses and multipliers
MULT_1HANDBONUS_STR_DMG = 0.5     # strength bonus for 1-h wielding per STR
MULT_1HANDBONUS_STR_PEN = 0.25    # strength bonus for 1-h wielding per STR
MULT_2HANDBONUS_STR_DMG = 0.75    # strength bonus for 2-h wielding per STR
MULT_2HANDBONUS_STR_PEN = 0.5     # strength bonus for 2-h wielding per STR
# penalty to offhand weapons wielded (other than weapons designed for offhand)
OFFHAND_PENALTY_DFN = 0.5   # multiplier
OFFHAND_PENALTY_ARM = 0.5   # multiplier
OFFHAND_PENALTY_PRO = 0.5   # multiplier
# bonuses for when you fight with a 1-handed weapon in 2 hands
MOD_2HANDBONUS_ASP    = 25      # attack speed you gain
MOD_2HANDBONUS_ATK    = 4       # attack you gain
MULT_2HANDBONUS_DMG   = 1.2     # damage MULTIPLIER
MOD_2HANDBONUS_PEN    = 2       # penetration you gain
MOD_2HANDBONUS_DFN    = 2       # defense you gain
MOD_2HANDBONUS_ARM    = 1       # armor you gain
MOD_2HANDBONUS_PRO    = 1       # protection you gain
# penalties for when you fight with a 2-handed weapon in 1 hand
MOD_1HANDPENALTY_ASP  = 75      # attack speed you lose
MOD_1HANDPENALTY_ATK  = 10      # attack you lose
MULT_1HANDPENALTY_DMG = 0.5     # multiplier
MULT_1HANDPENALTY_PEN = 0.5     # multiplier
MOD_1HANDPENALTY_DFN  = 5       # defense you lose
MOD_1HANDPENALTY_ARM  = 2       # armor you lose
MOD_1HANDPENALTY_PRO  = 2       # protection you lose


# maximum + quality upgrade
MAXGRIND_GRAPHENE   = 1
MAXGRIND_GLASS      = 2
MAXGRIND_CERAMIC    = 2
MAXGRIND_PLASTIC    = 3
MAXGRIND_WOOD       = 4
MAXGRIND_BONE       = 4
MAXGRIND_STONE      = 4
MAXGRIND_METAL      = 5

# $$ values of things not given values elsewhere
VAL_HUMAN           = 5000

#combat
CMB_ROLL_PEN        = 6     # dice roll for penetration bonus
CMB_ROLL_ATK        = 20    # dice roll for to-hit bonus (Attack)
CMB_MDMGMIN         = 0.6   # multplier for damage (minimum)
CMB_MDMG            = 0.4   # multplier for damage (diff. btn min/max)


#sounds
VOLUME_DEAFEN       = 500

#items
FOOD_BIGMEAL        = 96
FOOD_MEAL           = 24
FOOD_RATION         = 12
FOOD_SERVING        = 4
FOOD_MORSEL         = 1
FOOD_BIGMEAL_NRG    = 1200000   # 1800000       AP cost for eating
FOOD_MEAL_NRG       = 300000    #  600000
FOOD_RATION_NRG     = 200000    #  300000
FOOD_SERVING_NRG    = 60000     #  100000
FOOD_MORSEL_NRG     = 15000     #   25000
SATIETY_PER_RATION  = 100   # how much hunger is healed per ration of food
WATER_HYDRATION     = 100   # how much hydration is healed per unit of water

#crafting
CRAFT_NRG_MULT      = 5     # multiplier for crafting AP cost (all recipes)

#skills
SKILLMAX            = 2     # highest skill level you can attain

#stats
##SUPER_HEARING       = 500   # hearing level you need to be able to tell direction and volume of sounds
AVG_HEARING         = 100
AVG_SPD             = 100

#energy (action potential or AP) cost to perform actions
NRG_MOVE            = 100   # on default terrain (flat ground) 
NRG_ATTACK          = 200   
NRG_BOMB            = 150   
NRG_PICKUP          = 50    # grab thing and wield it (requires empty hand)
NRG_POCKET          = 100   # picking up and putting in your inventory
NRG_RUMMAGE         = 50    # Cost to look at the contents of a container
NRG_OPEN            = 50    # Cost to open a door
NRG_CLOSE           = 20    # Cost to close a door or simple container
NRG_TAKE            = 100   # Cost of picking an item from a container
NRG_EXAMINE         = 200
NRG_QUAFF           = 100
NRG_EAT             = 300   # default AP cost per unit of consumption to eat
NRG_READ            = 50    # cost to read a simple thing (phrase/sentence)
NRG_READPARAGRAPH   = 250   # cost to read an idea (paragraph/complex sentence)
NRG_READPAGE        = 2500  # cost to read a page of a book (several ideas forming one meta-idea that requires you to read it all to understand)
NRG_USE             = 100   # generic use function
NRG_WIELD           = 75    # default time it takes to brandish a weapon (medium sized 1-h, like a club). Notice "default" keyword. It can be more or less depending on context/skill of user, etc.
NRG_WIELDSMALL      = 25    # default time it takes to brandish a weapon (small or easy to brandish, like handguns, knives, swords, etc.)
NRG_WIELDLARGE      = 200   # default time it takes to brandish a weapon (large / 2-h)
NRG_WIELDXLARGE     = 400   # default time it takes to brandish a weapon (largest 2-h weapons)
# multipliers
NRGM_QUICKATTACK    = 0.6
STAM_QUICKATTACK    = 1.5

# skills
SKLMOD_ARMOR_PRO    = 1.25
SKLMOD_ARMOR_AV     = 1.25
SKLMOD_ARMOR_DV     = 1.25



# statuses of bodies / body parts

i=0;
BODYPOS_UPRIGHT     = i; i+=1;
BODYPOS_CROUCHED    = i; i+=1;
BODYPOS_SEATED      = i; i+=1;
BODYPOS_SUPINE      = i; i+=1;
BODYPOS_PRONE       = i; i+=1;

i=0;
BONESTATUS_NORMAL       = i; i+=1;
BONESTATUS_DAMAGED      = i; i+=1; # bone is damaged, susceptible to fracture or breakage
BONESTATUS_FRACTURED    = i; i+=1; # hairline fracture
BONESTATUS_CRACKED      = i; i+=1; # badly cracked
BONESTATUS_BROKEN       = i; i+=1; # fully broken in half
BONESTATUS_MULTIBREAKS  = i; i+=1; # fully broken in half in multiple places
BONESTATUS_SHATTERED    = i; i+=1; # broken into many pieces
BONESTATUS_MANGLED      = i; i+=1; # bone is in utter ruin

i=0;
MUSCLESTATUS_NORMAL     = i; i+=1;
MUSCLESTATUS_SORE       = i; i+=1; # muscle is sore from a workout or from massaging out knots
MUSCLESTATUS_KNOTTED    = i; i+=1; # muscle has knots that need massage
MUSCLESTATUS_CONTUSION  = i; i+=1; # bruised
MUSCLESTATUS_STRAINED   = i; i+=1; # muscle mildly torn
MUSCLESTATUS_TORN       = i; i+=1; # muscle badly torn
MUSCLESTATUS_RIPPED     = i; i+=1; # muscle is mostly ripped in half
MUSCLESTATUS_RUPTURED   = i; i+=1; # ruptured tendon or fully ripped in half muscle belly
MUSCLESTATUS_MANGLED    = i; i+=1; # muscle is in utter ruin

i=0;
ARTERYSTATUS_NORMAL     = i; i+=1;
ARTERYSTATUS_CLOGGED    = i; i+=1; # clogged, not working at full capacity
ARTERYSTATUS_OPEN       = i; i+=1; # artery opened, causing massive bleeding
ARTERYSTATUS_CUT        = i; i+=1; # fully cut, requiring urgent surgery

i=0;
SKINSTATUS_NORMAL       = i; i+=1;
SKINSTATUS_RASH         = i; i+=1; # irritation / inflammation
SKINSTATUS_SCRAPED      = i; i+=1; # very mild abrasion (a boo-boo)
SKINSTATUS_MINORABRASION= i; i+=1; # mild abrasion
SKINSTATUS_MAJORABRASION= i; i+=1; # serious deep and/or wide-ranging scrape
SKINSTATUS_CUT          = i; i+=1; # cut open
SKINSTATUS_DEEPCUT      = i; i+=1; # deeply cut to the muscle
SKINSTATUS_BURNED       = i; i+=1; # skin is burned at the surface level (overwrite cuts and abrasions)
SKINSTATUS_DEEPBURNED   = i; i+=1; # skin is burned at a deep level (overwrite all of the above)
SKINSTATUS_SKINNED      = i; i+=1; # skin is partially removed
SKINSTATUS_FULLYSKINNED = i; i+=1; # skin is fully / almost fully removed

i=0;
BRAINSTATUS_NORMAL      = i; i+=1; # swelling brain is a status effect, not a brain status
BRAINSTATUS_CONTUSION   = i; i+=1; # brain bruise - mild injury
BRAINSTATUS_CONCUSSION  = i; i+=1; # concussion - altered mental state maybe unconciousness
BRAINSTATUS_DAMAGE      = i; i+=1; # temporary brain damage
BRAINSTATUS_PERMDAMAGE  = i; i+=1; # permanent brain damage
BRAINSTATUS_MAJORDAMAGE = i; i+=1; # MAJOR permanent brain damage
BRAINSTATUS_DEAD        = i; i+=1; # braindead

i=0;
HAIRSTATUS_NORMAL       = i; i+=1;
HAIRSTATUS_DAMAGED      = i; i+=1; # minor damage to hair
HAIRSTATUS_SINGED       = i; i+=1; # minor burn
HAIRSTATUS_BURNED       = i; i+=1; # badly burned
# destroyed hair == no hair (status==NORMAL and length==0)

i=0;
HEARTSTATUS_NORMAL      = i; i+=1;
HEARTSTATUS_INJURED     = i; i+=1;

i=0;
LUNGSTATUS_NORMAL       = i; i+=1;
LUNGSTATUS_IRRITATED    = i; i+=1; # lung inflamed
LUNGSTATUS_CLOGGED      = i; i+=1; # can't breathe; lung clogged up with something

i=0;
GUTSSTATUS_NORMAL       = i; i+=1;
GUTSSTATUS_UPSET        = i; i+=1; # might cause vomiting / diarrhea
GUTSSTATUS_SICK         = i; i+=1; # likely to cause vomiting / diarrhea
GUTSSTATUS_ILL          = i; i+=1; # guaranteed to cause vomiting / diarrhea

# Penalties for BPP statuses
# skin
ADDMODS_BPP_SKINSTATUS = { # stat : value
SKINSTATUS_RASH         :{'resbio':-1,'respain':-2,'resbleed':-2,'resfire':-2,},
SKINSTATUS_SCRAPED      :{'resbio':-2,'respain':-3,'resbleed':-4,'resfire':-3,},
SKINSTATUS_MINORABRASION:{'resbio':-3,'respain':-5,'resbleed':-6,'resfire':-4,},
SKINSTATUS_CUT          :{'resbio':-10,'respain':-5,'resbleed':-10,},
SKINSTATUS_MAJORABRASION:{'resbio':-10,'respain':-10,'resbleed':-10,'resfire':-6,},
SKINSTATUS_DEEPCUT      :{'resbio':-25,'respain':-10,'resbleed':-20,},
SKINSTATUS_BURNED       :{'resbio':-5,'respain':-10,'resbleed':-10,'resfire':-10,},
SKINSTATUS_DEEPBURNED   :{'resbio':-10,'respain':-20,'resbleed':-20,'resfire':-20,},
SKINSTATUS_SKINNED      :{'resbio':-10,'respain':-10,'resbleed':-20,'resfire':-10,},
SKINSTATUS_FULLYSKINNED :{'resbio':-15,'respain':-20,'resbleed':-40,'resfire':-20,},
    }
# face
ADDMODS_BPP_FACE_SKINSTATUS = { # stat : value
SKINSTATUS_RASH         :{'beauty':-2,'intimidation':1,'resbio':-2,'respain':-2,'resbleed':-4,'resfire':-4,},
SKINSTATUS_SCRAPED      :{'beauty':-2,'intimidation':1,'resbio':-4,'respain':-3,'resbleed':-8,'resfire':-6,},
SKINSTATUS_MINORABRASION:{'beauty':-4,'intimidation':1,'resbio':-6,'respain':-5,'resbleed':-12,'resfire':-8,},
SKINSTATUS_MAJORABRASION:{'beauty':-6,'intimidation':1,'resbio':-12,'respain':-10,'resbleed':-20,'resfire':-12,},
SKINSTATUS_CUT          :{'beauty':-2,'intimidation':1,'resbio':-20,'respain':-5,'resbleed':-20,},
SKINSTATUS_DEEPCUT      :{'beauty':-6,'intimidation':2,'resbio':-50,'respain':-10,'resbleed':-40,},
SKINSTATUS_BURNED       :{'beauty':-6,'intimidation':3,'resbio':-10,'respain':-10,'resbleed':-20,'resfire':-15,},
SKINSTATUS_DEEPBURNED   :{'beauty':-12,'intimidation':6,'resbio':-20,'respain':-20,'resbleed':-40,'resfire':-30,},
SKINSTATUS_SKINNED      :{'beauty':-24,'intimidation':10,'resbio':-20,'respain':-10,'resbleed':-40,'resfire':-15,},
SKINSTATUS_FULLYSKINNED :{'beauty':-48,'intimidation':20,'resbio':-30,'respain':-20,'resbleed':-60,'resfire':-30,},
    }
# head
MULTMODS_BPP_HEAD_BONESTATUS = { # stat : value
BONESTATUS_FRACTURED    :{'int':0.9,'bal':0.9,'sight':0.9,'mpmax':0.9, 'mp':0.9,},
BONESTATUS_CRACKED      :{'int':0.8,'bal':0.8,'sight':0.8,'mpmax':0.8, 'mp':0.8,},
BONESTATUS_BROKEN       :{'int':0.7,'bal':0.7,'sight':0.7,'mpmax':0.7, 'mp':0.7,},
BONESTATUS_SHATTERED    :{'int':0.6,'bal':0.6,'sight':0.6,'mpmax':0.6, 'mp':0.6,},
    }
# brain
ADDMODS_BPP_BRAIN_STATUS = { # stat : value
BRAINSTATUS_CONTUSION   :{'atk':-2,'dfn':-2,},
BRAINSTATUS_CONCUSSION  :{'atk':-4,'dfn':-4,},
BRAINSTATUS_DAMAGE      :{'atk':-6,'dfn':-6,},
BRAINSTATUS_PERMDAMAGE  :{'atk':-8,'dfn':-8,},
    }
MULTMODS_BPP_BRAIN_STATUS = { # stat : value
BRAINSTATUS_CONTUSION   :{'int':0.9,'bal':0.9,'sight':0.9,'hearing':0.9,'mpmax':0.9,'mp':0.9,},
BRAINSTATUS_CONCUSSION  :{'int':0.8,'bal':0.8,'sight':0.8,'hearing':0.8,'mpmax':0.8,'mp':0.8,},
BRAINSTATUS_DAMAGE      :{'int':0.7,'bal':0.7,'sight':0.7,'hearing':0.7,'mpmax':0.7,'mp':0.7,},
BRAINSTATUS_PERMDAMAGE  :{'int':0.6,'bal':0.6,'sight':0.6,'hearing':0.6,'mpmax':0.6,'mp':0.6,},
    }
# arm
ADDMODS_BPP_ARM_BONESTATUS = { # stat : value
BONESTATUS_FRACTURED    :{'atk':-1,'dfn':-1,'gra':-2,'respain':-5,},
BONESTATUS_CRACKED      :{'atk':-2,'dfn':-2,'gra':-4,'respain':-10,},
BONESTATUS_BROKEN       :{'atk':-3,'dfn':-3,'gra':-6,'respain':-15,},
BONESTATUS_SHATTERED    :{'atk':-4,'dfn':-4,'gra':-8,'respain':-20,},
    }
ADDMODS_BPP_ARM_MUSCLESTATUS = { # stat : value
MUSCLESTATUS_SORE       :{'respain':-5,},
MUSCLESTATUS_KNOTTED    :{'asp':-3,'respain':-5,},
MUSCLESTATUS_CONTUSION  :{'asp':-3,'respain':-5,'resbleed':-5,},
MUSCLESTATUS_STRAINED   :{'atk':-1,'dfn':-1,'asp':-5,'gra':-1,'resbleed':-2,},
MUSCLESTATUS_TORN       :{'atk':-2,'dfn':-2,'asp':-10,'gra':-2,'resbleed':-4,},
MUSCLESTATUS_RIPPED     :{'atk':-3,'dfn':-3,'asp':-15,'gra':-3,'resbleed':-6,},
MUSCLESTATUS_RUPTURED   :{'str':-1,'atk':-4,'dfn':-4,'asp':-20,'gra':-4,'resbleed':-8,},
    }
# leg
ADDMODS_BPP_LEG_BONESTATUS = { # stat : value
BONESTATUS_FRACTURED    :{'atk':-1,'dfn':-1,'gra':-2,'respain':-5,},
BONESTATUS_CRACKED      :{'atk':-2,'dfn':-2,'gra':-4,'respain':-10,},
BONESTATUS_BROKEN       :{'atk':-3,'dfn':-3,'gra':-6,'respain':-15,},
BONESTATUS_SHATTERED    :{'atk':-4,'dfn':-4,'gra':-8,'respain':-20,},
    }
MULTMODS_BPP_LEG_BONESTATUS = { # stat : value
BONESTATUS_FRACTURED    :{'bal':0.9,'msp':0.83333,}, #5/6
BONESTATUS_CRACKED      :{'bal':0.8,'msp':0.66667,}, #2/3
BONESTATUS_BROKEN       :{'bal':0.7,'msp':0.5,},     #1/2
BONESTATUS_SHATTERED    :{'bal':0.6,'msp':0.33333,}, #1/3
    }
ADDMODS_BPP_LEG_MUSCLESTATUS = { # stat : value
MUSCLESTATUS_SORE       :{'respain':-5,},
MUSCLESTATUS_KNOTTED    :{'msp':-3,'respain':-5,},
MUSCLESTATUS_CONTUSION  :{'msp':-3,'respain':-5,'resbleed':-5,},
MUSCLESTATUS_STRAINED   :{'atk':-1,'dfn':-1,'msp':-8,'gra':-1,'resbleed':-2,'bal':-1,},
MUSCLESTATUS_TORN       :{'atk':-2,'dfn':-2,'msp':-16,'gra':-2,'resbleed':-4,'bal':-2,},
MUSCLESTATUS_RIPPED     :{'atk':-3,'dfn':-3,'msp':-24,'gra':-3,'resbleed':-6,'bal':-3,},
MUSCLESTATUS_RUPTURED   :{'str':-1,'atk':-4,'dfn':-4,'msp':-32,'gra':-4,'resbleed':-8,'bal':-4,},
    }



#STATUSES

# bleed
BLEED_PLASTIC   = 6     # default bleed values for sharpened weapons of material types
BLEED_WOOD      = 12
BLEED_BONE      = 12
BLEED_STONE     = 12
BLEED_GLASS     = 96
BLEED_CERAMIC   = 72
BLEED_METAL     = 24
BLEED_STEEL     = 48
BLEED_GRAPHENE  = 192
BLEED_DIAMONITE = 144

#wet
WET_RESFIRE     = 50    # fire resistance gained while wet

#sprint
SPRINT_SPEEDMOD     = 100   # move speed bonus when you sprint

#hasty
HASTE_SPEEDMOD      = 50    # speed bonus when hasty

#slow
SLOW_SPEEDMOD       = -33   # speed penalty while slowed (PERCENTAGE?)

# temp (fire)
FIRE_METERLOSS  = -1    #temperature points lost per turn
FIRE_METERGAIN  = 1
FIRE_METERMAX   = 1000  #maximum temperature a thing can reach
FIRE_MAXTEMP    = 400   #max temperature you can reach from normal means
FIRE_TEMP       = 100   #avg. temperature at which a thing will set fire
FIRE_BURN       = 34    #dmg fire deals to things (in fire damage) per turn
FIRE_PAIN       = 10    #fire hurts!
FIRE_DAMAGE     = 1     #lo dmg dealt per turn to things w/ burning status effect
FIRE_LIGHT      = 12    #how much light is produced by fire?
#FIRE_LEVELMAX     = 3     #max fire level; 0 is no fire, max is blazing flame

# bio (sick)
BIO_METERLOSS   = 1     # sickness points lost per turn
BIO_HURT        = 1     # damage per turn while sick

# chem (exposure)
CHEM_METERLOSS  = 5     # exposure points lost per turn
CHEM_HURT       = 5     # damage chem effect causes when exposure meter fills

# acid
ACID_HURT       = 2

# irritation
IRRIT_ATKMOD    = -10
IRRIT_RANGEMOD  = -10
IRRIT_SIGHTMOD  = -5

# paralysis
PARAL_ROLLSAVE  = 10    #affects chance to undo paralysis

# cough
COUGH_CHANCE    = 33
COUGH_ATKMOD    = -10
COUGH_DFNMOD    = -10

# vomit
VOMIT_CHANCE    = 10

# blind
BLIND_SIGHTMOD = -9999

# deaf
DEAF_HEARINGMOD = -9999

# trauma
#

#electricity
ELEC_PARALYZETIME= 3





#
# Tiles
#

FLOOR           =   249     # centered dot
ROUGH           =   7       # big solid circle
SHRUB           =   5       # club
BRAMBLE         =   6       # spade
JUNGLE          =   13      # musical note (16th note)
JUNGLE2         =   14      # musical note (8th note pair)
WALL            = ord('#')
DOORCLOSED      = ord('+')
DOOROPEN        = ord('-')
VAULTCLOSED     =   241     # +/-
VAULTOPEN       =   240     # =_
STAIRUP         = ord('<')
STAIRDOWN       = ord('>')
##FUNGUS          = ord('\"')
##TREE            =   5       # club #these are things, not tiles...
##SHROOM          =   6       # spade
##PUDDLE          =   7       # circle
##SHALLOW         = ord('_')
##WATER           = ord('~')
##DEEPWATER       =   247     # double ~

#
# Thing types
#

    # ord
T_TRAP          = ord('!')
T_DRUG          = ord('?')  # ("magic scroll") equivalent
T_FUNGUS        = ord('\"')
T_MONEY         = ord('$')
T_CORPSE        = ord('%')
T_FOOD          = ord('&')
T_SHELTER       = ord('^')
T_AMMO          = ord(':')  # bullet / shell / ball / cartridge / arrow
T_LIGHT         = ord(';')  # torch, etc.
T_BOULDER       = ord('0')
T_DUST          = ord('_')
T_FOLIAGE       = ord('+')
T_MELEEWEAPON   = ord('/')
T_TWOHANDWEAP   = ord('\\') # FROM "OFFHANDWEAP"
T_HEAVYWEAPON   = ord('=')
T_TURRET        =   20      # backward |P
T_EXPLOSIVE     = ord('*')
T_BOW           = ord(')')
T_SLING         = ord('(')
T_ARMOR         = ord(']')
T_HELMET        = ord('[')
T_SHIELD        = ord('}')
T_CLOAK         = ord('{')
T_GAS           = ord('~')
    # raw mats
T_RAWMAT        =   172     # 1/4  (raw materials not covered by the following)
T_SCRAP         =   171     # 1/2
T_STICK         = ord('|')  # stick, pole, or pipe
T_SHARD         = ord(",")
T_PARCEL        = ord(".")
T_PIECE         = ord("'")
T_CHUNK         =   7       # crystal
T_SLAB          =   4       # diamond
T_CUBOID        =   22      # horizontal rectangle
T_CUBE          =   219     # large block
    # digits not used elsewhere
T_TREE          =   5       # club
T_SHROOM        =   6       # spade
T_TABLE         =   10      # pi
T_FIREPIT       =   15      # gear-looking thing
T_LOG           =   29      # double arrow facing left and right
T_VORTEX        =   21      # hurricane-looking thing
T_BOX           =   22      # horizontal rectangle
T_SHED          =   127     # house looking thing
T_POT           =   129     # u umlaut
T_STILL         =   150     # u ^
T_CRUCIBLE      =   154     # U umlaut
T_CREDITS       =   155     # cents symbol
T_TERMINAL      =   167     # o underlined
T_DEVICE        =   168     # upside down '?' ("magic wand" equivalent)
T_GUN           =   169     # pistol-looking char
T_ENERGYWEAPON  =   170     # backward pistol-looking char     
##T_SCRAPMETAL    =   171     # 1/2
##T_SCRAPELEC     =   172     # 1/4
T_FLASK         =   173     # upside down '!' ("potion" equivalent)
T_SPOOL         =   237     # circle with line through it
T_FOUNTAIN      =   244     # faucet-looking thing
##T_WOOD          =   246     # div
T_FLUID         =   247     # ~~
T_MISC          =   248     # high circle
T_GRAVE         =   252     # nu
T_TOWEL         =   254     # vertical rectangle

'''
unused chars:
'''

# special chars #

# border 0
# single-line on all sides
CH_VW       = [179, 179, 186] # vertical wall
CH_HW       = [196, 205, 205] # horizontal wall
CH_TLC      = [218, 213, 201] # top-left corner
CH_BLC      = [192, 212, 200] # bottom-left corner
CH_BRC      = [217, 190, 188] # bottom-right corner
CH_TRC      = [191, 184, 187] # top-right corner



#
# equip types
#
i=1;
EQ_MAINHAND =i; i+=1;
EQ_OFFHAND  =i; i+=1;
EQ_BODY     =i; i+=1;
EQ_BACK     =i; i+=1;
EQ_HEAD     =i; i+=1;
EQ_AMMO     =i; i+=1;




#
# genders
#
GENDER_MALE     = 11
GENDER_FEMALE   = 12
GENDER_OTHER    = 255





#
# Elements (types of damage)
#
i=1;
ELEM_PHYS   = i; i+=1;
ELEM_BIO    = i; i+=1;
ELEM_RADS   = i; i+=1;
ELEM_CHEM   = i; i+=1;
ELEM_IRIT   = i; i+=1;  # irritation
ELEM_FIRE   = i; i+=1;
ELEM_COLD   = i; i+=1;
ELEM_ELEC   = i; i+=1;
ELEM_PAIN   = i; i+=1;
ELEM_BLEED  = i; i+=1;
ELEM_RUST   = i; i+=1;
ELEM_ROT    = i; i+=1;
ELEM_WET    = i; i+=1;  # water damage



#
# Alerts
#

ALERT_EMPTYCONTAINER    = "This container is empty."
ALERT_CANTUSE           = "You can't use that!"



#
# Tastes
#
i=1;
TASTE_NASTY = i; i+=1;
TASTE_BITTER = i; i+=1;
TASTE_SWEET = i; i+=1;
TASTE_SALTY = i; i+=1;
TASTE_SAVORY = i; i+=1;

TASTES = {
    TASTE_NASTY : "yuck, disgusting!",
    TASTE_BITTER : "ack, bitter.",
    TASTE_SWEET : "yum, sweet.",
    TASTE_SALTY : "ack, salty.",
    TASTE_SAVORY : "mmm... delicious!",
}




#
# Tools
#
i=1;
TOOL_CUT        =i;i+=1;
TOOL_SHARPENER  =i;i+=1;
TOOL_CHOP       =i;i+=1;
TOOL_HAMMER     =i;i+=1;
TOOL_CHISEL     =i;i+=1;
TOOL_SAW        =i;i+=1;
TOOL_ANVIL      =i;i+=1;
TOOL_WELD       =i;i+=1;
TOOL_CRUCIBLE   =i;i+=1;
TOOL_FURNACE    =i;i+=1;
TOOL_TONGS      =i;i+=1;
TOOL_PLIERS     =i;i+=1;
TOOL_DRILL      =i;i+=1;
TOOL_SEW        =i;i+=1;

TOOL_DECAY_RATE_GLOBAL=10
TOOL_DECAY_RATES={
    # how rapidly tools decay (take damage) when used in crafting.
    #   scale of 0-1 with 1 being fastest, 0 being no damage
    TOOL_CUT        : 1.0,
    TOOL_SHARPENER  : 0.1,
    TOOL_CHOP       : 0.5,
    TOOL_HAMMER     : 0.2,
    TOOL_CHISEL     : 0.8,
    TOOL_SAW        : 1.0,
    TOOL_ANVIL      : 0.1,
    TOOL_WELD       : 0.1,
    TOOL_CRUCIBLE   : 0.1,
    TOOL_FURNACE    : 0.5,
    TOOL_TONGS      : 0.2,
    TOOL_PLIERS     : 0.1,
    TOOL_DRILL      : 1.0,
    TOOL_SEW        : 0.5,
    }





#
# Materials
#
i=1;
MAT_FLESH       = i; i+=1;
MAT_BONE        = i; i+=1;
MAT_METAL       = i; i+=1;
MAT_CARBON      = i; i+=1;
MAT_PLASTIC     = i; i+=1;
MAT_TARP        = i; i+=1;
MAT_STONE       = i; i+=1;
MAT_DUST        = i; i+=1;
MAT_WOOD        = i; i+=1;
MAT_PAPER       = i; i+=1;
MAT_LEATHER     = i; i+=1;
MAT_BLEATHER    = i; i+=1; # boiled leather
MAT_CLOTH       = i; i+=1;
MAT_ROPE        = i; i+=1;
MAT_GLASS       = i; i+=1;
MAT_RUST        = i; i+=1;
MAT_CLAY        = i; i+=1; 
MAT_CERAMIC     = i; i+=1;
MAT_GAS         = i; i+=1;
MAT_WATER       = i; i+=1;
MAT_OIL         = i; i+=1;
MAT_QUARTZ      = i; i+=1;#silica, sand
MAT_RUBBER      = i; i+=1;
##MAT_FUNGUS      = i; i+=1; #use flesh
##MAT_VEGGIE      = i; i+=1; #use wood
##MAT_SAWDUST     = i; i+=1; # just use DUST
##MAT_GUNPOWDER   = i; i+=1;
#
# FLUIDS are mats, too.
#
##i=1;
FL_WATER        =i; i+=1;
FL_OIL          =i; i+=1;
FL_BLOOD        =i; i+=1;
FL_ACID         =i; i+=1;
FL_STRONGACID   =i; i+=1;
FL_SMOKE        =i; i+=1;
FL_ALCOHOL      =i; i+=1;
FL_NAPALM       =i; i+=1;
FL_GASOLINE     =i; i+=1;
FL_HAZMATS      =i; i+=1;

# material fuel values
FUEL_MULT       = 1.00 # global multiplier for all materials
MAT_FUEL={
MAT_FLESH       : 1,
MAT_BONE        : 0,
MAT_METAL       : 0,
MAT_CARBON      : 0,
MAT_PLASTIC     : 2,
MAT_TARP        : 0.5,
MAT_STONE       : 0,
MAT_DUST        : 0.1,
MAT_WOOD        : 2,
MAT_PAPER       : 20,
MAT_LEATHER     : 0.5,
MAT_BLEATHER    : 0.25,
MAT_CLOTH       : 1.5,
MAT_ROPE        : 1.5,
MAT_GLASS       : 0,
MAT_RUST        : 0,
MAT_CLAY        : 0, 
MAT_CERAMIC     : 0,
MAT_GAS         : 0,
MAT_WATER       : 0,
MAT_OIL         : 10,
MAT_QUARTZ      : 0,
MAT_RUBBER      : 0.5,
    }

#quality from material table
MAXGRIND_FROM_MATERIAL={
MAT_CARBON      : MAXGRIND_GRAPHENE,
MAT_METAL       : MAXGRIND_METAL,
MAT_WOOD        : MAXGRIND_WOOD,
MAT_PLASTIC     : MAXGRIND_PLASTIC,
MAT_STONE       : MAXGRIND_STONE,
MAT_BONE        : MAXGRIND_BONE,
MAT_GLASS       : MAXGRIND_GLASS,
MAT_CERAMIC     : MAXGRIND_CERAMIC,
    }






#
# phases of matter
#
i=1;
PHASE_SOLID     =i; i+=1;
PHASE_FLUID     =i; i+=1;   # liquid and gas



#
# Ammo types
#
i=1;
AMMO_BULLETS        = i; i+=1;  # bullets for muskets, etc.
AMMO_CANNONBALLS    = i; i+=1;  # large bullets for cannons, hand cannons, arquebuses
AMMO_SLING          = i; i+=1;  # slings/slingshots - pellets, bullets, stones
AMMO_WARARROWS      = i; i+=1;  # large heavy arrows
AMMO_ARROWS         = i; i+=1;
AMMO_BOLTS          = i; i+=1;  # crossbow bolts
AMMO_DARTS          = i; i+=1;  # blow darts
AMMO_SPEARS         = i; i+=1;
AMMO_AIRGUN         = i; i+=1;  # darts, hollowed arrows, bullets
AMMO_PERCUSSIONCAPS = i; i+=1;
AMMO_PAPERCARTRIDGES= i; i+=1;
AMMO_22LR           = i; i+=1;
AMMO_9MM            = i; i+=1;  # AKA .38 Spl
AMMO_357            = i; i+=1;  # 9mm magnum
AMMO_10MM           = i; i+=1;
AMMO_45ACP          = i; i+=1;
AMMO_44SPL          = i; i+=1;  # .44 is a larger caliber than 10mm (~11mm)
AMMO_44MAG          = i; i+=1;  # .44 magnum is more common than .44 Spl
AMMO_556            = i; i+=1;
AMMO_30CARBINE      = i; i+=1;  # 7.62x33mm
AMMO_762            = i; i+=1;  # 7.62x39mm
AMMO_308            = i; i+=1;  # 7.62x51mm
AMMO_3006           = i; i+=1;  # 7.62x63mm
AMMO_300            = i; i+=1;  # 7.62x67mm (winchester .300 magnum)
AMMO_50BMG          = i; i+=1;
AMMO_12GA           = i; i+=1;
AMMO_10GA           = i; i+=1;
AMMO_8GA            = i; i+=1;
AMMO_6GA            = i; i+=1;
AMMO_4GA            = i; i+=1;
AMMO_3GA            = i; i+=1;
AMMO_2GA            = i; i+=1;
AMMO_ELEC           = i; i+=1;  # electricity
AMMO_OIL            = i; i+=1;
AMMO_HAZMATS        = i; i+=1;
AMMO_ACID           = i; i+=1;
AMMO_CHEMS          = i; i+=1;
AMMO_ROCKETS        = i; i+=1;
AMMO_GRENADES       = i; i+=1;
AMMO_FLUIDS         = i; i+=1;  # any fluids
AMMO_FLAMMABLE      = i; i+=1;  # any flammable fluid
AMMO_ANYTHING       = i; i+=1;  # literally anything



#
# Skills
#
SKILL_EFFECTIVENESS_MULTIPLIER = 0.1 # higher -> skills have more effect
SKILL_MAXIMUM = 100

i=1;
# Melee
SKL_ARMOR       = i; i+=1; #combat skill: armor wearing
SKL_UNARMORED   = i; i+=1; #combat skill: wearing no armor / light armor
SKL_SHIELDS     = i; i+=1; #combat skill: shields
SKL_BOXING      = i; i+=1; #combat skill: fisticuffs
SKL_WRESTLING   = i; i+=1; #combat skill: fight on ground, grappling: knocking down foes, binds, locks, mounting foes, throwing foes, and resisting grappling
SKL_BLUDGEONS   = i; i+=1; #combat skill: bludgeons (clubs, maces, batons, cudgels, spiked clubs, whips)
SKL_JAVELINS    = i; i+=1; #combat skill: 1-h spears (javelins/shortspears)
SKL_SPEARS      = i; i+=1; #combat skill: 2-h spears
SKL_POLEARMS    = i; i+=1; #combat skill: pole weapons other than spears
SKL_KNIVES      = i; i+=1; #combat skill: knives, daggers
SKL_SWORDS      = i; i+=1; #combat skill: swords, machetes
SKL_LONGSWORDS  = i; i+=1; #combat skill: 2-h swords
SKL_GREATSWORDS = i; i+=1; #combat skill: 2-h swords with reach
SKL_AXES        = i; i+=1; #combat skill: 1-h axes
SKL_GREATAXES   = i; i+=1; #combat skill: 2-h axes
SKL_HAMMERS     = i; i+=1; #combat skill: 1-h hammers
SKL_MALLETS     = i; i+=1; #combat skill: 2-h hammers
SKL_STAVES      = i; i+=1; #combat skill: 2-h staves
SKL_BULLWHIPS   = i; i+=1; #combat skill: bullwhips
SKL_PUSHDAGGERS = i; i+=1; #combat skill: push daggers
# throwing
SKL_THROWING    = i; i+=1; #throwing skill (throwing small things not foes)
SKL_PITCHING    = i; i+=1; #throwing skill: tumbling throws (rocks, balls, grenades, etc.)
SKL_ENDOVEREND  = i; i+=1; #throwing skill: end-over-end (axes, knives)
SKL_SPINNING    = i; i+=1; #throwing skill: spinning (boomerangs, frisbees, shurikens, cards)
SKL_TIPFIRST    = i; i+=1; #throwing skill: tip-first (javelins, spears, darts, swords)
# Explosives
SKL_IEDS        = i; i+=1; #explosives skill: IEDs
SKL_EMPS        = i; i+=1; #explosives skill: EMPs
SKL_MINES       = i; i+=1; #explosives skill: Mines
# Archery
SKL_SLINGS      = i; i+=1; #archery skill: slings and slingshots
SKL_BOWS        = i; i+=1; #archery skill: bows
SKL_CROSSBOWS   = i; i+=1; #archery skill: crossbows
# Guns
SKL_CANNONS     = i; i+=1; #guns skill: cannons, hand-cannons, caplock guns
SKL_PISTOLS     = i; i+=1; #guns skill: pistols
SKL_RIFLES      = i; i+=1; #guns skill: rifles and carbines (semi-auto, burst-fire)
SKL_SHOTGUNS    = i; i+=1; #guns skill: shotguns
SKL_SMGS        = i; i+=1; #guns skill: SMGs
SKL_MACHINEGUNS = i; i+=1; #guns skill: machine guns (automatic rifles, etc.)
SKL_HEAVY       = i; i+=1; #guns skill: missiles, chem/bio/flame weapons, launchers
SKL_ENERGY      = i; i+=1; #guns skill: lasers, masers, sonic
# Physical / Technical
SKL_ATHLETE     = i; i+=1; #enables sprinting, jumping, climbing, Msp+ while crouched, prone, supine, on tough terrain (penalty to Msp is reduced, you don't actually GAIN Msp)
SKL_STEALTH     = i; i+=1; #enables sneaking (Msp cut to 50%, make less sound when you move)
SKL_COMPUTERS   = i; i+=1; #technology skill (hacking, programming, etc.)
SKL_PILOT       = i; i+=1; #operating vehicles
SKL_PERSUASION  = i; i+=1; #speech skill, manipulating people
SKL_CHEMISTRY   = i; i+=1; #chemistry
SKL_SURVIVAL    = i; i+=1; #harvesting animals, plants, fungi, rocks, etc.
SKL_LOCKPICK    = i; i+=1; #
SKL_MEDICINE    = i; i+=1; #healing using herbs, bandages, potions, etc. (healing the skin and minor damages)
SKL_SURGERY     = i; i+=1; #stiching, organ/limb removal/transplanting, repairing organs (healing major damages)
##SKL_PERCEPTION  = i; i+=1; #hear exactly what happens, hearing range ++
# Crafting
SKL_ASSEMBLY    = i; i+=1; #crafting base skill
SKL_COOKING     = i; i+=1; #food prep
SKL_WOOD        = i; i+=1; #woodcraft and repairing wooden things
SKL_BONE        = i; i+=1; #bonecraft and repairing bone things
SKL_PLASTIC     = i; i+=1; #plasticraft and repairing plastic things
SKL_STONE       = i; i+=1; #stonecraft and repairing stone things
SKL_GLASS       = i; i+=1; #glasscraft
SKL_METAL       = i; i+=1; #metalcraft and repairing metal things
SKL_CERAMIC     = i; i+=1; #ceramicraft
SKL_LEATHER     = i; i+=1; #leatherworking
SKL_BOWYER      = i; i+=1; #
SKL_FLETCHER    = i; i+=1; #
SKL_BLADESMITH  = i; i+=1; #making and repairing knives
SKL_GUNSMITH    = i; i+=1; #making and repairing guns (child of: metal, wood)
SKL_HARDWARE    = i; i+=1; #computer building and repair
SKL_ARMORSMITH  = i; i+=1; #making and repairing armor
##SKL_SWORDSMITH  = i; i+=1; #making and repairing swords (bladesmithing skill -- incorporated)
# Languages
##SKL_CHINESE     = i; i+=1; #related to: cantonese, tibetan, burmese
##SKL_JAPANESE    = i; i+=1; #
##SKL_HINDUSTANI  = i; i+=1; #related to: bengali, punjabi, marathi, kashmiri, nepali
##SKL_BENGALI     = i; i+=1; #related to: hindustani, punjabi, marathi, kashmiri, nepali
##SKL_ARABIC      = i; i+=1; #related to: Hebrew, Amharic, Aramaic
##SKL_MALAY       = i; i+=1; #related to: Javanese, Tagalog
##SKL_RUSSIAN     = i; i+=1; #related to: Ukrainian, Belarusian
##SKL_ENGLISH     = i; i+=1; #related to: german, dutch, frisian
##SKL_GERMAN      = i; i+=1; #related to: english
##SKL_FRENCH      = i; i+=1; #related to: portuguese, spanish, italian, romanian
##SKL_SPANISH     = i; i+=1; #related to: french, portuguese, italian, romanian
##SKL_PORTUGUESE  = i; i+=1; #related to: french, spanish, italian, romanian

##SKL_STRENGTH    = i; i+=1; #Dmg+2, can overpower similar-sized foes without strength
##SKL_PHYSIQUE    = i; i+=1; #Msp penalty for equipping gear cut in half
##SKL_POISE       = i; i+=1; #Not easily knocked down or moved
##SKL_MOBILITY    = i; i+=1; #Msp+50
##SKL_AGILITY     = i; i+=1; #DV+4, Msp+10, Asp+25
##SKL_DEXTERITY   = i; i+=1; #Atk+4, DV+2, Asp+25
##SKL_DEFENSE     = i; i+=1; #DV+2, AV+2, Pro+2
##SKL_ENDURANCE   = i; i+=1; #Lo+20
##SKL_WILLPOWER   = i; i+=1; #Hi+20

##SKL_MELEE       = i; i+=1; #melee combat root skill
##SKL_THROWING    = i; i+=1; #throwing weapons root skill
##SKL_EXPLOSIVES  = i; i+=1; #explosives root skill
##SKL_ARCHERY     = i; i+=1; #archery root skill - ranged weapons other than guns
##SKL_GUNS        = i; i+=1; #guns umbrella skill


# Combat Skills
##UMBRELLAS_COMBAT={
##SKL_MELEE       :'melee combat',
##SKL_THROWING    :'throwing',
##SKL_EXPLOSIVES  :'explosives',
##SKL_ARCHERY     :'archery',
##SKL_GUNS        :'guns',
##    }



# skill data
SKILLS_COMBAT={ # ID : (SP,name,)
    # SP = skill points required to learn
SKL_ARMOR       :(2,'armored combat',),
SKL_UNARMORED   :(2,'unarmored combat',),
SKL_SHIELDS     :(2,'shields',),
SKL_BOXING      :(3,'boxing',),
SKL_WRESTLING   :(3,'wrestling',),
SKL_AXES        :(2,'1-handed axes',),
SKL_GREATAXES   :(2,'2-handed axes',),
SKL_HAMMERS     :(2,'1-handed hammers',),
SKL_MALLETS     :(2,'2-handed hammers',),
SKL_JAVELINS    :(1,'1-handed spears',),
SKL_SPEARS      :(1,'2-handed spears',),
SKL_SWORDS      :(2,'1-handed swords',),
SKL_LONGSWORDS  :(2,'2-handed swords',),
SKL_POLEARMS    :(2,'polearms',),
SKL_GREATSWORDS :(3,'greatswords',),
SKL_KNIVES      :(3,'knives',),
SKL_BLUDGEONS   :(1,'bludgeons',),
SKL_STAVES      :(1,'staves',),
SKL_BULLWHIPS   :(3,'bullwhips',),
SKL_THROWING    :(1,'throwing',),
SKL_IEDS        :(3,'IEDs',),
SKL_EMPS        :(3,'EMPs',),
SKL_MINES       :(3,'mines',),
SKL_SLINGS      :(3,'slings',),
SKL_BOWS        :(3,'bows',),
SKL_CROSSBOWS   :(1,'crossbows',),
SKL_CANNONS     :(1,'cannons',),
SKL_PISTOLS     :(1,'pistols',),
SKL_RIFLES      :(1,'rifles',),
SKL_SHOTGUNS    :(1,'shotguns',),
SKL_SMGS        :(1,'SMGs',),
SKL_MACHINEGUNS :(1,'machine guns',),
SKL_HEAVY       :(1,'big guns',),
SKL_ENERGY      :(2,'energy weapons',),
##SKL_PITCHING    :(1,'pitching',),
##SKL_ENDOVEREND  :(1,'throwing end-over-end',),
##SKL_SPINNING    :(1,'throwing with the wrist',),
##SKL_TIPFIRST    :(2,'throwing tip-first',),
    }

# Physical / Technical Skills
SKILLS_PHYSTECH={ # ID : (SP,name,)
SKL_ATHLETE     :(2,'athleticism',),
SKL_STEALTH     :(1,'stealth',),
SKL_COMPUTERS   :(2,'computers',),
SKL_PILOT       :(1,'pilot',),
SKL_PERSUASION  :(3,'speech',),
SKL_CHEMISTRY   :(4,'chemistry',),
SKL_SURVIVAL    :(1,'survival',),
SKL_LOCKPICK    :(1,'lockpick',),
SKL_MEDICINE    :(2,'medicine',),
SKL_SURGERY     :(4,'surgery',),
    }

# Crafting Skills
SKILLS_CRAFTING={ # ID : (SP,name,)
SKL_ASSEMBLY    :(1,'crafting',),
SKL_COOKING     :(1,'cooking',),
SKL_WOOD        :(1,'woodworking',),
SKL_BONE        :(2,'boneworking',),
SKL_LEATHER     :(2,'leatherworking',),
SKL_PLASTIC     :(1,'plasticworking',),
SKL_STONE       :(2,'stoneworking',),
SKL_GLASS       :(3,'glassworking',),
SKL_METAL       :(3,'metalworking',),
SKL_BOWYER      :(3,'bowyer',),
SKL_FLETCHER    :(2,'fletcher',),
SKL_BLADESMITH  :(3,'bladesmith',),
SKL_GUNSMITH    :(3,'gunsmith',),
SKL_HARDWARE    :(2,'technosmith',),
SKL_ARMORSMITH  :(3,'armorsmith',),
    }
# WEAPONS
    # these modifiers apply if you wield a weapon in your main hand
    # that you are skilled in
# TODO: update to a linear scaling system
#   *based on a gradient (levels of skill) rather than binary skill
# IDEA: both multiplicative and additive modifiers for skills.
    # add +2 Atk and +2 Dfn, +30Asp at minimum. Dmg, Pen are multipliers
SKILL_WEAPSTATDATA={
SKL_BOXING      : {'atk':6,'dmg':2,'pen':2,'gra':1,'dfn':4,'asp':60,},
SKL_WRESTLING   : {'gra':4,'dfn':4,},
SKL_AXES        : {'atk':4,'dmg':2,'pen':2,'gra':2,'dfn':4,'asp':40,},
SKL_GREATAXES   : {'atk':5,'dmg':4,'pen':2,'gra':2,'dfn':4,'asp':40,},
SKL_HAMMERS     : {'atk':4,'dmg':2,'pen':2,'gra':1,'dfn':4,'asp':40,},
SKL_MALLETS     : {'atk':4,'dmg':4,'pen':2,'gra':1,'dfn':4,'asp':40,},
SKL_JAVELINS    : {'atk':4,'dmg':2,'pen':2,'dfn':4,'asp':40,},
SKL_SPEARS      : {'atk':5,'dmg':4,'pen':2,'dfn':4,'asp':40,},
SKL_SWORDS      : {'atk':4,'dmg':2,'pen':2,'gra':1,'dfn':5,'asp':40,},
SKL_LONGSWORDS  : {'atk':5,'dmg':4,'pen':2,'gra':1,'dfn':5,'asp':40,},
SKL_POLEARMS    : {'atk':5,'dmg':4,'pen':2,'dfn':4,'asp':40,},
SKL_GREATSWORDS : {'atk':5,'dmg':4,'pen':2,'gra':1,'dfn':4,'asp':40,},
SKL_KNIVES      : {'atk':4,'dmg':2,'pen':2,'gra':1,'dfn':4,'asp':50,},
SKL_BLUDGEONS   : {'atk':4,'dmg':2,'pen':2,'gra':1,'dfn':4,'asp':40,},
SKL_STAVES      : {'atk':5,'dmg':4,'pen':2,'gra':1,'dfn':4,'asp':40,},
SKL_BULLWHIPS   : {'atk':4,'dmg':2,'pen':2,'dfn':4,'asp':50,},
SKL_PITCHING    : {},
SKL_ENDOVEREND  : {},
SKL_SPINNING    : {},
SKL_TIPFIRST    : {},
SKL_IEDS        : {},
SKL_EMPS        : {},
SKL_MINES       : {},
SKL_SLINGS      : {},
SKL_BOWS        : {},
SKL_CROSSBOWS   : {},
SKL_PISTOLS     : {},
SKL_RIFLES      : {},
SKL_SHOTGUNS    : {},
SKL_SMGS        : {},
SKL_MACHINEGUNS : {},
SKL_HEAVY       : {},
SKL_ENERGY      : {},
    }
SKILL_RANGEDSTATDATA={
SKL_THROWING    : {'atk':6,'dmg':2,'pen':2,'asp':40,},
SKL_SLINGS      : {'atk':6,'dmg':4,'pen':2,'asp':40,},
SKL_BOWS        : {'atk':6,'dmg':4,'pen':2,'asp':50,},
SKL_CROSSBOWS   : {'atk':6,'pen':2,'asp':50,},
SKL_PISTOLS     : {'atk':6,'pen':2,'asp':50,},
SKL_RIFLES      : {'atk':6,'pen':2,'asp':40,},
SKL_SHOTGUNS    : {'atk':6,'pen':2,'asp':40,},
SKL_SMGS        : {'atk':6,'pen':2,'asp':30,},
SKL_MACHINEGUNS : {'atk':6,'pen':2,'asp':50,},
SKL_HEAVY       : {'atk':6,'pen':2,'asp':60,},
SKL_ENERGY      : {'atk':6,'pen':2,'asp':60,},
    }

# weapons
WEAPONCLASS_CRITDAMAGE={ # damage % of target's total health on critical hit
SKL_SWORDS          : 0.4,
SKL_LONGSWORDS      : 0.3333334,
SKL_GREATSWORDS     : 0.25,
SKL_POLEARMS        : 0.25,
SKL_KNIVES          : 0.5,
SKL_HAMMERS         : 0.25,
SKL_MALLETS         : 0.25,
SKL_AXES            : 0.3333334,
SKL_GREATAXES       : 0.3333334,
SKL_JAVELINS        : 0.3333334,
SKL_SPEARS          : 0.3333334,
SKL_BLUDGEONS       : 0.25,
SKL_SHIELDS         : 0.2,
SKL_BULLWHIPS       : 0.2,
SKL_BOXING          : 0.25,
    }

# Skill data (stat modifiers gained from skills)
# ARMOR
SKLMOD_ARMOR_PRO        = 1.2       # multiplier modifier
SKLMOD_ARMOR_AV         = 1.25      # multiplier modifier
SKLMOD_ARMOR_DV         = 1.4       # multiplier modifier
SKLMOD_UNARMORED_ATK    = 5         # adder modifier
SKLMOD_UNARMORED_PRO    = 2         # adder modifier
SKLMOD_UNARMORED_AV     = 2         # adder modifier
SKLMOD_UNARMORED_DV     = 5         # adder modifier



#
# Classes
#
# includes all jobs, even non-playable jobs
i=1;
CLS_ENGINEER    = i; i+=1;
CLS_TECHNICIAN  = i; i+=1;
CLS_SECURITY    = i; i+=1;
CLS_ATHLETE     = i; i+=1;
CLS_PILOT       = i; i+=1;
CLS_SMUGGLER    = i; i+=1;
CLS_CHEMIST     = i; i+=1;
CLS_POLITICIAN  = i; i+=1;
CLS_RIOTPOLICE  = i; i+=1;
CLS_JANITOR     = i; i+=1;
CLS_DEPRIVED    = i; i+=1;
CLS_SOLDIER     = i; i+=1;
CLS_THIEF       = i; i+=1;
CLS_ACROBAT     = i; i+=1;
CLS_WRESTLER    = i; i+=1;



#
# Factions
# flags used for diplomacy
#
i=1;
FACT_ROGUE      = i; i+=1;
FACT_CITIZENS   = i; i+=1;
FACT_DEPRIVED   = i; i+=1;
FACT_ELITE      = i; i+=1;
FACT_WATCH      = i; i+=1;
FACT_MONSTERS   = i; i+=1;
#FACT_      = i; i+=1;





#
# Sounds
#

NOISE_SOME      = "something"
NOISE_WHISPER   = "someone whisper"
NOISE_SQUEAK    = "a squeak"
NOISE_RACKET    = "a violent racket"
NOISE_POP       = "popping noises"
NOISE_BANG      = "an explosion"
NOISE_DING      = "a high-pitched ringing sound"
NOISE_SCREECH   = "someone screeching"
NOISE_WATERFALL = "water falling"
NOISE_CLATTER   = "the kind of clattering that elicits concern"

                # vol, superHearing, generic sound
SND_FIRE        = (40, "a fire",    NOISE_POP,)
SND_FIGHT       = (100,"a struggle",NOISE_RACKET,)
SND_DOUSE       = (30, "a fire going out",NOISE_WHISPER,)
SND_QUAFF       = (20, "gulping noises",NOISE_SOME,)
SND_COUGH       = (80, "someone coughing",NOISE_SCREECH,)
SND_VOMIT       = (80, "someone vomiting",NOISE_WATERFALL,)
SND_GUNSHOT     = (450,"a gunshot",NOISE_BANG,)


##class Struct_Sound():
##    def __init__(self):
##        self.textSee=textSee
##        self.textHear=textHear


###
### Things, specific
###
##
##class THG:#(Flag)
##    i=1;
##    GORE                = i; i+=1;
##    GUNPOWDER           = i; i+=1;
##    PEBBLE              = i; i+=1;
##    SAND                = i; i+=1;
##    JUG                 = i; i+=1;
##    CORPSE_SHROOM       = i; i+=1;
##    TREE                = i; i+=1;
##    LOG                 = i; i+=1;
##    WOOD                = i; i+=1;
##    SAWDUST             = i; i+=1;
##    DUST                = i; i+=1;
##    GRAVE               = i; i+=1;
##    SAFE                = i; i+=1;
##    BOX                 = i; i+=1;
##    POT                 = i; i+=1;
##    CASTIRONPAN         = i; i+=1;
##    STILL               = i; i+=1;
##    DOSIMETER           = i; i+=1;
##    TOWEL               = i; i+=1;
##    TOOTHBRUSH          = i; i+=1;
##    FACEFLANNEL         = i; i+=1;
##    SOAP                = i; i+=1;
##    TINOFBISCUITS       = i; i+=1;
##    FLASK               = i; i+=1;
##    COMPASS             = i; i+=1;
##    MAP                 = i; i+=1;
##    BALLOFSTRING        = i; i+=1;
##    GNATSPRAY           = i; i+=1;
##    TORCH               = i; i+=1;
##    BARREL              = i; i+=1;
##    METALDRUM           = i; i+=1;
##    TABLE               = i; i+=1;
##    TERMINAL            = i; i+=1;
##    COPPERTUBING        = i; i+=1;
##    COPPERWIRE          = i; i+=1;
##    SCRAPMETAL          = i; i+=1;
##    SCRAPELECTRONICS    = i; i+=1;
##    SPRING              = i; i+=1;
##    CHAINGUN            = i; i+=1;
##    LIGHTER             = i; i+=1;
##    CLAYPOT             = i; i+=1;
##    EXTINGUISHER        = i; i+=1;
##




'''
#
# gear qualities
#
i=1;
QU_LOW          =i; i+=1;
QU_MEDLOW       =i; i+=1;
QU_MED          =i; i+=1;
QU_MEDHIGH      =i; i+=1;
QU_HIGH         =i; i+=1;

QUALITIES={
    # %%    stats modifier (multiplier)
    # $$    value modifier (multiplier)
# ID            :   name        Color,      %%,  $$,
QU_LOW          : ("crude",     "neutral",  0.5, 0.1,), #(-33,-50,-40,-66,-333,42,),),
QU_MEDLOW       : ("improvised","ltgray",   0.75,0.33,),    #(-16,-25,-20,-33,-150,25,),),
QU_MED          : ("",          "accent",   1.0, 1.0),   #(0,  0,  0,  0,  0,  0,),),
QU_MEDHIGH      : ("military",  "trueblue", 1.25,3.0),  #(16, 25, 20, 25, 150,-16,),),
QU_HIGH         : ("pre-war",  "truepurple",1.5, 10.0), #(33, 50, 50, 50, 333,33,),),
##QU_LEGENDARY    : ("legendary","trueyellow",2.0, 100.0), #(33, 50, 50, 50, 333,33,),),
    }
QUALITIES_STATS={
    cmp.Stats : {"range":16,"atk":25,"dfn":20,},
    cmp.Form : {"value":150,"mass":16,},
    }
'''













