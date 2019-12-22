'''
    tilemap.py
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

    TODO: learn "dirty" updating!!!!!!!
'''

import time
import numpy as np
import tcod as libtcod
import random
import math
from dataclasses import dataclass

from const import *
import rogue as rog
import components as cmp
from colors import COLORS as COL
import levelgen
import maths
import misc
import dice




@dataclass
class Tile():
    '''
    Tiles are simple objects that can be minimally interacted with
       without much overhead.
       There is only one instance for each type of tile.
           References to a particular tile on the grid look at the unique
           instance created in the TILES constant.
    '''
    char:       str     #ASCII character to represent the tile
    fg:         str     #foreground color
    bg:         str     #background color
    nrg_enter:  int     #action points it takes to enter this tile
    nrg_leave:  int     #action points it takes to exit this tile
    opaque:     bool    #False if you can see through it
    dampen:     int     #volume dampen amount


# BUG: costLeave not working right. Rough next to wall allows you to walk into the wall. Related to the cost calculation for moving (probably).

TILES={         #                 fgcolor ,  bg,costEnter,Leave, opaque,damp
    FLOOR       : Tile(FLOOR,     'neutral', 'deep',    100,0,  False,1,),
    ROUGH       : Tile(ROUGH,     'dkgreen', 'blue', 150,50,False,1,),
    SHRUB       : Tile(SHRUB,     'green',  'vdkgreen', 300,100,False,1,),
    BRAMBLE     : Tile(BRAMBLE,   'green',  'vdkgreen', 500,200,False,1,),
    JUNGLE      : Tile(JUNGLE,    'dkgreen','vdkgreen',1200,300,False,2,),
    JUNGLE2     : Tile(JUNGLE2,   'dkgreen','vdkgreen',1200,300,False,2,),
    # TODO: change costEnter to 0 for WALL! This is TEMPORARY for TESTING LEVEL GEN
    WALL        : Tile(WALL,      'dkred', 'orange',   110,  0,  True, 50,),
    STAIRDOWN   : Tile(STAIRDOWN, 'accent', 'purple',  100,0,  False,1,),
    STAIRUP     : Tile(STAIRUP,   'accent', 'purple',  100,0,  False,1,),
    DOOROPEN    : Tile(DOOROPEN,  'yellow', 'brown',   100,0,  False,1,),
    DOORCLOSED  : Tile(DOORCLOSED,'yellow', 'brown',   0,0,    True,5,),
    VAULTOPEN   : Tile(VAULTOPEN, 'metal', 'deep',    100,0,  False,1,),
    VAULTCLOSED : Tile(VAULTCLOSED,'metal', 'deep',   0,0,    True,100,),
    }
    # these should prolly be entities, not tiles.
##    FUNGUS      : Tile(FUNGUS,    'purple', 'vdkgreen',100,20, False,1,),
##    SHROOM      : Tile(SHROOM,    'green', 'vdkgreen', 150,20,  True,2,),
    #water is now a fluid, not a tile...
    #PUDDLE      : Tile(PUDDLE,    'blue',   'deep',     100,10,  True,2,),
    #SHALLOW     : Tile(SHALLOW,   'blue',  'dkblue',     100,25,  True,2,),
    #WATER       : Tile(WATER,     'trueblue','dkblue',  100,50,  True,2,),
    #DEEPWATER   : Tile(DEEPWATER, 'dkblue', 'deep',     100,100,  True,2,),
     

class TileMap():
    '''
The grid class that stores data about:
    terrain, things, lights,   -fluids?? -fires??
    grid_things must be in a particular order:
        creature goes on top
            * currently only one creature allowed per tile
        inanimate things below that.

This class currently also handles rendering.
TODO: move rendering code to a new, different class.
    '''
    
    # TODO: do not use put_char or map_set_properties, they are deprecated in the newest version of tcod.
    
    def __init__(self,w,h):
        '''
            Note: see func "init_specialGrids",
                and other "init_" functions, for other initializations
        '''
        
        self.BG_COLOR_MAIN = COL['deep']

        self.w = w
        self.h = h
        
        #baseTemp=32 # room temperature #should not be stored in tilemap object
        self.grid_terrain =     [ [ None for y in range(h)] for x in range(w) ]

