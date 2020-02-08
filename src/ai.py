'''
    ai.py
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

import math

from const import *
import rogue as rog
import components as cmp
import maths
import action
import dice




##def tick(ent): # handled by a processor now
##    world = rog.world()
##    if not world.has_component(ent, cmp.AI): return
##    aiFunc = world.component_for_entity(ent, cmp.AI).func
##    actor = world.component_for_entity(ent, cmp.Actor)
##    while actor.ap > 0:
##        aiFunc(ent)

class Desires():
    # stores monster's desires to move in each direction
    def __init__(self, default=0, wander=7):
        self.data=[
            [ default + dice.roll(wander) for j in range(3)]
            for i in range(3)
        ]
    def get(self,x,y):  return self.data[x+1][y+1]
    def add_for(self, x,y, val):        self.data[x+1] [y+1]  += val
    def add_against(self, x,y, val):
        # add desire to move AWAY from a direction. Implemented as
        # a positive desire in the opposite direction rather than
        # a negative desire in the given direction.
        self.data[-x+1][-y+1] += val


def stateless(bot):
    '''
        Dumb temporary NPC controller function
        implementing a simple 8-directional desire system
    '''
    
    world=rog.world()
    desires=Desires(wander=7)
    sight=rog.getms(bot, "sight")
    pos=world.component_for_entity(bot, cmp.Position)
    botCreature=world.component_for_entity(bot, cmp.Creature)
##    botType=world.component_for_entity(bot, cmp.Draw).char #should not depend on draw component
    
    # Where should this go????
##    rog.run_fov_manager(bot) # moved to can_see
    
    
    # TODO: write this function
    def isFoe(myFaction, theirFaction):
        return True

    # TODO: re-implement listening
    # listen to events
    '''lis=rog.listen(bot)
    if lis:
        for ev in lis:
            if rog.can_see(bot,ev.x,ev.y):
                continue
            # hearing
            if not ev.volume: continue
            if rog.can_hear(bot, ev.x,ev.y, ev.volume):
                interest=5
                _add_desire_direction(
                    desires, bot.x,bot.y, ev.x,ev.y, interest)
        rog.clear_listen_events(bot)'''
    
    # iterate through each tile in sight and see what is there...
    # is there a better way to do this?
    # This code is a little slow.    
    for x in range(     pos.x - sight,  pos.x + sight + 1 ):
        for y in range( pos.y - sight,  pos.y + sight + 1 ):
            if (not rog.is_in_grid(x,y) # out of bounds
                    or (x == pos.x and y == pos.y) ): # ignore self
                continue
            if not rog.can_see(bot,x,y,sight): continue # can't see it
            
            here = rog.thingat(x,y)
            
            if here:
                isCreature = world.has_component(here, cmp.Creature)
                # decide what it is and what to do about it
                if isCreature:
                    creature = world.component_for_entity(here, cmp.Creature)
                    if rog.on(here,DEAD): continue # no interest in dead things
                    
                    interest=0
                    
                    #desire to fight
                    if creature.faction == FACT_ROGUE:
                        interest=1000
                    #grouping behavior
                    elif creature.faction == botCreature.faction:
                        interest = 5
                        
                    if (interest > 0):
                        _add_desire_direction(
                            desires, pos.x,pos.y, x,y, interest
                            )
                    elif (interest < 0):
                        _add_fear_direction(
                            desires, pos.x,pos.y, x,y, interest
                            )
                #if thing is inanimate
                else:
                    #food desire if hungry
                    #treasure desire
                    pass
                
    # pick the direction it wants to move in the most
    highest=-999
    for i in range(3):
        for j in range(3):
            new=desires.get(j-1, i-1)
            if new > highest:
                highest=new
                coords=(j-1, i-1,)
    dx, dy =coords
    xto=pos.x + dx
    yto=pos.y + dy
    
    # out of bounds
    if not rog.is_in_grid(xto, yto):
        return
    
    # fight if there is a foe present
    mon = rog.monat(xto, yto)
    if (mon and mon is not bot):
        monFaction = world.component_for_entity(mon, cmp.Creature).faction
        if isFoe(botCreature.faction, monFaction):
            action.fight(bot, mon)
            return
    # or move
    elif not rog.solidat(xto, yto):
        if action.move(bot, dx,dy):
            return

    # if no action was done, just wait
    action.wait(bot)



#LOCAL FUNCTIONS

def _add_desire_direction(desires, xf,yf, xt,yt, interest):
    # desire to move in the given direction
    # desires = Desires object instance
    # interest = amount that it cares about moving in this direction
    if not interest: return
    dx,dy = _get_dir_xy(xf,yf,xt,yt)
    desires.add_for(dx,dy, interest)
def _add_fear_direction(desires, xf,yf, xt,yt, interest):
    # desire to move in the opposite direction
    # desires = Desires object instance
    # interest = amount that it cares about moving away from this direction
    if not interest: return
    dx,dy = _get_dir_xy(xf,yf,xt,yt)
    desires.add_against(dx,dy, interest)
def _get_dir_xy(x1,y1,x2,y2):
    # return the direction from (xf,yf) to (xt,yt)
    rads=maths.pdir(x1,y1, x2,y2)
    dx=round(math.cos(rads))
    dy=round(math.sin(rads))
    return (dx,dy,)
    

















