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
# func render_hud
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
def _get(stat): return rog.getms(pc, stat)
def _gets(stat): return rog.getms(pc, stat)//MULT_STATS
def _geta(att): return rog.getms(pc, att)//MULT_ATT
def _getb(stat): return rog.world().component_for_entity(pc, cmp.Stats).__dict__[stat]//MULT_ATT
# render the regular abridged in-game HUD that only shows vitals
def render_hud(w,h,pc,turn,level):
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
        dlv=level,t=turn,
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
#

# render the entire character info page(s), with page scrolling if necessary
def render_charpage(w,h,pc,turn,level):
    # Setup #
    world = rog.world()
    con = libtcod.console_new(w,h)
    name = world.component_for_entity(pc, cmp.Name)
    meters = world.component_for_entity(pc, cmp.Meters)
    
    # status effects
    effects=""
    for k,v in STATUSES.items():
        clsname=type(k).__name__
        if world.has_component(pc, clsname):
            compo=world.component_for_entity(pc, clsname)
            effects += "{v:>32} : {t:<6}\n".format(
                v="* {}".format(v), t=compo.timer )
    if effects: effects=effects[:-1] # remove final '\n'
    #
    
    # gauges (meters)
    lgauges=[]
    if meters.rads > 0:
        lgauges.append( (meters.rads, "{v:>32} : {a:<6}\n".format(
                v="* {}".format('radiation'), a=meters.rads ),) )
    if meters.sick > 0:
        lgauges.append( (meters.sick, "{v:>32} : {a:<6}\n".format(
                v="* {}".format('sickness'), a=meters.sick ),) )
    if meters.expo > 0:
        lgauges.append( (meters.expo, "{v:>32} : {a:<6}\n".format(
                v="* {}".format('exposure'), a=meters.expo ),) )
    if meters.pain > 0:
        lgauges.append( (meters.pain, "{v:>32} : {a:<6}\n".format(
                v="* {}".format('pain'), a=meters.pain ),) )
    if meters.fear > 0:
        lgauges.append( (meters.fear, "{v:>32} : {a:<6}\n".format(
                v="* {}".format('fear'), a=meters.fear ),) )
    if meters.bleed > 0:
        lgauges.append( (meters.bleed, "{v:>32} : {a:<6}\n".format(
                v="* {}".format('bleed'), a=meters.bleed ),) )
    if meters.rust > 0:
        lgauges.append( (meters.rust, "{v:>32} : {a:<6}\n".format(
                v="* {}".format('rust'), a=meters.rust ),) )
    if meters.rot > 0:
        lgauges.append( (meters.rot, "{v:>32} : {a:<6}\n".format(
                v="* {}".format('rot'), a=meters.rot ),) )
    if meters.wet > 0:
        lgauges.append( (meters.wet, "{v:>32} : {a:<6}\n".format(
                v="* {}".format('wetness'), a=meters.wet ),) )
    # sort
    lgauges.sort(key = lambda x: x[0], reverse=True)
    # get all in one string
    gauges=""
    for gauge in lgauges:
        gauges += gauge[1]
    if gauges: gauges=gauges[:-1] # remove final '\n'
    #
    
    # create the display format string
    # TODO: minimum display values (but only after debugging stats/HUD!!!)
    strngStats = '''
{titledelim} character {titledelim}
                    name{delim}{name}
                 faction{delim}{fact}
                     job{delim}{job}
                    mass{delim}{kg} kg
                  height{delim}{cm} cm
            encumberance{delim}{encpc}% (enc / encmax) <encstr>

                        {subdelim} status {subdelim}
                (life)----HP{statline}{hp:>5} / {hpmax:<5}
             (stamina)----SP{statline}{sp:>5} / {spmax:<5}
    effects:
        {effects}
    gauge:
        temperature: {temp} ({normalbodytemp})
        {gauges}
        
                            {subdelim} attribute {subdelim}
             (agility)---AGI{attdelim}{_agi:<2}{attdelim}(bagi)
            (strength)---STR{attdelim}{_str:<2}{attdelim}(bstr)
           (endurance)---END{attdelim}{_end:<2}{attdelim}(bend)
           (dexterity)---DEX{attdelim}{_dex:<2}{attdelim}(bdex)
        (intelligence)---INT{attdelim}{_int:<2}{attdelim}(bint)
        (constitution)---CON{attdelim}{_con:<2}{attdelim}(bcon)
       
                            {subdelim} statistic {subdelim}
          (protection)---PRO{attdelim}{pro:<4}{statdelim}(bpro)
         (dodge value)----DV{attdelim}{dv:<4}{statdelim}(bdv)
         (armor value)----AV{attdelim}{av:<4}{statdelim}(bav)
         (penetration)---PEN{attdelim}{pen:<4}{statdelim}(bpen)
              (attack)---ATK{attdelim}{atk:<4}{statdelim}(batk)
              (damage)---DMG{attdelim}{dmg:<4}{statdelim}(bdmg)
             (balance)---BAL{attdelim}{bal:<4}{statdelim}(bbal)
           (grappling)---GRA{attdelim}{gra:<4}{statdelim}(bgra)
      (counter-strike)---CTR{attdelim}{ctr:<4}{statdelim}(bctr)
             (courage)---CRG{attdelim}{crg:<4}{statdelim}(bcrg)
        (intimidation)---IDN{attdelim}{idn:<4}{statdelim}(bidn)
              (beauty)---BEA{attdelim}{bea:<4}{statdelim}(bbea)
              (vision)---VIS{attdelim}{vis:<4}{statdelim}(bvis)
             (hearing)---AUD{attdelim}{aud:<4}{statdelim}(baud)
                (mass)----KG{attdelim}{kg:<4}{statdelim}(bkg)
              (height)----CM{attdelim}{cm:<4}{statdelim}(bcm)
        (encumberance)---ENC{attdelim}{enc:<4}{statdelim}
    (max.encumberance)ENCMAX{attdelim}{encmax:<4}{statdelim}(bencmax)
       
                            {subdelim} resistance {subdelim}
                (heat)---FIR{attdelim}{fir:<4}{resdelim}{bfir}
                (cold)---ICE{attdelim}{ice:<4}{resdelim}{bice}
          (bio-hazard)---BIO{attdelim}{bio:<4}{resdelim}{bbio}
         (electricity)---ELC{attdelim}{elc:<4}{resdelim}{belc}
            (physical)---PHS{attdelim}{phs:<4}{resdelim}{bphs}
                (pain)---PAI{attdelim}{pai:<4}{resdelim}{bpai}
               (bleed)---BLD{attdelim}{bld:<4}{resdelim}{bbld}
               (light)---LGT{attdelim}{lgt:<4}{resdelim}{blgt}
               (sound)---SND{attdelim}{snd:<4}{resdelim}{bsnd}
                (rust)---RUS{attdelim}{rus:<4}{resdelim}{brus}
                 (rot)---ROT{attdelim}{rot:<4}{resdelim}{brot}
               (water)---WET{attdelim}{wet:<4}{resdelim}{bwet}
'''.format(
        titledelim="--------------------------------",
        subdelim ="--",
        statline ="------------",
        delim    ="........",
        attdelim ="........",
        statdelim="......",
        resdelim ="......",
        effects=effects,gauges=gauges,
        dlv=level,t=turn,
        name=name.name,
        temp=meters.temp,
        normalbodytemp=37, #TEMPORARY
        hp=_get('hp'),hpmax=_get('hpmax'),sp=_get('mp'),spmax=_get('mpmax'),
        # attributes
        _str=_gets('str'),_agi=_gets('agi'),_dex=_gets('dex'),
        _end=_gets('end'),_int=_gets('int'),_con=_gets('con'),
        # base attributes
        bstr=_getb('str'),bagi=_getb('agi'),bdex=_getb('dex'),
        bend=_getb('end'),bint=_getb('int'),bcon=_getb('con'),
        # stats
        spd=_get('spd'),asp=_get('asp'),msp=_get('msp'),
        hit=_gets('atk'),dmg=_gets('dmg'),pen=_gets('pen'),
        dfn=_gets('dfn'),arm=_gets('arm'),pro=_gets('pro'),
        ctr=_gets('ctr'),gra=_gets('gra'),bal=_gets('bal'),
        crg=_gets('courage'),idn=_gets('intimidation'),
        bea=_gets('beauty'),
        vis=_gets('vision'),aud=_gets('hearing'),
        enc=_gets('enc'),encmax=_gets('encmax'),
        # base stats
        bspd=_getb('spd'),basp=_getb('asp'),bmsp=_getb('msp'),
        bhit=_getb('atk'),bdmg=_getb('dmg'),bpen=_getb('pen'),
        bdfn=_getb('dfn'),barm=_getb('arm'),bpro=_getb('pro'),
        bctr=_getb('ctr'),bgra=_getb('gra'),bbal=_getb('bal'),
        bcrg=_getb('courage'),bidn=_getb('intimidation'),
        bbea=_getb('beauty'),
        bvis=_getb('vision'),baud=_getb('hearing'),
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
#



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
            col=string_colors._get(ch,None)
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





