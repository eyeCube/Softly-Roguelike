'''
    main.py
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


import tcod as libtcod

from const import *

import rogue as rog
import orangio as IO
import game
import player
##import observer    # TODO: implement observer as a processor


#



#------------------------------------------------#
                    # main #
#------------------------------------------------#

def main():
    
#------------------------------------------------#
    # INIT
#------------------------------------------------#
    
    rog.Rogue.create_settings() # later controllers may depend on settings
    rog.Rogue.create_window()
    rog.Rogue.create_consoles()
    rog.Rogue.create_world()
    rog.Rogue.create_controller()
    rog.Rogue.create_data()
    rog.Rogue.create_map(ROOMW,ROOMH)
##    rog.Rogue.create_fov_maps()
    rog.Rogue.create_clock()
    rog.Rogue.create_updater()
    rog.Rogue.create_view()
    rog.Rogue.create_log()
    rog.Rogue.create_savedGame() # TODO: learn/use Pickle.
    rog.Rogue.create_processors()
    rog.Rogue.create_perturn_managers()
    rog.Rogue.create_const_managers()
    
    rog.init_keyBindings()
        
    #map generation
    rog.map(rog.dlvl()).init_specialGrids() # inits fov_map; do this before you init terrain
    rog.map(rog.dlvl()).init_terrain(WALL) # clear the map to all walls
    rog.map(rog.dlvl()).generate_dlvl(rog.dlvl())
        
    # init player

    # TESTING THIS IS ALL TEMPORARY!!!
    # temporary: find a position to place the player
    xpos = 15
    ypos = 15
    _borders = 10
    while rog.map(rog.dlvl()).tileat(xpos, ypos) == WALL:
        xpos +=1
        if xpos >= ROOMW - _borders:
            xpos = _borders
            ypos += 1
        if ypos >= ROOMH:
            print("~~ ! FATAL ERROR ! Failed to place player in the map!")
            break
        
##    rog.create_monster("L", 5,1)
##    rog.create_monster("L", 9,1)
##    rog.create_monster("L", 15,1)
        
    rog.Rogue.create_player(xpos, ypos) # create player
    
    rog.make(rog.pc(), NVISION)
    # TESTING
##    import action
    import components as cmp
##    from colors import COLORS as COL
##    import debug
##    import entities
    #

    ##    rog.setskill(rog.pc(), SKL_BOXING, 100)
##    rog.setskill(rog.pc(), SKL_SWORDS, 30)
##    rog.setskill(rog.pc(), SKL_ARMOR, 100)
##    rog.sets(rog.pc(), 'dex', 120)
##    rog.sets(rog.pc(), 'int', 40)
##    rog.setskill(rog.pc(), SKL_UNARMORED, 40)

    rog.create_monster("L", 1,1)
##    rog.create_monster("L", 25,1)
##    rog.create_monster("L", 30,1)
##    rog.create_monster("L", 35,1)
##    rog.create_monster("L", 40,1)
##    rog.create_monster("L", 45,1)
##    rog.create_monster("L", 50,1)
##    rog.create_monster("L", 55,1)
##    rog.create_monster("L", 60,1)
##    rog.create_monster("L", 65,1)
##    rog.create_monster("L", 70,1)
    
    weap=rog.create_weapon("longsword", 0,0)
    rog.damage(weap, 100)
    rog.equip(
        rog.pc(),weap,EQ_MAINHAND
        )
    rog.equip(
        rog.pc(),rog.create_weapon("metal shield", 0,0),EQ_OFFHAND
        )
    rog.equip(
        rog.pc(),rog.create_armor("metal gear", 0,0),EQ_FRONT
        )
    rog.equip(
        rog.pc(),rog.create_headwear("metal helm", 0,0),EQ_MAINHEAD
        )
    rog.equip(
        rog.pc(),rog.create_legwear("metal mail legging", 0,0),EQ_MAINLEG
        )
    rog.equip(
        rog.pc(),rog.create_legwear("metal mail legging", 0,0),EQ_OFFLEG
        )
##    rog.equip(
##        rog.pc(),rog.create_armwear("metal vambrace", 0,0),EQ_MAINARM
##        )
##    rog.equip(
##        rog.pc(),rog.create_armwear("metal vambrace", 0,0),EQ_OFFARM
##        )
##    rog.equip(
##        rog.pc(),rog.create_footwear("metal boot", 0,0),EQ_MAINFOOT
##        )
##    rog.equip(
##        rog.pc(),rog.create_footwear("metal boot", 0,0),EQ_OFFFOOT
##        )
    #
    
    # create light so player can see
##    log=rog.create_rawmat("log", 18,18)
##    rog.burn(log,500)
    #
    # /TESTING /TEMPORARY
    #
    
    # TODO?: observer for player
##    obs=observer.Observer_playerChange()
##    pc.observer_add(obs)
    pos=rog.get(rog.pc(),cmp.Position)
##    rog.create_monster('W',pos.x,pos.y-1) # all entities showing up as '@'
        

    
#-----------------------------------------------#
#               # MAIN GAME LOOP #              #
#-----------------------------------------------#

    rog.game_set_state("normal")
    
    while rog.game_is_running():
        pc=rog.pc()
        
        # manually close game #
        if libtcod.console_is_window_closed():
            rog.end()
        
        # defeat conditions #
        if rog.on(pc, DEAD):
            rog.game_set_state("game over")
        
        # get input #
        pcInput=IO.get_raw_input()
        pcAct=IO.handle_mousekeys(pcInput).items()
        
        # commands that are available from anywhere #
        player.commands_const(pc, pcAct)
        
        # Finally record game state after any/all changes #
        gameState=rog.game_state()
        
        
                        #----------#
                        #   PLAY   #
                        #----------#
                
        #
        # normal game play
        #
        if gameState == "normal":
            game.play(pc, pcAct)
        #
        # manager game states #
        #
        elif gameState == "manager":
            manager=rog.get_active_manager()
            manager.run(pcAct)
            if manager.result:
                rog.close_active_manager()
        #
        
        elif gameState == "game over":
            rog.msg("You died...")

        
    # end while

    
        
# end def



if __name__ == '__main__':
    main()










    #tt = time.time()

## TIMING
'''tr = time.time() - tt
libtcod.console_print(0,0,0,str(tr))
tt = time.time()'''
##

'''import cProfile
    import re
    cProfile.run('main()')
    #'''
