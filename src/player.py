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
    along with this program.  If not, see <https://www.gnu.org/licenses/>

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
                rog.alert("That tile is occupied.")
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

        if act == "target-prompt": #target entity + fire / throw / attack
            action.target_pc(pc)
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
##    world = rog.world()
##
##    # name
##    _name = "pseudo" #random.choice(DEFAULT_NAMES)
##
##    # gender
##    _gender = random.choice("male", "female")
##
##    # class
##    for k,v in entities.getJobs().items(): # k=ID v=charType
####        if v not in rog.playableJobs(): continue #can't play as this class yet
##        ID=k        # get ID of the class
##        typ=v       # get chartype of the class
##        name=entities.getJobName(ID)
##        _classList.update({name:(typ,ID,)})
##    _class = random.choice(_classList.keys())
##    # TODO: make class stats make a difference...
##    
##    # mass, height
##    if _gender=="female":
##        mass = 57 + int(random.random()*21)
##        height = 152 + int(random.random()*21)
##    elif _gender=="male":
##        mass = 72 + int(random.random()*21)
##        height = 160 + int(random.random()*31)
##    
##    # create body
##    body, newmass = rog.create_body_humanoid(
##        mass=mass, height=height, female=(_genderName=="female") )
##    
##    # create entity
##    pc = world.create_entity(
##        cmp.Name(_name, title=_title),
##        cmp.Draw('@', COL['white'], COL['deep']),
##        cmp.Position(sx, sy),
##        cmp.Actor(),
##        cmp.Form( mat=MAT_FLESH, val=VAL_HUMAN*MULT_VALUE ),
##        cmp.Creature(job=_className, faction=FACT_ROGUE),
##        cmp.Gender(_genderName,_pronouns),
##        cmp.Stats(
##            hp=BASE_HP*MULT_STATS,
##            mp=BASE_MP*MULT_STATS,
##            mass=newmass, # base mass before weight of water and blood and fat is added
##            encmax=BASE_ENCMAX*MASS_MULT,
##            resfire=BASE_RESFIRE,
##            rescold=BASE_RESCOLD,
##            resbio=BASE_RESBIO,
##            reselec=BASE_RESELEC,
##            resphys=BASE_RESPHYS,
##            reswet=BASE_RESWET,
##            respain=BASE_RESPAIN,
##            resbleed=BASE_RESBLEED,
##            resrust=BASE_RESRUST,
##            resrot=BASE_RESROT,
##            reslight=BASE_RESLIGHT,
##            ressound=BASE_RESSOUND,
##            _str=BASE_STR*MULT_ATT,
##            _con=BASE_CON*MULT_ATT,
##            _int=BASE_INT*MULT_ATT,
##            _agi=BASE_AGI*MULT_ATT,
##            _dex=BASE_DEX*MULT_ATT,
##            _end=BASE_END*MULT_ATT,
##            gra=BASE_GRA*MULT_STATS,
##            bal=BASE_BAL*MULT_STATS,
##            ctr=BASE_CTR*MULT_STATS,
##            atk=BASE_ATK*MULT_STATS,
##            dmg=BASE_DMG*MULT_STATS,
##            pen=BASE_PEN*MULT_STATS,
##            dfn=BASE_DFN*MULT_STATS,
##            arm=BASE_ARM*MULT_STATS,
##            pro=BASE_PRO*MULT_STATS,
##            spd=BASE_SPD, asp=BASE_ASP, msp=BASE_MSP,
##            sight=0, hearing=0, # senses gained from Body component now
##            courage=BASE_COURAGE, scary=BASE_SCARY
##            ),
##        cmp.Skills(), cmp.Flags(),
##        cmp.SenseSight(), cmp.SenseHearing(),
##        cmp.Mutable(),
##        cmp.Inventory(),
##        body,
##    )
##
##    # additional skills... (TODO)
##    
##    # init
##    rog.register_creature(pc)
##    init(pc)
##    return pc

#
# Chargen
# Create and return the player Thing object,
#   and get/set the starting conditions for the player
# Arguments:
#   sx, sy: starting position x, y of player entity
#
def chargen(sx, sy):

    # TODO: better UI: show character data to the right of the menus
    # TODO: saving/loading game
    
    # draw the string to con_game
    def _printElement(elemStr,iy):
        rog.dbox(x1,y1+iy,ww,3,text=elemStr,
            wrap=False,border=None,con=rog.con_final(),disp='mono')
        return iy+1
    def _drawskills(con, skillscompo):
        skillstr = misc._get_skills(skillscompo)
        libtcod.console_print(con, 48,2, "-- skills --")
        libtcod.console_print(con, 24,4, skillstr)
