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


class GlobalData:
    __N = 0
    __i = 0

class Room:
    def __init__(
            self,
            xo : int, yo : int, area : list, perimeter : list,
            boundw = -1, boundh = -1
            ):
        if boundw == -1: boundw = 999
        if boundh == -1: boundh = 999
        self.x_offset = xo
        self.y_offset = yo
        self.area=area
        self.perimeter=perimeter
        self.boundw = boundw # maximum width / height of this room:
        self.boundh = boundh #   area+perimeter cannot exceed this value


# Level generation data
# global vars for use by generate_ functions
class LGD:
    prev_xo=0
    prev_yo=0

##class RoomTree:
##    def __init__(self, rootData):
##        self.root = BinNode(rootData) # root node
##    def add(self, data):
##        
    
class BinNode:
    def __init__(self, data, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right

def _dig_get_new_dir(xdir, ydir):
    result = random.random()
    if (xdir == 0):
        if result < 0.5:
            xdir = -1
            ydir = 0
        else:
            xdir = 1
            ydir = 0
    else:
        if result < 0.5:
            xdir = 0
            ydir = -1
        else:
            xdir = 0
            ydir = 1
    return (xdir, ydir,)
            
def dig(
    usedareas,
    xstart=-1,ystart=-1, xend=-1,yend=-1,
    maxTurns=2, maxTiles=999
    ):
    '''
        (try to) dig out a corridor
        return the list of tiles or an empty list if failure
        Parameters:
            usedareas   list of (x1,y1,x2,y2) pointlists
            xstart      start position x
            ystart      start position y
            xend        end position x
            yend        end position y
            maxTurns    maximum number of 90 degree turns in the corridor
            maxTiles    maximum number of tiles in the corridor
    '''
    success = False
    tiles = set()
    numTurns = 0
    xpos = xstart
    ypos = ystart
    
    # pick a starting direction
    xd = xend - xpos
    yd = yend - ypos
    diff = rog.sign(abs(xd) - abs(yd))
    if diff > 0:
        xdir = rog.sign(xd)
        ydir = 0
    else:
        xdir = 0
        ydir = rog.sign(yd)

    tiles.add((xstart, ystart,))
    
    while True:        
        if len(tiles) >= maxTiles:
            return set() # failure -> empty set
        # goal reached?
        if (xend == xpos and yend == ypos):
            break
        # check that this tile is not intercepting used tiles
        for area in usedareas:
            x1,y1,x2,y2 = area
            if (xpos >= x1 and xpos <= x2 and ypos >= y1 and ypos <= y2):
                return set()
        
        # move towards the goal position
        if xpos == xend:
            xdir = 0
            ydir = rog.sign(yend - ypos)
        if ypos == yend:
            xdir = rog.sign(xend - xpos)
            ydir = 0
        
        # continue digging
        xpos += xdir
        ypos += ydir
        
        # add this tile to the corridor
        tiles.add((xpos, ypos,))
    
    return tiles

# pick offset x, y position for a room
def get_offset_position(width, height, borders=5, offsetd=40):
    xo = LGD.prev_xo + int(random.random() * (offsetd*2) - offsetd)
    yo = LGD.prev_yo + int(random.random() * (offsetd*2) - offsetd)
    xo = max(borders, min(width - borders, xo))
    yo = max(borders, min(height - borders, yo))
    print("chosen position {}, {}".format(xo, yo))
    return (xo, yo,)

# pick x and y scale for a room
def get_scale(minsize, sizev_w, sizev_h, maxw=-1, maxh=-1):
    if maxw==-1: maxw=9999
    if maxh==-1: maxh=9999
    xs = minsize + min(maxw-2, int(random.random()*sizev_w))
    ys = minsize + min(maxh-2, int(random.random()*sizev_h))
    return (xs, ys,)

def pick_roomtype(corridors=True):
    '''
        randomly select a room type constant
        Parameters:
            corridors    allow the function to select corridor-room types
    '''
    # Total percentage of all options added together:
    # corridors allowed:
    #   94%
    
    val = 0
    if corridors:
        rangen=60
    else:
        rangen=100
    result = random.random()*rangen
    
    val += 30
    if result < val: return RT_ROOM

    if corridors:
        val += 35
        if result < val: return RT_CORRIDOR
    
    val += 8
    if result < val: return RT_CAVEROOM
    
    val += 5
    if result < val: return RT_CONGLOMERATEROOM
    
    val += 5
    if result < val: return RT_THEMEDROOM
    
    if corridors:
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

def make_room(width, height, maxw=-1, maxh=-1, offset=True):
    ''' make a room (no corridors), only return the room object '''
    return _make_room(
        width, height,
        corridors_allowed=False,
        maxw=maxw, maxh=maxh, offset=offset
        )[0]
def _make_room(width, height, corridors_allowed=True, maxw=-1, maxh=-1, offset=True):
    '''
        make a room or a corridor
        Parameters:
            width     level horizontal size
            height    level vertical size
            corridors_allowed whether the algo. can create corridors or not
            maxw      maximum horizontal size of each individual room
            maxh      maximum vertical size of each individual room
            offset    whether or not to set an offset for the room
        Returns: (the room object, and whether it is a corridor (bool))
    '''
    roomtype = pick_roomtype(corridors_allowed)
        
##    print("picked room type ", roomtype)

    corridor=False
    if roomtype==RT_ROOM:
        room = generate_room(width, height, maxw=maxw, maxh=maxh, setOffset=offset)
    elif roomtype==RT_BIGROOM:
        room = generate_room_big(width, height, maxw=maxw, maxh=maxh, setOffset=offset)
    elif roomtype==RT_CAVEROOM:
        room = generate_room_cave(width, height, maxw=maxw, maxh=maxh, setOffset=offset)
    elif roomtype==RT_BIGCAVEROOM:
        room = generate_room_cave_big(width, height, maxw=maxw, maxh=maxh, setOffset=offset)
    elif roomtype==RT_THEMEDROOM:
        room = generate_room_themed(width, height, maxw=maxw, maxh=maxh, setOffset=offset)
    elif roomtype==RT_RARETHEMEDROOM:
        room = generate_room_themed_rare(width, height, maxw=maxw, maxh=maxh, setOffset=offset)
    elif roomtype==RT_CONGLOMERATEROOM:
        room = generate_room_conglomerate(width, height, maxw=maxw, maxh=maxh, setOffset=offset)
    elif roomtype==RT_BIGCONGLOMERATEROOM:
        room = generate_room_conglomerate_big(width, height, maxw=maxw, maxh=maxh, setOffset=offset)
    elif roomtype==RT_CORRIDOR:
        room = generate_corridor(width, height, maxw=maxw, maxh=maxh, setOffset=offset)
        corridor=True
    elif roomtype==RT_DRUNKENCORRIDOR:
        room = generate_corridor_drunken(width, height, maxw=maxw, maxh=maxh, setOffset=offset)
        corridor=True
    return (room, corridor,)

def create_origin_room(width, height):
    # origin room at center of the map
    ow = 4 + int(random.random()*12)
    oh = 4 + int(random.random()*12)
    room = _generate_room(ow, oh)
    room.x_offset = int(random.random()*width/2 + width/4)
    room.y_offset = int(random.random()*height/2 + height/4)
    LGD.prev_xo = room.x_offset
    LGD.prev_yo = room.y_offset
    return room


#-------------------------#
# Room Generate functions #
#-------------------------#

    
# TODO: create all room and corridor gen functions.
# For now they just do *something* so it doesn't raise an error.

def generate_room_themed(levelwidth, levelheight, maxw=-1, maxh=-1, setOffset=True):
    return generate_room(levelwidth, levelheight, maxw=maxw, maxh=maxh, setOffset=setOffset)
def generate_room_themed_rare(levelwidth, levelheight, maxw=-1, maxh=-1, setOffset=True):
    return generate_room(levelwidth, levelheight, maxw=maxw, maxh=maxh, setOffset=setOffset)

def generate_room_cave(levelwidth, levelheight, maxw=-1, maxh=-1, setOffset=True):
    return generate_room(levelwidth, levelheight, maxw=maxw, maxh=maxh, setOffset=setOffset)
def generate_room_cave_big(levelwidth, levelheight, maxw=-1, maxh=-1, setOffset=True):
    return generate_room(levelwidth, levelheight, maxw=maxw, maxh=maxh, setOffset=setOffset)

def generate_corridor_drunken(levelwidth, levelheight, maxw=-1, maxh=-1, setOffset=True):
    return generate_corridor(levelwidth, levelheight, maxw=maxw, maxh=maxh, setOffset=setOffset)

def generate_room_big(levelwidth, levelheight, maxw=-1, maxh=-1, setOffset=True):
    return generate_room(levelwidth, levelheight, mins=10, sizev=5, maxw=maxw, maxh=maxh, setOffset=setOffset)
def generate_room_conglomerate_big(levelwidth, levelheight, maxw=-1, maxh=-1, setOffset=True):
    return generate_room_conglomerate(levelwidth, levelheight, mins=2, sizev=8, xvar=6, yvar=6, num=16, maxw=maxw, maxh=maxh, setOffset=setOffset)

def _generate_room(w, h):
    '''
        create a regular box room
        Parameters:
            w     width of the room
            h     height of the room
    '''
    borders = 5 # size of padding where origin of rooms cannot be placed
    area = set()
    perimeter = set()
    
    # area (get all floor tiles together)
    for xx in range(w):
        for yy in range(h):
            area.add( (xx - (w//2), yy - (h//2),) )
    
    # perimeter (get all surrounding/wall tiles together)
    for xx in range(w):
        perimeter.add( (xx - (w//2), -(h//2) - 1,) )
        perimeter.add( (xx - (w//2), math.ceil(h/2),) )
    for yy in range(h):
        perimeter.add( (-(w//2) - 1, yy - (h//2),) )
        perimeter.add( (math.ceil(w/2), yy - (h//2),) )
    
    # create the room object
    room = Room(0,0, area, perimeter, boundw=w+2, boundh=h+2)
    return room

def generate_room(levelwidth, levelheight, mins=2, sizev=5, maxw=-1, maxh=-1, setOffset=True):
    '''
        BUG: boundw and boundh are being set as -1 which is a bug
        must be set to the actual bounding area of the room
        
        create a regular box room
        Parameters:
            mins     minimum size
            sizev    size variation (mins + sizev == max size)
    '''
    borders = 5 # size of padding where origin of rooms cannot be placed
    area = set()
    perimeter = set()
    if setOffset == True:
        xo, yo = get_offset_position(levelwidth, levelheight, borders)
    else:
        xo = yo = 0
    # scale
    xs, ys = get_scale(mins, sizev, sizev, maxw, maxh)
    
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
    room = Room(xo,yo, area, perimeter, boundw=maxw, boundh=maxh)
    return room
    
def generate_room_conglomerate(levelwidth, levelheight, mins=2, sizev=4, xvar=4, yvar=4, num=8, maxw=-1, maxh=-1, setOffset=True):
    '''
        create a conglomerate room made of several juxtaposed boxes
        Parameters:
            mins     minimum size of each individual room
            sizev    size variation (mins + sizev == max size) of each individual room
            xvar     x variation between each individual box (+/-)
            yvar     y variation between each individual box (+/-)
    '''

    # TODO: fix this so that maxw/maxh will bound the conglomerate room
    
    borders = 5 # size of padding where origin of rooms cannot be placed
    area = set()
    perimeter = set()
    if setOffset == True:
        xo, yo = get_offset_position(levelwidth, levelheight, borders)
    else:
        xo = yo = 0
    # make a bunch of rectangle rooms that are juxtaposed
    for ii in range(num):
        thisarea = set() # individual rectangle area / perimeter
        thisperi = set()
        # individual rectangle offset
        xoo = int(random.random() * xvar*2) - xvar
        yoo = int(random.random() * yvar*2) - xvar
        # individual rectangle scale
        xs, ys = get_scale(mins, sizev, sizev)
        
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
    room = Room(xo,yo, area, perimeter, boundw=maxw, boundh=maxh)
    return room

def generate_corridor(levelwidth, levelheight, maxw=-1, maxh=-1, setOffset=True):
    borders = 10 # size of padding where origin of rooms cannot be placed
    result = random.random()*100
    area = set()
    perimeter = set()
    if setOffset == True:
        xo, yo = get_offset_position(levelwidth, levelheight, borders)
    else:
        xo = yo = 0
    
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
    room = Room(xo,yo, area, perimeter, boundw=maxw, boundh=maxh)
    return room



    #------------------#
    # level generation #
    #------------------#


def generate_level(width, height, z, density=250, algo="dumb"):
    '''
        Make a dungeon level
        Generate a tilemap terrain grid and populate it with stuff
        Parameters:
            width and height are the level's width and height
            z is the dungeon level (integer)
            density has to do with the number of rooms or iterations
            algo is the algorithm to use to build the level
                "dumb"    brute force method
                "tree"    use a tree data struct to form the map
        returns: N/A
    '''
    if algo=="dumb":
        _generate_level_dumb(
            width, height, z,
            density=density
            )
    if algo=="tree":
        _generate_level_tree(
            width, height, z,
            density=density//15,
            maxDensity=density//5
            )

def _get_area(room):
    x1 = room.x_offset - room.boundw // 2
    y1 = room.y_offset - room.boundh // 2
    x2 = room.x_offset + math.ceil(room.boundw / 2)
    y2 = room.y_offset + math.ceil(room.boundh / 2)
    return (x1,y1,x2,y2,)
def _add_usedarea(usedareas, room):
    usedareas.add(_get_area(room))

def _areas_overlapping(area1, area2):
    ax1,ay1,ax2,ay2 = area1
    bx1,by1,bx2,by2 = area2
    if (
        (ax1 >= bx1 and ax1 <= bx2 and ay1 >= by1 and ay1 <= by2) or
        (ax2 >= bx1 and ax2 <= bx2 and ay1 >= by1 and ay1 <= by2) or
        (ax1 >= bx1 and ax1 <= bx2 and ay2 >= by1 and ay2 <= by2) or
        (ax2 >= bx1 and ax2 <= bx2 and ay2 >= by1 and ay2 <= by2)
        ):
        return True
    return False

def _try_build_next_room(node, width, height, usedareas):
    # pick a size and location for the next room; make the room
    maxdist = 32
    mindist = 10
    borders = 10
    roomw=2 + int(random.random()*13) +2 #must add +2 for borders
    roomh=2 + int(random.random()*13) +2 #must add +2 for borders
    room = _generate_room(roomw-2, roomh-2)
    while (room.x_offset == 0 or
           abs(room.x_offset - node.data.x_offset) + abs(
               room.y_offset - node.data.y_offset) < mindist): # not too close -- ensure distance exceeds certain value
        room.x_offset = min(width-borders, max(borders,
            node.data.x_offset - maxdist + int(2*maxdist*random.random()) ))
        room.y_offset = min(height-borders, max(borders,
            node.data.y_offset - maxdist + int(2*maxdist*random.random()) ))

    print("Trying to fit room at {}, {}".format(room.x_offset,room.y_offset))
    
    # make sure it fits
    overlap = False
    area = _get_area(room)
    print(area)
    for usedarea in usedareas:
        print(usedarea)
        if _areas_overlapping(area, usedarea):
            overlap = True
            break
    if overlap: # it doesn't fit, try again with a different room
        return None # failure

    print("Fit room at {}, {}.".format(room.x_offset,room.y_offset))
    
    # pick a perimeter tile of parent room to start the digger
    zipped=[]
    for tile in node.data.perimeter:
        dx = abs(tile[0] + node.data.x_offset - room.x_offset)
        dy = abs(tile[1] + node.data.y_offset - room.y_offset)
        zipped.append((tile, dx+dy,))
    weighted = sorted(zipped, key=lambda x: x[-1])
    
    p1x, p1y = weighted[0][0]
    p1x += node.data.x_offset
    p1y += node.data.y_offset
    
    # pick a perimeter tile of destination room to end the digger
    zipped=[]
    for tile in room.perimeter:
        dx = abs(tile[0] + room.x_offset - node.data.x_offset)
        dy = abs(tile[1] + room.y_offset - node.data.y_offset)
        zipped.append((tile, dx+dy,))
    weighted = sorted(zipped, key=lambda x: x[-1])
    
    p2x, p2y = weighted[0][0]
    p2x += room.x_offset
    p2y += room.y_offset
    
    # dig corridor
    diglist=[]
    iterations=0
    while (not diglist and iterations < 5):
        iterations += 1
        # try to dig a connecting corridor to parent room
        diglist = dig(
            usedareas, xstart=p1x, ystart=p1y, xend=p2x, yend=p2y
            )
        
    if diglist:
        # successfully connected the rooms.
        
        GlobalData.__N += 1
        # usedareas: add the tiles to the set of used room tiles
        _add_usedarea(usedareas, room)
        # dig the corridor out
        for tile in diglist:
            rog.map(rog.dlvl()).tile_change(tile[0], tile[1], FLOOR)
        # dig the room area out
        for tile in room.area:
            xi = tile[0] + room.x_offset
            yi = tile[1] + room.y_offset
            rog.map(rog.dlvl()).tile_change(xi, yi, FLOOR)
            
        print("~~~")
        print(diglist)
        
        return room # success, return room
    print("Failed to dig to new room")
    return None # failure

# generate rooms and corridors recursively
def _genRecursive(node, usedareas, width, height, z, nMin, nMax, maxi):
    '''
        node:       previous (parent) node (node object)
        usedareas:  list of (x1,y1,x2,y2) areas used by rooms
        width:      level width
        height:     level height
        z:          dungeon level
        nMin:       minimum number of rooms we must (at least try to) place
        maxi:       max iterations allowed before it gives up
    '''
    if (GlobalData.__N > nMax):
        return
    if (GlobalData.__i >= maxi):
        return
    GlobalData.__i += 1
    
    numTries = 5
    
    # left child
    if GlobalData.__N < nMin:
        randval = 0.25
    else:
        randval = 0.1
    if (random.random() < randval and node.left==None):
        for _ in range(numTries):
            room = _try_build_next_room(node, width, height, usedareas)
            if room:
                # add a node to the tree
                node.left = BinNode(room)
                # possibly dig extra connecting corridors to adjacent rooms TODO
                # possibly add some child nodes/rooms to this room.
                _genRecursive(
                    node.left, usedareas,
                    width, height, z,
                    nMin, nMax, maxi
                    )
                break
    
    # right child
    if GlobalData.__N < nMin:
        randval = 1
    else:
        randval = 0.2
    if ((random.random() < randval) and node.right==None):
        for _ in range(numTries):
            room = _try_build_next_room(node, width, height, usedareas)
            if room:
                # add a node to the tree
                node.right = BinNode(room)
                # possibly dig extra connecting corridors to adjacent rooms TODO
                # possibly add some child nodes/rooms to this room.
                _genRecursive(
                    node.right, usedareas,
                    width, height, z,
                    nMin, nMax, maxi
                    )
                break

def _generate_level_tree(width, height, z, density=15, maxDensity=50):
    '''
        generate a floor using recursive binary tree descent
            build the tree of room nodes at the same time we dig out the map
        density is the minimum number of rooms; maxDensity the maximum
        returns: N/A
    '''
    
    def traverse(rooms, node):
        # store this room in the list
        rooms.append(node.data)
        # deal with child nodes
        if node.left:
            traverse(rooms, node.left)
        if node.right:
            traverse(rooms, node.right)
            
    GlobalData.__N = 1
    GlobalData.__i = 0
    
    rooms = []
    usedareas=set()
    print("Generating level {}...".format(z))
    
    # origin room is created somewhere in the middle of the map
    origin = create_origin_room(width, height) 
    rooms.append(origin)
    root = BinNode(origin)
    _add_usedarea(usedareas, origin)
    for tile in origin.area:
        xx = tile[0] + origin.x_offset
        yy = tile[1] + origin.y_offset
        rog.map(z).tile_change(xx, yy, FLOOR)
        
    # create other rooms
    _genRecursive(
        root, usedareas,
        width, height, z,
        density, maxDensity, 1000
        )
    # get all rooms in the tree into the room list
    traverse(rooms, root)
    # modify rooms, add connectors(?)
    # finished generating map, tilemap map now contains all level info
    # now populate with entities
    print("Done generating level.")

# old dumb algorithm


def _generate_level_dumb(width, height, z, density=250):
    '''
        use a brute force method to place rooms adjacent to one another
        density is the maximum number of iterations to try placing rooms
        returns: N/A
    '''
    rooms = []
    doors = [] # potential doors that could be added in
    holes = []
    borders = 6
    consecutive_failures = 0
    
    print("Generating level {}...".format(z))
    print("...Generating rooms...")
    # origin room at center of the map
    origin = create_origin_room(width, height) # origin room
    rooms.append(origin)
    # other rooms
    for _ in range(density):
        room, corridor = _make_room(width, height, corridors_allowed=True)
        
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



##        # twisting corridors
##        if xend != -1:
##            if numTurns < maxTurns:
##                if random.random()*100 < 5:
##                    numTurns += 1
##                    xdir, ydir = _dig_get_new_dir(xdir, ydir)


