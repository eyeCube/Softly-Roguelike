'''
    colors

'''

# The values here are just used as the defaults,
# for if the settings file is corrupted.
# Global Settings object modifies these values
# at runtime, using the settings file.
# The values for each key are converted from strings
# into libtcod Color objects derived from the RGB string.

COLORS={
    'deep'          : '20,20,0',
    'accent'        : '255,215,128',
    'neutral'       : '138,100,0',
    'silver'        : '152,180,212',
    'metal'         : '103,120,146',
    'dkblue'        : '20,51,103',
    'blue'          : '26,125,160',
    'trueblue'      : '16,25,255',
    'ltblue'        : '140,183,217',
    'bio'           : '205,236,162',
    'green'         : '0,170,30',
    'dkgreen'       : '0,95,17',
    'vdkgreen'      : '20,37,9',
    'dkmagenta'     : '150,0,60',
    'orange'        : '255,177,0',
    'gold'          : '255,200,60',
    'brown'         : '125,91,0',
    'dkbrown'       : '55,36,6',
    'scarlet'       : '223,61,32', #'255,40,0'
    'red'           : '242,5,50',
    'dkred'         : '50,0,0',
    'truered'       : '255,0,0',
    'purple'        : '180,60,120',
    'truepurple'    : '172,0,255',
    'yellow'        : '115,190,60',
    'trueyellow'    : '255,255,0',
    'white'         : '255,255,255',
    'black'         : '0,0,0',
    'ltgray'        : '200,200,200',
    'gray'          : '128,128,128',
    'dkgray'        : '80,80,80',
    'vdkgray'       : '50,50,50',
}

colored_strings=[]
