'''
    player.py
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
    along with this program.  If not, see <https://Chargen.www.gnu.org/licenses/>

    TODO : finish up chargen function
    
'''

import os
import random

from const      import *
from colors     import COLORS as COL
import rogue    as rog
import components as cmp
import action
import debug
import dice
import entities
import misc




#
#   init player object. Pass an entity into the function...
#

def init(pc):
    
    # register for sense events for the message log
##    rog.add_listener_sights(pc) # TODO: implement this... There is a distinction btn. Events object for regular listening events of sights/sounds, and also two more classes for sights seen and sounds heard by the player. These should probably work differently...
##    rog.add_listener_sounds(pc)
    rog.fov_init(pc)
    rog.view_center(pc)
    rog.givehp(pc)
    rog.givemp(pc)
#


#
#   constant commands
#   can be performed from anywhere in the main game loop
#

def commands_const(pc, pcAct):
    for act,arg in pcAct:        
        if act == "console":    debug.cmd_prompt(globals(), locals())
        elif act == "last cmd": debug.execute_last_cmd(globals(), locals()) 
        elif act == "quit game":rog.end()

def commands_pages(pc, pcAct):
    for act,arg in pcAct:
        if act == "message history" :
            rog.routine_print_msgHistory()
            return
        if act == "character page" :
            rog.routine_print_charPage()
            return
        if act == "inventory" :
            action.inventory_pc(pc)
            return
        if act == "equipment" :
            action.equipment_pc(pc)
            return
        if act == "abilities" :
            action.abilities_pc(pc)
            return

#
#   commands
#

def _Update():
    rog.update_game()
    rog.update_fov(rog.pc())
##    rog.update_final()
    rog.update_hud()
def commands(pc, pcAct):
    world = rog.world()

    directional_command = 'move'
    
    for act,arg in pcAct:

##        print(act)
##        print(arg)
        
        rog.update_base()
        
        #----------------#
        # convert action #
        #----------------#
        
        if act =='context-dir':
            act=directional_command
##        if act =='context':
##            pass
        # moving using the menu move keys
        if (act =='menu-nav' and rog.game_state()=="normal"):
            act=directional_command
        
        
        #----------------#
        # perform action #
        #----------------#
#-----------MOUSE ACTION----------------------------#
        
        if act == 'lclick':
            mousex,mousey,z=arg
            if rog.wallat(mousex,mousey):
                return
            pos = world.component_for_entity(pc, cmp.Position)
            print("Left click unimplemented")
##            rog.path_compute(pc.path, pos.x,pos.y, rog.mapx(mousex), rog.mapy(mousey))
            #rog.occupation_set(pc,'path')

        if act == 'rclick':
            pass
        
#------------OTHER ACTION--------------------------#
        
        if act == 'help':
            rog.help()

        # "move-prompt" : True
        # prompt for a direction
        #   and then perform the move action in that direction
        if act == 'move-prompt':
            pass

        # "attack-prompt" : True
        # prompt for a direction
        #   and then perform the attack action in that direction
        if act == 'attack-prompt':
            pass
        
        # "move" : (x_change, y_change, z_change,)
        if act == 'move':
            _Update()
            dx,dy,dz=arg
            pos = world.component_for_entity(pc, cmp.Position)
            actor = world.component_for_entity(pc, cmp.Actor)
            xto=pos.x + dx
            yto=pos.y + dy

            # wait
            if (xto==pos.x and yto==pos.y):
                actor.ap = 0
                return

            # out of bounds
            if ( not rog.is_in_grid_x(xto) or not rog.is_in_grid_y(yto) ):
                return

            # warning for slow move speed
            if rog.allow_warning_msp():
                msp=rog.getms(pc, 'msp')
                if msp <= 10:
                    inp=rog.prompt(
                        0,0,rog.window_w(), 6, mode='wait',
                        q='''Warning: your movement speed is critically slow
(MSP: {}). Are you sure you want to move? y/n'''.format(msp)
                        )
                    if inp!='y':
                        return
                    else:
                        rog.expire_warning_msp() #TODO: when is best time to reset this warning?
            # end if
            
            # choose context-sensitive action #
            
            # fight if there is a monster present
            mon = rog.monat(xto,yto)
            if mon: # and mon != pc):
                action.fight(pc,mon)
            # or move
            elif not rog.solidat(xto,yto):
                # space is free, so we can move
                if action.move(pc, dx,dy):
                    rog.view_center_player()
            else:
                rog.alert("That space is occupied.")
        # end conditional
        
        # "attack" : (x, y, z,)
        if act == 'attack':
            _Update()
            xto,yto,zto=arg
            pos = world.component_for_entity(pc, cmp.Position)
            actor = world.component_for_entity(pc, cmp.Actor)

            # out of bounds
            if ( not rog.is_in_grid_x(xto) or not rog.is_in_grid_y(yto) ):
                return
            
            # fight if there is a monster present
            mon = rog.monat(xto,yto)
            # ... but don't attack yourself!
            if mon == pc:
                rog.alert("You can't fight yourself!")
                return
            
            if mon:
                action.fight(pc,mon)
            else:
                ent = rog.thingat(xto,yto)
                if ent:
                    action.fight(pc,ent)
                else:
                    rog.msg("You strike out at thin air, losing your balance.")
                    actor.ap = 0
                    rog.set_status(
                        pc, cmp.StatusOffBalance,
                        t=2, q=-MISS_BAL_PENALTY
                        )
        # end conditional

        # chat with closest speaking entity;
        #   if multiple good options, prompt for which one.
        if act == "chat-context":
            action.chat_context(pc)
            _Update()
            return
        if act == "change-pos": # change body position
            action.change_bodypos_pc(pc)
            _Update()
            return
        if act == "change-msp": # change speed of movement (walking, running, jogging, etc.)
            action.change_speed_pc(pc)
            _Update()
            return
        if act == "msp-up": # change from walk to powerwalk, to trot, jog, etc.
            action.speed_up_pc(pc)
            _Update()
            return
        if act == "msp-down": # change from sprint to run, to jog, to trot, etc.
            action.slow_down_pc(pc)
            _Update()
            return
        if act == "target-prompt": #target entity + fire / throw / attack
            action.target_pc_generic(pc)
            _Update()
            return
        if act == "get-prompt":
            action.pickup_pc(pc)
            _Update()
            return
        if act == "openclose-prompt": #open or close
            action.open_pc(pc)
            _Update()
            return
        if act == "open-prompt": #open or close
            action.open_pc(pc)
            _Update()
            return
        if act == "close-prompt": #open or close
            action.open_pc(pc)
            _Update()
            return
        if act == "jog": #begin jogging
            action.jog_pc(pc)
            _Update()
            return
        if act == "run": #begin running
            action.run_pc(pc)
            _Update()
            return
        if act == "sprint": #begin sprinting
            action.sprint_pc(pc)
            _Update()
            return

        #unused actions
        '''if act == "bomb":
            action.bomb_pc(pc)
            return'''
        
        #
        #
        # special actions #
        #
        
        if act == 'find player': #useful to immediately show where the player is
            pos = world.component_for_entity(pc, cmp.Position)
            rog.view_center_player()
            rog.update_game()
            rog.update_final()
            rog.game_update() #call all the updates
            rog.alert('press any key to continue...')
            rog.Input(rog.getx(pos.x), rog.gety(pos.y), mode='wait')
            rog.update_base()
            rog.alert('')
            return
        if act == "look":
            pos = world.component_for_entity(pc, cmp.Position)
            rog.routine_look(pos.x,pos.y)
            return
        if act == "move view":
            rog.routine_move_view()
            return
        if act == "fixed view":
            rog.fixedViewMode_toggle()
            return  
        if act == 'select':
            # TESTING
            print(rog.Input(0,0,20))
            return
        if act == 'exit':
            return

    # end for