##        self.levels = {}
    #
    
    def tileat(self, x, y):
        if (x >= self.w or x < 0 or y >= self.h or y < 0):
            return WALL
        return self.get_char(x, y)
    def get_blocks_sight(self,x,y):     return self.grid_terrain[x][y].opaque
    def get_nrg_cost_enter(self,x,y):   return self.grid_terrain[x][y].nrg_enter
    def get_nrg_cost_leave(self,x,y):   return self.grid_terrain[x][y].nrg_leave
    def get_audio_dampen(self,x,y):     return self.grid_terrain[x][y].dampen
    def get_char(self,x,y):         return self.grid_terrain[x][y].char
    def get_color(self,x,y):        return COL[self.grid_terrain[x][y].fg]
    def get_bgcolor(self,x,y):
        if rog.fireat(x,y):
            choices=['gold','orange','trueyellow']
            bgCol=COL[choices[dice.roll(len(choices)) - 1]]
        else: bgCol=COL[ self.grid_terrain[x][y].bg ]
        return bgCol
    
    def nthings(self,x,y):              return len(self.grid_things[x][y])
    def thingsat(self,x,y):             return self.grid_things[x][y]
    def thingat(self,x,y): #return the thing at the top of the pile at tile
        listHere = self.grid_things[x][y]
        return listHere[-1] if listHere else None
    
    def inanat(self,x,y): #return inanimate thing at top of the pile at tile
        listHere=self.grid_things[x][y]
        if not listHere: return None
        ent=listHere[-1]
        if rog.world().has_component(ent, cmp.Creature):
            if len(listHere) > 1:
                return listHere[-2] #thing under the top thing
            else:
                return None
        else:
            return ent
    
    def monat (self,x,y):
        '''
            get monster in tile
            (only 1 mon per tile is allowed at a time.
              Monster is always the last element in the list of entities.)
        '''
        ent = self.thingat(x,y)
        if not ent: return None
        isCreature = rog.world().has_component(ent, cmp.Creature)
        return ent if isCreature else None
    
    def solidat(self,x,y):    # get solid thing in tile i.e. things that cannot be moved through... only 1 allowed per tile
        ent = self.thingat(x,y)
        if not ent: return None
        return ent if rog.on(ent, ISSOLID) else None
    
    def lightsat(self,x,y):
        return self.grid_lights[x][y]
    
    def fluidsat(self,x,y):
        return self.grid_fluids[x][y]
    
    
    def COPY(self, tilemap):
        ''' copy another TileMap object into this object '''
        for k,v in tilemap.__dict__.items():
            self.__dict__.update({k:v})
            
    def init_specialGrids(self):
        '''
            # call this function to initialize the global tilemap object
            #   that will contain the level data.
            # temporary tilemap objects that do not need these data, and
            #   which only need access to a few functions within TileMap,
            #   can leave these uninitialized.
        '''
        w=self.w
        h=self.h
            # init special grids
        self.grid_things =      [ [ [] for y in range(h)] for x in range(w) ]
        self.grid_lights =      [ [ [] for y in range(h)] for x in range(w) ]
        #self.grid_fluids =      [ [ [] for y in range(h)] for x in range(w) ]
            # Init root FOVmap
        self.fov_map = libtcod.map_new(w,h)
            # init lightmap which stores luminosity values for each tile
        self.lightmap_init()
            # lists of tiles of interest
        self.question_marks = []
            # init consoles for UI 
        self.con_memories = libtcod.console_new(w,h)
        self.con_map_state = libtcod.console_new(w,h)

    def init_terrain(self, default=FLOOR):
        '''
            Call this to initialize the terrain tile grid with default data.
        '''
        for x in range(self.w):
            for y in range(self.h):
                self._tile_init(x,y,default)
        # TESTING
