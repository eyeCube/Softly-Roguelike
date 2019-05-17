#
# some various managers
# and parent manager objects
#

import libtcodpy as libtcod
import numpy as np
import esper
import time
import math

from const      import *
import rogue    as rog
import orangio  as IO
import components as cmp
import maths
import misc
import dice



#**********************************************************************
# NOTE:
# Managers become those things which run independent of other processors
# Processors all run one after another. This is important!
#**********************************************************************


#
# Action Queue
#

class ActionQueueProcessor(esper.Processor):
    def __init__(self):
        super(ActionQueueProcessor, self).__init__()

        self.queue=[]

    def process(self):
        pass


#
# Timers
#

class TimersProcessor(esper.Processor):
    ID=0

    def __init__(self):
        super(TimersProcessor, self).__init__()

        self.data={}

    def process(self):
        super(TimersProcessor, self).run()
        
        for _id,t in self.data.items():
            t-=1
            if t<=0:
                self.remove(_id)
            self.data.update({_id : t})

    def add(self,t):
        _id=TimersProcessor.ID
        TimersProcessor.ID +=1
        self.data.update({_id : t})
        return _id
    def remove(self,_id):
        self.data.remove(_id)

'''
timer=bt_managers['timers'].add(time)
return timer
'''



#
# Fires
#
    # stores fire grid; controls fires;
    #   light and messages from fire, fire spreading and dousing
    # Note: does not control burning status effect
