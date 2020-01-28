



l=[('a',1,),('b',2,),]
s=sorted(l, key=lambda x: x[1])
print(s)

'''
# inreach | in reach | in_reach 
# Calculate if your target is within your reach (melee range).
# Instead of calculating with a slow* sqrt func, we access this cute grid:
_REACHGRIDQUAD=[ #0==origin, -1==never in reach
    [10,10,-1,-1,-1,-1,], # we only need 1 quadrant of the total
    [8, 8, 9, 10,-1,-1,], # grid to calculate if you are in reach.
    [6, 7, 7, 9, 10,-1,],
    [4, 5, 6, 7, 9, -1,],
    [2, 3, 5, 7, 8, 10,],
    [0, 2, 4, 6, 8, 10,],
]
#   *not sure if this is actually faster, but it also gives me direct
#    control over which tiles are covered by which reach values.
def inreach(x1,y1, x2,y2, reach):
    xd = abs(x2 - x1) # put the coordinates in the upper right quadrant ...
    yd = -abs(y2 - y1) # ... to match with the quadrant grid above
    if (xd > 5 or yd < -5): return False # maximum distance exceeded
    reachNeeded = _REACHGRIDQUAD[5+yd][xd]
    if reachNeeded==-1:
        return False
    if reach >= reachNeeded:
        return True
    return False


print(inreach(15,15, 14,16, 2))
print(inreach(16,16, 5,16, 30))
print(inreach(16,16, 12,12, 10))
'''
