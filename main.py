'''
    main.py
    Part of Softly Into the Night, a roguelike by Jacob Wharton.
    Copyright 2019.
'''

import esper

import rogue as rog

    
def main():
    rog.Rogue.create_world()
    rog.Rogue.create_map()
    rog.Rogue.create_player()

    while True:
        world.process()
    


if __name__ == "__main__":
    main()
