'''
    processors.py
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

###
### in action.py:
###
##def finishFunc(ent, data):
##    pass
##def cancelFunc(ent, data, apRemaining):
##    # create a useless pile of junk, remove some components from inventory,
##    # etc.
##    pass
##ActionQueue.queue(
##    pc,
##    nrgCost,
##    finishFunc,
##    data=ActionCraftingItem(),
##    cancelfunc=cancelFunc
##    )
###


##class GUI:
##    def
    
##class GUIProcessor(esper.Processor):
##    def process(self):
##        pass



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

# Stores the data for tasks that take entities multiple turns to finish
# call "queue" to add a new task,
#   "get" to get the Action object,
#   "pay" to spend a certain number of AP towards finishing the task

class ActionQueue:
    
    @classmethod
    def get(cls, ent):
        assert(rog.world().has_component(ent, cmp.QueuedAction))
        return rog.world().component_for_entity(ent, cmp.QueuedAction)
    
    @classmethod
    def queue(cls, ent, totalAP, func, data=None, cancelfunc=None):
        '''
            queue a new job
            Parameters:
                ent     : entity performing the job
                totalAP : total Action Points required to complete the job
                func    : the function that will be executed when the job
                          is completed
                data    : additional data needed by the job to be completed
                          e.g. the item entity being crafted
        '''
        rog.world().add_component(ent, cmp.QueuedAction(
            totalAP, func, data=data, cancelfunc=cancelfunc ))

    @classmethod
    def interrupt(cls, ent):  # set QueuedAction.interrupted = True
        assert(rog.world().has_component(ent, cmp.QueuedAction))
        rog.world().component_for_entity(
            ent, cmp.QueuedAction).interrupted = True
        
    @classmethod
    def resume(cls, ent): # turn a PausedAction into a QueuedAction
        world = rog.world()
        assert(world.has_component(ent, cmp.PausedAction))
        compo = world.component_for_entity(ent, cmp.PausedAction)
        world.add_component(ent, cmp.QueuedAction(  # copy all vars/
            compo.ap, compo.func, data=compo.data,  #/from one component/
            cancelfunc=compo.cancelfunc ))          #/to the other
        world.remove_component(ent, cmp.PausedAction)
        
    @classmethod
    def _pay(cls, ent, qa, actor, points):
        '''
            pay towards the AP debt to make progress in completing
                the action.
            Return True if the job is completed, or False otherwise.
            Parameters:
                _id : the id of the Action to pay for
                ap  : the amount of Action Points to pay towards the job
        '''
        qa.elapsed += 1 # track how many times we pay
        qa.ap -= points
        actor.ap -= points
        if qa.ap <=0: # finished job
            cls._finish(ent, qa)
        else:
            assert(actor.ap == 0) # TEST (should have spent all available AP towards this job if we got this far)
    
    @classmethod
    def _finish(cls, ent, qa): # successfully completed job
        ''' call the Action's function and remove the Action '''
        qa.func(ent, qa.data)
        self.world.remove_component(ent, cmp.QueuedAction)
        
    @classmethod
    def _interrupt(cls, ent, qa): # prematurely terminated job
        '''
            - give entity a PausedAction component with the qa info
                so that the information is not lost
            - the entity AI can decide what to do about this component
        '''
        # what happens when job is unfinished? Maybe makes a
        # half-finished crafting item? Half-eaten food object?
        if qa.cancelfunc:  #pass in qa.data, qa.ap; possibly modify qa ...
            qa.cancelfunc(ent, qa)  # ... before copying into PausedAction
        self.world.add_component(ent, cmp.PausedAction(qa))
        self.world.remove_component(ent, cmp.QueuedAction)
# end class
#

#
# Actors processor
# and Action Queues processor
#
class ActorsProcessor(esper.Processor):
    def process(self):
        world=self.world

        # give AP to all actors
        for ent,actor in world.get_component(cmp.Actor):
            if rog.on(ent,DEAD):
                actor.ap=0
                continue
            spd=max(MIN_SPD, rog.getms(ent, 'spd'))
            actor.ap = min(actor.ap + spd, spd)
        
        # Action Queues
        for ent, (qa, actor) in self.world.get_components(
            cmp.QueuedAction, cmp.Actor ):
            
            # process interruptions and cancelled / paused jobs
            if qa.interrupted:
                ActionQueue._interrupt(ent, qa)
                continue
            if actor.ap <= 0:
                continue
            
            # proceed with the job
            # spend as much AP as we can / as we need
            # automatically finishes the job if applicable
            points = min(actor.ap, qa.ap)
            ActionQueue._pay(ent, qa, actor, points)
        
        # If no Action Queued, then continue with turn as normal #
        
        # NPC / AI / computer turn
        for ent,(actor, _ai) in world.get_components(
            cmp.Actor, cmp.AI ):
            while actor.ap > 0:
                _ai.func(ent)
