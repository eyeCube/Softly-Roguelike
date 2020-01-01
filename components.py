'''
    components.py
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

from const import *

class Observable:
    __slots__=['observers']
    def __init__(self):
        self.observers=[]

class DeathFunction:
    __slots__=['func'] # idea: add "circumstances of death" variable which is passed into func, so the function knows under what circumstances the thing was killed (crushed, cut, stabbed, etc.)
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

class Form: #physical makeup of the object
    __slots__=['material','value','length','phase']
    def __init__(self, mat=0, val=0, length=0, phase=0): #, volume, shape
        self.material=int(mat)   # fluid types are materials
        self.value=int(val)
        self.length=int(length)
        self.phase=int(phase)    # phase of matter, solid, liquid, etc.
        # TODO: fluids are implemented by:
        # phase, material, mass.
        #   phase-PHASE_FLUID
        #   material is a FL_ constant
        #   mass indicates volume depending on density
        # TODO: length could be a value for weapons to indicate reach in small degrees, like a sword can reach to hit foes on the ground easily but a dagger cannot unless you're on top of them, etc.
       

class Position:
    __slots__=['x','y']
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)

class AI:
    __slots__=['func']
    def __init__(self, func=None):
        self.func=func

class Creature:
    __slots__=['job','faction']
    def __init__(self, job=None, faction=None):
        self.job=job
        self.faction=faction
       
class Actor:
    __slots__=['ap']
    def __init__(self, ap=0):
        self.ap=int(ap)      #action points (energy/potential to act)

class Player: # the player has some unique stats that only apply to them
    __slots__=['identify']
    def __init__(self, identify=0):
        self.identify=int(identify)

class Targetable:
    __slots__=['kind']
    def __init__(self, kind=0):
        self.kind = kind
       
class Meters:
    __slots__=[
        'temp','rads','sick','expo','pain','bleed',
        'rust','rot','wet','fear',#'dirt',
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
##        self.dirt=0 # how dirty it is. Dirt Res == Water Res. for simplicity.
class Stats: #base stats
    def __init__(self, hp=1,mp=1, mass=1,
                 _str=0,_con=0,_int=0,_agi=0,_dex=0,_end=0,luck=0,
                 resfire=100,rescold=100,resbio=100,reselec=100,
                 resphys=100,resrust=100,resrot=100,reswet=100,
                 respain=100,resbleed=100,reslight=100,ressound=100,
                 atk=0,dmg=0,pen=0,dfn=0,arm=0,pro=0,
                 spd=0,asp=0,msp=0,gra=0,ctr=0,bal=0,
                 encmax=0,force=0,sight=0,hearing=0,
                 courage=0,scary=0,beauty=0,
                 ):
        # attributes
        self.str=int(_str)           
        self.con=int(_con)
        self.int=int(_int)
        self.agi=int(_agi)
        self.dex=int(_dex)
        self.end=int(_end)
        self.luck=int(luck)
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
        self.courage=int(courage)   # COU
        # stats
        self.mass=int(mass)
        self.hpmax=int(hp)          # life
        self.hp=self.hpmax
        self.mpmax=int(mp)          # stamina
        self.mp=self.mpmax
        self.encmax=int(encmax)     # encumberance
        self.enc=0                  # " maximum
        self.force=int(force)       # how much force its attack has (knockback)
        self.atk=int(atk)    #Attack -- accuracy
        self.dmg=int(dmg)    #Damage, physical (melee)
        self.pen=int(pen)    #Penetration
        self.dfn=int(dfn)    #Defense -- DV (dodge value)
        self.arm=int(arm)    #Armor -- AV (armor value)
        self.pro=int(pro)    #Protection
        self.spd=int(spd)    #Speed -- AP gained per turn
        self.asp=int(asp)    #Attack speed (affects AP cost of attacking)
        self.msp=int(msp)    #Move speed (affects AP cost of moving)
        self.gra=int(gra)    #Grappling (wrestling)
        self.ctr=int(ctr)    #Counter-attack chance
        self.bal=int(bal)    #Maximum Balance (being off-balance can be handled by status effect like OffBalance with variable "amount" that determines how much reduced balance you have, this is very temporary
        self.sight=int(sight)        # senses
        self.hearing=int(hearing)
        self.scary=int(scary) # intimidation / scariness
        self.beauty=int(beauty) # factors into persuasion / love


class ModdedStats: # stores the modified stat values for an entity
    def __init__(self):
        pass

class LightSource:
    __slots__=['lightID','light']
    def __init__(self, lightID, light):
        self.lightID=lightID
        self.light=light # Light object
class Fuel: # fuel for fires
    __slots__=['fuel'] #,'ignition_temp'
    def __init__(self, fuel=1): #, ignition_temp=None
        self.fuel = int(fuel)
##        self.ignition_temp = int(ignition_temp) if ignition_temp is not None else FIRE_THRESHOLD

class SenseSight:
    __slots__=['fov_map','events']
    def __init__(self):
        self.fov_map = None #rog.init_fov_map(FOV_NORMAL)
        self.events = []
class SenseHearing:
    __slots__=['events']
    def __init__(self):
        self.events = []

class Gender:
    __slots__=['gender','pronouns']
    def __init__(self, gender: str, pronouns: tuple): #("he", "him", "his",)
        self.gender=gender
        self.pronouns=pronouns

class Mutable:
    __slots__=['mutations']
    def __init__(self):
        self.mutations=0
        
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

# Queued Actions / Delayed Actions / multi-turn actions / queued jobs / queued tasks / action queue / ActionQueueProcessor
# Actions that take multiple turns to complete use these components
# to keep track of the progress and to finish up the task when complete
# (func) or cancelled (cancelfunc). Interrupted means task is cancelled
# and is pending its cancellation being processed by ActionQueueProcessor.
class QueuedAction:
    __slots__=['ap','apMax','func','data','cancelfunc',
               'interrupted','elapsed' ]
    def __init__(self, totalAP, func, data=None, cancelfunc=None):
        self.ap=totalAP
        self.apMax=totalAP
        self.func=func # function that runs when action completed. Two parameters: ent, which is the entity calling the function, and data, which is special data about the job e.g. the item being crafted.
        self.data=data
        self.cancelfunc = cancelfunc # function that runs when action cancelled. 3 params: ent, data, and AP remaining in the job. The AP remaining might influence what happens when the job is cancelled (might come out half-finished and be able to be resumed later etc.)
        self.elapsed=0 # number of turns elapsed since the job began
        self.interrupted=False # set to True when/if action is interrupted
class PausedAction: # QueuedAction that has been put on pause
    __slots__=['ap','func','data','cancelfunc','elapsed']
    def __init__(self, queuedAction):
        self.ap         = queuedAction.ap
        self.func       = queuedAction.func
        self.data       = queuedAction.data
        self.cancelfunc = queuedAction.cancelfunc
        self.elapsed    = queuedAction.elapsed

class PartiallyEaten:
    __slots__=['string']
    def __init__(self, string=""):
        self.string = string # string to add to the prefix of the name

class CountersRemaining:
    __slots__=['quantity']
    def __init__(self, q=None):
        self.quantity=q

##class Breathes:
##    __slots__=[]
##    def __init__(self):
##        self.

class Slot:
    __slots__=['item','covers']
    def __init__(self, item=None, covers=()):
        self.item=item
        self.covers=covers


class Body:
    '''
        contains information about the physical geometrical makeup
            of a multi-part body/entity
    plan        int constant, refers to the type of body
                    e.g. humanoid which has 2 arms, 2 legs, a torso and a head.
    slot        the "About" slot which is for wearing things over your body
    core        the BPC sub-component of the core (where the hearts are)
    parts       list of all other BPC sub-components
    position    int refers to an int const corresponding to predefined position
    bodyfat     int, total mass of fat in the whole body
    blood       int, total mass of blood in the whole body / bloodMax=maximum
    hydration   int, total mass of water in the whole body / maximum
    satiation   int, units of hunger satisfaction / maximum
    sleep       int, units of sleep satisfaction / maximum
    '''
    __slots__=[
        'plan','slot','core','parts','height','position',
        'blood','bloodMax','bodyfat',
        'hydration','hydrationMax',
        'satiation','satiationMax',
        'sleep','sleepMax'
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
        self.sleep=sleep                # moments (seconds?) of wakefulness left before madness (or sleep)
        self.sleepMax=sleep
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
    __slots__=['arms']
    def __init__(self, *args):
        self.arms=[]
        for arg in args:
            self.arms.append(arg)
class BPC_Legs:
    __slots__=['legs']
    def __init__(self, *args):
        self.legs=[]
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
        self.eyes=BP_Eyes()
        self.ears=BP_Ears()
        self.nose=BP_Nose()
        self.neck=BP_Neck()
        self.mouth=BP_Mouth()
class BPM_Arm:
    __slots__=['hand','arm','dominant']
    def __init__(self, dominant=False):
        self.arm=BP_Arm()
        self.hand=BP_Hand()
        self.dominant=dominant # the dominant arm?
class BPM_Leg:
    __slots__=['leg','foot','dominant']
    def __init__(self, dominant=False):
        self.leg=BP_Leg()
        self.foot=BP_Foot()
        self.dominant=dominant # the dominant leg?
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
    usually contain a slot, and optional BPP sub-components
    DO NOT have a STATUS
'''
class BP_TorsoCore:
    __slots__=['slot','artery','muscle','skin','guts']
    def __init__(self):
        self.slot=Slot()
        self.artery=BPP_Artery()
        self.muscle=BPP_Muscle() # abs
        self.skin=BPP_Skin()
        self.guts=BPP_Guts()
