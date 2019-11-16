'''
    fluids.py
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

# FLUIDS #

 # TODO : implement fluids.


class Data:
    '''
        Fluid data
        each type of fluid has 1 unique fluid data object.
    '''

    def __init__(self, x,y, t=T_FLUID, name=None,
                 color=None, material=None, d=1,v=1,kg=1,
                 burns=False, putsout=False):

        self._type=t
        self.name=name
        self.color=color
        self.material=material
        self.density=d
        self.viscosity=v
        self.mass=kg
        self.flammable=burns
        self.extinguish=putsout  #does it put out fires?

##
##class Fluid:
##
##    def __init__(self, x,y):
##        super(Fluid, self).__init__(x, y)
##        self.dic={}
##        self.size=0 #total quantity of fluid in this tile
##
##    def getData(self, stat):    #get a particular stat about the fluid
##        return FLUIDS[self.name].__dict__[stat]
##    
##    def clear(self):            #completely remove all fluids from the tile
##        self.dic={}
##        self.size=0
##    
##    def add(self, name, quantity=1):
##        newQuant = self.dic.get(name, 0) + quantity
##        self.dic.update({name : newQuant})
##        self.size += quantity
##        
##        '''floodFill = False
##        if self.size + quantity > MAX_FLUID_IN_TILE:
##            quantity = MAX_FLUID_IN_TILE - self.size
##            floodFill = True #partial floodfill / mixing
##            #how should the fluids behave when you "inject" a new fluid into a full lake of water, etc.?
##            #regular floodfill will not cut it
##            #maybe just replace the current fluid with the new fluid to keep it simple.
##            '''
##
##        '''if floodFill:
##            #do flood fill algo.
##            #this is going to also have to run a cellular automata to distribute different types of fluids
##            return'''
##
##    def removeType(self, name, quantity=1):
##        if self.size > 0:
##            curQuant = self.dic.get(name, 0)
##            newQuant = max(0, curQuant - quantity)
##            diff = curQuant - newQuant
##            if not diff:     #no fluid of that type to remove
##                return
##            self.size -= diff
##            if newQuant != 0:
##                self.dic.update({name : newQuant})
##            else:
##                #we've run out of this type of fluid
##                self.dic.remove(name)
        

##
##def simulate_flow():
###idea: if any fluid tiles contain more than the maximum allowed,
##    #always flow outward using flood fill if necessary.
##    for fluid in rog.list_fluids():
##        #simultaneous cellular automata
##        newMap = TileMap(self.w,self.h)
##        newMap.COPY(rog.map())
##        #define some functions to reduce duplicate code
##        def _doYourThing(x,y,num,nValues): # alter a tile or keep it the same based on input
##            if nValues[num]==-1:
##                newMap.tile_change(x,y,offChar)
##            elif nValues[num]==1:
##                newMap.tile_change(x,y,onChar)
##        for ii in range(iterations):
##            for x in range(self.w):
##                for y in range(self.h):
##                    num = newMap.countNeighbors(x,y, onChar)
##                    _doYourThing(x,y,num,nValues)
##        self.COPY(newMap)
##