# end def




##def chargen_roll():
##    '''
##        Roll a random character
##    '''


#
# Chargen
#
''' global data for use by character generation function '''
class Chargen:
    pass
def __init__Chargen():
    Chargen.pc = None # player character entity
    # points remaining
    Chargen.skillPts=SKILLPOINTS
    Chargen.attPts=ATTRIBUTEPOINTS
    Chargen.statPts=STATPOINTS
    Chargen.traitPts=CHARACTERPOINTS
    # pre-big menu data
    Chargen._name=""
    Chargen._genderName=""
    Chargen._gender=0
    Chargen._pronouns=()
    Chargen._cm=0
    Chargen._cmMult=0
    Chargen._kg=0
    Chargen._kgMult=0
    Chargen.statsCompo=None
    Chargen.skillsCompo=None
    Chargen.flags=None
    # multipliers and characteristics (component indicators)
    Chargen.mreach=1
    Chargen.mmsp=1
    Chargen.mmass=1
    Chargen.mass=0
    Chargen.mcm=1
    Chargen.mbodyfat=1
    Chargen.bodyfat=0
    Chargen.mgut=1
    Chargen.mvision=1
    Chargen.astigmatism=False
    Chargen.cancer=False
    Chargen.rapidMetabolism=False
    Chargen.ironGut=False
    Chargen.immuneVenom=False
    Chargen.hydrophobia=False
    Chargen.attractedMen=False
    Chargen.attractedWomen=False
    Chargen.fastLearner=False
    # menu dicts
    Chargen.menu={} # <- big meta-menu containing all choices
    Chargen.skilldict={}
##    _skilldict={} # used for getting the skill ID from the skill name
    Chargen.statdict={}
    Chargen.traitdict={}
    Chargen.attdict={}
    # selected data
    Chargen._skillIDs=[]
    Chargen._skillNames=[]
    Chargen._stats=[]
    Chargen._traits=[]
    Chargen._attributes=[]
    # menu states
    Chargen.confirm = False
    Chargen.open_skills=False
    Chargen.open_stats=False
    Chargen.open_traits=False
    Chargen.open_attributes=False
    # menu position / window size
    Chargen.x1 = 0; Chargen.y1 = 0;
    Chargen.xx = 0; Chargen.yy = 3;
    Chargen.iy = 0;
    Chargen.ww = rog.window_w(); Chargen.hh = 5;
# end class

# draw the string to con_game
def _printElement(elemStr,iy):
    rog.dbox(Chargen.x1,Chargen.y1+iy,Chargen.ww,3,text=elemStr,
        wrap=False,border=None,con=rog.con_final(),disp='mono')
    return iy+1
def _drawskills(con):
    skillstr = misc._get_skills(Chargen.skillsCompo, showxp=False)
    libtcod.console_print(con, 64,2, "-- skills --")
    libtcod.console_print(con, 40,4, skillstr)
def _drawtraits(con):
    traitstr = misc._get_traits(Chargen._traits)
    yy = 6 + len(Chargen.skillsCompo.skills.keys())
    libtcod.console_print(con, 64,yy, "-- traits --")
    libtcod.console_print(con, 56,yy+2, traitstr)
##def reroll(stats, skills):
    

def chargen(sx, sy):
    ''' character generation function
    # Create and return the player Thing object,
    #   and get/set the starting conditions for the player
    # Arguments:
    #   sx, sy: starting position x, y of player entity
    '''
    # TODO: saving/loading game
    
    # init
    world = rog.world()
    __init__Chargen()   # init some global vars for use during chargen
    height_default = AVG_HUMAN_HEIGHT
    libtcod.console_clear(0)
    libtcod.console_clear(rog.con_game())
    libtcod.console_clear(rog.con_final())
    #
    
    # get character data from player input #
    
    # name
    Chargen._name=rog.prompt(Chargen.x1,Chargen.y1,Chargen.ww,Chargen.hh,maxw=20, q="what is your name?", mode="text")
    _title = 0
    
    # print char data so far
    print("name chosen: ", Chargen._name)
    libtcod.console_clear(rog.con_final())
    Chargen.iy=_printElement("name: {}".format(Chargen._name), Chargen.iy)
    #
    
    # load saved game
    loadedGame = False
    
        # TODO: forget this -- use Pickle or similar
    