##        for x in range(self.w):
##            for y in range(self.h):
##                if random.random()*100 > 50:
##                    self._tile_init(x,y,ROUGH)
    
    # procedurally generate a dungeon level
    def generate_dlvl(self, level):
        # if level < 10:
        algo = "tree"
        levelgen.generate_level(self.w, self.h, level, algo=algo)
    
    # add tile (set tile) in the grid
                 
    def tile_change(self, x,y, typ):
        '''
            change tile at (x,y), update fov_map if necessary
            return True if fov_maps for objects must now be updated, too
        '''
        try:
            currentOpacity=self.get_blocks_sight(x,y)
            self.grid_terrain[x][y] = TILES[typ]
            newOpacity=self.get_blocks_sight(x,y)
            #update fov_map base if we need to
            if not (currentOpacity == newOpacity):
                self._update_fov_map_cell_opacity(x,y,(not newOpacity))
                return True
            else:
                return False
        except IndexError:
            print( '''TILE CHANGE ERROR at {},{}. Cannot change to {}.
Reason: out of bounds of grid array.'''.format(x,y,typ) )
            return False
        except Exception as e:
            print( '''TILE CHANGE ERROR at {},{}. Cannot change to {}.
Reason: {}.'''.format(x,y,typ, e) )
            return False
    #
        
    def add_thing(self, ent):
        ''' try to add a thing to the grid, return success/failure '''
        if not rog.world().has_component(ent, cmp.Position):
            print('''Failed to add entity {} to grid.
Reason: entity has no position component.'''.format(ent))
            return False
        pos = rog.world().component_for_entity(ent, cmp.Position)
        x = pos.x; y = pos.y;
        if self.monat(x,y): 
            if rog.world().has_component(ent, cmp.Creature):
                return False #only one creature per tile is allowed
            else: #insert thing right below the creature
                self.grid_things[x][y][-1:0] = [ent]
                return True
        else: #insert thing at top of the list
            self.grid_things[x][y].append(ent)
            return True
    
    def remove_thing(self, ent):
        ''' try to remove an entity from the grid, return success/failure '''
        if not rog.world().has_component(ent, cmp.Position):
            print('''Failed to remove entity {} from grid.
Reason: entity has no position component.'''.format(ent))
            return False
        pos = rog.world().component_for_entity(ent, cmp.Position)
        grid = self.grid_things[pos.x][pos.y]
        if ent in grid:
            grid.remove(ent)
            return True
        print('''Error: failed to remove entity {} from grid.
Reason: entity not in grid.'''.format(ent))
        return False #thing was not in the grid.
    
    def countNeighbors(self, x,y, char):
        '''
            count number tiles of char char adjacent to (x,y)
            (on the terrain grid)
        '''
        num=0
        for _dir in DIRECTIONS.keys():
            xx,yy = _dir
            if xx==0 and yy==0:
                continue #ignore self
            x1=x+xx #position in the tilemap
            y1=y+yy
            if (x1<0 or x1>=self.w or y1<0 or y1>=self.h):
                continue #ignore out of bounds
            if (self.get_char(x1,y1) == char):
                num+=1
        return num
    
    # draw functions
    
    def render_gameArea(self, pc, view_x,view_y,view_w,view_h):
        sight=rog.getms(pc, 'sight')
        self._create_memories(pc, sight)
        self._recall_memories( view_x,view_y,view_w,view_h)
        
        self._draw_distant_lights(pc, view_x,view_y,view_w,view_h)
        self._draw_what_player_sees(pc, sight)
        return self.con_map_state
        
    def get_map_state(self):
        self._recall_memories( 0,0,ROOMW,ROOMH)
        self._draw_what_player_sees(rog.pc())
        return self.con_map_state
    
    # A* paths wrappers
    
    def path_new_movement(self, pathData):
        return libtcod.path_new_using_function(
            ROOMW, ROOMH, self.path_get_cost_movement,
            pathData, 1.41 )
    def path_new_sound(self, pathData):
        return libtcod.path_new_using_function(
            ROOMW, ROOMH, self.path_get_cost_sound,
            pathData, 1.41 )
    
    def path_delete(self, path):    libtcod.path_delete(path)
    # path data functions
    def path_get_cost_movement(self,xFrom,yFrom,xTo,yTo, data):
        return self.get_nrg_cost_enter(xTo,yTo) + self.get_nrg_cost_leave(xFrom,yFrom)
    def path_get_cost_sound(self,xFrom,yFrom,xTo,yTo, data):
        return self.get_audio_dampen(xTo,yTo)
    
    # lighting map
    
    def lightmap_init(self):
        self.grid_lighting=np.full((self.w,self.h), 0)
    def tile_lighten(self, x, y, value):
        self.grid_lighting[x][y] += value
    def tile_darken(self, x, y, value):
        self.grid_lighting[x][y] = max(0, self.grid_lighting[x][y] - value)
    def tile_set_light_value(self, x, y, value):
        self.grid_lighting[x][y]=value
    def get_light_value(self, x, y):
        return self.grid_lighting[x][y]
    
    # private functions
    
    def _tile_init(self, x,y, typ):
        '''
            initialize a tile that has not yet been set
        '''
        self.grid_terrain[x][y] = TILES[typ]
        newOpacity = self.get_blocks_sight(x,y)
        self._update_fov_map_cell_opacity(x,y,(not newOpacity))
        
    def _update_fov_map_cell_opacity(self, x,y, value):
        libtcod.map_set_properties( self.fov_map, x, y, value, True)
    
    def _recall_memories(self, view_x,view_y, view_w,view_h):
        libtcod.console_blit(self.con_memories, view_x,view_y,view_w,view_h,
                             self.con_map_state, view_x,view_y)
            
    def _draw_what_player_sees(self, pc, sight):
        world=rog.world()
        seer=world.component_for_entity(pc, cmp.SenseSight)
        pos=world.component_for_entity(pc, cmp.Position)
        rend=world.component_for_entity(pc, cmp.Draw)

        sight = 100#TEMPORARY!!!!!

        for     x in range( max(0, pos.x-sight), min(self.w, pos.x+sight+1) ):
            for y in range( max(0, pos.y-sight), min(self.h, pos.y+sight+1) ):
