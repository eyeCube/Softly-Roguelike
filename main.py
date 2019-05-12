'''
    main.py
'''

import esper

    
def main():
    world = esper.World()
    player = create_creature()

    while True:
        world.process()
    


if __name__ == "__main__":
    main()