##    savedir=os.listdir(os.path.join(
##        os.path.curdir,os.path.pardir,"save"))
##    for filedir in savedir:
##        if ".save" != filedir[-5:] :
##            continue #wrong filetype
##        try:
##            with open(filedir, "r") as save:
##                line = save.readline()
##                if ("name:{}\n".format(Chargen._name) == line):
##                    #found a match. Begin reading data
##                    pc=loadFromSaveFile(save)                    
##                    return pc
##        except FileNotFoundError:
##            pass
##        except:
##            print("ERROR: Corrupted save file detected.")
##            print("Continuing chargen...")
##            break
    # end for
    
    if loadedGame:
        # load old character (TODO)
        pass
    else:
        # make a new character

        # create a basic entity for the PC, with no defining characteristics
        Chargen.skillsCompo = cmp.Skills()
        Chargen.flags = cmp.Flags(IMMUNERUST,)
        Chargen.pc = world.create_entity(
            Chargen.skillsCompo, Chargen.flags)
        #continue chargen by refining the details of the PC...
        
        #gender selection
        _select_gender()
        
        # body type
        _select_height()
        _select_mass()
        
        
            #-------#
            # class #
            #-------#
        
        rog.dbox(Chargen.x1,Chargen.y1+Chargen.iy,Chargen.ww,3,text="what is your profession?",
            wrap=True,border=None,con=rog.con_final(),disp='mono')
        rog.refresh()
        _classList={} #stores {className : (classChar, classID,)} #all classes
        #create menu options
        _menuList={} #stores {classChar : className} #all playable classes
        _randList=[] #for random selection.
        for k,v in entities.getJobs().items(): # k=ID v=charType
##            if v not in rog.playableJobs(): continue #can't play as this class yet
            ID=k        # get ID of the class
            typ=v       # get chartype of the class
            name=entities.getJobName(ID)
            _classList.update({name:(typ,ID,)})
            _menuList.update({typ:name})
            _randList.append(ID)
        _menuList.update({'*':'random'})
        #user selects a class
        _className = rog.menu("class select",Chargen.xx,Chargen.yy+Chargen.iy,_menuList,autoItemize=False)
        #random
        if (_className == 'random' or _className == -1):
            _classID = random.choice(_randList)
            _className = entities.JOBS[_classID][1]
        #get the relevant data
        _type = _classList[_className][0] # get the class Char value
        _mask = _type
        _classID = _classList[_className][1]
        _mass = entities.getJobMass(_classID)
        _jobstats = entities.getJobStats(_classID).items()
        _jobskills = entities.getJobSkills(_classID)
        Chargen._className = _className
        
        #add specific class skills
        for sk_id in _jobskills:
            rog.setskill(Chargen.pc, sk_id, SKILL_LEVELS_JOB)
        
        # print char data so far
        _printChargenData()
        rog.refresh()
        print("class chosen: ", _className)
        #
        
        
        #----------------------------------#
        # start creating player components #
        #----------------------------------#
        
        # create stats component
        Chargen.statsCompo=cmp.Stats(
            hp=BASE_HP, mp=BASE_MP, mpregen=BASE_MPREGEN*MULT_STATS,
            mass=0, # base mass before weight of water and blood and fat is added
            encmax=BASE_ENCMAX,
            resfire=BASE_RESFIRE, rescold=BASE_RESCOLD,
            resbio=BASE_RESBIO, reselec=BASE_RESELEC,
            resphys=BASE_RESPHYS, reswet=BASE_RESWET,
            respain=BASE_RESPAIN, resbleed=BASE_RESBLEED,
            resrust=BASE_RESRUST, resrot=BASE_RESROT,
            reslight=BASE_RESLIGHT, ressound=BASE_RESSOUND,
            _str=BASE_STR*MULT_ATT, _con=BASE_CON*MULT_ATT,
            _int=BASE_INT*MULT_ATT, _agi=BASE_AGI*MULT_ATT,
            _dex=BASE_DEX*MULT_ATT, _end=BASE_END*MULT_ATT,
            atk=BASE_ATK*MULT_STATS, dmg=BASE_DMG*MULT_STATS,
            pen=BASE_PEN*MULT_STATS, dfn=BASE_DFN*MULT_STATS,
            arm=BASE_ARM*MULT_STATS, pro=BASE_PRO*MULT_STATS,
            gra=BASE_GRA*MULT_STATS, bal=BASE_BAL*MULT_STATS,
            ctr=BASE_CTR*MULT_STATS,
            reach=BASE_REACH*MULT_STATS,
            spd=BASE_SPD, asp=BASE_ASP, msp=BASE_MSP,
            sight=0, hearing=0, # senses gained from Body component now. TODO: do the same things for monster gen...
            courage=BASE_COURAGE + PLAYER_COURAGE, # + MAS_COU if not female else 0,
            scary=BASE_SCARY, # + MAS_IDN if not female else 0,
            beauty=BASE_BEAUTY # + FEM_BEA if female else 0
            )
        #add specific class stats
        for stat, val in _jobstats:
            value=val*MULT_STATS if stat in STATS_TO_MULT.keys() else val
            Chargen.statsCompo.__dict__[stat] += value
        #
        
        
        #----------------#
        #    big menu    #
        #----------------#
        
        # (attributes/stats/skills/characteristics)
        
        # menu loop until uer selects "<confirm>"
        while(not Chargen.confirm):
            Chargen.menu={}
            Chargen.menu.update({"<confirm>" : "confirm"})
            _chargen_attributes()
            _chargen_stats()
            _chargen_skills()
            _chargen_traits()
            _selectFromBigMenu()
        # end while

        # choose a personality
        personality = random.choice(MAIN_PERSONALITIES)
        print(personality)
        
        
        # continue creating player entity #
        
            # calculate some stats
        cm = int(height_default * Chargen._cmMult * Chargen.mcm)
        kg = int((_mass + Chargen.mass) * Chargen._kgMult * Chargen.mmass)
        
            # mass stat mods
        fatratio=DEFAULT_BODYFAT_HUMAN
        if Chargen._kg >= 5:
            fatratio += (Chargen._kg-4)/16
        elif Chargen._kg < 3:
            fatratio -= fatratio*(3-Chargen._kg)/3
        fatratio += Chargen.bodyfat/100
        fatratio *= Chargen.mbodyfat
        print("bodyfat: ", fatratio)
        
            # height stat mods
        reachMult = 1 + (Chargen._cm-5)/20 #/10
        reachMult *= Chargen.mreach
        if Chargen._cm < 5:
            mspMult = 1 + (Chargen._cm-5)/24 #/12
        else:
            mspMult = 1 + (Chargen._cm-5)/32 #/16
        mspMult *= Chargen.mmsp
            #
        
        # create body
        body, basemass = rog.create_body_humanoid(
            kg=kg, cm=cm, female=Chargen.female,
            bodyfat=fatratio)
        body.hydration = body.hydrationMax * 0.98
        body.satiation = body.satiationMax * 0.85
        # body temperature
        meters = cmp.Meters()
        meters.temp = BODY_TEMP[BODYPLAN_HUMANOID][0]
        
        # confirmation #
        
        # print char data
        libtcod.console_clear(rog.con_final())
        Chargen.iy=0
        Chargen.iy=_printElement("name: {}".format(Chargen._name), Chargen.iy)
        Chargen.iy=_printElement("gender: {}".format(Chargen._genderName), Chargen.iy)
        Chargen.iy=_printElement("class: {} ({})".format(Chargen._className, _type), Chargen.iy)
        Chargen.iy=_printElement("height: {} cm ({} / 9)".format(cm, Chargen._cm), Chargen.iy)
        Chargen.iy=_printElement("mass: {} kg ({} / 9)".format(kg, Chargen._kg), Chargen.iy)
        _drawskills(rog.con_final())
        _drawtraits(rog.con_final())
        rog.refresh()
        #
        
        # prompt to continue or restart chargen
        _ans=''
        while _ans!='y':
            # roll character
