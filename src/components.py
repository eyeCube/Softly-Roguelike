'''
    components.py
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

from const import *

class Child:
    __slots__=['parent']
    def __init__(self, parent):
        self.parent=parent

class Suspended: # entity is suspended from interacting with systems.
    __slots__=[]
    def __init__(self):
        pass

class Observable:
    __slots__=['observers']
    def __init__(self):
        self.observers=[]

class DeathFunction:
    __slots__=['func'] # idea: pass DEATH_ const "circumstances of death" param into func
    def __init__(self, func):
        self.func=func

class Draw:
    __slots__=['char','fgcol','bgcol']
    def __init__(self, char, fgcol, bgcol):
        self.char=char
        self.fgcol=fgcol
        self.bgcol=bgcol
       
class Name:
    __slots__=['name','title']
    def __init__(self, name: str, title=0):
        self.name = name
        self.title = title
    def __eq__(self, other):
        return (self.name==other.name)
    def __hash__(self):
        return self.name
    def __repr__(self):
        return "{}{}".format(TITLES[self.title],self.name)


class Position:
    __slots__=['x','y']
    def __init__(self, x=-1, y=-1):
        self.x = int(x)
        self.y = int(y)
    def __eq__(self, other):
        return (self.x==other.x and self.y==other.y)
    def __hash__(self):
        return self.x*rog.window_w() + self.y
    def __repr__(self):
        return "Position: ({}, {})".format(self.x,self.y)
    
class Direction:
    __slots__=['dir']
    def __init__(self, _dir):
        self.dir = int(_dir) # 0-7
    def __eq__(self, other): return (self.dir==other.dir)
    def __hash__(self): return self.dir
    def __repr__(self):
        return "Direction: ({}, {})".format(self.dir[0],self.dir[1])

class Form: #physical makeup of the object
    __slots__=['material','value','length','phase','shape']
    def __init__(self, mat=0, val=0, length=0, phase=0, shape=0): #, volume
        self.material=int(mat)  # fluid types are materials
        self.value=int(val)
        self.length=int(length)
        self.phase=int(phase)   # phase of matter, solid, liquid, etc.
        self.shape=shape        # SHAPE_ const for identification purposes.
        # TODO: fluids are implemented by:
        # phase, material, mass.
        #   phase-PHASE_FLUID
        #   material is a FL_ constant
        #   mass indicates volume depending on density

class AI:
    __slots__=['func']
    def __init__(self, func=None):
        self.func=func

class Creature:
    __slots__=['job','faction','species']
    def __init__(self, job=None, faction=None, species=None):
        self.job=job
        self.faction=faction
        self.species=species
       
class Actor:
    __slots__=['ap']
    def __init__(self, ap=0):
        self.ap=int(ap)      #action points (energy/potential to act)

class Momentum: # has some speed built up in a given direction
    __slots__=['pace','direction']
    def __init__(self, pace: int, direction: tuple):
        self.pace=pace           # PACE_ const (speed relative to MSp stat)
        self.direction=direction # DIRECTIONS dict key
        
class Player: # uniquely identify the one entity that's controlled by user
    # the player has some unique stats that only apply to them
    __slots__=['identify']
    def __init__(self, identify=0):
        self.identify=int(identify) # base identify stat
##        self.luck=luck

class Identify: # for identification purposes
    __slots__=["generic",'difficulty']
    def __init__(self, generic, difficulty=1):
        self.generic=generic # ID_ const -> indicates name that appears when its type is identified (but not the specific instance)
        self.difficulty=int(difficulty) # how difficult it is to identify it
class Identified: # identified by the player
    __slots__=["quality"]
    def __init__(self, quality=1):
        self.quality=quality # level of identification

class Targetable:
    __slots__=['kind']
    def __init__(self, kind=0):
        self.kind = kind

class ItemByQuantity: # item has a quantity value and can stack / stackable
    __slots__=['quantity']
    def __init__(self, quantity=1):
        self.quantity=quantity


    #-------------------------#
    # conversation / dialogue #
    #-------------------------#

class Speaks: # can speak/talk/hold conversation/be persuaded/barter/engage in dialogue/etc.
    __slots__=[]        # If an entity has Speaks component,
    def __init__(self): # it is expected to also have following components:
        pass            #   Disposition, Personality
class Disposition: # feelings towards the PC
    __slots__=['disposition']
    def __init__(self, default=250):
        self.disposition=int(default)
class Personality: # TODO: give personality to all creatures
    __slots__=['personality']
    def __init__(self, personality=1):
        self.personality=int(personality)
class Sympathy: # feels sympathy for other creatures
    __slots__=['sympathy']
    def __init__(self, sympathy=1):
        self.sympathy=int(sympathy)
class ConversationMemory:
    __slots__=['memories','max_len']
    def __init__(self, max_len=10, *args):
        self.memories=[]
        self.max_len=max_len
        for arg in args:
            self.memories.append(arg)
class GetsAngry: # can get mad for any reasons, can result in violence
    __slots__=['anger']
    def __init__(self):
        self.anger=0 # buildup of anger
class GetsAnnoyed: # gets bothered by e.g. repeatedly talking to them
    __slots__=['annoyance']
    def __init__(self):
        self.annoyance = 0 # buildup of annoyance
class GetsDiabetes: # can only take so much flattery in one sitting
    __slots__=['diabetes']
    def __init__(self):
        self.diabetes = 0 # buildup of diabetes
class InLove: # in romantic love with entity entity
    __slots__=['entity']
    def __init__(self, entity):
        self.entity=entity
class InHate: # has a deep, profound hate for entity entity
    __slots__=['entity']
    def __init__(self, entity):
        self.entity=entity
class GetsCreepedOut: # can become creeped out
    __slots__=[]
    def __init__(self):
        pass
class Untrusting: # doesn't easily come to trust / love people
    __slots__=[]
    def __init__(self):
        pass
class Antisocial: # person inherently doesn't like people
    __slots__=[]
    def __init__(self):
        pass
class NeverAcceptsBribes:
    __slots__=[]
    def __init__(self):
        pass
class Rich: # has rich parents
    __slots__=[]
    def __init__(self):
        pass
class Taken: # has a lover already
    __slots__=[]
    def __init__(self):
        pass
class Ascetic: # doesn't easily partake in sinful behavior
    __slots__=[]
    def __init__(self):
        pass
# pseudo-statuses
class Taunted: # was taunted by PC recently
    __slots__=[]
    def __init__(self):
        pass
class SmallTalked: # has small talked to PC recently
    __slots__=[]
    def __init__(self):
        pass
class Introduced: # PC has had this person introduced to them.
    __slots__=[]
    def __init__(self):
        pass

# traits
class Talented:
    __slots__=['skill']
    def __init__(self, skill: int):
        self.skill=skill
class AttractedToMen:
    __slots__=[]
    def __init__(self):
        pass
class AttractedToWomen:
    __slots__=[]
    def __init__(self):
        pass
class FastLearner:
    __slots__=[]
    def __init__(self):
        pass
class ComboTauntFlattery:
    __slots__=[]
    def __init__(self):
        pass

class Ambidextrous: # can be wielded by either right or left hand dominant entities (if a weapon)
    __slots__=[] # if not a weapon, then this indicates that you can wield weapons in either hand (and have it considered dominant hand)
    def __init__(self):
        pass
class LeftHanded: # dominant arm/hand is left
    __slots__=[]
    def __init__(self):
        pass
class Stuck: # entity is stuck inside another entity
    # e.g. an arrow stuck in a monster's flesh.
    # TODO: implement
    __slots__=['entity','quality']
    def __init__(self, entity, quality=1):
        self.entity=entity
        self.quality=quality # how stuck are we?? Integer, 1 is least.
class HasStuck: # entity(s) are stuck inside this entity
    __slots__=['stuck']
    def __init__(self, *args):
        self.stuck=[] # the entities which are stuck
        for arg in args:
            self.stuck.append(arg)

class Meters:
    __slots__=[
        'temp','rads','sick','expo','pain','bleed',
        'rust','rot','wet','fear','dirt',
        ]
    def __init__(self):
        # all floating point values, no need for hyper precision
        self.temp=0 # temperature
        self.rads=0 # radiation
        self.sick=0 # illness / infection
        self.expo=0 # exposure to harmful chemicals
        self.pain=0 # respain increases the thresholds for pain tolerance
        self.fear=0 # 100 fear == fully overcome by fear
        self.bleed=0 # greater bleed -> take damage more frequently
        self.rust=0 # amount of rustedness
        self.rot=0 # amount of rot
        self.wet=0 # amount of water it's taken on
        self.dirt=0 # how dirty it is. Dirt Res == Water Res. for simplicity.
class Stats: #base stats
    # all stats should be stored as integers
    # the actual in-game displayed value / value used for calculations
    # is equal to the stat divided by a multiplier (MULT_STATS) for most
    # stats, but not resistances, life, mass, etc.
    # Some pseudo-stats are stats of the ModdedStats component but not
    # stats of this component. They have no base stat and are instead
    # derived from gear and other sources. Examples are ratk, rpen, tatk.
    #
    def __init__(self, hp=1,mp=1,mpregen=1,hpregen=0, mass=1,height=0,
                 _str=0,_con=0,_int=0,_agi=0,_dex=0,_end=0,
                 resfire=100,rescold=100,resbio=100,reselec=100,
                 resphys=100,resrust=100,resrot=100,reswet=100,
                 respain=100,resbleed=100,reslight=100,ressound=100,
                 atk=0,dmg=0,pen=0,dfn=0,arm=0,pro=0,reach=0,
                 gra=0,ctr=0,bal=0,spd=0,asp=0,msp=0,
                 encmax=0,sight=0,hearing=0,
                 courage=0,scary=0,beauty=0,
                 camo=0,stealth=0
                 ):
        # attributes (MULT_ATT or MULT_STATS)
        self.str=int(_str)           
        self.con=int(_con)
        self.int=int(_int)
        self.agi=int(_agi)
        self.dex=int(_dex)
        self.end=int(_end)
        # resistances
        self.resfire=int(resfire)   # FIR
        self.rescold=int(rescold)   # ICE
        self.resbio=int(resbio)     # BIO
        self.reselec=int(reselec)   # ELC
        self.resphys=int(resphys)   # PHS - resist physical damage excepting falls / G forces.
        self.respain=int(respain)   # PAI
        self.resrust=int(resrust)   # RUS
        self.resrot=int(resrot)     # ROT
        self.reswet=int(reswet)     # WET
        self.resbleed=int(resbleed) # BLD
        self.reslight=int(reslight) # LGT
        self.ressound=int(ressound) # SND
        # stats
        self.mass=int(mass)         # 1 == smallest mass unit
        self.height=int(height)     # cm
        self.hpmax=int(hp)          # life
        self.hp=self.hpmax
        self.mpmax=int(mp)          # stamina
        self.mp=self.mpmax
        self.hpregen=hpregen        # HP regeneration rate (MULT_STATS)
        self.mpregen=mpregen        # SP regeneration rate (MULT_STATS)
        self.encmax=int(encmax)     # encumberance maximum
        self.enc=0                  # encumberance
        self.spd=int(spd)    # Speed -- AP gained per turn
        self.asp=int(asp)    # Attack Speed (affects AP cost of attacking)
        self.msp=int(msp)    # Move Speed (affects AP cost of moving)
        self.atk=int(atk)    # Attack -- accuracy (MULT_STATS)
        self.dmg=int(dmg)    # Damage, physical (melee) (MULT_STATS)
        self.pen=int(pen)    # Penetration (MULT_STATS)
        self.reach=int(reach)# Reach -- melee range (MULT_STATS)
        self.dfn=int(dfn)    # Defense -- DV (dodge value) (MULT_STATS)
        self.arm=int(arm)    # Armor -- AV (armor value) (MULT_STATS)
        self.pro=int(pro)    # Protection (MULT_STATS)
        self.gra=int(gra)    # Grappling (wrestling) (MULT_STATS)
        self.ctr=int(ctr)    # Counter-attack chance (MULT_STATS)
        self.bal=int(bal)    # Balance (MULT_STATS)
        self.sight=int(sight)        # senses
        self.hearing=int(hearing)
        self.cou=int(courage)   # courage -- resistance to fear
        self.idn=int(scary) # intimidation / scariness
        self.bea=int(beauty) # factors into persuasion / love
        self.camo=int(camo)     # affects visibility
        self.stealth=int(stealth) # affects audibility

class ModdedStats: # stores the modified stat values for an entity
    def __init__(self):
        pass


class LightSource:
    __slots__=['lightID','light']
    def __init__(self, lightID, light):
        self.lightID=lightID
        self.light=light # lights.Light object
class Fuel: # fuel for fires
    __slots__=['fuel'] #,'ignition_temp'
    def __init__(self, fuel=1): #, ignition_temp=None
        self.fuel = int(fuel)
##        self.ignition_temp = int(ignition_temp) if ignition_temp is not None else FIRE_THRESHOLD

class SenseSight:
    __slots__=['fovID','events']
    def __init__(self):
        self.fovID = -1
        self.events = []
class SenseHearing:
    __slots__=['events']
    def __init__(self):
        self.events = []

class Job:
    __slots__=['job']
    def __init__(self, job: int):
        self.job=job # CLS_ const

class Gender:
    __slots__=['gender']
    def __init__(self, gender: int):
        self.gender=gender      # GENDER_ const

class Mutable:
    __slots__=['mutations']
    def __init__(self):
        self.mutations=0

class Camo:
    __slots__=['terrains']
    def __init__(self, terrains):
        self.terrains=terrains # {terrain_constant : camo_bonus,}
        #e.g. {ROUGH : 2, SHRUB : 8, BRAMBLE: 4, JUNGLE: 16, JUNGLE2: 16,}
        
class Flags:
    __slots__=['flags']
    def __init__(self, *args):
        self.flags=set()
        for arg in args:
            self.flags.add(arg)
class Skills:
    __slots__=['skills']
    def __init__(self, skills=None):
        # skills = {int SKILL_CONSTANT : int skill_experience}
        self.skills = skills if skills else {}
        # exp to next level is always constant e.g. 1000 (paper mario style)
        #   this is much easier for people to understand.
        # Also this way, after a certain point, low level shit will no longer
        #   suffice to level you up.
        # level is calculated using experience -> experience % 1000
##class _Skill: # shouldn't be necessary if using modulus system of exp
##    __slots__=["level", "experience"]
##    def __init__(self, level=0, experience=0):
##        self.level = level # int level
##        self.experience = experience # int experience CURRENT LEVEL

class DelayedAction:
# Queued Actions / Delayed Actions / multi-turn actions / queued jobs / queued tasks / action queue / ActionQueueProcessor
# Actions that take multiple turns to complete use these components
# to keep track of the progress and to finish up the task when complete
# (func) or cancelled (cancelfunc). Cancelled means task is cancelled
# and is pending its cancellation being processed by ActionQueueProcessor.
# Interrogate
    __slots__=['ap','apMax','func','data','cancelfunc',
               'cancelled','interrupted','elapsed']
    def __init__(self, jobtype, totalAP, func, cancelfunc):
        self.ap=totalAP
        self.apmax=totalAP
        self.func=func # function that runs when action completed. Two parameters: ent, which is the entity calling the function, and data, which is special data about the job e.g. the item being crafted.
        self.jobtype=jobtype # JOB_ const: what type of job?
        self.cancelfunc=cancelfunc # function that runs when action cancelled. 3 params: ent, data, and AP remaining in the job. The AP remaining might influence what happens when the job is cancelled (might come out half-finished and be able to be resumed later etc.)
            # IS THERE A BETTER WAY TO DO THIS?
        self.elapsed=0 # number of turns elapsed since the job began (for timing so you know how long it's taken)
        self.cancelled=False # set to True to cause task to end early (entity cannot continue the action without restarting).
        self.interrupted=False # set to True if something notable happens that might cause the entity to reassess its strategy / change tasks.
class PausedAction: # QueuedAction that has been put on pause
# PausedAction - given to entity doing the queued action
    __slots__=['ap','func','data','cancelfunc','elapsed']
    def __init__(self, queuedAction):
        self.ap         = queuedAction.ap
        self.func       = queuedAction.func
        self.data       = queuedAction.data
        self.cancelfunc = queuedAction.cancelfunc
        self.elapsed    = queuedAction.elapsed
class UnfinishedJob:
# Queued Job / Unfinished job / crafting item:
# given to the subject of a PausedAction's data
# when a crafting job is paused, a crafting result item may be created,
# which is half-finished or 3/4 finished or w/e.
# This item can then be finished to produce the final crafting product.
# The entity with this component is that unfinished product of some kind.
    __slots__=['ap','func','cancelfunc']
    def __init__(self, ap, func, cancelfunc=None):
        self.ap = ap
        self.func = func
        self.cancelfunc = cancelfunc

class Crafting:
    __slots__=['job']
    def __init__(self, job):
        self.job=job # data object containing info about crafting job


class Prefixes:
    __slots__=['prefixes']
    def __init__(self, *args):
        self.prefixes=[] # PREFIX_ consts to add to the prefix of the name
        for arg in args:
            self.prefixes.append(arg)

class MaterialPrefix: # TODO: add this to all items that can be created with multiple materials.
    __slots__=[]
    def __init__(self):
        pass

class CountersRemaining:
    __slots__=['quantity']
    def __init__(self, q=None):
        self.quantity=q

class Breathes: # needs to breathe to survive
    __slots__=['status']
    def __init__(self, status=0):
        self.status=status # BREATHE_ const; holding breath, inhaling, exhaling, hyperventilating, etc.

class Inventory: #item container
    __slots__=['capacity','size','money','mass','data','enc']
    # renamed variable "size" --> "mass"
    # "size" is now related to capacity
    def __init__(self, capacity=-1, size=1, money=0):
        self.capacity=capacity  # encumberance maximum (-1 == infinite) before items fall out of your bag, your bag breaks, your items poke you in the side, etc.
        self.size=size          # max. encumberance any one item can have inside this container (TODO: implement this! A backpack could have a high size and capacity, and you can share your inventory with the backpack when it's equipped (adds capacity and uses max size of all inventories you possess))
        self.money=money        # current amount of money in the container
        self.mass=0             # total mass of all entities in the container
        self.enc=0              # current total encumberance value
        self.data=[]            # list of entities
        
class FluidContainer:
    __slots__=['capacity','size','data']
    def __init__(self, capacity):
        self.capacity=capacity
        self.size=0
        self.data={}    # { FLUIDTYPE : quantity }
    
class Carried: # entity is inside an inventory
    __slots__=['owner']
    def __init__(self, owner):
        self.owner=owner # entity who is carrying this item


class Injured: # permanent injury or weakness, independent of BP statuses
    __slots__=['injuries']
    def __init__(self, _list):
        self.injuries=_list
class _Injury: # for use by Injured component
    __slots__=['type','name','mods']
    def __init__(self, _type, name, mods):
        self.type=_type # injury type constant
        self.name=name  # name of the injury for display on GUI
        self.mods=mods  # {component : {var : modf}}



    #-------------------#
    # Trigger functions #
    #-------------------#

# Trigger functions run for entities when certain conditions are met.
# These classes have a variable "func" which is a pointer to
#   the function that runs when the trigger is pulled.
#   The parameters for each function are specified by the class.

class OnImpact: # conglomerate w/ ShattersOnImpact
    __slots__=['func']
    def __init__(self, func):
        self.func=func  # params: (entity1, entity2, force)
                        # where entity1 is the one calling the function
class OnForce: # G-forces affect creatures even if no impact occurs
    __slots__=['func']
    def __init__(self, func):
        self.func=func  # params: (entity, force)
class ReactsWithWater:
    __slots__=['func']  # function that runs when it touches water
    def __init__(self, func):
        self.func=func  # params: (entity, massOfWater)
class ReactsWithFire:   # being on fire makes it explode, transform, etc. (melting is transforming.)
    __slots__=['func']  # function that runs if it catches fire
    def __init__(self, func):
        self.func=func  # params: (entity)
class ReactsWithAir:
    __slots__=['func']
    def __init__(self, func):
        self.func=func  # params: (entity)
class ReactsWithElectricity: # / powered by electricity
    __slots__=['func']
    def __init__(self, func):
        self.func=func  # params: (entity, powerInput)
    
class Rots: # thing is susceptible to rotting
    __slots__=[]
    def __init__(self):
        pass
class Rusts: # thing is susceptible to rusting
    __slots__=[]
    def __init__(self):
        pass
class Wets: # gets wet
    __slots__=[]
    def __init__(self):
        pass
class Dirties: # gets dirty
    __slots__=[]
    def __init__(self):
        pass
class Bleeds: # can bleed
    __slots__=[]
    def __init__(self):
        pass
class FeelsPain: # sucsceptible to pain
    __slots__=[]
    def __init__(self):
        pass
class FeelsFear: # sucsceptible to fear
    __slots__=[]
    def __init__(self):
        pass
class GetsSick: # sucsceptible to getting sick
    __slots__=[]
    def __init__(self):
        pass
        



    #--------------#
    #     Body     #
    #--------------#

class Slot:
    __slots__=['item','fit','covers','covered']
    def __init__(self, item=None, fit=0, covers=()):
        self.item=item
        self.fit=fit        # how well this item is secured in its slot currently
        self.covers=covers  # tuple of additional component instances
        self.covered=False  # covered by the item in this slot

class Body:
    '''
        contains information about the physical geometrical makeup
            of a multi-part body/entity
    plan        int constant, refers to the type of body
                    e.g. humanoid which has 2 arms, 2 legs, a torso and a head.
    slot        the "About" slot which is for wearing things over your body
    core        the BPC sub-component of the core (where the hearts are)
    parts       dict of all other BPC sub-components {compoClass : instance}
    position    int refers to an int const corresponding to predefined position
    bodyfat     int, total mass of fat in the whole body
    blood       int, total mass of blood in the whole body / bloodMax=maximum
    hydration   int, total mass of water in the whole body / maximum
    satiation   int, units of hunger satisfaction / maximum
    sleep       int, units of sleep satisfaction / maximum
    '''
    __slots__=[
        'plan','slot','covered',
        'core','parts','height','position',
        'blood','bloodMax','bodyfat',
        'hydration','hydrationMax',
        'satiation','satiationMax',
        'fatigue','fatigueMax'
        ]
    def __init__(self, plan, core, parts={}, height=175, blood=0, fat=0, hydration=0, satiation=0, sleep=0):
        self.plan=plan      # int constant
        self.slot=Slot()    # 'about' slot
        self.core=core      # core body component (BPC core)
        self.parts=parts        # dict of BPC objects other than the core
        self.bodyfat=fat        # total mass of body fat : floating point
        self.blood=blood                # mass of blood in the body
        self.bloodMax=blood             #   (7% of total mass of the body for humans)
        self.satiation=satiation        # calories available to the body
        self.satiationMax=satiation  
        self.hydration=hydration        # mass of water in the body != satisfaction of hydration
        self.hydrationMax=hydration  
        self.fatigue=0                  # accrued fatigue (how tired/sleepy you are)
        self.fatigueMax=sleep           # amount of fatigue that results in falling asleep uncontrollably
        self.height=height              # int = height in centimeters
        self.position=0     # body pos.: standing, crouched, prone, etc.
    # end def
# end class
        
'''
    Body Part Containers (BPC)*
    contain only BP_ / BPM_ objects or lists of BP_ / BPM_ objects
    * this is the high-level objects that are sub-components of
        the Body component