class BP_TorsoFront:
    __slots__=['slot','bone','artery','muscle','skin']
    def __init__(self):
        self.slot=Slot()
        self.artery=BPP_Artery()
        self.bone=BPP_Bone() # ribs
        self.muscle=BPP_Muscle() # pecs
        self.skin=BPP_Skin()
class BP_TorsoBack:
    __slots__=['slot','bone','artery','muscle','skin']
    def __init__(self):
        self.slot=Slot()
        self.artery=BPP_Artery()
        self.bone=BPP_Bone() # spine
        self.muscle=BPP_Muscle()
        self.skin=BPP_Skin()
class BP_Hips:
    __slots__=['slot','bone','artery','muscle','skin']
    def __init__(self):
        self.slot=Slot()
        self.artery=BPP_Artery()
        self.bone=BPP_Bone() # pelvis
        self.muscle=BPP_Muscle()
        self.skin=BPP_Skin()
class BP_Cell:
    __slots__=['slot']
    def __init__(self):
        self.slot=Slot()
class BP_Head:
    __slots__=['slot','bone','brain','skin','hair']
    def __init__(self):
        self.slot=Slot()
        self.bone=BPP_Bone() # skull
        self.brain=BPP_Brain()
        self.skin=BPP_Skin()
        self.hair=BPP_Hair()