# end class


            
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
    # NOTE: This is not the processor -- it's a helper class
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
        return cls.fires[x][y]
    
    # heat
    @classmethod
    def init_heat(cls):
        cls.heat = np.full((ROOMW,ROOMH,), fill_value=0, dtype=np.float64)
    @classmethod
    def tempat(cls, x,y): # get temperature at pos x,y
        return cls.heat[x][y]
    @classmethod
    def add_heat(cls,x,y,temp): cls.heat[x][y] += temp
    @classmethod
    def remove_heat(cls,x,y,temp): cls.heat[x][y] -= temp
    
    # fuel
    @classmethod
    def init_fuel(cls):
        cls.fuel = np.full((ROOMW,ROOMH,), fill_value=0, dtype=np.int16)
    @classmethod
    def add_fuel(cls,x,y,fuel): cls.fuel[x][y] += fuel
    @classmethod
    def remove_fuel(cls,x,y,fuel):
        cls.fuel[x][y] = max(0, cls.fuel[x][y] - fuel)
    
    # heat sources
    @classmethod
    def init_heat_sources(cls):
        cls.heat_sources = np.full(
            (ROOMW,ROOMH,), fill_value=0, dtype=np.float64
            )
    @classmethod
    def add_heat_source(cls,x,y,temp): cls.heat_sources[x][y] += temp
    @classmethod
    def remove_heat_source(cls,x,y,temp): cls.heat_sources[x][y] -= temp
    
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
# end class
#
class FireProcessor(esper.Processor):
    
    def __init__(self):
        self.clist=[] # coordinate list of fires
        self.lights={} # dict of lights created by fires
    
    def process(self):
        pass
##        world = self.world
##        
##        # get fuel amount
##            # for now this should be fine; only update this if
##            # performance from this particular 3 lines of code
##            # is seriously something to be concerned about.
##        Fires.init_fuel()
##        for ent, compos in world.get_components(cmp.Fuel, cmp.Position):
##            fuel, pos = compos
##            # apply fuel multipliers
##            # mass affects fuel value
##            mass = rog.getms(ent,"mass") / MULT_MASS
##            # add fuel to the grid
##            Fires.add_fuel(pos.x, pos.y, round(fuel.fuel * mass))
##            
##        # disperse heat, handle fires
##        dispersion=Fires.get_disperse(rog.wind_force(),rog.wind_direction())
##        Fires.heat += Fires.heat_sources # heat sources radiating heat
##        Fires.heat += Fires.fires * Fires.fuel # fires creating heat
##        Fires.heat += ENV_DELTA_HEAT # passive heat loss (or gain)
##        Fires.heat = scipy.signal.convolve2d( # Spread heat to adjacent cells.
##            Fires.heat, dispersion, mode='same', boundary='fill', fillvalue=0
##        )
##        
##        # get the fires grid
##        Fires.fires = (Fires.heat >= FIRE_THRESHOLD) * (Fires.fuel > 0) # get grid of fires (true/false)
##        
##        # limits
##        np.clip(Fires.heat, HEATMIN, HEATMAX, out=Fires.heat) # min/max the heat grid
##        
##        # get list of x,y coordinate pairs of cells that are on fire
##        oldlist=self.clist.copy() # old list = the list before we update it.
##        self.clist=np.stack(Fires.fires.nonzero(), axis = 1) # coord. list
##        oldset=set() # old coordinate index set from last iteration
##        for item in oldlist:
##            y, x = item
##            oldset.add(Fires.Index(x,y))
##        cset=set() # current coordinate index set
##        for item in self.clist:
##            y, x = item
##            cset.add(Fires.Index(x,y))
##        
##        # get the fires which are new since last iteration
##        newfires = [i for i in cset if i not in oldset]
##        # get the fires which have gone out since last iteration
##        outfires = [i for i in oldset if i not in cset]
##        
##        # add new lights where there are new fires
##        for fireID in newfires:
##            x, y = Fires.Coords(fireID)
####            print("new fire at pos. x={} y={}".format(x,y))
##            light=rog.create_light(x,y, FIRE_LIGHT, owner=None)
##            self.lights.update({fireID : light})
##        # release lights from fires that have gone out
##        for fireID in outfires:
##            x, y = Fires.Coords(fireID)
####            print("fire put out at pos. x={} y={}".format(x,y))
##            rog.release_light(self.lights[fireID])
##            del self.lights[fireID]
# end class


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
# end class

