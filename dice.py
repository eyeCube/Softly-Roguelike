'''
    dice.py
    Jacob Wharton
'''

import random

#returns 1 through n (inclusive)
def roll(n):    return 1 + int( random.random()*max(n,0) )