class BP_Neck:
    __slots__=['slot','artery','bone','muscle','skin']
    def __init__(self):
        self.slot=Slot()
        self.bone=BPP_Bone()
        self.artery=BPP_Artery()
        self.muscle=BPP_Muscle()
        self.skin=BPP_Skin()
class BP_Face:
    __slots__=['slot','features','skin']
    def __init__(self):
        self.slot=Slot()
        self.features=BPP_FacialFeatures()
        self.skin=BPP_Skin()
class BP_Mouth:
    __slots__=['bone','muscle','teeth','gustatorySystem']
    def __init__(self, taste=20): # quality of taste system
        self.bone=BPP_Bone()
        self.muscle=BPP_Muscle()
        self.teeth=BPP_Teeth()
        self.gustatorySystem=BPP_GustatorySystem(quality=taste)
class BP_Eyes:
    __slots__=['slot','visualSystem']
    def __init__(self, quantity=2, quality=20): #numEyes; vision;
        self.slot=Slot()        # eyewear for protecting eyes
        self.visualSystem=BPP_VisualSystem(quantity=quantity,quality=quality)
class BP_Ears:
    __slots__=['slot','auditorySystem']
    def __init__(self, quantity=2, quality=60):
        self.slot=Slot()        # earplugs, for protecting ears
        self.auditorySystem=BPP_AuditorySystem(quantity=quantity,quality=quality)
class BP_Nose:
    __slots__=['bone','olfactorySystem']
    def __init__(self, quality=10):
        self.bone=BPP_Bone()
        self.olfactorySystem=BPP_OlfactorySystem(quality=quality)
class BP_Arm: # upper / middle arm and shoulder
    __slots__=['slot','bone','artery','muscle','skin']
    def __init__(self):
        self.slot=Slot()
        self.artery=BPP_Artery()
        self.bone=BPP_Bone()
        self.muscle=BPP_Muscle()
        self.skin=BPP_Skin()
class BP_Hand: # hand and lower forearm
    __slots__=['slot','bone','artery','muscle','skin']
    def __init__(self):
        self.slot=Slot()
        self.artery=BPP_Artery()
        self.bone=BPP_Bone()
        self.muscle=BPP_Muscle()
        self.skin=BPP_Skin()
