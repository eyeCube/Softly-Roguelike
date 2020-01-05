'''
    misc.py
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
    
    #TODO: distribute these functions into other modules
'''

import libtcodpy as libtcod
import textwrap
import math
import copy

import rogue as rog
from const  import *
import orangio  as IO
import components as cmp
import word
import colors
COL = colors.COLORS




# files #

def file_is_line_comment(line):
    return ((line[0]=='/' and line[1]=='/') or line[0]=='\n')

# libtcod #

def color_invert(rgb):
    return libtcod.Color(255-rgb[0],255-rgb[1],255-rgb[2])




'''
# func render_charpage_string
# func render_hud
    (and helper functions for those functions)
'''
class _HUD_Stat(): # helper classes/ functions for the render functions
    def __init__(self, x,y, text,color):
        self.x=x
        self.y=y
        self.text=text
        self.color=color
def _HUD_get_color(stat):
    col=COL['white']
    if stat[:3] == 'HP:':
        col=COL['crystal']
    elif stat[:3] == 'SP:':
        col=COL['magenta']
    elif stat[:4] == 'Atk:':
        col=COL['scarlet']
    elif stat[:4] == 'Dmg:':
        col=COL['scarlet']
    elif stat[:4] == 'Pen:':
        col=COL['scarlet']
    elif stat[:3] == 'DV:':
        col=COL['ltblue']
    elif stat[:3] == 'AV:':
        col=COL['ltblue']
    elif stat[:4] == 'Pro:':
        col=COL['ltblue']
    return col
def _getheight():
    return rog.world().component_for_entity(rog.pc(), cmp.Body).height
def _get(stat):
    return rog.getms(rog.pc(), stat)
def _gets(stat): # get stat
    return rog.getms(rog.pc(), stat)//MULT_STATS
def _geta(att): # get attribute
    return rog.getms(rog.pc(), att)//MULT_ATT
def _getb(stat): # get base
    return rog.world().component_for_entity(rog.pc(), cmp.Stats).__dict__[stat]
def _getba(stat): # get base att
    return rog.world().component_for_entity(rog.pc(), cmp.Stats).__dict__[stat]//MULT_ATT
def _getbs(stat): # get base stat
    return rog.world().component_for_entity(rog.pc(), cmp.Stats).__dict__[stat]//MULT_STATS

# _get_equipment
def __add_eq(equipment, bpname, slot, equipableCompo):
    if slot.item:
        world = rog.world()
        equipable = world.component_for_entity(slot.item, equipableCompo)
        itemname = world.component_for_entity(slot.item, cmp.Name)
        mods=__eqdadd(equipable.mods)
        # covers
        covers = ""
        for cover in slot.covers:
            covers += "| {} ".format(cmp.NAMES[cover])
        #
        equipment += '''    < {bp} {cov}>
        {n} ({hp} / {hpmax})
'''.format(
            bp=bpname,
            n=itemname.name,
            hp=rog.getms(slot.item, "hp"),
            hpmax=rog.getms(slot.item, "hpmax"),
            cov=covers,
            mods=mods
            )
    return equipment
def __eqdadd(mods):
    string=""
    for k, v in mods.items():
        sign = "+" if v > 0 else ""
        name=STATS[k]
        ww=rog.window_w() - 26
        if len(string)-string.count('\n')*ww > ww:
            string += "\n                "
        string += "{n}: {sign}{v}, ".format(n=name, v=v, sign=sign)
    if string: string = string[:-2] # remove final delim
    return string
def _get_equipment(body):
    equipment=""
        
    # human / humanoid shape bodies
    if body.plan==BODYPLAN_HUMANOID:
        # core
        equipment=__add_eq(equipment,"core",body.core.core.slot,
                           cmp.EquipableInCoreSlot)
        equipment=__add_eq(equipment,"front",body.core.front.slot,
                           cmp.EquipableInFrontSlot)
        equipment=__add_eq(equipment,"back",body.core.back.slot,
                           cmp.EquipableInBackSlot)
        equipment=__add_eq(equipment,"hips",body.core.hips.slot,
                           cmp.EquipableInHipsSlot)
        # parts
        for head in body.parts[cmp.BPC_Heads].heads:
            equipment=__add_eq(equipment,"head",head.head.slot,
                           cmp.EquipableInHeadSlot)
            equipment=__add_eq(equipment,"face",head.face.slot,
                           cmp.EquipableInFaceSlot)
            equipment=__add_eq(equipment,"neck",head.neck.slot,
                           cmp.EquipableInNeckSlot)
            equipment=__add_eq(equipment,"eyes",head.eyes.slot,
                           cmp.EquipableInEyesSlot)
            equipment=__add_eq(equipment,"ears",head.ears.slot,
                           cmp.EquipableInEarsSlot)
        i=-1
        for arm in body.parts[cmp.BPC_Arms].arms:
            i+=1
            if arm is None: continue
            a="dominant " if i==0 else "" # first item in list is dominant
            equipment=__add_eq(equipment,"{}arm".format(a),arm.arm.slot,
                           cmp.EquipableInArmSlot)
            equipment=__add_eq(equipment,"{}hand".format(a),arm.hand.slot,
                           cmp.EquipableInHandSlot)
        i=-1
        for leg in body.parts[cmp.BPC_Legs].legs:
            i+=1
            if leg is None: continue
            a="dominant " if i==0 else "" # first item in list is dominant
            equipment=__add_eq(equipment,"{}leg".format(a),leg.leg.slot,
                           cmp.EquipableInLegSlot)
            equipment=__add_eq(equipment,"{}foot".format(a),leg.foot.slot,
                           cmp.EquipableInFootSlot)
    #
    if equipment: equipment = equipment[:-1]
    return equipment