##            reroll(statsCompo, Chargen.skillsCompo)
            _ans=rog.prompt(Chargen.x1,rog.window_h()-4,Chargen.ww,4,maxw=20,
                            q="continue with this character? y/n", #/r (reroll)
                            mode="wait"
                            )
            if _ans.lower()=='n':
                return chargen(sx,sy)
##            if _ans.lower()=='r':
##                reroll(statsCompo, Chargen.skillsCompo)
        # end if
        

            #----------------------------------#
            #     finish creating player       #
            #----------------------------------#

        # apply any stat changes from Chargen that haven't been applied

        Chargen.statsCompo.mass += basemass
        Chargen.statsCompo.reach = round(reachMult*Chargen.statsCompo.reach)
        Chargen.statsCompo.msp = round(mspMult*Chargen.statsCompo.msp)
        if Chargen.fastLearner:
            world.add_component(pc, cmp.FastLearner())
        if Chargen.attractedMen:
            world.add_component(pc, cmp.AttractedToMen())
        if Chargen.attractedWomen:
            world.add_component(pc, cmp.AttractedToWomen())
        
        #create pc object from the data given in chargen
        
        # add components to entity
        pc=Chargen.pc
        world.add_component(pc, Chargen.statsCompo)
        world.add_component(pc, body)
        world.add_component(pc, meters)
        world.add_component(pc, cmp.Player())
        world.add_component(pc, cmp.Name(Chargen._name, title=_title))
        world.add_component(pc, cmp.Draw('@', COL['white'], COL['deep']))
        world.add_component(pc, cmp.Position(sx, sy))
        world.add_component(pc, cmp.Actor())
        world.add_component(pc, cmp.Form(
            mat=MAT_FLESH, val=VAL_HUMAN*MULT_VALUE ))
        world.add_component(pc, cmp.Creature(
            job = Chargen._className,
            faction = FACT_ROGUE,
            species = SPECIE_HUMAN
            ))
        world.add_component(pc, cmp.SenseSight())
        world.add_component(pc, cmp.SenseHearing())
        world.add_component(pc, cmp.Mutable())
        world.add_component(pc, cmp.Inventory())
        world.add_component(pc, cmp.Gender(Chargen._gender))
        world.add_component(pc, cmp.Speaks())
        world.add_component(pc, cmp.Personality(personality))
    # end if
    
    # init PC entity
    pc=Chargen.pc
    rog.register_entity(pc)
    rog.add_listener_sights(pc)
    rog.add_listener_sounds(pc)
    rog.grid_insert(pc)
    rog.update_fov(pc)
    init(pc)
    return pc
#

def _printChargenData():
    _printElement("name: {}".format(Chargen._name), Chargen.iy-4)
    _printElement("gender: {}".format(Chargen._genderName), Chargen.iy-3)
    _printElement("height: {} / 9".format(Chargen._cm), Chargen.iy-2)
    _printElement("mass: {} / 9".format(Chargen._kg), Chargen.iy-1)
    _printElement("class: {}".format(Chargen._className), Chargen.iy)

