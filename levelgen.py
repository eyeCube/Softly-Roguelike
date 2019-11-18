'''
    levelgen.py
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

SLIDE_X = 3 #[1,7,4,3,]
SLIDE_Y = 5

class Room:
    def __init__(self, xo : int, yo : int, area : list, perimeter : list):
        self.x_offset = xo
        self.y_offset = yo
        self.area=area
        self.perimeter=perimeter


# Level generation data
# global vars for use by generate_ functions
class LGD:
    prev_xo=0
    prev_yo=0
    
def get_offset_position(width, height, borders=5, offsetd=40):
    xo = LGD.prev_xo + int(random.random() * (offsetd*2) - offsetd)
    yo = LGD.prev_yo + int(random.random() * (offsetd*2) - offsetd)
    xo = max(borders, min(width - borders, xo))
    yo = max(borders, min(height - borders, yo))
    print("chosen position {}, {}".format(xo, yo))
    return (xo, yo,)


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
    xo, yo = get_offset_position(levelwidth, levelheight, borders)
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
    xo, yo = get_offset_position(levelwidth, levelheight, borders)
    
    # make a bunch of rectangle rooms that are juxtaposed
    for ii in range(num):
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
        if ii == 0:
            touches = True
        else:
            touches = False
        for tile in thisperi:
            if tile in area:
                touches = True
                break
        if touches == False:
            continue
        
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
    
##    print("area")
##    for tile in area:
##        print(tile)
##    print("perimeter")
##    for tile in perimeter:
##        print(tile)
    
    
    # create the room object
    room = Room(xo,yo, area, perimeter)
    return room

def generate_corridor(levelwidth, levelheight):
    borders = 10 # size of padding where origin of rooms cannot be placed
    result = random.random()*100
    area = set()
    perimeter = set()
    xo, yo = get_offset_position(levelwidth, levelheight, borders)
    
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
def generate_level(width, height, z, density=250):
    '''
        Make a dungeon level
        Generate a tilemap terrain grid and populate it with stuff
        Parameters:
            width and height are the level's width and height
            z is the dungeon level (integer)
    '''
    rooms = []
    doors = [] # potential doors that could be added in
    holes = []
    borders = 6
    consecutive_failures = 0
    
    print("Generating level {}...".format(z))
    print("...Generating rooms...")
    # origin room at center of the map
    room = generate_room(width, height)
    room.x_offset = int(random.random()*width/2 + width/4)
    room.y_offset = int(random.random()*height/2 + height/4)
    LGD.prev_xo = room.x_offset
    LGD.prev_yo = room.y_offset
    rooms.append(room)
    # other rooms
    for _ in range(density):
        corridor=False # last room placed was a corridor
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
            # as long as it touches some existing room,
            #   just add the corridor (allow overlapping)
            # find a place to fit it
            success = False
            for _ in range(4):
                if success:
                    break
                # else, slide the room and try again
                overlaps = False
                touches = False
                room.x_offset +=SLIDE_X
                if room.x_offset > width - borders:
                    room.x_offset -= SLIDE_X*5
                    room.y_offset += SLIDE_Y
                if room.y_offset > height - borders:
                    room.y_offset -= SLIDE_Y*3
                for _rm in rooms:
                    # perimeter touching, get potential doors
                    for tile in _rm.perimeter:
                        if touches: break
                        x, y = tile
                        xi = x + _rm.x_offset
                        yi = y + _rm.y_offset
                        for tile2 in room.perimeter:
                            x2, y2 = tile2
                            xi2 = x2 + room.x_offset
                            yi2 = y2 + room.y_offset
                            if xi == xi2 and yi == yi2:
                                touches = True
                                # add a potential door
                                doors.append((xi, yi,))
                                holes.append((xi, yi,))
##                                break
                        # end for tile2
                    # end for tile
                    if not touches:
                        for tile in _rm.area:
                            if overlaps: break
                            x, y = tile
                            xi = x + _rm.x_offset
                            yi = y + _rm.y_offset
                            for tile2 in room.area:
                                x2, y2 = tile2
                                xi2 = x2 + room.x_offset
                                yi2 = y2 + room.y_offset
                                if xi == xi2 and yi == yi2:
                                    overlaps = True
                                    break
                            # end for tile2
                        # end for tile
                    # end if
                    if overlaps or touches:
                        success = True
                        break
                # end for room
                
            # end for range
        #
        else: # it's a room (not a corridor)
            # make sure it touches but does not overlap existing rooms.
            # once we've found the proper place to put it, add to the grid
            # find a place to fit it
            success = False
            for _ in range(4):
                if success:
                    break
                # else, slide the room and try again
                touches = False
                overlaps = False
                room.x_offset +=SLIDE_X
                if room.x_offset > width - borders:
                    room.x_offset -= SLIDE_X*5
                    room.y_offset += SLIDE_Y
                if room.y_offset > height - borders:
                    room.y_offset -= SLIDE_Y*3
                for _rm in rooms:
                    for tile in _rm.perimeter:
                        if touches: break
                        x, y = tile
                        xi = x + _rm.x_offset
                        yi = y + _rm.y_offset
                        for tile2 in room.perimeter:
                            x2, y2 = tile2
                            xi2 = x2 + room.x_offset
                            yi2 = y2 + room.y_offset
                            if (xi == xi2 and yi == yi2):
                                touches = True
                                doors.append((xi, yi,))
                                holes.append((xi, yi,))
                                break
                        # end for tile2
                    # end for tile
                    for tile in _rm.area:
                        if overlaps: break
                        x, y = tile
                        xi = x + _rm.x_offset
                        yi = y + _rm.y_offset
                        for tile2 in room.area:
                            x2, y2 = tile2
                            xi2 = x2 + room.x_offset
                            yi2 = y2 + room.y_offset
                            if xi == xi2 and yi == yi2:
                                overlaps = True
                                break
                        # end for tile2
                    # end for tile
                    if touches and not overlaps:
                        success = True
                        break
                # end for room
            # end for range
        # end if
        if success:
            LGD.prev_xo = room.x_offset
            LGD.prev_yo = room.y_offset
            rooms.append(room)
            consecutive_failures = 0
        else:
            consecutive_failures += 1
            if consecutive_failures >= 3:
                if len(rooms) <= 1:
                    LGD.prev_xo = rooms[0].x_offset
                    LGD.prev_yo = rooms[0].y_offset
                else:
                    LGD.prev_xo = int(random.random()*(width-borders*2) + borders)
                    LGD.prev_yo = int(random.random()*(height-borders*2) + borders)
                    consecutive_failures = 0
    # end for range
    
    # get floor tiles all in one grid
    floor_grid = get_grid_from_rooms(rooms, width, height)
    
    # done with big dungeon changes, now just tweak and add stuff
    
    print("Removing dead ends...")
    list_tiles=[]
    new_list=[]
    for xx in range(width):
        for yy in range(height):
            list_tiles.append((xx,yy,))
    nnn=-1
    while list_tiles:
        nnn+=1
        print("iteration num ", nnn)
        for tile in list_tiles:
            xx, yy = tile
            if floor_grid[xx][yy] == 1:
                walls = 0
                if (xx-1 > 0 and floor_grid[xx-1][yy] == 0):
                    walls += 1
                if (xx+1 < width-1 and floor_grid[xx+1][yy] == 0):
                    walls += 1
                if (yy-1 > 0 and floor_grid[xx][yy-1] == 0):
                    walls += 1
                if (yy+1 < height-1 and floor_grid[xx][yy+1] == 0):
                    walls += 1
                if walls == 3: # dead end
                    print("dead end found at {}, {}".format(xx, yy))
                    if xx-1 > 0:
                        new_list.append((xx-1, yy,))
                    if xx+1 < width-1:
                        new_list.append((xx+1, yy,))
                    if yy-1 > 0:
                        new_list.append((xx, yy-1,))
                    if yy+1 < height-1:
                        new_list.append((xx, yy+1,))
                    floor_grid[xx][yy] = 0
        list_tiles=new_list
        new_list=[]
    #
    
    for hole in holes: # dig out other tiles not covered by the rooms
        x, y = hole
        floor_grid[x][y] = 1
    
    # done editing temporary grids
    # from here on out only edit the actual tilemap terrain grid
    
    print("...Clearing map...")
    rog.map(z).init_terrain(WALL)
    
    print("...Digging out the rooms and corridors...")
    level_init_from_grids(
        rog.map(z),
        (floor_grid,),
        width, height,
        digtile=FLOOR
        )
    
    print("...Adding dungeon features...")
    for tile in doors:
        x, y = tile
        canPlaceDoor = False
        if ( rog.map(z).tileat(x - 1, y) == WALL
            and rog.map(z).tileat(x + 1, y) == WALL
            and rog.map(z).tileat(x, y - 1) == FLOOR
            and rog.map(z).tileat(x, y + 1) == FLOOR ):
            canPlaceDoor = True
        elif ( rog.map(z).tileat(x, y - 1) == WALL
            and rog.map(z).tileat(x, y + 1) == WALL
            and rog.map(z).tileat(x - 1, y) == FLOOR
            and rog.map(z).tileat(x + 1, y) == FLOOR ):
            canPlaceDoor = True
        if not canPlaceDoor:
            continue
        rog.map(z).tile_change(x, y, DOORCLOSED) # TEMPORARY:: see following
##        if random.random()*100 < 30:
##            pass
##        elif random.random()*100 < 50:
##            rog.map(z).tile_change(x, y, FLOOR)
##        elif random.random()*100 < 75:
##            rog.map(z).tile_change(x, y, DOORCLOSED)
##        elif random.random()*100 < 85:
##            rog.map(z).tile_change(x, y, DOOROPEN)
##        elif random.random()*100 < 95:
##            rog.map(z).tile_change(x, y, DOORLOCKED)
##        else:
##            rog.map(z).tile_change(x, y, SECRETDOOR)

    # add staircases

    # DEBUG
##    for room in rooms:
##        for tile in room.perimeter:
##            x, y = tile
##            xi = x + room.x_offset
##            yi = y + room.y_offset
##            rog.map(z).tile_change(xi, yi, ROUGH)
    
    print("...Populating...") # add entities
    # add creatures
    # add items

    print("Done.")

def level_init_from_grids(Map, grids, width, height, digtile=FLOOR, testTile=ROUGH):
    for grid in grids:
        for x in range(width):
            for y in range(height):
                if grid[x][y] == 1:
                    Map.tile_change(x, y, digtile)
                if grid[x][y] == -1:
                    Map.tile_change(x, y, testTile)

def get_grid_from_rooms(rooms, width, height):
    return_grid = [[0 for yy in range(height)] for xx in range(width)]
    for room in rooms:
        for tile in room.area:
            x, y = tile
            xi = x + room.x_offset
            yi = y + room.y_offset
            if xi >= 1 and yi >= 1 and xi < width-1 and yi < height-1:
                return_grid[xi][yi] = 1
    return return_grid


##if __name__ == "__main__":
##    generate_room_conglomerate(80,50, mins=2, sizev=2, xvar=2, yvar=2, num=3)
##    generate_room(80,50)
##    generate_corridor(80,50)



##                                and ( ( (xi-1,yi,) in _rm.perimeter
##                                    and (xi-1,yi,) in room.perimeter )
##                                  or ( (xi+1,yi,) in _rm.perimeter
##                                    and (xi+1,yi,) in room.perimeter ) 
##                                  or ( (xi,yi-1,) in _rm.perimeter
##                                    and (xi,yi-1,) in room.perimeter ) 
##                                  or ( (xi,yi+1,) in _rm.perimeter
##                                    and (xi,yi+1,) in room.perimeter ) )):