def _get_gauges(meters):
    lgauges=[]
    gauges=""
    if meters.rads > 0:
        lgauges.append( (meters.rads, "{v:>24}: {a:<6}\n".format(v='radiation',a=meters.rads),) )
    if meters.sick > 0:
        lgauges.append( (meters.sick, "{v:>24}: {a:<6}\n".format(v='sickness',a=meters.sick),) )
    if meters.expo > 0:
        lgauges.append( (meters.expo, "{v:>24}: {a:<6}\n".format(v='exposure',a=meters.expo),) )
    if meters.pain > 0:
        lgauges.append( (meters.pain, "{v:>24}: {a:<6}\n".format(v='pain',a=meters.pain),) )
    if meters.fear > 0:
        lgauges.append( (meters.fear, "{v:>24}: {a:<6}\n".format(v='fear',a=meters.fear),) )
    if meters.bleed > 0:
        lgauges.append( (meters.bleed, "{v:>24}: {a:<6}\n".format(v='bleed',a=meters.bleed),) )
    if meters.rust > 0:
        lgauges.append( (meters.rust, "{v:>24}: {a:<6}\n".format(v='rust',a=meters.rust),) )
    if meters.rot > 0:
        lgauges.append( (meters.rot, "{v:>24}: {a:<6}\n".format(v='rot',a=meters.rot),) )
    if meters.wet > 0:
        lgauges.append( (meters.wet, "{v:>24}: {a:<6}\n".format(v='wetness',a=meters.wet),) )
    # sort
    lgauges.sort(key = lambda x: x[0], reverse=True)
    # get all in one string
    for gauge in lgauges:
        gauges += gauge[1]
    if gauges: gauges=gauges[:-1] # remove final '\n'
    return gauges
def _get_effects(world, pc):
    effects=""
    for k,v in cmp.STATUSES.items():
        clsname=type(k).__name__
        if world.has_component(pc, clsname):
            compo=world.component_for_entity(pc, clsname)
            effects += "{v:>24}: {t}\n".format(
                v=v, t=compo.timer )
    if effects: effects=effects[:-1] # remove final '\n'
    return effects

# _get_body_effects
def __gdadd(_dict, status):
    string=""
    mods = _dict[status]
    for k, v in mods.items():
        sign = "+" if v > 0 else ""
        name=STATS[k]
        string += "{n}: {sign}{v}, ".format(n=name, v=v, sign=sign)
    if string: string = string[:-2] # remove final delim
    return string
def __gdmul(_dict, status):
    string=""
    mods = _dict[status]
    for k, v in mods.items():
        name=STATS[k]
        string += "{n}: {v}%, ".format(n=name, v=int(v*100))
    if string: string = string[:-2] # remove final delim
    return string
