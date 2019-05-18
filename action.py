'''
    action.py
    Part of Softly Into the Night, a roguelike by Jacob Wharton.
    Copyright 2019.
'''

# wrapper for things that creatures can do in the game
#   - actions cost energy
# PC actions are for the player object to give feedback
#   - (if you try to eat something inedible, it should say so, etc.)
#

from const import *
import rogue as rog
import dice
import maths
import items




occupations={}
dirStr=" <hjklyubn.>"


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
        if rog.on(choice,FIRE):
            answer=""
            while True:
                answer=rog.prompt(0,0,rog.window_w(),1,maxw=1,
                    q="That thing is on fire! Are you sure? y/n",
                    mode='wait',border=None)
                answer=answer.lower()
                if answer == "y" or answer == " " or answer == K_ENTER:
                    rog.alert("You burn your hands!")
                    rog.burn(pc, FIRE_BURN)
                    rog.hurt(pc, FIRE_HURT)
                    break
                elif answer == "n" or answer == K_ESCAPE:
                    return
        # put in inventory
        pocketThing(pc, choice)
##    elif choice == "all":
##        for tt in things:
##            pocketThing(pc, tt)
    else:
        rog.alert("There is nothing there to pick up.")


def inventory_pc(pc,pcInv):
    world=Rogue.world()
##    assert world.has_component(pc, cmp.Inventory), "PC missing inventory"
    pcInv = world.component_for_entity(pc, cmp.Inventory)
    pcn = world.component_for_entity(pc, cmp.Name)
    x=0
    y=rog.view_port_y()
#   items menu
    item=rog.menu("{}{}'s Inventory".format(
        pcn.title,pcn.name), x,y, pcInv.items)
    
#   viewing an item
    if not item == -1:
        itemn = world.component_for_entity(item, cmp.Name)
##        itemn = world.component_for_entity(item, cmp.Name)
        keysItems={}
        
    #   get available actions for this item...
        if world.has_component(item, cmp.Edible):
            keysItems.update({"E":"Eat"})
        if world.has_component(item, cmp.Quaffable):
            keysItems.update({"q":"quaff"})
        if world.has_component(item, cmp.Equipable):
            keysItems.update({"e":"equip"})
            # throwables - subset of equipables
            if world.component_for_entity(item, cmp.Equipable).equipType == EQ_MAINHAND:
                keysItems.update({"t":"throw"})
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
        elif opt == "throw":    rmg=True; throw_pc(pc, item)
        elif opt == "eat":      rmg=True; eat_pc(pc, item)
        elif opt == "quaff":    rmg=True; quaff_pc(pc, item)
        elif opt == "use":      rmg=True; use_pc(pc, item)
        elif opt == "examine":  rmg=True; examine_pc(pc, item)
        
        if rmg: rog.drain(pc, 'nrg', NRG_RUMMAGE)
#

def drop_pc(pc,item):
    rog.alert("Place {i} where?{d}".format(d=dirStr,i=item.name))
    args=rog.get_direction()
    if not args: return
    dx,dy,dz=args
    
    if not drop(pc, item):
        rog.alert("You can't put that there!")

def open_pc(pc):
    rog.alert("Open what?{d}".format(d=dirStr))
    args=rog.get_direction()
    if not args: return
    dx,dy,dz=args
    xto=pc.x+dx
    yto=pc.y+dy
    
    if not openClose(pc, xto, yto):
        rog.alert("It won't open.")

def sprint_pc(pc):
    #if sprint cooldown elapsed
    if not rog.on(pc, TIRED):
        sprint(pc)
    else:
        rog.alert("You're too tired to sprint.")

def throw_pc(pc):
    pass
    

def equip_pc(pc,item):
    pass
    #fornow, just wield it THIS SCRIPT NEEDS SERIOUS WORK*****>>>>...
    '''
    rog.drain(pc, 'nrg', NRG_RUMMAGE + NRG_WIELD)
    if rog.has_equip(pc, item):
        if rog.deequip(pc, item.equipType):
            rog.msg("{t}{n} wields {i}.".format(t=pc.title,n=pc.name,i=item.name))
        else: rog.alert("You are already wielding something in that hand.")
    else: rog.wield(pc,item)'''