class BP_Leg: # thigh and knee
    __slots__=['slot','bone','artery','muscle','skin']
    def __init__(self):
        self.slot=Slot()
        self.artery=BPP_Artery()
        self.bone=BPP_Bone()
        self.muscle=BPP_Muscle()
        self.skin=BPP_Skin()
class BP_Foot: # foot, ankle and lower leg
    __slots__=['slot','bone','artery','muscle','skin']
    def __init__(self):
        self.slot=Slot()
        self.artery=BPP_Artery()
        self.bone=BPP_Bone()
        self.muscle=BPP_Muscle()
        self.skin=BPP_Skin()
class BP_Tentacle: # arm and "hand" in one, can grasp things like a hand can
    __slots__=['slot','artery','muscle','skin','stickies']
    def __init__(self, stickies=0):
        self.slot=Slot()
        self.artery=BPP_Artery()
        self.muscle=BPP_Muscle()
        self.skin=BPP_Skin()
        self.stickies=stickies      # number/quality of suction cups on the tentacles (or other sticky thingies)
class BP_Pseudopod:
    __slots__=['slot']
    def __init__(self):
        self.slot=Slot()
class BP_Ameboid:
    __slots__=['slot','nucleus']
    def __init__(self):
        self.slot=Slot()
        self.nucleus=BPP_Nucleus()
class BP_Wing:
    __slots__=['slot','bone','muscle','skin']
    def __init__(self):
        self.slot=Slot()
        self.bone=BPP_Bone()
        self.muscle=BPP_Muscle()
        self.skin=BPP_Skin()
class BP_Tail:
    __slots__=['slot','bone','artery','muscle','skin']
    def __init__(self):
        self.slot=Slot()
        self.artery=BPP_Artery()
        self.bone=BPP_Bone()
        self.muscle=BPP_Muscle()
        self.skin=BPP_Skin()
class BP_Genitals:
    __slots__=['genitals']
    def __init__(self):
        self.genitals=BPP_Genitals()
class BP_Appendage: #worthless appendage (small boneless, musclesless tails, etc.)
    __slots__=['kind']
    def __init__(self, kind):
        self.kind=kind # int const referring to a pre-conceived name in a pre-defined dict

'''
    Body Parts Piece (BPP)
    piece of body parts, sub-components of BP_ objects
    do NOT contain slots
    contain a STATUS
'''
class BPP_Skin: # 16% of total body mass
    __slots__=['status','material']
    def __init__(self, mat=-1):
        if mat==-1: mat=MAT_FLESH
        self.material=mat
        self.status=0
class BPP_Hair:
    __slots__=['status','length']#,'color']
    def __init__(self, length=1):
        self.status=0
        self.length=length
##        self.color=col
##        self.style=style
class BPP_Artery:
    __slots__=['status']
    def __init__(self):
        self.status=0
class BPP_Bone:
    __slots__=['material','status']
    def __init__(self, mat=-1):
        if mat==-1: mat=MAT_BONE
        self.material=mat # determines Strength of the bone
        self.status=0
class BPP_Muscle:
    __slots__=['status','str','fatigue','fatigueMax']
    def __init__(self, _str=1):
        self.str=_str
        self.status=0
        self.fatigue=0
        self.fatigueMax=0
class BPP_Brain:
    __slots__=['status','quality']
    def __init__(self, quality=1):
        self.status=0
        self.quality=quality
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
class BPP_FacialFeatures:
    __slots__=['beauty','scary']
    def __init__(self, beauty=32, scary=32):
        self.beauty=beauty
        self.scary=scary
class BPP_Teeth:
    __slots__=['quantity','quality','material']
    def __init__(self, quantity=26, quality=2, mat=-1):
        if mat==-1: mat=MAT_BONE
        self.quantity=quantity
        self.quality=quality
        self.material=mat
class BPP_Heart:
    __slots__=['status','str']
    def __init__(self, _str=1):
        self.str=_str
        self.status=0
class BPP_Lung:
    __slots__=['status','capacity']
    def __init__(self, cap=1):
        self.capacity=cap
        self.status=0
class BPP_Guts:
    __slots__=['status']
    def __init__(self):
        self.status=0
class BPP_Genitals:
    __slots__=['status']
    def __init__(self):
        self.status=0
class BPP_Nucleus:
    __slots__=['status']
    def __init__(self):
        self.status=0
