'''
    processors.py
    Part of Softly Into the Night, a roguelike by Jacob Wharton.
    Copyright 2019.
'''

##from dataclasses import dataclass
import tcod as libtcod
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




#************************************************************************
# NOTE:                                                                 *
# Managers are those things which run independent of other processors   *
# Processors all run one after another. This is important!              *
#************************************************************************



##class GUI:
##    def
    
class GUIProcessor(esper.Processor):
    def process(self):
        pass



#
# FOV
#

class FOV:
    _list = []
    @classmethod
    def getList(cls): return cls._list
    @classmethod
    def clear(cls): cls._list = []
    # register an entity to have its FOV updated this turn
    @classmethod
    def add(cls, ent):
        if not rog.world().has_component(ent, cmp.SenseSight):
            return      # reject ents that cannot see
        cls._list.append(ent)
    
class FOVProcessor(esper.Processor):
    def process(self):
        for ent in FOV.getList():
            rog.fov_compute(ent)
        FOV.clear()


        
#
# Action Queue
#

class ActionQueue:
    ID=0
    queue=[]
    @classmethod
    def add(self, ap, func):
        ActionQueue.ID += 1
        newAction = (ActionQueue.ID, ap, func,)
        ActionQueue.queue.append(newAction)
        return newAction[0] # ID of queued action

class ActionQueueProcessor(esper.Processor):
    def process(self):
        pass


# TODO: make this, consolidate with ActionQueueProcessor
##class DelayedActionProcessor(esper.Processor):
##    
##    def __init__(self): 
##        super(DelayedActionProcessor, self).__init__()
##
##        self.actors={}
##
##    def process(self):
##        newDic = {}
##        for actor,turns in self.actors.items():
##            turns = turns - 1
##            if turns:
##                newDic.update({actor : turns})
##            else:
##                #finish task
##                self.remove(actor)
##        self.actors = newDic
##
##    def add(self, actor, turns):
##        #rog.busy(actor)
##        self.actors.update({actor : turns})
##
##    def remove(self, actor):
##        #rog.free(actor)
##        del self.actors[actor]
    


#
# Timers
#

class Timers:
    ID=0
    data={}
    @classmethod
    def add(self,t):
        _id=Timers.ID
        Timers.ID +=1
        Timers.data.update({_id : t})
        return _id
    @classmethod
    def remove(self,_id):
        Timers.data.remove(_id)

class TimersProcessor(esper.Processor):
    def process(self):
        removeList=[]
        for _id,t in Timers.data.items():
            t-=1
            if t<=0:
                removeList.append(_id)
            else:
                Timers.data.update({_id : t})
        for _id in removeList:
            Timers.remove(_id)

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
class Fires:
    _fires={}
    newfires={}
##    strongFires={} #fires that can't be put out
    lights={}
    removeList=[]
    soundsList={}

    @classmethod
    def fireat(self, x,y):
        return self._fires.get((x,y,), False)
    @classmethod
    def fires(self):
        return self._fires.keys()

    # set a tile on fire
    @classmethod
    def add(self, x,y):
        if self.fireat(x,y): return
        #print("fire addition!!")
        self._fires.update({ (x,y,) : True })
        light=rog.create_light(x,y, FIRE_LIGHT, owner=None)
        self.lights.update({(x,y,) : light})
        
        #obj.observer_add(light)
        #self.lights.update({obj : light})
        
    # remove a fire from a tile
    @classmethod
    def remove(self, x,y):
        #print("~trying to remove fire")
        if not self.fireat(x,y): return
        #print("fire removal!")
        del self._fires[(x,y,)]
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
    @classmethod
    def _addLater(self, x,y):
        if self.newfires.get((x,y,),False): return
        self.newfires.update({ (x,y,) : True})
    #put new fires onto fire grid
    @classmethod
    def _fuseGrids(self):
        for k,v in self.newfires.items():
            x,y = k
            self.add(x,y)
        self.newfires={} #reset grid2

    # look nearby a burning tile to try and set other stuff on fire
    @classmethod
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
    @classmethod
    def _gobble(self, ent):
        world = rog.world()
        pos = world.component_for_entity(ent, cmp.Position)
        form = world.component_for_entity(ent, cmp.Form)
        isCreature = world.has_component(ent, cmp.Creature)
        #print("gobbling object {} at {},{}".format(obj.name,obj.x,obj.y))
        food = 0
        if form.material == MAT_WOOD:
            food = 10
            if dice.roll(6) == 1: #chance to make popping fire sound
                self.soundsList.update( {(pos.x,pos.y,) : SND_FIRE} )
        elif form.material == MAT_FLESH:
            food = 2
            if not isCreature: #corpses burn better than alive people
                food = 3
        elif form.material == MAT_VEGGIE:
            food = 3
        elif form.material == MAT_SAWDUST:
            food = 50
##        elif obj.material == MAT_GUNPOWDER:
##            food = 100
        elif form.material == MAT_PAPER:
            food = 10
        elif form.material == MAT_CLOTH:
            food = 10
        elif form.material == MAT_LEATHER:
            food = 1
        elif form.material == MAT_FUNGUS:
            food = 1
        elif form.material == MAT_PLASTIC:
            food = 1
        return food

class FireProcessor(esper.Processor):
    def process(self):
        pass
    # TODO: update this to use the method w/o for loops (numpy/scipy)
    