##    def reroll(stats, skills):
##        
    #
    
    # init
    world = rog.world()
    x1 = 0; y1 = 0;
    xx = 0; yy = 3;
    iy = 0;
    ww = rog.window_w(); hh = 5;
    height = 175
    libtcod.console_clear(0)
    libtcod.console_clear(rog.con_game())
    libtcod.console_clear(rog.con_final())
    #
    
    # get character data from player input #
    
    # name
    _name=rog.prompt(x1,y1,ww,hh,maxw=20, q="What is your name?", mode="text")
    _title = 0

    # print char data so far
    print("name chosen: ", _name)
    libtcod.console_clear(rog.con_final())
    iy=_printElement("name: {}".format(_name), iy)
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
##                if ("name:{}\n".format(_name) == line):
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
        
        skillscompo = cmp.Skills()
        flags = cmp.Flags(IMMUNERUST,)
        pc = world.create_entity(skillscompo)
        world.add_component(pc, flags)
        #continue chargen...
        
        # gender
        rog.dbox(x1,y1+iy,ww,3,text="What is your gender?",
            wrap=True,border=None,con=rog.con_final(),disp='mono')
        rog.refresh()
        #get added genders
        _genderList = {}
        genderFileDir=os.path.join(
            os.path.curdir,os.path.pardir,"settings","genders.txt")
        try:
            with open(genderFileDir, "r") as file:
                for line in file:
                    if "//" in line: continue
                    data = line.split(':')
                    if len(data) < 2: continue
                    gname = data[0]
                    data = data[1].split(',')
                    gpronouns = data
                    _genderList.update({gname:gpronouns})
        except FileNotFoundError:
            print("ALERT: file '{}' not found. Creating new file...".format(genderFileDir))
            with open(genderFileDir, "w+") as file:
                file.write("\n")

        
        #gender selection
        _gender = ''
        while (_gender == ''):
            _menuList={'m':'male','f':'female','n':'nonbinary','*':'random',}
            
            _gender=rog.menu("Gender Select",xx,yy,_menuList,autoItemize=False)
            if _gender == -1:
                _gender = 'random'
            if _gender == 'nonbinary':
                _genderName = "nonbinary" # temporary...