'''
# cores
class BPC_SingleCore: # core=BP_Ameboid()
    __slots__=['core']
    def __init__(self, core):
        self.core=core
class BPC_Torso:
    __slots__=['core','front','back','hips','hearts','lungs','guts']
    def __init__(self):
        self.core=BP_TorsoCore()
        self.front=BP_TorsoFront()
        self.back=BP_TorsoBack()
        self.hips=BP_Hips()
        self.hearts=BPM_Hearts()
        self.lungs=BPM_Lungs()
# others
class BPC_Heads:
    __slots__=['heads']
    def __init__(self, *args):
        self.heads=[]
        for arg in args:
            self.heads.append(arg)
class BPC_Arms:
    __slots__=['arms'] # expected to have at least 2 items. Use None for N/A
    def __init__(self, *args):
        self.arms=[] if args else [None,None,] # None == No arm
        for arg in args: # the arm in slot 0 is dominant. If only one arm exists and it is the off-arm, then it should go in slot 1, and slot 0 should be None.
            self.arms.append(arg)
class BPC_Legs: # see BPC_Arms
    __slots__=['legs']
    def __init__(self, *args):
        self.legs=[] if args else [None,None,]
        for arg in args:
            self.legs.append(arg)
class BPC_Pseudopods:
    __slots__=['pseudopods']
    def __init__(self, *args):
        self.pseudopods=[]
        for arg in args:
            self.pseudopods.append(arg)
class BPC_Wings:
    __slots__=['wings']
    def __init__(self, *args):
        self.wings=[]
        for arg in args:
            self.wings.append(arg)
class BPC_Tails:
    __slots__=['tails']
    def __init__(self, *args):
        self.tails=[]
        for arg in args:
            self.tails.append(arg)
##class BPC_Genitals:
##    __slots__=['genitals']
##    def __init__(self):
##        self.genitals=BP_Genitals()

'''
    Body Parts Meta (BPM)
    contain BP sub-components
    * This is the intermediate level of abstraction which are
        contained in lists in BPC components
