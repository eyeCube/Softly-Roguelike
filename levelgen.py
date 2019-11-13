'''
    levelgen.py
    Part of Softly Into the Night, a roguelike by Jacob Wharton.
    Copyright 2019.

    procedural generation of dungeon levels
'''

import math
import random

RT_ROOM=0
RT_BIGROOM=1
RT_DRUNKENROOM=2
RT_CORRIDOR=3
RT_DRUNKENCORRIDOR=4
RT_THEMEDROOM=5
RT_CAVEROOM=6
RT_BIGCAVEROOM=7

class Room:
    def __init__(self, xo : int, yo : int, area : list, perimeter : list):
        self.x_offset = xo
        self.y_offset = yo
        self.area=area
        self.perimeter=perimeter

# idea: separate corridor and room gen?
#   make rooms then corridors.
def pick_roomtype():
    val = 0
    result = random.random()*100
    val += 30
    if result < val: return RT_ROOM            
    val += 5
    if result < val: return RT_BIGROOM          
    val += 10
    if result < val: return RT_CAVEROOM        
    val += 1
    if result < val: return RT_BIGCAVEROOM      
    val += 5
    if result < val: return RT_DRUNKENROOM      
    val += 5
    if result < val: return RT_THEMEDROOM        
    val += 1
    if result < val: return RT_RARETHEMEDROOM
    val += 35
    if result < val: return RT_CORRIDOR          
    val += 5
    if result < val: return RT_DRUNKENCORRIDOR
    return RT_ROOM # default

def generate_room(levelwidth, levelheight):
    borders = 5 # size of padding where origin of rooms cannot be placed
    # offset position
    xo = int(random.random() * (levelwidth - borders*2)) + borders
    yo = int(random.random() * (levelheight - borders*2)) + borders
    # scale
    xs = 2 + int(random.random()*5)
    ys = 2 + int(random.random()*5)
    # area and perimeter
        # NOTE: these values are starting from an origin of (0,0).
        #   Add the offset values to get the true x,y position on the map.
    # area (get all floor tiles together)
    area = []
    for xx in range(xs):
        for yy in range(ys):
            area.append( (xx - (xs//2), yy - (ys//2),) )
    # perimeter (get all surrounding/wall tiles together)
    perimeter = []
    for xx in range(xs):
        perimeter.append( (xx - (xs//2), -(ys//2) - 1,) )
        perimeter.append( (xx - (xs//2), math.ceil(ys/2),) )
    for yy in range(ys):
        perimeter.append( (-(xs//2) - 1, yy - (ys//2),) )
        perimeter.append( (math.ceil(xs/2), yy - (ys//2),) )
    # create the room object
    room = Room(xo,yo, area, perimeter)
    return room

def generate_corridor(levelwidth, levelheight):
    borders = 10 # size of padding where origin of rooms cannot be placed
    result = random.random()*100
    area = []
    perimeter = []
    # offset position
    xo = int(random.random() * (levelwidth - borders*2)) + borders
    yo = int(random.random() * (levelheight - borders*2)) + borders
    # pick what kind of corridor, vertical or horizontal
    if result < 40: # horizontal
        # scale
        scale = 3 + int(random.random()*13)
        perimeter.append( (-(scale//2) - 1, 0,) )
        perimeter.append( (math.ceil(scale/2), 0,) )
        for xx in range(scale):
            area.append( (xx - (scale//2), 0,) )
            perimeter.append( (xx - (scale//2), -1,) )
            perimeter.append( (xx - (scale//2), 1,) )
    elif result < 80: # vertical
        # scale
        scale = 3 + int(random.random()*13)
        perimeter.append( (0, -(scale//2) - 1,) )
        perimeter.append( (0, math.ceil(scale/2),) )
        for yy in range(scale):
            area.append( (0, yy - (scale//2),) )
            perimeter.append( (-1, yy - (scale//2),) )
            perimeter.append( (1, yy - (scale//2),) )
    else:#elif result < 90: # diagonal nw-se
        # TODO: test this and add other diagonal
        scale = 3 + int(random.random()*10)
        ceil = math.ceil(scale/2)
        perimeter.append( (-(scale//2), -(scale//2) + 1,) )
        perimeter.append( (-(scale//2) + 1, -(scale//2) + 1,) )
        perimeter.append( (ceil, ceil - 1,) )
        perimeter.append( (ceil + 1, ceil - 1,) )
        for dd in range(scale):
            area.append( (dd - (scale//2), dd - (scale//2),) )
            area.append( (dd - (scale//2) + 1, dd - (scale//2),) )
            perimeter.append( (dd - (scale//2) - 1, dd - (scale//2),) )
            perimeter.append( (dd - (scale//2) + 2, dd - (scale//2),) )
##    else: # diagonal ne-sw
##        scale = 3 + int(random.random()*10)
    # create the room object
    room = Room(xo,yo, area, perimeter)
    return room


# level generation
def generate_level(width, height, z):
    '''
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
    corr_grid = [[0 for xx in range(80)] for yy in range(50)]
    room_grid = [[0 for xx in range(80)] for yy in range(50)]
    
    for _ in range(100):
        roomtype = pick_roomtype()
        corridor=False
        if roomtype==RT_ROOM:
            room = generate_room(width, height)
        if roomtype==RT_BIGROOM:
            room = generate_room_big(width, height)
        if roomtype==RT_CAVEROOM:
            room = generate_room_cave(width, height)
        if roomtype==RT_BIGCAVEROOM:
            room = generate_room_bigcave(width, height)
        if roomtype==RT_THEMEDROOM:
            room = generate_room_themed(width, height)
        if roomtype==RT_DRUNKENROOM:
            room = generate_room_drunken(width, height)
        if roomtype==RT_CORRIDOR:
            room = generate_corridor(width, height)
            corridor=True
        if roomtype==RT_DRUNKENCORRIDOR:
            room = generate_corridor_drunken(width, height)
            corridor=True
        # try to put the room in the grid
        if corridor:
            # as long as it touches some existing room,
            #   just add the corridor, allow overlapping.
            for tile in room.area:
                x, y = tile
                grid_set_floor(corr_grid, x, y)
        else:
            # make sure it touches but does not overlap existing rooms.
            # once we've found the proper place to put it, add to the grid
            for tile in room.area:
                x, y = tile
                grid_set_floor(room_grid, x, y)
    # set all tiles to walls
    rog.map().init_terrain(WALL)
    # dig out the rooms and corridors
    level_generate_from_grids( rog.map(z), (room_grid, corr_grid,) )
    # populate the level with entities
    
    

def level_generate_from_grids(Map, grids, digtile=FLOOR):
    for grid in grids:
        for tile in grid:
            x, y = tile
            Map.tile_change(x, y, digtile)


##corr_grid = [[0 for __ in range(5)] for _ in range(8)]
##print(corr_grid)
##print(corr_grid[7][4])
##generate_room(80,50)
generate_corridor(80,50)