##        self.dna=(2,1,3, 2,3,1, 0,0,2, 0,0,2, 0,1,1,)
##class BPP_Fat:
##    __slots__=['mass','status']
##    def __init__(self, mass=1):
##        self.mass=mass
##        self.status=0
       
##class Equipped: # entity has been equipped by someone # NOT NEEDED ANYMORE RIGHT?
##    __slots__=['owner','slot']
##    def __init__(self, owner, slot):
##        self.owner=owner # entity that has equipped this item
##        self.slot=slot   # slot the item is equipped in

'''
    Equippable components

    ap:     Action Points cost to equip / remove
    mods:   stat mod dict {var : modf,}
    fit:    the entity it's fitted to. 0==None. 
'''
class EquipableInAmmoSlot:
    __slots__=['ap','mods','fit']
    def __init__(self, ap, mods, fit=0): #{var : modf,}
        self.ap=ap
        self.mods=mods
        self.fit=fit
class EquipableInFrontSlot: # breastplate
    __slots__=['ap','mods','fit']
    def __init__(self, ap, mods, fit=0): #{var : modf,}
        self.ap=ap
        self.mods=mods
        self.fit=fit
        self.coversBack=coversBack
        self.coversCore=coversCore
        self.coversHips=coversHips
class EquipableInCoreSlot: # tummy area
    __slots__=['ap','mods','fit'] # ap = AP (Energy) cost to equip / take off
    def __init__(self, ap, mods, fit=0): #{var : modf,}
        self.ap=ap
        self.mods=mods
        self.fit=fit
class EquipableInBackSlot: # the back slot is for backpacks, jetpacks, oxygen tanks, etc.
    __slots__=['ap','mods','fit']
    def __init__(self, ap, mods, fit=0): #{var : modf,}
        self.ap=ap
        self.mods=mods
        self.fit=fit
class EquipableInHipsSlot: #
    __slots__=['ap','mods','fit']
    def __init__(self, ap, mods, fit=0): #{var : modf,}
        self.ap=ap
        self.mods=mods
        self.fit=fit
class EquipableInAboutSlot: # about body slot (coverings like disposable PPE, cloaks, capes, etc.)
    __slots__=['ap','mods','fit']
    def __init__(self, ap, mods, fit=0): #{var : modf,}
        self.ap=ap
        self.mods=mods
        self.fit=fit
class EquipableInHeadSlot:
    __slots__=['ap','mods','fit','coversFace','coversEyes']
    def __init__(self, ap, mods, fit=0, coversFace=False, coversEyes=False): #{component : {var : modf,}}
        self.ap=ap
        self.mods=mods        
        self.fit=fit
        self.coversFace=coversFace
        self.coversEyes=coversEyes
class EquipableInFaceSlot:
    __slots__=['ap','mods','fit','coversEyes']
    def __init__(self, ap, mods, fit=0, coversEyes=False): #{component : {var : modf,}}
        self.ap=ap
        self.mods=mods
        self.fit=fit
        self.coversEyes=coversEyes
class EquipableInEyesSlot:
    __slots__=['ap','mods','fit',]
    def __init__(self, ap, mods, fit=0): #{var : modf,}
        self.ap=ap
        self.mods=mods
        self.fit=fit
# weapon classes
class EquipableInHandSlot: #melee weapon/ ranged weapon/ shield
    __slots__=['ap','mods','fit',]
    def __init__(self, ap, sta, mods, fit=0): #{var : modf,}
        self.ap=ap
        self.stamina=sta # stamina cost of attacking with this weapon
        self.mods=mods
        self.fit=fit
        
# unused
##
##class EquipableInJewelrySlot: # slot that has infinite room for more shit
##    __slots__=['ap','mods']
##    def __init__(self, ap, mods): #{var : modf,}
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

        

class Ammo: # can be used as ammo
    __slots__=['quantity','ammoType']
    def __init__(self, ammoType,quantity=1):
        self.ammoType=ammoType
        self.quantity=quantity
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
    def __init__(self, func=None, hyd=0, taste=0, ap=1):
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

class Moddable: # for weapons, etc. that can be temporarily upgraded using parts like silencers, bayonets, flashlights, magazines, scopes, straps, etc.
    __slots__=['allowed','mods']
    def __init__(self, possible): # {MOD_BAYONET : {cmp.CombatStats : {'atk':2,'dmg':6,'pen':6,'asp':30,},},}
        self.possible=possible # dict of MODTYPE constants and the respective stat changes
        self.mods=[] # current modifications (list of entities that are modded on)
