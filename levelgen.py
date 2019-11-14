'''
    levelgen.py
    Part of Softly Into the Night, a roguelike by Jacob Wharton.
    Copyright 2019.

    procedural generation of dungeon levels
'''

import math
import random

from const import *
import rogue as rog

RT_ROOM=0
RT_BIGROOM=1
RT_CONGLOMERATEROOM=2
RT_BIGCONGLOMERATEROOM=3
RT_CORRIDOR=4
RT_DRUNKENCORRIDOR=5
RT_THEMEDROOM=6
RT_RARETHEMEDROOM=7
RT_CAVEROOM=8
RT_BIGCAVEROOM=9

class Room:
    def __init__(self, xo : int, yo : int, area : list, perimeter : list):
        self.x_offset = xo
        self.y_offset = yo
        self.area=area
        self.perimeter=perimeter

# idea: separate corridor and room gen?
#   make rooms then corridors.
def pick_roomtype():
    # Total percentage of all options added together:
    #   94%
    
    val = 0
    result = random.random()*100
    
    val += 30
    if result < val: return RT_ROOM
    
    val += 35
    if result < val: return RT_CORRIDOR
    
    val += 8
    if result < val: return RT_CAVEROOM
    
    val += 5
    if result < val: return RT_CONGLOMERATEROOM
    
    val += 5
    if result < val: return RT_THEMEDROOM
    
    val += 5
    if result < val: return RT_DRUNKENCORRIDOR
    
    val += 3
    if result < val: return RT_BIGROOM
    
    val += 1
    if result < val: return RT_RARETHEMEDROOM
    
    val += 1
    if result < val: return RT_BIGCONGLOMERATEROOM
    
    val += 1
    if result < val: return RT_BIGCAVEROOM
    
    return RT_ROOM # default

def grid_set_floor(grid, x, y):
    grid[x][y] = 1

# TODO: create all room and corridor gen functions.
# For now they just do *something* so it doesn't raise an error.

def generate_room_themed(levelwidth, levelheight):
    return generate_room(levelwidth, levelheight)
def generate_room_themed_rare(levelwidth, levelheight):
    return generate_room(levelwidth, levelheight)

def generate_room_cave(levelwidth, levelheight):
    return generate_room(levelwidth, levelheight)
def generate_room_cave_big(levelwidth, levelheight):
    return generate_room(levelwidth, levelheight)

def generate_corridor_drunken(levelwidth, levelheight):
    return generate_corridor(levelwidth, levelheight)

def generate_room_big(levelwidth, levelheight):
    return generate_room(levelwidth, levelheight, mins=10, sizev=5)
def generate_room_conglomerate_big(levelwidth, levelheight):
    return generate_room_conglomerate(levelwidth, levelheight, mins=2, sizev=8, xvar=6, yvar=6, num=16)

