'''
    levels.py

    level design algorithms
'''

import libtcodpy as libtcod
import random

from const import *
import tilemap


# generate
# main procedural level generator
# Parameters:
#   Map : TileMap object (pointer)
#   level : current dungeon level that we're creating
#   nRooms : maximum number of "rooms" to generate on this floor
def generate(Map, level, nRooms=50):
    if level == 0:
        # create base
        Map.cellular_automata(
            FUNGUS,FLOOR,8, (-1, -1,-1,-1,0, 1,1,1,1,), simultaneous=True )
        # create rooms
    elif level == 1:
        #unfinished code...
        floor = tilemap.TileMap(ROOMW,ROOMH)
        hyper = tilemap.TileMap(ROOMW,ROOMH)
        for rr in range(nRooms):
            build_random_room(hyper)
            #try to put this room on the floor

# algorithm assumes a blank TileMap object is passed in
def build_random_room(Map):
    #pick a type of room to place on the map
    choices = ("cave","box","cross","circle","cavern",)
    roomType = random.choice(choices)
    if roomType == "cave": #small cave-like room
        drunkardWalk(Map, 3, 10, 0.5, (1,1,1,1,1,1,1,1,))
    elif roomType == "box": #rectangle
        pass
    elif roomType == "cross": #two rectangles overlaid
        pass
    elif roomType == "circle":
        pass
    elif roomType == "cavern": #large cave
        pass
    print("New room created of type {}".format(roomType))
#

# drunken walk algorithm
# Parameters:
#   walks           number of walks to go on
#   length          length of each walk
#   bounciness      tendency to remain around origin rather than branch out
#   weights         iterable w/ directional weights in 8 directions
#                       - index 0 is 0 degrees, 1 is 45 deg, etc.
def drunkardWalk(Map, walks, length, bounciness, weights):
    xp = 15
    yp = 15
    for i in range(10): # clearing where you start
        for j in range(10):
            self.tile_change(xp-5+i,yp-5+j,T_FLOOR)
    self.tile_change(xp,yp,T_FLOOR)
    for i in range(6000):
        xp+=int(random.random()*3)-1
        yp+=int(random.random()*3)-1
        xp=maths.restrict(xp, 0,w-1)
        yp=maths.restrict(yp, 0,h-1)
        self.tile_change(xp,yp,T_FLOOR)
        
        for x in range(1,4):
            for y in range(1,2):
                xx=maths.restrict(x+xp-1, 0,w-1)
                yy=maths.restrict(y+yp-1, 0,h-1)
                self.tile_change(xx,yy,T_FLOOR)
                    
    self.tile_change(xp,yp,T_STAIRDOWN)
#

#UNFINISHED...
# file == .lvl file to load from when creating the cells
'''def make_celledRoom(cols,rows,Map,file):
    # read from the file
    if file[:-4] != ".lvl":
        print("ERROR: File '{}' wrong file type (must be '.lvl'). Aborting...".format(file))
        raise
    mode=0
    try:
        with open(file, "r") as f:
            numCells = f.readline().strip()
            cellw = f.readline().strip()
            cellh = f.readline().strip()
            cy=0
            for line in f:
                if mode==0:
                    if line.strip().lower() == "center":
                        mode=1 #begin reading in the cell data
                elif mode==1:
                    cx=0
                    for char in line.strip():
                        if char=='#':
                            Map.tile_change(cx,cy,)
                        cx+=1
                cy+=1
            #
                    
    except FileNotFoundError:
        print("ERROR: File '{}' not found. Aborting...".format(file))
        raise
'''

'''# for each cell in the room
    for cc in range(cols):
        for rr in range(rows):
            # for each tile in each cell
            for xx in range(cellw):
                for yy in range(cellh):
                    Map.tile_change(x,y,T_FLOOR)'''


#make_celledRoom(16,12,5,5,)
