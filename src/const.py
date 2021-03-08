'''
    const.py
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


##from enum import Flag, auto

import tcod as libtcod



# private, only for use inside this script
#   (vars beginning w/ "_" will not be imported with "from const import *"

# fractions (_1_8 == 1/8)
_1_8    = 0.125
_1_16   = 0.0625
_1_32   = 0.03125
_1_64   = 0.015625
_1_128  = 0.0078125
_1_256  = 0.00390625
_1_512  = 0.001953125
_1_1024 = 0.0009765625



# public


    # entities
i=1;
ENT_STONE_WALL      =i;i+=1;



    #--------------#
    # #Exceptions  #
    #--------------#

class Error_wrongNumberCommandsLoaded(Exception):
#tried to load key commands from key_bindings
#but received the wrong number of commands.
    pass

UNID="<?>" #"<unID'd>" #"<unidentified>"

    #------------#
    # #History   #
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
    ##Init Global Constants #
    #-----------------------#

GAME_TITLE = "Softly Into the Night"

TILES_PER_ROW = 16          # Num tiles per row (size of the char sheet 
TILES_PER_COL = 16          # " per column         used for ASCII display)

MENU_CTRL_MOD       = 256


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


STATS={
# in-code name : in-game name
'str' : 'STR', #,'strength'),
'con' : 'CON',
'int' : 'INT',
'agi' : 'AGI',
'dex' : 'DEX',
'end' : 'END',
'resfire' : 'FIR',
'rescold' : 'ICE',
'resbio' : 'BIO',
'reselec' : 'ELC',
'resphys' : 'PHS',
'respain' : 'PAI',
'resrust' : 'RUS',
'resrot' : 'ROT',
'reswet' : 'WET',
'resbleed' : 'BLD',
'reslight' : 'LGT',
'ressound' : 'SND',
'mass' : 'KG',
'hpmax' : 'HPMAX',
'hp' : 'HP',
'mpmax' : 'SPMAX',
'mp' : 'SP',
'mpregen' : 'SPR',
'encmax' : 'ENCMAX',
'enc' : 'ENC',
'atk' : 'ATK',
'dmg' : 'DMG',
'pen' : 'PEN',
'dfn' : 'DV',
'arm' : 'AV',
'pro' : 'PRO',
'spd' : 'SPD',
'asp' : 'ASP',
'msp' : 'MSP',
'rasp' : 'RASP',
'ratk' : 'RATK',
'rpen' : 'RPEN',
'rdmg' : 'RDMG',
'minrng' : 'MINRNG',
'maxrng' : 'MAXRNG',
'trng' : 'TRNG',
'gra' : 'GRA',
'ctr' : 'CTR',
'bal' : 'BAL',
'sight' : 'VIS',
'hearing' : 'AUD',
'cou' : 'COU',
'idn' : 'IDN',
'bea' : 'BEA',
}

STATS_TO_MULT={
'str' : 'STR', #,'strength'),
'con' : 'CON',
'int' : 'INT',
'agi' : 'AGI',
'dex' : 'DEX',
'end' : 'END',
'atk' : 'ATK',
'dmg' : 'DMG',
'pen' : 'PEN',
'dfn' : 'DV',
'arm' : 'AV',
'pro' : 'PRO',
'gra' : 'GRA',
'ctr' : 'CTR',
'bal' : 'BAL',
'ratk' : 'RATK',
'rpen' : 'RPEN',
'rdmg' : 'RDMG',
}


# titles
i=0;
TITLE_NONE          =i;i+=1;
TITLE_A             =i;i+=1;
TITLE_AN            =i;i+=1;
TITLE_THE           =i;i+=1;
TITLE_MR            =i;i+=1;
TITLE_MRS           =i;i+=1;
TITLE_MS            =i;i+=1;
TITLE_SIR           =i;i+=1;
TITLE_THEHONORABLE  =i;i+=1;
TITLE_LORD          =i;i+=1;
TITLE_LADY          =i;i+=1;
TITLE_DR            =i;i+=1;
TITLES={
TITLE_NONE          : "",
TITLE_A             : "a ",
TITLE_AN            : "an ",
TITLE_THE           : "the ",
TITLE_MR            : "Mr. ",
TITLE_MRS           : "Mrs. ",
TITLE_MS            : "Ms. ",
TITLE_SIR           : "Sir ",
TITLE_THEHONORABLE  : "the Honorable ",
TITLE_LORD          : "Lord ",
TITLE_LADY          : "Lady ",
TITLE_DR            : "Dr. ",
}


# death types (sent to DeathFunction component to tell it how the thing died)
i=1;
DEATH_SHATTERED     =i;i+=1;
DEATH_STABBED       =i;i+=1;
DEATH_CUT           =i;i+=1;
DEATH_CRUSHED       =i;i+=1;
DEATH_MELTED        =i;i+=1;
DEATH_BURNED        =i;i+=1;
DEATH_RUSTED        =i;i+=1;
DEATH_ELECTROCUTED  =i;i+=1;




    #----------------#
    #   #Crafting    #
    #----------------#

SKILL_CRAFTING_ROLL = 1 # how much does skill level affect crafting ability?
RECIPE_SOUND_MULTIPLIER=10 # global modifier for sound level of crafting recipes

i=1;
CRAFTJOB_HACK       =i;i+=1;
CRAFTJOB_QUICK      =i;i+=1;
CRAFTJOB_NORMAL     =i;i+=1;
CRAFTJOB_DETAILED   =i;i+=1;
CRAFTJOB_FINE       =i;i+=1;
CRAFTJOB_METICULOUS =i;i+=1;
CRAFTJOB_THESIS     =i;i+=1;

CRAFTJOBS={
# ID : (name (+" job"), to roll,)
    # multipliers: fail: chance to fail. Crude: chance to make crude item. Quality: chance to make quality item. Masterpiece: chance to make masterpiece item.
CRAFTJOB_HACK       : ("hack",      -24,),
CRAFTJOB_QUICK      : ("quick",     -12,),
CRAFTJOB_NORMAL     : ("normal",    0,),
CRAFTJOB_DETAILED   : ("detailed",  8,),
CRAFTJOB_FINE       : ("fine",      16,),
CRAFTJOB_METICULOUS : ("meticulous",24,),
CRAFTJOB_THESIS     : ("thesis",    32,),
}

# Crafting Recipe Categories
i=1;
CRC_PLASTIC         =i;i+=1; # plasticraft (whittling, chiseling)
CRC_WOOD            =i;i+=1; # woodcraft (whittling, chiseling)
CRC_BONE            =i;i+=1; # bonecraft (whittling, chiseling)
CRC_STONE           =i;i+=1; # stonecraft (chiseling)
CRC_METAL           =i;i+=1; # metalcraft (forging)
CRC_GLASS           =i;i+=1; # glasscraft (chiseling)
CRC_GLASSBLOWING    =i;i+=1; # glass blowing, separate skill from glass chiseling
CRC_CLAY            =i;i+=1; # potter
CRC_LEATHER         =i;i+=1; # tanner
CRC_BOILEDLEATHER   =i;i+=1; # boiled leathercraft
CRC_RUBBER          =i;i+=1; # Joergcraft
CRC_CLOTH           =i;i+=1; # tailor
CRC_FLESH           =i;i+=1; # fleshcraft
CRC_ARMOR           =i;i+=1; # armor making
CRC_ASSEMBLY        =i;i+=1; # basic putting stuff together skills
CRC_SURVIVAL        =i;i+=1; # living off the land
CRC_SWORDS          =i;i+=1; # swordsmithing (parents: metalcraft)
CRC_GUNS            =i;i+=1; # gunsmithing (parents: wood, metalcraft)
CRC_BOWS            =i;i+=1; # 
CRC_ARROWS          =i;i+=1; # 
CRC_CARTRIDGES      =i;i+=1; # 



#
# Crafting Recipe Types (which table to access)
#
i=1;
CRT_WEAPONS         =i;i+=1;
CRT_ARMOR           =i;i+=1;
CRT_HEADWEAR        =i;i+=1;
CRT_LEGWEAR         =i;i+=1;
CRT_ARMWEAR         =i;i+=1;
CRT_FOOTWEAR        =i;i+=1;
CRT_HANDWEAR        =i;i+=1;
CRT_FACEWEAR        =i;i+=1;
CRT_EYEWEAR         =i;i+=1;
CRT_EARWEAR         =i;i+=1;
CRT_ABOUTWEAR       =i;i+=1;
CRT_TOOLS           =i;i+=1;
CRT_FOOD            =i;i+=1;
CRT_STUFF           =i;i+=1;
CRT_RAWMATS         =i;i+=1;



#
# Flags
#

# Monster and item flags

i = 1
RAVAGED     =i;i+=1;  # Creature is starved: strong desire for food
THIEF       =i;i+=1;  # Creature desires gold / treasure and will steal it
MEAN        =i;i+=1;  # Creature is always hostile to rogues
DEAD        =i;i+=1;  # Is dead
FLYING      =i;i+=1;  # Is currently flying
NVISION     =i;i+=1;  # Has Night vision
INVIS       =i;i+=1;  # Is invisible
SEEINV      =i;i+=1;  # Can see invisible things
SEEXRAY     =i;i+=1;  # LOS not blocked by walls
TWOHANDS    =i;i+=1;  # 2-handed only (when wielded in hands)
ISSOLID     =i;i+=1;  # Is solid (cannot walk through it)
CANCOUNTER  =i;i+=1;  # Is able to counter-attack this turn
IMMUNEBIO   =i;i+=1;  # Immune to bio / chems / radiation damage
IMMUNERUST  =i;i+=1;  # Immune to rusting
IMMUNEROT   =i;i+=1;  # Immune to rotting
IMMUNEWATER =i;i+=1;  # Immune to getting wet
IMMUNEBLEED =i;i+=1;  # Immune to bleeding
IMMUNEPAIN  =i;i+=1;  # Immune to pain
IMMUNEFEAR  =i;i+=1;  # Immune to fear / intimidation
DIRTY_STATS =i;i+=1;  # private -- indicates entity's stats (may) have changed


#
# FOV maps | FOVmaps
#
i=1;
FOVMAP_NORMAL       =i;i+=1;


# $$ values of things not given values elsewhere
VAL_HUMAN           = 5000

#combat system
CMB_ROLL_PEN        = 6     # dice roll for penetration bonus
CMB_ROLL_ATK        = 20    # dice roll for to-hit bonus (Attack)
CMB_MDMGMIN         = 0.6   # multplier for damage (minimum)
CMB_MDMG            = 0.4   # multplier for damage (diff. btn min/max)
MISS_BAL_PENALTY    = 5     # balance penalty for attacking nothing
BAL_MASS_MULT       = 20    # X where effective mass == mass*bal/X (for purposes of getting knocked off-balance)
MAXREACH            = 6     # meters
BODY_DMG_PEN_BPS    = 6     # number of penetration breakpoints for body status inflicting
GEAR_DMG_PEN_THRESHOLD = 4  # number of penetrations before attacks do not damage gear, but only damage the body wearing it
CHANCE_HURT_SELF    = 0.01  # decimal chance to hurt self with weapon when unskilled
SKILL_HURT_SELF     = 0.02  # decrease chance to hurt self when skilled (each skill level decreases chance by this ratio)
SKILL_JAM_FIX_AP    = -1    # weapon jams can be more rapidly fixed when skilled in the weapon

#sounds
VOLUME_DEAFEN       = 500




    #------------------------#
    #  #Gameplay Constants   #
    #------------------------#

ROOMW       = 160       # max dungeon level size, width
ROOMH       = 100       # ", height
MAXLEVEL    = 20        # deepest dungeon level
STARTING_TIME = 25200   # turns elapsed at start of game (beginning time of day)
CRAFT_CONSTRUCT_MULTIPLIER = 2  # construction time multiplier for all crafting recipes

MAX_SKILL           = 100   # max skill level maximum skill lvl maxskilllvl skillmax skill_max
CM_ADVANTAGE_BP     = 8     # how much extra height you need to gain +1 advantage in combat
HEIGHTMAP_GRADIENT  = 0.1   # ratio of height value on heightmap to the width/height of a tile
CM_PER_TILE         = 100   # tiles are exactly 1x1m

RNG_ATK_PENALTY = 1     # Atk penalty per tile of distance

# global multipliers
# the displayed integer value in-game and in the code is the same
#   but in-engine, the actual value is always an integer.
MULT_VALUE          = 12    # 12 pence == 1 pound. multiplier for value of all things
MULT_MASS           = 100000  # @1000, smallest mass unit == 1 gram. @100000, 1/100 gram. multiplier for mass of all things (to make it stored as an integer by Python)
MULT_STATS          = 10    # finer scale for Atk/DV/AV/dmg/pen/pro/Gra/Ctr/Bal but only each 10 makes any difference. Shows up /10 without the decimal in-game and functions the same way by the mechanics.
MULT_ATT            = MULT_STATS    # finer scale for Attributes but only each 10 (assuming the value is 10) makes any difference. Shows up /10 without the decimal in-game and functions the same way by the mechanics.
MULT_HYD            = 1000  # finer scale for hydration control
MIN_MSP             = 5     # minimum movement speed under normal conditions

MULTSTATS=(
    'atk','dfn','pen','pro','arm','dmg','gra','bal','ctr','str','con','int','agi','dex','end',
    )
##__MULTATT=('str','con','int','agi','dex','end',)

# fire / ice
FIRE_THRESHOLD  = 800 # average combustion temperature (ignition temperature)
ENV_DELTA_HEAT  = -0.1 # global change in heat each iteration of heat dispersion
HEATMIN         = -300 # minimum temperature
HEATMAX         = 16000 # maximum temperature
FREEZE_THRESHOLD= -30
FREEZE_DMG_PC   = 0.17  # damage dealt when you become frozen (% of max lo)

#fluids
MAX_FLUID_IN_TILE   = 1000 * MULT_MASS

# combat

BP_DAMAGE_MULTIPLIER = 1 # global multiplier for damage dealt to body parts
SKILL_LV_WOUND_MODIFIER = 0.05 # higher -> the more combat levels affect wounding quality

#misc
DURMOD_ASP = -50




    #---------------#
    #  #equipment   #
    #---------------#

FITTED_ENCMOD = 1 # multiplier
FIT_HELD_MAX = 15   # maximum fit value for weapons fitted to your character
FIT_ARMOR_MAX = 30  # maximum fit value for armor fitted to your character

# 1-h / 2-h constants

# insufficient strength penalties
INSUFF_STR_PEN_PENALTY  = 1 # each is a penalty PER Str point missing
INSUFF_STR_DMG_PENALTY  = 1
INSUFF_STR_ATK_PENALTY  = 3
INSUFF_STR_DFN_PENALTY  = 1.5
INSUFF_STR_PRO_PENALTY  = 1
INSUFF_STR_ARM_PENALTY  = 0.5
INSUFF_STR_GRA_PENALTY  = 2
INSUFF_STR_ASP_PENALTY  = 18
INSUFF_STR_RNG_PENALTY  = 0.1 # ratio penalty for throwing range
# insufficient dexterity penalties
INSUFF_DEX_PEN_PENALTY  = 2 # each is a penalty PER Dex point missing
INSUFF_DEX_ATK_PENALTY  = 4
INSUFF_DEX_DFN_PENALTY  = 1.25
INSUFF_DEX_GRA_PENALTY  = 1.5
INSUFF_DEX_ASP_PENALTY  = 12
INSUFF_DEX_DMG_PENALTY  = 2
INSUFF_DEX_RNG_PENALTY  = 0.2 # ratio penalty for throwing range
#TODO: insufficient penalties for ranged stats!!!

# attribute bonuses and multipliers
MULT_1HANDBONUS_STR_DMG = 0.5     # strength bonus for 1-h wielding per STR
MULT_1HANDBONUS_STR_PEN = 0.25    # strength bonus for 1-h wielding per STR
MULT_2HANDBONUS_STR_DMG = 0.75    # strength bonus for 2-h wielding per STR
MULT_2HANDBONUS_STR_PEN = 0.5     # strength bonus for 2-h wielding per STR
# penalty to offhand weapons wielded (other than weapons designed for offhand)
OFFHAND_PENALTY_DFNMOD  = 0.5   # multiplier
OFFHAND_PENALTY_ARMMOD  = 0.5   # multiplier
OFFHAND_PENALTY_PROMOD  = 0.5   # multiplier
OFFHAND_PENALTY_GRA     = -2    # adder
# bonuses for when you fight with a 1-handed weapon in 2 hands
MULT_2HANDBONUS_STRREQ  = 0.8    # strength required multiplier
MULT_2HANDPENALTY_REACH = 0.75  # reach is reduced w/ 2 hands
MULT_2HANDBONUS_ASP     = 1.3333334 # attack speed multiplier modifier
MULT_2HANDBONUS_STAMINA = 0.8   # stamina cost multiplier
MULT_2HANDBONUS_DMG     = 1.2     # damage multiplier (IDEA: DO STRENGTH BONUS INSTEAD -- this may be too complex)
MOD_2HANDBONUS_ATK    = 4       # attack you gain
MOD_2HANDBONUS_PEN    = 2       # penetration you gain
MOD_2HANDBONUS_DFN    = 2       # defense you gain
MOD_2HANDBONUS_ARM    = 1       # armor you gain
MOD_2HANDBONUS_PRO    = 1       # protection you gain
# penalties for when you fight with a 2-handed weapon in 1 hand
MULT_1HANDPENALTY_STRREQ = 1.5  # strength required multiplier
MULT_1HANDBONUS_REACH = 1.25 # reach is increased w/ one hand
MOD_1HANDPENALTY_ASP  = -75     # attack speed you lose
MOD_1HANDPENALTY_ATK  = -10     # attack you lose
MOD_1HANDPENALTY_PEN  = -6      # penetration you lose
MOD_1HANDPENALTY_DFN  = -5      # defense you lose
MOD_1HANDPENALTY_ARM  = -2      # armor you lose
MOD_1HANDPENALTY_PRO  = -2      # protection you lose


# maximum + quality upgrade
MAXGRIND_GRAPHENE   = 1
MAXGRIND_CLOTH      = 2
MAXGRIND_GLASS      = 2
MAXGRIND_CERAMIC    = 2
MAXGRIND_PLASTIC    = 3
MAXGRIND_WOOD       = 4
MAXGRIND_BONE       = 4
MAXGRIND_STONE      = 4
MAXGRIND_METAL      = 5





    #---------------#
    #    #Stats     #
    #---------------#

    # base stats for typical creature
BASE_HP         = 2
BASE_MP         = 40
BASE_MPREGEN    = 1
BASE_ENCMAX     = 60
BASE_REACH      = 2
BASE_STR        = 12 # strength
BASE_CON        = 12 # constitution
BASE_INT        = 12 # intelligence
BASE_DEX        = 12 # dexterity
BASE_AGI        = 12 # agility
BASE_END        = 12 # endurance
BASE_VIT        = 12 # vitality
BASE_LUCK       = 100
BASE_ATK        = 0
BASE_DMG        = 1
BASE_PEN        = 0
BASE_DFN        = 10
BASE_ARM        = 0
BASE_PRO        = 6
BASE_SPD        = 100
BASE_MSP        = 100
BASE_ASP        = 40
BASE_BAL        = 2
BASE_GRA        = 0
BASE_CTR        = 0
BASE_SIGHT      = 20
BASE_HEARING    = 80
BASE_SMELLING   = 5
BASE_COURAGE    = 64
BASE_SCARY      = 32
BASE_BEAUTY     = 16
BASE_RESFIRE    = 20
BASE_RESCOLD    = 20
BASE_RESBIO     = 20
BASE_RESPHYS    = 20
BASE_RESELEC    = 20
BASE_RESPAIN    = 20
BASE_RESBLEED   = 20
BASE_RESRUST    = 0
BASE_RESROT     = 0
BASE_RESWET     = 20
BASE_RESLIGHT   = 0
BASE_RESSOUND   = 0
# player bonuses
PLAYER_COURAGE  = 64    # a hero must be exceptionally courageous

# Female / male gender stat differences
# IDEA: instead of this, allow stat buffs during chargen
FEM_BEA = 16
MAS_IDN = 8
MAS_COU = 8

#TODO: attribute selection in chargen
##STATS_CHARGEN={ # select 1 stat to buff by x points
###stat   : x,
##'hpmax' : 6,
##'cou'   : 16,
##'idn'   : 16,
##'bea'   : 16,
##}

# other stat consts
SPREGEN_MIN = 0.25
SPREGEN_D   = 1.75
MASS_GRIP   = 0.1       # bonus feet grip gained from mass

# attributes

# Strength
ATT_STR_TRNG            = 0.5 # throwing range bonus
ATT_STR_DMG             = 0.3333334 # melee/thrown damage
ATT_STR_ATK             = 0.15 # melee/thrown accuracy -- less than Dex bonus
ATT_STR_PEN             = 0.2 # melee/thrown penetration -- less than Dex bonus
ATT_STR_AV              = 0.15 # armor from strength -- less than Con bonus
ATT_STR_ENCMAX          = 2.5 # strength gives some carrying capacity -- less than Con bonus
ATT_STR_GRA             = 1 # grappling / wrestling, grip, climbing
ATT_STR_SCARY           = 1 # intimidation +
ATT_STR_FORCEMULT       = 0.0833334 # ratio extra force for every strength point
ATT_STR_GRIP            = 0.3333334 # hand grip +

# Agility
ATT_AGI_DV              = 0.5 # dodge value
ATT_AGI_PRO             = 0.25 # protection
ATT_AGI_BAL             = 1 # balance / poise
ATT_AGI_MSP             = 2 # movement speed +
ATT_AGI_ASP             = 5 # melee attack speed
ATT_AGI_GRIP            = 0.25 # feet grip +

# Dexterity
ATT_DEX_ATK             = 0.5 # melee accuracy
ATT_DEX_RATK            = 0.75 # ranged Accuracy bonus
ATT_DEX_PEN             = 0.3333334 # melee penetration
ATT_DEX_RPEN            = 0.3333334 # ranged Penetration bonus
ATT_DEX_ASP             = 3 # speed bonus for all tasks using hands -- attacking, crafting, reloading, throwing, etc. NOT a bonus to "speed" attribute itself, but applied across various domains.
ATT_DEX_RASP            = 3 # speed bonus for ranged attacks
ATT_DEX_RNG             = 1 # range of bows and guns
ATT_DEX_TRNG            = 0.25 # throwing range bonus -- less than Str bonus
ATT_DEX_GRIP            = 0.1666667 # hand grip +

# Endurance
ATT_END_HP              = 0.5   # life -- less than Con bonus
ATT_END_SP              = 15    # stamina
ATT_END_SPREGEN         = 1     # stamina regen
ATT_END_RESHEAT         = 2     # endurance grants many resistances
ATT_END_RESCOLD         = 2
ATT_END_RESPHYS         = 1
ATT_END_RESPAIN         = 3     # res pain -- significantly more than Con bonus
ATT_END_RESBIO          = 1     # res bio -- less than Con bonus
ATT_END_RESBLEED        = 1

# Intelligence
ATT_INT_AUGS            = 0.25 # mental augmentations
ATT_INT_PERSUASION      = 0.5 # charisma is not an attribute so it's shared w/ int
ATT_INT_IDENTIFY        = 1 # identify ability
ATT_INT_EXPBONUS        = 0.08333   # % bonus EXP for skills per INT point

# Constitution
ATT_CON_AUGS            = 0.25 # physical augmentations
ATT_CON_AV              = 0.2   # armor value
ATT_CON_HP              = 1.5   # life
ATT_CON_ENCMAX          = 5     # encumberance maximum -- more than Str bonus
ATT_CON_RESELEC         = 2     # constitution grants some resistances
ATT_CON_RESBIO          = 2 
ATT_CON_RESBLEED        = 2
ATT_CON_RESPAIN         = 1
ATT_CON_COURAGE         = 1

ATTRIBUTES={
'str': '''
Strength improves melee combat effectiveness, raising damage, attack,
penetration, armor, grappling, and force of attacks. It also improves
throwing range and effectiveness, and adds some carry capacity. Finally,
it also grants some additional intimidation value. All equipment types
require some amount of strength to effectively equip.''',
'agi': '''
Agility improves speed of movement and melee attacks, and grants extra
dodge value, protection, and balance.''',
'dex': '''
Dexterity enhances both melee and ranged combat effectiveness, increasing
penetration, accuracy, and attack speed. It also increases maximum range
of ranged and throwing weapons. A certain amount of dexterity is required
to equip specific types of weapons.''',
'end': '''
Endurance increases SP and SP regeneration rate. It also grants some HP
and improves various resistances.''',
'con': '''
Constitution determines the maximum number of physical augmentations.
It also greatly improves maximum HP, armor value, and carrying
capacity, and grants some resistances.
''',
'int': '''
Intelligence determines the maximum number of mental augmentations.
In addition, it enhances identify and persuasion.''',
}


# body augmentations #
PAUG_LIMITBREAKER_STR   =i;i+=1;
PAUG_KERATINIZEDSKIN    =i;i+=1; # exoskeleton made of keratin
PAUG_GILLS              =i;i+=1; # can breathe underwater
PAUG_CLAWS              =i;i+=1; # hands use claw limb-weapon
PAUG_              =i;i+=1;

AUGS_PHYS = {
PAUG_LIMITBREAKER_STR   : {'str':5,},
PAUG_KERATINIZEDSKIN    : {'arm':2,'pro':2,'bea':-16,},
PAUG_GILLS              : {},
PAUG_CLAWS              : {'dex':-4,}, # keratin claws
}

#    -------------   Information on Body augs:   ----------------   #
# Strength Limit Breaker:
#   * Removes the natural limitations placed on one's muscles
#       in order to unlock supernatural strength. However, this
#       leaves one's muscles highly prone to damage.
#   Str +5
#   Muscles 10x more prone to tearing
#   Muscles fatigue at 2x the normal rate
    
#

# fatigue (low stamina) penalties
    # these values represent the penalty for having 0 stamina
    #   -- any value above 0 SP results in a lesser penalty
FATIGUE_PENALTY_DFN  = 12
FATIGUE_PENALTY_CTR  = 10
FATIGUE_PENALTY_BAL  = 10
FATIGUE_PENALTY_GRA  = 20
FATIGUE_PENALTY_PRO  = 12
FATIGUE_PENALTY_PEN  = 12
FATIGUE_PENALTY_TPEN = 12
FATIGUE_PENALTY_RPEN = 12
FATIGUE_PENALTY_ATK  = 12
FATIGUE_PENALTY_TATK = 15
FATIGUE_PENALTY_RATK = 20
FATIGUE_PENALTY_MSP  = 20
FATIGUE_PENALTY_ASP  = 30
FATIGUE_PENALTY_TASP = 40
FATIGUE_PENALTY_RASP = 50

# minimum stats
MIN_SPD     = 10
MIN_ASP     = 5
MIN_MSP     = 1

##SUPER_HEARING       = 500
AVG_HEARING         = 100
AVG_SPD             = 100
AVG_HUMAN_HEIGHT    = 175 #CM
AVG_MASS            = 75  #KG
##AVG_HUMAN_MASS      = 75



# ENCUMBERANCE

ENC_BP_1    = 0.35
ENC_BP_2    = 0.50
ENC_BP_3    = 0.70
ENC_BP_4    = 0.85
ENC_BP_5    = 0.90
ENC_BP_6    = 0.95
ENCUMBERANCE_MODIFIERS = {
# note: encumberance affecting attributes (like Agi) is difficult to
#   implement and is a recipe for disaster... so it only affects
#   derived stats here.
#stat : Encumberance Breakpoint
# BP:   1     2     3     4     5     6     7
#Enc% ( >=35% >=50% >=70% >=85% >=90% >=95% >=100% )
'msp' :(0.95, 0.9,  0.85, 0.75, 0.65, 0.5,  0,),
'asp' :(0.95, 0.9,  0.85, 0.8,  0.75, 0.7,  0.65,),
'atk' :(0.95, 0.9,  0.8,  0.75, 0.67, 0.6,  0.5,),
'dfn' :(0.95, 0.9,  0.8,  0.67, 0.6,  0.5,  0.4,),
'pro' :(0.95, 0.9,  0.8,  0.67, 0.6,  0.5,  0.4,),
'gra' :(0.9,  0.8,  0.7,  0.6,  0.5,  0.4,  0.3,),
'bal' :(0.9,  0.75, 0.6,  0.5,  0.4,  0.3,  0.2,),
}



    

    #-------------------------------------------------------#
    #  #conversation /#dialogue /#persuasion /#personality  #
    #-------------------------------------------------------#

# constants
MAX_NPC_CONVO_MEMORIES = 10 # how many conversation memories each NPC can store
PERSONALITY_DISPOSITION_INFLUENCE = 1.5
MAX_DISPOSITION = 1000
MAX_ANGER = 100
MAX_ANNOYANCE = 120
MAX_DIABETES = 160

# response types
i=0;
RESPONSE_NONE       =i;i+=1; # no response
RESPONSE_REJECTION  =i;i+=1; # denial of conversation
RESPONSE_ACCEPT     =i;i+=1; # neutral reaction -- move forward with no change in disposition
RESPONSE_MINUS1     =i;i+=1; # 1 -- mild reaction
RESPONSE_MINUS2     =i;i+=1; # 2 -- moderate reaction
RESPONSE_MINUS3     =i;i+=1; # 3 -- intense reaction
RESPONSE_MINUS4     =i;i+=1; # 4 -- reserved for extreme reactions only
RESPONSE_PLUS1      =i;i+=1;
RESPONSE_PLUS2      =i;i+=1;
RESPONSE_PLUS3      =i;i+=1;
RESPONSE_PLUS4      =i;i+=1;

# conversation styles
i=0;
CONVO_DRY           =i;i+=1; # emotionless or monotone style
CONVO_JOKING        =i;i+=1; # rely on humor and lightheartedness
CONVO_POLITE        =i;i+=1; # generically respectful attitude
CONVO_RUDE          =i;i+=1; # generically rude attitude
CONVO_RESPECTFUL    =i;i+=1; # specifically respectful attitude
CONVO_DISRESPECTFUL =i;i+=1; # specifically rude attitude
CONVO_HAUGHTY       =i;i+=1; # generically self-righteous attitude
CONVO_REVERENT      =i;i+=1; # specifically worshipful attitude
CONVO_FRIENDLY      =i;i+=1; # act like their friend
CONVO_COMBATIVE     =i;i+=1; # act like their enemy

CONVO_STYLE_INTENSITY={
CONVO_DRY           : 0,
CONVO_JOKING        : 0.5,
CONVO_POLITE        : 0,
CONVO_RUDE          : 0.1,
CONVO_RESPECTFUL    : 0.1,
CONVO_DISRESPECTFUL : 0.25,
CONVO_HAUGHTY       : 0.1,
CONVO_REVERENT      : 0.25,
CONVO_FRIENDLY      : 0,
CONVO_COMBATIVE     : 1,
}

# persuasion / dialogue types
i=1;
TALK_INTRODUCTION   =i;i+=1; # introduction; first time meeting someone
TALK_GREETING       =i;i+=1; # start of conversation
TALK_REJECTION      =i;i+=1; # rejection of conversation
    # persuasion to yield services
TALK_ASKQUESTION    =i;i+=1;
TALK_INTERROGATE    =i;i+=1; # use intimiation to question
TALK_GOSSIP         =i;i+=1; # rumors / idle chit-chat
TALK_TORTURE        =i;i+=1; # use pain to interrogate
TALK_ASKFAVOR       =i;i+=1;
TALK_BEG            =i;i+=1; # ask favor by appeal to sympathy
TALK_BARTER         =i;i+=1; # trade -- buy/sell
    # persuasion to temporarily improve disposition
    # all of these types of persuasion induce the Charmed status effect
TALK_CHARM          =i;i+=1; 
TALK_BOAST          =i;i+=1; 
    # persuasion to permanently improve disposition
TALK_SMALLTALK      =i;i+=1;
TALK_BRIBERY        =i;i+=1;
TALK_INTIMIDATION   =i;i+=1;
TALK_FLATTERY       =i;i+=1;
TALK_FLIRTATION     =i;i+=1;
TALK_DEBATE         =i;i+=1;
TALK_PESTER         =i;i+=1; # annoy / bother / try to make them mad
TALK_TAUNT          =i;i+=1; # try to make them mad directly
TALK_         =i;i+=1;

PERSUASION={
TALK_GREETING       : ('_',"greet",MAX_DISPOSITION,),
TALK_ASKFAVOR       : ('a',"ask favor",MAX_DISPOSITION,),
TALK_BARTER         : ('b',"barter",0.75*MAX_DISPOSITION,),
TALK_BRIBERY        : ('B',"bribe",0.8*MAX_DISPOSITION),
TALK_CHARM          : ('c',"charm",0.5*MAX_DISPOSITION),
TALK_DEBATE         : ('d',"debate",0.7*MAX_DISPOSITION),
TALK_GOSSIP         : ('g',"gossip",0.6*MAX_DISPOSITION),
TALK_FLATTERY       : ('f',"flatter",0.9*MAX_DISPOSITION),
TALK_FLIRTATION     : ('F',"flirt",MAX_DISPOSITION),
TALK_INTIMIDATION   : ('i',"intimidate",0.5*MAX_DISPOSITION),
TALK_INTERROGATE    : ('I',"interrogate",MAX_DISPOSITION),
TALK_BOAST          : ('o',"boast",0.5*MAX_DISPOSITION),
TALK_PESTER         : ('p',"pester",0.5*MAX_DISPOSITION),
TALK_BEG            : ('P',"beg",0.5*MAX_DISPOSITION),
TALK_ASKQUESTION    : ('q',"ask question",0.5*MAX_DISPOSITION),
TALK_SMALLTALK      : ('s',"small talk",0.5*MAX_DISPOSITION),
TALK_TAUNT          : ('t',"taunt",MAX_DISPOSITION),
TALK_TORTURE        : ('T',"torture",MAX_DISPOSITION),
}

# personality types
i=0;
PERSON_NONE                 =i;i+=1; # no personality
PERSON_PROUD                =i;i+=1;
PERSON_LOWSELFESTEEM        =i;i+=1;
PERSON_ARGUMENTATIVE        =i;i+=1;
PERSON_NONCONFRONTATIONAL   =i;i+=1;
PERSON_OUTGOING             =i;i+=1;
PERSON_SHY                  =i;i+=1;
PERSON_INDEPENDENT          =i;i+=1;
PERSON_CODEPENDENT          =i;i+=1;
PERSON_BUBBLY               =i;i+=1;
PERSON_LOWENERGY            =i;i+=1;
PERSON_MOTIVATED            =i;i+=1;
PERSON_UNMOTIVATED          =i;i+=1;
PERSON_RELAXED              =i;i+=1;
PERSON_UPTIGHT              =i;i+=1;
PERSON_PROACTIVE            =i;i+=1;
PERSON_APATHETIC            =i;i+=1;
PERSON_BEAST                =i;i+=1;
PERSON_ROBOT                =i;i+=1;
PERSON_            =i;i+=1;

# personality compatibility | personality compatibilities
i=1;
E=i;i+=1;
D=i;i+=1;
C=i;i+=1;
B=i;i+=1;
A=i;i+=1;
PERSONALITY_COMPATIBILITIES={
# personality               :           (compatibility)
#                             N P L A N O S I C B L M U R U P A B R 
#                             O R O R O U H N O U O O N E P R P E O 
#                             N O W G N T Y D D B W T M L T O A A B 
#                             E U   U - G   E E B   I O A I A T S O 
#                               D E M C O   P P L E V T X G C H T T 
#                                 S E O I   E E Y N A I E H T E     
#                                 T N N N   N N   E T V D T I T     
#                                 E T F G   D D   R E A     V I     
#                                 E A R     E E   G D T     E C     
#                                 M T O     N N   Y   E             
#                                   I N     T T       D             
#                                   V T                             
#                                   E .                             
#                                                                   
PERSON_NONE                 :(C,C,C,C,C,C,C,C,C,C,C,C,C,C,C,C,C,C,C,),
PERSON_PROUD                :(E,B,D,D,C,A,C,B,D,C,D,A,E,B,D,C,D,E,D,),
PERSON_LOWSELFESTEEM        :(E,C,B,D,B,E,B,D,B,C,B,D,C,B,E,B,C,D,C,),
PERSON_ARGUMENTATIVE        :(E,C,C,A,E,B,D,A,C,B,D,B,D,D,D,B,D,E,E,),
PERSON_NONCONFRONTATIONAL   :(E,D,C,E,B,D,A,B,D,C,B,C,C,A,E,D,B,D,C,),
PERSON_OUTGOING             :(E,B,E,C,C,A,C,C,C,A,E,B,D,C,C,C,C,E,C,),
PERSON_SHY                  :(E,C,B,E,A,D,B,D,B,D,B,D,B,B,C,C,B,E,C,),
PERSON_INDEPENDENT          :(E,C,E,D,C,C,C,C,D,C,C,B,E,B,B,C,E,D,C,),
PERSON_CODEPENDENT          :(E,B,B,B,D,C,B,A,A,C,D,B,C,C,C,B,C,D,B,),
PERSON_BUBBLY               :(E,C,D,B,C,B,C,C,C,A,E,B,D,C,C,B,D,E,C,),
PERSON_LOWENERGY            :(E,E,B,E,A,D,C,B,D,E,B,D,B,A,E,D,B,D,C,),
PERSON_MOTIVATED            :(E,B,C,B,D,B,E,B,D,C,D,B,E,D,B,C,E,C,C,),
PERSON_UNMOTIVATED          :(E,E,B,D,B,C,B,D,B,C,B,C,A,B,E,E,B,D,C,),
PERSON_RELAXED              :(E,D,C,D,B,C,B,B,D,D,B,C,B,A,E,D,C,C,C,),
PERSON_UPTIGHT              :(E,B,D,E,C,D,D,A,E,C,D,B,E,D,B,E,E,E,D,),
PERSON_PROACTIVE            :(E,D,D,B,E,B,D,B,C,C,D,B,D,D,C,A,E,B,B,),
PERSON_APATHETIC            :(E,C,C,C,C,C,C,C,C,C,C,C,C,C,C,C,C,C,C,),
PERSON_BEAST                :(E,B,E,D,D,C,C,C,C,C,E,B,E,D,C,D,A,A,E,),
PERSON_ROBOT                :(C,C,C,C,C,C,C,C,C,C,C,C,C,C,C,C,C,E,A,),
}

MAIN_PERSONALITIES=(
    PERSON_PROUD,
    PERSON_LOWSELFESTEEM,
    PERSON_ARGUMENTATIVE,
    PERSON_NONCONFRONTATIONAL,
    PERSON_OUTGOING,
    PERSON_SHY,
    PERSON_INDEPENDENT,
    PERSON_CODEPENDENT,
    PERSON_BUBBLY,
    PERSON_LOWENERGY,
    PERSON_MOTIVATED,
    PERSON_UNMOTIVATED,
    PERSON_RELAXED,
    PERSON_UPTIGHT,
    PERSON_PROACTIVE,
    PERSON_APATHETIC,
    )

# value modifiers for bartering (value of own things vs. other things)
VAL_NORM=1
VAL_PLUS1=1.1
VAL_MINUS1=0.9
VAL_PLUS2=1.2
VAL_MINUS2=0.8
VAL_PLUS3=1.3
VAL_MINUS3=0.7

PERSONALITIES={
# personality : (
#   name, likes, dislikes,
#   perceived_value_owned, perceived_value_other,
#   )
PERSON_PROUD : (
    "proud",
    (TALK_FLATTERY,CONVO_RESPECTFUL,),
    (TALK_INTIMIDATION,CONVO_DISRESPECTFUL,),
    VAL_PLUS2, VAL_MINUS2,
    ),
PERSON_LOWSELFESTEEM : (
    "low self-esteem",
    (TALK_FLATTERY,CONVO_DISRESPECTFUL,),
    (TALK_FLIRTATION,CONVO_RESPECTFUL,),
    VAL_NORM, VAL_NORM,
    ),
PERSON_ARGUMENTATIVE : (
    "argumentative",
    (TALK_DEBATE,CONVO_COMBATIVE,),
    (TALK_GOSSIP,CONVO_FRIENDLY,),
    VAL_PLUS1, VAL_MINUS1,
    ),
PERSON_NONCONFRONTATIONAL : (
    "non-confrontational",
    (TALK_GOSSIP,CONVO_FRIENDLY,),
    (TALK_DEBATE,CONVO_COMBATIVE,),
    VAL_PLUS1, VAL_MINUS1,
    ),
PERSON_OUTGOING : (
    "outgoing",
    (TALK_GOSSIP,CONVO_HAUGHTY,),
    (TALK_INTIMIDATION,CONVO_RUDE,),
    VAL_PLUS1, VAL_MINUS1,
    ),
PERSON_SHY : (
    "shy",
    (TALK_FLATTERY,CONVO_DRY,),
    (TALK_SMALLTALK,CONVO_JOKING,),
    VAL_PLUS1, VAL_MINUS1,
    ),
PERSON_INDEPENDENT : (
    "independent",
    (TALK_SMALLTALK,CONVO_POLITE,),
    (TALK_BRIBERY,CONVO_HAUGHTY,),
    VAL_PLUS2, VAL_MINUS2,
    ),
PERSON_CODEPENDENT : (
    "codependent",
    (TALK_INTIMIDATION,CONVO_HAUGHTY,),
    (TALK_BRIBERY,CONVO_RESPECTFUL,),
    VAL_NORM, VAL_NORM,
    ),
PERSON_BUBBLY : (
    "bubbly",
    (TALK_FLIRTATION,CONVO_JOKING,),
    (TALK_FLATTERY,CONVO_DRY,),
    VAL_PLUS1, VAL_MINUS1,
    ),
PERSON_LOWENERGY : (
    "low energy",
    (TALK_SMALLTALK,CONVO_DRY,),
    (TALK_FLIRTATION,CONVO_COMBATIVE,),
    VAL_PLUS1, VAL_MINUS1,
    ),
PERSON_MOTIVATED : (
    "motivated",
    (TALK_BRIBERY,CONVO_POLITE,),
    (TALK_GOSSIP,CONVO_JOKING,),
    VAL_PLUS1, VAL_MINUS1,
    ),
PERSON_UNMOTIVATED : (
    "unmotivated",
    (TALK_INTIMIDATION,CONVO_DRY,),
    (TALK_DEBATE,CONVO_POLITE,),
    VAL_PLUS1, VAL_MINUS1,
    ),
PERSON_RELAXED : (
    "relaxed",
    (TALK_SMALLTALK,CONVO_FRIENDLY,),
    (TALK_DEBATE,CONVO_HAUGHTY,),
    VAL_PLUS1, VAL_MINUS1,
    ),
PERSON_UPTIGHT : (
    "uptight",
    (TALK_DEBATE,CONVO_POLITE,),
    (TALK_GOSSIP,CONVO_RUDE,),
    VAL_PLUS1, VAL_MINUS1,
    ),
PERSON_PROACTIVE : (
    "proactive",
    (TALK_DEBATE,CONVO_COMBATIVE,),
    (TALK_SMALLTALK,CONVO_DISRESPECTFUL,),
    VAL_PLUS1, VAL_MINUS1,
    ),
PERSON_ROBOT : (
    "Mr. VendR",
    (TALK_BARTER,CONVO_DRY,),
    (TALK_SMALLTALK,CONVO_JOKING,),
    VAL_PLUS3, VAL_MINUS3,
    ),
PERSON_APATHETIC : (
    "apathetic", (0,0,), (0,0,), VAL_NORM, VAL_NORM,
    ),
PERSON_NONE : (
    "emotionless", (0,0,), (0,0,), VAL_NORM, VAL_NORM,
    ),
}

DISPOSITION_LEVELS={
#>= : string,
0   : 'loathes',
1   : 'hates',
100 : 'dislikes',
200 : 'is indifferent to',
300 : 'is partial to',
400 : 'likes',
500 : 'trusts',
600 : 'cares about',
700 : 'cares deeply about',
800 : 'loves',
900 : 'worships',
1000: 'unconditionally loves',
}


    #---------#
    # #paces  #
    #---------#
i=0;




    #---------#
    # #items  #
    #---------#

# crafting
CRAFT_NRG_MULT      = 5     # multiplier for crafting AP cost (all recipes)

# limb weapons
i=1;
LIMBWPN_HAND        =i;i+=1;
LIMBWPN_KERATINCLAW =i;i+=1;
LIMBWPN_BONECLAW    =i;i+=1;
LIMBWPN_METALHAND   =i;i+=1; # cyborg / android hand
LIMBWPN_TENTACLE    =i;i+=1;
LIMBWPN_PSEUDOPOD   =i;i+=1;
LIMBWPN_PINCER      =i;i+=1; # mandible / pincer-claw
LIMBWPN_TEETH       =i;i+=1; # herbivore / omnivore's teeth
LIMBWPN_SHARPTEETH  =i;i+=1; # carnivore's teeth





    #-------------------#
    #      #body        #
    #-------------------#

# food
SATIETY_PER_MORSEL  = 25    # Calories per morsel of food
SATIETY_MULT_RAPID  = 0.25  # caloric value multiplier when you eat fast
FOOD_BIGMEAL        = 108   # caloric content (multiplier)
FOOD_MEAL           = 36
FOOD_RATION         = 12
FOOD_SERVING        = 4
FOOD_MORSEL         = 1
FOOD_BIGMEAL_NRG    = 12000*AVG_SPD   # AP cost for eating
FOOD_MEAL_NRG       = 3000*AVG_SPD
FOOD_RATION_NRG     = 2000*AVG_SPD
FOOD_SERVING_NRG    = 600*AVG_SPD
FOOD_MORSEL_NRG     = 150*AVG_SPD

# calorie costs for 75kg human per turn of actions (1 Calorie == 1000 calories. Typically we refer to "calories" meaning KiloCalories, but I mean actual calories here, not KiloCalories.)
CALCOST_SLEEP           = 25        # metabolism while asleep
CALCOST_REST            = 40        # metabolism at rest (awake, alert)
CALCOST_LIGHTACTIVITY   = 100       # walking, doing any small motor task
CALCOST_MEDIUMACTIVITY  = 200       # jogging, big motor muscle task
CALCOST_HEAVYACTIVITY   = 300       # running, climbing, jumping, swimming, light combat
CALCOST_INTENSEACTIVITY = 600       # wrestling, combat
CALCOST_MAXINTENSITY    = 1200      # sprinting, intense combat
# metabolism
METABOLISM_HEAT         = 0.00001   # heat generated from metabolism
METABOLISM_THIRST       = 0.05      # metabolising food takes some amount of water
FAT_RESCOLD             = 2         # per kg of fat
FAT_RESHEAT             = -1        # per kg of fat
DEFAULT_BODYFAT_HUMAN   = 0.1       # ratio of total mass
# sleepiness
FATIGUE_SLEEP           = -1        # fatigue regeneration while asleep
FATIGUE_REST            = 1         # fatigue regen. at rest (awake, alert)
FATIGUE_LIGHTACTIVITY   = 10        # walking, doing any small motor task
FATIGUE_MEDIUMACTIVITY  = 25        # jogging, big motor muscle task
FATIGUE_HEAVYACTIVITY   = 50        # running, climbing, jumping, swimming, light combat
FATIGUE_INTENSEACTIVITY = 100       # wrestling, combat
FATIGUE_MAXINTENSITY    = 200       # sprinting, intense combat

# MP (stamina) cost to perform actions
STA_SLOWWALK        = 2 # slow movement
STA_MOVE            = 4 # standard movement option
STA_JOG             = 8
STA_RUN             = 16
STA_SPRINT          = 32
STA_ATTACK          = 8 # multiplied by STA cost of weapons?
STA_PUNCH           = 24
STA_GRAB            = 4
STA_PICKUP          = 1 # times KG?
STA_POCKET          = 1
STA_RUMMAGE         = 2
STA_OPEN            = 2
STA_CLOSE           = 1
STA_EXAMINE         = 0
STA_QUAFF           = 0
STA_EAT             = 1
STA_READ            = 0
STA_WIELDSMALL      = 1
STA_WIELDLARGE      = 2
STA_WIELDXLARGE     = 4
STA_USE             = 1 # default use item cost

#energy (action potential or AP) cost to perform actions
NRG_MOVE            = 100   # on default terrain (flat ground) 
NRG_ATTACK          = 200
NRG_TALK            = 200
NRG_BOMB            = 200   
NRG_PICKUP          = 50    # grab thing and wield it (requires empty hand)
NRG_POCKET          = 100   # picking up and putting in your inventory
NRG_RUMMAGE         = 50    # Cost to look at the contents of a container
NRG_OPEN            = 80    # Cost to open a door
NRG_CLOSE           = 40    # Cost to close a door or simple container
NRG_TAKE            = 100   # Cost of picking an item from a container
NRG_IDENTIFY        = 100   # observing something to identify it better
NRG_QUAFF           = 100   # AP cost to swallow something smooth
NRG_EAT             = 300   # default AP cost per unit of consumption to eat
NRG_EAT_FAST        = 150   # rapid consumption AP cost
NRG_EAT_MIN         = 50    # minimum AP cost to eat any amount of food
NRG_READ            = 50    # cost to read a simple thing (phrase/sentence)
NRG_READPARAGRAPH   = 250   # cost to read an idea (paragraph/complex sentence)
NRG_READPAGE        = 2500  # cost to read a page of a book (several ideas forming one meta-idea that requires you to read it all to understand)
NRG_USE             = 100   # generic use function
NRG_WIELDSMALL      = 25    # default AP it takes to brandish a weapon (small or easy to brandish, like handguns, knives, swords, etc.)
NRG_WIELD           = 75    # default AP it takes to brandish a weapon (medium sized 1-h, like a club). Notice "default" keyword. It can be more or less depending on context/skill of user, etc.
NRG_WIELDLARGE      = 150   # default AP it takes to brandish a weapon (large / 2-h)
NRG_WIELDXLARGE     = 300   # default AP it takes to brandish a weapon (largest 2-h weapons)
NRG_WIELDCUMBERSOME = 600   # default AP it takes to brandish a cumbersome item as a weapon
NRG_RELOAD          = 200
# multipliers
NRGM_QUICKATTACK    = 0.6
STAM_QUICKATTACK    = 1.5

# paces
i=0;
PACE_STOPPED    =i;i+=1;
PACE_SNAILPACE  =i;i+=1;
PACE_SLOWWALK   =i;i+=1;
PACE_POWERWALK  =i;i+=1;
PACE_JOG        =i;i+=1;
PACE_RUN        =i;i+=1;
PACE_SPRINT     =i;i+=1;

# getting activity levels
PACE_TO_ACTIVITY={ # from movement pace
PACE_STOPPED    : (0,CALCOST_REST,FATIGUE_REST,),
PACE_SNAILPACE  : (STA_SLOWWALK,CALCOST_LIGHTACTIVITY,FATIGUE_LIGHTACTIVITY,),
PACE_SLOWWALK   : (STA_SLOWWALK,CALCOST_LIGHTACTIVITY,FATIGUE_LIGHTACTIVITY,),
PACE_POWERWALK  : (STA_MOVE,CALCOST_LIGHTACTIVITY,FATIGUE_LIGHTACTIVITY,),
PACE_JOG        : (STA_JOG,CALCOST_MEDIUMACTIVITY,FATIGUE_MEDIUMACTIVITY,),
PACE_RUN        : (STA_RUN,CALCOST_HEAVYACTIVITY,FATIGUE_HEAVYACTIVITY,),
PACE_SPRINT     : (STA_SPRINT,CALCOST_MAXINTENSITY,FATIGUE_MAXINTENSITY,),
}


# body plans #
i=1;
BODYPLAN_HUMANOID   =i;i+=1;
BODYPLAN_INSECTOID  =i;i+=1; # 6-legged
BODYPLAN_ARACHNID   =i;i+=1; # 8-legged arthropod
BODYPLAN_4LEGGED    =i;i+=1; # canine, feline, equestrian, 
BODYPLAN_8ARMS      =i;i+=1; # octopus
BODYPLAN_SNAKE      =i;i+=1; # no legs; head and long body (and tail?)
BODYPLAN_CUSTOM     =i;i+=1; # for special cases, body plan built up manually
#

BODY_TEMP = { #temperature
# plan  : (avg_temp, +hyperthermia, +hypothermia)
BODYPLAN_HUMANOID   : (37, 3, -9,),
BODYPLAN_4LEGGED    : (39, 6, -9,),
BODYPLAN_INSECTOID  : (30, 8, -8,),
}
BODY_BLOOD = {
# plan : blood mass as a ratio of body mass, % blood needed to survive
BODYPLAN_HUMANOID   : (0.07, 0.5,),
BODYPLAN_4LEGGED    : (0.08, 0.5,),
BODYPLAN_INSECTOID  : (0.04, 0.5,),
}

METABOLIC_RATE_FOOD = { # how fast you metabolize calories from food
BODYPLAN_HUMANOID   : 3334,
BODYPLAN_4LEGGED    : 5000,
BODYPLAN_INSECTOID  : 6667,
}
METABOLIC_RATE_WATER = { # how fast you metabolize water
BODYPLAN_HUMANOID   : 10000,
BODYPLAN_4LEGGED    : 10000,
BODYPLAN_INSECTOID  : 50000,
}


# #statuses of bodies / body parts  #

# body positions
i=1;
BODYPOS_UPRIGHT     =i;i+=1;
BODYPOS_CROUCHED    =i;i+=1;
BODYPOS_SEATED      =i;i+=1;
BODYPOS_SUPINE      =i;i+=1;
BODYPOS_PRONE       =i;i+=1;
BODYPOS_OFFENSIVE   =i;i+=1;
BODYPOS_DEFENSIVE   =i;i+=1;
BODYPOS_CQB         =i;i+=1;

BODYPOSITIONS={
BODYPOS_UPRIGHT     : "upright",
BODYPOS_CROUCHED    : "crouched",
BODYPOS_SEATED      : "seated",
BODYPOS_SUPINE      : "supine",
BODYPOS_PRONE       : "prone",
BODYPOS_OFFENSIVE   : "offensive stance",
BODYPOS_DEFENSIVE   : "defensive stance",
BODYPOS_CQB         : "CQB stance",
}

# position stat modifiers
CROUCHED_MSPMOD     = 0.6666667
CROUCHED_HEIGHTMOD  = 0.75
CROUCHED_AGIMOD     = 0.9
CROUCHED_ATK        = -5
CROUCHED_DFN        = -10
CROUCHED_PEN        = -3
CROUCHED_PRO        = -3
CROUCHED_GRA        = 3

SEATED_MSPMOD       = 0.15
SEATED_HEIGHTMOD    = 0.5
SEATED_AGIMOD       = 0.666667
SEATED_ATK          = -20
SEATED_DFN          = -20
SEATED_PEN          = -6
SEATED_PRO          = -6
SEATED_GRA          = -3

SUPINE_MSPMOD       = 0.1
SUPINE_HEIGHTMOD    = 0.2
SUPINE_AGIMOD       = 0.25
SUPINE_ATK          = -25
SUPINE_DFN          = -25
SUPINE_PEN          = -9
SUPINE_PRO          = -9
SUPINE_GRA          = -6

PRONE_MSPMOD        = 0.075
PRONE_HEIGHTMOD     = 0.2
PRONE_AGIMOD        = 0.5
PRONE_ATK           = -30
PRONE_DFN           = -30
PRONE_PEN           = -12
PRONE_PRO           = -12
PRONE_GRA           = -12

OFFENSIVE_REACHMOD  = 1.2
OFFENSIVE_DMGMOD    = 1.5
OFFENSIVE_ASP       = -40
OFFENSIVE_ATK       = 4
OFFENSIVE_DFN       = -8
OFFENSIVE_GRA       = -6
OFFENSIVE_PEN       = 2
OFFENSIVE_PRO       = -3

DEFENSIVE_REACHMOD  = 0.75
DEFENSIVE_DMGMOD    = 0.666667
DEFENSIVE_ASP       = 40
DEFENSIVE_ATK       = -4
DEFENSIVE_DFN       = 4
DEFENSIVE_GRA       = 4
DEFENSIVE_PEN       = -4
DEFENSIVE_PRO       = 2
DEFENSIVE_CTR       = 5
DEFENSIVE_SPLASHMOD = 1.5

CQB_REACHMOD        = 0
CQB_ATK             = 4
CQB_DFN             = -4
CQB_GRA             = 6
CQB_PEN             = 6
CQB_PRO             = 1
CQB_SPLASHMOD       = 0.25

# body cores
i=1;
CORETYPE_TORSO  =i;i+=1;
CORETYPE_  =i;i+=1;

CORETYPES={
BODYPLAN_HUMANOID : CORETYPE_TORSO,
}

# body parts

i=1;
BP_HEAD         =i;i+=1;
BP_NECK         =i;i+=1;
BP_FACE         =i;i+=1;
BP_EYES         =i;i+=1;
BP_EARS         =i;i+=1;
BP_MOUTH        =i;i+=1;
BP_FRONT        =i;i+=1;
BP_BACK         =i;i+=1;
BP_HIPS         =i;i+=1;
BP_CORE         =i;i+=1;
BP_ARM          =i;i+=1;
BP_LEG          =i;i+=1;
BP_HAND         =i;i+=1;
BP_FOOT         =i;i+=1;
BP_WING         =i;i+=1;
BP_TAIL         =i;i+=1;
BP_BEAK         =i;i+=1;
BP_GENITALS     =i;i+=1;
BP_APPENDAGE    =i;i+=1;
BP_TENTACLE     =i;i+=1;
BP_PSEUDOPOD    =i;i+=1;
BP_AMEBOID      =i;i+=1;
BP_MANDIBLE     =i;i+=1;
BP_INSECTHEAD   =i;i+=1;
BP_INSECTLEG    =i;i+=1;
BP_INSECTTHORAX =i;i+=1;
BP_INSECTABDOMEN=i;i+=1;
# coverage of specific body parts, for armor skill bonuses
COVERAGE={
    BP_HAND  : 0.05,
    BP_ARM   : 0.1,
    BP_LEG   : 0.1,
    BP_HEAD  : 0.1,
    BP_CORE  : 0.1,
    BP_FRONT : 0.1,
    BP_BACK  : 0.1,
    BP_HIPS  : 0.1,
}

# body parts meta

i=1;
BPM_TORSO        =i;i+=1;
BPM_HEAD         =i;i+=1;
BPM_ARM          =i;i+=1;
BPM_LEG          =i;i+=1;

# body plan data #

BPM_COVERAGE={ # for ranged battle
    # plan : {BPM_const : {BP_ const : coverage (adds up to 100),},},
    BODYPLAN_HUMANOID:{
BPM_TORSO   : {BP_CORE:30,BP_HIPS:30,BP_FRONT:20,BP_BACK:20,},
BPM_HEAD    : {BP_FACE:25,BP_HEAD:50,BP_MOUTH:10,BP_EYES:1,BP_EARS:4,BP_NECK:10,},
BPM_ARM     : {BP_ARM:80,BP_HAND:20,},
BPM_LEG     : {BP_LEG:80,BP_FOOT:20,},
    },
}

BODY_COVERAGE={ # for ranged battle
    #   body part coverage, for targeting a specific body part
    # {plan : {BPM_ const : body coverage per part},},
    # coverage must add up to 100 (*with the healthy # of limbs)
#(example: human: (2 legs==2*15==30) + (2 arms==2*10==20) + 45 + 5 == 100)
BODYPLAN_HUMANOID   : {BPM_TORSO:45, BPM_HEAD:5, BPM_LEG:15, BPM_ARM:10,},
#TODO:update all these to same format as above!
BODYPLAN_INSECTOID  : {"core":60, "head":15, "legs":25,}, 
BODYPLAN_4LEGGED    : {"core":45, "head":5, "legs":50,},
BODYPLAN_8ARMS      : {"core":10, "head":25, "arms":65,},
BODYPLAN_CUSTOM     : {"core":100,},
}


    # Wounds / Penalties for BP statuses / BP damage (body part statuses / body part damage) #

# wound Types
i=1;
WOUNDTYPE_A     =i;i+=1;
WOUNDTYPE_B     =i;i+=1;
WOUNDTYPE_C     =i;i+=1;
WOUNDTYPE_0     =i;i+=1;
WOUNDTYPE_1     =i;i+=1;
WOUNDTYPE_2     =i;i+=1;
WOUNDTYPE_3A    =i;i+=1;
WOUNDTYPE_3B    =i;i+=1;
WOUNDTYPE_3C    =i;i+=1;
WOUNDTYPE_4     =i;i+=1;

WOUNDTYPE_DESCRIPTIONS={
WOUNDTYPE_A  :"Type A wound: superficial or microscopic soft tissue damage.",
WOUNDTYPE_B  :"Type B wound: damage to deep nervous or muscle tissue.",
WOUNDTYPE_C  :"Type C wound: deep organ damage requiring urgent medical care.",
WOUNDTYPE_0  :"Type 0 wound: <= 1mm, microscopic or no tissue damage.",
WOUNDTYPE_1  :"Type 1 wound: <= 1cm, minimal contamination or muscle damage.",
WOUNDTYPE_2  :"Type 2 wound: <= 10cm, moderate soft tissue injury",
WOUNDTYPE_3A :"Type 3A wound: typically > 10cm, extensive soft tissue damage and contamination",
WOUNDTYPE_3B :"Type 3B wound: extensive periosteal stripping, requires soft tissue coverage",
WOUNDTYPE_3C :"Type 3C wound: typically > 10cm, vascular or arterial injury requiring urgent surgery",
WOUNDTYPE_4  :"Type 4 wound: typically > 10cm, vascular or arterial injury requiring urgent specialist surgery"
}
#Type 4: wound typically > 10cm, vascular or arterial injury requiring urgent specialist surgery

# wound status categories. One entity can only have one of each type of injury.
# Injuries overwrite others of the same type if the degree exceeds that of the
# existing injury. If the degree is the same, increase the degree by 1 (not
# to exceed the maximum).
i=1;
WOUND_RASH      =i;i+=1;
WOUND_CUT       =i;i+=1;
WOUND_PUNCTURE  =i;i+=1;
WOUND_GUNSHOT   =i;i+=1;
WOUND_MUSCLE    =i;i+=1;
WOUND_ORGAN     =i;i+=1;
WOUND_BRAIN     =i;i+=1;

WOUNDS={
# status category : { degree : {data} }
# player sees the stats: name, description, and wound type description;
#   as well as the stats affected with the injury
#   descriptions are only available if you hover over the injury name with the mouse
#       or go to the body status page, which details the body status specifically
#           (TODO: make this)
WOUND_RASH:{ # abrasions, burns, etc.
    'degrees':8,
    1:{'name':'irritation', 'desc':'rash', 'type':WOUNDTYPE_A,
       'resbio':-2, 'respain':-2, 'resbleed':-2, 'resfire':-1,},
    2:{'name':'inflammation', 'desc':'a scape or multiple rashes', 'type':WOUNDTYPE_A,
       'resbio':-4, 'respain':-4, 'resbleed':-4, 'resfire':-2,},
    3:{'name':'abrasion', 'desc':'or multiple scrapes', 'type':WOUNDTYPE_A,
       'resbio':-6, 'respain':-8, 'resbleed':-6, 'resfire':-4,},
    4:{'name':'laceration', 'desc':'or multiple abrasions', 'type':WOUNDTYPE_0,
       'resbio':-8, 'respain':-16, 'resbleed':-8, 'resfire':-8,'rescold':-2,},
    5:{'name':'burn', 'desc':'or multiple lacerations', 'type':WOUNDTYPE_1,
       'resbio':-8, 'respain':-32, 'resbleed':-8, 'resfire':-16,'rescold':-4,},
    6:{'name':'deep burn', 'desc':'or multiple burns', 'type':WOUNDTYPE_2,
       'resbio':-16, 'respain':-64, 'resbleed':-16, 'resfire':-32,'rescold':-8,},
    7:{'name':'skinned', 'desc':'substantial amount of damaged skin', 'type':WOUNDTYPE_3B,
       'resbio':-32, 'respain':-64, 'resbleed':-32, 'resfire':-32,'rescold':-16,},
    8:{'name':'fully skinned', 'desc':'<= 1/2 total skin remaining', 'type':WOUNDTYPE_3B,
       'resbio':-64, 'respain':-128, 'resbleed':-64, 'resfire':-64,'rescold':-32,},
    },
WOUND_CUT:{ # cuts
    'degrees':6,
    1:{'name':'nick', 'desc':'paper cut', 'type':WOUNDTYPE_0,
       'resbio':-4, 'respain':-1, 'resbleed':-2,},
    2:{'name':'cut', 'desc':'or multiple nicks', 'type':WOUNDTYPE_1,
       'resbio':-8, 'respain':-2, 'resbleed':-4,},
    3:{'name':'slice', 'desc':'or multiple cuts', 'type':WOUNDTYPE_2,
       'gra':-1, 'resbio':-16, 'respain':-4, 'resbleed':-8,},
    4:{'name':'deep cut', 'desc':'or multiple slices', 'type':WOUNDTYPE_3A,
       'gra':-2, 'resbio':-32, 'respain':-8, 'resbleed':-16,},
    5:{'name':'arterial cut', 'desc':'or multiple deep cuts', 'type':WOUNDTYPE_3C,
       'gra':-4, 'resbio':-64, 'respain':-16, 'resbleed':-32,},
    6:{'name':'gushing slice', 'desc':'possibly inhumane blades used', 'type':WOUNDTYPE_4,
       'gra':-8, 'resbio':-64, 'respain':-32, 'resbleed':-64,},
    },
WOUND_PUNCTURE:{ # puncture or stab wounds.
    # Harder to heal than cuts, and cause more bleeding at the time of the damage.
    # However, stat mods are less penalizing than with cuts.
    'degrees':6,
    1:{'name':'incision', 'desc':'needle poke', 'type':WOUNDTYPE_0,
       'resbio':-4, 'resbleed':-1,},
    2:{'name':'piercing', 'desc':'or multiple incisions', 'type':WOUNDTYPE_1,
       'resbio':-8, 'resbleed':-2,},
    3:{'name':'puncture', 'desc':'deep or wide incision, or multiple piercings', 'type':WOUNDTYPE_2,
       'resbio':-16, 'resbleed':-4,},
    4:{'name':'stab wound', 'desc':'full-depth puncture, or multiple punctures', 'type':WOUNDTYPE_3A,
       'resbio':-32, 'resbleed':-8,},
    5:{'name':'arterial puncture', 'desc':'or multible stab wounds', 'type':WOUNDTYPE_3C,
       'resbio':-64, 'resbleed':-16,},
    6:{'name':'gushing hole', 'desc':'possibly inhumane blades used', 'type':WOUNDTYPE_4,
       'resbio':-64, 'respain':-16, 'resbleed':-32,},
    },
WOUND_GUNSHOT:{ # gun shot wounds
    'degrees':5,
    1:{'name':'low-velocity gunshot', 'desc':'projectile speed <=1100 ft/s', 'type':WOUNDTYPE_1,
       'resbio':-8, 'respain':-8, 'resbleed':-4,},
    2:{'name':'medium-velocity gunshot', 'desc':'projectile speed 1200-2000 ft/s or multiple low-velocity gunshots', 'type':WOUNDTYPE_2,
       'resbio':-16, 'respain':-16, 'resbleed':-8,},
    3:{'name':'high-velocity gunshot', 'desc':'projectile speed 2000-3500 ft/s or multiple medium-velocity gunshots', 'type':WOUNDTYPE_3A,
       'resbio':-32, 'respain':-32, 'resbleed':-16,},
    4:{'name':'arterial gunshot', 'desc':'or high high-velocity gunshots', 'type':WOUNDTYPE_3C,
       'resbio':-64, 'respain':-64, 'resbleed':-32,},
    5:{'name':'gushing gunshot', 'desc':'possibly inhumane rounds used', 'type':WOUNDTYPE_4,
       'resbio':-96, 'respain':-96, 'resbleed':-64,},
    },
WOUND_MUSCLE:{ # bruising and tears / ruptured muscle
    'degrees':8,
    1:{'name':'sore muscles', 'desc':'dull ache', 'type':WOUNDTYPE_A,
       'respain':-16, 'msp':0.98, },
    2:{'name':'knotted muscles', 'desc':'or intense soreness', 'type':WOUNDTYPE_A,
       'atk':-1,'dfn':-1,'gra':-1, 'respain':-24, 'msp':0.95, 'asp':0.98,},
    3:{'name':'contusion', 'desc':'a bruise or edema; microscopic muscle tears', 'type':WOUNDTYPE_A,
       'atk':-2,'dfn':-2,'gra':-2, 'respain':-32, 'msp':0.9, 'asp':0.96,},
    4:{'name':'strained muscles', 'desc':'or sprain; macroscopic muscular tears', 'type':WOUNDTYPE_B,
       'atk':-3,'dfn':-3,'gra':-3, 'respain':-48, 'msp':0.85, 'asp':0.94,},
    5:{'name':'torn muscles', 'desc':'or multiple strained muscles', 'type':WOUNDTYPE_B,
       'atk':-4,'dfn':-4,'gra':-4, 'respain':-64, 'msp':0.8, 'asp':0.92,},
    6:{'name':'ripped muscles', 'desc':'or multiple torn muscles', 'type':WOUNDTYPE_B,
       'atk':-6,'dfn':-6,'gra':-6, 'respain':-80, 'msp':0.7, 'asp':0.9,},
    7:{'name':'ruptured muscles', 'desc':'or multiple ripped muscles', 'type':WOUNDTYPE_3B,
       'atk':-8,'dfn':-8,'gra':-8, 'respain':-96, 'msp':0.6, 'asp':0.85,},
    8:{'name':'mangled muscles', 'desc':'or multiple ruptured muscles', 'type':WOUNDTYPE_3B,
       'atk':-16,'dfn':-16,'gra':-16, 'respain':-128, 'msp':0.5, 'asp':0.75,},
    },
WOUND_ORGAN:{ # internal organ damage
    'degrees':4,
    1:{'name':'bruised organs', 'desc':'minor internal organ damage', 'type':WOUNDTYPE_A,
       'end':-1, 'con':-1, 'respain':-16, 'resbleed':-16, },
    2:{'name':'organ damage', 'desc':'permanent internal organ damage', 'type':WOUNDTYPE_C,
       'end':-2, 'con':-2, 'respain':-32, 'resbleed':-32,},
    3:{'name':'organ failure', 'desc':'life-threatening organ damage', 'type':WOUNDTYPE_C,
       'end':-4, 'con':-4, 'respain':-64, 'resbleed':-64,},
    4:{'name':'septic shock', 'desc':'systemic organ failure', 'type':WOUNDTYPE_C,
       'end':-8, 'con':-8, 'respain':-128, 'resbleed':-128,},
    },
WOUND_BRAIN:{ # uses multipliers
    'degrees':6,
    1:{'name':'brain contusion', 'desc':'bleeding and swelling of the brain', 'type':WOUNDTYPE_C,
       'int':0.9, 'agi':0.9, 'dex':0.9, 'bal':0.9, },
    2:{'name':'concussion', 'desc':'temporary unconsciousness or confusion', 'type':WOUNDTYPE_C,
       'int':0.8, 'agi': 0.8, 'dex':0.8, 'bal':0.8, },
    3:{'name':'brain damage', 'desc':'temporary loss of cognition and motor function', 'type':WOUNDTYPE_C,
       'int':0.7, 'agi':0.7, 'dex':0.7, 'bal':0.7, },
    4:{'name':'permanent brain damage', 'desc':'permanent loss of cognition and motor function', 'type':WOUNDTYPE_C,
       'int':0.6, 'agi':0.6, 'dex':0.6, 'bal':0.6, },
    5:{'name':'major brain damage', 'desc':'near-total shutdown of the entire nervous system', 'type':WOUNDTYPE_C,
       'int':0.3, 'agi':0.5, 'dex':0.5, 'bal':0.3, },
    6:{'name':'brain dead', 'desc':'total shutdown of the entire nervous system', 'type':WOUNDTYPE_C,
       'int':0, 'agi':0, 'dex':0, 'bal':0, },
    },
}

# body part damage
BP_HEALTH_MAX = 100
BP_STAMINA_MAX = 100

# body part damage stat mods -- bone health of body parts -> stat penalties
BP_HEALTH_STATMODS={
    # BP_ type : {ratio (multiplied by BP_HEALTH_MAX) : {mods}}
    # some mods use multipliers (take note when updating _update_stats!)
BP_HEAD         :{
    0.8 : {'int':-1, 'respain':-2, 'bal':-1, 'hearing':0.9, 'sight':0.9,},
    0.6 : {'int':-2, 'respain':-4, 'bal':-2, 'hearing':0.8, 'sight':0.8,},
    0.4 : {'int':-3, 'respain':-8, 'bal':-4, 'hearing':0.7, 'sight':0.7,},
    0.2 : {'int':-4, 'respain':-16, 'bal':-8, 'hearing':0.6, 'sight':0.6,},
    0   : {'int':-5, 'respain':-32, 'bal':-16, 'hearing':0.5, 'sight':0.5,},
    },
BP_NECK         :{
    0.8 : {'respain':-2, 'resbleed':-4,},
    0.6 : {'respain':-4, 'resbleed':-8,},
    0.4 : {'respain':-8, 'resbleed':-16,},
    0.2 : {'respain':-16, 'resbleed':-32,},
    0   : {'respain':-32, 'resbleed':-64,},
    },
BP_FACE         :{
    0.8 : {'respain':-2, 'bea':-4, 'idn':-4,},
    0.6 : {'respain':-4, 'bea':-8, 'idn':-8,},
    0.4 : {'respain':-8, 'bea':-16, 'idn':-12,},
    0.2 : {'respain':-16, 'bea':-32, 'idn':-16,},
    0   : {'respain':-32, 'bea':-64, 'idn':-20,},
    },
BP_EYES         :{
    # NOTE: in cases of multiple visual systems, the ratio is taken as the combined
    # average health of all visual systems for the entity. Thus, one destroyed set of
    # eyes and one fully healed set of eyes will together yield a ratio of 0.5 for the
    # purposes of the following stat penalties.
    0.8:{'sight':0.9, 'resbio': -2, 'pro': -1, 'dfn':-1,},
    0.6:{'sight':0.8, 'resbio': -4, 'pen':-1, 'pro': -2, 'atk':-1, 'dfn':-2,},
    0.4:{'sight':0.6, 'resbio': -8, 'pen':-2, 'pro': -3, 'atk':-2, 'dfn':-4,},
    0.2:{'sight':0.3, 'resbio': -16, 'pen':-4, 'pro': -6, 'atk':-4, 'dfn':-8,},
    0  :{'sight':0,   'resbio': -32, 'pen':-6, 'pro': -12, 'atk':-8, 'dfn':-16,},
    },
BP_EARS         :{
    # NOTE: same averaging system applies to ears as to eyes
    0.8:{'hearing':0.9, 'pro': -1, 'dfn':-1, 'bal':-1,},
    0.6:{'hearing':0.8, 'pro': -2, 'dfn':-2, 'bal':-2,},
    0.4:{'hearing':0.6, 'pro': -3, 'dfn':-4, 'bal':-4,},
    0.2:{'hearing':0.3, 'pro': -4, 'dfn':-6, 'bal':-6,},
    0  :{'hearing':0,   'pro': -5, 'dfn':-8, 'bal':-8,},
    },
BP_MOUTH        :{
    0.8 : {'respain':-4, 'bea':-4,},
    0.4 : {'respain':-16, 'bea':-16, 'idn':-4,},
    0   : {'respain':-64, 'bea':-64, 'idn':-16,},
    },
BP_FRONT        :{
    0.8 : {'str':-1, 'respain':-1, 'asp': -3, 'msp': -3,},
    0.6 : {'str':-2, 'respain':-2, 'asp': -6, 'msp': -6,},
    0.4 : {'str':-3, 'respain':-4, 'asp': -9, 'msp': -9,},
    0.2 : {'str':-4, 'respain':-8, 'asp': -12, 'msp': -12,},
    0   : {'str':-5, 'respain':-16, 'asp': -15, 'msp': -15,},
    },
BP_BACK         :{
    0.8 : {'con':-1, 'respain':-1, 'asp': -3, 'msp': -3,},
    0.6 : {'con':-2, 'respain':-2, 'asp': -6, 'msp': -6,},
    0.4 : {'con':-3, 'respain':-4, 'asp': -9, 'msp': -9,},
    0.2 : {'con':-4, 'respain':-8, 'asp': -12, 'msp': -12,},
    0   : {'con':-5, 'respain':-16, 'asp': -15, 'msp': -15,},
    },
BP_HIPS         :{
    0.8 : {'end':-1, 'respain':-1, 'asp': -3, 'msp': -12,},
    0.6 : {'end':-2, 'respain':-2, 'asp': -6, 'msp': -24,},
    0.4 : {'end':-3, 'respain':-4, 'asp': -12, 'msp': -36,},
    0.2 : {'end':-4, 'respain':-8, 'asp': -24, 'msp': -48,},
    0   : {'end':-5, 'respain':-16, 'asp': -36, 'msp': -64,},
    },
BP_CORE         :{
    0.8 : {'agi':-1, 'respain':-1, 'asp': -6, 'msp': -3,},
    0.6 : {'agi':-2, 'respain':-2, 'asp': -12, 'msp': -6,},
    0.4 : {'agi':-3, 'respain':-4, 'asp': -24, 'msp': -9,},
    0.2 : {'agi':-4, 'respain':-8, 'asp': -36, 'msp': -12,},
    0   : {'agi':-5, 'respain':-16, 'asp': -48, 'msp': -15,},
    },
BP_ARM          :{
    0.8 : {'dex':-1, 'respain':-1,},
    0.6 : {'dex':-2, 'respain':-2,},
    0.4 : {'dex':-3, 'respain':-4,},
    0.2 : {'dex':-4, 'respain':-8,},
    0   : {'dex':-5, 'respain':-16,},
    },
BP_LEG          :{
    0.8 : {'agi':-1, 'respain':-1, 'msp':-3,},
    0.6 : {'agi':-2, 'respain':-2, 'msp':-6,},
    0.4 : {'agi':-3, 'respain':-4, 'msp':-12,},
    0.2 : {'agi':-4, 'respain':-8, 'msp':-24,},
    0   : {'agi':-5, 'respain':-16, 'msp':-48,},
    },
BP_HAND         :{
    0.8 : {'dex':-1, 'respain':-1,},
    0.6 : {'dex':-2, 'respain':-2,},
    0.4 : {'dex':-3, 'respain':-4,},
    0.2 : {'dex':-4, 'respain':-8,},
    0   : {'dex':-5, 'respain':-16,},
    },
BP_FOOT         :{
    0.8 : {'respain':-1, 'msp':-6,},
    0.6 : {'respain':-2, 'msp':-12,},
    0.4 : {'respain':-4, 'msp':-18,},
    0.2 : {'respain':-8, 'msp':-30,},
    0   : {'respain':-16, 'msp':-60,},
    },
BP_WING         :{
    0.8 : {'flight':0.6,}, # TODO: figure this out. Can/should flight be a stat?
    0.4 : {'flight':0.2,},
    0   : {'flight':0,},
    },
BP_TAIL         :{
    0.8 : {'bal':-1,},
    0.6 : {'bal':-2,},
    0.4 : {'bal':-4,},
    0.2 : {'bal':-8,},
    0   : {'bal':-12,},
    },
BP_BEAK         :{
    0.8 : {'bea':-8, 'idn':-4,},
    0.4 : {'bea':-32, 'idn':-8,},
    0   : {'bea':-64, 'idn':-16,},
    },
BP_GENITALS     :{
    0.8 : {'respain':-32,},
    0.4 : {'respain':-64,},
    0   : {'respain':-128,},
    },
BP_APPENDAGE    :{
    0.5 : {'respain':-8,},
    0   : {'respain':-32,},
    },
BP_TENTACLE     :{
    0.8 : {'str':-1,},
    0.4 : {'str':-2,},
    0   : {'str':-3,},
    },
BP_PSEUDOPOD    :{
    0.8 : {'str':-1, 'agi':-2,},
    0.4 : {'str':-2, 'agi':-4,},
    0   : {'str':-3, 'agi':-6,},
    },
BP_AMEBOID      :{
    0.8 : {'con':-2, 'end':-2,},
    0.4 : {'con':-4, 'end':-4,},
    0   : {'con':-6, 'end':-6,},
    },
BP_MANDIBLE     :{
    0.5 : {'respain':-8,},
    0   : {'respain':-32,},
    },
BP_INSECTHEAD   :{
    0.8 : {'int':-1, 'bal':-1, 'sight':0.9,},
    0.6 : {'int':-2, 'bal':-2, 'sight':0.8,},
    0.4 : {'int':-3, 'bal':-4, 'sight':0.7,},
    0.2 : {'int':-4, 'bal':-8, 'sight':0.6,},
    0   : {'int':-5, 'bal':-16, 'sight':0.5,},
    },
BP_INSECTLEG    :{
    0.8 : {'msp':-3,},
    0.6 : {'msp':-6,},
    0.4 : {'msp':-12,},
    0.2 : {'msp':-18,},
    0   : {'msp':-24,},
    },
BP_INSECTTHORAX :{
    0.8 : {'con':-2, 'end':-2,},
    0.4 : {'con':-4, 'end':-4,},
    0   : {'con':-6, 'end':-6,},
    },
BP_INSECTABDOMEN:{
    0.8 : {'agi':-2,},
    0.4 : {'agi':-4,},
    0   : {'agi':-6,},
    },

}



#STATUSES

QUALITYMODF=-1     # flag indicates to use component quality variable instead of constant modifier

# is this a good place to put this?
# TODO: do this for all relevant statuses, apply them when status activated and remove them when deactivated
STATUS_STARVING_MULTMODS={'str':0.5,'end':0.5,}

# bodily processes
SHIVER_TEMP_GAIN = 0.1
SWEAT_TEMP_LOSS  = 0.1

# bleed
BLEED_METERLOSS = 1
BLEED_PLASTIC   = 6     # default bleed values for sharpened weapons of material types
BLEED_WOOD      = 12
BLEED_BONE      = 18
BLEED_STONE     = 18
BLEED_GLASS     = 96
BLEED_CERAMIC   = 72
BLEED_METAL     = 24
BLEED_STEEL     = 48
BLEED_GRAPHENE  = 192
BLEED_DIAMONITE = 144
BLEED_QUALITY_MINORWOUND    = 1 # suggestions for bleed quality amounts
BLEED_QUALITY_CONTUSION     = 3
BLEED_QUALITY_MULTIWOUNDS   = 5
BLEED_QUALITY_MAJORWOUND    = 8
BLEED_QUALITY_ARTERIAL      = 15

#wet
WET_RESFIRE     = 200   # fire resistance gained while wet (per liter)

# temp (burn)
FIRE_METERMAX   = 3600  #maximum temperature a thing can reach
FIRE_MAXTEMP    = 1200  #max temperature you can reach from normal means
FIRE_BURN       = 34    #heat dmg fire deals to things per turn
FIRE_PAIN       = 10    #fire hurts!
FIRE_DAMAGE     = 1     #lo dmg dealt per turn to things w/ burning status effect
FIRE_LIGHT      = 12    #how much light is produced by fire? TODO: make this depend on the heat of the fire
HOT_SPREGENMOD  = 0.5   # how fast stamina regenerates while hot
HOT_HYDRATIONLOSS = 2   # multiplier (?)


# chilly / cold
CHILLY_INTMOD       = 0.6666667
CHILLY_SPDMOD       = 0.6666667
CHILLY_STAMMOD      = 0.6666667
CHILLY_SPREGENMOD   = 0.6666667
COLD_INTMOD         = 0.3333333
COLD_SPDMOD         = 0.3333333
COLD_STAMMOD        = 0.3333333
COLD_SPREGENMOD     = 0.3333333
FROZEN_INTMOD       = 0
FROZEN_SPDMOD       = 0
FROZEN_STAMMOD      = 0.1
FROZEN_SPREGENMOD   = 0.1

# bio sick
BIO_METERLOSS   = 1     # sickness points lost per turn
SICK_STRMOD     = 0.9
SICK_ENDMOD     = 0.9
SICK_CONMOD     = 0.9
SICK_RESPAIN    = -50

# chem (exposure)
CHEM_METERLOSS  = 2     # exposure points lost per turn
CHEM_HURT       = 20    # pain chem effect causes when exposure meter fills
CHEM_DAMAGE     = 5     # damage chem effect causes when exposure meter fills

# acid
ACID_HURT       = 2
ACID_DAMAGE     = 1.0

# irritation
IRRIT_ATK       = -4
IRRIT_DFN       = -6
IRRIT_RESBLEED  = -10
IRRIT_RESPAIN   = -25
IRRIT_SIGHTMOD  = 0.75
IRRIT_HEARINGMOD= 0.75

# paralysis
PARAL_ROLLSAVE  = 10    #affects chance to undo paralysis
PARAL_SPDMOD    = 0.1
PARAL_ATK       = -15
PARAL_DFN       = -15

# cough
COUGH_CHANCE    = 33
COUGH_ATK       = -2
COUGH_DFN       = -4

# vomit
VOMIT_CHANCE    = 10

# blind
BLIND_SIGHTMOD = 0.2 # multiplier
DEAF_HEARINGMOD = 0.1 # multiplier
DISOR_SIGHTMOD = 0.6666667
DISOR_HEARINGMOD = 0.6666667
DISOR_BAL       = -5

# pain
PAIN_METERLOSS = 1
PAIN_STRMOD  = 0.8333334    # pain level: 1
PAIN_ENDMOD  = 0.8333334
PAIN_CONMOD  = 0.9
AGONY_STRMOD = 0.6666667    # pain level: 2
AGONY_ENDMOD = 0.6666667
AGONY_CONMOD = 0.75
EXCRU_STRMOD = 0.3333334    # pain level: 3
EXCRU_ENDMOD = 0.3333334
EXCRU_CONMOD = 0.5
# Pain can also K.O. you if your pain reaches MAX_PAIN, and that is
#   effectively pain level 4 -- but that doesn't directly affect stats.

# fear
FEAR_METERLOSS = 1

#hasty
HASTE_SPDMOD        = 1.5    # speed bonus when hasty (mult modifier)

#slow
SLOW_SPDMOD         = 0.6666667 # speed penalty while slowed (mult modifier)

# slow walk
SLOWWALK_MSPMOD     = 0.6666667   # move speed modifier when you walk

# powerwalk
POWERWALK_MSPMOD    = 1   # move speed modifier when you powerwalk

# jog / trot
JOG_MSPMOD          = 1.333334   # move speed modifier when you jog

# run
RUN_MSPMOD          = 1.666667   # move speed modifier when you run

#sprint
SPRINT_MSPMOD       = 2   # move speed modifier when you sprint

# drunk
DRUNK_BAL           = -0.2 # how much drunkness affects balance per quality
DRUNK_INT           = -0.1 # "                          intelligence "

# hazy
HAZY_SIGHTMOD       = 0.75
HAZY_RESPAIN        = -20
HAZY_SPREGENMOD     = 0.83
HAZY_INTMOD         = 0.75

# full
FULL_SPREGENMOD     = 0.8

# tired
TIRED_SPREGENMOD    = 0.8
TIRED_SIGHTMOD      = 0.75
TIRED_INTMOD        = 0.9

# hungry
HUNGRY_SPREGENMOD   = 0.5
HUNGRY_ENDMOD       = 0.75
HUNGRY_CONMOD       = 0.75

# emaciated
EMACI_SPREGENMOD    = 0.25
EMACI_ENDMOD        = 0.5
EMACI_CONMOD        = 0.5

# dehydrated
DEHYD_SPREGENMOD    = 0.5
DEHYD_RESFIRE       = -25
DEHYD_RESPAIN       = -25

# KO
KO_SPDMOD = 0

# trauma
#

#electricity





#
# Tiles
#


FLOOR           =   249     # centered dot
ROUGH           = 249 + 256
PIT             =   9       # big 0-looking thing
SHRUB           =   5       # club
BRAMBLE         =   6       # spade
JUNGLE          =   13      # musical note (16th note)
JUNGLE2         =   14      # musical note (8th note pair)
WALL            = ord('#')

DOORCLOSED      = ord('+')
DOOROPEN        = ord('-')
DOORCLOSED2     = ord('+') + 256
DOOROPEN2       = ord('-') + 256
LOCKEDCLOSED    = DOORCLOSED
LOCKEDOPEN      = DOOROPEN

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
T_MONEY         = ord('$')
T_TRAP          = ord('!')
T_DRUG          = ord('?')  # ("magic scroll") equivalent
T_FUNGUS        = ord('\"')
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
T_HEADWEAR      = ord('[')
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
# equip types / slots
#
# ordered: we have a slot EQ_ const followed by all EQ_ consts
# of the same type for increasing number of BPs
# main arm -> off arm -> 3rd arm -> 4th arm, etc.
# This proximity makes it easy to find EQ_ consts based on body part type
# for instance, to get the next limb, just add +1
MAXARMS=8
MAXLEGS=4
MAXILEGS=8
MAXHEADS=2
MAXIHEADS=1
MAXTENTACLES=8
MAXWINGS=2
MAXTAILS=1
i=0;
EQ_NONE     =i;i+=1; # NULL value
EQ_ABOUT    =i;i+=1; # about the body (e.g. a cloak)
EQ_MAINHANDW=i;i+=1; # W == WIELDED
EQ_OFFHANDW =i;i+=1;
EQ_3HANDW   =i;i+=1;
EQ_4HANDW   =i;i+=1;
EQ_5HANDW   =i;i+=1;
EQ_6HANDW   =i;i+=1;
EQ_7HANDW   =i;i+=1;
EQ_8HANDW   =i;i+=1; # 8 arms is the limit
EQ_MAINHAND =i;i+=1; # hand - worn
EQ_OFFHAND  =i;i+=1;
EQ_3HAND    =i;i+=1;
EQ_4HAND    =i;i+=1;
EQ_5HAND    =i;i+=1;
EQ_6HAND    =i;i+=1;
EQ_7HAND    =i;i+=1;
EQ_8HAND    =i;i+=1; # 8 arms is the limit
EQ_MAINARM  =i;i+=1; # arm worn slots
EQ_OFFARM   =i;i+=1;
EQ_3ARM     =i;i+=1;
EQ_4ARM     =i;i+=1;
EQ_5ARM     =i;i+=1;
EQ_6ARM     =i;i+=1;
EQ_7ARM     =i;i+=1;
EQ_8ARM     =i;i+=1; # 8 arms is the limit
EQ_MAINFOOT =i;i+=1; # feet
EQ_OFFFOOT  =i;i+=1;
EQ_3FOOT    =i;i+=1;
EQ_4FOOT    =i;i+=1;
EQ_MAINLEG  =i;i+=1; # legs
EQ_OFFLEG   =i;i+=1;
EQ_3LEG     =i;i+=1;
EQ_4LEG     =i;i+=1;
EQ_FRONT    =i;i+=1; # core
EQ_BACK     =i;i+=1;
EQ_HIPS     =i;i+=1;
EQ_CORE     =i;i+=1;
EQ_ABDOMEN  =i;i+=1;
EQ_MAINHEAD =i;i+=1; # head
EQ_OFFHEAD  =i;i+=1;
EQ_MAINFACE =i;i+=1;
EQ_OFFFACE  =i;i+=1;
EQ_MAINNECK =i;i+=1;
EQ_OFFNECK  =i;i+=1;
EQ_MAINEYES =i;i+=1;
EQ_OFFEYES  =i;i+=1;
EQ_MAINEARS =i;i+=1;
EQ_OFFEARS  =i;i+=1;
EQ_MAINMOUTH=i;i+=1;
EQ_OFFMOUTH =i;i+=1;
EQ_AMMO     =i;i+=1;
EQ_GENITALS =i;i+=1;
EQ_IHEAD    =i;i+=1; # insect parts (beginning w/ "I")
EQ_IMANDIBLE=i;i+=1;
EQ_ITHORAX  =i;i+=1;
EQ_IABDOMEN =i;i+=1;
EQ_IMAINLEG =i;i+=1;
EQ_IOFFLEG  =i;i+=1;
EQ_I3LEG    =i;i+=1;
EQ_I4LEG    =i;i+=1;
EQ_I5LEG    =i;i+=1;
EQ_I6LEG    =i;i+=1;
EQ_I7LEG    =i;i+=1;
EQ_I8LEG    =i;i+=1;
EQ_1TENTACLE=i;i+=1; # tentacles
EQ_2TENTACLE=i;i+=1;
EQ_3TENTACLE=i;i+=1;
EQ_4TENTACLE=i;i+=1;
EQ_5TENTACLE=i;i+=1;
EQ_6TENTACLE=i;i+=1;
EQ_7TENTACLE=i;i+=1;
EQ_8TENTACLE=i;i+=1;
EQ_1TENTACLEW=i;i+=1; # held by tentacles
EQ_2TENTACLEW=i;i+=1;
EQ_3TENTACLEW=i;i+=1;
EQ_4TENTACLEW=i;i+=1;
EQ_5TENTACLEW=i;i+=1;
EQ_6TENTACLEW=i;i+=1;
EQ_7TENTACLEW=i;i+=1;
EQ_8TENTACLEW=i;i+=1;
EQ_MAINWING =i;i+=1; # wings
EQ_OFFWING  =i;i+=1;
EQ_CELL     =i;i+=1; # other
EQ_AMEBOID  =i;i+=1;
EQ_PSEUDOPOD=i;i+=1;
EQ_1TAIL    =i;i+=1;

EQ_TYPE_STRINGS={ # used for messages
# EQ_ const :('wear/wield','preposition','generic noun','descriptive noun')
EQ_NONE     :('EQ_NONE','EQ_NONE','EQ_NONE','EQ_NONE',),
EQ_ABOUT    :('wear','about','self','self',),
EQ_MAINHANDW:('wield','in','hand','main hand',),
EQ_OFFHANDW :('wield','in','hand','off hand',),
EQ_3HANDW   :('wield','in','hand','3rd hand',),
EQ_4HANDW   :('wield','in','hand','4th hand',),
EQ_5HANDW   :('wield','in','hand','5th hand',),
EQ_6HANDW   :('wield','in','hand','6th hand',),
EQ_7HANDW   :('wield','in','hand','7th hand',),
EQ_8HANDW   :('wield','in','hand','8th hand',),
EQ_MAINHAND :('wear','on','hand','main hand',),
EQ_OFFHAND  :('wear','on','hand','off hand',),
EQ_3HAND    :('wear','on','hand','3rd hand',),
EQ_4HAND    :('wear','on','hand','4th hand',),
EQ_5HAND    :('wear','on','hand','5th hand',),
EQ_6HAND    :('wear','on','hand','6th hand',),
EQ_7HAND    :('wear','on','hand','7th hand',),
EQ_8HAND    :('wear','on','hand','8th hand',),
EQ_MAINARM  :('wear','on','hand','main arm',),
EQ_OFFARM   :('wear','on','arm','off arm',),
EQ_3ARM     :('wear','on','arm','3rd arm',),
EQ_4ARM     :('wear','on','arm','4th arm',),
EQ_5ARM     :('wear','on','arm','5th arm',),
EQ_6ARM     :('wear','on','arm','6th arm',),
EQ_7ARM     :('wear','on','arm','7th arm',),
EQ_8ARM     :('wear','on','arm','8th arm',),
EQ_MAINFOOT :('wear','on','foot','main foot',),
EQ_OFFFOOT  :('wear','on','foot','off foot',),
EQ_3FOOT    :('wear','on','foot','3rd foot',),
EQ_4FOOT    :('wear','on','foot','4th foot',),
EQ_MAINLEG  :('wear','on','leg','main leg',),
EQ_OFFLEG   :('wear','on','leg','off leg',),
EQ_3LEG     :('wear','on','leg','3rd leg',),
EQ_4LEG     :('wear','on','leg','4th leg',),
EQ_FRONT    :('wear','on','torso','chest',),
EQ_BACK     :('wear','on','torso','back',),
EQ_HIPS     :('wear','on','torso','hips',),
EQ_CORE     :('wear','on','torso','core',),
EQ_ABDOMEN  :('wear','on','abdomen','abdomen',),
EQ_MAINHEAD :('wear','on','head','main head',),
EQ_OFFHEAD  :('wear','on','head','off head',),
EQ_MAINFACE :('wear','on','face','main face',),
EQ_OFFFACE  :('wear','on','face','off face',),
EQ_MAINNECK :('wear','on','neck','main neck',),
EQ_OFFNECK  :('wear','on','neck','off neck',),
EQ_MAINEYES :('wear','on','eyes','main eyes',),
EQ_OFFEYES  :('wear','on','eyes','off eyes',),
EQ_MAINEARS :('wear','on','ears','main ears',),
EQ_OFFEARS  :('wear','on','ears','off ears',),
EQ_MAINMOUTH:('hold','in','mouth','main mouth',),
EQ_OFFMOUTH :('hold','in','mouth','off mouth',),
EQ_AMMO     :('wear','on','belt','ammo pouch',),
EQ_GENITALS :('wear','on','belt','genitals',),
EQ_IHEAD    :('wear','on','head','insect head',),
EQ_IMANDIBLE:('hold','in','mandible','insect mandible',),
EQ_ITHORAX  :('wear','on','thorax','insect thorax',),
EQ_IABDOMEN :('wear','on','abdomen','insect abdomen',),
EQ_IMAINLEG :('wear','on','leg','main leg',),
EQ_IOFFLEG  :('wear','on','leg','off leg',),
EQ_I3LEG    :('wear','on','leg','3rd leg',),
EQ_I4LEG    :('wear','on','leg','4th leg',),
EQ_I5LEG    :('wear','on','leg','5th leg',),
EQ_I6LEG    :('wear','on','leg','6th leg',),
EQ_I7LEG    :('wear','on','leg','7th leg',),
EQ_I8LEG    :('wear','on','leg','8th leg',),
EQ_1TENTACLE:('wear','on','tentacle','main tentacle',),
EQ_2TENTACLE:('wear','on','tentacle','off tentacle',),
EQ_3TENTACLE:('wear','on','tentacle','3rd tentacle',),
EQ_4TENTACLE:('wear','on','tentacle','4th tentacle',),
EQ_5TENTACLE:('wear','on','tentacle','5th tentacle',),
EQ_6TENTACLE:('wear','on','tentacle','6th tentacle',),
EQ_7TENTACLE:('wear','on','tentacle','7th tentacle',),
EQ_8TENTACLE:('wear','on','tentacle','8th tentacle',),
EQ_1TENTACLEW:('wield','in','tentacle','main tentacle',),
EQ_2TENTACLEW:('wield','in','tentacle','off tentacle',),
EQ_3TENTACLEW:('wield','in','tentacle','3rd tentacle',),
EQ_4TENTACLEW:('wield','in','tentacle','4th tentacle',),
EQ_5TENTACLEW:('wield','in','tentacle','5th tentacle',),
EQ_6TENTACLEW:('wield','in','tentacle','6th tentacle',),
EQ_7TENTACLEW:('wield','in','tentacle','7th tentacle',),
EQ_8TENTACLEW:('wield','in','tentacle','8th tentacle',),
EQ_MAINWING :('wear','on','wing','1st wing',),
EQ_OFFWING  :('wear','on','wing','2nd wing',),
EQ_CELL     :('wear','on','ameboid','cellular body',),
EQ_AMEBOID  :('wear','on','ameboid','ameboid',),
EQ_PSEUDOPOD:('hold','in','pseudopod','pseudopod',),
EQ_1TAIL    :('wear','on','tail','1st tail',),
}

# names of limbs based on index (ordering of EQ_ consts)
#   [MAINARM is first, then OFFARM, then 3ARM, etc.]
BPINDEX={
    0 : 'main',
    1 : 'off',
    2 : '3rd',
    3 : '4th',
    4 : '5th',
    5 : '6th',
    6 : '7th',
    7 : '8th',
}





#
# prefixes
#
i=1;
PREFIX_PARTIALLY_EATEN      =i;i+=1;

PREFIXES={
PREFIX_PARTIALLY_EATEN      : "partially eaten",
}




#
# genders
#
i=0;
GENDER_NONE     =i;i+=1; # for inanimate objects and genderless creatures
GENDER_MALE     =i;i+=1;
GENDER_FEMALE   =i;i+=1;
GENDER_OTHER    =i;i+=1; # nonbinary
GENDER_NEW      =i; # index for creating a new gender

GENDERS={
# gender        : (string,
#    pronouns: subject, object, possessive, generic, polite, informal,)
GENDER_NONE     : (
    "genderless",
    ('it', 'it', 'its', 'its', "thing", "thing", "thing",),),
GENDER_MALE     : (
    "male",
    ('he',  'him', 'his', 'his', "man", "sir", "guy",),),
GENDER_FEMALE   : (
    "female",
    ('she', 'her', 'her', 'hers', "woman", "madam", "girl",),),
GENDER_OTHER    : (
    "nonbinary",
    ('they','them','their','theirs',"person","individual","person",),),
}




#
# Alerts
#

ALERT_EMPTYCONTAINER    = "This container is empty."
ALERT_CANTUSE           = "You can't use that!"



#
# Times of Day
#

TIMES_OF_DAY={ # as ratios of the full length of the day
# ratio     :(actual name, colloquial name,)
0           :("midnight","morning",), # 12:00am
0.1666667   :("dusk","morning",), # 4:00am
0.25        :("morning","morning",), # 6:00am
0.48        :("noon","morning",), # ~11:30am
0.625       :("afternoon","afternoon",), # 3:00pm / 15:00
0.75        :("evening","evening",), # 6:00pm / 18:00
0.8333334   :("night","evening",), # 8:00pm / 20:00
}



#
# Tastes
#
i=1;
TASTE_NASTY     =i;i+=1;
TASTE_BITTER    =i;i+=1;
TASTE_SWEET     =i;i+=1;
TASTE_SALTY     =i;i+=1;
TASTE_SAVORY    =i;i+=1;
TASTE_BLAND     =i;i+=1;
TASTE_ACIDIC    =i;i+=1; # sour
TASTE_INEDIBLE  =i;i+=1;
TASTE_TOOSWEET  =i;i+=1;
TASTE_TOOSALTY  =i;i+=1;
TASTE_EXQUISITE =i;i+=1;
TASTE_SUPERBITTER=i;i+=1;

TASTES = {
    TASTE_INEDIBLE : "*gag* disgusting!",
    TASTE_NASTY : "yuck, that tastes nasty!",
    TASTE_BITTER : "ack, bitter.",
    TASTE_SUPERBITTER : "ack, that's extremely bitter!",
    TASTE_SWEET : "yum, sweet!",
    TASTE_TOOSWEET : "ach! Way too sweet.",
    TASTE_SALTY : "that's salty.",
    TASTE_TOOSALTY : "ack, too much salt.",
    TASTE_SAVORY : "yum, savory!",
    TASTE_EXQUISITE : "mmm... delicious!",
    TASTE_BLAND : "it's rather bland.",
    TASTE_ACIDIC : "sour!",
}





#
# Breathing statuses # Breathe statuses # Breath statuses
#

i=0;
BREATHE_NORMAL      =i;i+=1;
BREATHE_INHALING    =i;i+=1;
BREATHE_EXHALING    =i;i+=1;
BREATHE_HOLDING     =i;i+=1; # holding breath
BREATHE_HYPER       =i;i+=1; # hyperventilating





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
MAT_FLESH       =i;i+=1;
MAT_BONE        =i;i+=1;
MAT_METAL       =i;i+=1;
MAT_CARBON      =i;i+=1;
MAT_PLASTIC     =i;i+=1;
MAT_TARP        =i;i+=1;
MAT_STONE       =i;i+=1;
MAT_DUST        =i;i+=1;
MAT_WOOD        =i;i+=1;
MAT_PAPER       =i;i+=1;
MAT_LEATHER     =i;i+=1;
MAT_BLEATHER    =i;i+=1; # boiled leather
MAT_CLOTH       =i;i+=1;
MAT_ROPE        =i;i+=1;
MAT_GLASS       =i;i+=1;
MAT_RUST        =i;i+=1;
MAT_CLAY        =i;i+=1; 
MAT_CERAMIC     =i;i+=1;
MAT_QUARTZ      =i;i+=1;#silica, sand
MAT_RUBBER      =i;i+=1;
MAT_CHITIN      =i;i+=1; # fungi, arthropods, crustaceans, insects, molluscs, cephalopod beaks, fish/amphibian scales
MAT_KERATIN     =i;i+=1; # vertebrates (reptiles, birds, amphibians, mammals, spider silk)
MAT_OIL         =i;i+=1;
MAT_COPPER      =i;i+=1;
MAT_ALUMINUM    =i;i+=1;
MAT_STEEL       =i;i+=1;
MAT_DIAMOND     =i;i+=1;


##MAT_FUNGUS      =i;i+=1; #use flesh
##MAT_VEGGIE      =i;i+=1; #use wood
##MAT_SAWDUST     =i;i+=1; # just use DUST
##MAT_GUNPOWDER   =i;i+=1; # just use DUST
#
# FLUIDS are mats, too.
#
##i=1;
FL_WATER        =i;i+=1;
FL_OIL          =i;i+=1;
FL_BLOOD        =i;i+=1;
FL_ACID         =i;i+=1;
FL_STRONGACID   =i;i+=1;
FL_SMOKE        =i;i+=1;
FL_ALCOHOL      =i;i+=1;
FL_NAPALM       =i;i+=1;
FL_GASOLINE     =i;i+=1;
FL_HAZMATS      =i;i+=1;

# material names and data
MATERIALS={
    # DT : damage threshold; how much damage a generic item of this
        # material can take before breaking (independent of durability)
    # hardness: relative hardness on scale of 0-10
    # $/kg: price per kilogram (used to calculate price of crafted items)
    # value not set in stone for:
    #   paper, ceramic, chitin, keratin, copper, aluminum, water, 
    #   oil, blood, acid, strong acid, smoke, alocohol, napalm,
    #   gasoline, and hazmats.
# ID            : (name,            DT, hardness,$/kg)
MAT_FLESH       : ("flesh",         100, 0, 5,),
MAT_BONE        : ("bone",          20,  3, 4,),
MAT_METAL       : ("metal",         80,  5, 50,),
MAT_CARBON      : ("carbon",        160, 4, 10,),
MAT_PLASTIC     : ("plastic",       10,  1, 1,),
MAT_TARP        : ("tarp",          100, 0, 10,),
MAT_STONE       : ("stone",         20,  3, 1,),
MAT_DUST        : ("dust",          100, 0, 0,),
MAT_WOOD        : ("wood",          20,  1, 5,),
MAT_PAPER       : ("paper",         20,  0, 10,),
MAT_LEATHER     : ("leather",       60,  0, 10,),
MAT_BLEATHER    : ("boiled leather",30,  0, 15,),
MAT_CLOTH       : ("cloth",         100, 0, 20,),
MAT_ROPE        : ("rope",          50,  0, 20,),
MAT_GLASS       : ("glass",         10,  5, 25,),
MAT_RUST        : ("rust",          5,   2, 5,),
MAT_CLAY        : ("clay",          100, 0, 0.6666667,),
MAT_CERAMIC     : ("ceramic",       10,  9, 2,),
MAT_QUARTZ      : ("quartz",        20,  0, 5,),
MAT_RUBBER      : ("rubber",        100, 0, 20,),
MAT_CHITIN      : ("chitin",        20,  3, 10,),
MAT_KERATIN     : ("keratin",       20,  2, 5,),
MAT_COPPER      : ("copper",        40,  3, 25,),
MAT_ALUMINUM    : ("aluminum",      40,  2, 10,),
MAT_STEEL       : ("steel",         160, 6, 250,),
MAT_DIAMOND     : ("diamond",       60,  10,150,),
FL_WATER        : ("water",         999, 0, 10,),
FL_OIL          : ("oil",           999, 0, 5,),
FL_BLOOD        : ("blood",         999, 0, 400,),
FL_ACID         : ("acid",          999, 0, 5,),
FL_STRONGACID   : ("strong acid",   999, 0, 100,),
FL_SMOKE        : ("smoke",         999, 0, 0,),
FL_ALCOHOL      : ("alcohol",       999, 0, 10,),
FL_NAPALM       : ("napalm",        999, 0, 400,),
FL_GASOLINE     : ("petrol",        999, 0, 20,),
FL_HAZMATS      : ("bio-hazard",    999, 0, 0,),
}

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
##MAT_GAS         : 0,
##MAT_WATER       : 0,
##MAT_OIL         : 10,
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
MAT_CLOTH       : MAXGRIND_CLOTH,
}

# Boiling, Melting, flash (Ignition) Points
# temperature related to the points:
#   below MP, it's solid
#   between MP and BP, it's liquid
#   above BP, it's a gas
MATERIAL_PHYSICS={
# material      : (MP,  BP,  IP,)
MAT_FLESH       : (300, 900, 150,),
MAT_BONE        : (1600,9999,1500,),
MAT_METAL       : (1500,9999,9999,),
MAT_CARBON      : (4200,9999,350,),
MAT_PLASTIC     : (150, 9999,100,),
MAT_TARP        : (200, 9999,100,),
MAT_STONE       : (700, 9999,9999,),
MAT_DUST        : (9999,9999,70,),
MAT_WOOD        : (9999,9999,100,),
MAT_PAPER       : (9999,9999,80,),
MAT_LEATHER     : (9999,9999,200,),
MAT_BLEATHER    : (9999,9999,300,),
MAT_CLOTH       : (9999,9999,100,),
MAT_ROPE        : (9999,9999,200,),
MAT_GLASS       : (2200,9999,9999,),
MAT_RUST        : (1500,9999,9999,),
MAT_CLAY        : (9999,9999,9999,),
MAT_CERAMIC     : (9999,9999,9999,),
##MAT_GAS         : (9999,9999,9999,),
##MAT_WATER       : (0,   100, 9999,),
##MAT_OIL         : (20,  500, 400,),
MAT_QUARTZ      : (9999,9999,9999,),
MAT_RUBBER      : (70,  9999,300,),
}

MATERIAL_COLORS={
MAT_CLAY : 'silver',
MAT_CERAMIC : 'accent',
MAT_CLOTH : 'white',
MAT_STONE : 'gray',
MAT_PLASTIC : 'offwhite',
MAT_WOOD : 'brown',
MAT_BONE : 'bone',
MAT_METAL : 'metal',
MAT_STEEL : 'puremetal',
MAT_LEATHER : 'tan',
MAT_FLESH : 'red',
MAT_TARP : 'blue',
MAT_BLEATHER : 'dkbrown',
MAT_GLASS : 'truegreen',
MAT_RUBBER : 'magenta',
MAT_DUST : 'ltbrown',
MAT_CARBON : 'graypurple',
MAT_ROPE : 'tan',
MAT_QUARTZ : 'crystal',
}





#
# phases of matter
#
i=1;
PHASE_SOLID     =i;i+=1;
PHASE_FLUID     =i;i+=1;   # liquid and gas




#
# Armor #
#
ARMOR_SOFT = 1
ARMOR_HARD = 2

ARMOR={ # default armor types from material
MAT_FLESH       : ARMOR_SOFT,
MAT_BONE        : ARMOR_HARD,
MAT_METAL       : ARMOR_HARD,
MAT_CARBON      : ARMOR_HARD,
MAT_PLASTIC     : ARMOR_HARD,
MAT_TARP        : ARMOR_SOFT,
MAT_STONE       : ARMOR_HARD,
MAT_DUST        : ARMOR_SOFT,
MAT_WOOD        : ARMOR_HARD,
MAT_PAPER       : ARMOR_SOFT,
MAT_LEATHER     : ARMOR_SOFT,
MAT_BLEATHER    : ARMOR_SOFT,
MAT_CLOTH       : ARMOR_SOFT,
MAT_ROPE        : ARMOR_SOFT,
MAT_GLASS       : ARMOR_HARD,
MAT_RUST        : ARMOR_SOFT,
MAT_CLAY        : ARMOR_SOFT,
MAT_CERAMIC     : ARMOR_HARD,
MAT_QUARTZ      : ARMOR_HARD,
MAT_RUBBER      : ARMOR_SOFT,
MAT_CHITIN      : ARMOR_HARD,
MAT_KERATIN     : ARMOR_HARD,
MAT_OIL         : ARMOR_SOFT,
MAT_COPPER      : ARMOR_HARD,
MAT_ALUMINUM    : ARMOR_HARD,
MAT_STEEL       : ARMOR_HARD,
MAT_DIAMOND     : ARMOR_HARD,
}




#
# Elements (types of damage)
#
MIN_RES = -95   # minimum resistance

i=1;
ELEM_PHYS   =i;i+=1;
ELEM_BIO    =i;i+=1;
ELEM_RADS   =i;i+=1;
ELEM_CHEM   =i;i+=1;
ELEM_IRIT   =i;i+=1;  # irritation
ELEM_FIRE   =i;i+=1;
ELEM_COLD   =i;i+=1;
ELEM_ELEC   =i;i+=1;
ELEM_PAIN   =i;i+=1;
ELEM_BLEED  =i;i+=1;
ELEM_RUST   =i;i+=1;
ELEM_ROT    =i;i+=1;
ELEM_WET    =i;i+=1;  # water damage
ELEM_LIGHT  =i;i+=1;
ELEM_SOUND  =i;i+=1;

ELEMENTS={
ELEM_PHYS   : ('PHS','physical',),
ELEM_BIO    : ('BIO','bio-hazard',),
ELEM_RADS   : ('RAD','radiation',),
ELEM_CHEM   : ('CHM','chemical',),
ELEM_IRIT   : ('IRR','irritation',),
ELEM_FIRE   : ('FIR','heat',),
ELEM_COLD   : ('ICE','cold',),
ELEM_ELEC   : ('ELC','electricity',),
ELEM_PAIN   : ('PAI','pain',),
ELEM_BLEED  : ('BLD','bleed',),
ELEM_RUST   : ('RUS','rust',),
ELEM_ROT    : ('ROT','rot',),
ELEM_WET    : ('WET','water',),
ELEM_LIGHT  : ('LGT','light',),
ELEM_SOUND  : ('SND','sound',),
}

LIGHT_DMG_BLIND         = 1024      #2^10
LIGHT_DMG_PERMABLIND    = 32768     #2^15
LIGHT_DMG_BURN          = 4096      #2^12
SOUND_DMG_DEAFEN        = 10000


# Elemental Meters

MAX_PAIN    = 1000
MAX_BLEED   = 200
MAX_TEMP    = 999999
MIN_TEMP    = -200
MAX_SICK    = 100
MAX_EXPO    = 100
MAX_RUST    = 1000
MAX_ROT     = 1000
MAX_RADS    = 1000
MAX_FEAR    = 100
MAX_DIRT    = 100
# (max wetness depends on the item.)


RUSTEDNESS={
# amt   - rustedness amount
# sm    - stat modifier
# vm    - value modifier (value cannot go below the cost of the raw mats)
#amt : (sm,  vm,  name mod)
0.042: (0.99,0.95,"rusting",),
0.167: (0.97,0.83,"rusty",),
0.333: (0.91,0.6, "rusted",),
0.667: (0.8, 0.33,"deeply rusted",),
0.900: (0.6, 0.2, "thoroughly rusted",),
0.950: (0.3, 0.1, "fully rusted",),
1.000: (0.1, 0.04,"fully rusted",),
}
ROTTEDNESS={
# amt   - rot amount
# sm    - stat modifier
# vm    - value modifier
#amt : (sm,  vm,  name mod)
0.025: (0.98,0.8, "moldy",),
0.100: (0.9, 0.5, "rotting",),
0.333: (0.7, 0.1, "rotted",),
0.667: (0.3, 0.01,"deeply rotted",),
0.950: (0,   0.001,"thoroughly rotted",),
}
WETNESS_MAX_MATERIAL={
MAT_FLESH       : 0.01,
MAT_BONE        : 0.1,
MAT_METAL       : 0.01,
MAT_CARBON      : 0.01,
MAT_PLASTIC     : 0.01,
MAT_TARP        : 0,
MAT_STONE       : 0.1,
MAT_DUST        : 0.25,
MAT_WOOD        : 1.2,
MAT_PAPER       : 8,
MAT_LEATHER     : 0.1,
MAT_BLEATHER    : 0,
MAT_CLOTH       : 1.5,
MAT_ROPE        : 0.1,
MAT_GLASS       : 0,
MAT_RUST        : 0.1,
MAT_CLAY        : 1,
MAT_CERAMIC     : 0,
##MAT_GAS         : 1,
##MAT_WATER       : 0,
##MAT_OIL         : 0,
MAT_QUARTZ      : 0.01,
MAT_RUBBER      : 0.01,
MAT_CHITIN      : 0.01,
MAT_KERATIN     : 0.01,
}

PAIN_QUALITIES={
1 : 0.1,
2 : 0.333,
3 : 0.75,
}
DIRT_QUALITIES={
1 : 0.1,
2 : 0.333,
3 : 0.75,
}
RUST_QUALITIES={}
i=0
for k,v in RUSTEDNESS.items():
    i+=1
    RUST_QUALITIES[i] = k
ROT_QUALITIES={}
i=0
for k,v in ROTTEDNESS.items():
    i+=1
    ROT_QUALITIES[i] = k






#
# Modular parts / item mods / weapon mods / gun mods / gunmods
#
i=1;
IMOD_PISTOLSCOPE    =i;i+=1;
IMOD_RIFLESCOPE     =i;i+=1;
IMOD_SHOTGUNSCOPE   =i;i+=1;
IMOD_STRAP          =i;i+=1;
IMOD_STOCK          =i;i+=1;
IMOD_LASER          =i;i+=1;
IMOD_BAYONET        =i;i+=1;
IMOD_BIPOD          =i;i+=1;
IMOD_MAGAZINE       =i;i+=1;
IMOD_FLASHLIGHT     =i;i+=1;
IMOD_SUPPRESSOR     =i;i+=1;
IMOD_GRENADELAUNCHER=i;i+=1;



#
# Ammo types
#
i=1;
AMMO_BULLETS        =i;i+=1;  # bullets for muskets, etc.
AMMO_CANNONBALLS    =i;i+=1;  # large bullets for cannons, hand cannons, arquebuses
AMMO_SLING          =i;i+=1;  # slings/slingshots - pellets, bullets, stones
AMMO_WARARROWS      =i;i+=1;  # large heavy arrows
AMMO_ARROWS         =i;i+=1;
AMMO_BOLTS          =i;i+=1;  # crossbow bolts
AMMO_DARTS          =i;i+=1;  # blow darts
AMMO_SPEARS         =i;i+=1;
AMMO_AIRGUN         =i;i+=1;  # darts, hollowed arrows, bullets
AMMO_PERCUSSIONCAPS =i;i+=1;
AMMO_PAPERCARTRIDGES=i;i+=1;
AMMO_22LR           =i;i+=1;
AMMO_9MM            =i;i+=1;  # AKA .38 Spl
AMMO_357            =i;i+=1;  # 9mm magnum
AMMO_10MM           =i;i+=1;
AMMO_45ACP          =i;i+=1;
AMMO_44SPL          =i;i+=1;  # .44 is a larger caliber than 10mm (~11mm)
AMMO_44MAG          =i;i+=1;  # .44 magnum is more common than .44 Spl
AMMO_556            =i;i+=1;
AMMO_30CARBINE      =i;i+=1;  # 7.62x33mm
AMMO_762            =i;i+=1;  # 7.62x39mm
AMMO_308            =i;i+=1;  # 7.62x51mm
AMMO_3006           =i;i+=1;  # 7.62x63mm
AMMO_300            =i;i+=1;  # 7.62x67mm (winchester .300 magnum)
AMMO_50BMG          =i;i+=1;
AMMO_12GA           =i;i+=1;
AMMO_10GA           =i;i+=1;
AMMO_8GA            =i;i+=1;
AMMO_6GA            =i;i+=1;
AMMO_4GA            =i;i+=1;
AMMO_3GA            =i;i+=1;
AMMO_2GA            =i;i+=1;
AMMO_ELEC           =i;i+=1;  # electricity
AMMO_OIL            =i;i+=1;
AMMO_HAZMATS        =i;i+=1;
AMMO_ACID           =i;i+=1;
AMMO_CHEMS          =i;i+=1;
AMMO_ROCKETS        =i;i+=1;
AMMO_GRENADES       =i;i+=1;
AMMO_FLUIDS         =i;i+=1;  # any fluids
AMMO_FLAMMABLE      =i;i+=1;  # any flammable fluid
AMMO_ANYTHING       =i;i+=1;  # literally anything



#
# Skills SKILL CONSTANTS
#

# constants
SKILL_EFFECTIVENESS_MULTIPLIER = 0.6666667 # higher -> skills have more effect
SKILL_MAXIMUM       = 100   # max level of skills
EXP_LEVEL           = 10000  # experience needed to level up skills
EXP_DIMINISH_RATE   = 20    # you gain x less exp per level

#
# Skills IDs skills unique IDs skill unique IDs
#

i=1;
# Melee
SKL_ARMOR       =i;i+=1; #combat skill: armor wearing
SKL_UNARMORED   =i;i+=1; #combat skill: wearing no armor / light armor
SKL_COMBAT      =i;i+=1; #combat skill: melee combat (generic)
SKL_RANGED      =i;i+=1; #combat skill: ranged combat (generic)
SKL_SHIELDS     =i;i+=1; #combat skill: shields
SKL_BOXING      =i;i+=1; #combat skill: fisticuffs
SKL_WRESTLING   =i;i+=1; #combat skill: fight on ground, grappling: knocking down foes, binds, locks, mounting foes, throwing foes, and resisting grappling
SKL_BLUDGEONS   =i;i+=1; #combat skill: bludgeons (clubs, maces, batons, cudgels, spiked clubs, whips)
SKL_JAVELINS    =i;i+=1; #combat skill: 1-h spears (javelins/shortspears)
SKL_SPEARS      =i;i+=1; #combat skill: 2-h spears
SKL_POLEARMS    =i;i+=1; #combat skill: pole weapons other than spears
SKL_KNIVES      =i;i+=1; #combat skill: knives, daggers
SKL_SWORDS      =i;i+=1; #combat skill: swords, machetes
SKL_LONGSWORDS  =i;i+=1; #combat skill: 2-h swords
SKL_GREATSWORDS =i;i+=1; #combat skill: 2-h swords with reach
SKL_AXES        =i;i+=1; #combat skill: 1-h axes
SKL_GREATAXES   =i;i+=1; #combat skill: 2-h axes
SKL_HAMMERS     =i;i+=1; #combat skill: 1-h hammers
SKL_MALLETS     =i;i+=1; #combat skill: 2-h hammers
SKL_STAVES      =i;i+=1; #combat skill: bo staves, short staves
SKL_LONGSTAVES  =i;i+=1; #combat skill: quarterstaves and longstaves
SKL_BULLWHIPS   =i;i+=1; #combat skill: bullwhips
SKL_PUSHDAGGERS =i;i+=1; #combat skill: push daggers
SKL_ASSASSIN    =i;i+=1; #combat skill: killing (insta-kill attacks)
# throwing
SKL_THROWING    =i;i+=1; #throwing skill (throwing small things not foes)
##SKL_PITCHING    =i;i+=1; #throwing skill: tumbling throws (rocks, balls, grenades, etc.)
##SKL_ENDOVEREND  =i;i+=1; #throwing skill: end-over-end (axes, knives)
##SKL_SPINNING    =i;i+=1; #throwing skill: spinning (boomerangs, frisbees, shurikens, cards)
##SKL_TIPFIRST    =i;i+=1; #throwing skill: tip-first (javelins, spears, darts, swords)
# Explosives
SKL_IEDS        =i;i+=1; #explosives skill: IEDs
##SKL_EMPS        =i;i+=1; #explosives skill: EMPs
##SKL_MINES       =i;i+=1; #explosives skill: Mines
# Archery
SKL_SLINGS      =i;i+=1; #archery skill: slings and slingshots(?)
SKL_BOWS        =i;i+=1; #archery skill: bows
SKL_CROSSBOWS   =i;i+=1; #archery skill: crossbows
# Guns
SKL_CANNONS     =i;i+=1; #guns skill: cannons, hand-cannons, caplock guns
SKL_PISTOLS     =i;i+=1; #guns skill: pistols
SKL_RIFLES      =i;i+=1; #guns skill: rifles and carbines (semi-auto, burst-fire)
SKL_SHOTGUNS    =i;i+=1; #guns skill: shotguns
SKL_SMGS        =i;i+=1; #guns skill: SMGs
SKL_MACHINEGUNS =i;i+=1; #guns skill: machine guns (automatic rifles, etc.)
SKL_HEAVY       =i;i+=1; #guns skill: missiles, chem/bio/flame weapons, launchers
SKL_ENERGY      =i;i+=1; #guns skill: lasers, masers, sonic
# Physical / Technical
SKL_ATHLETE     =i;i+=1; #enables sprinting, jumping, climbing, Msp+ while crouched, prone, supine, on tough terrain (penalty to Msp is reduced, you don't actually GAIN Msp)
SKL_STEALTH     =i;i+=1; #hiding/sneaking (Msp cut to 50%, +stealth, +camo)
SKL_COMPUTERS   =i;i+=1; #technology skill (hacking, programming, etc.)
SKL_PILOT       =i;i+=1; #operating vehicles
SKL_PERSUASION  =i;i+=1; #speech skill, manipulating people
SKL_CHEMISTRY   =i;i+=1; #chemistry
SKL_SURVIVAL    =i;i+=1; #harvesting animals, plants, fungi, rocks, etc.
SKL_PERCEPTION  =i;i+=1; #how effectively you can use your senses and peripheral awareness esp. during focused work (e.g. aiming at a distant target)
SKL_LOCKPICK    =i;i+=1; #
SKL_MEDICINE    =i;i+=1; #healing using herbs, bandages, potions, etc. (healing the skin and minor damages)
SKL_SURGERY     =i;i+=1; #stiching, organ/limb removal/transplanting, repairing organs (healing major damages)
SKL_MASSAGE     =i;i+=1; #healing muscle/connective tissue using manual working of the tissue
##SKL_PERCEPTION  =i;i+=1; #hear exactly what happens, hearing range ++
# Crafting
SKL_ASSEMBLY    =i;i+=1; #crafting base skill
SKL_FIRESTARTING=i;i+=1; #starting fires
SKL_COOKING     =i;i+=1; #food prep
SKL_WOOD        =i;i+=1; #woodcraft and repairing wooden things
SKL_BONE        =i;i+=1; #bonecraft and repairing bone things
SKL_PLASTIC     =i;i+=1; #plasticraft and repairing plastic things
SKL_STONE       =i;i+=1; #stonecraft and repairing stone things
SKL_GLASS       =i;i+=1; #glasscraft
SKL_CLAY        =i;i+=1; #ceramicraft (earthenware craft, clay molding,...)
SKL_METAL       =i;i+=1; #metalcraft and repairing metal things
SKL_CERAMIC     =i;i+=1; #ceramicraft
SKL_LEATHER     =i;i+=1; #leatherworking
SKL_SEWING      =i;i+=1; #sewing cloth
SKL_BOWYER      =i;i+=1; #
SKL_FLETCHER    =i;i+=1; #
SKL_BLADESMITH  =i;i+=1; #making and repairing knives
SKL_GUNSMITH    =i;i+=1; #making and repairing guns (child of: metal, wood)
SKL_HARDWARE    =i;i+=1; #computer building and repair
SKL_MECHANIC    =i;i+=1; #machine building and repair
SKL_ARMORSMITH  =i;i+=1; #making and repairing armor
SKL_WELDING     =i;i+=1; #
SKL_TESTER1     =i;i+=1; #
SKL_TESTER2     =i;i+=1; #
SKL_TESTER3     =i;i+=1; #
##SKL_SWORDSMITH  =i;i+=1; #making and repairing swords (bladesmithing skill -- incorporated)
# Languages
##SKL_CHINESE     =i;i+=1; #related to: cantonese, tibetan, burmese
##SKL_JAPANESE    =i;i+=1; #
##SKL_HINDUSTANI  =i;i+=1; #related to: bengali, punjabi, marathi, kashmiri, nepali
##SKL_BENGALI     =i;i+=1; #related to: hindustani, punjabi, marathi, kashmiri, nepali
##SKL_ARABIC      =i;i+=1; #related to: Hebrew, Amharic, Aramaic
##SKL_MALAY       =i;i+=1; #related to: Javanese, Tagalog
##SKL_RUSSIAN     =i;i+=1; #related to: Ukrainian, Belarusian
##SKL_ENGLISH     =i;i+=1; #related to: german, dutch, frisian
##SKL_GERMAN      =i;i+=1; #related to: english
##SKL_FRENCH      =i;i+=1; #related to: portuguese, spanish, italian, romanian
##SKL_SPANISH     =i;i+=1; #related to: french, portuguese, italian, romanian
##SKL_PORTUGUESE  =i;i+=1; #related to: french, spanish, italian, romanian

##SKL_STRENGTH    =i;i+=1; #Dmg+2, can overpower similar-sized foes without strength
##SKL_PHYSIQUE    =i;i+=1; #Msp penalty for equipping gear cut in half
##SKL_POISE       =i;i+=1; #Not easily knocked down or moved
##SKL_MOBILITY    =i;i+=1; #Msp+50
##SKL_AGILITY     =i;i+=1; #DV+4, Msp+10, Asp+25
##SKL_DEXTERITY   =i;i+=1; #Atk+4, DV+2, Asp+25
##SKL_DEFENSE     =i;i+=1; #DV+2, AV+2, Pro+2
##SKL_ENDURANCE   =i;i+=1; #Lo+20
##SKL_WILLPOWER   =i;i+=1; #Hi+20

##SKL_MELEE       =i;i+=1; #melee combat root skill
##SKL_THROWING    =i;i+=1; #throwing weapons root skill
##SKL_EXPLOSIVES  =i;i+=1; #explosives root skill
##SKL_ARCHERY     =i;i+=1; #archery root skill - ranged weapons other than guns
##SKL_GUNS        =i;i+=1; #guns umbrella skill


# Combat Skills
##UMBRELLAS_COMBAT={
##SKL_MELEE       :'melee combat',
##SKL_THROWING    :'throwing',
##SKL_EXPLOSIVES  :'explosives',
##SKL_ARCHERY     :'archery',
##SKL_GUNS        :'guns',
##}




#
# Skills data skill data
#

SKILLPOINTS = 16 # max num skill pts user can distribute during chargen -- 60 is evenly divisible by 2, 3, 4, 5, and 6. (but 60 is a lot of points to distribute...)
ATTRIBUTEPOINTS = 12
STATPOINTS = 20
CHARACTERPOINTS = 4
SKILL_LEVELS_PER_SELECTION = 10
SKILL_LEVELS_JOB = 30 # starting skill level for given job
SKILL_INCREQ = 25   # how many skill levels before the skill costs 1 more skill point.

SKILL_I_COST = 0    # tuple indices for following dict values
SKILL_I_RATE = 1
SKILL_I_NAME = 2

SKILLS={ # ID : (SP, Learn_rate, name,)
    # SP = skill points required to learn (in chargen)
SKL_ARMOR       :(3,1.0,'armored combat',),
SKL_UNARMORED   :(2,1.0,'unarmored combat',),
SKL_COMBAT      :(2,1.5,'melee combat',),
SKL_RANGED      :(2,1.0,'ranged combat',),
SKL_SHIELDS     :(2,2.5,'shields',),
SKL_BOXING      :(2,1.5,'boxing',),
SKL_WRESTLING   :(2,1.5,'wrestling',),
SKL_AXES        :(1,2.0,'axes, one-handed',),
SKL_GREATAXES   :(2,1.5,'axes, two-handed',),
SKL_HAMMERS     :(1,1.5,'hammers, one-handed',),
SKL_MALLETS     :(2,1.5,'hammers, two-handed',),
SKL_JAVELINS    :(1,3.0,'spears, one-handed',),
SKL_SPEARS      :(1,4.0,'spears, two-handed',),
SKL_SWORDS      :(2,1.0,'swords, one-handed',),
SKL_LONGSWORDS  :(2,1.5,'swords, two-handed',),
SKL_STAVES      :(1,2.0,'bo staves',),
SKL_LONGSTAVES  :(1,1.5,'quarterstaves',),
SKL_POLEARMS    :(2,2.0,'polearms',),
SKL_GREATSWORDS :(3,1.0,'greatswords',),
SKL_KNIVES      :(2,1.0,'knives',),
SKL_BLUDGEONS   :(1,4.0,'bludgeons',),
SKL_BULLWHIPS   :(1,1.0,'bullwhips',),
SKL_THROWING    :(1,2.0,'throwing',),
SKL_IEDS        :(4,2.0,'explosives',), # crafting and diffusing
SKL_SLINGS      :(1,1.0,'slings',),
SKL_BOWS        :(3,1.0,'bows',),
SKL_CROSSBOWS   :(1,5.0,'crossbows',),
SKL_CANNONS     :(1,1.0,'lockguns',),
SKL_PISTOLS     :(2,2.0,'pistols',),
SKL_RIFLES      :(2,1.5,'rifles',),
SKL_SHOTGUNS    :(1,2.5,'shotguns',),
SKL_SMGS        :(2,1.25,'SMGs',),
SKL_MACHINEGUNS :(3,1.0,'machine guns',),
SKL_HEAVY       :(3,1.0,'heavy weapons',),
SKL_ENERGY      :(4,1.0,'energy weapons',),
# Physical / Technical Skills
SKL_ATHLETE     :(1,1.5,'athleticism',),
SKL_STEALTH     :(1,1.5,'sneaking',), # stealth and hiding (camo)
SKL_COMPUTERS   :(2,1.0,'computers',),
SKL_PILOT       :(2,1.0,'piloting',),
SKL_PERSUASION  :(2,1.0,'persuasion',),
SKL_CHEMISTRY   :(4,1.0,'chemistry',),
SKL_SURVIVAL    :(1,1.0,'survival',),
SKL_PERCEPTION  :(1,1.0,'perception',),
SKL_LOCKPICK    :(1,1.5,'lockpicking',),
SKL_MEDICINE    :(2,1.0,'medicine',),
SKL_SURGERY     :(3,1.0,'surgery',),
SKL_MASSAGE     :(1,1.5,'massage',),
# Crafting Skills
SKL_FIRESTARTING:(1,2.0,'fire starting',),
SKL_ASSEMBLY    :(1,2.0,'crafting',),
SKL_COOKING     :(1,1.0,'cooking',),
SKL_WOOD        :(1,2.5,'woodcraft',),
SKL_BONE        :(1,1.2,'bonecraft',),
SKL_LEATHER     :(2,1.0,'leathercraft',),
SKL_SEWING      :(1,2.0,'sewcraft',),
SKL_PLASTIC     :(1,3.0,'plasticraft',),
SKL_STONE       :(1,1.0,'stonecraft',),
SKL_CLAY        :(1,1.5,'ceramicraft',),
SKL_GLASS       :(3,1.0,'glasscraft',),
SKL_METAL       :(3,1.0,'metalcraft',),
SKL_BOWYER      :(2,1.0,'bowcraft',),
SKL_FLETCHER    :(1,1.0,'fletching',),
SKL_BLADESMITH  :(3,1.0,'bladesmithing',),
SKL_GUNSMITH    :(3,1.0,'gunsmithing',),
SKL_HARDWARE    :(2,1.0,'technosmithing',),
SKL_MECHANIC    :(2,1.0,'autosmithing',),
SKL_ARMORSMITH  :(3,1.0,'armorsmithing',),
SKL_WELDING     :(2,1.0,'welding',),
##SKL_TESTER1     :(1,1.0,'TESTER1',),
##SKL_TESTER2     :(2,1.0,'TESTER2',),
##SKL_TESTER3     :(3,1.0,'TESTER3',),
}
    

# weapons
WEAPONCLASS_CRITDAMAGE={ # damage % of target's total health on critical hit
SKL_SWORDS          : 0.4,
SKL_LONGSWORDS      : 0.4,
SKL_GREATSWORDS     : 0.3333334,
SKL_POLEARMS        : 0.3333334,
SKL_KNIVES          : 0.5,
SKL_HAMMERS         : 0.25,
SKL_MALLETS         : 0.2,
SKL_STAVES          : 0.25,
SKL_AXES            : 0.3333334,
SKL_GREATAXES       : 0.3333334,
SKL_JAVELINS        : 0.25,
SKL_SPEARS          : 0.3333334,
SKL_BLUDGEONS       : 0.25,
SKL_SHIELDS         : 0.2,
SKL_BULLWHIPS       : 0.1,
SKL_BOXING          : 0.2,
0                   : 0.1, # default
}

# weapon classifications / categories
i=0;
WPNTYPE_BLADE       =i;i+=1;
WPNTYPE_KNIFE       =i;i+=1;
WPNTYPE_HACK        =i;i+=1;
WPNTYPE_BLUNT       =i;i+=1;
WPNTYPE_STICK       =i;i+=1;
WPNTYPE_POLE        =i;i+=1;
WPNTYPE_SHIELD      =i;i+=1;
WPNTYPE_OTHER       =i;i+=1;

WEAPONCLASS_CATEGORIES={
SKL_SWORDS          : WPNTYPE_BLADE,
SKL_LONGSWORDS      : WPNTYPE_BLADE,
SKL_GREATSWORDS     : WPNTYPE_BLADE,
SKL_POLEARMS        : WPNTYPE_POLE,
SKL_KNIVES          : WPNTYPE_KNIFE,
SKL_HAMMERS         : WPNTYPE_BLUNT,
SKL_MALLETS         : WPNTYPE_BLUNT,
SKL_STAVES          : WPNTYPE_STICK,
SKL_AXES            : WPNTYPE_HACK,
SKL_GREATAXES       : WPNTYPE_HACK,
SKL_JAVELINS        : WPNTYPE_POLE,
SKL_SPEARS          : WPNTYPE_POLE,
SKL_BLUDGEONS       : WPNTYPE_BLUNT,
SKL_SHIELDS         : WPNTYPE_SHIELD,
SKL_BULLWHIPS       : WPNTYPE_OTHER,
SKL_BOXING          : WPNTYPE_OTHER,
}



# Skill data (stat modifiers gained from skills)

# misc.
SKL_ATHLETE_MSP         = 1

# ARMOR
SKLMOD_ARMOR_PRO        = 0.3       # adder modifier - per level
SKLMOD_ARMOR_AV         = 0.16666667# adder modifier - per level
SKLMOD_ARMOR_DV         = 0.16666667# adder modifier - per level
SKLMOD_UNARMORED_PRO    = 0.33333334# adder modifier - per level
SKLMOD_UNARMORED_AV     = 0.1       # adder modifier - per level
SKLMOD_UNARMORED_DV     = 0.2       # adder modifier - per level

# WEAPONS
# Multiplier per level for each weapons, and defaults
#   defaults apply for a given dict/skill if the skill has no key.
# Otherwise the value in the dict applies for that skill as a modifier
#   for growth for each skill level gained.
DEFAULT_SKLMOD_ATK   = 0.5
DEFAULT_SKLMOD_DFN   = 0.25
DEFAULT_SKLMOD_PEN   = 0.36363636 #~4/11
DEFAULT_SKLMOD_PRO   = 0.16666667
DEFAULT_SKLMOD_DMG   = 0.25
DEFAULT_SKLMOD_ARM   = 0.1
DEFAULT_SKLMOD_ASP   = 2
DEFAULT_SKLMOD_GRA   = 0.25
DEFAULT_SKLMOD_CTR   = 0.1
DEFAULT_SKLMOD_ENC   = 0.5 # greater -> skill affects Enc more. 
DEFAULT_SKLMOD_RASP  = 2
DEFAULT_SKLMOD_RNG   = 0.25
DEFAULT_SKLMOD_TRNG  = 0.5 # throwing range -- throwing skill works differently. All weapons that can be thrown act the same for throwing skill.
DEFAULT_SKLMOD_RATK  = 0.75
DEFAULT_SKLMOD_RPEN  = 0.33333334
DEFAULT_SKLMOD_RDMG  = 0.1

SKLMOD_ATK   = { # melee attack accuracy
    SKL_COMBAT      : DEFAULT_SKLMOD_ATK*0.5,
    SKL_RANGED      : 0,
    SKL_WRESTLING   : DEFAULT_SKLMOD_ATK*0.2,
    SKL_BOXING      : DEFAULT_SKLMOD_ATK*0.9,
    SKL_SHIELDS     : DEFAULT_SKLMOD_ATK*0.333334,
    SKL_BULLWHIPS   : DEFAULT_SKLMOD_ATK*1.25,
    SKL_SLINGS      : 0,
    SKL_BOWS        : 0,
    SKL_CROSSBOWS   : 0,
    SKL_CANNONS     : 0,
    SKL_PISTOLS     : 0,
    SKL_RIFLES      : 0,
    SKL_SHOTGUNS    : 0,
    SKL_SMGS        : 0,
    SKL_MACHINEGUNS : 0,
    SKL_HEAVY       : 0,
    SKL_ENERGY      : 0,
    SKL_SURGERY     : DEFAULT_SKLMOD_ATK*0.1,
}

SKLMOD_DFN   = { # Dodge Value
    SKL_COMBAT      : DEFAULT_SKLMOD_DFN*0.5,
    SKL_RANGED      : 0,
    SKL_SWORDS      : DEFAULT_SKLMOD_DFN*1.2,
    SKL_LONGSWORDS  : DEFAULT_SKLMOD_DFN*1.25,
    SKL_WRESTLING   : DEFAULT_SKLMOD_DFN*0.2,
    SKL_BOXING      : DEFAULT_SKLMOD_DFN*0.83,
    SKL_SHIELDS     : DEFAULT_SKLMOD_DFN*1.25,
    SKL_BULLWHIPS   : DEFAULT_SKLMOD_DFN*0.2,
    SKL_SLINGS      : DEFAULT_SKLMOD_DFN*0.2,
    SKL_BOWS        : DEFAULT_SKLMOD_DFN*0.4,
    SKL_CROSSBOWS   : DEFAULT_SKLMOD_DFN*0.2,
    SKL_CANNONS     : DEFAULT_SKLMOD_DFN*0.3,
    SKL_PISTOLS     : DEFAULT_SKLMOD_DFN*0.2,
    SKL_RIFLES      : DEFAULT_SKLMOD_DFN*0.05,
    SKL_SHOTGUNS    : DEFAULT_SKLMOD_DFN*0.2,
    SKL_SMGS        : DEFAULT_SKLMOD_DFN*0.2,
    SKL_MACHINEGUNS : DEFAULT_SKLMOD_DFN*0.1,
    SKL_HEAVY       : DEFAULT_SKLMOD_DFN*0.1,
    SKL_ENERGY      : DEFAULT_SKLMOD_DFN*0.1,
    SKL_SURGERY     : 0,
}

SKLMOD_PEN   = { # melee penetration
    SKL_COMBAT      : DEFAULT_SKLMOD_PEN*0.5,
    SKL_RANGED      : 0,
    SKL_WRESTLING   : 0,
    SKL_BOXING      : DEFAULT_SKLMOD_PEN*0.75,
    SKL_SHIELDS     : DEFAULT_SKLMOD_PEN*0.5,
    SKL_SWORDS      : DEFAULT_SKLMOD_PEN*1.16666667,
    SKL_LONGSWORDS  : DEFAULT_SKLMOD_PEN*1.16666667,
    SKL_KNIVES      : DEFAULT_SKLMOD_PEN*1.25,
    SKL_PUSHDAGGERS : DEFAULT_SKLMOD_PEN*1.16666667,
    SKL_SPEARS      : DEFAULT_SKLMOD_PEN*1.1,
    SKL_POLEARMS    : DEFAULT_SKLMOD_PEN*1.1,
    SKL_BLUDGEONS   : DEFAULT_SKLMOD_PEN*0.83,
    SKL_STAVES      : DEFAULT_SKLMOD_PEN*0.75,
    SKL_HAMMERS     : DEFAULT_SKLMOD_PEN*1.05,
    SKL_MALLETS     : DEFAULT_SKLMOD_PEN*0.75,
    SKL_SLINGS      : 0,
    SKL_BOWS        : 0,
    SKL_CROSSBOWS   : 0,
    SKL_CANNONS     : 0,
    SKL_PISTOLS     : 0,
    SKL_RIFLES      : 0,
    SKL_SHOTGUNS    : 0,
    SKL_SMGS        : 0,
    SKL_MACHINEGUNS : 0,
    SKL_HEAVY       : 0,
    SKL_ENERGY      : 0,
    SKL_SURGERY     : DEFAULT_SKLMOD_PEN*0.25,
}

SKLMOD_PRO   = { # protection
    SKL_COMBAT      : DEFAULT_SKLMOD_PRO*0.5,
    SKL_RANGED      : 0,
    SKL_WRESTLING   : DEFAULT_SKLMOD_PRO*0.3333334,
    SKL_BOXING      : DEFAULT_SKLMOD_PRO*0.6666667,
    SKL_SHIELDS     : DEFAULT_SKLMOD_PRO*1.1666667,
    SKL_BOWS        : DEFAULT_SKLMOD_PRO*0.05,
    SKL_CROSSBOWS   : DEFAULT_SKLMOD_PRO*0.1,
    SKL_CANNONS     : DEFAULT_SKLMOD_PRO*0.3333334,
    SKL_PISTOLS     : DEFAULT_SKLMOD_PRO*0.1,
    SKL_RIFLES      : DEFAULT_SKLMOD_PRO*0.1,
    SKL_SHOTGUNS    : DEFAULT_SKLMOD_PRO*0.25,
    SKL_SMGS        : DEFAULT_SKLMOD_PRO*0.1,
    SKL_MACHINEGUNS : DEFAULT_SKLMOD_PRO*0.25,
    SKL_HEAVY       : DEFAULT_SKLMOD_PRO*0.25,
    SKL_ENERGY      : DEFAULT_SKLMOD_PRO*0.05,
    SKL_SLINGS      : DEFAULT_SKLMOD_PRO*0.05,
    SKL_SURGERY     : 0,
}

SKLMOD_DMG   = { # melee damage
    # note 2-handed weapons get primary dmg bonus from str, not skill
    SKL_COMBAT      : DEFAULT_SKLMOD_DMG*0.25,
    SKL_RANGED      : 0,
    SKL_WRESTLING   : 0,
    SKL_BOXING      : DEFAULT_SKLMOD_DMG*0.75,
    SKL_BULLWHIPS   : DEFAULT_SKLMOD_DMG*0.5,
    SKL_SLINGS      : 0,
    SKL_BOWS        : 0,
    SKL_CROSSBOWS   : 0,
    SKL_CANNONS     : 0,
    SKL_PISTOLS     : DEFAULT_SKLMOD_DMG*0.5,
    SKL_RIFLES      : DEFAULT_SKLMOD_DMG*0.25,
    SKL_SHOTGUNS    : DEFAULT_SKLMOD_DMG*0.3333334,
    SKL_SMGS        : DEFAULT_SKLMOD_DMG*0.4,
    SKL_MACHINEGUNS : 0,
    SKL_HEAVY       : DEFAULT_SKLMOD_DMG*0.25,
    SKL_ENERGY      : 0,
    SKL_SURGERY     : DEFAULT_SKLMOD_DMG*0.25,
}

SKLMOD_ARM   = { # Armor Value
    SKL_COMBAT      : DEFAULT_SKLMOD_ARM*0.5,
    SKL_RANGED      : 0,
    SKL_WRESTLING   : DEFAULT_SKLMOD_ARM*0.05,
    SKL_BOXING      : DEFAULT_SKLMOD_ARM*0.25,
    SKL_SHIELDS     : DEFAULT_SKLMOD_ARM*1.25,
    SKL_BULLWHIPS   : DEFAULT_SKLMOD_ARM*0.05,
    SKL_SLINGS      : 0,
    SKL_BOWS        : 0,
    SKL_CROSSBOWS   : DEFAULT_SKLMOD_ARM*0.25,
    SKL_CANNONS     : DEFAULT_SKLMOD_ARM*0.5,
    SKL_PISTOLS     : DEFAULT_SKLMOD_ARM*0.3333334,
    SKL_RIFLES      : DEFAULT_SKLMOD_ARM*0.15,
    SKL_SHOTGUNS    : DEFAULT_SKLMOD_ARM*0.4,
    SKL_SMGS        : DEFAULT_SKLMOD_ARM*0.3333334,
    SKL_MACHINEGUNS : DEFAULT_SKLMOD_ARM*0.25,
    SKL_HEAVY       : DEFAULT_SKLMOD_ARM*0.25,
    SKL_ENERGY      : 0,
    SKL_SURGERY     : 0,
}

SKLMOD_ASP   = { # melee attack speed
    SKL_COMBAT      : DEFAULT_SKLMOD_ASP*0.3333334,
    SKL_RANGED      : 0,
    SKL_WRESTLING   : DEFAULT_SKLMOD_ASP*0.3333334,
    SKL_BOXING      : DEFAULT_SKLMOD_ASP*0.6666667,
    SKL_SHIELDS     : DEFAULT_SKLMOD_ASP*0.5,
    SKL_SLINGS      : DEFAULT_SKLMOD_ASP*0.5,
    SKL_CROSSBOWS   : DEFAULT_SKLMOD_ASP*0.5,
    SKL_CANNONS     : DEFAULT_SKLMOD_ASP*0.5,
    SKL_PISTOLS     : DEFAULT_SKLMOD_ASP*0.5,
    SKL_RIFLES      : DEFAULT_SKLMOD_ASP*0.5,
    SKL_SHOTGUNS    : DEFAULT_SKLMOD_ASP*0.5,
    SKL_SMGS        : DEFAULT_SKLMOD_ASP*0.5,
    SKL_MACHINEGUNS : DEFAULT_SKLMOD_ASP*0.5,
    SKL_HEAVY       : DEFAULT_SKLMOD_ASP*0.5,
    SKL_ENERGY      : DEFAULT_SKLMOD_ASP*0.5,
    SKL_SURGERY     : DEFAULT_SKLMOD_ASP*0.25,
}

SKLMOD_GRA   = { # grappling
    SKL_COMBAT      : DEFAULT_SKLMOD_GRA*0.25,
    SKL_RANGED      : 0,
    SKL_WRESTLING   : DEFAULT_SKLMOD_GRA*4,
    SKL_BOXING      : DEFAULT_SKLMOD_GRA*0.75,
    SKL_BULLWHIPS   : 0,
    SKL_BLUDGEONS   : DEFAULT_SKLMOD_GRA*0.4,
    SKL_PUSHDAGGERS : DEFAULT_SKLMOD_GRA*0.2,
    SKL_POLEARMS    : DEFAULT_SKLMOD_GRA*0.3333334,
    SKL_GREATSWORDS : DEFAULT_SKLMOD_GRA*0.6,
    SKL_MALLETS     : DEFAULT_SKLMOD_GRA*0.3,
    SKL_GREATAXES   : DEFAULT_SKLMOD_GRA*0.5,
    SKL_SPEARS      : DEFAULT_SKLMOD_GRA*0.3,
    SKL_BOWS        : 0,
    SKL_CROSSBOWS   : 0,
    SKL_CANNONS     : 0,
    SKL_PISTOLS     : DEFAULT_SKLMOD_GRA*0.5,
    SKL_RIFLES      : 0,
    SKL_SHOTGUNS    : DEFAULT_SKLMOD_GRA*0.25,
    SKL_SMGS        : DEFAULT_SKLMOD_GRA*0.4,
    SKL_MACHINEGUNS : 0,
    SKL_HEAVY       : 0,
    SKL_ENERGY      : 0,
    SKL_SLINGS      : 0,
    SKL_SURGERY     : 0,
}

SKLMOD_CTR   = { # counter-attack
    SKL_COMBAT      : DEFAULT_SKLMOD_CTR*0.5,
    SKL_RANGED      : 0,
    SKL_WRESTLING   : DEFAULT_SKLMOD_CTR*0.25,
    SKL_BOXING      : DEFAULT_SKLMOD_CTR*0.5,
    SKL_KNIVES      : DEFAULT_SKLMOD_CTR*1.5,
    SKL_SWORDS      : DEFAULT_SKLMOD_CTR*1.25,
    SKL_LONGSWORDS  : DEFAULT_SKLMOD_CTR*1.1,
    SKL_BOWS        : 0,
    SKL_CROSSBOWS   : 0,
    SKL_CANNONS     : 0,
    SKL_PISTOLS     : 0,
    SKL_RIFLES      : 0,
    SKL_SHOTGUNS    : 0,
    SKL_SMGS        : 0,
    SKL_MACHINEGUNS : 0,
    SKL_HEAVY       : 0,
    SKL_ENERGY      : 0,
    SKL_SLINGS      : 0,
    SKL_SURGERY     : DEFAULT_SKLMOD_CTR*0.1,
}

SKLMOD_RASP={ # ranged attack speed
    SKL_COMBAT      : 0,
    SKL_RANGED      : DEFAULT_SKLMOD_RASP*0.5,
    SKL_SHIELDS     : 0,
    SKL_BOXING      : 0,
    SKL_WRESTLING   : 0,
    SKL_BLUDGEONS   : 0,
    SKL_JAVELINS    : 0,
    SKL_SPEARS      : 0,
    SKL_POLEARMS    : 0,
    SKL_KNIVES      : 0,
    SKL_SWORDS      : 0,
    SKL_LONGSWORDS  : 0,
    SKL_GREATSWORDS : 0,
    SKL_AXES        : 0,
    SKL_GREATAXES   : 0,
    SKL_HAMMERS     : 0,
    SKL_MALLETS     : 0,
    SKL_STAVES      : 0,
    SKL_BULLWHIPS   : 0,
    SKL_PUSHDAGGERS : 0,
    SKL_SURGERY     : 0,
    SKL_SLINGS      : DEFAULT_SKLMOD_RASP*1.2, # slings have very low base Asp
    SKL_BOWS        : DEFAULT_SKLMOD_RASP*1,
    SKL_CROSSBOWS   : DEFAULT_SKLMOD_RASP*0.75,
    SKL_CANNONS     : DEFAULT_SKLMOD_RASP*0.5,
    SKL_PISTOLS     : DEFAULT_SKLMOD_RASP*1.1,
    SKL_RIFLES      : DEFAULT_SKLMOD_RASP*0.75,
    SKL_SHOTGUNS    : DEFAULT_SKLMOD_RASP*0.75,
    SKL_SMGS        : DEFAULT_SKLMOD_RASP*1.1,
    SKL_MACHINEGUNS : DEFAULT_SKLMOD_RASP*0.5,
    SKL_HEAVY       : DEFAULT_SKLMOD_RASP*0.5,
    SKL_ENERGY      : DEFAULT_SKLMOD_RASP*1,
}

DEFAULT_SKLMOD_RNG={ # max range
    SKL_COMBAT      : 0,
    SKL_RANGED      : DEFAULT_SKLMOD_RNG*0.5,
    SKL_SHIELDS     : 0,
    SKL_BOXING      : 0,
    SKL_WRESTLING   : 0,
    SKL_BLUDGEONS   : 0,
    SKL_JAVELINS    : 0,
    SKL_SPEARS      : 0,
    SKL_POLEARMS    : 0,
    SKL_KNIVES      : 0,
    SKL_SWORDS      : 0,
    SKL_LONGSWORDS  : 0,
    SKL_GREATSWORDS : 0,
    SKL_AXES        : 0,
    SKL_GREATAXES   : 0,
    SKL_HAMMERS     : 0,
    SKL_MALLETS     : 0,
    SKL_STAVES      : 0,
    SKL_BULLWHIPS   : 0,
    SKL_PUSHDAGGERS : 0,
    SKL_SURGERY     : 0,
    SKL_SLINGS      : DEFAULT_SKLMOD_RNG*1.3333334,
    SKL_BOWS        : DEFAULT_SKLMOD_RNG*1.3333334,
    SKL_CROSSBOWS   : DEFAULT_SKLMOD_RNG*0.9,
    SKL_CANNONS     : DEFAULT_SKLMOD_RNG*1.5,
    SKL_PISTOLS     : DEFAULT_SKLMOD_RNG*1.25,
    SKL_RIFLES      : DEFAULT_SKLMOD_RNG*1.6666667,
    SKL_SHOTGUNS    : DEFAULT_SKLMOD_RNG*0.8333334,
    SKL_SMGS        : DEFAULT_SKLMOD_RNG*0.9,
    SKL_MACHINEGUNS : DEFAULT_SKLMOD_RNG*1.4,
    SKL_HEAVY       : DEFAULT_SKLMOD_RNG*0.8333334,
    SKL_ENERGY      : DEFAULT_SKLMOD_RNG*1.05,
}

SKLMOD_RATK={ # ranged accuracy
    SKL_COMBAT      : 0,
    SKL_RANGED      : DEFAULT_SKLMOD_RATK*0.5,
    SKL_SHIELDS     : 0,
    SKL_BOXING      : 0,
    SKL_WRESTLING   : 0,
    SKL_BLUDGEONS   : 0,
    SKL_JAVELINS    : 0,
    SKL_SPEARS      : 0,
    SKL_POLEARMS    : 0,
    SKL_KNIVES      : 0,
    SKL_SWORDS      : 0,
    SKL_LONGSWORDS  : 0,
    SKL_GREATSWORDS : 0,
    SKL_AXES        : 0,
    SKL_GREATAXES   : 0,
    SKL_HAMMERS     : 0,
    SKL_MALLETS     : 0,
    SKL_STAVES      : 0,
    SKL_BULLWHIPS   : 0,
    SKL_PUSHDAGGERS : 0,
    SKL_SURGERY     : 0,
    SKL_SLINGS      : DEFAULT_SKLMOD_RATK*1.3333334,
    SKL_BOWS        : DEFAULT_SKLMOD_RATK*1.25,
    SKL_CROSSBOWS   : DEFAULT_SKLMOD_RATK*0.9,
    SKL_CANNONS     : DEFAULT_SKLMOD_RATK*0.5,
    SKL_PISTOLS     : DEFAULT_SKLMOD_RATK*1.1,
    SKL_RIFLES      : DEFAULT_SKLMOD_RATK*1.5,
    SKL_SHOTGUNS    : DEFAULT_SKLMOD_RATK*0.75,
    SKL_SMGS        : DEFAULT_SKLMOD_RATK*0.8333334,
    SKL_MACHINEGUNS : DEFAULT_SKLMOD_RATK*1,
    SKL_HEAVY       : DEFAULT_SKLMOD_RATK*0.6666667,
    SKL_ENERGY      : DEFAULT_SKLMOD_RATK*1.05,
}

DEFAULT_SKLMOD_RDMG={ # ranged damage
    SKL_COMBAT      : 0,
    SKL_RANGED      : DEFAULT_SKLMOD_RDMG*0.5,
    SKL_SHIELDS     : 0,
    SKL_BOXING      : 0,
    SKL_WRESTLING   : 0,
    SKL_BLUDGEONS   : 0,
    SKL_JAVELINS    : 0,
    SKL_SPEARS      : 0,
    SKL_POLEARMS    : 0,
    SKL_KNIVES      : 0,
    SKL_SWORDS      : 0,
    SKL_LONGSWORDS  : 0,
    SKL_GREATSWORDS : 0,
    SKL_AXES        : 0,
    SKL_GREATAXES   : 0,
    SKL_HAMMERS     : 0,
    SKL_MALLETS     : 0,
    SKL_STAVES      : 0,
    SKL_BULLWHIPS   : 0,
    SKL_PUSHDAGGERS : 0,
    SKL_SURGERY     : 0,
    SKL_SLINGS      : DEFAULT_SKLMOD_RDMG*1.1,
    SKL_BOWS        : DEFAULT_SKLMOD_RDMG*1.1,
    SKL_CROSSBOWS   : DEFAULT_SKLMOD_RDMG*0.9,
    SKL_CANNONS     : DEFAULT_SKLMOD_RDMG*1.5,
    SKL_PISTOLS     : DEFAULT_SKLMOD_RDMG*1,
    SKL_RIFLES      : DEFAULT_SKLMOD_RDMG*1.25,
    SKL_SHOTGUNS    : DEFAULT_SKLMOD_RDMG*1,
    SKL_SMGS        : DEFAULT_SKLMOD_RDMG*1,
    SKL_MACHINEGUNS : DEFAULT_SKLMOD_RDMG*1,
    SKL_HEAVY       : DEFAULT_SKLMOD_RDMG*0.5,
    SKL_ENERGY      : 0,
}

DEFAULT_SKLMOD_RPEN={ # ranged penetration
    SKL_COMBAT      : 0,
    SKL_RANGED      : DEFAULT_SKLMOD_RPEN*0.5,
    SKL_SHIELDS     : 0,
    SKL_BOXING      : 0,
    SKL_WRESTLING   : 0,
    SKL_BLUDGEONS   : 0,
    SKL_JAVELINS    : 0,
    SKL_SPEARS      : 0,
    SKL_POLEARMS    : 0,
    SKL_KNIVES      : 0,
    SKL_SWORDS      : 0,
    SKL_LONGSWORDS  : 0,
    SKL_GREATSWORDS : 0,
    SKL_AXES        : 0,
    SKL_GREATAXES   : 0,
    SKL_HAMMERS     : 0,
    SKL_MALLETS     : 0,
    SKL_STAVES      : 0,
    SKL_BULLWHIPS   : 0,
    SKL_PUSHDAGGERS : 0,
    SKL_SURGERY     : 0,
    SKL_SLINGS      : DEFAULT_SKLMOD_RPEN*0.75,
    SKL_BOWS        : DEFAULT_SKLMOD_RPEN*1.05,
    SKL_CROSSBOWS   : DEFAULT_SKLMOD_RPEN*0.9,
    SKL_CANNONS     : DEFAULT_SKLMOD_RPEN*0.6666667,
    SKL_PISTOLS     : DEFAULT_SKLMOD_RPEN*1.1,
    SKL_RIFLES      : DEFAULT_SKLMOD_RPEN*1.3333334,
    SKL_SHOTGUNS    : DEFAULT_SKLMOD_RPEN*0.8333334,
    SKL_SMGS        : DEFAULT_SKLMOD_RPEN*0.9,
    SKL_MACHINEGUNS : DEFAULT_SKLMOD_RPEN*1.25,
    SKL_HEAVY       : DEFAULT_SKLMOD_RPEN*0.75,
    SKL_ENERGY      : 0,
}

COMBATSKILLS=set((
    SKL_COMBAT,SKL_SHIELDS,SKL_BOXING,SKL_WRESTLING,SKL_BLUDGEONS,
    SKL_JAVELINS,SKL_SPEARS,SKL_POLEARMS,SKL_KNIVES,SKL_SWORDS,
    SKL_LONGSWORDS,SKL_GREATSWORDS,SKL_AXES,SKL_GREATAXES,SKL_HAMMERS,
    SKL_MALLETS,SKL_STAVES,SKL_BULLWHIPS,SKL_PUSHDAGGERS,SKL_SURGERY,
    ))
RANGEDSKILLS=set((
    SKL_SLINGS,SKL_BOWS,SKL_CROSSBOWS,SKL_CANNONS,SKL_PISTOLS,
    SKL_RIFLES,SKL_SHOTGUNS,SKL_SMGS,SKL_MACHINEGUNS,SKL_HEAVY,
    SKL_ENERGY,
    ))



    #---------------#
    #    #Combat    #
    #---------------#

i=1;    
DMGTYPE_CUT         = i; i += 1;
DMGTYPE_HACK        = i; i += 1;
DMGTYPE_BLUNT       = i; i += 1;
DMGTYPE_SPIKES      = i; i += 1;
DMGTYPE_STUDS       = i; i += 1; # small spikes / flanges
DMGTYPE_BURN        = i; i += 1;
DMGTYPE_ABRASION    = i; i += 1;
DMGTYPE_PIERCE      = i; i += 1;

DMGTYPES={ # default damage types for specific weapon classes
SKL_SHIELDS     : DMGTYPE_BLUNT,
SKL_BOXING      : DMGTYPE_BLUNT,
SKL_WRESTLING   : DMGTYPE_BLUNT,
SKL_AXES        : DMGTYPE_HACK,
SKL_GREATAXES   : DMGTYPE_HACK,
SKL_HAMMERS     : DMGTYPE_BLUNT,
SKL_MALLETS     : DMGTYPE_BLUNT,
SKL_JAVELINS    : DMGTYPE_PIERCE,
SKL_SPEARS      : DMGTYPE_PIERCE,
SKL_SWORDS      : DMGTYPE_CUT,
SKL_LONGSWORDS  : DMGTYPE_CUT,
SKL_POLEARMS    : DMGTYPE_HACK,
SKL_GREATSWORDS : DMGTYPE_CUT,
SKL_KNIVES      : DMGTYPE_CUT,
SKL_BLUDGEONS   : DMGTYPE_BLUNT,
SKL_STAVES      : DMGTYPE_BLUNT,
SKL_BULLWHIPS   : DMGTYPE_ABRASION,
# all ranged weapons == blunt melee weapons.
    # ranged damage type depends on the ammunition.
SKL_SLINGS      : DMGTYPE_BLUNT,
SKL_BOWS        : DMGTYPE_BLUNT,
SKL_CROSSBOWS   : DMGTYPE_BLUNT,
SKL_CANNONS     : DMGTYPE_BLUNT,
SKL_PISTOLS     : DMGTYPE_BLUNT,
SKL_RIFLES      : DMGTYPE_BLUNT,
SKL_SHOTGUNS    : DMGTYPE_BLUNT,
SKL_SMGS        : DMGTYPE_BLUNT,
SKL_MACHINEGUNS : DMGTYPE_BLUNT,
SKL_HEAVY       : DMGTYPE_BLUNT,
SKL_ENERGY      : DMGTYPE_BLUNT,
}



#
# Classes
#
# includes all jobs, even non-playable jobs
i=1;
CLS_ENGINEER    =i;i+=1;
CLS_TECHNICIAN  =i;i+=1;
CLS_SECURITY    =i;i+=1;
CLS_ATHLETE     =i;i+=1;
CLS_PILOT       =i;i+=1;
CLS_SMUGGLER    =i;i+=1;
CLS_CHEMIST     =i;i+=1;
CLS_POLITICIAN  =i;i+=1;
CLS_RIOTPOLICE  =i;i+=1;
CLS_JANITOR     =i;i+=1;
CLS_DEPRIVED    =i;i+=1;
CLS_SOLDIER     =i;i+=1;
CLS_THIEF       =i;i+=1;
CLS_ACROBAT     =i;i+=1;
CLS_WRESTLER    =i;i+=1;
CLS_DOCTOR      =i;i+=1;
CLS_PROGRAMMER  =i;i+=1;
CLS_MONK        =i;i+=1;
CLS_BOUNTYHUNTER=i;i+=1;
CLS_ARMORSMITH  =i;i+=1;
CLS_MECHANIC    =i;i+=1;
CLS_BLADESMITH  =i;i+=1;

CLASSES={ # colloquial names (not true titles)
CLS_ENGINEER    : "Engineer",
CLS_TECHNICIAN  : "Technician",
CLS_SECURITY    : "Security Guard",
CLS_ATHLETE     : "Olympian",
CLS_PILOT       : "Driver",
CLS_SMUGGLER    : "Smuggler",
CLS_CHEMIST     : "Scientist",
CLS_POLITICIAN  : "Politician",
CLS_RIOTPOLICE  : "Officer",
CLS_JANITOR     : "Janitor",
CLS_DEPRIVED    : "Hobo",
CLS_SOLDIER     : "Marine",
CLS_THIEF       : "Thief",
CLS_ACROBAT     : "Juggler",
CLS_WRESTLER    : "Grappler",
CLS_DOCTOR      : "Doctor",
CLS_PROGRAMMER  : "Techwizard",
CLS_MONK        : "Bowlhead",
CLS_BOUNTYHUNTER: "Bounty Hunter",
CLS_ARMORSMITH  : "Armorsmithy",
CLS_MECHANIC    : "Mechanic",
CLS_BLADESMITH  : "Bladesmithy",
}
JOBDESCRIPTIONS={
CLS_TECHNICIAN  : "Computer technician, skilled in machine building and repair.",
CLS_SECURITY    : "A security officer, trained to subdue with nonlethal force.",
CLS_ATHLETE     : "Gold medal winner. Extremely well-toned and naturally swift.",
CLS_PILOT       : "A seasoned pilot with over 10,000 hours in the air.",
CLS_SMUGGLER    : "Smooth-talking scoundrel. Skilled pilot and gunslinger.",
CLS_CHEMIST     : "A master chemist, brilliant and hardworking in their field.",
CLS_POLITICIAN  : "An outspoken politician. Starts the game with a significant amount of money, fame, and infamy.",
CLS_RIOTPOLICE  : "Drilled like a soldier. The badge behind the mask.",
CLS_JANITOR     : "A lowly janitor. No outstanding qualities.",
CLS_DEPRIVED    : "Wretched, lacking creature, born into filth and poverty.",
CLS_SOLDIER     : "Hardened marine. Skilled in heavy rifle combat.",
CLS_THIEF       : "Skilled burglar. Can easily manage heavy loads.",
CLS_WRESTLER    : "A professional grappler with a promising career.",
CLS_DOCTOR      : "Ph.D in medicine. Also skilled in surgery.",
CLS_PROGRAMMER  : "Hacker. Programmer. Geek. Computer wizard.",
CLS_MONK        : "Highly perceptive and courageous. A master of unarmored, nonlethal combat.",
CLS_BOUNTYHUNTER: "Makes a living killing outlaws. Skilled in the hunting art.",
CLS_ARMORSMITH  : "Skilled artisan. Trained in all manner of armor-making; also versed in armored combat.",
CLS_MECHANIC    : "Handy with a torque wrench.",
CLS_BLADESMITH  : "Skilled artisan. Trained in bladesmithing as well as the martial art of the blade.",
CLS_ENGINEER    : "DESCRIPTION",
CLS_ACROBAT     : "DESCRIPTION",
}





#
# Chargen
#

# constants
TALENTED_EXPMOD=1.25
FASTLEARNER_EXPMOD=1.1

# Characteristics / traits / "perks"
CHARACTERISTICS={
    # CP: character points, how many points are gained/lost by
    #    choosing a particular characteristic/trait
    # stat mods beginning with "m" signify that it's a multiplier value
    #    otherwise, by default, all stat mods are adders.
# name                  : (CP, info)
"ugly"                  : (1, {'bea':-64,},),
"timid"                 : (1, {'cou':-64,},),
"feeble"                : (1, {'idn':-64,},),
"long bones"            : (-2,{'mcm':1.34,'mreach':1.25,'mmsp':1.2,},),
"masculine"             : (-2,{'cou':16,'idn':16,'str':2,'con':2,},),
"feminine"              : (-2,{'bea':32,'end':2,'agi':2,},),
"hemophilia"            : (2, {'resbleed':-50,},),
"HIV"                   : (2, {'resbio':-75,},),
"acclimated to heat"    : (-2,{'resheat':50,},),
"acclimated to cold"    : (-2,{'rescold':50,},),
"pain tolerance"        : (-2,{'respain':100,},),
"strong immune system"  : (-2,{'resbio':75,},),
"immune to pain"        : (-2,{'immunePain':True,},),
"immune to venom"       : (-2,{'immuneVenom':True},),
"immune to poison"      : (-2,{'immunePoison':True},),
"rapid metabolism"      : (-2,{'rapidMetabolism':True,},),
"iron gut"              : (-2,{'ironGut':True,},),
"talented"              : (-2,{'talent':True,},),
"fast learner"          : (-4,{'fastLearner':True,},),
"attracted to men"      : (1, {'attractedMen':True,},),
"attracted to women"    : (1, {'attractedWomen':True,},),
"hydrophobia"           : (2, {'hydrophobia':True,},),
"cancer"                : (8, {'cancer':True,},),
"traumatic childhood"   : (4, {'trauma':True,},),
"addiction"             : (4, {'addict':True,},),
"allergy"               : (1, {'allergy':True,},),
"scarred"               : (1, {'scarred':True,},),
"dwarf"                 : (2, {"mcm":0.75,"mreach":0.75,'mmsp':0.83,},),
"obese"                 : (2, {"mmass":1.75,"fat":5,"mfat":2,"end":-2,},),
"gaunt"                 : (1, {"mmass":0.8,"mfat":0.5,"end":-2,},),
"astigmatism"           : (2, {'mvision':0.5,'astigmatism':True,},),
"big stomach"           : (-2,{'mgut':3},), # stomach capacity
"wealthy upbringing"    : (-8,{'money':5000,},),
"apprentice"            : (-8,{"skillPts":SKILLPOINTS,},),
"natural physique"      : (-8,{"statPts":STATPOINTS,},),
"genetically engineered": (-8,{"attPts":ATTRIBUTEPOINTS,},),
"educated"              : (-4,{'identify':20,},),
}

CHARACTERISTICS_DESCRIPT={ # TODO: apply these when selecting traits in chargen. Input wait w/ y/n option like "do you want to select this trait?" confirmation
    # TODO: do a similar thing for class selection as well, to give context for what each class is good at / shortcomings etc.
"ugly"                  : '''beauty is significantly reduced''',
"timid"                 : '''courage is significantly reduced''',
"feeble"                : '''intimidation is significantly reduced''',
"long bones"            : '''much taller; more reach; faster movement speed''',
"masculine"             : '''increased courage, intimidation, strength, and constitution''',
"feminine"              : '''increased beauty, endurance, and agility''',
"acclimated to heat"    : '''increased resistance to heat''',
"acclimated to cold"    : '''increased resistance to cold''',
"pain tolerance"        : '''increased resistance to pain''',
"strong immune system"  : '''increased resistance to bio-hazards''',
"big stomach"           : '''larger stomach capacity''',
"wealthy upbringing"    : '''start with extra money''',
"apprentice"            : '''gain {} extra skill points'''.format(
    CHARACTERISTICS["apprentice"][1]['skillPts']),
"natural physique"      : '''gain {} extra stat points'''.format(
    CHARACTERISTICS["natural physique"][1]['statPts']),
"genetically engineered": '''gain {} extra attribute points'''.format(
    CHARACTERISTICS["genetically engineered"][1]['attPts']),
"educated"              : '''increased identify stat''',
"rapid metabolism"      : '''gain energy/water from consumed food and fluids more rapidly; gain overall less energy/water''',
"iron gut"              : '''increased resistance to ingested poisons''',
"pain tolerance"        : '''increased resistance to pain''',
"strong immune system"  : '''increased resistance to bio-hazards''',
"hemophilia"            : '''decreased resistance to bleeding''',
"HIV"                   : '''decreased resistance to bio-hazards''',
"immune to pain"        : '''pain has no effect on you''',
"immune to venom"       : '''injected venoms have no effect on you''',
"immune to poison"      : '''ingested poisons have no effect on you''',
"talented"              : '''<choose> talented in one chosen skill, for which you gain experience more rapidly''',
"fast learner"          : '''gain experience more rapidly in all skills''',
"dwarf"                 : '''much shorter; less reach; slower movement speed''',
"obese"                 : '''much fatter and more massive; also reduces endurance''',
"gaunt"                 : '''greatly reduced bodyfat and overall body mass; also reduces endurance''',
"astigmatism"           : '''reduced vision while not wearing glasses that are fitted to your eyes''',
"attracted to men"      : '''you have a weakness for men; penalty to all rolls against men (persuasion rolls, attack rolls, etc.)''',
"attracted to women"    : '''you have a weakness for women; penalty to all rolls against women (persuasion rolls, attack rolls, etc.)''',
"hydrophobia"           : '''deathly afraid of water''',
"scarred"               : '''you sport a nasty scar on chosen body part(s); stat changes to intimidation and beauty''',
"cancer"                : '''you have cancer, and in order to remain healthy you must receive regular treatments.
These can result in negative side effects''',
"traumatic childhood"   : '''<choose> adds one chosen mental illness.
Mental illnesses vary wildly in effects, and can be debilitating, though they can be treated with medication''',
"addiction"             : '''<choose> you require regular doses of a chosen drug class in order to avoid withdrawal''',
"allergy"               : '''<choose> you are allergic to one chosen class of allergens.
Contact with items of this class will result in irritation (bio damage) to the afflicted tissue''',
}

CHAR_SCARRED=( # where are you scarred?
'chest','back','leg','arm','head','face',
    )

CHARGEN_STATS={ # chargen stats changes when choosing stats in chargen
# stat  : add,
"hpmax"     : 1,
"mpmax"     : 10,
"encmax"    : 3,
"asp"       : 2,
"msp"       : 1,
"bal"       : 1*MULT_STATS,
"ctr"       : 1*MULT_STATS,
"cou"       : 4,
"bea"       : 4,
"idn"       : 4,
"camo"      : 1,
"stealth"   : 1,
}

CHARGEN_ATTRIBUTES={
# if x >= current value : cost to upgrade +1
"str":{
    0 : 1,
    20 : 2,
    30 : 3,
    40 : 4,
},
"end":{
    0 : 1,
    20 : 2,
    30 : 3,
    40 : 4,
},
"dex":{
    0 : 1,
    20 : 2,
    30 : 3,
    40 : 4,
},
"agi":{
    0 : 1,
    15 : 2,
    20 : 3,
    25 : 4,
    30 : 5,
},
"int":{
    0 : 1,
    16 : 2,
    20 : 3,
    24 : 4,
    28 : 5,
},
"con":{
    0 : 1,
    16 : 2,
    20 : 3,
    24 : 4,
    28 : 5,
},
}


#
# Species
#
i=1;
SPECIE_HUMAN    =i;i+=1;
SPECIE_MUTANT   =i;i+=1;
SPECIE_CHIMERA  =i;i+=1;
SPECIE_DOG      =i;i+=1;
SPECIE_CAT      =i;i+=1;
SPECIE_HORSE    =i;i+=1;
SPECIE_MANTIS   =i;i+=1;

SPECIES={
SPECIE_HUMAN    :"human",
SPECIE_MUTANT   :"mutant",
SPECIE_CHIMERA  :"chimera",
SPECIE_DOG      :"dog",
SPECIE_CAT      :"cat",
SPECIE_HORSE    :"horse",
SPECIE_MANTIS   :"mantis",
}


#
# Factions
# flags used for diplomacy
#
i=1;
FACT_ROGUE      =i;i+=1;
FACT_CITIZENS   =i;i+=1;
FACT_DEPRIVED   =i;i+=1;
FACT_ELITE      =i;i+=1;
FACT_WATCH      =i;i+=1;
FACT_MONSTERS   =i;i+=1;
#FACT_      =i;i+=1;

FACTIONS={
FACT_ROGUE      : "rogue",
FACT_CITIZENS   : "neutral",
FACT_DEPRIVED   : "deprived",
FACT_ELITE      : "elite",
FACT_WATCH      : "watch",
FACT_MONSTERS   : "unaligned",
}

DIPLOMACY={
    #Factions:
    #(Rogue,Citizens,Deprived,Elite,Watch,Abominations,)
    FACT_ROGUE      : (1,1,1,0,0,0,),
    FACT_CITIZENS   : (1,1,0,0,0,0,),
    FACT_DEPRIVED   : (1,0,1,0,0,0,),
    FACT_ELITE      : (0,1,0,1,1,0,),
    FACT_WATCH      : (0,1,0,1,1,0,),
    FACT_MONSTERS   : (0,0,0,0,0,1,),
}





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
NOISE_CLATTER   = "the kind of clattering that causes concern"

                # vol, superHearing, generic sound
SND_FIRE        = (40, "a fire",    NOISE_POP,)
SND_FIGHT       = (100,"a struggle",NOISE_RACKET,)
SND_DOUSE       = (30, "a fire going out",NOISE_WHISPER,)
SND_QUAFF       = (20, "gulping noises",NOISE_SOME,)
SND_COUGH       = (80, "someone coughing",NOISE_SCREECH,)
SND_VOMIT       = (80, "someone vomiting",NOISE_WATERFALL,)
SND_GUNSHOT     = (450,"a gunshot",NOISE_BANG,)




    #----------#
    # #Lights  #
    #----------#

DAZZLING_LIGHT = 15 # perceived light level that results in temp. blindness
BLINDING_LIGHT = 20 # " permanent blindness
# TODO: implement light blinding when too bright. How to handle this?




    #-------------------#
    # #shape and #form  #
    #-------------------#

# shapes, the lowest level of identification on an entity you can achieve
i=1;
SHAPE_WALL          =i;i+=1;
SHAPE_FIGURE        =i;i+=1;
SHAPE_CREATURE      =i;i+=1;
SHAPE_BEAST         =i;i+=1;
SHAPE_MACHINE       =i;i+=1;
SHAPE_ORGANIC       =i;i+=1;
SHAPE_ARTIFICIAL    =i;i+=1;
SHAPE_DEVICE        =i;i+=1;
SHAPE_TOOL          =i;i+=1;
SHAPE_GUN           =i;i+=1;
SHAPE_SPHERE        =i;i+=1;
SHAPE_ROUND         =i;i+=1;
SHAPE_ROCK          =i;i+=1;
SHAPE_BLOCK         =i;i+=1;
SHAPE_CYLINDER      =i;i+=1;
SHAPE_PYRAMID       =i;i+=1;
SHAPE_CONE          =i;i+=1;
SHAPE_RING          =i;i+=1;
SHAPE_CROSS         =i;i+=1;
SHAPE_CLUB          =i;i+=1;
SHAPE_DISC          =i;i+=1;
SHAPE_SLAB          =i;i+=1;
SHAPE_TUBE          =i;i+=1;
SHAPE_STICK         =i;i+=1;
SHAPE_SQUARE        =i;i+=1;
SHAPE_SHARP         =i;i+=1;
SHAPE_LINE          =i;i+=1;
SHAPE_RECTANGLE     =i;i+=1;
SHAPE_Y             =i;i+=1;
SHAPE_CURVED        =i;i+=1;
SHAPE_JAGGED        =i;i+=1;
SHAPE_RIGHTANGLES   =i;i+=1;
SHAPE_SILKY         =i;i+=1; # cloth
SHAPE_STRING        =i;i+=1;
SHAPE_INDISTINCT    =i;i+=1;
SHAPE_AMORPHOUS     =i;i+=1;
SHAPE_LOAF          =i;i+=1;
SHAPE_FORK          =i;i+=1;
SHAPE_PAPER         =i;i+=1; # paper-thin
SHAPE_PILE          =i;i+=1;
# names of shapes, for identification purposes
SHAPES={
SHAPE_WALL          : "wall",
SHAPE_FIGURE        : "figure",
SHAPE_CREATURE      : "creature",
SHAPE_BEAST         : "beast",
SHAPE_MACHINE       : "machine",
SHAPE_ORGANIC       : "organic object",
SHAPE_ARTIFICIAL    : "artificial object",
SHAPE_DEVICE        : "device",
SHAPE_TOOL          : "tool",
SHAPE_GUN           : "gun",
SHAPE_SPHERE        : "spherical object",
SHAPE_ROUND         : "round object",
SHAPE_ROCK          : "rock-like object",
SHAPE_BLOCK         : "cubical object",
SHAPE_CYLINDER      : "cylindrical object",
SHAPE_PYRAMID       : "pyramidal object",
SHAPE_CONE          : "conical object",
SHAPE_RING          : "ring-shaped object",
SHAPE_CROSS         : "cross-shaped object",
SHAPE_CLUB          : "club-shaped object",
SHAPE_DISC          : "disc-shaped object",
SHAPE_SLAB          : "slab-shaped object",
SHAPE_TUBE          : "tube-shaped object",
SHAPE_STICK         : "stick",
SHAPE_SQUARE        : "square-shaped object",
SHAPE_SHARP         : "pointy object",
SHAPE_LINE          : "linear object",
SHAPE_RECTANGLE     : "rectangular object",
SHAPE_Y             : "Y-shaped object",
SHAPE_CURVED        : "curved object",
SHAPE_JAGGED        : "jagged object",
SHAPE_RIGHTANGLES   : "right-angled object",
SHAPE_SILKY         : "silky object",
SHAPE_STRING        : "rope-like object",
SHAPE_INDISTINCT    : "indistinct object",
SHAPE_AMORPHOUS     : "amorphous blob",
SHAPE_LOAF          : "loaf",
SHAPE_FORK          : "forked object",
SHAPE_PAPER         : "paper-like object",
SHAPE_PILE          : "pile of something",
}
    


    #------------------#
    # #IDENTIFICATION  #
    #------------------#

i=1;

# creatures
ID_HUMANOID         =i;i+=1;
ID_HOMINID          =i;i+=1;
ID_INSECTOID        =i;i+=1;
ID_4LEGBEAST        =i;i+=1;
ID_2LEGBEAST        =i;i+=1;
ID_8ARMS            =i;i+=1;
ID_ANDROID          =i;i+=1;
ID_ROBOT            =i;i+=1;
ID_MACHINE          =i;i+=1;
##print("end creatures: ", ID_MACHINE)

# weapon-type items
ID_CLUB             =i;i+=1;
ID_MACE             =i;i+=1;
ID_HAMMER           =i;i+=1;
ID_AXE              =i;i+=1;
ID_KNIFE            =i;i+=1;
ID_DAGGER           =i;i+=1;
ID_SWORD            =i;i+=1;
ID_LONGSWORD        =i;i+=1;
ID_STAFF            =i;i+=1;
ID_JAVELIN          =i;i+=1;
ID_SHIELD           =i;i+=1;
ID_LONGSTAFF        =i;i+=1;
ID_SPEAR            =i;i+=1;
ID_POLEARM          =i;i+=1;
ID_GREATSWORD       =i;i+=1;
ID_GREATAXE         =i;i+=1;
ID_GREATHAMMER      =i;i+=1;
ID_GREATCLUB        =i;i+=1;
ID_PUSHDAGGER       =i;i+=1;
ID_BATON            =i;i+=1;
ID_WHIP             =i;i+=1;
ID_BULLWHIP         =i;i+=1;
ID_KNUCKLES         =i;i+=1;
ID_BOOMERANG        =i;i+=1;
ID_MACHETE          =i;i+=1;
ID_PISTOL           =i;i+=1;
ID_MUSKET           =i;i+=1;
ID_SHOTGUN          =i;i+=1;
ID_SMG              =i;i+=1;
ID_RIFLE            =i;i+=1;
ID_AUTORIFLE        =i;i+=1;
ID_MACHINEGUN       =i;i+=1;
ID_SLINGSHOT        =i;i+=1;
ID_BOW              =i;i+=1;
ID_CROSSBOW         =i;i+=1;
ID_CANNON           =i;i+=1;
ID_ENERGYWEAPON     =i;i+=1;
ID_BLOWGUN          =i;i+=1;
##print("end weapon: ", ID_BLOWGUN)

# clothing / armor
ID_VEST             =i;i+=1; # torso clothes
ID_SHIRT            =i;i+=1;
ID_LONGSHIRT        =i;i+=1; # long == long-sleeved
ID_HOODY            =i;i+=1;
ID_JACKET           =i;i+=1;
ID_ARMOR            =i;i+=1; # armor
ID_GEAR             =i;i+=1;
ID_CUIRASS          =i;i+=1;
ID_SUIT             =i;i+=1;
ID_FURSUIT          =i;i+=1;
ID_MAILSHIRT        =i;i+=1;
ID_MAILLONGSHIRT    =i;i+=1;
ID_PADDEDSHIRT      =i;i+=1;
ID_PADDEDLONGSHIRT  =i;i+=1;
ID_HAZARDSUIT       =i;i+=1;
ID_PPE              =i;i+=1;
ID_BULLETPROOFVEST  =i;i+=1;
ID_VAMBRACE         =i;i+=1; # arm
ID_PADDEDLEGGING    =i;i+=1; # leg
ID_MAILLEGGING      =i;i+=1;
ID_GREAVE           =i;i+=1;
ID_PANTS            =i;i+=1;
ID_SHORTS           =i;i+=1; 
ID_PJS              =i;i+=1;
ID_BOOT             =i;i+=1; # feet
ID_SHOE             =i;i+=1;
ID_SANDAL           =i;i+=1;
ID_SAFETYGOGGLES    =i;i+=1; # eyewear
ID_SUNGLASSES       =i;i+=1;
ID_GLASSES          =i;i+=1;
ID_MASK             =i;i+=1; # facewear
ID_RESPIRATOR       =i;i+=1;
ID_GASMASK          =i;i+=1;
ID_PLAGUEMASK       =i;i+=1;
ID_WELDINGMASK      =i;i+=1;
ID_MOTORCYCLEHELM   =i;i+=1; # headwear
ID_BIOHELM          =i;i+=1;
ID_PADDEDCOIF       =i;i+=1;
ID_MAILCOIF         =i;i+=1;
ID_HELMET           =i;i+=1; # skull cap to half helm
ID_HELM             =i;i+=1; # half to full helm
ID_GLOVE            =i;i+=1; # hand armor
ID_GAUNTLET         =i;i+=1;
ID_CLOAK            =i;i+=1; # about
##print("end clothing: ", ID_CLOAK)

# misc. items
ID_MONEY            =i;i+=1;
ID_TRASH            =i;i+=1;
ID_ELECTRONICS      =i;i+=1;
ID_FIREPIT          =i;i+=1;
ID_LIGHTER          =i;i+=1;
ID_MOBILEDEVICE     =i;i+=1; # phone / PDA / geiger counter / calculator / etc.
ID_BOX              =i;i+=1;
ID_LOCKBOX          =i;i+=1; # tough looking box e.g. safe
ID_BARREL           =i;i+=1;
ID_STILL            =i;i+=1;
ID_POT              =i;i+=1;
ID_GRAVE            =i;i+=1;
ID_GRAVESLAB        =i;i+=1;
ID_TORCH            =i;i+=1;
ID_FLUIDTANK        =i;i+=1; # compressed air or liquid tank e.g. helium, oxygen tanks, propane, extinguishers, etc.
ID_BAG              =i;i+=1;
ID_RAG              =i;i+=1;
ID_RAGS             =i;i+=1; # big rag / cloth
ID_BANDAGE          =i;i+=1;
ID_RUBBERBAND       =i;i+=1;
ID_FLESH            =i;i+=1;
ID_FUNGUS           =i;i+=1;
ID_FOLIAGE          =i;i+=1; #
ID_FLOWER           =i;i+=1; #
ID_SEEDNUT          =i;i+=1;
ID_ROOT             =i;i+=1;
ID_BREAD            =i;i+=1;
ID_FRUIT            =i;i+=1;
ID_MRE              =i;i+=1;
ID_GUNMAGAZINE      =i;i+=1;
ID_GUNSCOPE         =i;i+=1;
ID_GUNSTRAP         =i;i+=1;
ID_GUNSTOCK         =i;i+=1;
ID_GUNMOD           =i;i+=1;
ID_FLASHLIGHT       =i;i+=1;
ID_LASER            =i;i+=1;
ID_SUPPRESSOR       =i;i+=1;
ID_BIPOD            =i;i+=1;
##print("end misc.: ", ID_BIPOD)

# tools
ID_TOOL             =i;i+=1;
ID_SCALPEL          =i;i+=1;
ID_SCISSORS         =i;i+=1;
ID_PLIERS           =i;i+=1;
ID_SCREWDRIVER      =i;i+=1;
ID_WHETSTONE        =i;i+=1;
ID_SHOVEL           =i;i+=1;
ID_PICKAXE          =i;i+=1;
##print("end tools: ", ID_PICKAXE)

# raw mats
ID_STRING           =i;i+=1;
ID_PARTICLES        =i;i+=1;
ID_POWDER           =i;i+=1;
ID_CLAY             =i;i+=1;
ID_WOOD             =i;i+=1;
ID_MEAT             =i;i+=1;
ID_SCRAP            =i;i+=1;
ID_SCRAPELECTRONICS =i;i+=1;
ID_ROCK             =i;i+=1;
ID_TARP             =i;i+=1;
ID_CLOTH            =i;i+=1;
ID_BONE             =i;i+=1;
ID_BONEPILE         =i;i+=1;
ID_GLASS            =i;i+=1;
ID_CHUNK            =i;i+=1;
ID_SLAB             =i;i+=1;
ID_CUBOID           =i;i+=1;
ID_CUBE             =i;i+=1;
ID_SHARD            =i;i+=1;
ID_STICK            =i;i+=1;
ID_POLE             =i;i+=1;
ID_RING             =i;i+=1;
ID_CONTAINER        =i;i+=1;
ID_OIL              =i;i+=1;
ID_GOOP             =i;i+=1;
ID_ROLL             =i;i+=1;
ID_BATTERY          =i;i+=1;
ID_SPOOL            =i;i+=1;
ID_TUBE             =i;i+=1;
ID_PIPE             =i;i+=1;
ID_BAR              =i;i+=1;
ID_INGOT            =i;i+=1;
ID_CUP              =i;i+=1;
ID_BOTTLE           =i;i+=1;
ID_WIRE             =i;i+=1;
ID_PLANK            =i;i+=1;
ID_LEAF             =i;i+=1;
ID_PLANT            =i;i+=1;
ID_LENS             =i;i+=1;
ID_SPRING           =i;i+=1;
ID_CHAIN            =i;i+=1;
ID_ROPE             =i;i+=1;
##print("end rawmats: ", ID_ROPE)
NUMIDS = i - 1

IDENTIFICATION={
    
# creatures
ID_HUMANOID         : ("humanoid",SHAPE_FIGURE,),
ID_HOMINID          : ("hominid",SHAPE_FIGURE,),
ID_INSECTOID        : ("insectoid",SHAPE_CREATURE,),
ID_4LEGBEAST        : ("beast",SHAPE_BEAST,),
ID_2LEGBEAST        : ("2-legged beast",SHAPE_FIGURE,),
ID_8ARMS            : ("octopodal creature",SHAPE_ORGANIC,),
ID_ANDROID          : ("android",SHAPE_FIGURE,),
ID_ROBOT            : ("robot",SHAPE_MACHINE,),
ID_MACHINE          : ("machine",SHAPE_MACHINE,),

# weapons
ID_CLUB             : ("club",SHAPE_CLUB,),
ID_MACE             : ("mace",SHAPE_CLUB,),
ID_HAMMER           : ("hammer",SHAPE_TOOL,),
ID_AXE              : ("axe",SHAPE_TOOL,),
ID_KNIFE            : ("knife",SHAPE_SHARP,),
ID_DAGGER           : ("dagger",SHAPE_CROSS,),
ID_SWORD            : ("sword",SHAPE_CROSS,),
ID_LONGSWORD        : ("longsword",SHAPE_CROSS,),
ID_STAFF            : ("staff",SHAPE_STICK,),
ID_JAVELIN          : ("javelin",SHAPE_STICK,),
ID_SHIELD           : ("shield",SHAPE_DISC,),
ID_LONGSTAFF        : ("longstaff",SHAPE_STICK,),
ID_SPEAR            : ("spear",SHAPE_STICK,),
ID_POLEARM          : ("polearm",SHAPE_STICK,),
ID_GREATSWORD       : ("greatsword",SHAPE_CROSS,),
ID_GREATAXE         : ("greataxe",SHAPE_TOOL,),
ID_GREATHAMMER      : ("greathammer",SHAPE_TOOL,),
ID_GREATCLUB        : ("greatclub",SHAPE_CLUB,),
ID_PUSHDAGGER       : ("pushdagger",SHAPE_TOOL,),
ID_BATON            : ("baton",SHAPE_STICK,),
ID_WHIP             : ("whip",SHAPE_STICK,),
ID_BULLWHIP         : ("bullwhip",SHAPE_STRING,),
ID_KNUCKLES         : ("knuckledusters",SHAPE_INDISTINCT,),
ID_BOOMERANG        : ("boomerang",SHAPE_DISC,),
ID_MACHETE          : ("machete",SHAPE_TOOL,),
ID_PISTOL           : ("pistol",SHAPE_GUN,),
ID_MUSKET           : ("musket",SHAPE_GUN,),
ID_SHOTGUN          : ("shotgun",SHAPE_GUN,),
ID_SMG              : ("smg",SHAPE_GUN,),
ID_RIFLE            : ("rifle",SHAPE_GUN,),
ID_AUTORIFLE        : ("automatic rifle",SHAPE_GUN,),
ID_MACHINEGUN       : ("machine gun",SHAPE_GUN,),
ID_SLINGSHOT        : ("slingshot",SHAPE_Y,),
ID_BOW              : ("bow",SHAPE_CURVED,),
ID_CROSSBOW         : ("crossbow",SHAPE_DEVICE,),
ID_CANNON           : ("cannon",SHAPE_CYLINDER,),
ID_ENERGYWEAPON     : ("energy weapon",SHAPE_DEVICE,),
ID_BLOWGUN          : ("blowgun",SHAPE_TUBE,),

# clothing / armor
ID_VEST             : ("vest",SHAPE_AMORPHOUS,),
ID_SHIRT            : ("tee",SHAPE_AMORPHOUS,),
ID_LONGSHIRT        : ("shirt",SHAPE_AMORPHOUS,),
ID_HOODY            : ("hoody",SHAPE_AMORPHOUS,),
ID_JACKET           : ("jacket",SHAPE_AMORPHOUS,),
ID_ARMOR            : ("armor",SHAPE_INDISTINCT,),
ID_GEAR             : ("gear",SHAPE_INDISTINCT,),
ID_CUIRASS          : ("cuirass",SHAPE_INDISTINCT,),
ID_SUIT             : ("suit",SHAPE_AMORPHOUS,),
ID_FURSUIT          : ("fur suit",SHAPE_AMORPHOUS,),
ID_MAILSHIRT        : ("mail vest",SHAPE_AMORPHOUS,),
ID_MAILLONGSHIRT    : ("mail shirt",SHAPE_AMORPHOUS,),
ID_PADDEDSHIRT      : ("padded vest",SHAPE_AMORPHOUS,),
ID_PADDEDLONGSHIRT  : ("padded shirt",SHAPE_AMORPHOUS,),
ID_HAZARDSUIT       : ("hazard suit",SHAPE_AMORPHOUS,),
ID_PPE              : ("PPE",SHAPE_AMORPHOUS,),
ID_BULLETPROOFVEST  : ("bullet-proof vest",SHAPE_AMORPHOUS,),
ID_VAMBRACE         : ("vambrace",SHAPE_INDISTINCT,),
ID_PADDEDLEGGING    : ("padded legging",SHAPE_SILKY,),
ID_MAILLEGGING      : ("mail legging",SHAPE_AMORPHOUS,),
ID_GREAVE           : ("greave",SHAPE_INDISTINCT,),
ID_PANTS            : ("pants",SHAPE_SILKY,),
ID_SHORTS           : ("shorts",SHAPE_SILKY,),
ID_PJS              : ("P-Js",SHAPE_AMORPHOUS,),
ID_BOOT             : ("boot",SHAPE_INDISTINCT,),
ID_SHOE             : ("shoe",SHAPE_INDISTINCT,),
ID_SANDAL           : ("sandal",SHAPE_INDISTINCT,),
ID_SAFETYGOGGLES    : ("safety goggles",SHAPE_INDISTINCT,),
ID_SUNGLASSES       : ("sunglasses",SHAPE_INDISTINCT,),
ID_GLASSES          : ("glasses",SHAPE_INDISTINCT,),
ID_MASK             : ("mask",SHAPE_DISC,),
ID_RESPIRATOR       : ("respirator",SHAPE_INDISTINCT,),
ID_GASMASK          : ("gas mask",SHAPE_INDISTINCT,),
ID_PLAGUEMASK       : ("plague mask",SHAPE_CONE,),
ID_WELDINGMASK      : ("welding mask",SHAPE_SQUARE,),
ID_MOTORCYCLEHELM   : ("motorcycle helmet",SHAPE_SPHERE,),
ID_BIOHELM          : ("bio helm",SHAPE_SPHERE,),
ID_PADDEDCOIF       : ("padded coif",SHAPE_AMORPHOUS,),
ID_MAILCOIF         : ("mail coif",SHAPE_AMORPHOUS,),
ID_HELMET           : ("helmet",SHAPE_SPHERE,),
ID_HELM             : ("helm",SHAPE_SPHERE,),
ID_GLOVE            : ("glove",SHAPE_INDISTINCT,),
ID_GAUNTLET         : ("gauntlet",SHAPE_INDISTINCT,),
ID_CLOAK            : ("cloak",SHAPE_AMORPHOUS,),

# misc. items
ID_MONEY            : ("money",SHAPE_PAPER,),
ID_TRASH            : ("garbage",SHAPE_INDISTINCT,),
ID_ELECTRONICS      : ("electronic",SHAPE_ARTIFICIAL,),
ID_FIREPIT          : ("fire pit",SHAPE_PILE,),
ID_LIGHTER          : ("lighter",SHAPE_TOOL,),
ID_MOBILEDEVICE     : ("mobile device",SHAPE_DEVICE,),
ID_BOX              : ("box",SHAPE_BLOCK,),
ID_LOCKBOX          : ("lockbox",SHAPE_BLOCK,),
ID_BARREL           : ("barrel",SHAPE_CYLINDER,),
ID_STILL            : ("still",SHAPE_CYLINDER,),
ID_POT              : ("pot",SHAPE_CYLINDER,),
ID_GRAVE            : ("grave",SHAPE_BLOCK,),
ID_GRAVESLAB        : ("grave",SHAPE_SLAB,),
ID_TORCH            : ("torch",SHAPE_STICK,),
ID_FLUIDTANK        : ("fluid tank",SHAPE_CYLINDER,),
ID_BAG              : ("bag",SHAPE_AMORPHOUS,),
ID_RAG              : ("rag",SHAPE_AMORPHOUS,),
ID_RAGS             : ("rags",SHAPE_AMORPHOUS,),
ID_BANDAGE          : ("bandage",SHAPE_AMORPHOUS,),
ID_RUBBERBAND       : ("rubber band",SHAPE_INDISTINCT,),
ID_FLESH            : ("cut of flesh",SHAPE_ORGANIC,),
ID_FUNGUS           : ("fungus",SHAPE_ORGANIC,),
ID_FOLIAGE          : ("foliage",SHAPE_ORGANIC,),
ID_FLOWER           : ("flower",SHAPE_ORGANIC,),
ID_SEEDNUT          : ("nut",SHAPE_ROUND,),
ID_ROOT             : ("root",SHAPE_ORGANIC,),
ID_BREAD            : ("bread",SHAPE_LOAF,),
ID_FRUIT            : ("fruit",SHAPE_ORGANIC,),
ID_MRE              : ("MRE",SHAPE_BLOCK,),
ID_GUNMAGAZINE      : ("gun magazine",SHAPE_BLOCK,),
ID_GUNSCOPE         : ("gun scope",SHAPE_CYLINDER,),
ID_GUNSTRAP         : ("gun strap",SHAPE_STRING,),
ID_GUNSTOCK         : ("gun stock",SHAPE_RIGHTANGLES,),
ID_GUNMOD           : ("gun mod",SHAPE_INDISTINCT,),
ID_FLASHLIGHT       : ("flashlight",SHAPE_CYLINDER,),
ID_SUPPRESSOR       : ("suppressor",SHAPE_CYLINDER,),
ID_LASER            : ("laser pointer",SHAPE_CYLINDER,),
ID_BIPOD            : ("bipod",SHAPE_FORK,),

# tools
ID_TOOL             : ("tool",SHAPE_TOOL,),
ID_SCALPEL          : ("scalpel",SHAPE_TOOL,),
ID_SCISSORS         : ("scissors",SHAPE_TOOL,),
ID_PLIERS           : ("pliers",SHAPE_TOOL,),
ID_SCREWDRIVER      : ("screwdriver",SHAPE_TOOL,),
ID_WHETSTONE        : ("whetstone",SHAPE_BLOCK,),
ID_SHOVEL           : ("shovel",SHAPE_STICK,),
ID_PICKAXE          : ("pickaxe",SHAPE_STICK,),

# raw mats
ID_STRING           : ("string",SHAPE_LINE,),
ID_PARTICLES        : ("particles",SHAPE_AMORPHOUS,),
ID_POWDER           : ("powder",SHAPE_AMORPHOUS,),
ID_CLAY             : ("clay",SHAPE_AMORPHOUS,),
ID_WOOD             : ("wood",SHAPE_INDISTINCT,),
ID_MEAT             : ("meat",SHAPE_INDISTINCT,),
ID_SCRAP            : ("scrap",SHAPE_INDISTINCT,),
ID_SCRAPELECTRONICS : ("scrap electronics",SHAPE_INDISTINCT,),
ID_ROCK             : ("rock",SHAPE_ROCK,),
ID_TARP             : ("tarp",SHAPE_AMORPHOUS,),
ID_CLOTH            : ("cloth",SHAPE_AMORPHOUS,),
ID_BONE             : ("bone",SHAPE_INDISTINCT,),
ID_BONEPILE         : ("bones",SHAPE_INDISTINCT,),
ID_GLASS            : ("glass",SHAPE_INDISTINCT,),
ID_CHUNK            : ("chunk",SHAPE_INDISTINCT,),
ID_SLAB             : ("slab",SHAPE_SLAB,),
ID_CUBOID           : ("cuboid",SHAPE_BLOCK,),
ID_CUBE             : ("cube",SHAPE_BLOCK,),
ID_SHARD            : ("shard",SHAPE_SHARP,),
ID_STICK            : ("stick",SHAPE_STICK,),
ID_POLE             : ("pole",SHAPE_STICK,),
ID_RING             : ("ring",SHAPE_RING,),
ID_CONTAINER        : ("container",SHAPE_BLOCK,),
ID_OIL              : ("oil",SHAPE_AMORPHOUS,),
ID_GOOP             : ("goop",SHAPE_AMORPHOUS,),
ID_ROLL             : ("roll",SHAPE_CYLINDER,),
ID_BATTERY          : ("battery",SHAPE_CYLINDER,),
ID_SPOOL            : ("spool",SHAPE_SPHERE,),
ID_TUBE             : ("tube",SHAPE_CYLINDER,),
ID_PIPE             : ("pipe",SHAPE_CYLINDER,),
ID_BAR              : ("bar",SHAPE_STICK,),
ID_INGOT            : ("ingot",SHAPE_BLOCK,),
ID_CUP              : ("cup",SHAPE_CYLINDER,),
ID_BOTTLE           : ("bottle",SHAPE_CYLINDER,),
ID_WIRE             : ("wire",SHAPE_LINE,),
ID_PLANK            : ("plank",SHAPE_RECTANGLE,),
ID_LEAF             : ("leaf",SHAPE_ORGANIC,),
ID_PLANT            : ("plant",SHAPE_ORGANIC,),
ID_LENS             : ("lens",SHAPE_DISC,),
ID_SPRING           : ("spring",SHAPE_INDISTINCT,),
ID_CHAIN            : ("chain",SHAPE_RING,),
ID_ROPE             : ("rope",SHAPE_LINE,),
}
for x in range(NUMIDS+1):
    if (x!=0 and x not in IDENTIFICATION.keys()):
        print("missing ID # {} in IDENTIFICATION".format(x))
        print("(previous is {})".format(IDENTIFICATION.get(x-1, None)))





##class Struct_Sound():
##    def __init__(self):
##textSee=textSee
##textHear=textHear


###
### Things, specific
###
##

# Although it would be nice to have constants for every item type in the game,
# in practice this makes it tedious to add new items, and it's just nicer to
# have strings for item types.

##class THG:#(Flag)
##    i=1;
##    GORE                =i;i+=1;
##    GUNPOWDER           =i;i+=1;
##    PEBBLE              =i;i+=1;
##    SAND                =i;i+=1;
##    JUG                 =i;i+=1;
##    CORPSE_SHROOM       =i;i+=1;
##    TREE                =i;i+=1;
##    LOG                 =i;i+=1;
##    WOOD                =i;i+=1;
##    SAWDUST             =i;i+=1;
##    DUST                =i;i+=1;
##    GRAVE               =i;i+=1;
##    SAFE                =i;i+=1;
##    BOX                 =i;i+=1;
##    POT                 =i;i+=1;
##    CASTIRONPAN         =i;i+=1;
##    STILL               =i;i+=1;
##    DOSIMETER           =i;i+=1;
##    TOWEL               =i;i+=1;
##    TOOTHBRUSH          =i;i+=1;
##    FACEFLANNEL         =i;i+=1;
##    SOAP                =i;i+=1;
##    TINOFBISCUITS       =i;i+=1;
##    FLASK               =i;i+=1;
##    COMPASS             =i;i+=1;
##    MAP                 =i;i+=1;
##    BALLOFSTRING        =i;i+=1;
##    GNATSPRAY           =i;i+=1;
##    TORCH               =i;i+=1;
##    BARREL              =i;i+=1;
##    METALDRUM           =i;i+=1;
##    TABLE               =i;i+=1;
##    TERMINAL            =i;i+=1;
##    COPPERTUBING        =i;i+=1;
##    COPPERWIRE          =i;i+=1;
##    SCRAPMETAL          =i;i+=1;
##    SCRAPELECTRONICS    =i;i+=1;
##    SPRING              =i;i+=1;
##    CHAINGUN            =i;i+=1;
##    LIGHTER             =i;i+=1;
##    CLAYPOT             =i;i+=1;
##    EXTINGUISHER        =i;i+=1;
##




'''
#
# gear qualities
#
i=1;
QU_LOW          =i;i+=1;
QU_MEDLOW       =i;i+=1;
QU_MED          =i;i+=1;
QU_MEDHIGH      =i;i+=1;
QU_HIGH         =i;i+=1;

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



'''

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
    '''









