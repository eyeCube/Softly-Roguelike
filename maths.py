'''
    maths
'''

import math

def dist(x1,y1,x2,y2):      return math.sqrt((x1-x2)**2 + (y1-y2)**2)
def pdir(x1,y1,x2,y2):
    dy= y2 - y1; dx= x2 - x1
    return math.atan2(dy,dx)
def isodd (val):            return (val%2==1)
def iseven(val):            return (val%2==0)
def restrict(val,_min,_max): # restrict value to a domain
    val=max(_min,val); val=min(_max,val)
    return val
def sign(val):      return 1 if val >= 0 else -1
    
print(iseven(5))
