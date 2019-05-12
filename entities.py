'''
    monsters.py
    
'''


import esper

from const import *
import components as comp





diplomacy={
    #Factions:
    #(Rogue,Citizens,Deprived,Elite,Watch,Abominations,)
    FACT_ROGUE      : (1,1,1,0,0,0,),
    FACT_CITIZENS   : (1,1,0,0,0,0,),
    FACT_DEPRIVED   : (1,0,1,0,0,0,),
    FACT_ELITE      : (0,1,0,1,1,0,),
    FACT_WATCH      : (0,1,0,1,1,0,),
    FACT_MONSTERS   : (0,0,0,0,0,1,),
}




bestiary={
    # Column names in more detail:
    # Lo qi, Hi qi, Attack, Damage, Dodge, Armor, Speed, Move Speed, Attack Speed, Carrying Capacity, Mass, Gold.
    
#Type,  Name,                   (Lo\ Hi\ At\Dm\DV\AV\Spd\Msp\Asp\FIR\BIO\ELC\SIGT\HEAR\CARRY\KG\$$\),   FLAGS,

'@' : ('human',                 (20, 20, 5, 2, 2, 0, 100,100,100, 10, 10, 10, 20, 100, 60,  65, 500, ),(CANEAT,),),
'a' : ('abomination',           (16, 8,  0, 4, -8,2, 100,90, 110, 40, 50, 25, 6,  0,   30,  80, 0,  ),(),),
'b' : ('bug-eyed business guy', (20, 30, 5, 2, 2, 0, 150,120,100, 10, 10, 0,  25, 100, 90,  60, 500, ),(CANEAT,),),
'B' : ('butcher',               (50, 20, 5, 6, -4,0, 100,100,100,  0, 25, 25, 10, 100, 90,  130,300, ),(CANEAT,),),
'L' : ('raving lunatic',        (12, 25, 3, 2, 2, 0, 100,100,100,  0, 15, 30, 10, 0,   60,  50, 0, ),(),), #BABBLES,
'r' : ('ravaged',               (4,  1,  1, 2, -8,-1,100,80, 70,   0,  0, 0,  10, 0,   15,  35, 0,  ),(RAVAGED,),),
'R' : ('orctepus',              (15, 5,  6, 2,-12,0, 100,80, 145,  0, 60, 0,  8,  0,   120, 100,0,  ),(CANEAT,),),
's' : ('slithera',              (6,  15, 10,4, -4,0, 100,33, 150,  0, 20, 5,  5,  0,   35,  30, 0, ),(CANEAT,),),
'U' : ('obese scrupula',        (20, 2,  4, 8,-16,3, 100,50, 90,   0, 55, 50, 10, 0,   85,  140,100,  ),(),),
'V' : ('ash vampire',           (50, 80, 8, 5, 8, 0, 100,120,100, 10, 75, 5,  5,  200, 60,  30, 1000,  ),(MEAN,NVISION,),),
'w' : ('dire wolf',             (12, 3,  12,5, 8, 0, 100,225,115, 15, 15, 10, 15, 0,   20,  50, 0,  ),(RAVAGED,),),
'W' : ('whipmaster',            (24, 10, 5, 5, 4, 2, 100,80, 100, 25, 60, 15, 15, 0,   75,  75, 1000, ),(MEAN,NVISION,),),
'z' : ('zombie',                (8,  1,  0, 3,-12,-1,50, 40, 100,  5, 25, 15, 5,  0,   30,  45, 0,  ),(MEAN,),),


}

corpse_recurrence_percent={
    '@' : 100,
    'a' : 30,
    "A" : 100,
    'b' : 100,
    'B' : 100,
    "C" : 100,
    "d" : 100,
    "E" : 100,
    "I" : 100,
    "j" : 100,
    "O" : 100,
    "p" : 100,
    "P" : 100,
    'r' : 20,
    'R' : 75,
    'S' : 100,
    "t" : 100,
    "T" : 100,
    "u" : 100,
    'U' : 100,
    'V' : 100,
    'W' : 50,
    'z' : 20,
}



#
# Creatures
#

def create_creature(name, x, y):
    creature = world.create_entity(
        Name(name), Position(x,y), Creature(), Renderable(),
        Seer(), Listener(), Purse(), Senser()
        )
    return creature

#
# Create monster based on current dungeon level
# plugging in values from the table of monsters (bestiary)
# this monster has no special attributes; has generic name
#
def create_monster(world, typ, pos):
    
    mon=world.create_entity()
    
    # get generic monster attributes #
    
    monData = bestiary[typ]
    
    namestr = monData[0]
    hp,mp,atk,dmg,dfn,arm,spd,msp,asp,fir,bio,elc,vis,aud,inv,kg,val = monData[1]
    
    job = namestr
    world.add_component( comp.Name(namestr) )
    stats = comp.Combat()
    stats.hpmax=hp
    stats.mpmax=mp
    stats.atk=atk
    stats.dmg=dmg
    stats.dfn=dfn
    stats.arm=arm
    stats.spd=spd
    stats.msp=msp
    stats.asp=asp
    stats.resfire=fir
    stats.resbio=bio
    stats.reselec=elc
    world.add_component(mon, stats)
    #for flag in monData[i]:     rog.make(monst,flag) #flags
    #i+=1
    #for item in monData[i]:     rog.give(monst,item) #items
    
    #ai, mutations, color? should be handled elsewhere
    
    return monst
    
# end def












'''# level up #
    levels = 1
    for i in range(levels): rog.level(monst)
    '''