def _get_body_effects(world, pc): # TODO: finish all of these for each body part, and each BPP for each body part
    fxlist=[] # [ (priority, string,), ... ]
    body = world.component_for_entity(pc, cmp.Body)
    
    # what body type are we?
    # humanoid
    if body.plan == BODYPLAN_HUMANOID:
        
        # function for showing a body part status
        def __f(bppname,status, bpstatusdict, amd=None, mmd=None):
            # amd : add mod dict
            # mmd : mult. mod dict
            if status:

                # priority -- depending on status AND type of body part
                priority = status
                if "scalp" in bppname: # head skin higher priority than regular skin
                    priority += 10
                elif "muscle" in bppname: # muscles have higher priority than skin
                    priority += 20
                elif "bone" in bppname: # bones have high priority
                    priority += 30 # a broken bone is no bueno
                elif "skull" in bppname: # skull has very high priority
                    priority += 40
                elif "brain" in bppname: # brain has very highest priority
                    priority += 50
                    
                mm=""
                if mmd:
                    mm = "\n            [ {} ]".format(
                        __gdmul(mmd, status) )
                am=""
                if amd:
                    am = "\n            [ {} ]".format(
                        __gdadd(amd, status))
                fxlist.append(
                    (priority, "        {bpn}: {eff}{am}{mm}\n".format(
                    bpn=bppname, eff=bpstatusdict[status], am=am, mm=mm ),)
                    )
        # end def

        # for every body part in the plan, if it has a status,
        # add the status

        # core
        
        __f("core skin",body.core.core.skin.status,
            SKINSTATUSES, amd=ADDMODS_BPP_SKINSTATUS )
        __f("core muscle",body.core.core.muscle.status,
            MUSCLESTATUSES, amd=ADDMODS_BPP_TORSO_MUSCLESTATUS )
        
        __f("chest skin",body.core.front.skin.status,
            SKINSTATUSES, amd=ADDMODS_BPP_SKINSTATUS )
        __f("chest muscle",body.core.front.muscle.status,
            MUSCLESTATUSES, amd=ADDMODS_BPP_TORSO_MUSCLESTATUS )
        __f("chest bone",body.core.front.bone.status,
            BONESTATUSES, amd=ADDMODS_BPP_TORSO_BONESTATUS,
            mmd=MULTMODS_BPP_TORSO_BONESTATUS)
        
        __f("hip skin",body.core.hips.skin.status,
            SKINSTATUSES, amd=ADDMODS_BPP_SKINSTATUS )
        __f("hip muscle",body.core.hips.muscle.status,
            MUSCLESTATUSES, amd=ADDMODS_BPP_TORSO_MUSCLESTATUS )
        __f("hip bone",body.core.hips.bone.status,
            BONESTATUSES, amd=ADDMODS_BPP_TORSO_BONESTATUS,
            mmd=MULTMODS_BPP_TORSO_BONESTATUS)
        
        __f("back skin",body.core.back.skin.status,
            SKINSTATUSES, amd=ADDMODS_BPP_SKINSTATUS )
        __f("back muscle",body.core.back.muscle.status,
            MUSCLESTATUSES, amd=ADDMODS_BPP_BACK_MUSCLESTATUS )
        __f("back bone",body.core.back.bone.status,
            BONESTATUSES, amd=ADDMODS_BPP_BACK_BONESTATUS,
            mmd=MULTMODS_BPP_BACK_BONESTATUS)

        # head
        
        __f("scalp",body.parts[cmp.BPC_Heads].heads[0].head.skin.status,
            SKINSTATUSES, amd=ADDMODS_BPP_SKINSTATUS )
        __f("skull",body.parts[cmp.BPC_Heads].heads[0].head.bone.status,
            BONESTATUSES, amd=ADDMODS_BPP_HEAD_BONESTATUS,
            mmd=MULTMODS_BPP_HEAD_BONESTATUS)
        __f("brain",body.parts[cmp.BPC_Heads].heads[0].head.brain.status,
            BRAINSTATUSES, amd=ADDMODS_BPP_BRAINSTATUS,
            mmd=MULTMODS_BPP_BRAINSTATUS)
        
        __f("face skin",body.parts[cmp.BPC_Heads].heads[0].face.skin.status,
            SKINSTATUSES, amd=ADDMODS_BPP_FACE_SKINSTATUS )
        
        __f("neck skin",body.parts[cmp.BPC_Heads].heads[0].neck.skin.status,
            SKINSTATUSES, amd=ADDMODS_BPP_SKINSTATUS )
        __f("neck muscle",body.parts[cmp.BPC_Heads].heads[0].neck.muscle.status,
            MUSCLESTATUSES, amd=ADDMODS_BPP_NECK_MUSCLESTATUS)
        __f("neck bone",body.parts[cmp.BPC_Heads].heads[0].neck.bone.status,
            BONESTATUSES, amd=ADDMODS_BPP_NECK_BONESTATUS,
            mmd=MULTMODS_BPP_NECK_BONESTATUS)

        # arm 1
        
        index = 0
        for arm in body.parts[cmp.BPC_Arms].arms:
            index += 1
            __f("arm {} skin".format(index),
                arm.arm.skin.status,
                SKINSTATUSES, amd=ADDMODS_BPP_SKINSTATUS )
            __f("arm {} muscle".format(index),
                arm.arm.muscle.status,
                MUSCLESTATUSES, amd=ADDMODS_BPP_ARM_MUSCLESTATUS)
            __f("arm {} bone".format(index),
                arm.arm.bone.status,
                BONESTATUSES, amd=ADDMODS_BPP_ARM_BONESTATUS)
            
            __f("hand {} skin".format(index),
                arm.hand.skin.status,
                SKINSTATUSES, amd=ADDMODS_BPP_SKINSTATUS )
            __f("hand {} muscle".format(index),
                arm.hand.muscle.status,
                MUSCLESTATUSES, amd=ADDMODS_BPP_ARM_MUSCLESTATUS)
            __f("hand {} bone".format(index),
                arm.hand.bone.status,
                BONESTATUSES, amd=ADDMODS_BPP_ARM_BONESTATUS)
        # end for

        # leg 1
        
        index = 0
        for leg in body.parts[cmp.BPC_Legs].legs:
            index += 1
            __f("leg {} skin".format(index),
                leg.leg.skin.status,
                SKINSTATUSES, amd=ADDMODS_BPP_SKINSTATUS )
            __f("leg {} muscle".format(index),
                leg.leg.muscle.status,
                MUSCLESTATUSES, amd=ADDMODS_BPP_LEG_MUSCLESTATUS)
            __f("leg {} bone".format(index),
                leg.leg.bone.status,
                BONESTATUSES, amd=ADDMODS_BPP_LEG_BONESTATUS,
                mmd=MULTMODS_BPP_LEG_BONESTATUS)
            
            __f("foot {} skin".format(index),
                leg.foot.skin.status,
                SKINSTATUSES, amd=ADDMODS_BPP_SKINSTATUS )
            __f("foot {} muscle".format(index),
                leg.foot.muscle.status,
                MUSCLESTATUSES, amd=ADDMODS_BPP_LEG_MUSCLESTATUS)
            __f("foot {} bone".format(index),
                leg.foot.bone.status,
                BONESTATUSES, amd=ADDMODS_BPP_LEG_BONESTATUS,
                mmd=MULTMODS_BPP_LEG_BONESTATUS)
        # end for

        
    # end if
    
    # get the return string
    effects = ""
    fxlist.sort(key=lambda x: x[0], reverse=True) # sort by priority
    for eff in fxlist:
        priority, string = eff
        effects += string
    if effects: effects=effects[:-1] # remove final '\n'
    return effects