##                print("tile at {} {} has light level {}".format(x ,y, self.get_light_value(x,y)))
                
##                if not rog.in_range(pos.x,pos.y, x,y, sight):
##                    continue
##                if not libtcod.map_is_in_fov(seer.fov_map, x,y):
##                    continue
##
                ent=self.thingat(x, y)

##                if (not (x==pos.x and y==pos.y)
##                        and self.get_light_value(x,y) == 0
##                        and not rog.on(pc,NVISION) ):
##                    self._draw_silhouettes(pc, x,y, ent, sight)
##                    continue
##                
                if ent:
                    libtcod.console_put_char(
                        self.con_map_state, x,y,
                        rend.char)
                    libtcod.console_set_char_foreground(
                        self.con_map_state, x,y, rend.fgcol)
                    self._apply_rendered_bgcol(x,y, ent)
                else:
                    libtcod.console_put_char_ex(self.con_map_state, x,y,
                        self.get_char(x, y),
                        self.get_color(x, y), self.get_bgcolor(x, y))
    
    def _apply_rendered_bgcol(self, x, y, ent):
        '''
           get and apply the proper background color
           for the tile containing a thing
        '''
        bgTile=self.get_bgcolor(x, y) #terrain, fires
        bgCol=bgTile
        if not rog.fireat(x,y):
            if self.nthings(x, y) >= 2:
                bgCol=COL['dkgreen']
            elif (ent==rog.pc() and rog.settings().highlightPC ):
                bgCol=COL[rog.settings().highlightColor]
            elif not bgTile == self.BG_COLOR_MAIN:
                bgCol=bgTile
            else:
                bgCol=rog.world().component_for_entity(ent, cmp.Draw).bgcol
        libtcod.console_set_char_background(self.con_map_state, x,y, bgCol)
        
    def _discover_place(self, x,y,ent=None):
        world=rog.world()
