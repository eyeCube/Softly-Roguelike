'''
    rogue.py

    Jacob Wharton
'''

import esper

import components as cmp
import tilemap
import player


##
##class Ref():        # stores global references to objects
##    ctrl        = None  # global controller
##    con         = None  # consoles
##    data        = None
##    Map         = None
##    clock       = None
##    update      = None
##    settings    = None
##    view        = None
##    log         = None  # messages
##    pc          = None
##    environ     = None
##    manager     = None  # current active game state manager
##    savedGame   = None
##    et_managers = {}    # per turn managers that tick at end of each turn
##    bt_managers = {}    # per turn managers that tick at beginning of each turn
##    c_managers  = {}    # const managers, ran manually
##


class Rogue:
    @classmethod
    def create_world(cls):  cls.world = esper.World()
    @classmethod
    def create_map(cls):    cls.Map = tilemap.Tilemap()
    @classmethod
    def create_player(cls): cls.pc = player.chargen()

def world():    return Rogue.world
def pc():       return Rogue.pc




#-------------#
# "Fun"ctions #
#-------------#

# tilemap
def thingat(x,y):       return Rogue.Map.thingat(x,y) #Thing object
def thingsat(x,y):      return Rogue.Map.thingsat(x,y) #list
def inanat(x,y):        return Rogue.Map.inanat(x,y) #inanimate Thing at
def monat (x,y):        return Rogue.Map.monat(x,y) #monster at
def solidat(x,y):       return Rogue.Map.solidat(x,y) #solid Thing at
def wallat(x,y):        return (not Rogue.Map.get_nrg_cost_enter(x,y) ) #tile wall
def fluidsat(x,y):      return Rogue.et_managers['fluids'].fluidsat(x,y) #list
def lightsat(x,y):      return Rogue.Map.lightsat(x,y) #list
def fireat(x,y):        return Rogue.et_managers['fire'].fireat(x,y)

def cost_enter(x,y):    return Rogue.Map.get_nrg_cost_enter(x,y)
def cost_leave(x,y):    return Rogue.Map.get_nrg_cost_leave(x,y)
def cost_move(xf,yf,xt,yt,data):
    return Rogue.Map.path_get_cost_movement(xf,yf,xt,yt,data)

def is_in_grid_x(x):    return (x>=0 and x<ROOMW)
def is_in_grid_y(y):    return (y>=0 and y<ROOMH)
def is_in_grid(x,y):    return (x>=0 and x<ROOMW and y>=0 and y<ROOMH)
def in_range(x1,y1,x2,y2,Range):    return (maths.dist(x1,y1, x2,y2) <= Range + .34)

# view
def getx(x):        return x + view_port_x() - view_x()
def gety(y):        return y + view_port_y() - view_y()
def mapx(x):        return x - view_port_x() + view_x()
def mapy(y):        return y - view_port_y() + view_y()

# terraforming
def dig(x,y):
    #dig a hole in the floor if no solids here
    #else dig the wall out
    #use rogue's tile_change func so we update all FOVmaps
    tile_change(x,y,FLOOR)
def singe(x,y): #burn tile
    if Rogue.Map.get_char(x,y) == FUNGUS:
        tile_change(x,y,FLOOR)

# entity functions
def on(obj, flag):
    return flag in Rogue.world.component_for_entity(obj, set)
def make(obj, flag):
    Rogue.world.component_for_entity(obj, set).add(flag)
def makenot(obj, flag):
    Rogue.world.component_for_entity(obj, set).remove(flag)
def get(objID, component): #return an entity's component
    return Rogue.world.component_for_entity(objID, component)
def has(objID, component): #return whether entity has component
    return Rogue.world.has_component(objID, component)
def match(component):
    return Rogue.world.get_component(component)
def matchx(*components):
    return Rogue.world.get_components(components)
    return True
def copyflags(toObj,fromObj,copyStatusFlags=True): #use this to set an object's flags to that of another object.
    for flag in Rogue.world.component_for_entity(fromObj, set):
        if (copyStatusFlags or not flag in STATUSFLAGS):
            make(toObj, flag)
##def has_equip(obj,item):
##    return item in Rogue.world.component_for_entity(obj, )
def give(obj,item):
    if on(item,FIRE):
        burn(obj, FIRE_BURN)
        cooldown(item)
    get(obj, cmp.Inventory).data.append(item)