def _get_skills(compo):
    skills=""
    for const,exp in compo.skills.items():
        skillname=SKILLS[const][1]
        lvl=exp//EXP_LEVEL
        skills += "{n:>24}: lv. {lv} | xp. {xp}\n".format(
            n=skillname, lv=lvl, xp=(exp%EXP_LEVEL))
    if skills: skills=skills[:-1] # remove final '\n'
    return skills

def _get_satiation(body):
    string=""
    satpc = body.satiation / body.satiationMax
    if satpc >= 0.93:
        return "full"
    if satpc >= 0.75:
        return "sated"
    if satpc >= 0.6:
        return "content"
    if satpc >= 0.3:
        return "hungry"
    return "starving"

def _get_hydration(body):
    string=""
    hydpc = body.hydration / body.hydrationMax
    deathValue = 0.9
    if hydpc >= deathValue + (1-deathValue)*0.8:
        return "hydrated"
    if hydpc >= deathValue + (1-deathValue)*0.6:
        return "thirsty"
    if hydpc >= deathValue + (1-deathValue)*0.4:
        return "dehydrated"
    return "severely dehydrated"
def _get_encumberance_mods(pc):
    mods = "\n    [ "
    encbp = rog.get_encumberance_breakpoint(
        rog.getms(pc,'enc'), rog.getms(pc,'encmax') )
    if encbp > 0:
        index = encbp - 1
        mods += "ASP {}%, ".format(int(100*ENCUMBERANCE_MODIFIERS['asp'][index]))
        mods += "MSP {}%, ".format(int(100*ENCUMBERANCE_MODIFIERS['msp'][index]))
        mods += "ATK {}%, ".format(int(100*ENCUMBERANCE_MODIFIERS['atk'][index]))
        mods += "DV {}%, ".format(int(100*ENCUMBERANCE_MODIFIERS['dfn'][index]))
        mods += "PRO {}%, ".format(int(100*ENCUMBERANCE_MODIFIERS['pro'][index]))
        mods += "GRA {}%, ".format(int(100*ENCUMBERANCE_MODIFIERS['gra'][index]))
        mods += "BAL {}% ".format(int(100*ENCUMBERANCE_MODIFIERS['bal'][index]))
    else:
        return ""
    mods += "]"
    return mods


