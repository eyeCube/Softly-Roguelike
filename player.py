'''
    player.py
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




#
#   init player object. Pass an entity into the function...
#

def init(pc):
    
    # register for sense events for the message log
##    rog.add_listener_sights(pc) # TODO: implement this... There is a distinction btn. Events object for regular listening events of sights/sounds, and also two more classes for sights seen and sounds heard by the player. These should probably work differently...
##    rog.add_listener_sounds(pc)
    compo=rog.world().component_for_entity(pc, cmp.SenseSight)
    compo.fov_map=rog.fov_init()
    rog.view_center(pc)
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
            print("INVENTORY ACCESS (TODO: FIX)")
##            action.inventory_pc(pc)
            return

#
#   commands
#

def _Update():
    rog.update_game()
##    rog.update_final()
    rog.update_hud()
def commands(pc, pcAct):
    world = rog.world()

    directional_command = 'move'
    
    for act,arg in pcAct:
        
        rog.update_base()

        # actions that take multiple turns
        busyTask=rog.occupations(pc)
        if busyTask:
            if not rog.occupation_elapse_turn(pc):
                # interrupted
##                rog.Input("")
                pass
        
        #----------------#
        # convert action #
        #----------------#
        
        if act =='context-dir':
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
            
            rog.path_compute(pc.path, pos.x,pos.y, rog.mapx(mousex), rog.mapy(mousey))
            #rog.occupation_set(pc,'path')

        if act == 'rclick':
            pass
        
#------------OTHER ACTION--------------------------#

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
            dx,dy,dz=arg
            pos = world.component_for_entity(pc, cmp.Position)
            actor = world.component_for_entity(pc, cmp.Actor)
            xto=pos.x + dx
            yto=pos.y + dy

            # wait
            if (xto==pos.x and yto==pos.y):
                actor.ap = 0
                _Update()
                return

            # out of bounds
            if ( not rog.is_in_grid_x(xto) or not rog.is_in_grid_y(yto) ):
                return
            
            # fight if there is a monster present
            mon = rog.monat(xto,yto)
            if mon: # and mon != pc):
                _Update()
                action.fight(pc,mon)
            # or move
            elif not rog.solidat(xto,yto):
                # space is free, so we can move
                if action.move(pc, dx,dy):
                    _Update()
                    rog.view_center_player()
        # end conditional
        
        # "attack" : (x, y, z,)
        if act == 'attack':
            xto,yto,zto=arg
            pos = world.component_for_entity(pc, cmp.Position)
            actor = world.component_for_entity(pc, cmp.Actor)

            # out of bounds
            if ( not rog.is_in_grid_x(xto) or not rog.is_in_grid_y(yto) ):
                return
            
            # fight if there is a monster present
            mon = rog.monat(xto,yto)
            if mon == pc:
                rog.alert("You can't fight yourself!")
            if mon:
                _Update()
                action.fight(pc,mon)
            else:
                _Update()
                ent = rog.thingat(xto,yto)
                if ent:
                    action.fight(pc,ent)
                else:
                    rog.msg("You strike out at thin air, losing your balance.")
                    actor.ap = 0
                    rog.topple(pc, STRIKE_AIR_IMBALANCE_AMOUNT)
        # end conditional

        if act == "get":
            action.pickup_pc(pc)
            return
        if act == "open": #open or close
            action.open_pc(pc)
            return
        if act == "sprint": #begin sprinting
            action.sprint_pc(pc)
            return
        if act == "target": #target entity + fire / throw / attack
            action.target_pc(pc)
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
    
    world = rog.world()
    # init
    x1 = 0; y1 = 0;
    xx = 0; yy = 3;
    iy = 0;
    ww = rog.window_w(); hh = 5;
    
    # draw the string to con_game
    def _printElement(elemStr,iy):
        rog.dbox(x1,y1+iy,ww,3,text=elemStr,
            wrap=False,border=None,con=rog.con_game(),disp='mono')

        return iy+1
    # end def
    
    # get char data from player
    
    # name
    _name=rog.prompt(x1,y1,ww,hh,maxw=20, q="What is your name?", mode="text")
    _title = ""
    print("name chosen: ", _name)
##    iy+=1

    # load saved game
    loadedGame = False
    savedir=os.listdir(os.path.join(os.path.curdir,"save"))
    for filedir in savedir:
        if ".save" != filedir[-5:] :
            continue #wrong filetype
        try:
            with open(filedir, "r") as save:
                line = save.readline()
                if ("name:{}\n".format(_name) == line):
                    #found a match. Begin reading data
                    pc=loadFromSaveFile(save)                    
                    return pc
        except FileNotFoundError:
            pass
        except:
            print("ERROR: Corrupted save file detected.")
            print("Continuing chargen...")
            break

    # make a new character
    if not loadedGame:
        #continue chargen...
        
        # gender
        rog.dbox(x1,y1+iy,ww,3,text="What is your gender?",
            wrap=True,border=None,con=rog.con_final(),disp='mono')
        rog.refresh()
        #get added genders
        _genderList = {}
        genderFileDir=os.path.join(os.path.curdir,"settings","genders.txt")
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
                    print("YOOOO")
                elif _gender == 'female':
                    _genderName = "female"
                    _pronouns = ('she','her','hers',)
        print("gender chosen: ", _genderName)
##        iy+=1
        
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
        if _className == 'random':
            _classID = random.choice(_randList)
            _className = "__CLASSNAME__" #TEMP:  #jobs.getName(_classID)
        #get the relevant data
        _type = _classList[_className][0] # get the class Char value
        _mask = _type
        _classID = _classList[_className][1]
        _mass = entities.getJobMass(_classID)
        _stats = entities.getJobStats(_classID).items()
        _skills = entities.getJobSkills(_classID)
        
        #grant stats / abilities of your chosen class
        
        print("class chosen: ", _className)
##        iy+=1

        # skills
        _data=(("combat",SKILLS_COMBAT,),
               ("physical/technical",SKILLS_PHYSTECH,),
               ("crafting",SKILLS_CRAFTING,), )
        _skillNames=[]
        _skillIDs=[]
        for _str,_st in _data:
            rog.dbox(x1,y1+iy,ww,3,
                     text="choose 1 {} skill".format(_str),
                     wrap=True,border=None, con=rog.con_final(), disp='mono'
                     )
            #rog.refresh()
                #get list of all skills
            # TODO: remove all skills from this list that you already have from job
            _skillName = rog.menu(
                "{} skill select".format(_str), xx,yy+iy, _st.values()
                )
            #get the skill ID
            for skid,name in _st.items():
                if name == _skillName:
                    _skillID = skid
                    break
            print("{} skill chosen: {}".format(_str, _skillName))
            #should show ALL skills you're skilled in, not just the one you pick
            #for skill in jobs.getSkills(_skillID):
##            iy+=1
            _skillNames.append(_skillName)
            _skillIDs.append(_skillID)
        #
        
        # confirmation
        iy=_printElement("name: {}".format(_name),iy)
        iy=_printElement("gender: {}".format(_genderName),iy)
        iy=_printElement("class: {}".format(_className),iy)
        iy=_printElement("{} skill: {}".format(_data[0][0], _skillNames[0]),iy)
        iy=_printElement("{} skill: {}".format(_data[1][0], _skillNames[1]),iy)
        iy=_printElement("{} skill: {}".format(_data[2][0], _skillNames[2]),iy)
        rog.blit_to_final(rog.con_game(),0,0)
        rog.refresh()
        _ans=rog.prompt(x1,y1+7,ww,hh,maxw=20,
                        q="continue with this character? y/n",
                        mode="wait"
                        )
        if not _ans.lower()=='y':
            return chargen(sx,sy)
        #
            
        #stats?
        _stats = {}
        #gift?
        _gift = 0
        
        # mass, height
        mass = 70 # temporary
        height = 175 # temporary
            
        # create body
        body, newmass = rog.create_body_humanoid(
            mass=mass, height=height, female=(_genderName=="female") )
        
        meters = cmp.Meters()
        meters.temp = BODY_TEMP[BODYPLAN_HUMANOID][0]
        
        #create pc object from the data given in chargen
        
        # create entity
        pc = world.create_entity(
            body,meters,
            cmp.Player(),
            cmp.Name(_name, title=_title),
            cmp.Draw('@', COL['white'], COL['deep']),
            cmp.Position(sx, sy),
            cmp.Actor(),
            cmp.Form( mat=MAT_FLESH, val=VAL_HUMAN*MULT_VALUE ),
            cmp.Creature(job=_className, faction=FACT_ROGUE),
            cmp.Gender(_genderName,_pronouns),
            cmp.Stats(
                hp=BASE_HP, mp=BASE_MP,
                mass=newmass, # base mass before weight of water and blood and fat is added
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
                spd=BASE_SPD, asp=BASE_ASP, msp=BASE_MSP,
                sight=0, hearing=0, # senses gained from Body component now. TODO: do the same things for monster gen...
                courage=BASE_COURAGE, scary=BASE_SCARY
                ),
            cmp.Skills(), cmp.Flags(),
            cmp.SenseSight(), cmp.SenseHearing(),
            cmp.Mutable(),
            cmp.Inventory(),
        )
        
        
        #add specific class stats
##        for _var, _value in _stats:
##            #compo= # get component somehow...
##            world.component_for_entity(pc, compo).__dict__[_var] += _value
        #add specific class skills
        for sk_id in _skills:
            rog.setskill(pc, sk_id, 25)
        #add additional skill
        for sk_id in _skillIDs: # TODO: allow player to select skills to spend skill points on, each purchase is worth 5 levels of that skill and goes into the list (_skillIDs)
            rog.setskill(pc, sk_id, 5) # 15
    # init
    rog.register_creature(pc)
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
        genderFileDir=os.path.join(os.path.curdir,"settings",genderFileName)
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




                    
                    
    