'''
class BPM_Head:
    __slots__=['head','neck','face','eyes','ears','nose','mouth']
    def __init__(self):
        self.head=BP_Head()
        self.face=BP_Face()
        self.neck=BP_Neck()
        self.eyes=BP_Eyes()
        self.ears=BP_Ears()
        self.nose=BP_Nose()
        self.mouth=BP_Mouth()
class BPM_Arm:
    __slots__=['hand','arm']
    def __init__(self):
        self.arm=BP_Arm()
        self.hand=BP_Hand()
class BPM_Leg:
    __slots__=['leg','foot']
    def __init__(self):
        self.leg=BP_Leg()
        self.foot=BP_Foot()
class BPM_Lungs:
    __slots__=['lungs']
    def __init__(self):
        self.lungs=[]
class BPM_Hearts:
    __slots__=['hearts']
    def __init__(self):
        self.hearts=[]
       
'''
    Body Parts (BP)
    - All BPs have HP (health) and SP (stamina) values.
    - Usually contain a slot
    - Has optional BPP sub-components
    - DO NOT have a STATUS

    static constants:
    SOFT_TARGET  - fleshy (True) or bony (False)?
                    Affects blunt / sharp damage to BPs and wounding
    HAS_ORGANS   - if yes, can deal organ wounds
    HAS_BRAINS   - if yes, can deal brain wounds
    WEAR_TYPE    - EQ_ const (equipped item: armor, clothing, etc.)
    HOLD_TYPE    - EQ_ const (held item: weapons, etc.)