# render character page / render char page / render charpage
# render the entire character info page in one big string
def render_charpage_string(w, h, pc, turn, dlvl):
    # Setup #
    world = rog.world()
    con = libtcod.console_new(w,h)
    name = world.component_for_entity(pc, cmp.Name)
    meters = world.component_for_entity(pc, cmp.Meters)
    creature = world.component_for_entity(pc, cmp.Creature)
    body=world.component_for_entity(pc, cmp.Body)
    effects = _get_effects(world, pc)
    bodystatus = _get_body_effects(world, pc)
    gauges = _get_gauges(world.component_for_entity(pc, cmp.Meters))
    equipment=_get_equipment(world.component_for_entity(pc, cmp.Body))
    skills = _get_skills(world.component_for_entity(pc, cmp.Skills))
    augs=""
    npaugs=0
    nmaugs=0
    satstr=_get_satiation(body)
    hydstr=_get_hydration(body)
    encmods=_get_encumberance_mods(pc)
    
    # create the display format string
    strng = '''
                        {subdelim} identification {subdelim}
                    name{delim}{name}
                 species{delim}{species}
                 faction{delim}{fact}
                     job{delim}{job}
                    mass{delim}{kg} kg
                  height{delim}{cm} cm

                        {subdelim} status {subdelim}
                   satiation: {satstr}
                   hydration: {hydstr}
                (life)----HP{predelim}{hp:>5} / {hpmax:<5}
             (stamina)----SP{predelim}{sp:>5} / {spmax:<5}
        (encumberance)---ENC{predelim}{enc:>5} / {encmax:<5}{tab}{encpc:.2f}%{encmods}

    effects:
{effects}

    body status:
{bodystatus}

    gauge:
             temperature: {temp} ({normalbodytemp})
{gauges}

                        {subdelim} equipment {subdelim}
{equipment}

                        {subdelim} skill {subdelim}
{skills}

                        {subdelim} augmentation {subdelim}
{augs}
        
                        {subdelim} attribute {subdelim}
        (constitution)---CON{predelim}{_con:<2}{attdelim}({bcon}){tab}physical aug.: {paugs} / {paugsmax}
        (intelligence)---INT{predelim}{_int:<2}{attdelim}({bint}){tab}  mental aug.: {maugs} / {maugsmax}
            (strength)---STR{predelim}{_str:<2}{attdelim}({bstr})
             (agility)---AGI{predelim}{_agi:<2}{attdelim}({bagi})
           (dexterity)---DEX{predelim}{_dex:<2}{attdelim}({bdex})
           (endurance)---END{predelim}{_end:<2}{attdelim}({bend})
       
                        {subdelim} statistic {subdelim}
               (speed)---SPD{predelim}{spd:<4}{statdelim}({bspd})
        (attack speed)---ASP{predelim}{asp:<4}{statdelim}({basp})
      (movement speed)---MSP{predelim}{msp:<4}{statdelim}({bmsp})
          (protection)---PRO{predelim}{pro:<4}{statdelim}({bpro})
         (dodge value)----DV{predelim}{dv:<4}{statdelim}({bdv})
         (armor value)----AV{predelim}{av:<4}{statdelim}({bav})
         (penetration)---PEN{predelim}{pen:<4}{statdelim}({bpen})
     (attack / to-hit)---ATK{predelim}{atk:<4}{statdelim}({batk})
              (damage)---DMG{predelim}{dmg:<4}{statdelim}({bdmg})
    (stamina recovery)---SPR{predelim}{spr:<4}{statdelim}({bspr})
             (balance)---BAL{predelim}{bal:<4}{statdelim}({bbal})
           (grappling)---GRA{predelim}{gra:<4}{statdelim}({bgra})
      (counter-strike)---CTR{predelim}{ctr:<4}{statdelim}({bctr})
             (courage)---CRG{predelim}{crg:<4}{statdelim}({bcrg})
        (intimidation)---IDN{predelim}{idn:<4}{statdelim}({bidn})
              (beauty)---BEA{predelim}{bea:<4}{statdelim}({bbea})
   (visual perception)---VIS{predelim}{vis:<4}{statdelim}({bvis})
 (auditory perception)---AUD{predelim}{aud:<4}{statdelim}({baud})
                (mass)----KG{predelim}{kg:<6}{shortdelim}({bkg})
              (height)----CM{predelim}{cm:<4}
        (encumberance)---ENC{predelim}{enc:<4}
    (max.encumberance)ENCMAX{predelim}{encmax:<4}{statdelim}({bencmax})
       
                        {subdelim} resistance {subdelim}
                (heat)---FIR{predelim}{fir:<4}{resdelim}({bfir})
                (cold)---ICE{predelim}{ice:<4}{resdelim}({bice})
          (bio-hazard)---BIO{predelim}{bio:<4}{resdelim}({bbio}){tab}{immbio}
         (electricity)---ELC{predelim}{elc:<4}{resdelim}({belc})
            (physical)---PHS{predelim}{phs:<4}{resdelim}({bphs})
                (pain)---PAI{predelim}{pai:<4}{resdelim}({bpai}){tab}{immpain}
               (bleed)---BLD{predelim}{bld:<4}{resdelim}({bbld}){tab}{immbleed}
               (light)---LGT{predelim}{lgt:<4}{resdelim}({blgt})
               (sound)---SND{predelim}{snd:<4}{resdelim}({bsnd})
                (rust)---RUS{predelim}{rus:<4}{resdelim}({brus}){tab}{immrust}
                 (rot)---ROT{predelim}{rot:<4}{resdelim}({brot}){tab}{immrot}
               (water)---WET{predelim}{wet:<4}{resdelim}({bwet}){tab}{immwater}

'''.format(
        titledelim="~~~~",
        tab="    ",
        delim    ="........",
        subdelim ="--",
        predelim =": ",
        attdelim ="........",
        statdelim="......",
        resdelim ="......",
        shortdelim ="....",
        dlv=dlvl,t=turn,
        # flags
        immbio  ="IMMUNE" if rog.on(pc, IMMUNEBIO) else "",
        immrust ="IMMUNE" if rog.on(pc, IMMUNERUST) else "",
        immrot  ="IMMUNE" if rog.on(pc, IMMUNEROT) else "",
        immwater="IMMUNE" if rog.on(pc, IMMUNEWATER) else "",
        immbleed="IMMUNE" if rog.on(pc, IMMUNEBLEED) else "",
        immpain ="IMMUNE" if rog.on(pc, IMMUNEPAIN) else "",
        # component data
        effects=effects,gauges=gauges,augs=augs,
        equipment=equipment,skills=skills,bodystatus=bodystatus,
        satstr=satstr,hydstr=hydstr,encmods=encmods,
        name=name.name,
        species=SPECIES.get(creature.species, "unknown"),
        fact=FACTIONS.get(creature.faction, "unknown"),
        job=creature.job,
        temp=meters.temp,
        normalbodytemp=37, #TEMPORARY
        kg=_get('mass')/MULT_MASS,bkg=_getb('mass')/MULT_MASS,
        cm=int(_getheight()),
        hp=_getb('hp'),hpmax=_get('hpmax'),
        sp=_getb('mp'),spmax=_get('mpmax'),
        hppc=(_getb('hp')/_get('hpmax')*100),
        sppc=(_getb('mp')/_get('mpmax')*100),
        # attributes
        _str=_geta('str'),_agi=_geta('agi'),_dex=_geta('dex'),
        _end=_geta('end'),_int=_geta('int'),_con=_geta('con'),
        # base attributes
        bstr=_getba('str'),bagi=_getba('agi'),bdex=_getba('dex'),
        bend=_getba('end'),bint=_getba('int'),bcon=_getba('con'),
        # augmentations
        paugs=npaugs, paugsmax=int(_geta('con') * ATT_CON_AUGS),
        maugs=nmaugs, maugsmax=int(_geta('int') * ATT_INT_AUGS),
        # stats
            # TODO: minimum display values, but ONLY way later, like before release, as this is a helpful debug measure.
        atk=_gets('atk'),dmg=_gets('dmg'),pen=_gets('pen'),
        dv=_gets('dfn'),av=_gets('arm'),pro=_gets('pro'),
        ctr=_gets('ctr'),gra=_gets('gra'),bal=_gets('bal'),
        spr=_gets('mpregen'),
        spd=_get('spd'),asp=_get('asp'),msp=_get('msp'),
        crg=_get('courage'),idn=_get('scary'),bea=_get('beauty'),
        vis=_get('sight'),aud=_get('hearing'),
        enc=_get('enc'),encmax=_get('encmax'),
        encpc=(_get('enc') / _get('encmax') * 100),
        # base stats
        batk=_getbs('atk'),bdmg=_getbs('dmg'),bpen=_getbs('pen'),
        bdv=_getbs('dfn'),bav=_getbs('arm'),bpro=_getbs('pro'),
        bctr=_getbs('ctr'),bgra=_getbs('gra'),bbal=_getbs('bal'),
        bspr=_getbs('mpregen'),
        bspd=_getb('spd'),basp=_getb('asp'),bmsp=_getb('msp'),
        bcrg=_getb('courage'),bidn=_getb('scary'),bbea=_getb('beauty'),
        bvis=_getb('sight'),baud=_getb('hearing'),
        bencmax=_getb('encmax'),
        # res
        fir=_get('resfire'),ice=_get('rescold'),phs=_get('resphys'),
        bld=_get('resbleed'),bio=_get('resbio'),elc=_get('reselec'),
        pai=_get('respain'),lgt=_get('reslight'),snd=_get('ressound'),
        rus=_get('resrust'),rot=_get('resrot'),wet=_get('reswet'),
        # base res
        bfir=_getb('resfire'),bice=_getb('rescold'),bphs=_getb('resphys'),
        bbld=_getb('resbleed'),bbio=_getb('resbio'),belc=_getb('reselec'),
        bpai=_getb('respain'),blgt=_getb('reslight'),bsnd=_getb('ressound'),
        brus=_getb('resrust'),brot=_getb('resrot'),bwet=_getb('reswet'),
    )
    return strng