def take(obj,item):
    get(obj, cmp.Inventory).data.remove(item)
def mutate(obj):
    #do mutation
    get(obj, cmp.Mutable)
    event_sight(obj.x,obj.y,"{t}{n} mutated!".format(t=obj.title,n=obj.name))
def has_sight(obj):
    if (obj.stats.get('sight') and not on(obj,BLIND)): return True
    return False
def port(obj,x,y): # move thing to absolute location, update grid and FOV
    grid_remove(obj)
    pos = get(obj, cmp.Position)
    pos.x=x; pos.y=y;
    grid_insert(obj)
    update_fov(obj)
def drop(obj,item,dx=0,dy=0):   #remove item from obj's inventory, place it
    take(obj,item)              #on ground nearby obj.
    itempos=get(item, cmp.Position)
    objpos=get(obj, cmp.Position)
    itempos.x=objpos.x + dx
    itempos.y=objpos.y + dy
    register_inanimate(item)
def givehp(obj,val=9999):   get(obj, cmp.Health).hp+=val; caphp(obj)
def givemp(obj,val=9999):   get(obj, cmp.Health).mp+=val; capmp(obj)
def caphp (obj):
    health = get(obj, cmp.Health)
    health.hp = min(health.hp, health.hpmax)
def capmp (obj):
    health = get(obj, cmp.Health)
    health.mp = min(health.mp, health.mpmax)
#train (improve) skill
def train (obj,skill):
    skills = get(obj, cmp.Skills)
    skills.update({skill : max(SKILLMAX, skills.get(skill,0)+1) })
#damage hp
def hurt(obj, dmg: int):
##    assert isinstance(dmg, int)
    if dmg < 0: return
    health = get(obj, cmp.Health)
    health.hp -= dmg
    if health.hp <= 0:
        kill(obj)
#damage mp
def sap(obj, dmg):
    dmg = round(dmg)
    health = get(obj, cmp.Health)
    health.mp -= dmg
    if health.mp <= 0:
        zombify(obj)
#deal fire damage
def burn(obj, dmg, maxTemp=FIRE_MAXTEMP):
    if on(obj, DEAD): return False
    if on(obj, WET):
        clear_status(obj, WET)
        #steam=create_fluid(obj.x, obj.y, "steam")
        return False
    stuff.burn(obj, dmg, maxTemp)
    return True
def cooldown(obj, temp=999):
    if on(obj, DEAD): return False
    stuff.cooldown(obj, temp)
#deal bio damage
def disease(obj, dmg):
    if on(obj, DEAD): return False
    stuff.disease(obj, dmg)      #sick damage
def exposure(obj, dmg):
    if on(obj, DEAD): return False
    stuff.exposure(obj, dmg)    #chem damage
def corrode(obj, dmg):
    if on(obj, DEAD): return False
    stuff.corrode(obj, dmg)      #acid damage
def irradiate(obj, dmg):
    if on(obj, DEAD): return False
    stuff.irradiate(obj, dmg)  #rad damage
def intoxicate(obj, dmg):
    if on(obj, DEAD): return False
    stuff.intoxicate(obj, dmg)#drunk damage
def cough(obj, dmg): #coughing fit status
    if on(obj, DEAD): return False
    stuff.cough(obj, dmg)
def vomit(obj, dmg): #vomiting fit status
    if on(obj, DEAD): return False
    stuff.vomit(obj, dmg)
#deal electric damage
def electrify(obj, dmg):
    if on(obj, DEAD): return False
    stuff.electrify(obj, dmg)
#paralyze
def paralyze(obj, turns):
    if on(obj, DEAD): return False
    stuff.paralyze(obj, turns)
#mutate
def mutate(obj):
    if on(obj, DEAD): return False
    stuff.mutate(obj)
