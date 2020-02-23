
MAXREACH=6
# inreach | in reach | in_reach 
# Calculate if your target is within your reach (melee range).
# Instead of calculating with a slow* sqrt func, we access this cute grid:
_REACHGRIDQUAD=[ #0==origin
    [12,12,99,99,99,99,99,],
    [10,10,11,12,99,99,99,], # we only need 1 quadrant of the total
    [8, 8, 9, 10,11,99,99,], # grid to calculate if you are in reach.
    [6, 7, 7, 9, 10,12,99,],
    [4, 5, 6, 7, 9, 11,99,],
    [2, 3, 5, 7, 8, 10,12,],
    [0, 2, 4, 6, 8, 10,12,],
]
#   *not sure if this is actually faster, but it also gives me direct
#    control over which tiles are covered by which reach values.
def inreach(x1,y1, x2,y2, reach):
    ''' reach is the stat //MULT_STATS but not divided by 2 '''
    xd = abs(x2 - x1) # put the coordinates in the upper right quadrant ...
    yd = -abs(y2 - y1) # ... to match with the quadrant grid above
    if (xd > MAXREACH or yd < -MAXREACH): return False # max distance exceeded
    reachNeeded = _REACHGRIDQUAD[MAXREACH+yd][xd]
    if reach >= reachNeeded:
        return True
    return False
# end def

print(inreach(20,20,15,22, 11))