##                #select gender from list of added genders
##                _menuNonbin=[]
##                for jj in _genderList.keys():
##                    _menuNonbin.append(jj)
##                _menuNonbin.append('add new gender')
##                choice=rog.menu("Nonbinary Genders",xx,yy,_menuNonbin)
##                #add gender
##                if choice == 'add new gender':
##                    _genderName,_pronouns = _add_gender()
##                else:
##                    _genderName = choice
##                    _pronouns = _genderList[_genderName]
##                if _genderName=='': #failed to select or add new gender
##                    _gender='' #prompt user again for gender
            else: #random, male and female
                if _gender == 'random':
                    _gender = random.choice(("male","female",))
                if _gender == 'male':
                    _genderName = "male"
                    _pronouns = ('he','him','his',)
                elif _gender == 'female':
                    _genderName = "female"
                    _pronouns = ('she','her','hers',)
        # end while
        
        # print char data so far
        libtcod.console_clear(rog.con_final())
        _printElement("name: {}".format(_name), iy-1)
        iy=_printElement("gender: {}".format(_genderName), iy)
        print("gender chosen: ", _genderName)
        #
        
        female=(_genderName=="female")
        
        
        # body type
        avg = 3 if female else 5
        _cm=rog.prompt( x1,y1+iy,ww,6,maxw=20,
            q="How tall are you? (press a key from 1 to 9. {} is average)".format(avg),
            mode="wait" )
        try:
            _cm = int(_cm)
        except:
            _cm = avg
        if (_cm==0 or not _cm): _cm=avg
        _cmMult = 1 + (_cm - 5)/20
        
        # print char data so far
        _printElement("name: {}".format(_name), iy-2)
        _printElement("gender: {}".format(_genderName), iy-1)
        iy=_printElement("height: {} / 9".format(_cm), iy)
        print("height chosen: ", _cm)
        #
        
        _kg=rog.prompt( x1,y1+iy,ww,6,maxw=20,
            q="How heavy are you? (press a key from 1 to 9. 3 is average)",
            mode="wait" )
        try:
            _kg = int(_kg)
        except:
            _kg = 3
        if (_kg==0 or not _kg): _kg=3
        _kgMult = 1 + (_kg - 3)/8
        
        # print char data so far
        _printElement("name: {}".format(_name), iy-3)
        _printElement("gender: {}".format(_genderName), iy-2)
        _printElement("height: {} / 9".format(_cm), iy-1)
        iy=_printElement("mass: {} / 9".format(_kg), iy)
        print("mass chosen: ", _kg)
        #
        
        
        # class
        rog.dbox(x1,y1+iy,ww,3,text="What is your profession?",
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
        _className = rog.menu("Class Select",xx,yy+iy,_menuList,autoItemize=False)
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
        
        #add specific class skills
        for sk_id in _jobskills:
            rog.setskill(pc, sk_id, SKILL_LEVELS_JOB)
        
        # print char data so far
        print("class chosen: ", _className)
        _printElement("name: {}".format(_name), iy-4)
        _printElement("gender: {}".format(_genderName), iy-3)
        _printElement("height: {} / 9".format(_cm), iy-2)
        _printElement("mass: {} / 9".format(_kg), iy-1)
        iy=_printElement("class: {}".format(_className), iy)
        #
        
        
        # TODO: attribute selection (??)
        # cannot use traditional menu. Must create dedicated UI

        
        # TODO: strengths/weaknesses
        
        
        # skills (TODO: test new system of skills -- only one dict of skills, and you can pick up to 6(?) of them...
        _skillNames=[]
        _skillIDs=[]
        ptsRemaining=SKILLPOINTS
        cancel=False
            
        while ptsRemaining:
            skilldict={}
            for k, sk in SKILLS.items():
                x = rog.getskill(pc, k)//SKILL_INCREQ
                string = "{}: {}".format(sk[0] + x, sk[1])
                skilldict.update({string : k})
                
            _drawskills(0, skillscompo)
            rog.dbox(x1,y1+iy,ww,3,
                     text="choose a skill",
                     wrap=True,border=None, con=rog.con_final(), disp='mono'
                     )
            _skill = rog.menu( "skill points: {}".format(ptsRemaining),
                xx,yy,skilldict.keys() )
            if _skill == -1: # Esc
                break
            
            #get the skill ID
            _skillID = skilldict[_skill]
            _skillName = SKILLS[_skillID][1]
            _skillPts = SKILLS[_skillID][0] + rog.getskill(pc, _skillID)//SKILL_INCREQ
            if _skillPts==0: # "cancel"
                break
            if ptsRemaining < _skillPts:
                # NOT ENOUGH SKILL POINTS REMAINING.
                rog.dbox(0,0,rog.window_w(),5,
                         text='''Not enough skill points remaining.
Choose another skill.
(Points remaining: {})'''.format(ptsRemaining),
wrap=False,con=rog.con_final(),disp='mono'
                         )
                rog.refresh()
                rog.Input(rog.window_w()-2,1,mode='wait')
                continue
            
            # successfully selected skill
            rog.setskill(pc, _skillID, min(
                100, rog.getskill(pc, _skillID) + SKILL_LEVELS_PER_SELECTION) )
            
            ptsRemaining -= _skillPts
            print("skill chosen: {} (pts: {})".format(_skillName, ptsRemaining))
            _skillNames.append(_skillName)
            _skillIDs.append(_skillID)
        # end while

        
        # confirmation
        libtcod.console_clear(rog.con_final())
        cm = int(height*_cmMult)
        kg = int(_mass*_kgMult)
        
        # print char data
        iy=0
        iy=_printElement("name: {}".format(_name), iy)
        iy=_printElement("gender: {}".format(_genderName), iy)
        iy=_printElement("class: {} ({})".format(_className, _type), iy)
        iy=_printElement("height: {} cm ({} / 9)".format(cm, _cm), iy)
        iy=_printElement("mass: {} kg ({} / 9)".format(kg, _kg), iy)
        _drawskills(rog.con_final(), skillscompo)
        rog.refresh()
        #
        
        # prompt to continue or restart chargen
        _ans=''
        while _ans!='y':
            # roll character
##            reroll(statscompo, skillscompo)
            _ans=rog.prompt(x1,rog.window_h()-4,ww,4,maxw=20,
                            q="continue with this character? y/n", #/r (reroll)
                            mode="wait"
                            )
            if _ans.lower()=='n':
                return chargen(sx,sy)
##            if _ans.lower()=='r':
##                reroll(statscompo, skillscompo)
        #
        
            
        #stats?
        _stats = {}
        #gift?
        _gift = 0
        

            #----------------------------------#
            #      Finish creating entity      #
            #----------------------------------#
        
        # calculate some more stats
        
        # mass stat mods
        fatratio=DEFAULT_BODYFAT_HUMAN
        if _kg >= 5:
            fatratio += (_kg-4)/16
        elif _kg < 3:
            fatratio -= fatratio*(3-_kg)/3
        print("bodyfat: ", fatratio)
        
        # height stat mods
        reachMult = 1 + (_cm-5)/20 #/10
        if _cm < 5:
            mspMult = 1 + (_cm-5)/24 #/12
        else:
            mspMult = 1 + (_cm-5)/32 #/16
            
        # create body
        body, basekg = rog.create_body_humanoid(
            mass=kg, height=cm, female=female,
            bodyfat=fatratio)
        body.hydration = body.hydrationMax * 0.98
        body.satiation = body.satiationMax * 0.85
        # body temperature
        meters = cmp.Meters()
        meters.temp = BODY_TEMP[BODYPLAN_HUMANOID][0]
        
        #create pc object from the data given in chargen
        
        # add components to entity
        world.add_component(pc, body)
        world.add_component(pc, meters)
        world.add_component(pc, cmp.Player())
        world.add_component(pc, cmp.Name(_name, title=_title))
        world.add_component(pc, cmp.Draw('@', COL['white'], COL['deep']))
        world.add_component(pc, cmp.Position(sx, sy))
        world.add_component(pc, cmp.Actor())
        world.add_component(pc, cmp.Form(
            mat=MAT_FLESH, val=VAL_HUMAN*MULT_VALUE ))
        world.add_component(pc, cmp.Creature(
            job=_className, faction=FACT_ROGUE, species=SPECIE_HUMAN ))
        world.add_component(pc, cmp.SenseSight())
        world.add_component(pc, cmp.SenseHearing())
        world.add_component(pc, cmp.Mutable())
        world.add_component(pc, cmp.Inventory())
        world.add_component(pc, cmp.Gender(_genderName,_pronouns))
        world.add_component(pc, cmp.Stats(
            hp=BASE_HP, mp=BASE_MP, mpregen=BASE_MPREGEN*MULT_STATS,
            mass=basekg, # base mass before weight of water and blood and fat is added
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
            reach=BASE_REACH*MULT_STATS*reachMult,
            spd=BASE_SPD, asp=BASE_ASP, msp=BASE_MSP*mspMult,
            sight=0, hearing=0, # senses gained from Body component now. TODO: do the same things for monster gen...
            courage=BASE_COURAGE + PLAYER_COURAGE, # + MAS_COU if not female else 0,
            scary=BASE_SCARY, # + MAS_IDN if not female else 0,
            beauty=BASE_BEAUTY # + FEM_BEA if female else 0
            ))
        
        #add specific class stats
        for stat, val in _jobstats:
            value=val*MULT_STATS if stat in STATS_TO_MULT.keys() else val
            rog.alts(pc, stat, value)
    # end if

    
    # init
    rog.register_entity(pc)
    rog.add_listener_sights(pc)
    rog.add_listener_sounds(pc)
    rog.grid_insert(pc)
    rog.update_fov(pc)
    init(pc)
    return pc
#

# LOCAL FUNCTIONS

def _add_gender():
    x1=5
    y1=5
    ww=25
    hh=6
    #get new gender name
    _genderName=rog.prompt(x1,y1,ww,hh,maxw=20, q="What is your gender?", mode="text")
    #pronouns
    #subject pronoun
    _pronoun1=rog.prompt(
        x1,y1,ww,hh,maxw=10,
        q="What are your pronouns?\n\tSubject pronoun:",
        default="they",mode="text",insert=True
        )
    #object pronoun
    _pronoun2=rog.prompt(
        x1,y1,ww,hh,maxw=10,
        q="What are your pronouns?\n\tObject pronoun:",
        default="them",mode="text",insert=True
        )
    #possessive pronoun
    _pronoun3=rog.prompt(
        x1,y1,ww,hh,maxw=10,
        q="What are your pronouns?\n\tPossessive pronoun:",
        default="their",mode="text",insert=True
        )
    #confirm
    success=rog.prompt(x1,y1,50,15,
q='''Confirm gender: {}\nSubject pronoun: {}\nObject pronoun: {}
Possessive pronoun: {}
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




                    
                    
    


