'''
    maths.py
    Softly Into the Night, a sci-fi/Lovecraftian roguelike
    Copyright (C) 2020 Jacob Wharton.

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
    