def examine_pc(pc, item):
    rog.drain(pc, 'nrg', NRG_EXAMINE)
    rog.dbox(0,0,40,30, thing.DESCRIPTIONS[item.name])

def rest_pc(pc):
    turns=rog.prompt(0,0,rog.window_w(),1,maxw=3,
                     q="How long do you want to rest? Enter number of turns:",
                     mode='wait',border=None)
    for t in range(turns):
        rog.queue_action(pc, wait)

def towel_pc(pc, item):
    options={}
    options.update({"W" : "wrap around"})
    options.update({"l" : "lie"})
    options.update({"s" : "sail"})
    options.update({"w" : "wield"})
    options.update({"h" : "wear on head"})
    options.update({"x" : "wave"})
    options.update({"d" : "dry"})
    choice=rog.menu("use towel",0,0,options,autoItemize=False)
    if choice == "wear on head":
        pass
    elif choice == "wrap around":
        dirTo=rog.get_direction()
        if not args: return
        dx,dy,dz=args
        xto = pc.x + dx; yto = pc.y + dy;

        if (dx==0 and dy==0 and dz==0):
            pass #wrap around self
        
    elif choice == "wield":
        if rog.on(item, WET):
            pass #equip it
        else:
            rog.alert("You can't wield a towel that isn't wet!")
            
    elif choice == "dry":
        #itSeemsCleanEnough=...
        if ( itSeemsCleanEnough and not rog.on(item, WET) ):
            pass #dry self
        else:
            if not itSeemsCleanEnough:
                rog.alert("It doesn't seem clean enough.")
            elif rog.on(item, WET):
                rog.alert("It's too wet.")
                

################################################

#wait
#just stand still and do nothing
#recover your Action Points to their maximum
def wait(ent):
    rog.world().component_for_entity(ent, cmp.Actor).ap = 0

def cough(ent):
    world = rog.world()
    pos = world.component_for_entity(ent, cmp.Position)
    entn = world.component_for_entity(ent, cmp.Name)
    wait(ent)
    rog.event_sound(pos.x,pos.y, SND_COUGH)
    rog.event_sight(pos.x,pos.y, "{t}{n} hacks up a lung.".format(
        t=entn.title,n=entn.name))

#use
#"use" an item, whatever that means for the specific item
def use(obj, item):
    pass


#pocket thing
#a thing puts a thing in its inventory
def pocketThing(ent, item):
##    if not item: return False
    world = rog.world()
    rog.drain(ent, 'nrg', NRG_POCKET)
    rog.give(ent, item)
    rog.release_inanimate(item)
    entn = world.component_for_entity(ent, cmp.Name)
    itemn = world.component_for_entity(item, cmp.Name)
    rog.msg("{t}{n} packs {ti}{ni}.".format(
        t=entn.title,n=entn.name,ti=itemn.title,ni=itemn.name))
##    return True

def drop(ent, item):
    world = rog.world()
    pos = world.component_for_entity(ent, cmp.Position)
    dx=0; dy=0; # TODO: code AI to find a place to drop item
    if not rog.wallat(pos.x+dx,pos.y+dy):
        rog.drain(ent, 'nrg', NRG_RUMMAGE)
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
    rog.drain(ent, 'nrg', quaffable.timeToConsume)
    rog.givemp(ent, quaffable.hydration)

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


#move
#returns True if move was successful, else False
#do not drain Action Points unless move was successful
def move(ent,dx,dy):  # locomotion
    world = rog.world()
    pos = world.component_for_entity(ent, cmp.Position)
    cstats = world.component_for_entity(ent, cmp.CombatStats)
    actor = world.component_for_entity(ent, cmp.Actor)
    xto=pos.x+dx
    yto=pos.y+dy
    terrain_cost=rog.cost_move(pos.x,pos.y,xto,yto, None)
    if terrain_cost == 0:  return False     # 0 means we can't move there
    mult = 1.41 if (dx + dy) % 2==0 else 1  # diagonal extra cost
    modf=NRG_MOVE
    nrg_cost=round(modf*mult*terrain_cost*AVG_SPD/max(1, cstats.msp))
    actor.ap -= nrg_cost
    rog.port(ent, xto, yto)
    return True