class Quality:
    __slots__=['quality','minimum','maximum']
    def __init__(self, quality=0, minimum=-2, maximum=2):
        self.quality=quality
        self.minimum=minimum
        self.maximum=maximum
class WeaponSkill: #equipping as weapon benefits from having skill in this weapon school
    __slots__=['skill']
    def __init__(self, skill):
        self.skill=skill    # skill ID constant

class Shootable:
    __slots__=['ammoTypes','atk','dmg','pen','asp','rng','minrng','ammo','capacity','reloadTime','failChance','skill','func']
    def __init__(self, aTypes,atk=0,dmg=0,pen=0,asp=0,rng=0,minrng=0,aMax=0,rTime=0,jam=0,skill=None,func=None):
        self.ammoTypes=aTypes # *set* of ammo types that can be used
        self.atk=atk        #Attack -- accuracy
        self.dmg=dmg        #damage (ranged) - physical by default (ElementalDamage component affects elemental damage...)
        self.pen=pen        #Penetration
        self.asp=asp        #Attack speed for shooting: different from melee
        self.rng=rng        #range (maximum)
        self.minrng=minrng  #range (minimum)
        self.ammo=aMax      #current ammo quantity
        self.capacity=aMax  # maximum ammo capacity
        self.reloadTime=rTime # time to reload one shot or put/take mag
        self.failChance=jam # int in 1/100ths of a percent (10000==100%)
        self.skill=skill    # skill type constant for shooting this thing
        self.func=func      # function that runs when you shoot (makes noise, light, smoke, knocks you back, etc.)

class Throwable:
    __slots__=['atk','rng','dmg','pen','asp','func','skill']
    def __init__(self, rng=0,atk=0,dmg=0,pen=0,asp=0,func=None): #,skill=None
        self.rng=rng    # range when thrown
        self.atk=atk    # change in accuracy when thrown
        self.dmg=dmg    # change in damage when thrown
        self.pen=pen    # change in penetration when thrown
        self.asp=asp    # change in attack speed when thrown
        self.func=func  # script that runs when the item is thrown
##        self.skill=skill # skill type constant for throwing this thing

class ElementalDamageMelee: # and Thrown
    __slots__=['elements']
    def __init__(self, elements):
        self.elements=elements  # {ELEM_CONST : damage}
class ElementalDamageRanged: # for ranged attacks using the Shootable component
    __slots__=['elements']
    def __init__(self, elements):
        self.elements=elements  # {ELEM_CONST : damage}

class BonusToArmor: # bonus damage (and Atk?) vs. heavy-armor / hard targets
    __slots__=['value']
    def __init__(self, val):
        self.value=val
class BonusToFlesh: # bonus damage vs. flesh and other soft targets
    __slots__=['value']
    def __init__(self, val):
        self.value=val
class HacksOffLimbs: # can amputate opponent's limbs in combat
    __slots__=['value']
    def __init__(self, val):
        self.value=val
class Bludgeon: # can be used as a bludgeon to smash bone, stone, glass, etc.
    __slots__=['value']
    def __init__(self, val):
        self.value=val
       
class Harvestable: # Can harvest raw materials # 8-16-2019: Should we use this, or some other method to handle objects turning into raw mats based on their material or some shit??
    __slots__=['energy','mats','tools']
    def __init__(self, energy: int, mats: dict, tools: dict):
        # mats = {MATERIAL : quantity}
        # tools = {Component : quality}
        self.energy=energy # energy required to harvest
        self.mats=mats # raw materials that are harvested, and the amount
        self.tools=tools # tools needed, and the quality needed to harvest

class Light:
    __slots__=['brightness','type']
    def __init__(self, brightness: int, _type: int):
        self.brightness=brightness
        self.type=_type # source const. Fire? Electricity? Something else?

       
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
class Tool_Saw: # sawing removes material out of the way, good for big cutting jobs, but does not perform fine work.
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
class Tool_Anvil: # anvils bolster the hammer to allow for finer jobs in blacksmithing
    __slots__=['quality']
    def __init__(self, quality: int):
        self.quality=quality
class Tool_Furnace: # cooking, smelting, forge welding
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
class Tool_Crucible: # smelting (contains hot materials)
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
class Tool_LockPick:
    __slots__=['quality']
    def __init__(self, quality: int):
        self.quality=quality
class Tool_Screwdriver:
    __slots__=['quality']
    def __init__(self, quality: int):
        self.quality=quality