def generate_room(levelwidth, levelheight, mins=2, sizev=5):
    '''
        create a regular box room
        Parameters:
            mins     minimum size
            sizev    size variation (mins + sizev == max size)
    '''
    borders = 5 # size of padding where origin of rooms cannot be placed
    area = set()
    perimeter = set()
    # offset position
    xo = int(random.random() * (levelwidth - borders*2)) + borders
    yo = int(random.random() * (levelheight - borders*2)) + borders
    # scale
    xs = mins + int(random.random()*sizev)
    ys = mins + int(random.random()*sizev)
    
    # area and perimeter
        # NOTE: these values are starting from an origin of (0,0).
        #   Add the offset values to get the true x,y position on the map.
    
    # area (get all floor tiles together)
    for xx in range(xs):
        for yy in range(ys):
            area.add( (xx - (xs//2), yy - (ys//2),) )
    
    # perimeter (get all surrounding/wall tiles together)
    for xx in range(xs):
        perimeter.add( (xx - (xs//2), -(ys//2) - 1,) )
        perimeter.add( (xx - (xs//2), math.ceil(ys/2),) )
    for yy in range(ys):
        perimeter.add( (-(xs//2) - 1, yy - (ys//2),) )
        perimeter.add( (math.ceil(xs/2), yy - (ys//2),) )
    
    # create the room object
    room = Room(xo,yo, area, perimeter)
    return room
    
def generate_room_conglomerate(levelwidth, levelheight, mins=2, sizev=4, xvar=4, yvar=4, num=8):
    '''
        create a conglomerate room made of several juxtaposed boxes
        Parameters:
            mins     minimum size of each individual room
            sizev    size variation (mins + sizev == max size) of each individual room
            xvar     x variation between each individual box (+/-)
            yvar     y variation between each individual box (+/-)
    '''
    borders = 5 # size of padding where origin of rooms cannot be placed
    area = set()
    perimeter = set()
    # offset position
    xo = int(random.random() * (levelwidth - borders*2)) + borders
    yo = int(random.random() * (levelheight - borders*2)) + borders
    
    # make a bunch of rectangle rooms that are juxtaposed
    for _ in range(num):
        thisarea = set() # individual rectangle area / perimeter
        thisperi = set()
        # individual rectangle offset
        xoo = int(random.random() * xvar*2) - xvar
        yoo = int(random.random() * yvar*2) - xvar
        # individual rectangle scale
        xs = mins + int(random.random() * sizev)
        ys = mins + int(random.random() * sizev)
        
        # perimeter (get all surrounding/wall tiles together)
        for xx in range(xs):
            thisperi.add( (xx - (xs//2), -(ys//2) - 1,) )
            thisperi.add( (xx - (xs//2), math.ceil(ys/2),) )
        for yy in range(ys):
            thisperi.add( (-(xs//2) - 1, yy - (ys//2),) )
            thisperi.add( (math.ceil(xs/2), yy - (ys//2),) )
        
        # area (get all floor tiles together)
        for xx in range(xs):
            for yy in range(ys):
                thisarea.add( (xx - (xs//2), yy - (ys//2),) )
        
        # make sure this box is touching the existing shape else reject it.
        
        # add to the existing perimeter
        for tile in thisperi:
            x, y = tile
            perimeter.add((x + xoo, y + yoo,))
        
        # add to the existing area
        for tile in thisarea:
            x, y = tile
            area.add((x + xoo, y + yoo,))
        
    # overwrite perimeter data that overlaps with area
    #   this ensures the perimeter only goes around the outside
    for tile in area:
        if tile in perimeter:
            perimeter.remove(tile)
    
    # create the room object
    room = Room(xo,yo, area, perimeter)
    return room

def generate_corridor(levelwidth, levelheight):
    borders = 10 # size of padding where origin of rooms cannot be placed
    result = random.random()*100
    area = set()
    perimeter = set()
    # offset position
    xo = int(random.random() * (levelwidth - borders*2)) + borders
    yo = int(random.random() * (levelheight - borders*2)) + borders
    
    # pick what kind of corridor, vertical or horizontal
    if result < 40: # horizontal
        # scale
        scale = 3 + int(random.random()*13)
        
        # add short-edge perimeters
        perimeter.add( (-(scale//2) - 1, 0,) )
        perimeter.add( (math.ceil(scale/2), 0,) )
        for xx in range(scale):
            area.add( (xx - (scale//2), 0,) )
            perimeter.add( (xx - (scale//2), -1,) )
            perimeter.add( (xx - (scale//2), 1,) )
    elif result < 80: # vertical
        # scale
        scale = 3 + int(random.random()*13)
        perimeter.add( (0, -(scale//2) - 1,) )
        perimeter.add( (0, math.ceil(scale/2),) )
        for yy in range(scale):
            area.add( (0, yy - (scale//2),) )
            perimeter.add( (-1, yy - (scale//2),) )
            perimeter.add( (1, yy - (scale//2),) )
    elif result < 90: # diagonal nw-se
        scale = 3 + int(random.random()*10)
        ceil = math.ceil(scale/2)
        perimeter.add( (-(scale//2), -(scale//2) - 1,) )
        perimeter.add( (-(scale//2) + 1, -(scale//2) - 1,) )
        perimeter.add( (ceil - 1, ceil,) )
        perimeter.add( (ceil, ceil,) )
        for dd in range(scale):
            area.add( (dd - (scale//2), dd - (scale//2),) )
            area.add( (dd - (scale//2) + 1, dd - (scale//2),) )
            perimeter.add( (dd - (scale//2) - 1, dd - (scale//2),) )
            perimeter.add( (dd - (scale//2) + 2, dd - (scale//2),) )
    else: # diagonal ne-sw
        scale = 3# + int(random.random()*10)
        ceil = math.ceil(scale/2)
        perimeter.add( ((scale//2), -(scale//2) - 1,) )
        perimeter.add( ((scale//2) + 1, -(scale//2) - 1,) )
        perimeter.add( (-(scale//2), ceil,) )
        perimeter.add( (-(scale//2) + 1, ceil,) )
        for dd in range(scale):
            area.add( (-dd + (scale//2), dd - (scale//2),) )
            area.add( (-dd + (scale//2) + 1, dd - (scale//2),) )
            perimeter.add( (-dd + (scale//2) - 1, dd - (scale//2),) )
            perimeter.add( (-dd + (scale//2) + 2, dd - (scale//2),) )
    
    # create the room object
    room = Room(xo,yo, area, perimeter)
    return room


# level generation
def generate_level(width, height, z):
    '''
        Make a dungeon level
        Generate a tilemap terrain grid and populate it with stuff
        Parameters:
            width and height are the level's width and height
            z is the dungeon level (integer)
    '''
    # generate rooms then corridors ? Should they be separate?
    # maybe just separate corridor grid from room grid
    #   then combine them together after all are placed on a grid
    #   (combination goes into the actual map grid)
    #   the temp grids are corr_grid and room_grid
    print("Generating level {}...".format(z))
    corr_grid = [[0 for yy in range(height)] for xx in range(width)]
    room_grid = [[0 for yy in range(height)] for xx in range(width)]
    
    print("...Generating rooms...")
    for _ in range(50):
        corridor=False
        roomtype = pick_roomtype()

##        print("picked room type ", roomtype)
        
        if roomtype==RT_ROOM:
            room = generate_room(width, height)
        if roomtype==RT_BIGROOM:
            room = generate_room_big(width, height)
        if roomtype==RT_CAVEROOM:
            room = generate_room_cave(width, height)
        if roomtype==RT_BIGCAVEROOM:
            room = generate_room_cave_big(width, height)
        if roomtype==RT_THEMEDROOM:
            room = generate_room_themed(width, height)
        if roomtype==RT_RARETHEMEDROOM:
            room = generate_room_themed_rare(width, height)
        if roomtype==RT_CONGLOMERATEROOM:
            room = generate_room_conglomerate(width, height)
        if roomtype==RT_BIGCONGLOMERATEROOM:
            room = generate_room_conglomerate_big(width, height)
        if roomtype==RT_CORRIDOR:
            room = generate_corridor(width, height)
            corridor=True
        if roomtype==RT_DRUNKENCORRIDOR:
            room = generate_corridor_drunken(width, height)
            corridor=True
        
        # try to put the room in the grid
        if corridor:
            # slide into place
            xshift = 0
            yshift = 0
            # as long as it touches some existing room,
            #   just add the corridor, allow overlapping.
            for tile in room.area:
                x, y = tile
                xi = x + xshift
                yi = y + yshift
                if xi >= 0 and yi >= 0 and xi < width and yi < height:
                    grid_set_floor(corr_grid, xi, yi)
        else:
            # slide into place
            xshift = 0
            yshift = 0
            # make sure it touches but does not overlap existing rooms.
            # once we've found the proper place to put it, add to the grid
##            for tile in room.area:
##                x, y = tile
##                xi = x + xshift
##                yi = y + yshift
##                if xi >= 0 and yi >= 0 and xi < width and yi < height:
##                    if rog.map(z).tileat(xi, yi) == FLOOR:
##                        success=True
            for tile in room.area:
                x, y = tile
                xi = x + xshift + room.x_offset
                yi = y + yshift + room.y_offset
                if xi >= 0 and yi >= 0 and xi < width and yi < height:
                    grid_set_floor(room_grid, xi, yi)
    #
    print("...Clearing map...")
    rog.map(z).init_terrain(WALL)
    print("...Digging out the rooms and corridors...")
    level_generate_from_grids(
        rog.map(z),
        (room_grid, corr_grid,),
        width, height
        )
    print("...Adding dungeon features...")
    # add staircases
    print("...Populating...") # add entities
    # add creatures
    # add items
    print("Done.")

def level_generate_from_grids(Map, grids, width, height, digtile=FLOOR):
    for grid in grids:
        for x in range(width):
            for y in range(height):
                if grid[x][y] == 1:
                    Map.tile_change(x, y, digtile)


##corr_grid = [[0 for __ in range(5)] for _ in range(8)]
##for x in corr_grid:
##    for y in x:
##        print("x,y={}, {}".format(x, y))
##generate_room(80,50)
##generate_corridor(80,50)





