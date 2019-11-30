
def _areas_overlapping(area1, area2):
    ax1,ay1,ax2,ay2 = area1
    bx1,by1,bx2,by2 = area2
    if (
        (ax1 >= bx1 and ax1 <= bx2 and ay1 >= by1 and ay1 <= by2) or
        (ax2 >= bx1 and ax2 <= bx2 and ay1 >= by1 and ay1 <= by2) or
        (ax1 >= bx1 and ax1 <= bx2 and ay2 >= by1 and ay2 <= by2) or
        (ax2 >= bx1 and ax2 <= bx2 and ay2 >= by1 and ay2 <= by2) or
        (bx1 >= ax1 and bx1 <= ax2 and by1 >= ay1 and by1 <= ay2) or
        (bx2 >= ax1 and bx2 <= ax2 and by1 >= ay1 and by1 <= ay2) or
        (bx1 >= ax1 and bx1 <= ax2 and by2 >= ay1 and by2 <= ay2) or
        (bx2 >= ax1 and bx2 <= ax2 and by2 >= ay1 and by2 <= ay2)
        ):
        return True
    return False

##area=(-5,-5,5,5,)
##area2=(-2,-10,2,10,)
##for xx in range(22):
##    for yy in range(22):
##        xt = xx -12
##        yt = yy -12
##        area1 = (area2[0] + xt, area2[1] + yt, area2[2] + xt, area2[3] + yt)
##        if _areas_overlapping(area1, area)==False:
##            print("oh noes {} {}".format(xx, yy))

class GLOB:
    data = 0

class BinNode:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None
    
def rec(node):
    GLOB.data += 1
    print(GLOB.data)
    if GLOB.data < 50:
        left=right=True
    else:
        left=right=False
    if left:
        node.right = BinNode(GLOB.data)
        rec(node.right)
    if right:
        node.left = BinNode(GLOB.data)
        rec(node.left)


##rec(BinNode(0))
##print(GLOB.data)
##

area1=(0,0,10,10,)
area2=(5,5,15,7,)
print(_areas_overlapping(area1, area2))
##print((area1[0] >= area2[0] and area1[0] <= area2[2] and area1[1] >= area2[2] and area1[1] <= area2[3]))































