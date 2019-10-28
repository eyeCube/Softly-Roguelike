'''
    player.py
    Part of Softly Into the Night, a roguelike by Jacob Wharton.
    Copyright 2019.

    TODO : finish up chargen function
    
'''

import os
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
        if act == "inventory" :
            action.inventory_pc(pc)
            return


#
#   commands
#

directional_command = 'move'

def _Update():
    rog.update_game()
##    rog.update_final()
    rog.update_hud()
def commands(pc, pcAct):
    world = rog.world()
    
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
        
        if act =='target':  act=directional_command
        
        
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
            if (mon and mon is not pc):
                _Update()
                action.fight(pc,mon)
            # or move
            elif not rog.solidat(xto,yto):
                # space is free, so we can move
                if action.move(pc, dx,dy):
                    _Update()
                    rog.view_center_player()

        if act == "get":
            action.pickup_pc(pc)
            return
        if act == "open": #open or close
            action.open_pc(pc)
            return
        if act == "sprint": #begin sprinting
            action.sprint_pc(pc)
            return
        if act == "throw": #throw an object
            action.throw_pc(pc)
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
            print("ALERT: file '{}' not found. Creating new file...")
            with open(genderFileDir, "w+") as file:
                file.write("\n")
        
        #gender selection
        _gender = ''
        while (_gender == ''):
            _menuList={'m':'male','f':'female','n':'nonbinary','*':'random',}
            #read genders from genders.txt
            
            _gender=rog.menu("Gender Select",xx,yy,_menuList,autoItemize=False)
            if _gender == 'nonbinary':
                #select gender from list of added genders
                _menuNonbin=[]
                for jj in _genderList.keys():
                    _menuNonbin.append(jj)
                _menuNonbin.append('add new gender')
                choice=rog.menu("Nonbinary Genders",xx,yy,_menuNonbin)
                #add gender
                if choice == 'add new gender':
                    _genderName,_pronouns = _add_gender()
                else:
                    _genderName = choice
                    _pronouns = _genderList[_genderName]
                if _genderName=='': #failed to select or add new gender
                    _gender='' #prompt user again for gender
            else: #random, male and female
                if _gender == 'random':
                    _gender = random.choice(("male","female",))
                if _gender == 'male':
                    _genderName = "male"
                    _pronouns = ('he','him','his',)
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
            _className = "__CLASSNAME__"  #jobs.getName(_classID)
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
        
        #create pc object from the data given in chargen
        pc = world.create_entity(
            cmp.Name(_name, title=_title),
            cmp.Draw('@', COL['white'], COL['deep']),
            cmp.Position(sx, sy),
            cmp.Actor(),
            cmp.Form( mat=MAT_FLESH, val=VAL_HUMAN*MULT_VALUE ),
            cmp.Creature(job=_className, faction=FACT_ROGUE),
            cmp.Gender(_genderName,_pronouns),
            cmp.Stats(
                hp=BASE_HP, mp=BASE_MP, mass=0,#round(_mass*MULT_MASS), #TODO: mass calculated by body / inventory
                resfire=BASE_RESFIRE,
                rescold=BASE_RESCOLD,
                resbio=BASE_RESBIO,
                reselec=BASE_RESELEC,
                resphys=BASE_RESPHYS,
                reswet=BASE_RESWET,
                respain=BASE_RESPAIN,
                resbleed=BASE_RESBLEED,
                resrust=BASE_RESRUST,
                resrot=BASE_RESROT,
                _str=BASE_STR, _con=BASE_CON, _int=BASE_INT,
                gra=BASE_GRA, bal=BASE_BAL, ctr=BASE_CTR,
                atk=BASE_ATK, dmg=BASE_DMG, pen=BASE_PEN,
                dfn=BASE_DFN, arm=BASE_ARM, pro=BASE_PRO,
                spd=BASE_SPD, asp=BASE_ASP, msp=BASE_MSP,
                sight=BASE_SIGHT, hearing=BASE_HEARING,
                courage=BASE_COURAGE, scary=BASE_SCARY
                ),
            cmp.Skills(), cmp.Flags(),
            cmp.SenseSight(), cmp.SenseHearing(),
            cmp.Mutable(),
            cmp.Inventory(BASE_CARRY),
        )

        # create body
        body = rog.create_humanoid(_mass*MULT_MASS)
        rog.world().add_component(pc, body)
        
        
        #add specific class stats
##        for _var, _value in _stats:
##            #compo= # get component somehow...
##            world.component_for_entity(pc, compo).__dict__[_var] += _value
        #add specific class skills
        for skid in _skills:
            rog.train(pc,skid)
        #add additional skill
        for skid in _skillIDs:
            rog.train(pc,skid)
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




                    
                    
    