##        Fires.removeList=[]
##        Fires.soundsList={}
##        for fx,fy in Fires.fires:
##            #print("running fire manager for fire at {},{}".format(x,y))
##            _fluids = rog.fluidsat(fx,fy)
##            _things = rog.thingsat(fx,fy)
##            _exit=False
##
##            #tiles that put out fires or feed fires
##            '''
##            wet floor flag
##
##
##            '''
##
##            #fluids that put out fires or feed fires
##            '''for flud in _fluids:
##                if flud.extinguish:
##                    self.remove(fx,fy)
##                    _exit=True
##                    continue
##                if flud.flammable:
##                    self.fire_spread(fx,fy)
##                    continue
##                    '''
##
##            if _exit: continue
##
##            #check for no fuel condition
##            if not _things:
##                #print("no things to burn. Removing fire at {},{}".format(x,y))
##                self.removeList.append((fx,fy,))
##                continue
##
##            #BURN THINGS ALIVE (or dead)
##            food=0  #counter for amount of fuel gained by the fire
##            for ent in _things: #things that might fuel the fire (or put it out)
##                textSee=""
##                rog.burn(ent, FIRE_BURN)
##                if rog.on(ent,FIRE):
##                    food += self._gobble(ent)
##            
##            _FOOD_THRESHOLD=5
##            '''if food < _FOOD_THRESHOLD:
##                if dice.roll(food) == 1:
##                    print("not enough food. Removing fire at {},{}".format(fx,fy))
##                    self.removeList.append((fx,fy,))
##            else:'''
##            if food >= _FOOD_THRESHOLD:
##                iterations = 1+int((food - _FOOD_THRESHOLD)/3)
##                self._spread(fx,fy,iterations)
##            elif food == 0:
##                self.removeList.append((fx,fy,))
##                continue
##                    
##        #end for (fires)
##
##        #add new fires
##        self._fuseGrids()
##
##        #remove fires
##        for xx,yy in self.removeList:
##            #print("fire at {},{} is to be removed...".format(xx,yy))
##            self.remove(xx,yy)
##            
##            '''doNotDie=False
##            #don't let the fire die if something in this tile is still burning.
##            for tt in _things:
##                if rog.on(tt, FIRE):
##                    doNotDie=True
##            if doNotDie == False:'''
##
##        #sounds
##        for k,v in self.soundsList.items():
##            xx,yy = k
##            snd = v
##            rog.event_sound(xx,yy, snd)
                    

#
# Fluids
#

class Fluids:
    _fluids={}
    @classmethod
    def _flow(self):
        pass
    # TODO: use numpy to flow fluids...
    @classmethod
    def flow(self):
        Fluids._flow()

class FluidProcessor(esper.Processor):
    def process(self):
        Fluids.flow()


##    def fluidsat(self,x,y):
##        return self._fluids.get((x,y,), ())


    
#
# Status
#

class Status:
    @classmethod
    def add(self, ent, component):
        if rog.world().has_component(ent, component): return False
        #attribute modifiers
        #auxiliary effects
        #message
        ## NOTE: is this the best way to do this? 
        rog.world().add_component(ent, component)
        return True
        
    @classmethod
    def remove(self, ent, component):
        if not rog.world().has_component(ent, component): return False
        #attribute modifiers
        #auxiliary effects
        #message
        rog.world().remove_component(ent, component)
        return True
    
    @classmethod
    def remove_all(self, ent):
        for status in cmp.STATUS_COMPONENTS:
            if not rog.world().has_component(ent, component):
                continue
            #attribute modifiers
            #auxiliary effects
            #message
            rog.world().remove_component(ent, component)

class StatusProcessor(esper.Processor):
    def process(self):
        #get data
        removals=[]
        burningData_init=[]
        burningData=[]
        for ent, cc in self.world.get_component(cmp.StatusFire):
            hp = self.world.component_for_entity(ent, cmp.Stats).hp
            burningData_init.append((ent, cc.timer, hp,))
        
        #update data
        for ent, timer, hp in burningData_init:
            hp -= 1
            timer -= 1
            if timer <= 0:
                removals.update({ent, cmp.StatusFire})
                continue
            if hp <= 0:
                removals.update({ent, cmp.StatusFire})
                rog.kill(ent)
                continue
            burningData.append((ent, timer, hp,))
        
        #distribute data
        for ent, timer, hp in burningData:
            stats = self.world.component_for_entity(ent, cmp.Stats)
            status = self.world.component_for_entity(ent, cmp.StatusFire)
            status.timer = timer
            stats.hp = hp
            make(ent,DIRTY_STATS)
        
        #remove expired status effects
        for ent, component in removals:
            Status.remove(ent, component)
    



#
# Status Meters
#
    #Status Meters are the build-up counters for status effects like fire, sickness, etc.
        
class MetersProcessor(esper.Processor):
    def process(self):
        for ent,stats in self.world.get_component(cmp.Meters):
            #print(thing.name," is getting cooled down") #TESTING
            # cool down temperature meter if not currently burning
            if (stats.temp > 0 and not self.world.component_for_entity(ent, cmp.StatusFire)):
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
        
    


        












##STATUSES={
### ID    : defaultDur, onVerb, statusVerb,
##WET     : (100,     "is",   "wet",),
##SPRINT  : (10,      "begins", "sprinting",),
##TIRED   : (50,      "is", "tired",),
##HASTE   : (20,      "is", "hasty",),
##SLOW    : (10,      "is", "slowed",),
##FIRE    : (99999999,"catches", "on fire",),
##SICK    : (500,     "is", "sick",),
##ACID    : (7,       "begins", "corroding",),
##IRRIT   : (200,     "is", "irritated",),
##PARAL   : (5,       "is", "paralyzed",),
##COUGH   : (10,      "is", "in a coughing fit",),
##VOMIT   : (25,      "is", "wretching",),
##BLIND   : (20,      "is", "blinded",),
##DEAF    : (100,     "is", "deafened",),
##TRAUMA  : (99999999,"is", "traumatized",),
##    }

        