class FiresProcessor(esper.Processor):

    def __init__(self):
        super(FiresProcessor, self).__init__()

        self.fires={}
        self.newfires={}
        #self.strongFires={} #fires that can't be put out
        self.lights={}
        self.removeList=[]
        self.soundsList={}

    def process(self):
        super(FiresProcessor, self).run()

        self.removeList=[]
        self.soundsList={}
        for fx,fy in self.fires:
            #print("running fire manager for fire at {},{}".format(x,y))
            _fluids = rog.fluidsat(fx,fy)
            _things = rog.thingsat(fx,fy)
            _exit=False

            #tiles that put out fires or feed fires
            '''
            wet floor flag


            '''

            #fluids that put out fires or feed fires
            '''for flud in _fluids:
                if flud.extinguish:
                    self.remove(fx,fy)
                    _exit=True
                    continue
                if flud.flammable:
                    self.fire_spread(fx,fy)
                    continue
                    '''

            if _exit: continue

            #check for no fuel condition
            if not _things:
                #print("no things to burn. Removing fire at {},{}".format(x,y))
                self.removeList.append((fx,fy,))
                continue

            #BURN THINGS ALIVE (or dead)
            food=0  #counter for amount of fuel gained by the fire
            for ent in _things: #things that might fuel the fire (or put it out)
                textSee=""
                rog.burn(ent, FIRE_BURN)
                if rog.on(ent,FIRE):
                    food += self._gobble(ent)
            
            _FOOD_THRESHOLD=5
            '''if food < _FOOD_THRESHOLD:
                if dice.roll(food) == 1:
                    print("not enough food. Removing fire at {},{}".format(fx,fy))
                    self.removeList.append((fx,fy,))
            else:'''
            if food >= _FOOD_THRESHOLD:
                iterations = 1+int((food - _FOOD_THRESHOLD)/3)
                self._spread(fx,fy,iterations)
            elif food == 0:
                self.removeList.append((fx,fy,))
                continue
                    
        #end for (fires)

        #add new fires
        self._fuseGrids()

        #remove fires
        for xx,yy in self.removeList:
            #print("fire at {},{} is to be removed...".format(xx,yy))
            self.remove(xx,yy)
            
            '''doNotDie=False
            #don't let the fire die if something in this tile is still burning.
            for tt in _things:
                if rog.on(tt, FIRE):
                    doNotDie=True
            if doNotDie == False:'''

        #sounds
        for k,v in self.soundsList.items():
            xx,yy = k
            snd = v
            rog.event_sound(xx,yy, snd)
                    
    #end def

    def fireat(self, x,y):  return self.fires.get((x,y,), False)
    def fires(self):        return self.fires.keys()

    # set a tile on fire
    def add(self, x,y):
        if self.fireat(x,y): return
        #print("fire addition!!")
        self.fires.update({ (x,y,) : True })
        light=rog.create_light(x,y, FIRE_LIGHT, owner=None)
        self.lights.update({(x,y,) : light})
        
        #obj.observer_add(light)
        #self.lights.update({obj : light})
        
    # remove a fire from a tile
    def remove(self, x,y):
        #print("~trying to remove fire")
        if not self.fireat(x,y): return
        #print("fire removal!")
        del self.fires[(x,y,)]
        light=self.lights[(x,y,)]
        rog.release_light(light)
        del self.lights[(x,y,)]
        #TODO: Douse sound
        '''obj=rog.thingat(x,y)
        if obj:
            textSee="The fire on {n} is extinguished.".format(n=obj.name)
            rog.event_sight(obj.x,obj.y, textSee)
            #rog.event_sound(obj.x,obj.y, SND_DOUSE)'''

    #tell it to add a fire but not yet
    def _addLater(self, x,y):
        if self.newfires.get((x,y,),False): return
        self.newfires.update({ (x,y,) : True})
    #put new fires onto fire grid
    def _fuseGrids(self):
        for k,v in self.newfires.items():
            x,y = k
            self.add(x,y)
        self.newfires={} #reset grid2

    # look nearby a burning tile to try and set other stuff on fire
    def _spread(self, xo, yo, iterations):
        #heat=FIREBURN #could vary based on what's burning here, etc...
        for ii in range(iterations):
            index = dice.roll(8) - 1
            x,y = DIRECTION_FROM_INT[index]
            fuel=rog.thingat(xo + x, yo + y)
            if fuel:
                self._addLater(xo + x, yo + y)

    #consume an object
    #get food value based on object passed in
        #get sound effects "
    def _gobble(self, ent):
        world = rog.world()
        pos = world.component_for_entity(ent, cmp.Position)
        stats = world.component_for_entity(ent, cmp.BasicStats)
        isCreature = world.has_component(ent, cmp.Creature)
        #print("gobbling object {} at {},{}".format(obj.name,obj.x,obj.y))
        food = 0
        if stats.material == MAT_WOOD:
            food = 10
            if dice.roll(6) == 1: #chance to make popping fire sound
                self.soundsList.update( {(pos.x,pos.y,) : SND_FIRE} )
        elif stats.material == MAT_FLESH:
            food = 2
            if not isCreature: #corpses burn better than alive people
                food = 3
        elif obj.material == MAT_VEGGIE:
            food = 3
        elif obj.material == MAT_SAWDUST:
            food = 50
        elif obj.material == MAT_GUNPOWDER:
            food = 100
        elif obj.material == MAT_PAPER:
            food = 10
        elif obj.material == MAT_CLOTH:
            food = 10
        elif obj.material == MAT_LEATHER:
            food = 1
        elif obj.material == MAT_FUNGUS:
            food = 1
        elif obj.material == MAT_PLASTIC:
            food = 1
        return food


#
# Fluids
#

class FluidsProcessor(esper.Processor):
    def __init__(self):
        super(FluidsProcessor, self).__init__()
        
##        self._fluids={}

    def process(self):
        self._flow()

    def _flow(self):
        pass

##    def fluidsat(self,x,y):
##        return self._fluids.get((x,y,), ())


    
#
# Status
#
STATUSES={
# ID    : defaultDur, onVerb, statusVerb,
WET     : (100,     "is",   "wet",),
SPRINT  : (10,      "begins", "sprinting",),
TIRED   : (50,      "is", "tired",),
HASTE   : (20,      "is", "hasty",),
SLOW    : (10,      "is", "slowed",),
FIRE    : (99999999,"catches", "on fire",),
SICK    : (500,     "is", "sick",),
ACID    : (7,       "begins", "corroding",),
IRRIT   : (200,     "is", "irritated",),
PARAL   : (5,       "is", "paralyzed",),
COUGH   : (10,      "is", "in a coughing fit",),
VOMIT   : (25,      "is", "wretching",),
BLIND   : (20,      "is", "blinded",),
DEAF    : (100,     "is", "deafened",),
TRAUMA  : (99999999,"is", "traumatized",),
    }

    #manager for all status effects
