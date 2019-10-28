'''
    colors.py
    Jacob Wharton
'''

# The values here are just used as the defaults,
# for if the settings file is corrupted.
# Global Settings object modifies these values
# at runtime, using the settings file.
# The values for each key are converted from strings
# into libtcod Color objects derived from the RGB string.

COLORS={
    'white'         : '255,255,255',
    'black'         : '0,0,0',
    'gray'          : '128,128,128',
    'ltgray'        : '200,200,200',
    'dkgray'        : '80,80,80',
    'vdkgray'       : '50,50,50',
    'deep'          : '20,20,0', # background color
    'accent'        : '250,230,168', # main foreground color. Was '255,215,128'
    'neutral'       : '138,100,0',
    'offwhite'      : '245,231,209',
    'puremetal'     : '103,120,146',
    'metal'         : '190,131,118',
    'silver'        : '152,180,212',
    'mithril'       : '192,216,235',
    'crystal'       : '146,235,248',
    'bone'          : '239,222,182',
    'red'           : '242,5,50',
    'truered'       : '255,0,0',
    'dkred'         : '50,0,0',
    'scarlet'       : '223,61,32', #'255,40,0'
    'orange'        : '255,177,0',
    'ltorange'      : '255,215,128',
    'gold'          : '255,200,60',
    'brown'         : '125,91,0',
    'dkbrown'       : '55,36,6',
    'ltbrown'       : '204,150,38',
    'tan'           : '235,192,150',
    'yellow'        : '172,222,20', #'115,190,60'
    'trueyellow'    : '245,255,172', #'255,255,0'
    'lime'          : '153,255,0', # vibrant yellow-green
    'bio'           : '205,236,162', #light yellow-green
    'yellowgreen'   : '115,190,60', #darker yellow-green
    'green'         : '0,170,30',
    'truegreen'     : '0,227,57', #'0,255,0'
    'dkgreen'       : '0,95,17',
    'vdkgreen'      : '20,37,9',
    'graygreen'     : '205,219,181',
    'blue'          : '26,125,160',
    'trueblue'      : '16,25,255',
    'ltblue'        : '140,183,217',
    'dkblue'        : '20,51,103',
    'grayblue'      : '99,126,173',
    'purple'        : '180,60,120',
    'truepurple'    : '172,0,255',
    'graypurple'    : '216,137,176',
    'pink'          : '255,136,77',
    'magenta'       : '255,0,70',
    'dkmagenta'     : '150,0,60',
}

colored_strings=[]