def _select_gender():
    Chargen.ww=rog.window_w()
    rog.dbox(Chargen.x1,Chargen.y1+Chargen.iy,Chargen.ww,3,text="what is your gender?",
        wrap=True,border=None,con=rog.con_final(),disp='mono')
    rog.refresh()
    
    _gender=''
    while (_gender == ''):
        _menuList={'m':'male','f':'female','n':'nonbinary','*':'random',}
        
        _gender=rog.menu("gender select",Chargen.xx,Chargen.yy,_menuList,autoItemize=False)
        if _gender == -1:
            _gender = 'random'
        if _gender == 'nonbinary':
            _genderName = "nonbinary" # temporary...
            _genderID = GENDER_OTHER
        else: #random, male and female
            if _gender == 'random':
                _gender = random.choice(("male","female",))
            if _gender == 'male':
                _genderName = "male"
                _genderID = GENDER_MALE
            elif _gender == 'female':
                _genderName = "female"
                _genderID = GENDER_FEMALE
    # end while
    
    # save selected data
    Chargen._pronouns = rog._get_pronouns(_genderID)
    Chargen._gender = _genderID
    Chargen._genderName = _genderName
    Chargen.female=(Chargen._genderName=="female")
    # print char data so far
    libtcod.console_clear(rog.con_final())
    _printElement("name: {}".format(Chargen._name), Chargen.iy-1)
    Chargen.iy=_printElement("gender: {}".format(Chargen._genderName), Chargen.iy)
    print("gender chosen: ", Chargen._genderName)
# end def

def _select_height():
    Chargen.ww=rog.window_w()
    avg = 3 if Chargen.female else 5
    _cm=rog.prompt( Chargen.x1,Chargen.y1+Chargen.iy,Chargen.ww,6,maxw=20,
        q="How tall are you? (press a key from 1 to 9. {} is average)".format(avg),
        mode="wait" )
    try:
        _cm = int(_cm)
    except:
        _cm = avg
    if (_cm==0 or not _cm): _cm=avg
    _cmMult = 1 + (_cm - 5)/20
    
    # save selected data
    Chargen._cm = _cm
    Chargen._cmMult = _cmMult
    # print char data so far
    _printElement("name: {}".format(Chargen._name), Chargen.iy-2)
    _printElement("gender: {}".format(Chargen._genderName), Chargen.iy-1)
    Chargen.iy=_printElement("height: {} / 9".format(Chargen._cm), Chargen.iy)
    print("height chosen: ", Chargen._cm)
# end def

def _select_mass():
    _kg=rog.prompt( Chargen.x1,Chargen.y1+Chargen.iy,Chargen.ww,6,maxw=20,
        q="How heavy are you? (press a key from 1 to 9. 3 is average)",
        mode="wait" )
    try:
        _kg = int(_kg)
    except:
        _kg = 3
    if (_kg==0 or not _kg): _kg=3
    _kgMult = 1 + (_kg - 3)/8

    # save selected data
    Chargen._kg = _kg
    Chargen._kgMult = _kgMult
    # print char data so far
    _printElement("name: {}".format(Chargen._name), Chargen.iy-3)
    _printElement("gender: {}".format(Chargen._genderName), Chargen.iy-2)
    _printElement("height: {} / 9".format(Chargen._cm), Chargen.iy-1)
    Chargen.iy=_printElement("mass: {} / 9".format(Chargen._kg), Chargen.iy)
    print("mass chosen: ", Chargen._kg)
# end def

def _chargen_attributes():
    if Chargen.open_attributes:
        stats=Chargen.statsCompo
        _con=stats.con//MULT_STATS
        _int=stats.int//MULT_STATS
        _str=stats.str//MULT_STATS
        _agi=stats.agi//MULT_STATS
        _dex=stats.dex//MULT_STATS
        _end=stats.end//MULT_STATS
        Chargen.menu.update(
            {"- attributes (pts: {})".format(Chargen.attPts) : "close-attributes",})
        Chargen.attdict={
"... ({}) CON: Constitution {}".format(_get_attribute_cost("con"),_con) : "con",
"... ({}) INT: Intelligence {}".format(_get_attribute_cost("int"),_int) : "int",
"... ({}) STR: Strength     {}".format(_get_attribute_cost("str"),_str) : "str",
"... ({}) AGI: Agility      {}".format(_get_attribute_cost("agi"),_agi) : "agi",
"... ({}) DEX: Dexterity    {}".format(_get_attribute_cost("dex"),_dex) : "dex",
"... ({}) END: Endurance    {}".format(_get_attribute_cost("end"),_end) : "end",
        }
        for k,v in Chargen.attdict.items():
            Chargen.menu.update({k:v})
    else:
        Chargen.menu.update(
            {"+ attributes (pts: {})".format(Chargen.attPts) : "open-attributes",})
# end def

def _select_attribute(_stat):
    pc=Chargen.pc
    cost = _get_attribute_cost(_stat)
    if Chargen.attPts < cost:
        _insufficientPoints(Chargen.attPts, cost, "attribute")
        return False
    
    # change stat value
    Chargen.statsCompo.__dict__[_stat] += 1*MULT_STATS
    
    # save selected data
    Chargen.attPts -= cost
    if Chargen.attPts == 0:
        Chargen.open_attributes = False
    Chargen._attributes.append(_stat)
    print("attribute chosen: {} (pts: {})".format(_stat, Chargen.attPts))
    return True
# end def

def _get_attribute_cost(_stat):
    # increasing cost for higher attribute levels
    for k,v in CHARGEN_ATTRIBUTES[_stat].items():
        if Chargen.statsCompo.__dict__[_stat]//MULT_STATS >= k:
            cost = v
        else:
            break
    return cost

def _chargen_stats():
    if Chargen.open_stats:
        hp_d=CHARGEN_STATS['hpmax']
        sp_d=CHARGEN_STATS['mpmax']
        enc_d=CHARGEN_STATS['encmax']
        msp_d=CHARGEN_STATS['msp']
        asp_d=CHARGEN_STATS['asp']