class Tool_CrossbowReloader:
    __slots__=['quality','kind']
    def __init__(self, quality: int, kind: int):
        self.quality=quality
        self.kind=kind
class Tool_Brush:
    __slots__=['quality']
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
class Tool_:
    __slots__=['quality']
    def __init__(self, quality: int):
        self.quality=quality



       
       
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
##class Tool_FluidContainer: # FluidContainer is a component, no need for a separate Tool component

   
    #-----------------------#
    #       Molds           #
    #-----------------------#
   
class Mold_Anvil:
    __slots__=['quality']
    def __init__(self, quality: int):
        self.quality=quality
class Mold_AnvilSmall:
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


class Inventory: #item container
    __slots__=['capacity','mass','data','money','enc']
    # renamed variable "size" --> "mass" 
    def __init__(self, capacity=-1, money=0):
        self.capacity=capacity  # volume total maximum (-1 == infinite) (could be implemented as total encumberance...)
        self.mass=0             # total mass of all entities in the container
        self.enc=0              # current total encumberance value
        self.data=[]            # list of entities
        self.money=money        # current amount of money in the container
       
class FluidContainer:
    __slots__=['capacity','size','data']
    def __init__(self, capacity):
        self.capacity=capacity
        self.size=0
        self.data={}    # { FLUIDTYPE : quantity }

class ReactsWithWater:
    __slots__=['func'] # function that runs when it touches water
    def __init__(self, func):
        self.func=func
class ReactsWithFire: # being on fire makes it explode, transform, etc. (melting is transforming.)
    __slots__=['func'] # function that runs when it touches fire
    def __init__(self, func):
        self.func=func
class ReactsWithAir:
    __slots__=['func']
    def __init__(self, func):
        self.func=func
class ReactsWithElectricity: # / powered by electricity
    __slots__=['func']
    def __init__(self, func):
        self.func=func
       
##class ShattersOnImpact: # this could be a property of MATERIAL (Form) and need not be a new component... At least I think.
##    __slots__=['numParticles','particles']
##    def __init__(self, particles, numParticles):
##        self.particles=particles # object that it creates when shattered
##        self.numParticles=numParticles # number of objects to create


class Injured: # may be obselete with new body system
    __slots__=['injuries']
    def __init__(self, _list):
        self.injuries=_list
class _Injury: # for use by Injured component
    __slots__=['type','name','mods']
    def __init__(self, _type, name, mods):
        self.type=_type # injury type constant
        self.name=name  # name of the injury for display on GUI
        self.mods=mods  # {component : {var : modf}}

##class StatMods:
##    __slots__=['mods']
##    def __init__(self, mods): #{component : {var : modf,}}
##        self.mods=mods
##        #*args, **kwargs):
##        self.mods=[]
##        for arg in args:
##            self.mods.append(arg)
##        for k,w in kwargs:
##            self.mods.append((k,w,))


    #-----------------------#
    #    status effects     #
    #-----------------------#

    #owned by entities currently exhibiting status effect(s)
    # NOTE: when you add a new status effect component,
    #  you must add it into the list of statuses below.

# some statuses have quality, which affects the degree to which
#    you're affected by the status
class StatusFire: # too hot and taking constant damage from the heat
    # This status is unrelated to the fire phenomenon, light,
    #     heat production, etc. Just handles damage over time.
    __slots__=['timer']
    def __init__(self, t=-1):
        self.timer=t
class StatusFrozen: # too cold and taking constant damage from the cold
    __slots__=['timer']
    def __init__(self, t=-1):
        self.timer=t
class StatusAcid: # damage over time, can cause deep wounds
    __slots__=['timer']
    def __init__(self, t=8):
        self.timer=t
class StatusBlind: # vision -90%
    __slots__=['timer']
    def __init__(self, t=30):
        self.timer=t
class StatusDeaf: # hearing -96%
    __slots__=['timer']
    def __init__(self, t=300):
        self.timer=t
class StatusIrritated: # vision -25%, hearing -25%
    __slots__=['timer']
    def __init__(self, t=200):
        self.timer=t
class StatusBleed: # bleed: lose blood each turn, drops blood to the floor, gets your clothes bloody
    __slots__=['timer','quality']
    def __init__(self, t=128, q=1):
        '''
            quality == how many g of blood you lose per turn
            minor: 1
            major arterial bleeding: 15
        '''
        self.timer=t
        self.quality=q
