'''
    dialogue.py
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
import rogue as rog
import components as cmp
import dice
import random
import math
import messages

# Player -on- NPC dialogue #

MESSAGES={
TALK_INTRODUCTION   :(messages.INTRODUCTION,None,),
TALK_PESTER         :(messages.PESTER,None,),
TALK_ASKQUESTION    :(messages.QUESTION_SUCCESS,messages.QUESTION_FAILURE,),
TALK_GOSSIP         :(messages.GOSSIP_SUCCESS,messages.GOSSIP_FAILURE),
TALK_INTERROGATE    :(messages.INTERROGATE_SUCCESS,messages.INTERROGATE_FAILURE,),
TALK_ASKFAVOR       :(messages.ASKFAVOR_SUCCESS,messages.ASKFAVOR_FAILURE,),
TALK_BEG            :(messages.BEG_SUCCESS,messages.BEG_FAILURE,),
TALK_BARTER         :(messages.BARTER_SUCCESS,messages.BARTER_FAILURE,),
TALK_TORTURE        :(messages.TORTURE_SUCCESS,messages.TORTURE_FAILURE,),
TALK_CHARM          :(messages.CHARM_SUCCESS,messages.CHARM_FAILURE,),
TALK_BOAST          :(messages.BOAST_SUCCESS,messages.BOAST_FAILURE,),
TALK_SMALLTALK      :(messages.SMALLTALK_SUCCESS,messages.SMALLTALK_FAILURE,),
TALK_BRIBERY        :(messages.BRIBERY_SUCCESS,messages.BRIBERY_FAILURE,),
TALK_INTIMIDATION   :(messages.INTIMIDATION_SUCCESS,messages.INTIMIDATION_FAILURE,),
TALK_FLATTERY       :(messages.FLATTERY_SUCCESS,messages.FLATTERY_FAILURE,),
TALK_FLIRTATION     :(messages.FLIRTATION_SUCCESS,messages.FLIRTATION_FAILURE,),
TALK_DEBATE         :(messages.DEBATE_SUCCESS,messages.DEBATE_FAILURE,),
TALK_TAUNT          :(messages.TAUNT_SUCCESS,messages.TAUNT_FAILURE,),
    }

PERSONALITY_STRINGS={
PERSON_NONE                 : "NONE",
PERSON_PROUD                : "proud",
PERSON_LOWSELFESTEEM        : "low-self-esteem",
PERSON_ARGUMENTATIVE        : "argumentative",
PERSON_NONCONFRONTATIONAL   : "non-confrontational",
PERSON_OUTGOING             : "outgoing",
PERSON_SHY                  : "shy",
PERSON_INDEPENDENT          : "independent",
PERSON_CODEPENDENT          : "codependent",
PERSON_BUBBLY               : "bubbly",
PERSON_LOWENERGY            : "low-energy",
PERSON_MOTIVATED            : "motivated",
PERSON_UNMOTIVATED          : "unmotivated",
PERSON_RELAXED              : "relaxed",
PERSON_UPTIGHT              : "uptight",
PERSON_PROACTIVE            : "proactive",
PERSON_APATHETIC            : "apathetic",
    }

def _change_disposition(ent, amt):
    print("ent {} disp change: {}".format(rog.getname(ent), amt))
    rog.world().component_for_entity(ent,cmp.Disposition).disposition += amt

def _get_likes   (personality:int): return PERSONALITIES[personality][1]
def _get_dislikes(personality:int): return PERSONALITIES[personality][2]


    #-----------------------------#
    # response / reaction by NPCS #
    #-----------------------------#

# get possible responses
def __eval(
    personality_string: str, disposition:int, padding:int,
    meta: dict, lis: list
    ):
    DMAX = MAX_DISPOSITION
    for k,v in meta.items():
        if (k=="generic" or k==personality_string):
            for disp_ratio, strings in v.items():
                if (disposition >= rog.around(disp_ratio*DMAX)
                    and disposition <= rog.around((disp_ratio+padding)*DMAX)
                    ):
                    for string in strings:
                        lis.append(string)
def _get_possible_responses(
    talk_type:int, personality: int, disposition: int, padding=0.2
    ) -> tuple:
    ''' get a list of possible NPC text dialogue responses given:
        talk_type:   the type of conversation,
        personality: the personality type of the dialogue partner
        disposition: the sentiments the person has towards the PC
        padding:     float, affects size of range of possibilities
        Return both generic and personality-specific responses together.
            Format: (strings for success, strings for failure,)
    '''
    DMAX = MAX_DISPOSITION
    on_success = []
    on_failure = []
    meta_success = MESSAGES[talk_type][0]
    meta_failure = MESSAGES[talk_type][1]
    pid = PERSONALITY_STRINGS[personality]
    __eval(pid, disposition, padding, meta_success, on_success)
    __eval(pid, disposition, padding, meta_failure, on_failure)
    return (on_success, on_failure,)

def _get_response(possible: tuple, success: bool) -> str:
    ''' get response from list of possible responses '''
    lis = possible[0] if success else possible[1]
    response = random.choice(lis)
    return response

def _get_response_full(
    talk_type: int, possible: tuple, success: bool
    ) -> tuple:
    ''' Return a feedback string for failure or success,
        as well as the response by the NPC, given the possible options
    '''
    successfailure = "success" if success else "failure"
    cap = "<{} {}>".format(talk_type, successfailure)
    string = _get_response(possible, success)
    return (cap, string,)

def _get_reaction(
    ent:int, persuasion_type:int, personality:int, disposition:int,
    mx=1, value=0, style=0
    ) -> int:
    ''' get reaction from an entity based on conversational parameters
        mx: multiplier for intensity
        value: value of transaction, if it's a barter or bribe
        Returns >0 values for positive reactions, <0 for negative
            the greater the value, the higher the intensity
    '''
    world=rog.world()
    pc=rog.pc()
    DMAX = MAX_DISPOSITION
    reaction = -20  # default to a negative reaction
    
    # get stats for player
    speech_bonus = rog.getskill(pc, SKL_PERSUASION)
    speech_penalty = max(0, MAX_SKILL - speech_bonus)
    pc_idn = rog.getms(pc, 'idn')
    pc_bea = rog.getms(pc, 'bea')
    pc_pos = world.component_for_entity(pc, cmp.Position)
    
    # get stats for conversational partner
    ent_sight = rog.getms(ent,'sight')
    ent_cansee = rog.can_see(ent, pc_pos.x,pc_pos.y, ent_sight)
    
    # (perceived) value of the transaction
    value_modf = max(1, (value//MULT_VALUE)*0.1)
    if world.has_component(ent, cmp.NeverAcceptsBribes):
        value_modf = 1
    
    # intensity of the conversation based on type of conversation / persuasion
    intensity = value_modf
    intensity = max(intensity, intensity * pc_idn * 0.05)
    if persuasion_type==TALK_TORTURE:
        intensity = 10 * intensity
    elif persuasion_type==TALK_INTIMIDATION:
        intensity = 5 * intensity
    elif persuasion_type==TALK_INTERROGATE:
        intensity = 3 * intensity
    elif persuasion_type==TALK_DEBATE:
        intensity = 2 * intensity
    elif persuasion_type==TALK_FLIRTATION:
        intensity = 2 * intensity
    elif persuasion_type==TALK_BEG:
        intensity = 2 * intensity
    elif persuasion_type==TALK_BARTER:
        intensity = intensity + 0.1 * (value//MULT_VALUE)
    elif persuasion_type==TALK_BRIBERY:
        intensity = intensity + 0.05 * (value//MULT_VALUE)
    
    # generic reaction to your appearance and skill
    reaction += dice.roll(20)       # add element of random chance
    reaction += speech_bonus * 0.1  # add speech modifier
        # attraction
    attraction = 0
    pc_isfemale = rog.get_gender(pc)=="female"
    pc_ismale = rog.get_gender(pc)=="male"
    if (ent_cansee and pc_isfemale
        and world.has_component(ent, cmp.AttractedToWomen)
        ):
        intensity += 1
        attraction += 1 + pc_bea//10
    elif (ent_cansee and pc_ismale
        and world.has_component(ent, cmp.AttractedToMen)
        ):
        intensity += 1
        attraction += -1 + pc_idn//10 - (0.001 * pc_idn**2) + pc_bea//20
    reaction += attraction
    
    # likes and dislikes
    likes=_get_likes(personality)
    dislikes=_get_dislikes(personality)
            # persuasion types
    if persuasion_type == likes[0]:
        reaction += ( 0.01*DMAX + speech_bonus * 1 * mx ) * intensity
    elif persuasion_type == dislikes[0]:
        reaction -= ( 0.02*DMAX + speech_penalty * 0.1 * mx ) * intensity
    
    # special cases
    if (world.has_component(ent, cmp.NeverAcceptsBribes)
        and persuasion_type==TALK_BRIBERY):
        reaction = -0.05 * DMAX * mx
    if personality==PERSON_NONCONFRONTATIONAL:
        reaction -= (intensity - 2)
    if persuasion_type==TALK_TORTURE:
        reaction -= 0.1 * DMAX * mx
    if (persuasion_type==TALK_BEG and personality==PERSON_PROUD):
        reaction -= 0.05 * DMAX * mx
    elif (persuasion_type==TALK_INTERROGATE and personality==PERSON_RELAXED):
        reaction -= 0.02 * DMAX * mx
    elif (persuasion_type==TALK_CHARM and personality==PERSON_LOWENERGY):
        reaction -= 0.01 * DMAX * mx
    elif (persuasion_type==TALK_CHARM and personality==PERSON_BUBBLY):
        reaction += 0.01 * DMAX * mx
    elif (persuasion_type==TALK_BOAST and personality==PERSON_PROACTIVE):
        reaction -= 0.01 * DMAX * mx
    elif (persuasion_type==TALK_BOAST and personality==PERSON_MOTIVATED):
        reaction += 0.01 * DMAX * mx
    
    return math.ceil(abs(reaction)) * rog.sign(reaction)
# end def


    #-------------------#
    # public interface  #
    #-------------------#

def dialogue(ent:int, style=0):
    ''' wrapper dialogue function '''
    world=rog.world()
    if not world.has_component(ent,cmp.Speaks):
        return False
    newdisp = greet(ent, style=style)
    dispcompo=world.component_for_entity(ent,cmp.Disposition)
    personality=world.component_for_entity(ent,cmp.Personality).personality
    dispcompo.disposition = newdisp
    print("New disposition: ", dispcompo.disposition)
    menu={}
    menuitems=[]
    for k,v in PERSUASION.items():
        menu[v] = k
        menuitems.append(v)
    entn = world.component_for_entity(ent,cmp.Name)
    opt = rog.menu(
        "{}{}".format(TITLES[entn.title],entn.name),
        0,0, menuitems
        )
    result = menu[opt]
    _FUNCS[result](ent, personality, dispcompo.disposition, style=style)
# end def

def greet(ent:int, style=0) -> int:
    ''' introduce self / attempt to init conversation '''
    pc=rog.pc()
    world=rog.world()
    personality=world.component_for_entity(ent,cmp.Personality).personality
    dispcompo=world.component_for_entity(ent,cmp.Disposition)
    # new disposition after dialogue concludes
    new_disposition = dispcompo.disposition
    # effective disposition during this dialogue (not the new disposition)
    ed = dispcompo.disposition + _get_reaction(
        ent, TALK_GREETING, personality, dispcompo.disposition,
        style=style, mx=0.5
        )
    new_disposition += rog.sign(ed) # just nudge disposition
    fdisp = ed / MAX_DISPOSITION
    
    # roll for speech success
    speech_bonus = rog.getskill(pc, SKL_PERSUASION)
    roll=dice.roll(100) + speech_bonus
    if fdisp < 0.4:
        roll -= 8/fdisp
    else:
        roll += 100*fdisp
    # cases
    if roll <= 0:
        _response(ent, RESPONSE_REJECTION)
    else:
        _response(ent, RESPONSE_ACCEPT)
    return new_disposition
# end def

def _response(ent:int, response_type:int):
    record(ent, response_type)

def record(ent:int, memory):
    world=rog.world()
    if world.has_component(ent, cmp.ConversationMemory):
        compo=world.component_for_entity(ent, cmp.ConversationMemory)
        compo.memories.append(memory)
        if len(compo.memories) > compo.max_len:
            compo.memories.pop(0)
    else:
        world.add_component(ent, cmp.ConversationMemory(
            MAX_NPC_CONVO_MEMORIES, memory))
# end def
        
def forget(self, n=-1):
    world=rog.world()
    if world.has_component(ent, cmp.ConversationMemory):
        compo=world.component_for_entity(ent, cmp.ConversationMemory)
        if n==-1:
            compo.memories=[]
        else:
            for _ in range(n): compo.memories.pop(0)
        return True
    return False
# end def

    
def init_convo(ent:int, style=0):
    pass

    #---------------------------------#
    # persuasion / conversation types #
    #---------------------------------#

def _talk(success:bool, ttype:int, personality:int, disposition:int, padding=0.2) -> str:
    possible=_get_possible_responses(ttype,personality,disposition,padding)
    response=_get_response(possible, success)
    print(response)
    return response

def talk_introduce(ent:int, personality:int, disposition:int, style=0) -> str:
    ttype = TALK_INTRODUCTION
    reaction=_get_reaction(ent, ttype, personality, disposition)
    _change_disposition(ent, reaction)
    print("introduction {}: {}".format(rog.getname(ent),reaction))
    return _talk(success, ttype, personality, disposition, padding=0.1)

def talk_barter(ent:int, personality:int, disposition:int, style=0) -> str:
    ttype = TALK_BARTER
    reaction=_get_reaction(ent, ttype, personality, disposition)
    _change_disposition(ent, reaction)
    success = (reaction > 0)
    print("barter {}: {}, {}".format(rog.getname(ent),success,reaction))
    return _talk(success, ttype, personality, disposition, padding=1)

def talk_question(ent:int, personality:int, disposition:int, style=0) -> str:
    ttype = TALK_QUESTION
    reaction=_get_reaction(ent, ttype, personality, disposition)
    _change_disposition(ent, reaction)
    success = (reaction > 0)
    print("ask question {}: {}, {}".format(rog.getname(ent),success,reaction))
    return _talk(success, ttype, personality, disposition)

def talk_interrogate(ent:int, personality:int, disposition:int, style=0) -> str:
    ttype = TALK_INTERROGATE
    reaction=_get_reaction(ent, ttype, personality, disposition)
    _change_disposition(ent, reaction)
    success = (reaction > 0)
    print("interrogate {}: {}, {}".format(rog.getname(ent),success,reaction))
    return _talk(success, ttype, personality, disposition)

def talk_gossip(ent:int, personality:int, disposition:int, style=0) -> str:
    ttype = TALK_GOSSIP
    reaction=_get_reaction(ent, ttype, personality, disposition)
    _change_disposition(ent, reaction)
    success = (reaction > 0)
    print("gossip {}: {}, {}".format(rog.getname(ent),success,reaction))
    return _talk(success, ttype, personality, disposition)

def talk_torture(ent:int, personality:int, disposition:int, style=0) -> str:
    ttype = TALK_TORTURE
    reaction=_get_reaction(ent, ttype, personality, disposition)
    _change_disposition(ent, reaction)
    success = (reaction > 0)
    print("torture {}: {}, {}".format(rog.getname(ent),success,reaction))
    return _talk(success, ttype, personality, disposition)

def talk_askfavor(ent:int, personality:int, disposition:int, style=0) -> str:
    ttype = TALK_ASKFAVOR
    reaction=_get_reaction(ent, ttype, personality, disposition)
    _change_disposition(ent, reaction)
    success = (reaction > 0)
    print("ask favor {}: {}, {}".format(rog.getname(ent),success,reaction))
    return _talk(success, ttype, personality, disposition)

def talk_beg(ent:int, personality:int, disposition:int, style=0) -> str:
    ttype = TALK_BEG
    reaction=_get_reaction(ent, ttype, personality, disposition)
    _change_disposition(ent, reaction)
    success = (reaction > 0)
    print("beg {}: {}, {}".format(rog.getname(ent),success,reaction))
    return _talk(success, ttype, personality, disposition)
    
def talk_charm(ent:int, personality:int, disposition:int, style=0) -> str:
    ttype = TALK_CHARM
    reaction=_get_reaction(ent, ttype, personality, disposition)
    _change_disposition(ent, reaction)
    success = (reaction > 0)
    print("charm {}: {}, {}".format(rog.getname(ent),success,reaction))
    return _talk(success, ttype, personality, disposition)

def talk_boast(ent:int, personality:int, disposition:int, style=0) -> str:
    ttype = TALK_BOAST
    reaction=_get_reaction(ent, ttype, personality, disposition)
    _change_disposition(ent, reaction)
    success = (reaction > 0)
    print("boast {}: {}, {}".format(rog.getname(ent),success,reaction))
    return _talk(success, ttype, personality, disposition)

def talk_smalltalk(ent:int, personality:int, disposition:int, style=0) -> str:
    ttype = TALK_SMALLTALK
    reaction=_get_reaction(ent, ttype, personality, disposition)
    _change_disposition(ent, reaction)
    success = (reaction > 0)
    print("smalltalk {}: {}, {}".format(rog.getname(ent),success,reaction))
    return _talk(success, ttype, personality, disposition, padding=1)

def talk_bribe(ent:int, personality:int, disposition:int, style=0) -> str:
    ttype = TALK_BRIBERY
    reaction=_get_reaction(ent, ttype, personality, disposition)
    _change_disposition(ent, reaction)
    success = (reaction > 0)
    print("bribe {}: {}, {}".format(rog.getname(ent),success,reaction))
    return _talk(success, ttype, personality, disposition)

def talk_intimidate(ent:int, personality:int, disposition:int, style=0) -> str:
    ttype = TALK_INTIMIDATION
    reaction=_get_reaction(ent, ttype, personality, disposition)
    _change_disposition(ent, reaction)
    success = (reaction > 0)
    print("intimidate {}: {}, {}".format(rog.getname(ent),success,reaction))
    return _talk(success, ttype, personality, disposition, padding=1)

def talk_flatter(ent:int, personality:int, disposition:int, style=0) -> str:
    ttype = TALK_FLATTERY
    reaction=_get_reaction(ent, ttype, personality, disposition)
    _change_disposition(ent, reaction)
    success = (reaction > 0)
    print("flatter {}: {}, {}".format(rog.getname(ent),success,reaction))
    return _talk(success, ttype, personality, disposition)

def talk_flirt(ent:int, personality:int, disposition:int, style=0) -> str:
    ttype = TALK_FLIRTATION
    reaction=_get_reaction(ent, ttype, personality, disposition)
    _change_disposition(ent, reaction)
    success = (reaction > 0)
    print("flirt {}: {}, {}".format(rog.getname(ent),success,reaction))
    return _talk(success, ttype, personality, disposition)

def talk_debate(ent:int, personality:int, disposition:int, style=0) -> str:
    ttype = TALK_DEBATE
    reaction=_get_reaction(ent, ttype, personality, disposition)
    _change_disposition(ent, reaction)
    success = (reaction > 0)
    print("debate {}: {}, {}".format(rog.getname(ent),success,reaction))
    return _talk(success, ttype, personality, disposition)

def talk_pester(ent:int, personality:int, disposition:int, style=0) -> str:
    ttype = TALK_PESTER
    reaction=_get_reaction(ent, ttype, personality, disposition)
    _change_disposition(ent, reaction)
    print("pester {}: {}".format(rog.getname(ent),reaction))
    return _talk(True, ttype, personality, disposition, padding=1)

def talk_taunt(ent:int, personality:int, disposition:int, style=0) -> str:
    ttype = TALK_TAUNT
    reaction=_get_reaction(ent, ttype, personality, disposition)
    _change_disposition(ent, reaction)
    success = (reaction > 0)
    print("taunt {}: {}, {}".format(rog.getname(ent),success,reaction))
    return _talk(True, ttype, personality, disposition, padding=1)

    #-----------------------------------------------#
    # constants (relying on the above declarations) #
    #-----------------------------------------------#

_FUNCS={
TALK_ASKQUESTION    : talk_question,
TALK_INTERROGATE    : talk_interrogate,
TALK_ASKFAVOR       : talk_askfavor,
TALK_GOSSIP         : talk_gossip,
TALK_BEG            : talk_beg,
TALK_BARTER         : talk_barter,
TALK_TORTURE        : talk_torture,
TALK_CHARM          : talk_charm,
TALK_BOAST          : talk_boast,
TALK_SMALLTALK      : talk_smalltalk,
TALK_BRIBERY        : talk_bribe,
TALK_INTIMIDATION   : talk_intimidate,
TALK_FLATTERY       : talk_flatter,
TALK_FLIRTATION     : talk_flirt,
TALK_DEBATE         : talk_debate,
TALK_PESTER         : talk_pester,
TALK_TAUNT          : talk_taunt,
    }


#--------------------------END OF CODE------------------------------#





