def kill(obj): #remove a thing from the world
    if on(obj, DEAD): return
    world = Rogue.world
    if world.has_component(obj, cmp.DeathFunction): # call destroy function
        world.component_for_entity(obj, cmp.DeathFunction)()
    make(obj, DEAD)
    clear_status_all(obj)
    #drop inventory
    if has(obj, cmp.Inventory):
        for tt in get(obj, cmp.Inventory):
            drop(obj, tt)
    #creatures
    isCreature = has(obj, cmp.Creature)
    if isCreature:
        #create a corpse
        if dice.roll(100) < monsters.corpse_recurrence_percent[obj.type]:
            create_corpse(obj)
    #inanimate things
    else:
        #burn to ashes
        if on(obj, FIRE):
            mat = get(obj, cmp.Material).flag
            if (mat==MAT_FLESH
                or mat==MAT_WOOD
                or mat==MAT_FUNGUS
                or mat==MAT_VEGGIE
                or mat==MAT_LEATHER
                ):
                create_ashes(obj)
    #remove dead thing
    if on(obj, ONGRID):
        if isCreature:
            release_creature(obj)
        else:
            release_inanimate(obj)
def explosion(name, x, y, radius):
    event_sight(x, y, "{n} explodes!".format(n=name))







#----------------#
#     Things     #
#----------------#

def create_stuff(ID, x,y):
    tt = stuff.create(x,y, ID)
    register_inanimate(tt)
    return tt
def release_thing(ent):
    grid_remove(ent)
    Rogue.world.delete_entity(ent)
def register_inanimate(ent):
    name = get(ent, cmp.Name).name
    pos = get(ent, cmp.Position)
    print("registering {} at {},{}".format(name, pos.x, pos.y))
    grid_insert(ent)
def release_inanimate(obj):
    grid_remove(obj)


#---------------------#
#  creature/monsters  #
#---------------------#

#register and release functions do not perform checks to ensure proper calling
#must ensure manually that you insert an object of type Thing
#if a creature already exists in the tile of obj's position,
#   then this function will produce errors.
#likewise make sure you do not try to release an entity
#   that was not first registered.
#Always call proper release that corresponds with the register function
#   in order to remove an object from the game.
def register_creature(ent):
    grid_insert(ent)
def release_creature(ent):
    release_thing(ent)
    remove_listener_sights(ent)
    remove_listener_sounds(ent)





##def makeEquip(obj, component):
##    make(obj, CANEQUIP)
##    Rogue.world.add_component(obj, component)
###gain (improve) stat
##def gain (obj,stat,val=1,Max=999):
##    stats=obj.stats
##    setattr(stats, stat, min(Max, getattr(stats, stat) + val))
###drain (damage) stat
##def drain (obj,stat,val=1):
##    old = getattr(obj.stats,stat)
##    setattr(obj.stats,stat, old-val )
##    if (stat=='hpmax'): caphp(obj)
##    if (stat=='mpmax'): capmp(obj)

##def is_creature(obj):   return Rogue.world.component_for_entity(obj, Creature)
##def is_solid(obj):      return ISSOLID in Rogue.world.component_for_entity(obj, set)
##def on  (obj,flag):     return (flag in obj.flags)
##def make(obj,flag):     obj.flags.add(flag)
##def makenot(obj,flag):  obj.flags.remove(flag)
###set stat
##def setStat (obj,stat,val):
##    setattr(get(obj, cmp., stat, val)

'''
def getComp(objID, component):
    return Rogue.world.get_component(objID, component)

def hasComp(objID, component):
    return Rogue.world.has_component(objID, component)
    
def create_thing(name, x, y, char, color, bgcol):
    ent = Rogue.world.create_entity(set(), #flags set
        cmp.Name(name), cmp.Position(x,y),
        cmp.Draw(char, color, bgcol),
        cmp.BasicStats(),
        )
    return ent

def create_creature(name, x, y):
    ent = Rogue.world.create_entity(
        cmp.Draw(),
        cmp.Name(name), cmp.Position(x,y), cmp.TakesTurns(100),
        cmp.BasicStats(), cmp.CombatStats(), cmp.Creature(),
        cmp.Purse(), cmp.Inventory(), cmp.Skills(), cmp.Form(),
        cmp.StatMods(), cmp.StatusEffects(), cmp.Mutable(), 
        cmp.EquipBody(), cmp.EquipAmmo(), cmp.EquipBack(),
        cmp.EquipMainhand(), cmp.EquipOffhand(), cmp.EquipHead(),
        )
    return ent
'''






'''
TEST

Rogue.create_world()
i=Rogue.world.create_entity(cmp.Position(1,1))
print(get(i, cmp.Position))
if has(i, cmp.Name):
    print(get(i, cmp.Name))
    '''