# NOTE: arterial bleed is handled by the BPP artery component having its status set to SEVERED or w/e.
class StatusPain: # in overwhelming pain
    __slots__=['timer']
    def __init__(self, t=6):
        self.timer=t
class StatusParalyzed: # Speed -90%, Atk -15, Dfn -15
    __slots__=['timer']
    def __init__(self, t=6):
        self.timer=t
class StatusSick: # low chance to vomit, cough, sneeze; general fatigue, pain, etc.
    __slots__=['timer']
    def __init__(self, t=600):
        self.timer=t
class StatusVomit: # chance to vomit uncontrollably each turn
    __slots__=['timer']
    def __init__(self, t=48):
        self.timer=t
class StatusCough: # chance to cough uncontrollably each turn
    __slots__=['timer']
    def __init__(self, t=24):
        self.timer=t
class StatusSprint: # Msp +300%
    __slots__=['timer'] # THIS SHOULD NOT BE A STATUS
    def __init__(self, t=12):
        self.timer=t
class StatusFrightening: # add extra scariness for a time
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
class StatusDrunk: # balance -50%
    __slots__=['timer']
    def __init__(self, t=1920):
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
    def __init__(self, t=-1):
        self.timer=t
class StatusDehydrated: # dehydrated
    __slots__=['timer']
    def __init__(self, t=-1):
        self.timer=t
class StatusTired: # sleepy (stamina is a separate thing)
    __slots__=['timer']
    def __init__(self, t=144):
        self.timer=t
class StatusFull: # overeat
    __slots__=['timer']
    def __init__(self, t=384):
        self.timer=t
        
# quantity (non-timed) statuses #
# - statuses for which it would NEVER make sense for it to have a timer,
#   and it has some other quantity indicator of when it will run out.

class StatusDigest:
    __slots__=['satiation','hydration']
    def __init__(self, s=1, h=1):
        self.satiation=c # potential maximum satiation points available
        self.hydration=h # potential maximum hydration points available
        # TODO: add mass of the food(?)

# GLOBAL LISTS OF COMPONENTS #

STATUSES={ # dict of statuses that have a timer
    # component : string that appears when you have the status
    StatusFire      : 'burning',
    StatusFrozen    : 'frozen',
    StatusAcid      : 'corroding',
    StatusBlind     : 'blinded',
    StatusDeaf      : 'deafened',
    StatusIrritated : 'irritated',
    StatusPain      : 'overwhelmed by pain',
    StatusParalyzed : 'paralyzed',
    StatusSick      : 'sick',
    StatusVomit     : 'nauseous',
    StatusCough     : 'coughing fit',
    StatusSprint    : 'sprinting',
    StatusFrightening:'intimidating',
    StatusPanic     : 'panicking',
    StatusHaste     : 'hyper',
    StatusSlow      : 'sluggish',
    StatusDrunk     : 'inebriated',
    StatusHazy      : 'hazy',
    StatusSweat     : 'sweating',
    StatusShiver    : 'shivering',
    StatusEmaciated : 'emaciated',
    StatusDehydrated: 'dehydrated',
    StatusTired     : 'sleepy',
    StatusFull      : 'full (overeating)',
##    StatusBleed, # removed b/c it has quality
    }
##StatusDigest

























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

##class Rots: # thing is susceptible to rotting
##    __slots__=['rot']
##    def __init__(self, rot=0):
##        self.rot=rot    # amount of rot (0-1000)
##class Rusts: # thing is susceptible to rusting
##    __slots__=['rust']
##    def __init__(self, rust=0):
##        self.rust=rust  # amount of rust (0-1000)
##class Wets:
##    __slots__=['wetness']
##    def __init__(self, val=0):
##        self.wetness=val    # how wet is it? Amount == mass of water
##class Dirties:
##    __slots__=['dirtiness']
##    def __init__(self, val=0):
##        self.dirtiness=val  # how dirty is it? Amount == mass of dirt

# RESISTANCE TO THESE THINGS SHOULD BE STORED SEPARATELY. LIKE IN STATS?
##        self.res=res        # resistance to getting dirty (max: 100)



##class Ammo:
##    def __init__(self, ammoType=0):
##        self.ammoType=ammoType
##class UsesAmmo:
##    __slots__=['ammoType','capacity','reloadTime','jamChance']
##    def __init__(self, ammoType=0, capacity=1, reloadTime=1, jamChance=0):
##        self.ammoType=ammoType
##        self.capacity=capacity
##        self.reloadTime=reloadTime
##        self.jamChance=jamChance

      
