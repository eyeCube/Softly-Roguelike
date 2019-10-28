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
import action
import debug
import jobs
import dice





#
#   init player object. Pass a Thing into the function...
#

def init(pc):
    
    # register for sense events for the message log
    rog.add_listener_sights(pc)
    rog.add_listener_sounds(pc)
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
        if act == "inventory" :
            action.inventory_pc(pc)
            return


#
#   commands
#

directional_command = 'move'

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
                return

            # out of bounds
            if ( not rog.is_in_grid_x(xto) or not rog.is_in_grid_y(yto) ):
                return
            
            # fight if there is a monster present
            mon = rog.monat(xto,yto)
            if (mon and mon is not pc):
                action.fight(pc,mon)
            # or move
            elif not rog.solidat(xto,yto):
                # space is free, so we can move
                if action.move(pc, dx,dy):
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
            rog.update_base()
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
    xx = 0; yy = 4;
    iy = 0;
    ww = rog.window_w(); hh = 5;

    # _printElement - local function
    # draw the string to con_game at (x1,y1) then move y vars down
    def _printElement(elemStr):
        #global yy,y1,x1
        rog.dbox(x1,y1+iy,ROOMW,3,text=elemStr,
            wrap=False,border=None,con=rog.con_game(),disp='mono')
        rog.blit_to_final(rog.con_game(),0,0)
        rog.refresh()
    
    # get char data from player
    
    # name
    _name=rog.prompt(x1,y1,ww,hh,maxw=20, q="What is your name?", mode="text")
    _title = ""
    print("Name chosen: ", _name)
    _printElement("Name: {}".format(_name))
    iy+=1

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
        rog.dbox(x1,y1+iy,ROOMW,3,text="What is your gender?",
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
        print("Gender chosen: ", _genderName)
        _printElement("Gender: {}".format(_genderName))
        iy+=1
        
        # class
        rog.dbox(x1,y1+iy,ROOMW,3,text="What is your profession?",
            wrap=True,border=None,con=rog.con_final(),disp='mono')
        rog.refresh()
        _classList={} #stores {className : (classChar, classID,)} #all classes
        #create menu options
        _menuList={} #stores {classChar : className} #all playable classes
        _randList=[] #for random selection.
        for k,v in jobs.getJobs().items(): # k=ID v=charType
            if v not in rog.playableJobs(): continue #can't play as this class yet
            ID=k        # get ID of the class
            typ=v       # get chartype of the class
            name=jobs.getName(ID)
            _classList.update({name:(typ,ID,)})
            _menuList.update({typ:name})
            _randList.append(ID)
        _menuList.update({'*':'random'})
        #user selects a class
        _className = rog.menu("Class Select",xx,yy,_menuList,autoItemize=False)
        #random
        if _className == 'random':
            _classID = random.choice(_randList)
            _className = jobs.getName(_classID)
        #get the relevant data
        _type = _classList[_className][0] # get the class Char value
        _mask = _type
        _classID = _classList[_className][1]
        
        #grant stats / abilities of your chosen class
        
        print("Class chosen: ", _className)
        _printElement("Class: {}".format(_className))
        iy+=1

        # skill
        rog.dbox(x1,y1+iy,ROOMW,3,text="In which skill are you learned?",
            wrap=True,border=None,con=rog.con_final(),disp='mono')
        #rog.refresh()
            #get list of all skills
        _skillName = rog.menu("Skill Select",xx,yy,SKILLS.values())
        #get the skill ID
        for skid,name in SKILLS.items():
            if name == _skillName:
                _skillID = name
                break
        print("Skill chosen: ", _skillName)
        #should show ALL skills you're skilled in, not just the one you pick
        #for skill in jobs.getSkills(_skillID):
        _printElement("Skills: {}".format(_skillName))
        iy+=1

        #stats?
        _stats = {}
        #gift?
        _gift = 0

        #create pc object from the data given in chargen
        
##        pc = world.create_entity( # USE create_monster function!!!!
##            cmp.Position(sx,sy),
##            cmp.Name(_name, title=_title,pronouns=_pronouns),
##            cmp.Draw('@', COL['white']),
##            cmp.Form(
##            )
        
##        pc = rog.create_monster('@',0,0,COL['white'],mutate=0)
##        pc.name = _name
##        pc.title = _title
##        pc.mask = '@'
##        pc.job = _className
##        pc.gender = _genderName
##        pc.pronouns = _pronouns
##        pc.faction = FACT_ROGUE
##        #add additional skill
##        rog.train(pc,_skillID)
##        #add specific class stats
    
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




                    
                    
    
    '''
    pc = rog.create_monster('@',0,0,COL['white'],mutate=0)
    pc.name=save.readline().strip()
    pc.title=save.readline().strip()
    pc.pronouns=save.readline().strip()
    pc.color=save.readline().strip()
    pc.bgcolor=save.readline().strip()
    pc.flags=set((save.readline().strip()).split(','))
    #read in skills
    #read in equip data
    #read in stat mods
    #pc.isSolid=save.readline().strip()
    pc.x=save.readline().strip()
    pc.y=save.readline().strip()
    pc.z=save.readline().strip()
    pc.type=save.readline().strip()
    pc.mask=save.readline().strip()
    pc.mutations=save.readline().strip()
    pc.gender=save.readline().strip()
    pc.job=save.readline().strip()
    pc.faction=save.readline().strip()
    #read in fov_map
    #pc.senseEvents=save.readline().strip()
    pc.purse=save.readline().strip()
    pc.ai=save.readline().strip()
    pc.stats.sight=save.readline().strip()
    pc.stats.hearing=save.readline().strip()
    pc.stats.nrg=save.readline().strip()
    pc.stats.spd=save.readline().strip()
    pc.stats.asp=save.readline().strip()
    pc.stats.msp=save.readline().strip()
    pc.stats.carry=save.readline().strip()
    pc.stats.atk=save.readline().strip()
    pc.stats.dmg=save.readline().strip()
    pc.stats.dfn=save.readline().strip()
    pc.stats.arm=save.readline().strip()
    pc.stats.hp=save.readline().strip()
    pc.stats.hpmax=save.readline().strip()
    pc.stats.mp=save.readline().strip()
    pc.stats.mpmax=save.readline().strip()
    pc.stats.element=save.readline().strip()
    pc.stats.resfire=save.readline().strip()
    pc.stats.resbio=save.readline().strip()
    pc.stats.reselec=save.readline().strip()
    pc.stats.temp=save.readline().strip()
    pc.stats.rads=save.readline().strip()
    pc.stats.expo=save.readline().strip()
    pc.stats.sick=save.readline().strip()
    '''

'''
            # TESTING INPUT
            rog.update_final()
            text = rog.Input(0,0, 40,1)
            print("returned '" + text + "'")
            
                    ## TESTING TESTING WHY DON'T YOU ARRESTING
                    rog.Ref.Map.recall_memories(rog.view_x(),rog.view_y(),rog.view_w(),rog.view_h())
                    action.move(pc,14,14)
                    rog.Ref.Map.tile_change(pc.x,pc.y,FLOOR)
                    rog.Ref.Map.tile_change(pc.x,pc.y-1,FLOOR)
                    rog.Ref.Map.tile_change(pc.x,pc.y-2,FLOOR)
                    rog.Ref.Map.tile_change(pc.x-1,pc.y-2,FLOOR)
                    rog.Ref.Map.tile_change(pc.x-1,pc.y-1,FLOOR)
                    rog.Ref.Map.tile_change(pc.x-1,pc.y,FLOOR)
                    rog.view_center(pc)
                    ##
                    '''