##        ent = self.thingat(x,y)
        if ent and not world.has_component(ent, cmp.Creature):
            draw=world.component_for_entity(ent, cmp.Draw)
            libtcod.console_put_char_ex( # memorize items, not creatures
                self.con_memories, x,y, draw.char, COL['dkgray'],COL['black']
                )
        else:
            libtcod.console_put_char_ex(self.con_memories, x,y,
                                        self.get_char(x,y),
                                        COL['dkgray'], COL['black'])
    
    def _create_memories(self, pc, sight):
        world=rog.world()
        pos=world.component_for_entity(pc, cmp.Position)
        if not sight: # and you feel around (?)
            self._discover_place(pos.x,pos.y,self.inanat(x,y))
        for x in     range( max(0, pos.x-sight), min(self.w, pos.x+sight+1) ):
            for y in range( max(0, pos.y-sight), min(self.h, pos.y+sight+1) ):
                if rog.can_see(pc, x,y):
                    self._discover_place(x,y, self.inanat(x,y))
                    
    def _draw_distant_lights(self, pc, view_x,view_y,view_w,view_h):
        pcPos=rog.world().component_for_entity(pc, cmp.Position)
        for light in rog.list_lights():
            lx=light.x
            ly=light.y
            if (lx == pcPos.x and ly == pcPos.y): continue
            if not (lx >= view_x and ly >= view_y
                and lx <= view_x + view_w and ly <= view_y + view_h
                ):
                continue
            libtcod.line_init(pcPos.x,pcPos.y, lx,ly)
            canSee=True
            while True:
                x,y=libtcod.line_step()
                if x == None: break;
                if self.get_blocks_sight(x,y): canSee=False;break;
            if canSee:
                libtcod.console_put_char(self.con_map_state, lx,ly, "?")
    
    def _draw_silhouettes(self, pc, tx,ty, ent, sight):
        '''
        #   extend a line from tile tx,ty to a distant tile
        #   which is in the same direction from the player.
        #   Check for lit tiles, and if we find any along the way,
        #   draw a silhouette for the location of interest.
        #   Basically, if the ent is backlit, you can see
        #   a silhouette.
        '''
        world=rog.world()
        if not sight:
            return
        if not (ent and world.has_component(ent, cmp.Creature)):
            return
        pos=world.component_for_entity(ent, cmp.Position)  
        dist=maths.dist(pos.x,pos.y, tx,ty)
        dx=(tx - pos.x)/dist
        dy=(ty - pos.y)/dist
        xdest=tx + int(dx*sight)
        ydest=ty + int(dy*sight)
        libtcod.line_init(tx,ty, xdest,ydest)
        while True:
            x,y=libtcod.line_step()
            if x is None: return
            if maths.dist(pos.x,pos.y, x,y) > sight: return
            if self.get_blocks_sight(x,y):  return
            if self.get_light_value(x,y):
                libtcod.console_put_char(self.con_map_state, tx,ty, "?")
                return


#-----------------------#
# procedural generation #
#-----------------------#

    def cellular_automata(self,onChar,offChar,iterations,nValues,simultaneous=True):
        '''
        # apply cellular automata to the terrain map
        # Parameters:
        #   onChar : the "1" state character
        #   offChar: the "0" state char
        #   iterations: number of iterations to perform
        #   nValues: tuple containing 9 values. Represents 0-8 neighbors;
        #       - contains birth and death parameters.
        #       - what to do when number of neighbors of a given cell is
        #       the index value of nValues:
        #       -1      : switch to "0" or "off" if value at nValues[numNeighbors] == -1
        #       0       : remain unchanged
        #       1       : switch to "1" or "on"
        #   simultaneous: whether to update all cells at the same time or one by one
        #       True value results in smoother output
        '''
        newMap = None
        if simultaneous:
            newMap = TileMap(self.w,self.h)
            newMap.COPY(self)
        #define some functions to reduce duplicate code
        def _changeTile(x,y,char,simultaneous,newMap):
            if simultaneous:
                newMap.tile_change(x,y,char)
            else:
                self.tile_change(x,y,char)
        def _doYourThing(x,y,num,nValues): # alter a tile or keep it the same based on input
            if nValues[num]==-1:
                _changeTile(x,y,offChar,simultaneous,newMap)
            elif nValues[num]==1:
                _changeTile(x,y,onChar,simultaneous,newMap)
        for ii in range(iterations):
            for x in range(self.w):
                for y in range(self.h):
                    if simultaneous:
                        num = newMap.countNeighbors(x,y, onChar)
                    else:
                        num = self.countNeighbors(x,y, onChar)
                    _doYourThing(x,y,num,nValues)
        if simultaneous:
            self.COPY(newMap)