class StatusProcessor(esper.Processor):
    def __init__(self):
        super(StatusProcessor, self).__init__()

    def process(self):
        #get data
        removals=[]
        burningData_init=[]
        burningData=[]
        for ent, cc in self.world.get_component(cmp.StatusBurning):
            hp = self.world.component_for_entity(ent, cmp.BasicStats).hp
            burningData_init.append((ent, cc.timer, hp,))
        
        #update data
        for ent, timer, hp in burningData_init:
            hp -= 1
            timer -= 1
            if timer <= 0:
                removals.update({ent, cmp.StatusBurning})
                continue
            if hp <= 0:
                removals.update({ent, cmp.StatusBurning})
                rog.kill(ent)
                continue
            burningData.append((ent, timer, hp,))
        
        #distribute data
        for ent, timer, hp in burningData:
            stats = self.world.component_for_entity(ent, cmp.BasicStats)
            status = self.world.component_for_entity(ent, cmp.StatusBurning)
            stats.timer = timer
            stats.hp = hp
        
        #remove expired status effects
        for ent, component in removals:
            self.status_remove(ent, component)
    
    def status_add(self, ent, component):
        if self.world.has_component(ent, component): return False
        #attribute modifiers
        #auxiliary effects
        #message
        ## NOTE: is this the best way to do this? 
        self.world.add_component(ent, component)
        return True
        
    def status_remove(self, ent, component):
        if not self.world.has_component(ent, component): return False
        #attribute modifiers
        #auxiliary effects
        #message
        self.world.remove_component(ent, component)
        return True
        
            


#
# Status Meters
#
    #Status Meters are the build-up counters for status effects like fire, sickness, etc.
        
class MetersProcessor(esper.Processor):

    def __init__(self):
        super(MetersProcessor, self).__init__()

        pass

    def process(self):
        super(MetersProcessor, self).run()

        for ent in rog.list_things():
            stats = self.world.component_for_entity(ent, cmp.BasicStats)
            #print(thing.name," is getting cooled down") #TESTING
            # cool down temperature meter if not currently burning
            if (stats.temp > 0 and not rog.on(ent, FIRE)):
                stats.temp = max(0, stats.temp - FIRE_METERLOSS)
            #warm up
            if (stats.temp < 0):
                stats.temp = min(0, stats.temp + FIRE_METERGAIN)
            # sickness meter
            if (stats.sick > 0):
                stats.sick = max(0, stats.sick - BIO_METERLOSS)
            # exposure meter
            if (stats.expo > 0):
                stats.expo = max(0, stats.expo - CHEM_METERLOSS)
            # rads meter
            #if (thing.stats.rads > 0):
            #    thing.stats.rads -= 1
        


#
# FOV
#

class FOV_Processor(esper.Processor):

    def __init__(self):
        super(FOV_Processor, self).__init__()

        self.update_objs=[]

    def process(self):
        super(FOV_Processor, self).run()
        
        for obj in self.update_objs:
            rog.fov_compute(obj)
        
        self.update_objs=[]
    
    # register a monster to have its FOV updated next turn
    def add(self,obj):
        if obj.stats.get('sight') > 0:     # reject objects that can't see
            self.update_objs.append(obj)
        



class DelayedActionProcessor(esper.Processor):
    
    def __init__(self): 
        super(DelayedActionProcessor, self).__init__()

        self.actors={}

    def run(self):
        newDic = {}
        for actor,turns in self.actors.items():
            turns = turns - 1
            if turns:
                newDic.update({actor : turns})
            else:
                #finish task
                self.remove(actor)
        self.actors = newDic

    def add(self, actor, turns):
        #rog.busy(actor)
        self.actors.update({actor : turns})

    def remove(self, actor):
        #rog.free(actor)
        del self.actors[actor]
    
        