# end def

# render HUD
# render the regular abridged in-game HUD that only shows vitals
def render_hud(w,h,pc,turn,dlvl):
    # Setup #
    
    # TODO: minimum display values (but only after debugging stats/HUD!!!)
    con = libtcod.console_new(w,h)
    name = rog.world().component_for_entity(pc, cmp.Name)
    # TODO: update HUD:
    #  change to show more relevant stats, resistances are less important
    strngStats = "__{name}__|HP: {hp}|SP: {mp}|Speed: {spd}/{asp}/{msp}|Atk: {hit}|Dmg: {dmg}|Pen: {pen}|DV: {dfn}|AV: {arm}|Pro: {pro}|FIR: {fir}|BIO: {bio}|ELC: {elc}|DLvl: {dlv}|T: {t}".format(
        name=name.name,
        hp=_get('hp'),mp=_get('mp'),
        spd=_get('spd'),asp=_get('asp'),msp=_get('msp'),
        dlv=dlvl,t=turn,
        hit=_gets('atk'),dmg=_gets('dmg'),pen=_gets('pen'),
        dfn=_gets('dfn'),arm=_gets('arm'),pro=_gets('pro'),
        fir=_get('resfire'),bio=_get('resbio'),elc=_get('reselec'),
    )
    stats=strngStats.split('|')
    statLines=[[]]
    tot=0
    y=0
    for stat in stats:
        lenStat=len(stat) + 1
        col=_HUD_get_color(stat)
        new=_HUD_Stat(tot, y, stat, col)
        tot += lenStat
        if tot >= rog.window_w():
            tot=lenStat
            y += 1 # draw on next line
            new.x=0; new.y=y
            statLines.append([new])
            continue
        statLines[-1].append(new)
    
    
    # Print #
    for line in statLines:
        for stat in line:
            if stat.y > h-1: continue
            libtcod.console_set_default_foreground(con, stat.color)
            libtcod.console_print(con, stat.x,stat.y, stat.text)
    #
    
    return con
