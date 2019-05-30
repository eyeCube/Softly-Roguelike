

#----------------------#
#        Events        #
#----------------------#

def event_sight(x,y,text):
    if not text: return
    Ref.c_managers['events'].add_sight(x,y,text)
def event_sound(x,y,data):
    if (not data): return
    volume,text1,text2=data
    Ref.c_managers['events'].add_sound(x,y,text1,text2,volume)
def listen_sights(obj):     return  Ref.c_managers['events'].get_sights(obj)
def listen_sounds(obj):     return  Ref.c_managers['events'].get_sounds(obj)
def add_listener_sights(obj):       Ref.c_managers['events'].add_listener_sights(obj)
def add_listener_sounds(obj):       Ref.c_managers['events'].add_listener_sounds(obj)
def remove_listener_sights(obj):    Ref.c_managers['events'].remove_listener_sights(obj)
def remove_listener_sounds(obj):    Ref.c_managers['events'].remove_listener_sounds(obj)
def clear_listen_events_sights(obj):Ref.c_managers['events'].clear_sights(obj)
def clear_listen_events_sounds(obj):Ref.c_managers['events'].clear_sounds(obj)

def pc_listen_sights():
    pc=Rogue.pc
    lis=listen_sights(pc)
    if lis:
        for ev in lis:
            Ref.c_managers['sights'].add(ev)
        manager_sights_run()
def pc_listen_sounds():
    pc=Rogue.pc
    lis=listen_sounds(pc)
    if lis:
        for ev in lis:
            Ref.c_managers['sounds'].add(ev)
        manager_sounds_run()
def clear_listeners():      Ref.c_managers['events'].clear()


''' TODO: implement effects manager
#------------------------#
# Stats Functions + vars #
#------------------------#

def effect_add(obj,mod):        # Stat mod create
    effID=thing.effect_add(obj,mod)
    return effID
def effect_remove(obj,modID):   # Stat mod delete
    thing.effect_remove(obj,modID)
    '''


''' SHOULD WE USE LISTS OR JUST QUERIES?
#---------------#
#     Lists     #
#---------------#

class Lists():
    creatures   =[]     # living things
    inanimates  =[]     # nonliving
    lights      =[]
    fluids      =[]
    
    @classmethod
    def things(cls):
        lis1=set(cls.creatures)
        lis2=set(cls.inanimates)
        return lis1.union(lis2)

# lists functions #

def list_creatures():           return Lists.creatures
def list_inanimates():          return Lists.inanimates
def list_things():              return Lists.things()
def list_lights():              return Lists.lights
def list_fluids():              return Lists.fluids
def list_add_creature(obj):     Lists.creatures.append(obj)
def list_remove_creature(obj):  Lists.creatures.remove(obj)
def list_add_inanimate(obj):    Lists.inanimates.append(obj)
def list_remove_inanimate(obj): Lists.inanimates.remove(obj)
def list_add_light(obj):        Lists.lights.append(obj)
def list_remove_light(obj):     Lists.lights.remove(obj)
def list_add_fluid(obj):        Lists.fluids.append(obj)
def list_remove_fluid(obj):     Lists.fluids.remove(obj)
'''



#----------------#
#       FOV      #
#----------------#

#THIS CODE NEEDS TO BE UPDATED. ONLY MAKE AS MANY FOVMAPS AS NEEDED.
def fov_init():  # normal type FOV map init
    fovMap=libtcod.map_new(ROOMW,ROOMH)
    libtcod.map_copy(Rogue.map.fov_map,fovMap)  # get properties from Map
    return fovMap
#@debug.printr
def fov_compute(ent):
    pos = world().component_for_entity(ent, cmp.Position)
    seer = world().component_for_entity(ent, cmp.SenseSight)
    libtcod.map_compute_fov(
        obj.fov_map, pos.x, pos.y, seer.sight,
        light_walls=True, algo=libtcod.FOV_RESTRICTIVE
        )
def update_fovmap_property(fovmap, x,y, value): libtcod.map_set_properties( fovmap, x,y,value,True)
def compute_fovs():     Ref.c_managers['fov'].run()
def update_fov(obj):    Ref.c_managers['fov'].add(obj)
# circular FOV function
def can_see(obj,x,y):
    if (get_light_value(x,y) == 0 and not on(obj,NVISION)):
        return False
    return ( in_range(obj.x,obj.y, x,y, obj.stats.get('sight')) #<- circle-ize
             and libtcod.map_is_in_fov(obj.fov_map,x,y) )
#copies Map 's fov data to all creatures - only do this when needed
#   also flag all creatures for updating their fov maps
def update_all_fovmaps():
    for creat in list_creatures():
        if has_sight(creat):
            fovMap=creat.fov_map
            libtcod.map_copy(Rogue.map.fov_map,fovMap)
            update_fov(tt)
#******maybe we should overhaul this FOV system!~*************
        #creatures share fov_maps. There are a few fov_maps
        #which have different properties like x-ray vision, etc.
        #the only fov_maps we have should all be unique. Would save time.
        #update_all_fovmaps only updates these unique maps.
        #this would probably be much better, I should do this for sure.



#----------------#
#      Paths     #
#----------------#

def can_hear(obj, x,y, volume):
    if ( on(obj,DEAD) or on(obj,DEAF) or not obj.stats.get('hearing') ):
         return False
    dist=maths.dist(obj.x, obj.y, x, y)
    maxHearDist=volume*obj.stats.get('hearing')/AVG_HEARING
    if (obj.x == x and obj.y == y): return (0,0,maxHearDist,)
    if dist > maxHearDist: return False
    # calculate a path
    path=path_init_sound()
    path_compute(path, obj.x,obj.y, x,y)
    pathSize=libtcod.path_size(path)
    if dist >= 2:
        semifinal=libtcod.path_get(path, 0)
        xf,yf=semifinal
        dx=xf - obj.x
        dy=yf - obj.y
    else:
        dx=0
        dy=0
    path_destroy(path)
    loudness=(maxHearDist - pathSize - (pathSize - dist))
    if loudness > 0:
        return (dx,dy,loudness)

def path_init_movement():
    pathData=0
    return Rogue.map.path_new_movement(pathData)
def path_init_sound():
    pathData=0
    return Rogue.map.path_new_sound(pathData)
def path_destroy(path):     libtcod.path_delete(path)
def path_compute(path, xfrom,yfrom, xto,yto):
    libtcod.path_compute(path, xfrom,yfrom, xto,yto)
def path_step(path):
    x,y=libtcod.path_walk(path, True)
    return x,y
