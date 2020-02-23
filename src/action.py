'''
    action.py
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

# wrapper for things that creatures can do in the game
#   - actions cost energy
# PC actions are for the player object to give feedback
#   - (if you try to eat something inedible, it should say so, etc.)
#

import math

from const import *
import rogue as rog
import components as cmp
import dice
import maths
##import entities


dirStr=" <hjklyubn.>"


def _get_eq_data(equipType):
    if equipType == EQ_MAINHAND:
        return (wield_main, "wield", "hand",)
    elif equipType == EQ_OFFHAND:
        return (wield_off, "wield", "hand",)
    elif equipType == EQ_MAINARM:
        return (wear_arm_main, "wear", "arm",)
    elif equipType == EQ_OFFARM:
        return (wear_arm_off, "wear", "arm",)
    elif equipType == EQ_MAINFOOT:
        return (wear_foot_main, "wear", "foot",)
    elif equipType == EQ_OFFFOOT:
        return (wear_foot_off, "wear", "foot",)
    elif equipType == EQ_MAINLEG:
        return (wear_leg_main, "wear", "leg",)
    elif equipType == EQ_OFFLEG:
        return (wear_leg_off, "wear", "leg",)
    elif equipType == EQ_CORE:
        return (wear_core, "wear", "core",)
    elif equipType == EQ_FRONT:
        return (wear_front, "wear", "front",)
    elif equipType == EQ_BACK:
        return (wear_back, "wear", "back",)
    elif equipType == EQ_HIPS:
        return (wear_hips, "wear", "hips",)
    elif equipType == EQ_MAINHEAD:
        return (wear_head, "wear", "head",)
    elif equipType == EQ_MAINNECK:
        return (wear_neck, "wear", "neck",)
    elif equipType == EQ_MAINFACE:
        return (wear_face, "wear", "face",)
    elif equipType == EQ_MAINEYES:
        return (wear_eyes, "wear", "eyes",)
    elif equipType == EQ_MAINEARS:
        return (wear_ears, "wear", "ears",)
    

    # PC-specific actions first #

# pickup
# grab an item from the game world, removing it from the grid
def pickup_pc(pc):
    world = rog.world()
    pos = world.component_for_entity(pc, cmp.Position)
    pcx = pos.x
    pcy = pos.y
    rog.alert("Pick up what?{d}".format(d=dirStr))
    args=rog.get_direction()
    if not args:
        rog.alert()
        return
    dx,dy,dz=args
    xx,yy = pcx + dx, pcy + dy
    
    things=rog.thingsat(xx,yy)
    if pc in things: #can't pick yourself up.
        things.remove(pc)

    choice=None
    if len(things) > 1:
        rog.alert("There are multiple things here. Pick up which item?")
        choices = [] #["all",] #should player be able to pickup multiple things at once? Maybe could be a delayed action?
        for thing in things:
            choices.append(thing)
        choice=rog.menu(
            "pick up", rog.view_port_x()+2, rog.view_port_y()+2, choices
            )
    else:
        if things:
            choice=things[0]

    if (choice and not choice == "all"):

        if choice == K_ESCAPE:
            return
        
        #thing is creature! You can't pick up creatures :( or can you...?
        if world.has_component(choice, cmp.Creature):
            rog.alert("You can't pick that up!")
            return
        #thing is on fire, prompt user & burn persistent rogues
##        if rog.on(choice,FIRE):
##            answer=""
##            while True:
##                answer=rog.prompt(0,0,rog.window_w(),1,maxw=1,
##                    q="That thing is on fire! Are you sure? y/n",
##                    mode='wait',border=None)
##                answer=answer.lower()
##                if answer == "y" or answer == " " or answer == K_ENTER:
##                    rog.alert("You burn your hands!")
##                    rog.burn(pc, FIRE_BURN)
##                    rog.hurt(pc, FIRE_PAIN)
##                    rog.damage(pc, FIRE_DAMAGE)
##                    break
##                elif answer == "n" or answer == K_ESCAPE:
##                    return
        # put in inventory
        pocketThing(pc, choice)
        
##    elif choice == "all": # TODO
##        for tt in things:
##            pocketThing(pc, tt)
        
    else:
        rog.alert("There is nothing there to pick up.")


def inventory_pc(pc):
    world=rog.world()
    assert world.has_component(pc, cmp.Inventory), "PC missing inventory"
    pcInv = world.component_for_entity(pc, cmp.Inventory)
    pcn = world.component_for_entity(pc, cmp.Name)
    x=0
    y=rog.view_port_y()
#   items menu
    item=rog.menu("{}{}'s Inventory".format(
        pcn.title,pcn.name), x,y, pcInv.data)
    
#   viewing an item
    if not item == -1:
        itemn = world.component_for_entity(item, cmp.Name)
##        itemn = world.component_for_entity(item, cmp.Name)
        keysItems={}
        
    #   get available actions for this item...
        if world.has_component(item, cmp.Edible):
            keysItems.update({"e":"eat"})
        if world.has_component(item, cmp.Quaffable):
            keysItems.update({"q":"quaff"})
        if world.has_component(item, cmp.EquipableInHoldSlot):
            keysItems.update({"w":"wield"})
            # throwables - subset of equipables
            if world.has_component(item, cmp.Throwable):
                keysItems.update({"t":"throw"})
        if (world.has_component(item, cmp.EquipableInHandSlot)
            or world.has_component(item, cmp.EquipableInArmSlot)
            or world.has_component(item, cmp.EquipableInFootSlot)
            or world.has_component(item, cmp.EquipableInLegSlot)
            or world.has_component(item, cmp.EquipableInFrontSlot)
            or world.has_component(item, cmp.EquipableInCoreSlot)
            or world.has_component(item, cmp.EquipableInBackSlot)
            or world.has_component(item, cmp.EquipableInHipsSlot)
            or world.has_component(item, cmp.EquipableInAboutSlot)
            or world.has_component(item, cmp.EquipableInHeadSlot)
            or world.has_component(item, cmp.EquipableInFaceSlot)
            or world.has_component(item, cmp.EquipableInEyesSlot)
            or world.has_component(item, cmp.EquipableInEarsSlot)
            or world.has_component(item, cmp.EquipableInNeckSlot)
            ):
            keysItems.update({"W":"Wear"})
        if world.has_component(item, cmp.Usable):
            keysItems.update({"u":"use"})
        if world.has_component(item, cmp.Openable):
            keysItems.update({"o":"open"})
        keysItems.update({"x":"examine"})
        keysItems.update({"d":"drop"})
        #
        
        opt=rog.menu(
            "{}".format(itemn.name), x,y,
            keysItems, autoItemize=False
        )
        #print(opt)
        if opt == -1: return
        opt=opt.lower()
        
        rmg=False
        if   opt == "drop":     rmg=True; drop_pc(pc, item)
        elif opt == "equip":    rmg=True; equip_pc(pc, item)
        elif opt == "throw":    rmg=True; target_pc(pc, item)
        elif opt == "eat":      rmg=True; eat_pc(pc, item)
        elif opt == "quaff":    rmg=True; quaff_pc(pc, item)
        elif opt == "use":      rmg=True; use_pc(pc, item)
        elif opt == "examine":  rmg=True; examine_pc(pc, item)
        
        if rmg: rog.spendAP(pc, NRG_RUMMAGE)
#

def drop_pc(pc,item):
    rog.alert("Place {i} where?{d}".format(d=dirStr,i=item.name))
    args=rog.get_direction()
    if not args: return
    dx,dy,dz=args
    
    if not drop(pc, item):
        rog.alert("You can't put that there!")

def open_pc(pc): # open or close
    # pick what to open/close
    rog.alert("Open/close what?{d}".format(d=dirStr))
    args=rog.get_direction()
    if not args: return
    dx,dy,dz=args
    pos = rog.world().component_for_entity(pc, cmp.Position)
    xto = pos.x + dx
    yto = pos.y + dy
    # do the open/close action
    success = openClose(pc, xto, yto)
    if not success:
        return
    rog.update_game()
    rog.update_hud()
##    rog.update_fov(pc) # updated by tile change func

def sprint_pc(pc):
    #if sprint cooldown elapsed
    if rog.getms(pc,"mp") > 0:#not rog.world().has_component(pc, cmp.StatusTired):
        sprint(pc)
    else:
        rog.alert("You're too tired to sprint.")

def target_pc(pc):
    pos = world.component_for_entity(pc, cmp.Position)
    def targetfunc(target):
        # Temporary
        tname=world().component_for_entity(target, cmp.Name)
        tpos=world().component_for_entity(target, cmp.Position)
        print("Targeted entity named {} at {},{}".format(tname, tpos.x,tpos.y))
    rog.aim_find_target(targetfunc)
    
    
##def process_target(targeted):
##    
##    if targeted:
##        rog.alert("Target: {n} at ({x}, {y}) | x: strike / f: fire".format(
##            n=entname, x=pos.x,y=pos.y))
    
    

def examine_self_pc(pc):
    choices=['body (whole body)']
    
    ans=rog.menu(item=rog.menu("Examine what?".format(
        pcn.title,pcn.name), x,y, choices))

def equip_pc(pc, item, equipType):
    func, str1, str2 = _get_eq_data(equipType)

    # TODO: convert this to a queued action / get queued actions working!!
    
    result = func(pc, item) # try to equip
    
    # messages / alerts
    if result == 1:
        pass
    else:
        if result == -100:
            rog.alert("You can't {} that there.".format(str1))
        elif result == -101:
            rog.alert("You can't {} that there.".format(str1))
        elif result == -102:
            rog.alert("You are already {w}ing something in that {bp} slot.".format(w=str1, bp=str2))
# end def

def examine_pc(pc, item):
    rog.spendAP(pc, NRG_EXAMINE)
    rog.dbox(0,0,40,30, thing.DESCRIPTIONS[item.name])

def eat_pc(pc, item):
    result = eat(pc, item)
    # do something with the result

def rest_pc(pc):
    turns=rog.prompt(0,0,rog.window_w(),1,maxw=3,
                     q="How long do you want to rest? Enter number of turns:",
                     mode='wait',border=None)
    for t in range(turns):
        rog.queue_action(pc, wait)

# item use functions

##def use_towel_pc(pc, item):
##    world=rog.world()
##    options={}
####    options.update({"W" : "wrap around"}) # THESE SHOULD ALL BE COVERED BY THE EQUIPABLE COMPONENTS.
####    options.update({"w" : "wield"})
####    options.update({"h" : "wear on head"})
##    options.update({"d" : "dry [...]"})
##    options.update({"l" : "lie on"})
##    options.update({"x" : "wave"})
####    options.update({"s" : "sail"})
##    choice=rog.menu("use towel",0,0,options,autoItemize=False)
##            
##    if choice == "dry":
##        answer=rog.prompt(0,0,rog.window_w(),1,maxw=1,
##                    q="Dry what?",
##                    mode='wait',border=None)
##        # TODO: logic for what you want to dry...
####        if answer=='self' # how to handle this??????
##        #itSeemsCleanEnough=...
##        if ( itSeemsCleanEnough and not rog.on(item, WET) ):
##            pass #dry self
##        else:
##            if not itSeemsCleanEnough:
##                rog.alert("It doesn't seem clean enough.")
##            elif world.component_for_entity(item,cmp.Wets).wetness > 0:
##                rog.alert("It's too wet.")
                




#######################################################################
                    # Non-PC-specific actions #
#######################################################################


#wait
#just stand still and do nothing
#recover your Action Points to their maximum
def wait(ent):
    rog.setAP(ent, 0)
    rog.metabolism(ent, CALCOST_REST)
# end def

def cough(ent):
    world = rog.world()
    pos = world.component_for_entity(ent, cmp.Position)
    entn = world.component_for_entity(ent, cmp.Name)
    wait(ent)
    rog.event_sound(pos.x,pos.y, SND_COUGH)
    rog.event_sight(pos.x,pos.y, "{t}{n} doubles over coughing.".format(
        t=entn.title,n=entn.name))
# end def

def intimidate(ent):
    world=rog.world()
    stats=world.component_for_entity(ent, cmp.Stats)
    pos=world.component_for_entity(ent, cmp.Position)
    entn=world.component_for_entity(ent, cmp.Name)
    fear=rog.getms(ent, 'intimidation')
    world.add_component(ent, cmp.StatusFrightening(10))
    rog.event_sound(pos.x,pos.y,SND_ROAR)
    rog.event_sight(pos.x,pos.y,"{t}{n} makes an intimidating display.".format(
        t=entn.title,n=entn.name))
# end def

#use
#"use" an item, whatever that means for the specific item
# context-sensitive use action
def use(obj, item):
    pass

# equip
# try to put item in a specific slot; spend AP for success
def _equip(ent, item, equipType):
    result, compo = rog.equip(ent, item, equipType)
    if result == 1: # successfully equipped
        rog.spendAP(ent, compo.ap)

        # TODO: message
            # w and bp should be gotten from the type of equip function used, but how?
        entname = rog.world().component_for_entity(ent, cmp.Name)
        itemname = rog.world().component_for_entity(item, cmp.Name)
        rog.msg("{t}{n} {w}s {i} in {prn} {bp}".format(
            t=entname.title, n=entname.name, i=itemname.name, w="wield",
            prn=gender.pronouns[0], bp="hand"))
        
    return result
# end def

# specific equip functions (wrappers)
def wield_main(ent, item):      return _equip(ent, item, EQ_MAINHAND)
def wield_off(ent, item):       return _equip(ent, item, EQ_OFFHAND)
def wear_arm_main(ent, item):   return _equip(ent, item, EQ_MAINARM)
def wear_arm_off(ent, item):    return _equip(ent, item, EQ_OFFARM)
def wear_leg_main(ent, item):   return _equip(ent, item, EQ_MAINLEG)
def wear_leg_off(ent, item):    return _equip(ent, item, EQ_OFFLEG)
def wear_foot_main(ent, item):  return _equip(ent, item, EQ_MAINFOOT)
def wear_foot_off(ent, item):   return _equip(ent, item, EQ_OFFFOOT)
def wear_front(ent, item):      return _equip(ent, item, EQ_FRONT)
def wear_back(ent, item):       return _equip(ent, item, EQ_BACK)
def wear_hips(ent, item):       return _equip(ent, item, EQ_HIPS)
def wear_core(ent, item):       return _equip(ent, item, EQ_CORE)
def wear_head(ent, item):       return _equip(ent, item, EQ_MAINHEAD)
def wear_face(ent, item):       return _equip(ent, item, EQ_MAINFACE)
def wear_neck(ent, item):       return _equip(ent, item, EQ_MAINNECK)
def wear_eyes(ent, item):       return _equip(ent, item, EQ_MAINEYES)
def wear_ears(ent, item):       return _equip(ent, item, EQ_MAINEARS)
#

def pocketThing(ent, item): #entity puts item in its inventory
    world = rog.world()
    rog.grid_remove(item)
    rog.give(ent, item)
    rog.spendAP(ent, NRG_POCKET)
    world.add_component(item, cmp.Child(ent)) # item is Child of Entity carrying the item
    entn = world.component_for_entity(ent, cmp.Name)
    itemn = world.component_for_entity(item, cmp.Name)
    rog.msg("{t}{n} packs {ti}{ni}.".format(
        t=entn.title,n=entn.name,ti=TITLES[itemn.title],ni=itemn.name))
##    return True

def drop(ent, item):
    world = rog.world()
    pos = world.component_for_entity(ent, cmp.Position)
    dx=0; dy=0; # TODO: code AI to find a place to drop item
    if not rog.wallat(pos.x+dx,pos.y+dy):
        rog.spendAP(ent, NRG_RUMMAGE)
        rog.drop(ent,item, dx,dy)
        entn = world.component_for_entity(ent, cmp.Name)
        itemn = world.component_for_entity(item, cmp.Name)
        rog.msg("{t}{n} drops {ti}{ni}.".format(
            t=entn.title,n=entn.name,ti=itemn.title,ni=itemn.name))
        return True
    else:
        return False


#quaff
#drinking is instantaneous action
def quaff(ent, drink): 
    world = rog.world()
    pos = world.component_for_entity(ent, cmp.Position)
    quaffable=world.component_for_entity(drink, cmp.Quaffable)
    entn = world.component_for_entity(ent, cmp.Name)
    drinkn = world.component_for_entity(drink, cmp.Name)
    
    #quaff function
    quaffable.func(ent)
    
    # TODO: do delayed action instead of immediate action.
    # OBSELETE:
##    rog.drain(ent, 'nrg', quaffable.timeToConsume)
##    rog.givemp(ent, quaffable.hydration)

    #events - sight
    if ent == rog.pc():
        rog.msg("It tastes {t}".format(t=quaffable.taste))
    else:
        rog.event_sight(pos.x,pos.y, "{t}{n} quaffs a {p}.".format(
            t=entn.title, n=entn.name, p=drinkn.name))
    #events - sound
    rog.event_sound(pos.x,pos.y, SND_QUAFF)
    # TODO: make sure this works...
    world.delete_entity(drink)

def standup(ent):
    actor = rog.world().component_for_entity(ent, cmp.Actor)
    if rog.get_status(ent, cmp.StatusBPos_Crouched):
        rog.remove_status(ent, cmp.StatusBPos_Crouched)
        ap_cost = 40
    elif rog.get_status(ent, cmp.StatusBPos_Seated):
        rog.remove_status(ent, cmp.StatusBPos_Seated)
        ap_cost = 100
    elif rog.get_status(ent, cmp.StatusBPos_Prone):
        rog.remove_status(ent, cmp.StatusBPos_Prone)
        ap_cost = 200
    elif rog.get_status(ent, cmp.StatusBPos_Supine):
        rog.remove_status(ent, cmp.StatusBPos_Supine)
        ap_cost = 200
    actor.ap -= ap_cost
def crouch(ent):
    rog.set_status(ent, cmp.StatusBPos_Crouched)
    actor = rog.world().component_for_entity(ent, cmp.Actor)
    if rog.get_status(ent, cmp.StatusBPos_Seated):
        rog.remove_status(ent, cmp.StatusBPos_Seated)
        ap_cost = 100
    elif rog.get_status(ent, cmp.StatusBPos_Prone):
        rog.remove_status(ent, cmp.StatusBPos_Prone)
        ap_cost = 160
    elif rog.get_status(ent, cmp.StatusBPos_Supine):
        rog.remove_status(ent, cmp.StatusBPos_Supine)
        ap_cost = 160
    else:
        ap_cost = 25
    actor.ap -= ap_cost
def sit(ent):
    rog.set_status(ent, cmp.StatusBPos_Seated)
    actor = rog.world().component_for_entity(ent, cmp.Actor)
    if rog.get_status(ent, cmp.StatusBPos_Crouched):
        rog.remove_status(ent, cmp.StatusBPos_Crouched)
        ap_cost = 25
    elif rog.get_status(ent, cmp.StatusBPos_Prone):
        rog.remove_status(ent, cmp.StatusBPos_Prone)
        ap_cost = 100
    elif rog.get_status(ent, cmp.StatusBPos_Supine):
        rog.remove_status(ent, cmp.StatusBPos_Supine)
        ap_cost = 100
    else:
        ap_cost = 50
    actor.ap -= ap_cost
def lieprone(ent):
    rog.set_status(ent, cmp.StatusBPos_Prone)
    actor = rog.world().component_for_entity(ent, cmp.Actor)
    if rog.get_status(ent, cmp.StatusBPos_Crouched):
        rog.remove_status(ent, cmp.StatusBPos_Crouched)
        ap_cost = 100
    elif rog.get_status(ent, cmp.StatusBPos_Seated):
        rog.remove_status(ent, cmp.StatusBPos_Seated)
        ap_cost = 150
    elif rog.get_status(ent, cmp.StatusBPos_Supine):
        rog.remove_status(ent, cmp.StatusBPos_Supine)
        ap_cost = 100
    else:
        ap_cost = 100
    actor.ap -= ap_cost
def liesupine(ent):
    rog.set_status(ent, cmp.StatusBPos_Supine)
    actor = rog.world().component_for_entity(ent, cmp.Actor)
    if rog.get_status(ent, cmp.StatusBPos_Crouched):
        rog.remove_status(ent, cmp.StatusBPos_Crouched)
        ap_cost = 100
    elif rog.get_status(ent, cmp.StatusBPos_Seated):
        rog.remove_status(ent, cmp.StatusBPos_Seated)
        ap_cost = 50
    elif rog.get_status(ent, cmp.StatusBPos_Prone):
        rog.remove_status(ent, cmp.StatusBPos_Prone)
        ap_cost = 100
    else:
        ap_cost = 100
    actor.ap -= ap_cost
    
def move(ent,dx,dy, mx=1):  # actor locomotion
    '''
        move: generic actor locomotion
        Returns True if move was successful, else False
        Parameters:
            ent : entity that's moving
            dx  : change in x position
            dy  : change in y position
            mx  : AP/Calorie/Stamina cost multiplier value
    '''
    # init
    world = rog.world()
    pos = world.component_for_entity(ent, cmp.Position)
    xto = pos.x + dx
    yto = pos.y + dy
    terrainCost = rog.cost_move(pos.x, pos.y, xto, yto, None)
    if terrainCost == 0:
        return False        # 0 means we can't move there
    msp=rog.getms(ent,'msp')
    actor = world.component_for_entity(ent, cmp.Actor)
    #
    
    # AP cost
    mult = 1.414 if (dx + dy) % 2 == 0 else 1  # diagonal extra cost
    ap_cost = max(1, rog.around(
        mx * NRG_MOVE * mult * terrainCost / max(MIN_MSP, msp) ))
    actor.ap -= ap_cost
    
    # Stamina cost (TODO FOR ALL ACTIONS!)
    sta_cost = int(mx * STA_MOVE * mult)
    rog.sap(ent, sta_cost)
    
    # Satiation, hydration, fatigue (TODO FOR ALL ACTIONS!)
    cal_cost = int(mx * CALCOST_LIGHTACTIVITY * mult)
    rog.metabolism(ent, cal_cost)
    
    # perform action
    rog.port(ent, xto, yto)
    return True

def openClose(ent, xto, yto):
    #TODO: containers, test doors
    world = rog.world()
    actor = world.component_for_entity(ent, cmp.Actor)
    entn = world.component_for_entity(ent, cmp.Name)
    #open containers
    #close containers
    #open doors
    if rog.tile_get(xto,yto) == DOORCLOSED:
        actor.ap -= NRG_OPEN
        rog.tile_change(xto,yto, DOOROPEN)
        ss = "opened a door"
        rog.msg("{t}{n} {ss}.".format(t=entn.title,n=entn.name,ss=ss))
        return True
    #close doors
    if rog.tile_get(xto,yto) == DOOROPEN:
        actor.ap -= NRG_OPEN
        rog.tile_change(xto,yto, DOORCLOSED)
        ss = "closed a door"
        rog.msg("{t}{n} {ss}.".format(t=entn.title,n=entn.name,ss=ss))
        return True
    if ent==rog.pc(): rog.alert("It won't open.") # TODO: message about why you failed
    return False

def sprint(ent):
    #if sprint cooldown elapsed
    rog.world().add_component(ent, cmp.Sprint(SPRINT_TIME))
    entn = rog.world().component_for_entity(ent, cmp.Name)
    rog.msg("{n} begins sprinting.".format(n=entn.name))


def _strike(attkr,dfndr,aweap,dweap,
            adv=0,power=0, counterable=False,
            bptarget=None, targettype=None,
            apos=None, dpos=None):
    '''
        strike the target with your primary weapon or body part
            this in itself is not an action -- requires no AP
        (this is a helper function used by combat actions)

        adv         advantage to the attacker
        power       amount of power the attacker is putting into the attack
        counterable bool, can this strike be counter-striked?
        bptarget    None: aim for center mass. else a BP component object
        targettype  BP_ const indicates what type of BP is being targeted
        apos;dpos   Attacker Position component; Defender Position component
    '''
    # init
    hit=killed=crit=ctrd=grazed=False
    pens=trueDmg=rol=0
    feelStrings=[]
    
        # get the data we need
    world = rog.world()

    # components
    abody=world.component_for_entity(attkr, cmp.Body)
    dbody=world.component_for_entity(dfndr, cmp.Body)

    # skill
    if world.has_component(aweap,cmp.WeaponSkill):
        skillCompo=world.component_for_entity(aweap, cmp.WeaponSkill)
        skillLv=world.component_for_entity(attkr, cmp.Skills)
    else:
        skillCompo=None
        skillLv=0
    
    # attacker stats
    asp =   max( MIN_ASP, rog.getms(attkr,'asp') )
    acc =   rog.getms(attkr,'atk')//MULT_STATS
    pen =   rog.getms(attkr,'pen')//MULT_STATS
    dmg =   max( 0, rog.getms(attkr,'dmg')//MULT_STATS )
    areach =rog.getms(attkr,'reach')//MULT_STATS
    
    # defender stats
    dv =    rog.getms(dfndr,'dfn')//MULT_STATS
    prot =  rog.getms(dfndr,'pro')//MULT_STATS
    arm =   rog.getms(dfndr,'arm')//MULT_STATS
    ctr =   rog.getms(dfndr,'ctr')//MULT_STATS
    dreach =rog.getms(dfndr,'reach')//MULT_STATS
    resphys = rog.getms(dfndr,'resphys')

    # differences btn attacker and defender
##    dcm =   rog.getms(attkr,'height') - rog.getms(dfndr,'height')
##    dkg =   (rog.getms(attkr,'mass') - rog.getms(dfndr,'mass'))//MULT_MASS # only affects grappling, not fighting
    
    # advantages from stat differences
    # lesser reach has the advantage
    adv = dreach-areach
    
        # roll dice, calculate hit or miss
    rol = dice.roll(CMB_ROLL_ATK)
    hitDie = rol + acc + adv - dv
    if (rog.is_pc(dfndr) and rol==1): # when player is attacked, a roll of 1/20 always results in a miss.
        hit=False
    elif (rog.is_pc(attkr) and rol==20): # when player attacks, a roll of 20/20 always results in a hit.
        hit=True
    elif (hitDie >= 0): # normal hit roll, D&D "to-hit/AC"-style
        hit=True
    else: # miss
        hit=False
    
    # perform the attack
    if hit:
        grazed = (hitDie==0)

        # counter-attack
        if (counterable
        and rog.inreach(dpos.x,dpos.y, apos.x,apos.y, dreach)
        and rog.on(dfndr,CANCOUNTER)
            ):
            if (dice.roll(100) <= ctr):
                dweap = rog.dominant_arm(dfndr).hand.held.item
                _strike(
                    dfndr, attkr, dweap, aweap,
                    power=0, counterable=False
                    )
                rog.makenot(dfndr,CANCOUNTER)
                ctrd=True
        # end if
        
        # penetration (calculate armor effectiveness)
        if not grazed: # can't penetrate if you only grazed them
            while (pen-prot-(CMB_ROLL_PEN*pens) >= dice.roll(CMB_ROLL_PEN)):
                pens += 1   # number of penetrations ++
            armor = rog.around(arm * (0.5**pens))
        # end if
        
            #------------------#
            # calculate damage #
            #------------------#
        
        # physical damage
        
        if grazed:
            dmg = dmg*0.5
        resMult = 0.01*(100 - resphys)     # resistance multiplier
        rawDmg = dmg - armor
##        rmp = CMB_MDMGMIN + (CMB_MDMG*random.random()) # random multiplier -> variable damage
        
        # bonus damage (bonus to flesh, to armor, etc.)
##        dfndrArmored = False
##        if world.has_component(dfndr, cmp.EquipBody):
##            item=world.component_for_entity(dfndr, cmp.EquipBody).item
##            if item is not None:
##                if rog.on(item, ISHEAVYARMOR): # better way to do this?
##                    dfndrArmored = True
##        if dfndrArmored: # TODO: implement this and bonus to flesh!!!
##            if world.has_component(aweap, cmp.BonusDamageToArmor):
##                compo=world.component_for_entity(aweap, cmp.BonusDamageToArmor)
##                bonus = compo.dmg
##                rawDmg += bonus

        trueDmg = rog.around( max(0,rawDmg*resMult) ) #*rmp # apply modifiers
        
        # elemental damage
        if (world.has_component(aweap,cmp.ElementalDamageMelee)):
            elements=world.component_for_entity(aweap,cmp.ElementalDamageMelee).elements
        else:
            elements={}
        
        # extra critical damage: % based on Attack and Penetration
        # you need more atk and more pen than usual to score a crit.
        if (hitDie >= dice.roll(20) and pen-prot >= 24 ):
            # critical hit!
            if skillCompo:
                critMult = WEAPONCLASS_CRITDAMAGE[skillCompo.skill]
            else: # default crit damage
                critMult = WEAPONCLASS_CRITDAMAGE[0]
            # critical hits do a percentage of target's max HP in damage
            trueDmg += math.ceil(rog.getms(dfndr, 'hpmax')*critMult)
            crit=True
        # end if

            #--------------------#
            # body / gear damage #
            #--------------------#
            
        hitpp = min(BODY_DMG_PEN_BPS-1, pens)
        _boolDamageBodyPart = (hitpp!=0)
        # TODO: pick body part to hit randomly based on parameters
        if bptarget:
            bptarget = bptarget # TEMPORARY
        else:
            bptarget = rog.findbps(dfndr, cmp.BP_TorsoFront)[0]  # TEMPORARY
        # end if
        #
        # damage body part (inflict status)
        if _boolDamageBodyPart:
            # get damage type
            if world.has_component(aweap, cmp.DamageTypeMelee): # custom?
                compo=world.component_for_entity(aweap, cmp.DamageTypeMelee)
                dmgtype = compo.type
            else: # damage type based on skill of the weapon by default
                dmgtype = DMGTYPES[skillCompo.skill]
            # deal body damage
            rog.damagebp(bptarget, dmgtype)
            
            # organ damage (TODO) # how should this be done..?
            # criticals only? (criticals (temporarily?) disabled as of 2020-02-01)
            
        # end if
        #
        # damage gear
        gearitem = bptarget.slot.item
        if (gearitem and pens < GEAR_DMG_PEN_THRESHOLD):
            # the damage dealt to the gear is based on attacker's damage,
            # and the armor's AV; it has nothing to do with the stats of
            # the character who's wearing the gear.
            # Idea: could depend on armor-wearing skill of the wearer...
            geardmg = dmg - rog.getms(gearitem, 'arm')
            rog.damage(gearitem, geardmg)
        # end if
        
            #-------------------------------------#
            # deal damage, physical and elemental #
            #-------------------------------------#
            
        rog.damage(dfndr, trueDmg)
##        # sap some SP from defender;
##        rog.sap(dfndr, force*...)
        for element, elemDmg in elements.items():
            if grazed: elemDmg = elemDmg*0.5
            if element == ELEM_FIRE:
                rog.burn(dfndr, elemDmg)
                feelStrings.append("burns!")
            elif element == ELEM_BIO:
                rog.disease(dfndr, elemDmg)
            elif element == ELEM_ELEC:
                rog.electrify(dfndr, elemDmg)
                feelStrings.append("zaps!")                                                                                                                                                                                                                     # I love you Krishna
            elif element == ELEM_CHEM:
                rog.exposure(dfndr, elemDmg)
                feelStrings.append("stings!")
            elif element == ELEM_RADS:
                rog.irradiate(dfndr, elemDmg)
            elif element == ELEM_IRIT:
                rog.irritate(dfndr, elemDmg)
            elif element == ELEM_COLD:
                rog.cool(dfndr, elemDmg)
            elif element == ELEM_PAIN:
                # reduce pain if damage is low
                if trueDmg <= 0:
                    elemDmg = 1
                elif trueDmg <= 1:
                    elemDmg = elemDmg // 3
                elif trueDmg <= 2:
                    elemDmg = elemDmg // 2
                elif trueDmg <= 3:
                    elemDmg = elemDmg * 0.75
                rog.hurt(dfndr, elemDmg)
            elif element == ELEM_BLEED:
                if trueDmg <= 0: continue   # if phys dmg==0, no bleeding
                if pens == 0: continue   # if failed to penetrate, ""
                if pens == 1: # 1 penetration -> half bleed effect
                    elemDmg = elemDmg // 2
                rog.bleed(dfndr, elemDmg)
            elif element == ELEM_RUST:
                if pens == 0: continue   # if failed to penetrate, continue
                rog.rust(dfndr, elemDmg)
            elif element == ELEM_ROT:
                if pens == 0: continue   # if failed to penetrate, continue
                rog.rot(dfndr, elemDmg)
            elif element == ELEM_WET:
                rog.wet(dfndr, elemDmg)
        # end if
        
        killed = rog.on(dfndr,DEAD) #...did we kill it?
    # end if
    #
    # return info for the message log
    return (hit,pens,trueDmg,killed,crit,rol,ctrd,feelStrings,grazed,)


def fight(attkr,dfndr,adv=0,power=0):
    '''
    Combat function. Engage in combat:
    # Arguments:
        # attkr:    attacker (entity initiating combat)
        # dfndr:    defender (entity being attacked by attacker)
        # adv:      advantage attacker has over defender (bonus to-hit)
        # power:    amount of umph to use in the attack
        # grap:     grappling attack? (if False, do a striking attack)
        
        TODO: implement this!
        # power:    how much force putting in the attack?
            -1== subpar: use less than adequate force (bad leverage)
            0 == standard: use muscles in the attacking limb(s) / torso
            1 == heavy hit: use muscles in whole body (offensive)
                *leaves those body parts unable to provide defense
                 until your next turn
    '''
    
##    TODO: when you attack, look at your weapon entity to get:
        #-material of weapon
        #-flags of weapon
        
    # setting up
    world = rog.world()
    aactor = world.component_for_entity(attkr, cmp.Actor)
    apos = world.component_for_entity(attkr, cmp.Position)
    dpos = world.component_for_entity(dfndr, cmp.Position)
    aname=world.component_for_entity(attkr, cmp.Name)
    dname=world.component_for_entity(dfndr, cmp.Name)
        # weapons of the combatants (temporary ?)
    abody = world.component_for_entity(attkr, cmp.Body)
    dbody = world.component_for_entity(dfndr, cmp.Body)
    aarms = abody.parts.get(cmp.BPC_Arms, None)
    darms = dbody.parts.get(cmp.BPC_Arms, None)
    if aarms:
        aarm1 = aarms.arms[0]
        aarm2 = aarms.arms[1]
    else:
        aarm1=aarm2=None
    aweap1 = aarm1.hand.held.item if aarm1 else None
    aweap2 = aarm2.hand.held.item if aarm1 else None
    if darms:
        darm1 = darms.arms[0]
        darm2 = darms.arms[1]
    else:
        darm1=darm2=None
    dweap1 = darm1.hand.held.item if darm1 else None
    dweap2 = darm2.hand.held.item if darm1 else None
    #
    
    # ensure you have the proper amount of Stamina
    if aweap1:
        equipable = world.component_for_entity(aweap1, cmp.EquipableInHoldSlot)
        stamina_cost = equipable.stamina
    else:
        stamina_cost = STA_PUNCH
    if stamina_cost > rog.getms(attkr, "mp"):
        power=-1
    
    # counterability is affected by range/reach TODO!
##    dist=max(abs(apos.x - dpos.x), abs(apos.x - dpos.x))
##    if rog.withinreach(areach1, dist):
##        counterable = True
##    else:
##        counterable = False
    counterable = True
    
    # strike!
    hit,pens,trueDmg,killed,crit,rol,ctrd,feelStrings,grazed = _strike(
        attkr, dfndr, aweap1, dweap1,
        adv=adv, power=power, counterable=counterable,
        apos=apos,dpos=dpos
        )
    
    # AP cost
    aactor.ap -= rog.around( NRG_ATTACK * AVG_SPD / max(1, asp) )
    
    # stamina cost
    rog.sap(attkr, stamina_cost)
                 
    # metabolism
    rog.metabolism(attkr, CALCOST_HEAVYACTIVITY)
    
    # finishing up
    message = True # TEMPORARY!!!!
    a=aname.name; n=dname.name; at=aname.title; dt=dname.title;
    x='.'; ex="";
    dr="d{}".format(CMB_ROLL_ATK) #"d20"
        # make a message describing the fight
    if message:
        # TODO: show messages for grazed, crit, counter, feelStrings
        if hit==False:
            v="misses"
            if rog.is_pc(attkr):
                ex=" ({dr}:{ro})".format(dr=dr, ro=rol)
        else: # hit
            if rog.is_pc(attkr):
                ex=" ({dm}x{p})".format( #{dr}:{ro}|
                    dm=trueDmg, p=pens ) #dr=dr, ro=rol, 
            if killed:
                v="kills"
            else:
                if grazed:
                    v="grazes"
                else:
                    v = "*crits*" if crit else "hits"
        if ctrd: # TODO: more detailed counter message (i.e., " and ... counters (8x2)")
            m = " and {dt}{n} counters".format(dt=dt,n=n)
        rog.event_sight(
            dpos.x,dpos.y,
            "{at}{a} {v} {dt}{n}{ex}{m}{x}".format(
                a=a,v=v,n=n,at=at,dt=dt,ex=ex,x=x,m=m )
        )
        rog.event_sound(dpos.x,dpos.y, SND_FIGHT)
#

### grappling #
##def _grab(grplr, target): # should this just be incorporated into fight?
##    ''' entity grplr tries to grab (grappling) a target entity '''
##    
##    # setting up
##    world = rog.world()
##    aactor = world.component_for_entity(attkr, cmp.Actor)
##    apos = world.component_for_entity(attkr, cmp.Position)
##    dpos = world.component_for_entity(dfndr, cmp.Position)
##    aname=world.component_for_entity(attkr, cmp.Name)
##    dname=world.component_for_entity(dfndr, cmp.Name)
##    # weapons of the combatants
##    abody = Rogue.world.component_for_entity(grplr, cmp.Body)
##    dbody = Rogue.world.component_for_entity(target, cmp.Body)
##    aarms = abody.parts.get(cmp.BPC_Arms, None)
##    darms = dbody.parts.get(cmp.BPC_Arms, None)
##    if aarms: # temporary
##        aarm1 = aarms.arms[0]
##        aarm2 = aarms.arms[1]
##        aweap1 = aarm1.hand.held.item if aarm1 else None
##        aweap2 = aarm2.hand.held.item if aarm1 else None
##    if darms:
##        darm1 = darms.arms[0]
##        darm2 = darms.arms[1]
##        dweap1 = darm1.hand.held.item if darm1 else None
##        dweap2 = darm2.hand.held.item if darm1 else None
##    
##    # ensure you have the proper amount of Stamina
##    stamina_cost = 4 # TEMPORARY
##    if stamina_cost > rog.getms(attkr, "mp"):
##        power=-1
##    
##    # AP cost
##    aactor.ap -= rog.around( NRG_ATTACK * AVG_SPD / max(1, asp) )
##    
##    # stamina cost
##    rog.sap(attkr, stamina_cost)
##                 
##    # metabolism
##    rog.metabolism(attkr, CALCOST_HEAVYACTIVITY)
##    
##    # finishing up
##    message = True # TEMPORARY!!!!
##    a=aname.name; n=dname.name; at=aname.title; dt=dname.title;
##    x='.'; ex="";
##    dr="d{}".format(CMB_ROLL_ATK) #"d20"
##        # make a message describing the fight
##    if message:
##        v="grabs"
##        if ctrd:
##            m = "and {dt}{n} counters".format(dt=dt,n=n)
##        rog.event_sight(
##            dpos.x,dpos.y,
##            "{at}{a} {v} {dt}{n}{ex}{m}{x}".format(
##                a=a,v=v,n=n,at=at,dt=dt,ex=ex,x=x,m=m )
##        )
##        rog.event_sound(dpos.x,dpos.y, SND_FIGHT)
###
    



#######################################################################
            # Multi-turn actions / delayed actions #
#######################################################################


#


# eat
# initialize eating action
def eat(ent, item): # entity ent begins the eating action, eating food item
    world = rog.world()
    edible = world.component_for_entity(item, cmp.Edible)
    apCost = max(NRG_EAT_MIN, int(NRG_EAT*edible.satiation/1000) + edible.extraAP)
    proc.ActionQueue.queue( ent, apCost, _eat_finishFunc,
                            data=item, cancelFunc=_eat_cancelFunc )
# end def
def _eat_finishFunc(ent, item): # helper func for eat action
    edible = world.component_for_entity(item, cmp.Edible)
    foodmeter = world.component_for_entity(item, cmp.Meters)
    entmeter = world.component_for_entity(ent, cmp.Meters)
    
    # begin digesting the nutrients from the food
    rog.feed(ent, edible.satiation, edible.hydration)
    
    # stamina cost
    rog.sap(STA_EAT * qa.elapsed, exhaustOnZero=False)
    
    # heat up or cool down based on food's temperature
    # TODO: fix bug: the temperature of the food at the time you finish eating it is what affects your temperature, rather than the temperature of the food during the act of eating it...
##    tempdiff = (foodmeter.temp - entmeter.temp)
##    tempg = (tempdiff * rog.getms(item,'mass') / rog.getms(ent,'mass'))
##    if tempg > 0:
##        rog.burn(ent, tempg)
##    else:
##        rog.cool(ent, -tempg)
    
    # function -- what happens when entity ent eats the item?
    if edible.func: # pass in 1 to indicate we ate the entire thing
        edible.func(ent, 1) #waste products to be handled by the function

    # taste TODO
##        edible.taste

    # finally, delete the food item
    rog.kill(item)
# end def
def _eat_cancelFunc(ent, qa): # helper func for eat action
    item = qa.data
    name = world.component_for_entity(item, cmp.Name)
    edible = world.component_for_entity(item, cmp.Edible)
    form = world.component_for_entity(item, cmp.Form)
    draw = world.component_for_entity(item, cmp.Draw)
    meters = world.component_for_entity(item, cmp.Meters)
    pos = world.component_for_entity(ent, cmp.Position)
    mass = rog.getms(item,'mass')
    amountEaten = 1 - qa.ap // qa.apMax
    newMass = int(mass * amountEaten) # food mass remaining
    massdiff = mass - newMass # food mass eaten
    
    # satiation / hydration is only partial depending on how much you ate.
    cald = int(edible.satiation * amountEaten) # TODO: lose some calories due to inefficiency in eating (only applies to messy eaters (those without the TABLEMANNERS flag(?)))
    hydd = int(edible.hydration * amountEaten)
    # fill 'er up
    rog.feed(ent, cald, hydd)

    # stamina cost
    rog.sap(STA_EAT * qa.elapsed, exhaustOnZero=False)
    
    # heat up or cool down based on food's temperature
    # TODO: fix bug: the temperature of the food at the time you finish eating it is what affects your temperature, rather than the temperature of the food during the act of eating it...
##    tempdiff = (foodmeter.temp - entmeter.temp)
##    tempg = (tempdiff * massdiff / rog.getms(ent,'mass')) # multiply heat by how much of the food you ate (massdiff)
##    if tempg > 0:
##        rog.burn(ent, tempg)
##    else:
##        rog.cool(ent, -tempg)
    
    
    # function -- some foods call functions when you eat them
    if edible.func: # pass in the entity that ate it, and the ratio of ...
        edible.func(ent, amountEaten)#...how much it ate (same as finishFunc)
    
    # taste TODO
##        edible.taste
    
    # create the new partially eaten food item
    newitem = rog.world().create_entity(
        rog.dupCmpMeters(meters), # duplicate old meters component
        cmp.Edible(
            edible.func,
            edible.satiation - cald,
            edible.hydration - hydd,
            edible.taste,
            edible.extraAP
            ),
        cmp.Name(name.name, title=name.title),
        cmp.Form(mat=form.material, val=0, length=form.length, phase=form.phase),
        cmp.Draw(draw.char, draw.fgcol, draw.bgcol),
        cmp.Position(pos.x, pos.y),
        cmp.Stats(hp=1, mass=newMass),
        cmp.Prefixes("partially eaten"), # TODO: make this affect the name display in the UI -> make a global function that gets the full name of an entity including all its components' alterations to the name (stored name != displayed name).
        # or should this be just a PartiallyEaten() component?
        )
    
    # finally, delete the food item
    rog.kill(item)
# end def

def craft(ent, recipe):
    world=rog.world()
    data = recipes.RECIPES.get(recipe, {})
    if not data:
        entname=world.component_for_entity(ent, cmp.Name)
        entpos=world.component_for_entity(ent, cmp.Position)
        print("entity named '{}' at {},{} tried to craft recipe '{}', which does not exist.".format(
            entname, entpos.x, entpos.y, recipe))
        return False
    
    # ensure entity has appropriate crafting skill levels
    apMult = 1
    for packd in data['skills']:
        skill,lv = packd
        if lv > rog.getskill(ent, skill):
            return False
        apMult = max(0.1, 1 - (skillLv - lv)*0.005)
    
    # begin crafting job
    apCost = max(1, int( data['construct'] * apMult) )
    proc.ActionQueue.queue( ent, apCost, _craft_finishFunc,
                            data=data, cancelFunc=_craft_cancelFunc )
# end def





















# other actions #

#TODO: UPDATE THIS FUNCTION
def explosion(bomb):
    rog.msg("{t}{n} explodes! <UNIMPLEMENTED>".format(t=bomb.title, n=bomb.name))
    '''
    con=libtcod.console_new(ROOMW, ROOMH)
    fov=rog.fov_init()
    libtcod.map_compute_fov(
        fov, bomb.x,bomb.y, bomb.r,
        light_walls = True, algo=libtcod.FOV_RESTRICTIVE)
    for x in range(bomb.r*2 + 1):
        for y in range(bomb.r*2 + 1):
            xx=x + bomb.x - bomb.r
            yy=y + bomb.y - bomb.r
            if not libtcod.map_is_in_fov(fov, xx,yy):
                continue
            if not rog.is_in_grid(xx,yy): continue
            dist=maths.dist(bomb.x,bomb.y, xx,yy)
            if dist > bomb.r: continue
            
            thing=rog.thingat(xx, yy)
            if thing:
                if rog.on(thing,DEAD): continue
                
                if thing.isCreature:
                    decay=bomb.dmg/bomb.r
                    dmg= bomb.dmg - round(dist*decay) - thing.stats.get('arm')
                    rog.damage(thing, dmg)
                    if dmg==0: hitName="not damaged"
                    elif rog.on(thing,DEAD): hitName="killed"
                    else: hitName="hit"
                    rog.msg("{t}{n} is {h} by the blast.".format(
                        t=thing.title,n=thing.name,h=hitName) )
                else:
                    # explode any bombs caught in the blast
                    if (thing is not bomb
                            and hasattr(thing,'explode')
                            and dist <= bomb.r/2 ):
                        thing.timer=0
                        '''

#use
#"use" an item, whatever that means for the specific item
##def use_pc(obj, item):
##    item.useFunctionPlayer(obj)


# player only actions #

##def bomb_pc(pc): # drop a lit bomb
##    rog.alert("Place bomb where?{d}".format(d=dirStr))
##    args=rog.get_direction()
##    if not args: return
##    dx,dy,dz=args
##    xx,yy=pc.x + dx, pc.y + dy
##    
##    if not rog.thingat(xx,yy):
##        weapons.Bomb(xx,yy, 8)
##        rog.drain(pc, 'nrg', NRG_BOMB)
##        rog.msg("{t}{n} placed a bomb.".format(t=pc.title,n=pc.name))
##    else:
##        rog.alert("You cannot put that in an occupied space.")

''' SCRIPT TO SHOW BOMB DAMAGE AND DECAY

            decay=bomb.dmg/bomb.r
            dmg= bomb.dmg - round(dist*decay)
            libtcod.console_put_char_ex(con, xx, yy, chr(dmg+48), WHITE,BLACK)
            
    libtcod.console_blit(con,rog.view_x(),rog.view_y(),rog.view_w(),rog.view_h(),
                         0,rog.view_port_x(),rog.view_port_y())
    libtcod.console_flush()
    r=rog.Input(0,0,mode="wait")
    '''


'''if (not killed and not hpmax_before == dfndr.stats.hpmax):
            x=", injuring {pronoun}".format(pronoun=pronoun)
'''

'''
#TEST
if (obj.x==x and obj.y==y):
    obj.stats.sight +=1
    if obj.stats.sight >= 9:
        obj.stats.sight=9
else: obj.stats.sight = 5
#'''