# end def



'''
#
# func draw_textbox_border
#
'''
def rectangle(con,x,y,w,h,border):
    
    con_box = libtcod.console_new(w,h)
    
    b = border
    ch_hw   = CH_HW[b]; ch_vw   = CH_VW[b]; ch_tlc  = CH_TLC[b]
    ch_trc  = CH_TRC[b];ch_brc  = CH_BRC[b];ch_blc  = CH_BLC[b]
        
    # sides
    for i in range(w-2):
        libtcod.console_put_char_ex(con_box, i+1,0,   ch_hw, COL['white'],COL['black'])
    for i in range(w-2):
        libtcod.console_put_char_ex(con_box, i+1,h-1, ch_hw, COL['white'],COL['black'])
    for i in range(h-2):
        libtcod.console_put_char_ex(con_box, 0,i+1,   ch_vw, COL['white'],COL['black'])
    for i in range(h-2):
        libtcod.console_put_char_ex(con_box, w-1,i+1, ch_vw, COL['white'],COL['black'])
    # corners
    libtcod.console_put_char_ex(con_box, 0,0,       ch_tlc,  COL['white'],COL['black'])
    libtcod.console_put_char_ex(con_box, w-1,0,     ch_trc,  COL['white'],COL['black'])
    libtcod.console_put_char_ex(con_box, 0,h-1,     ch_blc,  COL['white'],COL['black'])
    libtcod.console_put_char_ex(con_box, w-1,h-1,   ch_brc,  COL['white'],COL['black'])

    # blit
    libtcod.console_blit(con_box, 0,0,w,h,  # Source
                         con,   x,y)    # Destination
    libtcod.console_delete(con_box)
#




'''
#
# func textbox
#
# display text box with border and word wrapping
#
    Args:
    x,y,w,h     location and size
    text        display string
    border      border style. None = No border
    wrap        whether to use automatic word wrapping
    margin      inside-the-box text padding on top and sides
    con         console on which to blit textbox, should never be 0
    disp        display mode: 'poly','mono'

'''

def dbox(x,y,w,h,text, wrap=True,border=0,margin=0,con=0,disp='poly') :
    con_box = libtcod.console_new(w,h)
    
    pad=0 if border == None else 1
    offset  = margin + pad
    fulltext= textwrap.fill(text, w-2*(margin+pad)) if wrap else text
    boxes   = word.split_stanza(fulltext, h-2*(margin+pad)) if disp=='poly' else [fulltext]
    length  = len(boxes)
    i=0
    for box in boxes:
        i += 1
        libtcod.console_clear(con_box)
    #   print
        if border is not None: rectangle(con_box,0,0, w,h, border)
        libtcod.console_print(
            con_box, offset, offset, box)
        put_text_special_colors(con_box, box, offset)
        libtcod.console_blit( con_box, 0,0,w,h, # Source
                              con,     x,y)     # Destination
    #   wait for user input to continue...
        if i < length: 
            rog.blit_to_final(con,0,0)
            rog.refresh()
            while True:
                reply=rog.Input(x+w-1, y+h-1, mode="wait")
                if (reply==' ' or reply==''): break
    libtcod.console_delete(con_box)

def put_text_special_colors(con, txt, offset):
    #   make dictionaries
        string_colors={
            "B" : 'blue',
            "R" : 'red',
            "G" : 'gray',
            "N" : 'green',
            "Y" : 'yellow',
        }
        color_strings={}
        for k,v in string_colors.items():
            color_strings.update({v : k})
    #   get a string of color data
        colorString=txt.lower()
        for replace,col in colors.colored_strings:
            colChar=color_strings[col]
            colorString=colorString.replace(replace, colChar*len(replace))
    #   iterate through that string, changing color on con
        yy=0
        xx=-1
        for ch in colorString:
            xx += 1
            if ch == '\n':
                xx=-1
                yy += 1
                continue
            col=string_colors.get(ch,None)
            if col:
                libtcod.console_set_char_foreground(
                    con, offset + xx, offset + yy, COL[col])



'''
    itemize generator

    like enumerate() but with letters
    - yields n,item with n as:
        - a-z first
        - then A-Z
        - then 0-9
        Then truncates any items remaining in list.
    Lots of magic numbers here. These are ASCII codes.
'''

def itemize(items):
    ch=0
    start=97                    #<- start with a-z
    for item in items:
        if ch >= 26:
            ch=0
            if start == 97:
                start=65        #<- start with A-Z
            else:
                start=48        #<- start with 0-9
        elif (ch > 9 and start == 48):
            break               #<- finished early, too many items
        yield (chr(ch+start),item)
        ch += 1
        
