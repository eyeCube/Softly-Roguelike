'''
    processors.py
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
'''

##from dataclasses import dataclass
import tcod as libtcod
import numpy as np
import scipy.signal
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
    soundsList={}
    entsources={} # entity heat sources
    
    fires           = np.full((ROOMW,ROOMH,), fill_value=False)
    fuel            = np.full((ROOMW,ROOMH,), fill_value=0, dtype=np.int16)
    heat            = np.full((ROOMW,ROOMH,), fill_value=0, dtype=np.float64)
    heat_sources    = np.full((ROOMW,ROOMH,), fill_value=0, dtype=np.float64)
    
    # dispersion arrays
    DISPERSE_0 = np.array( # no wind
        [   [5,  7,  5],
            [7,  67, 7],
            [5,  7,  5], ],
        dtype=np.float64,
    )
    DISPERSE_0 /= DISPERSE_0.sum()
    
    # orthogonal winds
    DISPERSE_1 = np.array( # easterly wind, slight strength
        [   [4,  6,  8],
            [3,  54, 16],
            [4,  6,  8], ],
        dtype=np.float64
    )
    DISPERSE_1 /= DISPERSE_1.sum()
    DISPERSE_2 = np.array( # easterly wind, med-low strength
        [   [4,  6,  12],
            [2,  54, 28],
            [4,  6,  12], ],
        dtype=np.float64
    )
    DISPERSE_2 /= DISPERSE_2.sum()
    DISPERSE_3 = np.array( # easterly wind, med-high strength
        [   [4,  6,  14],
            [2,  54, 42],
            [4,  6,  14], ],
        dtype=np.float64,
    )
    DISPERSE_3 /= DISPERSE_3.sum()
    DISPERSE_4 = np.array( # easterly wind, high strength
        [   [3,  6,  15],
            [2,  52, 54],
            [3,  6,  15], ],
        dtype=np.float64,
    )
    DISPERSE_4 /= DISPERSE_4.sum()
    DISPERSE_5 = np.array( # easterly wind, v. high strength
        [   [3,  6,  16],
            [2,  50, 66],
            [3,  6,  16], ],
        dtype=np.float64,
    )
    DISPERSE_5 /= DISPERSE_5.sum()
    
    # diagonal winds
    DISPERSE_1_DIAG = np.array( # southeasterly wind, slight strength
        [   [3,  5,  6],
            [5,  54, 10],
            [6,  10, 14], ],
        dtype=np.float64,
    )
    DISPERSE_1_DIAG /= DISPERSE_1_DIAG.sum()
    DISPERSE_2_DIAG = np.array( # southeasterly wind, med-low strength
        [   [3,  5,  6],
            [5,  54, 14],
            [6,  14, 22], ],
        dtype=np.float64,
    )
    DISPERSE_2_DIAG /= DISPERSE_2_DIAG.sum()
    DISPERSE_3_DIAG = np.array( # southeasterly wind, med-high strength
        [   [2,  4,  6],
            [4,  54, 16],
            [6,  16, 32], ],
        dtype=np.float64,
    )
    DISPERSE_3_DIAG /= DISPERSE_3_DIAG.sum()
    DISPERSE_4_DIAG = np.array( # southeasterly wind, high strength
        [   [2,  4,  6],
            [4,  50, 17],
            [6,  17, 42], ],
        dtype=np.float64,
    )
    DISPERSE_4_DIAG /= DISPERSE_4_DIAG.sum()
    DISPERSE_5_DIAG = np.array( # southeasterly wind, v. high strength
        [   [1,  3,  6],
            [3,  46, 17],
            [6,  17, 54], ],
        dtype=np.float64,
    )
    DISPERSE_5_DIAG /= DISPERSE_5_DIAG.sum()
    
    DISPERSE_ORTHO = (
        DISPERSE_1, DISPERSE_2, DISPERSE_3,
        DISPERSE_4, DISPERSE_5,
    )
    DISPERSE_DIAG  = (
        DISPERSE_1_DIAG, DISPERSE_2_DIAG, DISPERSE_3_DIAG,
        DISPERSE_4_DIAG, DISPERSE_5_DIAG,
    )
    
    ROTAMT = {
        # for getting number of 90 degree ccw rotations.
        #   From direction to number of rotations.
        #   Orthogonal directions use disperse_ortho grids,
        #   diagonal use the disperse_diag grids.
        (1,1)   : 0,
        (1,-1)  : 1,
        (-1,-1) : 2,
        (-1,1)  : 3,
        (1,0)   : 0,
        (0,-1)  : 1,
        (-1,0)  : 2,
        (0,1)   : 3,
        }
    
    # hashing
    @classmethod
    def Index(cls, x, y): # get a unique index for the x,y pair
        return x + y*1000
    @classmethod
    def Coords(cls, index): # get the coordinates corresponding to the index given
        return (index % 1000, index // 1000,)
    
    # fires
    @classmethod
    def init_fires(cls):
        cls.fires = np.full((ROOMW,ROOMH,), fill_value=False)
    @classmethod
    def fireat(cls, x,y): # fire present at pos x,y ?
        return cls.fires[y][x]
    
    # heat
    @classmethod
    def init_heat(cls):
        cls.heat = np.full((ROOMW,ROOMH,), fill_value=0, dtype=np.float64)
    @classmethod
    def tempat(cls, x,y): # get temperature at pos x,y
        return cls.heat[y][x]
    @classmethod
    def add_heat(cls,x,y,temp): cls.heat[y][x] += temp
    @classmethod
    def remove_heat(cls,x,y,temp): cls.heat[y][x] -= temp
    
    # fuel
    @classmethod
    def init_fuel(cls):
        cls.fuel = np.full((ROOMW,ROOMH,), fill_value=0, dtype=np.int16)
    @classmethod
    def add_fuel(cls,x,y,fuel): cls.fuel[y][x] += fuel
    @classmethod
    def remove_fuel(cls,x,y,fuel):
        cls.fuel[y][x] = max(0, cls.fuel[y][x] - fuel)
    
    # heat sources
    @classmethod
    def init_heat_sources(cls):
        cls.heat_sources = np.full(
            (ROOMW,ROOMH,), fill_value=0, dtype=np.float64
            )
    @classmethod
    def add_heat_source(cls,x,y,temp): cls.heat_sources[y][x] += temp
    @classmethod
    def remove_heat_source(cls,x,y,temp): cls.heat_sources[y][x] -= temp
    
    # entity heat sources
    @classmethod
    def add_entity_heat_source(cls, ent):
        pos = rog.world().component_for_entity(ent, cmp.Position)
        temp = rog.world().component_for_entity(ent, cmp.Meters).temp
        mass = rog.getms(ent, "mass")
        sourceValue = cls.calc_source_heat(temp, mass)
        if ent in cls.entsources: # remove current heat source data for entity
            cls.heat_sources[pos.y][pos.x] -= cls.entsources[ent]
        cls.heat_sources[pos.y][pos.x] += sourceValue
        cls.entsources[ent] = sourceValue
    @classmethod
    def remove_entity_heat_source(cls, ent):
        if ent in cls.entsources:
            pos = rog.world().component_for_entity(ent, cmp.Position)
            cls.heat_sources[pos.y][pos.x] -= cls.entsources[ent]
            del cls.entsources[ent]
    @classmethod
    def calc_source_heat(cls, temp, mass):
        return (temp*mass / (MULT_MASS*100))
    
    # wind
    @classmethod
    def get_disperse(cls, wind_force, wind_direction):
        if wind_force==0: # no wind, just return regular dispersion grid
            return cls.DISPERSE_0
        # get the basic matrix
        xd, yd = wind_direction
        if (xd + yd) % 2 == 0: # it's diagonal
            matrix = cls.DISPERSE_DIAG[wind_force - 1]
        else: # it's orthogonal
            matrix = cls.DISPERSE_ORTHO[wind_force - 1]
        # rotate matrix by direction
        rotamt = cls.ROTAMT[wind_direction]
        matrix = np.rot90(matrix, rotamt)
##        print("TESTING disperse array...\nforce: {}\ndir: {}\nmatrix: {}".format(
##            wind_force, wind_direction, matrix))
        return matrix

# Fires Processor Fire Processor
class FireProcessor(esper.Processor):
    
    def __init__(self):
        self.clist=[] # coordinate list of fires
        self.lights={} # dict of lights created by fires
    
    def process(self):
        world = rog.world()
        
        # get fuel amount
            # for now this should be fine; only update this if
            # performance from this particular 3 lines of code
            # is seriously something to be concerned about.
        Fires.init_fuel()
        for ent, compos in world.get_components(cmp.Fuel, cmp.Position):
            fuel, pos = compos
            # apply fuel multipliers
            # mass affects fuel value
            mass = rog.getms(ent,"mass") / MULT_MASS
            # add fuel to the grid
            Fires.add_fuel(pos.x, pos.y, round(fuel.fuel * mass))
            
        # disperse heat, handle fires
        dispersion=Fires.get_disperse(rog.wind_force(),rog.wind_direction())
        Fires.heat += Fires.heat_sources # heat sources radiating heat
        Fires.heat += Fires.fires * Fires.fuel # fires creating heat
        Fires.heat += ENVIRONMENT_DELTA_HEAT # passive heat loss (or gain)
        Fires.heat = scipy.signal.convolve2d( # Spread heat to adjacent cells.
            Fires.heat, dispersion, mode='same', boundary='fill', fillvalue=0
        )
        
        # get the fires grid
        Fires.fires = (Fires.heat >= FIRE_THRESHOLD) * (Fires.fuel > 0) # get grid of fires (true/false)
        
        # limits
        np.clip(Fires.heat, HEATMIN, HEATMAX, out=Fires.heat) # min/max the heat grid
        
        # get list of x,y coordinate pairs of cells that are on fire
        oldlist=self.clist.copy() # old list = the list before we update it.
        self.clist=np.stack(Fires.fires.nonzero(), axis = 1) # coord. list
        oldset=set() # old coordinate index set from last iteration
        for item in oldlist:
            y, x = item
            oldset.add(Fires.Index(x,y))
        cset=set() # current coordinate index set
        for item in self.clist:
            y, x = item
            cset.add(Fires.Index(x,y))
        
        # get the fires which are new since last iteration
        newfires = [i for i in cset if i not in oldset]
        # get the fires which have gone out since last iteration
        outfires = [i for i in oldset if i not in cset]
        
        # add new lights where there are new fires
        for fireID in newfires:
            x, y = Fires.Coords(fireID)
##            print("new fire at pos. x={} y={}".format(x,y))
            light=rog.create_light(x,y, FIRE_LIGHT, owner=None)
            self.lights.update({fireID : light})
        # release lights from fires that have gone out
        for fireID in outfires:
            x, y = Fires.Coords(fireID)
##            print("fire put out at pos. x={} y={}".format(x,y))
            rog.release_light(self.lights[fireID])
            del self.lights[fireID]
    #
#


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

# Fluid Processor Fluids Processor
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
    def add(self, ent, component, t=-1):
        if rog.world().has_component(ent, component): return False
        status_str = ""
        #attribute modifiers, aux. effects, message (based on status type)
        if component is cmp.StatusFire:
            status_str = " catches fire"
        elif component is cmp.StatusFrozen:
            status_str = " becomes frozen"
            rog.damage(ent, FREEZE_DAMAGE)
        elif component is cmp.StatusAcid:
            status_str = " begins corroding"
        elif component is cmp.StatusBlind:
            status_str = " becomes blinded"
        elif component is cmp.StatusDeaf:
            status_str = " becomes deafened"
        elif component is cmp.StatusIrritated:
            status_str = " becomes irritated"
        elif component is cmp.StatusBleed:
            status_str = " begin bleeding"
        elif component is cmp.StatusParalyzed:
            status_str = "'s muscles stiffen"
        elif component is cmp.StatusSick:
            status_str = " comes down with the sickness"
        elif component is cmp.StatusVomit:
            status_str = " becomes nauseous"
        elif component is cmp.StatusCough:
            status_str = " enters into a coughing fit"
        elif component is cmp.StatusSprint:
            status_str = " starts sprinting"
        elif component is cmp.StatusTired:
            status_str = " starts to yawn"
        elif component is cmp.StatusFrightening:
            status_str = " becomes scarier"
        elif component is cmp.StatusFrightened:
            status_str = " becomes frightened"
        elif component is cmp.StatusHaste:
            status_str = "'s movements speed up"
            rog.alts(ent, "spd", HASTE_SPEEDMOD)
        elif component is cmp.StatusSlow:
            status_str = "'s movements slow"
            rog.alts(ent, "spd", SLOW_SPEEDMOD)
        elif component is cmp.StatusDrunk:
            status_str = " becomes inebriated"
        elif component is cmp.StatusHeadInjury:
            status_str = " hits {} head".format(gender.pronouns[2])
        #if status_str:
            #"{}{}{}".format(name.title, name.name, status_str)
        if t==-1: # use the default time value for the component
            rog.world().add_component(ent, component())
        else: # pass in the time value
            rog.world().add_component(ent, component(t))
        return True
        
    @classmethod
    def remove(self, ent, component):
        if not rog.world().has_component(ent, component): return False
        status_str = ""
        #attribute modifiers, aux. effects, message (based on status type)
        if component is cmp.StatusHaste:
            status_str = "'s movements slow"
            rog.alts(ent, "spd", -HASTE_SPEEDMOD)
        elif component is cmp.StatusSlow:
            status_str = "'s movements speed up"
            rog.alts(ent, "spd", -SLOW_SPEEDMOD)
        #if status_str:
            #"{}{}{}".format(name.title, name.name, status_str)
        rog.world().remove_component(ent, component)
        return True
    
    @classmethod
    def remove_all(self, ent): # TODO: finish this and add STATUS_COMPONENTS constant to the class
        for status, component in cmp.STATUS_COMPONENTS:
            if not rog.world().has_component(ent, component):
                continue
            #attribute modifiers
            #auxiliary effects
            #message
            rog.world().remove_component(ent, component)

class StatusProcessor(esper.Processor):
    def process(self):
        for ent, compo in self.world.get_component(cmp.StatusFire):
            temp = self.world.component_for_entity(ent, cmp.Meters).temp
            if temp < FIRE_THRESHOLD:
                Status.remove(ent, cmp.StatusFire)
                continue
            rog.damage(ent, 1)
        for ent, compo in self.world.get_component(cmp.StatusFrozen):
            temp = self.world.component_for_entity(ent, cmp.Meters).temp
            if temp > FREEZE_THRESHOLD:
                Status.remove(ent, cmp.StatusFrozen)
                continue



#
# Status Meters
#
    #Status Meters are the build-up counters for status effects like fire, sickness, etc.
        
class MetersProcessor(esper.Processor):
    def process(self):
        for ent,stats in self.world.get_component(cmp.Meters):
            '''
                interface with environment
                    (e.g. in cases of heat exchange with the air)
                and take effects from internal state
            '''
            
            def _getambd(dt, mass):
                ''' get the amount of ambient temperature change
                    based on how much the entity's temperature changed.
                    The more massive, the greater the effect. '''
                return -dt * mass / MULT_MASS
            
            pos = rog.world().component_for_entity(ent, cmp.Position)
            ambient_temp = Fires.tempat(pos.x, pos.y)
            
            #print(thing.name," is getting cooled down") #TESTING
            # cool down temperature meter if not currently burning
            if (abs(stats.temp - ambient_temp) >= 1):
                # TODO: take insulation into account for deltatemp
                #   as well as the actual difference in temperature
                deltatemp = rog.sign(ambient_temp - stats.temp)
                stats.temp = stats.temp + deltatemp
                ambientdelta = _getambd(deltatemp, rog.getms(ent,"mass"))
                Fires.add_heat(pos.x, pos.y, ambientdelta)
##                print("adding heat {} to pos {} {} (mass {}) (heat={})".format(ambientdelta, pos.x, pos.y, rog.getms(ent,"mass"), Fires.tempat(pos.x,pos.y)))
                if (not rog.get_status(ent, cmp.StatusFire) and
                    stats.temp >= FIRE_THRESHOLD):
                    rog.set_status(ent, cmp.StatusFire)
                elif (not rog.get_status(ent, cmp.StatusFrozen) and
                    stats.temp <= FREEZE_THRESHOLD):
                    rog.set_status(ent, cmp.StatusFrozen)
            # sickness meter
            if (stats.sick > 0):
                stats.sick = max(0, stats.sick - BIO_METERLOSS)
            # exposure meter
            if (stats.expo > 0):
                stats.expo = max(0, stats.expo - CHEM_METERLOSS)
            # rads meter
            #if (thing.stats.rads > 0):
            #    thing.stats.rads -= 1
        
    


        










                ''' only commented out code below '''












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




# OLD CODE FOR FIRE MANAGER:   
##
##    # set a tile on fire
##    @classmethod
##    def add(self, x,y):
##        if self.fireat(x,y): return
##        #print("fire addition!!")
##        self._fires.update({ (x,y,) : True })
##        light=rog.create_light(x,y, FIRE_LIGHT, owner=None)
##        self.lights.update({(x,y,) : light})
##        
##        #obj.observer_add(light)
##        #self.lights.update({obj : light})
##        
##    # remove a fire from a tile
##    @classmethod
##    def remove(self, x,y):
##        #print("~trying to remove fire")
##        if not self.fireat(x,y): return
##        #print("fire removal!")
##        del self._fires[(x,y,)]
##        light=self.lights[(x,y,)]
##        rog.release_light(light)
##        del self.lights[(x,y,)]
##        #TODO: Douse sound
##        '''obj=rog.thingat(x,y)
##        if obj:
##            textSee="The fire on {n} is extinguished.".format(n=obj.name)
##            rog.event_sight(obj.x,obj.y, textSee)
##            #rog.event_sound(obj.x,obj.y, SND_DOUSE)'''
##
##    #tell it to add a fire but not yet
##    @classmethod
##    def _addLater(self, x,y):
##        if self.newfires.get((x,y,),False): return
##        self.newfires.update({ (x,y,) : True})
##    #put new fires onto fire grid
##    @classmethod
##    def _fuseGrids(self):
##        for k,v in self.newfires.items():
##            x,y = k
##            self.add(x,y)
##        self.newfires={} #reset grid2
##
##    # look nearby a burning tile to try and set other stuff on fire
##    @classmethod
##    def _spread(self, xo, yo, iterations):
##        #heat=FIREBURN #could vary based on what's burning here, etc...
##        for ii in range(iterations):
##            index = dice.roll(8) - 1
##            x,y = DIRECTION_FROM_INT[index]
##            fuel=rog.thingat(xo + x, yo + y)
##            if fuel:
##                self._addLater(xo + x, yo + y)
##
##    #consume an object
##    #get food value based on object passed in
##        #get sound effects "
##    @classmethod
##    def _gobble(self, ent):
##        world = rog.world()
##        pos = world.component_for_entity(ent, cmp.Position)
##        form = world.component_for_entity(ent, cmp.Form)
##        isCreature = world.has_component(ent, cmp.Creature)
##        #print("gobbling object {} at {},{}".format(obj.name,obj.x,obj.y))
##        food = 0
##        if form.material == MAT_WOOD:
##            food = 10
##            if dice.roll(6) == 1: #chance to make popping fire sound
##                self.soundsList.update( {(pos.x,pos.y,) : SND_FIRE} )
##        elif form.material == MAT_FLESH:
##            food = 2
##            if not isCreature: #corpses burn better than alive people
##                food = 3
##        elif form.material == MAT_VEGGIE:
##            food = 3
##        elif form.material == MAT_SAWDUST:
##            food = 50
####        elif obj.material == MAT_GUNPOWDER:
####            food = 100
##        elif form.material == MAT_PAPER:
##            food = 10
##        elif form.material == MAT_CLOTH:
##            food = 10
##        elif form.material == MAT_LEATHER:
##            food = 1
##        elif form.material == MAT_FUNGUS:
##            food = 1
##        elif form.material == MAT_PLASTIC:
##            food = 1
##        return food

    
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
                    

        