'''
class BP_TorsoCore: # abdomen
    __slots__=['slot','hp','sp']
    SOFT_TARGET = False
    HAS_ORGANS = True
    HAS_BRAINS = False
    WEAR_TYPE = EQ_CORE
    HOLD_TYPE = EQ_NONE
    def __init__(self):
        self.slot=Slot()
        self.hp=BP_HEALTH_MAX
        self.sp=BP_STAMINA_MAX
class BP_TorsoFront: # thorax front (chest)
    __slots__=['slot','hp','sp']
    SOFT_TARGET = False
    HAS_ORGANS = True
    HAS_BRAINS = False
    WEAR_TYPE = EQ_FRONT
    HOLD_TYPE = EQ_NONE
    def __init__(self):
        self.slot=Slot()
        self.hp=BP_HEALTH_MAX
        self.sp=BP_STAMINA_MAX
class BP_TorsoBack: # thorax back
    __slots__=['slot','hp','sp']
    SOFT_TARGET = False
    HAS_ORGANS = True
    HAS_BRAINS = False
    WEAR_TYPE = EQ_BACK
    HOLD_TYPE = EQ_NONE
    def __init__(self):
        self.slot=Slot()
        self.hp=BP_HEALTH_MAX
        self.sp=BP_STAMINA_MAX
class BP_Hips: # pelvic region
    __slots__=['slot','hp','sp']
    SOFT_TARGET = False
    HAS_ORGANS = True
    HAS_BRAINS = False
    WEAR_TYPE = EQ_HIPS
    HOLD_TYPE = EQ_NONE
    def __init__(self):
        self.slot=Slot()
        self.hp=BP_HEALTH_MAX
        self.sp=BP_STAMINA_MAX
class BP_Cell:
    __slots__=['slot']
    SOFT_TARGET = True
    HAS_ORGANS = True
    HAS_BRAINS = False
    WEAR_TYPE = EQ_CELL
    HOLD_TYPE = EQ_NONE
    def __init__(self):
        self.slot=Slot()
class BP_Head:
    __slots__=['slot','hp','sp']
    SOFT_TARGET = False
    HAS_ORGANS = False
    HAS_BRAINS = True
    WEAR_TYPE = EQ_MAINHEAD
    HOLD_TYPE = EQ_NONE
    def __init__(self):
        self.slot=Slot()
        self.hp=BP_HEALTH_MAX
        self.sp=BP_STAMINA_MAX
class BP_Neck:
    __slots__=['slot','hp','sp']
    SOFT_TARGET = False
    HAS_ORGANS = False
    HAS_BRAINS = False
    WEAR_TYPE = EQ_MAINNECK
    HOLD_TYPE = EQ_NONE
    def __init__(self):
        self.slot=Slot()
        self.hp=BP_HEALTH_MAX
        self.sp=BP_STAMINA_MAX
class BP_Face:
    __slots__=['slot','hp','sp']
    SOFT_TARGET = False
    HAS_ORGANS = False
    HAS_BRAINS = True
    WEAR_TYPE = EQ_MAINFACE
    HOLD_TYPE = EQ_NONE
    def __init__(self):
        self.slot=Slot()
        self.hp=BP_HEALTH_MAX
        self.sp=BP_STAMINA_MAX
class BP_Mouth:
    __slots__=['held','gustatorySystem','hp','sp','weapon']
    SOFT_TARGET = False
    HAS_ORGANS = False
    HAS_BRAINS = False
    WEAR_TYPE = EQ_NONE
    HOLD_TYPE = EQ_MAINMOUTH
    def __init__(self, taste=20): # quality of taste system
        self.held=Slot() # grabbed slot (weapon equip, etc.) (TODO: mouth holding / equipping items/weapons)
        self.hp=BP_HEALTH_MAX
        self.sp=BP_STAMINA_MAX
        self.weapon=LIMBWPN_TEETH
        self.gustatorySystem=BPP_GustatorySystem(quality=taste)
class BP_Eyes:
    __slots__=['slot','visualSystem','open','hp','sp']
    SOFT_TARGET = True
    HAS_ORGANS = False
    HAS_BRAINS = False
    WEAR_TYPE = EQ_MAINEYES
    HOLD_TYPE = EQ_NONE
    def __init__(self, quantity=2, quality=20): #numEyes; vision;
        self.slot=Slot()        # eyewear for protecting eyes
        self.hp=BP_HEALTH_MAX
        self.sp=BP_STAMINA_MAX
        self.visualSystem=BPP_VisualSystem(quantity=quantity,quality=quality)
        self.open=True #eyelids open or closed? (affects resistance to chemical / light / dust damage etc.)
class BP_Ears:
    __slots__=['slot','auditorySystem','hp','sp']
    SOFT_TARGET = True
    HAS_ORGANS = False
    HAS_BRAINS = False
    WEAR_TYPE = EQ_MAINEARS
    HOLD_TYPE = EQ_NONE
    def __init__(self, quantity=2, quality=60):
        self.slot=Slot()        # earplugs, for protecting ears
        self.hp=BP_HEALTH_MAX
        self.sp=BP_STAMINA_MAX
        self.auditorySystem=BPP_AuditorySystem(quantity=quantity,quality=quality)
class BP_Nose:
    __slots__=['olfactorySystem','hp','sp']
    SOFT_TARGET = True
    HAS_ORGANS = False
    HAS_BRAINS = False
    WEAR_TYPE = EQ_NONE
    HOLD_TYPE = EQ_NONE
    def __init__(self, quality=10):
        self.hp=BP_HEALTH_MAX
        self.sp=BP_STAMINA_MAX
        self.olfactorySystem=BPP_OlfactorySystem(quality=quality)
class BP_Arm: # upper / middle arm and shoulder
    __slots__=['slot','hp','sp','covered']
    SOFT_TARGET = False
    HAS_ORGANS = False
    HAS_BRAINS = False
    WEAR_TYPE = EQ_MAINARM
    HOLD_TYPE = EQ_NONE
    def __init__(self):
        self.slot=Slot()
        self.hp=BP_HEALTH_MAX
        self.sp=BP_STAMINA_MAX
        self.covered=False
class BP_Hand: # hand and lower forearm
    __slots__=['slot','held','hp','sp','grip','weapon']
    SOFT_TARGET = False
    HAS_ORGANS = False
    HAS_BRAINS = False
    WEAR_TYPE = EQ_MAINHAND
    HOLD_TYPE = EQ_MAINHANDW
    def __init__(self, grip=10):
        self.slot=Slot() # armor slot (gloves etc.)
        self.held=Slot() # grabbed slot (weapon equip, etc.)
        self.hp=BP_HEALTH_MAX
        self.sp=BP_STAMINA_MAX
        self.weapon=LIMBWPN_HAND # bare limb damage type w/ no weapon equipped (LIMBWPN_ const)
        self.grip=grip # grip your bare hand has
class BP_Leg: # thigh and knee
    __slots__=['slot','hp','sp','covered']
    SOFT_TARGET = False
    HAS_ORGANS = False
    HAS_BRAINS = False
    WEAR_TYPE = EQ_MAINLEG
    HOLD_TYPE = EQ_NONE
    def __init__(self):
        self.slot=Slot()
        self.hp=BP_HEALTH_MAX
        self.sp=BP_STAMINA_MAX
        self.covered=False
class BP_Foot: # foot, ankle and lower leg
    __slots__=['slot','hp','sp','covered','grip']
    SOFT_TARGET = False
    HAS_ORGANS = False
    HAS_BRAINS = False
    WEAR_TYPE = EQ_MAINFOOT
    HOLD_TYPE = EQ_NONE
    def __init__(self, grip=10):
        self.slot=Slot()
        self.hp=BP_HEALTH_MAX
        self.sp=BP_STAMINA_MAX
        self.grip=grip # grip your bare foot has
        self.covered=False
class BP_InsectThorax:
    __slots__=['slot','hp','sp','covered']
    SOFT_TARGET = False
    HAS_ORGANS = True
    HAS_BRAINS = False
    WEAR_TYPE = EQ_ITHORAX
    HOLD_TYPE = EQ_NONE
    def __init__(self):
        self.slot=Slot()
        self.hp=BP_HEALTH_MAX
        self.sp=BP_STAMINA_MAX
        self.covered=False
class BP_InsectAbdomen:
    __slots__=['slot','hp','sp','covered']
    SOFT_TARGET = False
    HAS_ORGANS = True
    HAS_BRAINS = False
    WEAR_TYPE = EQ_IABDOMEN
    HOLD_TYPE = EQ_NONE
    def __init__(self):
        self.slot=Slot()
        self.hp=BP_HEALTH_MAX
        self.sp=BP_STAMINA_MAX
        self.covered=False
class BP_InsectHead:
    __slots__=['slot','hp','sp','visualSystem','covered']
    SOFT_TARGET = False
    HAS_ORGANS = False
    HAS_BRAINS = True
    WEAR_TYPE = EQ_IHEAD
    HOLD_TYPE = EQ_NONE
    def __init__(self):
        self.slot=Slot()
        self.hp=BP_HEALTH_MAX
        self.sp=BP_STAMINA_MAX
        self.visualSystem=BPP_VisualSystem()
        self.covered=False
class BP_Mandible:
    __slots__=['held','hp','sp','holding','weapon']
    SOFT_TARGET = False
    HAS_ORGANS = False
    HAS_BRAINS = False
    WEAR_TYPE = EQ_IMANDIBLE
    HOLD_TYPE = EQ_NONE
    def __init__(self):
        self.held=Slot()
        self.hp=BP_HEALTH_MAX
        self.sp=BP_STAMINA_MAX
        self.weapon=LIMBWPN_PINCER # bare limb damage type w/ no weapon equipped (LIMBWPN_ const)
        self.holding=False
class BP_InsectLeg:
    __slots__=['slot','hp','sp','covered']
    SOFT_TARGET = False
    HAS_ORGANS = False
    HAS_BRAINS = False
    WEAR_TYPE = EQ_IMAINLEG
    HOLD_TYPE = EQ_NONE
    def __init__(self):
        self.slot=Slot()
        self.hp=BP_HEALTH_MAX
        self.sp=BP_STAMINA_MAX
        self.covered=False
class BP_Tentacle: # arm and "hand" in one, can grasp things like a hand can
    __slots__=['slot','held','hp','sp','stickies','covered','holding','weapon']
    SOFT_TARGET = True
    HAS_ORGANS = False
    HAS_BRAINS = False
    WEAR_TYPE = EQ_1TENTACLE
    HOLD_TYPE = EQ_1TENTACLEW
    def __init__(self, stickies=0):
        self.slot=Slot()
        self.held=Slot()
        self.hp=BP_HEALTH_MAX
        self.sp=BP_STAMINA_MAX
        self.weapon=LIMBWPN_TENTACLE # bare limb damage type w/ no weapon equipped (LIMBWPN_ const)
        self.stickies=stickies      # number/quality of suction cups on the tentacles (or other sticky thingies)
        self.covered=False
        self.holding=False
class BP_Pseudopod:
    __slots__=['slot','hp','sp','covered','weapon']
    SOFT_TARGET = True
    HAS_ORGANS = False
    HAS_BRAINS = False
    WEAR_TYPE = EQ_NONE
    HOLD_TYPE = EQ_PSEUDOPOD
    def __init__(self):
        self.slot=Slot()
        self.hp=BP_HEALTH_MAX
        self.sp=BP_STAMINA_MAX
        self.weapon=LIMBWPN_PSEUDOPOD # bare limb damage type w/ no weapon equipped (LIMBWPN_ const)
        self.covered=False
class BP_Ameboid:
    __slots__=['slot','hp','sp','covered']
    SOFT_TARGET = True
    HAS_ORGANS = True
    HAS_BRAINS = True
    WEAR_TYPE = EQ_AMEBOID
    HOLD_TYPE = EQ_NONE
    def __init__(self):
        self.slot=Slot()
        self.hp=BP_HEALTH_MAX
        self.sp=BP_STAMINA_MAX
        self.covered=False
class BP_Wing:
    __slots__=['slot','hp','sp','covered']
    SOFT_TARGET = False
    HAS_ORGANS = False
    HAS_BRAINS = False
    WEAR_TYPE = EQ_MAINWING
    HOLD_TYPE = EQ_NONE
    def __init__(self):
        self.slot=Slot()
        self.hp=BP_HEALTH_MAX
        self.sp=BP_STAMINA_MAX
        self.covered=False
class BP_Tail:
    __slots__=['slot','hp','sp','covered']
    SOFT_TARGET = False
    HAS_ORGANS = False
    HAS_BRAINS = False
    WEAR_TYPE = EQ_1TAIL
    HOLD_TYPE = EQ_NONE
    def __init__(self):
        self.slot=Slot()
        self.hp=BP_HEALTH_MAX
        self.sp=BP_STAMINA_MAX
        self.covered=False
class BP_Genitals:
    __slots__=['hp','sp','covered']
    SOFT_TARGET = True
    HAS_ORGANS = False
    HAS_BRAINS = False
    WEAR_TYPE = EQ_GENITALS
    HOLD_TYPE = EQ_NONE
    def __init__(self):
        self.hp=BP_HEALTH_MAX
        self.sp=BP_STAMINA_MAX
        self.covered=False
class BP_Appendage: #worthless appendage (small boneless, musclesless tails, etc.)
    __slots__=['kind','hp','sp','covered']
    SOFT_TARGET = True
    HAS_ORGANS = False
    HAS_BRAINS = False
    WEAR_TYPE = EQ_NONE
    HOLD_TYPE = EQ_NONE
    def __init__(self, kind):
        self.kind=kind # int const referring to a pre-conceived name in a pre-defined dict
        self.hp=BP_HEALTH_MAX
        self.sp=BP_STAMINA_MAX
        self.covered=False

''' BPP components (Body part component's subcomponents) ''' 
class BPP_VisualSystem:
    __slots__=['quantity','quality']
    def __init__(self, quantity=2, quality=20):
        self.quantity=quantity
        self.quality=quality    # combined quality of all eyes
class BPP_AuditorySystem:
    __slots__=['quantity','quality']
    def __init__(self, quantity=2, quality=60):
        self.quantity=quantity
        self.quality=quality    # combined quality of all ears
class BPP_OlfactorySystem:
    __slots__=['quality']
    def __init__(self, quality=20):
        self.quality=quality
class BPP_GustatorySystem:
    __slots__=['quality']
    def __init__(self, quality=20):
        self.quality=quality

'''
    Equippable components

    ap:         Action Points cost to equip / remove
    mods:       stat mod dict {var : modf,}
    strReq:     strength required to use effectively
    dexReq:     dexterity required to use effectively
    covers_:    covers the indicated body part in addition to the primary slot
    grip:       only for armor covering hands/feet/similar BPs
                    this affects how well that appendage can grip
'''
class Held: # entity is being held by someone (wielded in hand)
    __slots__=['owner','equipType']
    def __init__(self, owner, equipType):
        self.owner=owner # entity that has equipped this item
        self.equipType=equipType   # EQ_ const: slot the item is equipped in
class Equipped: # entity is being worn by someone (armor)
    __slots__=['owner','equipType']
    def __init__(self, owner, equipType):
        self.owner=owner # entity that has equipped this item
        self.equipType=equipType   # EQ_ const: slot the item is equipped in
class Fitted: # fitted to an entity.
    __slots__=['entity','height']
    def __init__(self, entity):
        self.entity=entity # the entity it's fitted to.
        self.height=height # the height of the entity it's fitted to.
        # in the case that an entity wants to use a fitted item that was
        # not fitted for that entity, the relative heights are used to
        # determine how well the item "fits." Bad fits are exponentially
        # worse for your stats as the height gap increases, until the item
        # canot be equipped because it's too small / too big.

class Clothes: # equipable armor-like component is clothing, not armor
    # hence it works with unarmored skill, not armored skill
    __slots__=['quality']
    def __init__(self,quality=0):
        self.quality=quality
        
class EquipableInAmmoSlot:
    __slots__=['ap','mods']
    def __init__(self, ap, mods): 
        self.ap=ap
        self.mods=mods
class EquipableInFrontSlot: # breastplate
    __slots__=['ap','mods','strReq',
               'coversBack','coversCore','coversHips']
    def __init__(self, ap, mods, strReq=0,
                 coversBack=False, coversCore=False,
                 coversHips=False): 
        self.ap=ap
        self.mods=mods
        self.coversBack=coversBack
        self.coversCore=coversCore
        self.coversHips=coversHips
        self.strReq=strReq
##        self.coversArms=coversArms
class EquipableInCoreSlot: # tummy area
    __slots__=['ap','mods','strReq',] # ap = AP (Energy) cost to equip / take off
    def __init__(self, ap, mods, strReq=0): 
        self.ap=ap
        self.mods=mods
        self.strReq=strReq
class EquipableInBackSlot: # the back slot is for backpacks, jetpacks, oxygen tanks, etc.
    __slots__=['ap','mods','strReq']
    def __init__(self, ap, mods, strReq=0): 
        self.ap=ap
        self.mods=mods
        self.strReq=strReq
class EquipableInHipsSlot: #
    __slots__=['ap','mods','strReq',]
    def __init__(self, ap, mods, strReq=0): 
        self.ap=ap
        self.mods=mods
        self.strReq=strReq
class EquipableInAboutSlot: # about body slot (coverings like disposable PPE, cloaks, capes, etc.)
    __slots__=['ap','mods','strReq',]
    def __init__(self, ap, mods, strReq=0): 
        self.ap=ap
        self.mods=mods
        self.strReq=strReq
class EquipableInHeadSlot:
    __slots__=['ap','mods','strReq',
               'coversFace','coversEyes','coversEars','coversNeck']
    def __init__(self, ap, mods, strReq=0,
                 coversFace=False, coversEyes=False,
                 coversEars=False, coversNeck=False ): #{component : {var : modf,}}
        self.ap=ap
        self.mods=mods
        self.coversFace=coversFace
        self.coversEyes=coversEyes
        self.coversEars=coversEars
        self.coversNeck=coversNeck
        self.strReq=strReq
class EquipableInFaceSlot:
    __slots__=['ap','mods','strReq',
               'coversEyes']
    def __init__(self, ap, mods, strReq=0,
                 coversEyes=False): #{component : {var : modf,}}
        self.ap=ap
        self.mods=mods
        self.coversEyes=coversEyes
        self.strReq=strReq
class EquipableInEyesSlot:
    __slots__=['ap','mods','strReq',]
    def __init__(self, ap, mods, strReq=0): 
        self.ap=ap
        self.mods=mods
        self.strReq=strReq
class EquipableInEarsSlot:
    __slots__=['ap','mods','strReq',]
    def __init__(self, ap, mods, strReq=0): 
        self.ap=ap
        self.mods=mods
        self.strReq=strReq
class EquipableInNeckSlot:
    __slots__=['ap','mods','strReq',]
    def __init__(self, ap, mods, strReq=0): 
        self.ap=ap
        self.mods=mods
        self.strReq=strReq
class EquipableInHandSlot: #gloves/gaunlets
    __slots__=['ap','mods','grip','strReq']
    def __init__(self, ap, mods, grip=0, strReq=0): 
        self.ap=ap
        self.mods=mods
        self.grip=grip # how much grip you've got on the hand wearing this
        self.strReq=strReq
class EquipableInHoldSlot: #melee weapon/ ranged weapon/ shield
    __slots__=['ap','mods','stamina',
               'grip','strReq','dexReq','force']
    def __init__(self, ap, sta, mods,
                 grip=1, strReq=0, dexReq=0, force=1): 
        self.ap=ap
        self.stamina=sta # stamina cost of attacking with this weapon
        self.mods=mods
        self.grip=grip # how easily you can get a grip on it.
        self.force=force # force multiplier (float) (basically constant)
        self.strReq=strReq
        self.dexReq=dexReq
class EquipableInArmSlot:
    __slots__=['ap','mods','strReq',]
    def __init__(self, ap, mods, strReq=0): 
        self.ap=ap
        self.mods=mods
        self.strReq=strReq
class EquipableInFootSlot: #shoe / boot
    __slots__=['ap','mods','grip','strReq',]
    def __init__(self, ap, mods, grip=0, strReq=0): 
        self.ap=ap
        self.mods=mods
        self.grip=grip # how much grip you've got on the foot wearing this
        self.strReq=strReq
class EquipableInLegSlot:
    __slots__=['ap','mods','strReq',
               'coversBoth']
    def __init__(self, ap, mods, strReq=0,
                 coversBoth=False): 
        self.ap=ap
        self.mods=mods
        self.coversBoth=coversBoth # covers two legs?
        self.strReq=strReq
        
# unused
##
##class EquipableInJewelrySlot: # slot that has infinite room for more shit
##    __slots__=['ap','mods']
##    def __init__(self, ap, mods): 
##        self.ap=ap
##        self.mods=mods
       
        # NOTE: these variables should probably be just flags
##        self.twoh=twoh # two-handed? 0 = no, 1 = allowed, 2 = required
##        self.prim=prim # primary hand: mainhand or offhand (penalty for equipping in the wrong hand).
        # IDEA: when you equip in offhand, you still get the full DV bonus, but don't do as much damage/have as much penetration
##class EquipableInNeckSlot:
##    __slots__=['mods']
##    def __init__(self, mods): #{component : {var : modf,}}
##        self.mods=mods

###

    #------------------#
    # Functions / Uses #
    #------------------#

class Description:
    __slots__=['description']
    def __init__(self, description):
        self.description=description # DESC_ const

class Usable:
    __slots__=['funcPC','funcNPC','usableFromWorld']
    def __init__(self, funcPC=None, funcNPC=None, usableFromWorld=False):
        self.funcPC=funcPC
        self.funcNPC=funcNPC
        self.usableFromWorld=usableFromWorld    #usable from world or only within actor's inventory?

class Pushable:
    __slots__=['slides','rolls']
    def __init__(self, slides=0, rolls=0):
        self.slides=slides  # how well it slides
        self.rolls=rolls    # how well it rolls

class Edible:
    __slots__=['func','satiation','hydration','taste','apCost']
    def __init__(self, func=None, sat=0, hyd=0, taste=0, ap=100):
        self.func=func
        self.satiation=sat
        self.hydration=hyd
        self.taste=taste
        self.extraAP=ap # extra AP cost to consume it

class Quaffable:
    __slots__=['func','hydration','taste','apCost']
    def __init__(self, func=None, hyd=0, taste=0, ap=100):
        self.func=func
        self.hydration=hyd
        self.taste=taste
        self.apCost=ap

class Openable:
    __slots__=['isOpen','isLocked']
    def __init__(self, isOpen=False, isLocked=False):
        self.isOpen=isOpen
        self.isLocked=isLocked

##class Ingredient: #can be used in crafting, cooking, etc. IS THIS NECESSARY?
##    __slots__=['data']
##    def __init__(self, data):
##        self.data=data

class Quality:
    __slots__=['quality','minimum','maximum']
    def __init__(self, quality=0, minimum=-2, maximum=2):
        self.quality=quality
        self.minimum=minimum
        self.maximum=maximum

class WeaponSkill: #equipping as weapon benefits from having skill in this weapon school
    __slots__=['skill','bonus']
    def __init__(self, skill, bonus=0):
        self.skill=skill    # skill ID constant
        self.bonus=bonus    # skill Level modifier while it's equipped

class DamageTypeMelee: # custom damage type(s)
    # idea: select e.g. "bludgeon" attack on target;
    # function checks if weapon's damage type is blugeoning,
    # if not, then looks for this component; if bludgeon is in types,
    # use the modifier to determine effectiveness of the attack.
    # The modifier affects: Atk,Dmg,Reach,Bal,Pen, elemental damage, and BP damage.
    __slots__=['types','default']
    def __init__(self, types: dict, default: int):
        self.types=types    # {DMGTYPE_ contant : int modifier} 
        self.default=default # default damage type

class Encumberance: # how encumbering it is. Multiplied by kg.
    # TODO: use this for inventory carrying.
    #  Inventory can only carry things under a certain encumberance value.
    __slots__=['value']
    def __init__(self, value):
        self.value=value

class Moddable: # for weapons, etc. that can be upgraded using parts like silencers, bayonets, flashlights, magazines, scopes, straps, etc.
    __slots__=['mods']
    def __init__(self, mods): # {MOD_BAYONET : item,},
        self.mods={} # current modifications -- value of None: no item in the slot.

class Mod: # used to upgrade a Moddable entity
    __slots__=['type','mods','ammotype']
    def __init__(self, _typ, mods, ammotype=None):
        self.type=_typ # MOD_ const
        self.ammotype=ammotype # mod only works for weapons w/ this ammo type. None indicates no requirement (works for all ammo types).
        self.mods=mods # {stat : modf} e.g. {'atk':2,'dmg':6,'pen':12,'asp':30,'reach':1,}

class Ammo: # can be used as ammo
    __slots__=['type','force','strReq','mods','func']
    def __init__(self, typ, force=0, strReq=0, func=None, mods=None, n=1):
        self.type=typ   # ammunition type (AMMO_ const)
        self.strReq=strReq # strength required to shoot the ammo
        self.force=force # added force the ammo provides (kick and knockback/stagger)
        self.func=func   # function that runs when you shoot the ammo (makes noise, light, smoke, knocks you back, etc.)
        self.nProjectiles=n # number of projectiles fired (>1 for shotgun spread shot, etc.)
        if not mods:
            self.mods={}
        else:
            self.mods=mods
            
class Shootable: # stats for ranged attack go in EquipableInHoldSlot mods
    __slots__=['ammoTypes','ammo','reloadTime','failChance','nShots',
               'stats',]
    def __init__(
        self, ammotypes,
        rtime=0,jam=0,nshots=1,cap=0,sights=0,prone=0,func=None
        ):
        self.ammoTypes=ammotypes # *set* of ammo types that can be used
        self.ammo=[] # ammo currently loaded in the weapon
        self.reloadTime=rtime # time to reload one shot or put/take mag
        self.failChance=jam # int in 1/100ths of a percent (10000==100%)
        self.nShots=nshots # 1==semi. >1 enables burst/auto fire.
        self.stats={ # shooting-specific stats
            'capacity':capacity, #Note: all gun stats represent fully unmodded version -- 1 mag capacity unless has a built-in mag or revolver chamber etc.
            'sights':sights, #scopes only apply their Atk bonus when you aim at an enemy that is sufficiently far away depending on the weapon type. So at melee range, scopes don't help at all.
            'prone':prone, #bonus to Atk while prone
            'atk':0,
            'noise':0,
            }
class Safety: # gun trigger safety mechanism
    __slots__=['status']
    def __init__(self, on=False):
        self.on=on      # safety on or off?
        
class Throwable: # stats for thrown attack go in EquipableInHoldSlot mods
    __slots__=['func']
    def __init__(self, func=None):
        self.func=func  # script that runs when the item is thrown

class CrossbowReloader:
    __slots__=['quality','kind']
    def __init__(self, quality: int, kind: int):
        self.quality=quality
        self.kind=kind
class MagazineReloader:
    __slots__=['quality','kind']
    def __init__(self, quality: int, kind: int):
        self.quality=quality
        self.kind=kind
        
class ElementalDamageMelee: # Melee and Thrown
    __slots__=['elements']
    def __init__(self, elements):
        self.elements=elements  # {ELEM_CONST : damage}
class ElementalDamageRanged: # for ranged attacks using the Shootable component
    __slots__=['elements']
    def __init__(self, elements):
        self.elements=elements  # {ELEM_CONST : damage}

class BonusToHard: # bonus offensive power vs. heavy-armor / hard targets (melee attacks)
    __slots__=['value']
    def __init__(self, val):
        self.value=val
class BonusToSoft: # bonus offensive power vs. soft targets (w/ melee attacks)
    __slots__=['value']
    def __init__(self, val):
        self.value=val
class BonusToHardRanged: # for ranged attacks using the Shootable component
    __slots__=['value']
    def __init__(self, val):
        self.value=val
class BonusToSoftRanged: # for ranged attacks using the Shootable component
    __slots__=['value']
    def __init__(self, val):
        self.value=val
class HacksOffLimbs: # can amputate opponent's limbs in combat (melee attacks)
    __slots__=['value']
    def __init__(self, val):
        self.value=val

class Harvestable: # Can harvest raw materials
    '''
        mats -- {MATERIAL : quantity}
        tools -- {Component : quality}
    '''
    __slots__=['energy','mats','tools']
    def __init__(self, energy: int, mats: dict, tools: dict):
        self.energy=energy # energy required to harvest
        self.mats=mats # raw materials that are harvested, and the amount
        self.tools=tools # tools needed, and the quality needed to harvest
        
    #-----------------------#
    #       Tools           #
    #-----------------------#


class Tool_Cut: # cutting pushes material aside, requires a sharp edge. Whittling is also available. Performs the finest work.
    __slots__=['quality']
    def __init__(self, quality: int):
        self.quality=quality
class Tool_Chop: # chopping is the quickest way to remove massive amount of material or break flexible things into many pieces.
    __slots__=['quality']
    def __init__(self, quality: int):
        self.quality=quality
class Tool_Machete: # clearing shrubs, dense brush and jungle
    __slots__=['quality']
    def __init__(self, quality: int):
        self.quality=quality
class Tool_Saw: # sawing removes material out of the way, good for big cutting jobs, but does not perform fine work.
    __slots__=['quality']
    def __init__(self, quality: int):
        self.quality=quality
class Tool_Scalpel: # for surgery incisions / superfine cutting jobs
    __slots__=['quality']
    def __init__(self, quality: int):
        self.quality=quality
class Tool_Hammer: # carpentry, blacksmithing, smashing, light crushing, etc.
    __slots__=['quality']
    def __init__(self, quality: int):
        self.quality=quality
class Tool_Striker: # heavy hammering/driving
    __slots__=['quality']
    def __init__(self, quality: int):
        self.quality=quality
class Tool_Chisel: # a chisel and hammer can remove a lot of material in a controlled manner to make fine crafts.
    __slots__=['quality']
    def __init__(self, quality: int):
        self.quality=quality
class Tool_Weld: # the quickest way to fuse two metals together
    __slots__=['quality']
    def __init__(self, quality: int):
        self.quality=quality
class Tool_Torch: # fire tool (for burning/melting/force welding tiny things)
    __slots__=['quality']
    def __init__(self, quality: int):
        self.quality=quality
class Tool_FireStarter: # match, flint/steel, etc.
    __slots__=['quality']
    def __init__(self, quality: int):
        self.quality=quality
class Tool_Tongs: # picking up hot things (as in a crucible in smelting)
    __slots__=['quality']
    def __init__(self, quality: int):
        self.quality=quality
class Tool_Pliers: # bending, clamping, pressing, plying
    __slots__=['quality']
    def __init__(self, quality: int):
        self.quality=quality
class Tool_Drill: # hole boring
    __slots__=['quality']
    def __init__(self, quality: int):
        self.quality=quality
class Tool_Sew: # sewing needle
    __slots__=['quality']
    def __init__(self, quality: int):
        self.quality=quality
class Tool_Grinder: # grinding (removing large amounts of material from metal, etc.)
    __slots__=['quality']
    def __init__(self, quality: int):
        self.quality=quality
class Tool_Sharpener: # blade sharpener
    __slots__=['quality']
    def __init__(self, quality: int):
        self.quality=quality
class Tool_Honer: # blade honing
    __slots__=['quality']
    def __init__(self, quality: int):
        self.quality=quality
class Tool_File: # smoother / detail filing
    __slots__=['quality']
    def __init__(self, quality: int):
        self.quality=quality
class Tool_Dig: # pit digging
    __slots__=['quality']
    def __init__(self, quality: int):
        self.quality=quality
class Tool_Pickaxe: # wall breaking
    __slots__=['quality']
    def __init__(self, quality: int):
        self.quality=quality
class Tool_Crush: # crushing, pressure welding
    __slots__=['quality']
    def __init__(self, quality: int):
        self.quality=quality
class Tool_Level: # leveling (straightening guide) tool
    __slots__=['quality']
    def __init__(self, quality: int):
        self.quality=quality
class Tool_LockPick:
    __slots__=['quality']
    def __init__(self, quality: int):
        self.quality=quality
class Tool_Screwdriver:
    __slots__=['quality']
    def __init__(self, quality: int):
        self.quality=quality
class Tool_AllenWrench:
    __slots__=['quality']
    def __init__(self, quality: int):
        self.quality=quality
class Tool_Wrench:
    __slots__=['quality']
    def __init__(self, quality: int):
        self.quality=quality
class Tool_Brush: # all kinds of brushes; quality distinguishes types. e.g. quality of 1==toothbrush, 2==hair brush, 3==coarse brush, 4==paint brush, 5==cleaning brush, 6==rough brush for industrial cleaning, cleaning tool files, etc.
    __slots__=['quality'] # if quality is too high for intended use, cannot be used for that purpose. This way we don't need several different brush tool types
    def __init__(self, quality: int):
        self.quality=quality
class Tool_Mandril:
    __slots__=['quality']
    def __init__(self, quality: int):
        self.quality=quality
class Tool_Swage:
    __slots__=['quality']
    def __init__(self, quality: int):
        self.quality=quality
class Tool_Fuller: # for forging rounded shapes into iron
    __slots__=['quality']
    def __init__(self, quality: int):
        self.quality=quality
class Tool_Lens:
    __slots__=['quality']
    def __init__(self, quality: int):
        self.quality=quality
class Tool_Identify:
    __slots__=['quality']
    def __init__(self, quality: int):
        self.quality=quality
class Tool_Drillbit_a:
    __slots__=['quality']
    def __init__(self, quality: int):
        self.quality=quality
class Tool_Drillbit_b:
    __slots__=['quality']
    def __init__(self, quality: int):
        self.quality=quality
class Tool_Drillbit_c:
    __slots__=['quality']
    def __init__(self, quality: int):
        self.quality=quality
class Tool_Drillbit_d:
    __slots__=['quality']
    def __init__(self, quality: int):
        self.quality=quality
class Tool_Drillbit_e:
    __slots__=['quality']
    def __init__(self, quality: int):
        self.quality=quality
class Tool_Drillbit_f:
    __slots__=['quality']
    def __init__(self, quality: int):
        self.quality=quality
class Tool_Clamp: # chemistry tools
    __slots__=['quality']
    def __init__(self, quality: int):
        self.quality=quality
class Tool_Thermometer: # measures temperature
    __slots__=['quality']
    def __init__(self, quality: int):
        self.quality=quality
class Tool_Stand: # chemistry set stand; just a stick poking up
    __slots__=['quality']
    def __init__(self, quality: int):
        self.quality=quality
class Tool_ChemistryClamp: # special clamp for chemistry / ring support
    __slots__=['quality']
    def __init__(self, quality: int):
        self.quality=quality
class Tool_Cork: # for cooking and/or chemistry
    __slots__=['quality']
    def __init__(self, quality: int):
        self.quality=quality
class Tool_Stopper: # like a cork but rubber
    __slots__=['quality']
    def __init__(self, quality: int):
        self.quality=quality
class Tool_Flask: # chemistry container
    __slots__=['quality','quantity']
    def __init__(self, quality: int, quantity:int):
        self.quality=quality
        self.quantity=quantity
class Tool_Pouring: # pours liquid better than regular cup-shaped container
    __slots__=['quality','quantity']
    def __init__(self, quality: int, quantity:int):
        self.quality=quality
        self.quantity=quantity
class Tool_GraduatedContainer: # measures contained quantity
    __slots__=['quality','quantity']
    def __init__(self, quality: int, quantity:int):
        self.quality=quality
        self.quantity=quantity
class Tool_Anvil: # anvils bolster the hammer to allow for finer jobs in blacksmithing
    __slots__=['quality','quantity']
    def __init__(self, quality: int, quantity:int):
        self.quality=quality
        self.quantity=quantity
class Tool_Stove: # cooking
    __slots__=['quality','quantity']
    def __init__(self, quality: int, quantity:int):
        self.quality=quality
        self.quantity=quantity
class Tool_Furnace: # cooking, smelting, forge welding
    __slots__=['quality','quantity']
    def __init__(self, quality: int, quantity:int):
        self.quality=quality
        self.quantity=quantity
class Tool_Crucible: # smelting (contains hot materials)
    __slots__=['quality','quantity']
    def __init__(self, quality: int, quantity:int):
        self.quality=quality
        self.quantity=quantity
class Tool_Dropper: # eye dropper / turkey baster
    __slots__=['quality','quantity']
    def __init__(self, quality: int, quantity:int):
        self.quality=quality
        self.quantity=quantity
class Tool_Syringe: # for cooking/or and chemistry
    __slots__=['quality','quantity']
    def __init__(self, quality: int, quantity:int):
        self.quality=quality
        self.quantity=quantity
class Tool_HeatResistantGloves: # for cooking/or and chemistry
    __slots__=['quality']
    def __init__(self, quality: int):
        self.quality=quality
class Tool_LoafPan: # cooking tools
    __slots__=['quality','quantity']
    def __init__(self, quality: int, quantity:int):
        self.quality=quality
        self.quantity=quantity
class Tool_Tray: # surface for cooking, eating, etc.
    __slots__=['quality','quantity']
    def __init__(self, quality: int, quantity:int):
        self.quality=quality
        self.quantity=quantity
class Tool_ChoppingBlock: # surface for cutting, chopping
    __slots__=['quality','quantity']
    def __init__(self, quality: int, quantity:int):
        self.quality=quality
        self.quantity=quantity
class Tool_Pot: # cooking pot
    __slots__=['quality','quantity']
    def __init__(self, quality: int, quantity:int):
        self.quality=quality
        self.quantity=quantity
class Tool_Dehydrator:
    __slots__=['quality','quantity']
    def __init__(self, quality: int, quantity:int):
        self.quality=quality
        self.quantity=quantity
class Tool_:
    __slots__=['quality']
    def __init__(self, quality: int):
        self.quality=quality

##class Tool_FluidContainer: # FluidContainer is a component, no need for a separate Tool component

       
       
    #-----------------------#
    #       Foods           #
    #-----------------------#
   
   
class Food_Dry:
    __slots__=['quality']
    def __init__(self, quality: int):
        self.quality=quality
class Food_Wet:
    __slots__=['quality']
    def __init__(self, quality: int):
        self.quality=quality
class Food_Fibrous:
    __slots__=['quality']
    def __init__(self, quality: int):
        self.quality=quality
class Food_Chewy:
    __slots__=['quality']
    def __init__(self, quality: int):
        self.quality=quality
class Food_Crunchy:
    __slots__=['quality']
    def __init__(self, quality: int):
        self.quality=quality
class Food_Soft:
    __slots__=['quality']
    def __init__(self, quality: int):
        self.quality=quality
class Food_Acidic:
    __slots__=['quality']
    def __init__(self, quality: int):
        self.quality=quality
class Food_Salty:
    __slots__=['quality']
    def __init__(self, quality: int):
        self.quality=quality
class Food_Bitter:
    __slots__=['quality']
    def __init__(self, quality: int):
        self.quality=quality
class Food_Sweet:
    __slots__=['quality']
    def __init__(self, quality: int):
        self.quality=quality
class Food_Spicy:
    __slots__=['quality']
    def __init__(self, quality: int):
        self.quality=quality
class Food_Savory:
    __slots__=['quality']
    def __init__(self, quality: int):
        self.quality=quality
class Food_:
    __slots__=['quality']
    def __init__(self, quality: int):
        self.quality=quality

   
    #-----------------------#
    #       Molds           #
    #-----------------------#
   
class Mold_Anvil:
    __slots__=['quality']
    def __init__(self, quality: int):
        self.quality=quality
class Mold_AnvilLarge:
    __slots__=['quality']
    def __init__(self, quality: int):
        self.quality=quality
class Mold_SwordPlastic:
    __slots__=['quality']
    def __init__(self, quality: int):
        self.quality=quality
class Mold_SwordMetal:
    __slots__=['quality']
    def __init__(self, quality: int):
        self.quality=quality
class Mold_Dagger:
    __slots__=['quality']
    def __init__(self, quality: int):
        self.quality=quality
class Mold_StaffMetal:
    __slots__=['quality']
    def __init__(self, quality: int):
        self.quality=quality
class Mold_BoomerangPlastic:
    __slots__=['quality']
    def __init__(self, quality: int):
        self.quality=quality
class Mold_BoomerangMetal:
    __slots__=['quality']
    def __init__(self, quality: int):
        self.quality=quality
class Mold_ChainLink:
    __slots__=['quality']
    def __init__(self, quality: int):
        self.quality=quality
class Mold_Bullet:
    __slots__=['quality']
    def __init__(self, quality: int):
        self.quality=quality
class Mold_BulletSmall:
    __slots__=['quality']
    def __init__(self, quality: int):
        self.quality=quality
class Mold_BulletLarge:
    __slots__=['quality']
    def __init__(self, quality: int):
        self.quality=quality
class Mold_MinniBall:
    __slots__=['quality']
    def __init__(self, quality: int):
        self.quality=quality
class Mold_:
    __slots__=['quality']
    def __init__(self, quality: int):
        self.quality=quality


    #-----------------------#
    #    status effects     #
    #-----------------------#

    #owned by entities currently exhibiting status effect(s)
    # NOTE: when you add a new status effect component,
    #  you must add it into the list of statuses below.

# some statuses have quality, which affects the degree to which
#    you're affected by the status
class StatusHot: # too hot -> heat exhaustion
    # This status is unrelated to the fire phenomenon, light,
    #     heat production, etc. Just handles damage over time.
    __slots__=['timer']
    def __init__(self, t=-1):
        self.timer=t
class StatusBurn: # way too hot and taking constant damage from smoldering/burning
    # This status is unrelated to the fire phenomenon, light,
    #     heat production, etc. Just handles damage over time.
    __slots__=['timer']
    def __init__(self, t=-1):
        self.timer=t
class StatusChilly: # too cold -> loss of motor functions / higher thought
    __slots__=['timer']
    def __init__(self, t=-1):
        self.timer=t
class StatusCold: # way too cold -- greater severity of Chilly status
    __slots__=['timer']
    def __init__(self, t=-1):
        self.timer=t
class StatusFrozen: # frozen solid
    __slots__=['timer']
    def __init__(self, t=-1):
        self.timer=t
class StatusAcid: # damage over time, can cause deep wounds
    __slots__=['timer']
    def __init__(self, t=8):
        self.timer=t
class StatusDisoriented: # perception down: vision -67%, hearing -67%
    __slots__=['timer']
    def __init__(self, t=8):
        self.timer=t
class StatusDazzled: # vision disrupted by bright light
    __slots__=['timer']
    def __init__(self, t=4):
        self.timer=t
class StatusIrritated: # vision -25%, hearing -25%, respain -25%, 
    __slots__=['timer']
    def __init__(self, t=196):
        self.timer=t
class StatusParalyzed: # Speed -90%, Atk -15, Dfn -15
    __slots__=['timer']
    def __init__(self, t=6):
        self.timer=t
class StatusSick: # low chance to vomit, cough, sneeze; general fatigue, pain, etc.
    __slots__=['timer']
    def __init__(self, t=640):
        self.timer=t
class StatusVomit: # chance to vomit uncontrollably each turn
    __slots__=['timer']
    def __init__(self, t=48):
        self.timer=t
class StatusCough: # chance to cough uncontrollably each turn
    __slots__=['timer']
    def __init__(self, t=24):
        self.timer=t
class StatusJog: # Msp +100%
    __slots__=['timer']
    def __init__(self, t=12):
        self.timer=t
class StatusRun: # Msp +200%
    __slots__=['timer']
    def __init__(self, t=12):
        self.timer=t
class StatusSprint: # Msp +300%
    __slots__=['timer']
    def __init__(self, t=12):
        self.timer=t
class StatusFrightening: # add extra intimidation for a time
    __slots__=['timer']
    def __init__(self, t=12):
        self.timer=t
class StatusCharming: # add extra beauty for a time (TODO: implement!)
    __slots__=['timer']
    def __init__(self, t=12):
        self.timer=t
class StatusDetermined: # add extra courage for a time (TODO: implement!)
    __slots__=['timer']
    def __init__(self, t=12):
        self.timer=t
class StatusFrightened: # overcome by fear and susceptible to panic
    __slots__=['timer']
    def __init__(self, t=108):
        self.timer=t
class StatusPanic: # panicking in intense fear, lose control of self
    __slots__=['timer']
    def __init__(self, t=16):
        self.timer=t
class StatusHaste: # speed +50%
    __slots__=['timer']
    def __init__(self, t=24):
        self.timer=t
class StatusSlow: # speed -33%
    __slots__=['timer']
    def __init__(self, t=24):
        self.timer=t
class StatusHazy: # headache, slurred speech, vision loss, weakness
    __slots__=['timer']
    def __init__(self, t=3840):
        self.timer=t
class StatusSweat: # sweating
    __slots__=['timer']
    def __init__(self, t=36):
        self.timer=t
class StatusShiver: # shivering
    __slots__=['timer']
    def __init__(self, t=36):
        self.timer=t
class StatusEmaciated: # starving famished starved emaciated
    __slots__=['timer']
    def __init__(self, t=64):
        self.timer=t
class StatusHungry: # 
    __slots__=['timer']
    def __init__(self, t=64):
        self.timer=t
class StatusDehydrated: # dehydrated
    __slots__=['timer']
    def __init__(self, t=8):
        self.timer=t
class StatusLowEnergy: # stamina max --, stamina regen --
    __slots__=['timer']
    def __init__(self, t=144):
        self.timer=t
class StatusTired: # sleepy (stamina is a separate thing)
    __slots__=['timer']
    def __init__(self, t=144):
        self.timer=t
class StatusFull: # overeat
    __slots__=['timer']
    def __init__(self, t=384):
        self.timer=t
class StatusBlink: # eyes blinking
    __slots__=['timer']
    def __init__(self, t=2):
        self.timer=t
class StatusKO: # knocked out / unconscious (and sleep..?)
    __slots__=['timer']
    def __init__(self, t=-1):
        self.timer=t
class StatusRage: # enraged, out of control with anger | furious
    __slots__=['timer']
    def __init__(self, t=64):
        self.timer=t
class StatusDiabetes: # too much flattery, any more will make them upset
    __slots__=['timer']
    def __init__(self, t=86400):
        self.timer=t
# Body Position statuses
class StatusBPos_Crouched: # body position: crouched (legs and/or torso bent to make self smaller / lower)
    __slots__=[]
    def __init__(self):
        pass
class StatusBPos_Seated: # body position: seated (on the ground propped up by legs/back muscles)
    __slots__=[]
    def __init__(self):
        pass
class StatusBPos_Supine: # body position: supine (lying / on the ground face-up)
    __slots__=[]
    def __init__(self):
        pass
class StatusBPos_Prone: # body position: prone (lying / on the ground face-down)
    __slots__=[]
    def __init__(self):
        pass
class StatusBPos_Offensive: # body position: offensive stance
    __slots__=[]            # power stance
    def __init__(self):
        pass
class StatusBPos_Defensive: # body position: defensive stance
    __slots__=[]            # protective, withdrawn stance
    def __init__(self):
        pass
class StatusBPos_CQB:   # body position: CQB (close-quarters battle) stance
    __slots__=[]        # grappling and half-swording stances, etc.
    def __init__(self):
        pass

# quality statuses
# wound statuses
class StatusWound_Rash:
    __slots__=['timer','quality']
    def __init__(self, q=1, t=-1):
        self.quality=q
        self.timer=t
class StatusWound_Cut:
    __slots__=['timer','quality']
    def __init__(self, q=1, t=-1):
        self.quality=q
        self.timer=t
class StatusWound_Puncture:
    __slots__=['timer','quality']
    def __init__(self, q=1, t=-1):
        self.quality=q
        self.timer=t
class StatusWound_Gunshot:
    __slots__=['timer','quality']
    def __init__(self, q=1, t=-1):
        self.quality=q
        self.timer=t
class StatusWound_Muscle:
    __slots__=['timer','quality']
    def __init__(self, q=1, t=-1):
        self.quality=q
        self.timer=t
class StatusWound_Organ:
    __slots__=['timer','quality']
    def __init__(self, q=1, t=-1):
        self.quality=q
        self.timer=t
class StatusWound_Brain:
    __slots__=['timer','quality']
    def __init__(self, q=1, t=-1):
        self.quality=q
        self.timer=t
# other quality statuses
class StatusAdrenaline: # adrenaline boosts fight/flight capability
    # boosts resistance to pain, and physical res.
    # also raises heart rate / breathing rate
            # what else should it do??
    # (TODO: implement)
    __slots__=['timer','quality']
    def __init__(self, t=32, q=1):
        self.timer=t
        self.quality=q
class StatusDemoralized: # temporary loss of courage
    __slots__=['timer','quality']
    def __init__(self, t=64, q=32):
        self.timer=t
        self.quality=q
class StatusRecoil: # Atk - quality
    __slots__=['timer','quality']
    def __init__(self, t=1, q=1):
        self.timer=t
        self.quality=q # how much Atk you lose (*MULT_STATS)
class StatusDirty:
    __slots__=['timer','quality']
    def __init__(self, t=-1, q=1):
        self.timer=t
        self.quality=q # degree of dirtiness
class StatusWet:
    __slots__=['timer','quality']
    def __init__(self, t=-1, q=1):
        self.timer=t
        self.quality=q # degree of wetness
class StatusRusted:
    __slots__=['timer','quality']
    def __init__(self, t=-1, q=1):
        self.timer=t
        self.quality=q # degree of rustedness
class StatusRotted:
    __slots__=['timer','quality']
    def __init__(self, t=-1, q=1):
        self.timer=t
        self.quality=q # degree of rot
class StatusPain: # in overwhelming pain
    __slots__=['timer','quality']
    def __init__(self, t=-1, q=1): # only lasts as long as the pain lasts
        self.timer=t
        self.quality=q # degree of pain
class StatusBleed: # bleed: lose blood each turn, drops blood to the floor, gets your clothes bloody
    __slots__=['timer','quality']
    def __init__(self, t=128, q=1): # quality is how much blood lost per turn
        self.timer=t
        self.quality=q # mass of blood you lose per turn (1g=minor, 15g=major arterial bleeding)
class StatusOffBalance: # off-balance or staggered temporarily
    __slots__=['timer','quality']
    def __init__(self, t=4, q=1):
        self.timer=t
        self.quality=q # how much balance you lose (*MULT_STATS)
class StatusDrunk: # balance --
    __slots__=['timer','quality']
    def __init__(self, t=960, q=1):
        self.timer=t
        self.quality=q # how much balance you lose (*MULT_STATS)
class StatusBlinded:
    __slots__=['timer','quality']
    def __init__(self, t=32, q=90):
        self.timer=t
        self.quality=q # % vision lost, int 1-100
class StatusDeafened:
    __slots__=['timer','quality']
    def __init__(self, t=256, q=96):
        self.timer=t
        self.quality=q # % hearing lost, int 1-100
class StatusFlanked: # already dodged/blocked/parried this turn
    __slots__=['timer','quality']
    def __init__(self, t=1, q=1):
        self.timer=t
        self.quality=q # DV loss (*MULT_STATS)

# statuses with targets or other variables
    # TODO: implement this status (what happens when you're angry?)
    #   (meters and status adding already handled.)
class StatusAngry: # mad at a particular entity | angry | taunt | aggro
    __slots__=['timer','entity']
    def __init__(self, entity, t=64):
        self.entity=entity  # which entity are you mad at?
        self.timer=t
class StatusAnnoyed: # annoyed at a particular entity | pestered | bothered | talked to already too many times
    __slots__=['timer','entity']
    def __init__(self, entity, t=3600):
        self.entity=entity  # which entity are you annoyed at?
        self.timer=t
class StatusCreepedOut: # creeped out | weirded out | freaked out by entity
    __slots__=['timer','entity']
    def __init__(self, entity, t=3600):
        self.entity=entity  # which entity are you creeped out from?
        self.timer=t
class StatusCharmed:
    __slots__=['timer','entity','quality']
    def __init__(self, entity, t=86400, q=1):
        self.timer=t
        self.entity=entity  # entity who charmed me
        self.quality=q      # change in disposition
#

# quantity (non-timed) statuses #
# - statuses for which it would NEVER make sense for it to have a timer,
#   and it has some other quantity indicator of when it will run out.

class StatusDigest:
    __slots__=['satiation','hydration','mass']
    def __init__(self, s=1, h=1, g=1):
        self.satiation=c # potential maximum satiation points available
        self.hydration=h # potential maximum hydration points available
        self.mass=g # total mass of the food/drink TODO: implement mass
#


# GLOBAL LISTS OF COMPONENTS #

BPNAMES={ # body part names
BP_TorsoCore    : "core",
BP_TorsoFront   : "chest",
BP_TorsoBack    : "back",
BP_Hips         : "hips",
BP_Head         : "head",
BP_Neck         : "neck",
BP_Face         : "face",
BP_Mouth        : "mouth",
BP_Eyes         : "eyes",
BP_Ears         : "ears",
BP_Nose         : "nose",
BP_Arm          : "arm",
BP_Hand         : "hand",
BP_Leg          : "leg",
BP_Foot         : "foot",
    }
BPNAMES_TO_CLASSES={} # body part names (reversed)}
for k,v in BPNAMES.items():
    BPNAMES_TO_CLASSES.update({v:k})

STATUSES={ # dict of statuses that have a timer
    # component : string that appears when you have the status
    StatusHot       : 'hot',
    StatusBurn      : 'burning',
    StatusChilly    : 'cold',
    StatusCold      : 'hypothermia',
    StatusAcid      : 'corroding',
    StatusBlinded   : 'blinded',
    StatusDeafened  : 'deafened',
    StatusDisoriented:'disoriented',
    StatusIrritated : 'irritated',
    StatusPain      : 'overwhelmed by pain',
    StatusParalyzed : 'paralyzed',
    StatusSick      : 'sick',
    StatusVomit     : 'nauseous',
    StatusCough     : 'coughing fit',
    StatusSprint    : 'sprinting',
    StatusJog       : 'jogging',
    StatusRun       : 'running',
    StatusAdrenaline: 'adrenaline',
    StatusFrightening:'frightening',
    StatusCharming  : 'charming',
    StatusDetermined: 'determined',
    StatusPanic     : 'panicking',
    StatusHaste     : 'hyper',
    StatusSlow      : 'sluggish',
    StatusDrunk     : 'inebriated',
    StatusHazy      : 'hazy',
    StatusSweat     : 'sweating',
    StatusShiver    : 'shivering',
    StatusHungry    : 'hungry',
    StatusEmaciated : 'emaciated',
    StatusDehydrated: 'dehydrated',
    StatusTired     : 'sleepy',
    StatusOffBalance: 'staggered',
    StatusFull      : 'full (overeating)',
    StatusKO        : 'K.O.',
    StatusBlink     : 'blinking eyes',
    StatusCharmed   : 'charmed',
    StatusRage      : 'enraged',
    StatusBPos_Crouched : "crouched",
    StatusBPos_Seated   : "seated",
    StatusBPos_Prone    : "prone",
    StatusBPos_Supine   : "supine",
##    StatusBleed, # removed b/c it has quality
    }
##StatusDigest

STATUSES_BODYPOSITIONS=[
    StatusBPos_Crouched,
    StatusBPos_Seated,
    StatusBPos_Prone,
    StatusBPos_Supine,
    ]

STATUS_MODS={
    #status compo   : (addMods, mulMods,)
    StatusHot       : ({},{'mpregen':HOT_SPREGENMOD,},),
    StatusBurn      : {},
    StatusChilly    : ({},{
        'int':CHILLY_INTMOD,'mpregen':CHILLY_SPREGENMOD,
        'mpmax':CHILLY_STAMMOD,'spd':CHILLY_SPDMOD,},),
    StatusCold      : ({},{
        'int':COLD_INTMOD,'mpregen':COLD_SPREGENMOD,
        'mpmax':COLD_STAMMOD,'spd':COLD_SPDMOD,},),
    StatusAcid      : ({},{},),
    StatusBlinded   : ({},{'sight':BLIND_SIGHTMOD,},),
    StatusDeafened  : ({},{'hearing':DEAF_HEARINGMOD,},),
    StatusDisoriented:({'bal':DISOR_BAL*MULT_STATS,},
        {'sight':DISOR_SIGHTMOD,'hearing':DISOR_HEARINGMOD,},),
    StatusIrritated : (
        {'atk':IRRIT_ATK*MULT_STATS,'resbleed':IRRIT_RESBLEED*MULT_STATS,},
        {'sight':IRRIT_SIGHTMOD,'hearing':IRRIT_HEARINGMOD,
        'respain':IRRIT_RESPAIN,},),
    StatusParalyzed : (
        {'atk':PARAL_ATK*MULT_STATS,'dfn':PARAL_DFN*MULT_STATS,},
        {'spd':PARAL_SPDMOD},),
    StatusPain      : ({},{},), # these mods affect attributes so are handled separately
    StatusSick      : ({},{},), # ""
    StatusVomit     : ({},{},),
    StatusCough     : (
        {'atk':COUGH_ATK*MULT_STATS,'dfn':COUGH_DFN*MULT_STATS},{},),
    StatusJog       : ({},{'msp':JOG_MSPMOD},),
    StatusRun       : ({},{'msp':RUN_MSPMOD},),
    StatusSprint    : ({},{'msp':SPRINT_MSPMOD},),
    StatusFrightening:({},{},),
    StatusPanic     : ({},{},),
    StatusHaste     : ({},{'spd':HASTE_SPDMOD,},),
    StatusSlow      : ({},{'spd':SLOW_SPDMOD,},),
    StatusHazy      : ({'respain':HAZY_RESPAIN,},
        {'mpregen':HAZY_SPREGENMOD,'sight':HAZY_SIGHTMOD,
         'int':HAZY_INTMOD,},),
    StatusSweat     : ({},{},),
    StatusShiver    : ({},{},),
    StatusHungry    : ({},
        {'mpregen':HUNGRY_SPREGENMOD,'con':HUNGRY_CONMOD,
         'end':HUNGRY_ENDMOD},),
    StatusEmaciated : ({},
        {'mpregen':EMACI_SPREGENMOD,'con':EMACI_CONMOD,
         'end':EMACI_ENDMOD},),
    StatusDehydrated: (
        {'resfire':DEHYD_RESFIRE,'respain':DEHYD_RESPAIN,},
        {'mpregen':DEHYD_SPREGENMOD,},),
    StatusTired     : ({},
        {'mpregen':TIRED_SPREGENMOD,'sight':TIRED_SIGHTMOD,
         'int':TIRED_INTMOD,},),
    StatusFull      : ({},{'mpregen':FULL_SPREGENMOD},),
    StatusDrunk     : ({'bal':QUALITYMODF,},{},),
    StatusOffBalance: ({'bal':QUALITYMODF,},{},),
    StatusBPos_Crouched : (
        {'atk':CROUCHED_ATK*MULT_STATS,'dfn':CROUCHED_DFN*MULT_STATS,
         'pen':CROUCHED_PEN*MULT_STATS,'pro':CROUCHED_PRO*MULT_STATS,
         'gra':CROUCHED_GRA*MULT_STATS,},
        {'msp':CROUCHED_MSPMOD,},),
    StatusBPos_Seated : (
        {'atk':SEATED_ATK*MULT_STATS,'dfn':SEATED_DFN*MULT_STATS,
         'pen':SEATED_PEN*MULT_STATS,'pro':SEATED_PRO*MULT_STATS,
         'gra':SEATED_GRA*MULT_STATS,},
        {'msp':SEATED_MSPMOD,},),
    StatusBPos_Prone : (
        {'atk':PRONE_ATK*MULT_STATS,'dfn':PRONE_DFN*MULT_STATS,
         'pen':PRONE_PEN*MULT_STATS,'pro':PRONE_PRO*MULT_STATS,
         'gra':PRONE_GRA*MULT_STATS,},
        {'msp':PRONE_MSPMOD,},),
    StatusBPos_Supine : (
        {'atk':SUPINE_ATK*MULT_STATS,'dfn':SUPINE_DFN*MULT_STATS,
         'pen':SUPINE_PEN*MULT_STATS,'pro':SUPINE_PRO*MULT_STATS,
         'gra':SUPINE_GRA*MULT_STATS,},
        {'msp':SUPINE_MSPMOD,},),
    }

TOOLS={
Tool_Cut                : 'cut',
Tool_Chop               : 'chop',
Tool_Machete            : 'machete',
Tool_Saw                : 'saw',
Tool_Hammer             : 'hammer',
Tool_Striker            : 'striker',
Tool_Chisel             : 'chisel',
Tool_Anvil              : 'anvil',
Tool_Furnace            : 'furnace',
Tool_Stove              : 'stove',
Tool_Weld               : 'weld',
Tool_Torch              : 'torch',
Tool_FireStarter        : 'fire starter',
Tool_Crucible           : 'crucible',
Tool_Tongs              : 'tongs',
Tool_Pliers             : 'pliers',
Tool_Drill              : 'drill',
Tool_Sew                : 'sewing needle',
Tool_Grinder            : 'grinder',
Tool_Sharpener          : 'sharpener',
Tool_Honer              : 'honer',
Tool_File               : 'file',
Tool_Dig                : 'dig',
Tool_Pickaxe            : 'pickaxe',
Tool_Crush              : 'press',
Tool_LockPick           : 'lockpick',
Tool_Screwdriver        : 'screwdriver',
Tool_Level              : 'level',
Tool_Brush              : 'brush',
Tool_Mandril            : 'mandril',
Tool_Swage              : 'swage',
Tool_Fuller             : 'fuller',
Tool_Lens               : 'lens',
Tool_Identify           : 'identifier',
Tool_Drillbit_a         : 'drillbit style a',
Tool_Drillbit_b         : 'drillbit style b',
Tool_Drillbit_c         : 'drillbit style c',
Tool_Drillbit_d         : 'drillbit style d',
Tool_Drillbit_e         : 'drillbit style e',
Tool_Drillbit_f         : 'drillbit style f',
Tool_Clamp              : 'clamp',
Tool_ChemistryClamp     : 'chemistry clamp',
Tool_Flask              : 'flask',
Tool_Pouring            : 'pouring',
Tool_GraduatedContainer : 'graduated container',
Tool_Thermometer        : 'thermometer',
Tool_Syringe            : 'syringe',
Tool_Stand              : 'stand',
Tool_Cork               : 'cork',
Tool_Stopper            : 'stopper',
Tool_HeatResistantGloves: 'heat-resistant gloves', #/mittens
Tool_LoafPan            : 'loaf pan',
Tool_Tray               : 'tray',
Tool_ChoppingBlock      : 'cutting board',
}

# BP -> list of BPPs
##BP_BPPS={ # TODO: add all BP_ classes to this dict
##BP_Arm          : (BPP_SKIN, BPP_BONE, BPP_MUSCLE, BPP_ARTERY,),
##BP_Hand         : (BPP_SKIN, BPP_BONE, BPP_MUSCLE, BPP_ARTERY,),
##BP_Leg          : (BPP_SKIN, BPP_BONE, BPP_MUSCLE, BPP_ARTERY,),
##BP_Foot         : (BPP_SKIN, BPP_BONE, BPP_MUSCLE, BPP_ARTERY,),
##BP_TorsoCore    : (BPP_SKIN, BPP_MUSCLE, BPP_ARTERY, BPP_GUTS,),
##BP_TorsoFront   : (BPP_SKIN, BPP_BONE, BPP_MUSCLE, BPP_ARTERY,),
##BP_TorsoBack    : (BPP_SKIN, BPP_BONE, BPP_MUSCLE, BPP_ARTERY,),
##BP_Hips         : (BPP_SKIN, BPP_BONE, BPP_MUSCLE, BPP_ARTERY,),
##BP_Head         : (BPP_SKIN, BPP_BONE, BPP_BRAIN, BPP_HAIR,),
##BP_Face         : (BPP_SKIN, BPP_FACE,),
##BP_Eyes         : (BPP_VISUAL,),
##BP_Nose         : (BPP_OLFACTORY,),
##BP_Mouth        : (BPP_GUSTATORY, BPP_TEETH, BPP_MUSCLE),
##BP_Ears         : (BPP_AUDITORY,),
##BP_Neck         : (BPP_SKIN, BPP_BONE, BPP_MUSCLE, BPP_ARTERY,),
##    }

WOUND_TYPE_TO_STATUS={ # connect WOUND_ const type to status component
WOUND_CUT       : StatusWound_Cut,
WOUND_RASH      : StatusWound_Rash,
WOUND_PUNCTURE  : StatusWound_Puncture,
WOUND_MUSCLE    : StatusWound_Muscle,
WOUND_GUNSHOT   : StatusWound_Gunshot,
WOUND_ORGAN     : StatusWound_Organ,
WOUND_BRAIN     : StatusWound_Brain,
    }

EQ_BPS_HOLD=(EQ_MAINHANDW, EQ_OFFHANDW,)
BP_BPS_HOLD=(BP_HAND,BP_TENTACLE,)

WEARABLE_COMPONENTS={
    EquipableInHandSlot     : 'hand',
    EquipableInArmSlot      : 'arm',
    EquipableInFootSlot     : 'foot',
    EquipableInLegSlot      : 'leg',
    EquipableInFrontSlot    : 'chest',
    EquipableInCoreSlot     : 'core',
    EquipableInBackSlot     : 'back',
    EquipableInHipsSlot     : 'hips',
    EquipableInAboutSlot    : 'about person',
    EquipableInHeadSlot     : 'head',
    EquipableInFaceSlot     : 'face',
    EquipableInEyesSlot     : 'eyes',
    EquipableInEarsSlot     : 'ears',
    EquipableInNeckSlot     : 'neck',
    }
WIELDABLE_BPS={
    BP_Hand         : 'hand (wield)',
    BP_Tentacle     : 'tentacle (wield)',
    BP_Mandible     : 'mandible (wield)',
    }




'''

BP_TorsoCore
BP_TorsoFront
BP_TorsoBack
BP_Hips
BP_Cell
BP_Head
BP_Neck
BP_Mouth
BP_Eyes
BP_Ears
BP_Nose
BP_Arm
BP_Hand
BP_Leg
BP_Foot
BP_InsectThorax
BP_InsectAbdomen
BP_InsectHead
BP_Mandible
BP_InsectLeg
BP_Tentacle
BP_Pseudopod
BP_Ameboid
BP_Wing
BP_Tail
BP_Genitals
BP_Appendage
'''


















##    __slots__=[ # not using slots so that we are able to iterate through stats
##        'str','con','int',
##        'hpmax','hp','mpmax','mp',
##        'resfire','rescold','resbio','reselec','resphys',
##        'resrust','resrot','reswet','respain','resbleed',
##        'atk','dfn','dmg','gra','arm','pen','pro','ctr',
##        'spd','asp','msp',
##        'sight','hearing','courage','intimidation',
##        ]
##class _BasicStats: # for use when an object doesn't need a full Stats profile (when carried in an inventory, a container, or otherwise not in the game world / not participating in the game
##    __slots__=[
##        'hpmax','hp','mpmax','mp',
##        'resfire','resbio','reselec','resphys',
##        ]
##    def __init__(self,
##                 hp=1, hpmax=1, mp=1, mpmax=1,
##                 resfire=0,resbio=0,reselec=0,resphys=0
##                 )
##        self.hp=hp
##        self.hpmax=hpmax
##        self.mp=mp
##        self.mpmax=mpmax
##        self.resfire=resfire    #resistances
##        self.resbio=resbio
##        self.reselec=reselec
##        self.resphys=resphys    # resist physical damage excepting fall damage or other G forces.
       
##class Temp_Stats: # storage for Stats while the Stats object is not needed.
##    def __init__(self):
##        pass

# Maybe all weapons should give you bonus for 2-handed wielding
##class Bonus_TwoHanded: #bonus stats for wielding the weapon two-handed
##    __slots__=['mods']
##    def __init__(self, mods): #{component : {var : modf,}}
##        self.mods=mods
       

##class Fluid: # integrated into Form.
##    __slots__=['ID','volume']
##    def __init__(self, _id,vol):
##        self.ID=_id
##        self.volume=vol


# RESISTANCE TO THESE THINGS SHOULD BE STORED SEPARATELY. LIKE IN STATS?
##        self.res=res        # resistance to getting dirty (max: 100)
