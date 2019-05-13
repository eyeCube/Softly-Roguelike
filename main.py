'''
    main.py

    Jacob Wharton
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
