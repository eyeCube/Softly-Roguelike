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

import math
import libtcodpy as libtcod

from const import *
import rogue as rog
import maths
import observer


'''
    Light
    casts and uncasts light
        by adding or subtracting values from a lightmap
'''
class Light(observer.Observer):
# "... the equation for the apparent brightness of a light source is given
#   by the luminosity divided by the surface area of a sphere with radius
#   equal to your distance from the light source ..."
#   ~sauce: https://www.e-education.psu.edu/astro801/content/l4_p4.html
#   F = L / 4 * pi * d^2
#   apparent brightness = Lumosity / 4*pi*d^2
    
    LOGBASE=2
    
    def __init__(self, x,y, lum, owner=None):
        super(Light, self).__init__()

        self.x=x
        self.y=y
        self.lum=int(lum) # luminosity: actual brightness (not the range of the light)
        self.fovID=None
        self.lit_tiles=[]
        self.owner=owner
        self.shone=False
    
    # get perceived brightness or how bright a tile appears
    # based on how much light is hitting the tile per square meter (lux)
    # (lux is the value stored in the lightmap).
    # Example values:
    #   perceived average brightness of sunlight: 10
    @classmethod
    def perceivedBrightness(cls, lux: int) -> int:
        return int(math.log2(lux)) # LOGBASE==2 so we use log base 2
    
    def add_tile(self,x,y,lux):
        self.lit_tiles.append( (x,y,lux,) )

    def update(self, *args,**kwargs):
        if not args: return
        attr,val=args
        if (attr == "x" or attr == "y"):
            self.reposition(self.owner.x, self.owner.y)

    #shine
    # increases the lightmap values.
    def shine(self): # shine light on environment; add light to lightmap
        assert(self.shone==False)   # cannot shine if we already did
        self.shone=True
        rang = self.getLumens(self.lum)
        libtcod.map_compute_fov( # Get the tiles we can see
            rog.getfovmap(self.fovID), self.x,self.y, rang,
            light_walls = True, algo=libtcod.FOV_RESTRICTIVE
            )
        for x in     range( max(0, self.x-rang), min(ROOMW, self.x+rang+1) ):
            for y in range( max(0, self.y-rang), min(ROOMH, self.y+rang+1) ):
                
                if ( rog.in_range(self.x,self.y, x,y, rang)
                        and libtcod.map_is_in_fov(
                            rog.getfovmap(self.fovID), x,y)
                    ):
                    dist=maths.dist(self.x,self.y, x,y)
                    # F = L / 4 * pi * d^2 (formula for light dispersion)
                    lux = self.lum // (12.5663706144 * (dist**2))
                    if lux:
                        self.add_tile(x,y,lux)
                        rog.tile_lighten(x,y,lux)
        # end for
        return True     #success
    #
    
    # remove light (undo shine / reverse of the shine function)
    def unshine(self):      # revert tiles to previous light values ...
        # ... before this instance of a light shone on the environment.
        assert(self.shone) # must shine before unshining
        self.shone=False
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
# end class

class EnvLight: # Environment Light | Ambient Light | EnvironmentLight | AmbientLight
    def __init__(self, lux, owner=None):
        self.lux=lux
        self.owner=owner

    def shine(self):
        for x in range(ROOMW):
            for y in range(ROOMH):
                rog.tile_lighten(x, y, self.lux)
    def unshine(self):
        for x in range(ROOMW):
            for y in range(ROOMH):
                rog.tile_darken(x, y, self.lux)
# end class


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
    
    



        