##        gra_d=CHARGEN_STATS['gra']//MULT_STATS
        bal_d=CHARGEN_STATS['bal']//MULT_STATS
        ctr_d=CHARGEN_STATS['ctr']//MULT_STATS
        cou_d=CHARGEN_STATS['cou']
        bea_d=CHARGEN_STATS['bea']
        idn_d=CHARGEN_STATS['idn']
        camo_d=CHARGEN_STATS['camo']
        stealth_d=CHARGEN_STATS['stealth']
        
        stats=Chargen.statsCompo
        _hp=stats.hpmax
        _sp=stats.mpmax
        _enc=stats.encmax
        _asp=stats.asp
        _msp=stats.msp
##        _gra=stats.gra//MULT_STATS
        _bal=stats.bal//MULT_STATS
        _ctr=stats.ctr//MULT_STATS
        _cou=stats.cou
        _bea=stats.bea
        _idn=stats.idn
        _camo=stats.camo
        _stealth=stats.stealth
        
        Chargen.menu.update(
            {"- base stats (pts: {})".format(Chargen.statPts) : "close-stats",})
        Chargen.statdict={
"... HPMAX: Life       {s:<4}(+{d})".format(d=hp_d,s=_hp) : "hpmax",
"... SPMAX: Stamina    {s:<4}(+{d})".format(d=sp_d,s=_sp) : "mpmax",
"... ENCMAX: Carry     {s:<4}(+{d})".format(d=enc_d,s=_enc) : "encmax",
"... ASP: Attack Speed {s:<4}(+{d})".format(d=asp_d,s=_asp) : "asp",
"... MSP: Move Speed   {s:<4}(+{d})".format(d=msp_d,s=_msp) : "msp",
"... BAL: Balance      {s:<4}(+{d})".format(d=bal_d,s=_bal) : "bal",
"... CTR: Counter      {s:<4}(+{d})".format(d=ctr_d,s=_ctr) : "ctr",
"... COU: Courage      {s:<4}(+{d})".format(d=cou_d,s=_cou) : "cou",
"... IDN: Intimidation {s:<4}(+{d})".format(d=idn_d,s=_idn) : "idn",
"... BEA: Beauty       {s:<4}(+{d})".format(d=bea_d,s=_bea) : "bea",
"... CAMO: Camo        {s:<4}(+{d})".format(d=camo_d,s=_camo) : "camo",
"... STEL: Stealth     {s:<4}(+{d})".format(d=stealth_d,s=_stealth) : "stealth",
        }
        for k,v in Chargen.statdict.items():
            Chargen.menu.update({k:v})
    else:
        Chargen.menu.update(
            {"+ stats (pts: {})".format(Chargen.statPts) : "open-stats",})
# end def

def _select_stat(_stat):
    pc=Chargen.pc
    if Chargen.statPts <= 0:
        _insufficientPoints(Chargen.statPts, 1, "stat")
        return False
    
    # change stat value
    val = CHARGEN_STATS[_stat] # the amount added depends on the stat
    Chargen.statsCompo.__dict__[_stat] += val
    
    # save selected data
    Chargen.statPts -= 1
    if Chargen.statPts <= 0:
        Chargen.open_stats = False
    Chargen._stats.append(_stat)
    print("stat chosen: {} (pts: {})".format(_stat, Chargen.statPts))
    return True
# end def

def _chargen_skills():
    pc=Chargen.pc
    if Chargen.open_skills:
        Chargen.menu.update(
            {"- skills (pts: {})".format(Chargen.skillPts) : "close-skills",})
        Chargen.skilldict={}
        sortdict = {k:v for k,v in sorted(
            SKILLS.items(), key=lambda item: item[1][1].lower())}
        for k, sk in sortdict.items(): # Python 3.6+ remembers dict ordering so skills are already ordered
            skilllv = rog.getskill(pc, k)
            x = skilllv // SKILL_INCREQ
            cost = "({})".format(sk[0] + x) if skilllv < 100 else "<MAX>"
            string = "... {} {}".format(cost, sk[1])
            Chargen.skilldict.update({string : k})
        
        for k,v in Chargen.skilldict.items():
            Chargen.menu.update({k:v})
    else:
        Chargen.menu.update(
            {"+ skills (pts: {})".format(Chargen.skillPts) : "open-skills",})
# end def

def _select_skill(_skillID):
    pc=Chargen.pc
    _skillName = SKILLS[_skillID][1]    
    _skillPts = SKILLS[_skillID][0] + rog.getskill(pc, _skillID)//SKILL_INCREQ
    if rog.getskill(pc, _skillID) >= MAX_SKILL:
        _maxedSkill(_skillName)
        return False
    if Chargen.skillPts < _skillPts:
        _insufficientPoints(Chargen.skillPts, _skillPts, "skill")
        return False
    
    # change skill level
    rog.setskill(pc, _skillID, min(
        100, rog.getskill(pc, _skillID) + SKILL_LEVELS_PER_SELECTION) )
    
    # save selected data
    Chargen.skillPts -= _skillPts
    if Chargen.skillPts <= 0:
        Chargen.open_skills = False
    Chargen._skillNames.append(_skillName)
    Chargen._skillIDs.append(_skillID)
    print("skill chosen: {} (pts: {})".format(_skillName, Chargen.skillPts))
    return True
# end def

def _chargen_traits():
    # characteristics #
    if Chargen.open_traits:
        Chargen.menu.update(
            {"- traits (pts: {})".format(Chargen.traitPts) : "close-traits",})
        Chargen.traitdict={}
        sortdict = {k:v for k,v in sorted(
            CHARACTERISTICS.items(), key=lambda item: item[0])}
        for k,v in sortdict.items():
            cost = cost = "+{}".format(v[0]) if v[0] > 0 else v[0]
            t = "<TAKEN> " if k in Chargen._traits else "({c}) ".format(c=cost)
            Chargen.traitdict.update({"... {t}{k}".format(t=t,k=k):k})
        
        for k,v in Chargen.traitdict.items():
            Chargen.menu.update({k:v})
    else:
        Chargen.menu.update(
            {"+ traits (pts: {})".format(Chargen.traitPts) : "open-traits",})
# end def