# Fluid Processor Fluids Processor
class FluidProcessor(esper.Processor):
    def process(self):
        Fluids.flow()
##    def fluidsat(self,x,y):
##        return self._fluids.get((x,y,), ())
# end class


    
#
# Stats Upkeep processor
#

class UpkeepProcessor(esper.Processor): # TODO: test this
    def process(self):
        for ent, (stats, creat) in self.world.get_components(
            cmp.Stats, cmp.Creature ):
            # just query some components that match entities
            # that will be needing stamina regen
##            print("mp regen ", rog.getms(ent, 'mpregen'))
            rog.givemp(ent, rog.getms(ent, 'mpregen')//MULT_STATS)



#
# Status
#

class Status:
    @classmethod
    def add(self, ent, component, t=-1, q=None):
        '''
            add a status if entity doesn't already have that status
            **MUST NOT set the DIRTYSTATS flag.
        '''
        if rog.world().has_component(ent, component): return False
        status_str = ""
        #attribute modifiers, aux. effects, message (based on status type)
        if component is cmp.StatusHot:
            status_str = " becomes hyperthermic"
        elif component is cmp.StatusBurn:
            status_str = " begins smoldering"
        elif component is cmp.StatusChilly:
            status_str = " becomes cold"
        elif component is cmp.StatusCold:
            status_str = " becomes hypothermic"
        elif component is cmp.StatusFrozen:
            status_str = " becomes frozen"
            rog.damage(ent, rog.getms(ent, 'hpmax') * FREEZE_DMG_PC)
        elif component is cmp.StatusAcid:
            status_str = " begins corroding"
        elif component is cmp.StatusBlinded:
            status_str = " becomes blinded"
        elif component is cmp.StatusDeafened:
            status_str = " becomes deafened"
        elif component is cmp.StatusIrritated:
            status_str = " becomes irritated"
        elif component is cmp.StatusBleed:
            status_str = " begins bleeding"
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
            status_str = " puts on a frightening display"
        elif component is cmp.StatusFrightened:
            status_str = " becomes frightened"
        elif component is cmp.StatusHaste:
            status_str = "'s movements speed up"
        elif component is cmp.StatusSlow:
            status_str = "'s movements slow"
        elif component is cmp.StatusDrunk:
            status_str = " becomes inebriated"
        elif component is cmp.StatusHazy:
            gender=rog.world().component_for_entity(ent, cmp.Gender)
            status_str = " begins slurring {} speech".format(gender.pronouns[2])
        #if status_str:
            #"{}{}{}".format(name.title, name.name, status_str)

        # TODO: events to display the messages
        
        if t==-1: # use the default time value for the component
            if q: # status components with quality variable
                rog.world().add_component(ent, component(q=q))
            else:
                rog.world().add_component(ent, component())
        else: # pass in the time value
            if q: # status components with quality variable
                rog.world().add_component(ent, component(t=t, q=q))
            else:
                rog.world().add_component(ent, component(t=t))
        return True
        
    @classmethod
    def remove(self, ent, component):
        if not rog.world().has_component(ent, component): return False
        status_str = ""
        #attribute modifiers, aux. effects, message (based on status type)
        if component is cmp.StatusHaste:
            status_str = "'s movements slow"
        elif component is cmp.StatusSlow:
            status_str = "'s movements speed up"
        #if status_str:
            #"{}{}{}".format(name.title, name.name, status_str)
        rog.world().remove_component(ent, component)
        return True
    
    @classmethod
    def remove_all(self, ent): # TODO: finish this
        for status, component in cmp.STATUSES.items():
            if not rog.world().has_component(ent, component):
                continue
            #attribute modifiers
            #auxiliary effects
            #message
            rog.world().remove_component(ent, component)
#
# Status Processor
#

# Processes statuses once per turn.

class StatusProcessor(esper.Processor):
    def process(self):
        world = self.world

        # fire burning
        for ent, (status, meters) in world.get_components(
            cmp.StatusBurn, cmp.Meters):
            status.timer -= 1
            if (status.timer == 0): #temporary? When should fire go out?
                Status.remove(ent, cmp.StatusBurn)
                continue
            rog.damage(ent, 1)

        # frozen ice
        for ent, (status, meters) in world.get_components(
            cmp.StatusFrozen, cmp.Meters):
            status.timer -= 1
            if (status.timer == 0):
                Status.remove(ent, cmp.StatusCold)
                continue
            
        # acid
        for ent, status in world.get_component(
            cmp.StatusAcid ):
            status.timer -= 1
            rog.damage(ent, ACID_DAMAGE)
            if status.timer == 0:
                Status.remove(ent, cmp.StatusAcid)
                continue
            
        # blind
        for ent, status in world.get_component(
            cmp.StatusBlinded ):
            status.timer -= 1
            if status.timer == 0:
                Status.remove(ent, cmp.StatusBlinded)
                continue
            
        # deaf
        for ent, status in world.get_component(
            cmp.StatusDeafened ):
            status.timer -= 1
            if status.timer == 0:
                Status.remove(ent, cmp.StatusDeafened)
                continue
            
        # irritated
        for ent, status in world.get_component(
            cmp.StatusIrritated ):
            status.timer -= 1
            if status.timer == 0:
                Status.remove(ent, cmp.StatusIrritated)
                continue
            
        # bleed
        for ent, (status, body) in world.get_components(
            cmp.StatusBleed, cmp.Body ):
            body.blood -= bleed.quality
            status.timer -= 1
            if status.timer == 0:
                Status.remove(ent, cmp.StatusBleed)
                continue
            
        # pain
        for ent, status in world.get_component(
            cmp.StatusPain ):
            status.timer -= 1
            if status.timer == 0:
                Status.remove(ent, cmp.StatusPain)
                continue
            
        # paralyzed
        for ent, status in world.get_component(
            cmp.StatusParalyzed ):
            status.timer -= 1
            if status.timer == 0:
                Status.remove(ent, cmp.StatusParalyzed)
                continue
            
        # sick
        for ent, status in world.get_component(
            cmp.StatusSick ):
            status.timer -= 1
            if status.timer == 0:
                Status.remove(ent, cmp.StatusSick)
                continue
            
        # vomit
        for ent, status in world.get_component(
            cmp.StatusVomit ):
            status.timer -= 1
            if status.timer == 0:
                Status.remove(ent, cmp.StatusVomit)
                continue
            
        # cough
        for ent, status in world.get_component(
            cmp.StatusCough ):
            status.timer -= 1
            if status.timer == 0:
                Status.remove(ent, cmp.StatusCough)
                continue
            
        # sprint
        for ent, status in world.get_component(
            cmp.StatusSprint ):
            status.timer -= 1
            if status.timer == 0:
                Status.remove(ent, cmp.StatusSprint)
                continue
            
        # Frightening
        for ent, status in world.get_component(
            cmp.StatusFrightening ):
            status.timer -= 1
            if status.timer == 0:
                Status.remove(ent, cmp.StatusFrightening)
                continue
            
        # Frightened
        for ent, status in world.get_component(
            cmp.StatusFrightened ):
            status.timer -= 1
            if status.timer == 0:
                Status.remove(ent, cmp.StatusFrightened)
                continue
            
        # Panicking
        for ent, status in world.get_component(
            cmp.StatusPanic ):
            status.timer -= 1
            if status.timer == 0:
                Status.remove(ent, cmp.StatusPanic)
                continue
            
        # Hasty hastey
        for ent, status in world.get_component(
            cmp.StatusHaste ):
            status.timer -= 1
            if status.timer == 0:
                Status.remove(ent, cmp.StatusHaste)
                continue
            
        # slowed
        for ent, status in world.get_component(
            cmp.StatusSlow ):
            status.timer -= 1
            if status.timer == 0:
                Status.remove(ent, cmp.StatusSlow)
                continue
            
        # drunk
        for ent, status in world.get_component(
            cmp.StatusDrunk ):
            status.timer -= 1
            if status.timer == 0:
                Status.remove(ent, cmp.StatusDrunk)
                continue
            
        # hazy (head injury, sickness, stroke, blood loss, bloody pissed, etc.)
        for ent, status in world.get_component(
            cmp.StatusHazy ):
            status.timer -= 1
            if status.timer == 0:
                Status.remove(ent, cmp.StatusHazy)
                continue
            
        # sweat sweating
        for ent, (status, meters) in world.get_components(
            cmp.StatusSweat, cmp.Meters ):
            meters.temp -= SWEAT_TEMP_LOSS
            status.timer -= 1
            if status.timer == 0:
                Status.remove(ent, cmp.StatusSweat)
                continue
            
        # shivering
        for ent, (status, meters) in world.get_components(
            cmp.StatusShiver, cmp.Meters ):
            meters.temp += SHIVER_TEMP_GAIN
            status.timer -= 1
            if status.timer == 0:
                Status.remove(ent, cmp.StatusShiver)
                continue
            
        # emaciated
        for ent, status in world.get_component(
            cmp.StatusEmaciated ):
            status.timer -= 1
            if status.timer == 0:
                Status.remove(ent, cmp.StatusEmaciated)
                continue
            
        # dehydrated
        for ent, status in world.get_component(
            cmp.StatusDehydrated ):
            status.timer -= 1
            if status.timer == 0:
                Status.remove(ent, cmp.StatusDehydrated)
                continue
            
        # tired
        for ent, status in world.get_component(
            cmp.StatusTired ):
            status.timer -= 1
            if status.timer == 0:
                Status.remove(ent, cmp.StatusTired)
                continue
            
        #-------------------------------------------------#
        # Quantity Status Effects (statuses w/ no timers) #
        #-------------------------------------------------#
            
        # digestion / digesting
        for ent, (status, body) in world.get_components(
            cmp.StatusDigest, cmp.Body ): #, cmp.Stats
            # quantity out -> clear status
            if (status.satiation <= 0 and status.hydration <= 0):
                Status.remove(ent, cmp.StatusDigest)
                continue
            # food
            if status.satiation > 0:
                amount = min(METABOLIC_RATE_FOOD.get(body.plan, 10),
                             status.satiation)
                status.satiation -= amount
                body.satiation += amount
            # water
            if status.hydration > 0:
                amount = min(METABOLIC_RATE_WATER.get(body.plan, 10),
                             status.hydration)
                status.hydration -= amount
                body.hydration += amount
# end class


#
# Status Meters
#
    #Status Meters are the build-up counters for status effects like fire, sickness, etc.
        
class MetersProcessor(esper.Processor):
    def _getambd(dt, mass):
        ''' get the amount of ambient temperature change
            based on how much the entity's temperature changed.
            The more massive, the greater the effect. '''
        return -dt * mass / MULT_MASS
    #
    def process(self):

        # TODO: interface heat exchange btn entities equipping or
        #  holding items in inventory
        #  I think we need a component for Equipped or InContainer to handle this.
        
        '''
            interface with environment
                (e.g. in cases of heat exchange with the air)
            and take effects from internal state
        '''
        for ent,(meters,pos) in self.world.get_components(
            cmp.Meters, cmp.Position ):
##            ambient_temp = Fires.tempat(pos.x, pos.y)
            
            # TODO: FIX THIS!!!!!!!
            #print(thing.name," is exchanging heat with the environment...") #TESTING
            # cool down temperature meter if not currently burning
##            if (abs(meters.temp - ambient_temp) >= 1):
##                # TODO: take insulation into account for deltatemp
##                #   as well as the actual difference in temperature
##            # TODO: also take into account the material of the entity (metal is faster to gain/lose heat)
##                deltatemp = rog.sign(ambient_temp - meters.temp)
##                meters.temp = meters.temp + deltatemp
##                ambientdelta = _getambd(deltatemp, rog.getms(ent,"mass"))
##                Fires.add_heat(pos.x, pos.y, ambientdelta)
####                print("adding heat {} to pos {} {} (mass {}) (heat={})".format(ambientdelta, pos.x, pos.y, rog.getms(ent,"mass"), Fires.tempat(pos.x,pos.y)))
##                if (not rog.get_status(ent, cmp.StatusFire) and
##                    meters.temp >= FIRE_THRESHOLD):
##                    rog.set_status(ent, cmp.StatusFire)
##                elif (not rog.get_status(ent, cmp.StatusFrozen) and
##                    meters.temp <= FREEZE_THRESHOLD):
##                    rog.set_status(ent, cmp.StatusFrozen)
            #
            
        for ent,meters in self.world.get_component(
            cmp.Meters ):
            if (meters.sick > 0):
                rog.make(ent, DIRTYSTATS)
                meters.sick = max(0, meters.sick - BIO_METERLOSS)
            if (meters.expo > 0):
                rog.make(ent, DIRTYSTATS)
                meters.expo = max(0, meters.expo - CHEM_METERLOSS)
            if (meters.pain > 0):
                rog.make(ent, DIRTYSTATS)
                meters.pain = max(0, meters.pain - PAIN_METERLOSS)
            if (meters.fear > 0):
                rog.make(ent, DIRTYSTATS)
                meters.fear = max(0, meters.fear - FEAR_METERLOSS)
            if (meters.bleed > 0):
                rog.make(ent, DIRTYSTATS)
                meters.bleed = max(0, meters.bleed - BLEED_METERLOSS)
            # rads meter
# end class



#
# Body Maintainence Processor / Body Processor
#

# Ran every turn.
# This processor focuses on critical and hyper-critical body conditions.
# HomeostasisProcessor worries about regulating less extreme conditions.

class BodyProcessor(esper.Processor):
    def process(self):
        for ent, (body, meters) in world.get_components(
            cmp.Body, cmp.Meters):
            
            # get body temperature information based on body plan
            bodytemp, plus, minus = BODY_TEMP.get[body.plan]
            bloodpc, bloodratio = BODY_BLOOD.get[body.plan]
            
            # too thirsty? (too little hydration?/too dehydrated?)
            if body.hydration <= body.hydrationMax*0.9: # hyper-critical
                entities.dehydrate(ent)
            # too hungry? (too little calories?)
            if body.satiation <= 0: # hyper-critical
                entities.starve(ent)
            # too hot?
            if meters.temp > bodytemp + plus: # hyper-critical
                rog.set_status(ent, cmp.StatusHyperthermia())
            # too cold?
            if meters.temp < bodytemp + minus: # hyper-critical
                rog.set_status(ent, cmp.StatusHypothermia())
            # too little blood?
            if body.blood <= body.bloodMax * bloodratio: # hyper-critical
                rog.set_status(ent, cmp.StatusExsanguination())
            elif body.blood <= body.bloodMax * ( # critical
                bloodratio + (1 - bloodratio)*0.5):
                rog.set_status(ent, cmp.StatusHazy())
# end class
                

#
# Homeostasis Processor
#

# Ran once every few turns or so.
# Concerned with body processes that are sub-critical.
# BodyProcessor is the critical body processes processor.

class HomeostasisProcessor(esper.Processor):
    def process(self):
        world = self.world
        for ent, (body, meters) in world.get_components(
            cmp.Body, cmp.Meters):
            
            # maintain heat equilibrium
            meters = self.world.component_for_entity(ent, cmp.Meters)
            if meters.temp > BODY_TEMP+1:
                rog.set_status(ent, cmp.StatusSweat())
            elif meters.temp < BODY_TEMP-1:
                rog.set_status(ent, cmp.StatusShiver())

            # TODO: Hot and Chilly/Cold statuses
            
            # digestion: get calories (satiation) from food consumed

            # TODO: when you eat, get StatusDigest status
            
        for ent, (body, status) in world.get_components(
            cmp.Body, cmp.StatusDigest):
            
            # satiation ++, caloriesAvailableInFood --
            metabolic_rate = stats.mass / MULT_MASS
            caloric_value = min(metabolic_rate, status.quantity)
            status.quantity -= caloric_value
            body.satiation += caloric_value
            # excess Calories -> fat
            if body.satiation > body.satiationMax:
                rog.set_status(ent, cmp.StatusFull())
                # 9 Calories per gram of fat (1/9 == 0.1111...)
##                df = body.satiationMax - body.satiation
                caltofat = 1000 #df / MULT_MASS *0.11111111
                body.bodyfat += caltofat*0.5
                body.satiation -= caltofat
# end class


        










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
                    

        