# to reverse the num-to-char method from itemize()
def get_num_from_char(char):
    result=ord(char)
    if result >= 97:
        return result - 97
    elif result >= 65:
        return result - 65 + 26
    else: return result - 48 + 26*2




















''' OLD HUD with HP and MP bars

    def _drawBar(con, x,y, val,Max, w,col,bg=COL['black']):
        numbars = math.ceil((val/Max)*w)
        for i in range(numbars):
            libtcod.console_set_char_background(con, x+i, 0, col)
            libtcod.console_set_char_foreground(con, x+i, 0, bg)
            

    hp_x1       = 16
    mp_x1       = 32
    text_offset = 6
    hp_x2       = hp_x1 + text_offset
    mp_x2       = mp_x1 + text_offset
    bar_offset  = 4
    hpbar_x     = hp_x1 + bar_offset
    mpbar_x     = mp_x1 + bar_offset
    barsize     = 10
    hp_low          = 5
    mp_low          = 5
    col_hp_full     = COL['accent']
    col_hp_good     = COL['green']
    col_hp_exposed  = COL['magenta']
    col_hp_danger   = COL['orange']
    col_hp_panic    = COL['red']
    col_mp_full     = COL['accent']
    col_mp_good     = COL['blue']
    col_mp_exposed  = COL['purple']
    col_mp_danger   = COL['yellow']
    col_mp_panic    = COL['red']
    
    spd_x       = 48
    turn_x      = 70
   # Draw Stats #
    
    # HP,MP
    libtcod.console_set_default_background(con,COL['dkbrown'])
    libtcod.console_clear(con)
    libtcod.console_set_default_foreground(con,COL['accent'])
    libtcod.console_print(con,0,0,name)
    libtcod.console_print(con,hp_x1,0,"lo: {}".format("-"*barsize))
    libtcod.console_print(con,mp_x1,0,"hi: {}".format("-"*barsize))
    libtcod.console_print(con,hp_x2,0,health)
    libtcod.console_print(con,mp_x2,0,mana)
    # Bars #
    
    # HP bar
    if hpmax <= hp_low: col=col_hp_danger
    elif hpmax == hp:   col=col_hp_full
    else:               col=col_hp_good
    _drawBar(con, hpbar_x,0, hp,hpmax, barsize,col)
    # low HP
    if hp == 0:
        col=col_hp_panic if hpmax <= 5 else col_hp_exposed
        _drawBar(con, hpbar_x,0, 1,1, barsize,col)
    
    # MP bar
    if mpmax <= mp_low: col=col_mp_danger
    elif mpmax == mp:   col=col_mp_full
    else:               col=col_mp_good
    _drawBar(con, mpbar_x,0, mp,mpmax, 10,col)
    # low MP
    if mp == 0:
        col=col_mp_panic if mpmax <= 5 else col_mp_exposed
        _drawBar(con, mpbar_x,0, 1,1, barsize,col)
    #
    '''


'''
    # for each stat in this list, get a modifier text or an empty string
    lis = ('atk','dmg','dfn','arm','spd','asp','msp')
    base = {}
    for k in lis:
        attr = getattr(stats,k)
        if not (attr==_get(k)):
            base.update({k : " ({})".format(attr)})
        else: base.update({k : ""})
'''



'''  {nam}

Zeal    {hp}
Health  {hpmax}
Sanity  {mp}
Wisdom  {mpmax}

Hit  {atk}{Atk}
Dmg  {dmg}{Dmg}
DV   {dfn}{Dfn}
AV   {arm}{Arm}

AP   {nrg}
Spd  {spd}{Spd}
Hspd {asps}{asp}{Asp}
Mspd {msps}{msp}{Msp}















Turn : {turn}

GameTime: 
v_0.15.format(
nam= pc.name,
hp= _get('hp'), hpmax= _get('hpmax'), mp= _get('mp'), mpmax= _get('mpmax'),
nrg= pc.stats.nrg,
asps= ('+' if _get('asp') >=0 else ''), asp= _get('asp'),
msps= ('+' if _get('msp') >=0 else ''), msp= _get('msp'),
atk= _get('atk'), dfn= _get('dfn'), dmg= _get('dmg'), arm= _get('arm'),
spd= _get('spd'),
turn= turn,
Spd= base['spd'], Asp= base['asp'], Msp= base['msp'],
Atk= base['atk'], Dfn= base['dfn'], Dmg= base['dmg'], Arm= base['arm'],
)'''

''' lvl= pc.stats.lvl, exp= pc.stats.exp,
req=exp_req,
'''
'''
stg= _get('str'), agi= _get('agi'), dex= _get('dex'),
mnd= _get('mnd'), end= _get('end'), chm= _get('chr'),
Str= base['str'], Agi= base['agi'], Dex= base['dex'],
Mnd= base['mnd'], End= base['end'], Chr= base['chr'],
'''