def _select_trait(_trait):
    pc=Chargen.pc
    pts = CHARACTERISTICS[_trait][0]
    # already have
    if _trait in Chargen._traits:
        _alreadyHaveTrait(_trait)
        return False
    # confirmation prompt
    description = CHARACTERISTICS_DESCRIPT[_trait]
    c = "Costs" if pts < 0 else "Gives"
    description = '{}: {}. {}: {} pts. Points remaining: {}'.format(
        _trait, description, c, abs(pts), Chargen.traitPts)
    rog.dbox( 0,0,Chargen.ww,8,
              text=description, wrap=True, con=rog.con_final() )
    inp=rog.prompt(0,10,Chargen.ww,4,q="select this trait? y/n", mode='wait')
    if inp!='y':
        return False
    # insufficient points
    if Chargen.traitPts < -pts:
        _insufficientPoints(Chargen.traitPts, -pts, "trait")
        return False
    
    success = False
    
    # (attempt to) apply trait
    data = CHARACTERISTICS[_trait][1]
    for k,v in data.items():
                # meta traits
        if k=="skillPts":
            Chargen.skillPts += v
            success = True
        elif k=="statPts":
            Chargen.statPts += v
            success = True
        elif k=="attPts":
            Chargen.attPts += v
            success = True
                # component flags
        elif k=="astigmatism": # TODO: make these apply components in chargen
            Chargen.astigmatism=True
            success = True
        elif k=="cancer":
            Chargen.cancer=True
            success = True
        elif k=="rapidMetabolism":
            Chargen.rapidMetabolism=True
            success = True
        elif k=="ironGut":
            Chargen.ironGut=True
            success = True
        elif k=="immuneVenom":
            Chargen.immuneVenom=True
            success = True
        elif k=="hydrophobia":
            Chargen.hydrophobia=True
            success = True
        elif k=="attractedMen":
            Chargen.attractedMen=True
            success = True
        elif k=="attractedWomen":
            Chargen.attractedWomen=True
            success = True
        elif k=="fastLearner":
            Chargen.fastLearner=True
            success = True
                # sub-menu traits
        elif k=="talent":
            success = _select_talent()
        elif k=="trauma":
            success = _select_trauma()
        elif k=="addict":
            success = _select_addict()
        elif k=="allergy":
            success = _select_allergy()
        elif k=="scarred":
            success = _select_scar()
                # body stats
        elif k=="mfat":
            Chargen.mbodyfat *= v #(TODO: make these change stats in chargen)
            success = True
        elif k=="fat":
            Chargen.bodyfat += v #(TODO: make these change stats in chargen)
            success = True
        elif k=="mgut":
            Chargen.mgut *= v #(TODO: make these change stats in chargen)
            success = True
        elif k=="mvision":
            Chargen.mvision *= v #(TODO: make these change stats in chargen)
            success = True
                # stats
        elif k=="mmass":
            Chargen.mmass *= v
            success = True
        elif k=="mass":
            Chargen.mass += v
            success = True
        elif k=="mcm":
            Chargen.mcm *= v
            success = True
        elif k=="mreach":
            Chargen.mreach *= v
            success = True
        elif k=="mreach":
            Chargen.mreach *= v
            success = True
        elif k=="mmsp":
            Chargen.mmsp *= v
            success = True
        elif k=="bea":
            Chargen.statsCompo.bea += v
            success = True
        elif k=="idn":
            Chargen.statsCompo.idn += v
            success = True
        elif k=="cou":
            Chargen.statsCompo.cou += v
            success = True
        elif k=="str":
            Chargen.statsCompo.str += v*MULT_STATS
            success = True
        elif k=="agi":
            Chargen.statsCompo.agi += v*MULT_STATS
            success = True
        elif k=="dex":
            Chargen.statsCompo.dex += v*MULT_STATS
            success = True
        elif k=="end":
            Chargen.statsCompo.end += v*MULT_STATS
            success = True
        elif k=="con":
            Chargen.statsCompo.con += v*MULT_STATS
            success = True
        elif k=="int":
            Chargen.statsCompo.int += v*MULT_STATS
            success = True
        elif k=="resbio":
            Chargen.statsCompo.resbio += v
            success = True
        elif k=="resfire":
            Chargen.statsCompo.resfire += v
            success = True
        elif k=="rescold":
            Chargen.statsCompo.rescold += v
            success = True
        elif k=="respain":
            Chargen.statsCompo.respain += v
            success = True
    # end for
    
    if success:
        # trait chosen successfully
        Chargen.traitPts += pts
        if Chargen.traitPts <= 0:
            Chargen.open_traits = False
        Chargen._traits.append(_trait)
        print("trait chosen: {} (pts: {})".format(_trait, Chargen.traitPts))
        return True
    return False
# end def

def _selectFromBigMenu():
    ''' run the big menu, return whether any char data has changed
    '''
    libtcod.console_clear(0)
    libtcod.console_clear(rog.con_final())
    _printChargenData()
    rog.refresh()
    _drawskills(0)
    _drawtraits(0)
    _choice = rog.menu( "character specs", Chargen.xx,10, Chargen.menu.keys() )
    if _choice == -1: # Esc
        Chargen.confirm = True
        return False
    selected=Chargen.menu.get(_choice, None)
    if not selected:
        print("Failure in _selectFromBigMenu()... information:")
        print("    selected: ", selected)
        print("    _choice: ", _choice)
        return False
    
    # selection successful.
    # figure out what type of option was selected
    if selected=="confirm":
        Chargen.confirm = True
    elif selected=="open-skills":
        Chargen.open_skills = True
    elif selected=="close-skills":
        Chargen.open_skills = False
    elif selected=="open-stats":
        Chargen.open_stats = True
    elif selected=="close-stats":
        Chargen.open_stats = False
    elif selected=="open-attributes":
        Chargen.open_attributes = True
    elif selected=="close-attributes":
        Chargen.open_attributes = False
    elif selected=="open-traits":
        Chargen.open_traits = True
    elif selected=="close-traits":
        Chargen.open_traits = False
    elif selected in Chargen.skilldict.values():
        return _select_skill(selected)
    elif selected in Chargen.statdict.values():
        return _select_stat(selected)
    elif selected in Chargen.attdict.values():
        return _select_attribute(selected)
    elif selected in Chargen.traitdict.values():
        return _select_trait(selected)
    
    return False