def openClose(ent, xto, yto):
    world = rog.world()
    actor = world.component_for_entity(ent, cmp.Actor)
    entn = world.component_for_entity(ent, cmp.Name)
    #open containers
    #close containers
    #open doors
    if rog.tile_get(xto,yto) == DOORCLOSED:
        actor.ap -= NRG_OPEN
        rog.tile_change(xto,yto, DOOROPEN)
        rog.msg("{t}{n} opened a door.".format(t=entn.title,n=entn.name))
        return True
    #close doors
    if rog.tile_get(xto,yto) == DOOROPEN:
        actor.ap -= NRG_OPEN
        rog.tile_change(xto,yto, DOORCLOSED)
        rog.msg("{t}{n} closed a door.".format(t=entn.title,n=entn.name))
        return True
    return False

def sprint(ent):
    entn = rog.world().component_for_entity(ent, cmp.Name)
    #if sprint cooldown elapsed
    rog.set_status(ent, SPRINT)
    rog.msg("{n} begins sprinting.".format(n=entn.name))


#
# fight
#
# Arguments:
# attkr,dfndr:  attacker, defender
# adv:          advantage attacker has over defender
# dtyp:         damage type:            
#                 - 'die' is a die roll,
#                 - 'crit' does max * extra damage

def fight(attkr,dfndr,adv=0):
##    TODO: when you attack, look at your weapon entity to get:
        #-material of weapon
        #-element of weapon
        #-flags of weapon
    world = rog.world()
    cstats = world.component_for_entity(attkr, cmp.CombatStats)
    dpos = world.component_for_entity(dfndr, cmp.Position)
    element = ELEM_PHYS #****TEMPORARY!!!! has_component...
    nrg_cost = round( NRG_ATTACK*AVG_SPD/max(1, cstats.asp) )
    cstats.ap -= nrg_cost

    die=COMBATROLL
    acc=cstats.atk
    dv=cstats.dfn
    hit = False
    rol = dice.roll(die + acc + adv - dv) - dice.roll(die)
    if (rol >= 0): # HIT!!!
        hit = True
        
        #type of damage dealt depends on the element attacker is using
        if element == ELEM_PHYS:
            #high attack values can pierce armor
##            if rol > ATK_BONUS_DMG_CUTOFF:
##                pierce = int( (rol - ATK_BONUS_DMG_CUTOFF)/2 )
##            else:
##                pierce = 0
            armor = dfndr.stats.get('arm') #max(0, dfndr.stats.get('arm') - pierce)
            dmg = max(0, attkr.stats.get('dmg') - armor)
            rog.hurt(dfndr, dmg)
        elif element == ELEM_FIRE:
            rog.burn(dfndr, dmg)
        elif element == ELEM_BIO:
            rog.disease(dfndr, dmg)
        elif element == ELEM_ELEC:
            rog.electrify(dfndr, dmg)
        elif element == ELEM_CHEM:
            rog.exposure(dfndr, dmg)
        elif element == ELEM_RADS:
            rog.irradiate(dfndr, dmg)
        
        killed = rog.on(dfndr,DEAD) #...did we kill it?
    #
    
    message = True
    a=attkr.name; n=dfndr.name; t1=attkr.title; t2=dfndr.title; x='.';
    
    # make a message describing the fight
    if message:
        if hit==False: v="misses"
        elif dmg==0: v="cannot penetrate"; x="'s armor!"
        elif killed: v="defeats"
        else: v="hits"
        rog.event_sight(
            dfndr.x,dfndr.y,
            "{t1}{a} {v} {t2}{n}{x}".format(a=a,v=v,n=n,t1=t1,t2=t2,x=x)
        )
        rog.event_sound(dpos.x,dpos.y, SND_FIGHT)
    
# end def


# not necessarily creature actions #
''' TODO: UPDATE THIS FUNCTION
def explosion(bomb):
    con=libtcod.console_new(ROOMW, ROOMH)
    rog.msg("{t}{n} explodes!".format(t=bomb.title, n=bomb.name))
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
                    rog.hurt(thing, dmg)
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
