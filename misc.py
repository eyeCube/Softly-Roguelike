#
# misc.py
#
# misc functions
#

#TODO: distribute these functions into other modules

import libtcodpy as libtcod
import textwrap
import math
import copy

import rogue as rog
from const  import *
import orangio  as IO
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
def render_hud(w,h,pc,turn,level):
    
    def get_color(stat):
        col=COL['white']
        if stat[:3] == 'Lo:':
            col=COL['blue']
        if stat[:3] == 'Hi:':
            col=COL['red']
        return col

    class Stat():
        def __init__(self, x,y, text,color):
            self.x=x
            self.y=y
            self.text=text
            self.color=color

    # Setup #
    
    get = pc.stats.get
    con = libtcod.console_new(w,h)
    
    strngStats = "__{name}__|Lo: {hp}|Hi: {mp}|Speed: {spd}/{asp}/{msp}|Hit: {hit}({hitb})|Pow: {dmg}({dmgb})|DV: {dfn}({dfnb})|AV: {arm}({armb})|FIR: {fir}|BIO: {bio}|DLvl: {dlv}|T: {t}".format(
        name=pc.name,
        hp=get('hp'),mp=get('mp'),
        spd=get('spd'),asp=get('asp'),msp=get('msp'),
        dlv=level,t=turn,
        hit=get('atk'),hitb=pc.stats.atk,dmg=get('dmg'),dmgb=pc.stats.dmg,
        dfn=get('dfn'),dfnb=pc.stats.dfn,arm=get('arm'),armb=pc.stats.arm,
        fir=get('resfire'),bio=get('resbio'),
    )
    stats=strngStats.split('|')
    statLines=[[]]
    tot=0
    y=0
    for stat in stats:
        lenStat=len(stat) + 1
        col=get_color(stat)
        new=Stat(tot, y, stat, col)
        tot += lenStat
        if tot >= rog.window_w():
            tot=lenStat
            y += 1
            new.x=0; new.y=y
            statLines.append([new])
            continue
        statLines[-1].append(new)
    
    
    # Print #
    for line in statLines:
        for stat in line:
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
        if not (attr==get(k)):
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
hp= get('hp'), hpmax= get('hpmax'), mp= get('mp'), mpmax= get('mpmax'),
nrg= pc.stats.nrg,
asps= ('+' if get('asp') >=0 else ''), asp= get('asp'),
msps= ('+' if get('msp') >=0 else ''), msp= get('msp'),
atk= get('atk'), dfn= get('dfn'), dmg= get('dmg'), arm= get('arm'),
spd= get('spd'),
turn= turn,
Spd= base['spd'], Asp= base['asp'], Msp= base['msp'],
Atk= base['atk'], Dfn= base['dfn'], Dmg= base['dmg'], Arm= base['arm'],
)'''

''' lvl= pc.stats.lvl, exp= pc.stats.exp,
req=exp_req,
'''
'''
stg= get('str'), agi= get('agi'), dex= get('dex'),
mnd= get('mnd'), end= get('end'), chm= get('chr'),
Str= base['str'], Agi= base['agi'], Dex= base['dex'],
Mnd= base['mnd'], End= base['end'], Chr= base['chr'],
'''





