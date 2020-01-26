

REACHGRID=[ #0==10, @==origin
    ['0','0',' ',' ',' ',' ',],
    ['8','8','9','0',' ',' ',],
    ['6','7','7','9','0',' ',],
    ['4','5','6','7','9',' ',],
    ['2','3','5','7','8','0',],
    ['@','2','4','6','8','0',],
]

def inreach(x1,y1, x2,y2, reach):
    xd = abs(x2 - x1)
    yd = -abs(y2 - y1)
    if (xd > 5 or yd < -5): return False
    char = REACHGRID[5+yd][xd]
    if char==' ':
        return False
    if char=='@':
        return True
    if char=='0':
        reachNeeded=10
    else:
        reachNeeded=int(char)
    if reach >= reachNeeded:
        return True
    return False

print(inreach(16,16, 15,15, 2))
print(inreach(16,16, 16,16, 1))
print(inreach(16,16, 15,15, 3))