# end def

def _select_talent():
    menu={}
    for k,v in sorted(SKILLS.items(), key=lambda x: x[1][1].lower()):
        menu[v[1]] = k
    menu["<cancel>"] = -1
    choice=rog.menu(
        "In which skill are you talented?",
        0,0, menu.keys(), autoItemize=True
        )
    if choice!=-1:
        selected = menu[choice]
        rog.world().add_component(Chargen.pc, cmp.Talented(selected))
        return True
    return False

def _insufficientPoints(points, cost, string):
    rog.dbox(
        0,0,rog.window_w(),5,
        text='''Not enough {} points remaining.
(Cost: {} | Points remaining: {})
<Press any key to continue>'''.format(string, cost, points),
wrap=False,con=rog.con_final(),disp='mono'
        )
    rog.refresh()
    rog.Input(rog.window_w()-2,1,mode='wait')
def _maxedSkill(string):
    rog.dbox(
        0,0,rog.window_w(),8,
        text='''You've reached the maximum skill level in skill:
"{}". Please choose another skill, or select "<confirm>" on the
"character specs" menu to continue.
<Press any key to continue>'''.format(string),
wrap=True,con=rog.con_final(),disp='mono'
        )
    rog.refresh()
    rog.Input(rog.window_w()-2,1,mode='wait')
def _alreadyHaveTrait(string):
    rog.dbox(
        0,0,rog.window_w(),4,
        text='''You already have this trait: "{}".
<Press any key to continue>'''.format(string),
wrap=True,con=rog.con_final(),disp='mono'
        )
    rog.refresh()
    rog.Input(rog.window_w()-2,1,mode='wait')


# other private chargen functions

def _add_gender():
    Chargen.x1=5
    Chargen.y1=5
    Chargen.ww=25
    Chargen.hh=6
    #get new gender name
    _genderName=rog.prompt(Chargen.x1,Chargen.y1,Chargen.ww,Chargen.hh,maxw=20, q="what is your gender?", mode="text")
    #pronouns
    #subject pronoun
    _pronoun1=rog.prompt(
        Chargen.x1,Chargen.y1,Chargen.ww,Chargen.hh,maxw=10,
        q="what are your pronouns?\n\tsubject pronoun:",
        default="they",mode="text",insert=True
        )
    #object pronoun
    _pronoun2=rog.prompt(
        Chargen.x1,Chargen.y1,Chargen.ww,Chargen.hh,maxw=10,
        q="what are your pronouns?\n\tobject pronoun:",
        default="them",mode="text",insert=True
        )
    #possessive pronoun
    _pronoun3=rog.prompt(
        Chargen.x1,Chargen.y1,Chargen.ww,Chargen.hh,maxw=10,
        q="what are your pronouns?\n\tpossessive pronoun:",
        default="their",mode="text",insert=True
        )
    #confirm
    success=rog.prompt(Chargen.x1,Chargen.y1,50,15,
q='''confirm gender: {}\nsubject pronoun: {}\nobject pronoun: {}
possessive pronoun: {}
\nConfirm (y) or Cancel (n)'''.format(
        _genderName,_pronoun1,_pronoun2,_pronoun3),
        mode='wait'
        )
    if success:
        #add the gender into the genders text file for next game
        genderFileName="genders.txt"
        genderFileDir=os.path.join(
            os.path.curdir,os.path.pardir,"settings",genderFileName)
        def writeGender(n,p1,p2,p3):
            with open(genderFileDir, "a+") as file:
                file.write("{}:{},{},{}\n".format(n,p1,p2,p3))
        try:
            writeGender(_genderName,_pronoun1,_pronoun2,_pronoun3)
        except FileNotFoundError:
            print("Failed to load {}, creating new file...".format(genderFileName))
            with open(genderFileDir, "w+") as file:
                file.write("\n") #nothing needed in the file
            writeGender(_genderName,_pronoun1,_pronoun2,_pronoun3) #then write
            
        #return gender information for chargen
        return (_genderName,(_pronoun1,_pronoun2,_pronoun3,),)
    else: #failure
        return ("",())
#


#
def loadFromSaveFile(save):
    # TODO: learn pickle / serialization
    pickle.dump(stats, save)















                    # commented out code below. #



##    #get added genders
##    _genderList = {}
##    genderFileDir=os.path.join(
##        os.path.curdir,os.path.pardir,"settings","genders.txt")
##    try:
##        with open(genderFileDir, "r") as file:
##            for line in file:
##                if "//" in line: continue
##                data = line.split(':')
##                if len(data) < 2: continue
##                gname = data[0]
##                data = data[1].split(',')
##                gpronouns = data
##                _genderList.update({gname:gpronouns})
##    except FileNotFoundError:
##        print("ALERT: file '{}' not found. Creating new file...".format(genderFileDir))
##        with open(genderFileDir, "w+") as file:
##            file.write("\n")

##                #select gender from list of added genders
##                _menuNonbin=[]
##                for jj in _genderList.keys():
##                    _menuNonbin.append(jj)
##                _menuNonbin.append('add new gender')
##                choice=rog.menu("Nonbinary Genders",Chargen.xx,Chargen.yy,_menuNonbin)
##                #add gender
##                if choice == 'add new gender':
##                    _genderName,_pronouns = _add_gender()
##                else:
##                    _genderName = choice
##                    _pronouns = _genderList[_genderName]
##                if _genderName=='': #failed to select or add new gender
##                    _gender='' #prompt user again for gender
                    
                    
    


