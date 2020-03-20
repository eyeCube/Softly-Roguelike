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

# Player -on- NPC dialogue #

def _like(ent, amt):
    rog.world().component_for_entity(ent,cmp.Disposition).disposition += amt
def _dislike(ent, amt):
    rog.world().component_for_entity(ent,cmp.Disposition).disposition -= amt

def _get_likes   (personality:int): return PERSONALITIES[personality][1]
def _get_dislikes(personality:int): return PERSONALITIES[personality][2]
def _get_reaction(
    ent:int, persuasion_type:int, personality:int, disposition:int,
    style=0, mx=1
    ):
    ''' get reaction from an entity based on conversational parameters
        Returns >0 values for positive reactions, <0 for negative
            the greater the value, the higher the intensity
    '''
    DMAX = MAX_DISPOSITION
    reaction -= 20  # default to a negative reaction
    speech_bonus = rog.getskill(rog.pc(), SKL_PERSUASION)
    speech_penalty = max(0, MAX_SKILL - speech_bonus)
    
    # generic reaction to your appearance and skill
    reaction += dice.roll(20)       # add element of random chance
    reaction += speech_bonus * 0.1  # add speech modifier
    
    # TODO: factor beauty, intimidation
    #...
    
    # likes and dislikes
    likes=_get_likes(personality)
    dislikes=_get_dislikes(personality)
            # persuasion types
    if persuasion_type == likes[0]:
        reaction += ( 0.01*DMAX + speech_bonus * 1 * mx )
    elif persuasion_type == dislikes[0]:
        reaction -= ( 0.02*DMAX + speech_penalty * 0.1 * mx )
            # styles of conversation
    if style == likes[1]:
        reaction += ( 0.001*DMAX + speech_bonus * 1 * mx )
    elif style == dislikes[1]:
        reaction -= ( 0.002*DMAX + speech_penalty * 0.1 * mx )
    
    # special cases
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

    # styles of conversation
    if style==CONVO_FRIENDLY:
        _like(ent, 1)
    elif style==CONVO_POLITE:
        _like(ent, 1)
    elif style==CONVO_RESPECTFUL:
        _like(ent, 2)
    elif style==CONVO_RUDE:
        _dislike(ent, 1)
    elif style==CONVO_DISRESPECTFUL:
        _dislike(ent, 2)
    
    return math.ceil(abs(reaction)) * rog.sign(reaction)
# end def

def dialogue(ent:int, style=0):
    # wrapper dialogue function
    world=rog.world()
    if not world.has_component(ent,cmp.Speaks):
        return False
    newdisp = greet(ent, style=style)
    dispcompo=world.component_for_entity(ent,cmp.Disposition)
    personality=world.component_for_entity(ent,cmp.Personality).personality
    dispcompo.disposition = newdisp
    menu={}
    for k,v in PERSUASION.items():
        menu[v] = k
    opt=rog.menu("{}{}".format(entn.title,entn.name), 0,0,menu.keys())
    result = menu[opt]
    _FUNCS(result)(ent, personality, disposition, style=style)
# end def

def greet(ent:int, style=0) -> int:
    ''' introduce self / attempt to init conversation '''
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
    fdisp = ed / DISPOSITION_MAX
    
    # roll for speech success
    speech_bonus = rog.getskill(rog.pc(), SKL_PERSUASION)
    roll=dice.roll(100) + speech_bonus
    if fdisp < 0.4:
        roll -= 8/fdisp
    else:
        roll += 100*fdisp
    # cases
    if roll <= 0: _response(ent, RESPONSE_REJECTION)
    elif roll < 40: _response(ent, RESPONSE_EXCUSE)
    elif roll < 80: _response(ent, RESPONSE_BUSY)
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
        compo.memories.append(response_type)
        if len(compo.memories) > compo.max_len:
            compo.memories.pop(0)
    else:
        world.add_component(ent, cmp.ConversationMemory(
            MAX_NPC_CONVO_MEMORIES, response_type))
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

def talk_barter(ent:int, speech:int, personality:int, disposition:int, style=0):
    pass

def talk_question(ent:int, speech:int, personality:int, disposition:int, style=0):
    

def talk_interrogate(ent:int, speech:int, personality:int, disposition:int, style=0):
    pass

def talk_torture(ent:int, speech:int, personality:int, disposition:int, style=0):
    pass

def talk_askfavor(ent:int, speech:int, personality:int, disposition:int, style=0):
    pass

def talk_beg(ent:int, speech:int, personality:int, disposition:int, style=0):
    pass
    
def talk_charm(ent:int, speech:int, personality:int, disposition:int, style=0):
    pass

def talk_boast(ent:int, speech:int, personality:int, disposition:int, style=0):
    pass

def talk_smalltalk(ent:int, speech:int, personality:int, disposition:int, style=0):
    pass

def talk_bribe(ent:int, speech:int, personality:int, disposition:int, style=0):
    pass

def talk_intimidate(ent:int, speech:int, personality:int, disposition:int, style=0):
    pass

def talk_flatter(ent:int, speech:int, personality:int, disposition:int, style=0):
    pass

def talk_flirt(ent:int, speech:int, personality:int, disposition:int, style=0):
    pass

def talk_debate(ent:int, speech:int, personality:int, disposition:int, style=0):
    pass


    #-----------------------------------------------#
    # constants (relying on the above declarations) #
    #-----------------------------------------------#

_FUNCS={
TALK_ASKQUESTION    : talk_question,
TALK_INTERROGATE    : talk_interrogate,
TALK_ASKFAVOR       : talk_askfavor,
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
    }


#--------------------------END OF CODE------------------------------#





















