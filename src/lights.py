'''
    lights
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

import libtcodpy as libtcod

from const import *
import rogue as rog
import maths
import observer


class Light(observer.Observer):
    '''
        casts and uncasts light
            by adding or subtracting values from a lightmap
    '''

    def __init__(self, x,y, lum, owner=None):
        super(Light, self).__init__()

        self.x=x
        self.y=y
        self.lum=lum
        self.fov_map=None
        self.lit_tiles=[]
        self.owner=owner
        self.shone=False

    def update(self, *args,**kwargs):
        if not args: return
        attr,val=args
        if (attr == "x" or attr == "y"):
            self.reposition(self.owner.x, self.owner.y)

    #shine
    # increases the lightmap values.
    def shine(self):        # add light to the lightmap
        if (self.shone):    # must unshine before shining again.
            print("ERROR: shine failed: shone==True")
            return False
        self.shone=True
        #get the tiles we can see and lighten them up
        libtcod.map_compute_fov(
            self.fov_map, self.x,self.y, self.lum,
            light_walls = True, algo=libtcod.FOV_RESTRICTIVE)
        rang = self.lum
        for x in     range( max(0, self.x-rang), min(ROOMW, self.x+rang+1) ):
            for y in range( max(0, self.y-rang), min(ROOMH, self.y+rang+1) ):
                
                if ( rog.in_range(self.x,self.y, x,y, rang)
                        and libtcod.map_is_in_fov(self.fov_map, x,y) ):
                    dist=maths.dist(self.x,self.y, x,y)
                    value=round(self.lum - dist)
                    if value > 0:
                        self.add_tile(x,y, value )
                        rog.tile_lighten(x,y,value)
        return True     #success
    #

    def unshine(self):      # revert tiles to previous light values
        if (self.shone==False): #cannot undo what has not been done
            print("ERROR: unshine failed: shone==False")
            return False #failed
        self.shone=False
        #darken all tiles that we lightened
        for tile in self.lit_tiles:
            x,y,value=tile
            rog.tile_darken(x,y,value)
        self.lit_tiles=[]
        return True     #success

    #move the light to a new position, changing the lightmap
    def reposition(self, x,y):
        self.unshine()
        rog.grid_lights_remove(self)
        self.x=x; self.y=y;
        rog.grid_lights_insert(self)
        self.shine()

    def add_tile(self,x,y,value):
        self.lit_tiles.append( (x,y,value,) )


'''
# TODO: this should go in entities
TORCHES={
    #  name/    char,light,Turns,color
    'torch'     : (';',6, 1000,'gold'),
    'brand'     : (';',2, 50, 'gold'),
}

def create_torch(name, x,y):
    torch=thing.Thing()
    data=TORCHES[name]
    torch.type=data[0]
    torch.mask=data[0]
    torch.name=name
    torch.x=x
    torch.y=y
    torch.lum=data[1]
    torch.color=COL['white']
'''
    
    



        
