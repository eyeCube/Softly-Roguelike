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
##import cProfile
##import sys

from const import *

import rogue as rog
import orangio as IO
import game
import player
##import observer    # TODO: implement observer as a processor


# program arguments #

##__PROFILE__     = 0
##if len(sys.argv) > 1:
##    __PROFILE__ = sys.argv[1]
    
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
    rog.getmap(rog.dlvl()).init_specialGrids() # inits fov_map; do this before you init terrain
    rog.getmap(rog.dlvl()).init_terrain(WALL) # clear the map to all walls
    rog.getmap(rog.dlvl()).generate_dlvl(rog.dlvl())
        
    # init player

    # TESTING THIS IS ALL TEMPORARY!!!
    # temporary: find a position to place the player
    xpos = 15
    ypos = 15
    _borders = 10
    while rog.getmap(rog.dlvl()).tileat(xpos, ypos) == WALL:
        xpos +=1
        if xpos >= ROOMW - _borders:
            xpos = _borders
            ypos += 1
        if ypos >= ROOMH:
            print("~~ ! FATAL ERROR ! Failed to place player in the map!")
            break
        
    rog.Rogue.create_player(xpos, ypos) # create player
    
    # TESTING
    # HELP THE PLAYER TO SEE
    rog.create_envlight(1)
    rog.make(rog.pc(), NVISION)
##    import action
    import components as cmp
##    from colors import COLORS as COL
##    import debug
##    import entities
    #
    pos=rog.get(rog.pc(),cmp.Position)
##    rog.create_monster('W',pos.x,pos.y-1) # all entities showing up as '@'
        
    ##    rog.setskill(rog.pc(), SKL_BOXING, 100)
##    rog.setskill(rog.pc(), SKL_SWORDS, 30)
##    rog.setskill(rog.pc(), SKL_ARMOR, 100)
##    rog.sets(rog.pc(), 'dex', 120)
##    rog.sets(rog.pc(), 'int', 40)
##    rog.setskill(rog.pc(), SKL_UNARMORED, 40)

##    for x in range(20):
##        rog.create_monster("L", 1+x*5,1)


    # TODO: re-test all encumberance values (changed system to use Encumberance component instead of direct stat modifiers)
    # TODO: implement Encumberance component with inventory system
    
    weap=rog.create_weapon("metal halberd", 0,0)
##    rog.damage(weap, 200)
##    rog.fitgear(weap, rog.pc())
    rog.equip(
        rog.pc(),weap,EQ_MAINHAND
        )
    rog.create_weapon("wooden club", pos.x,pos.y)
    rog.create_weapon("estoc", pos.x-1,pos.y)
    shield=rog.create_weapon("metal shield", 0,0)
    rog.equip(
        rog.pc(),shield,EQ_OFFHAND
        )
##    rog.fitgear(shield, rog.pc())
    armor=rog.create_armor("metal gear", 0,0)
    rog.equip(
        rog.pc(),armor,EQ_FRONT
        )
##    rog.fitgear(armor, rog.pc())
    helm=rog.create_headwear("metal helm", 0,0)
    rog.equip(
        rog.pc(),helm,EQ_MAINHEAD
        )
##    rog.fitgear(helm, rog.pc())
    leg1=rog.create_legwear("metal mail legging", 0,0)
    rog.equip(
        rog.pc(),leg1,EQ_MAINLEG
        )
##    rog.fitgear(leg1, rog.pc())
    leg2=rog.create_legwear("metal mail legging", 0,0)
    rog.equip(
        rog.pc(),leg2,EQ_OFFLEG
        )
##    rog.fitgear(leg2, rog.pc())
    arm1=rog.create_armwear("metal vambrace", 0,0)
    rog.equip(
        rog.pc(),arm1,EQ_MAINARM
        )
##    rog.fitgear(arm1, rog.pc())
    arm2=rog.create_armwear("metal vambrace", 0,0)
    rog.equip(
        rog.pc(),arm2,EQ_OFFARM
        )
##    rog.fitgear(arm2, rog.pc())
    foot1=rog.create_footwear("metal boot", 0,0)
    rog.equip(
        rog.pc(),foot1,EQ_MAINFOOT
        )
##    rog.fitgear(foot1, rog.pc())
    foot2=rog.create_footwear("metal boot", 0,0)
    rog.equip(
        rog.pc(),foot2,EQ_OFFFOOT
        )
##    rog.fitgear(foot2, rog.pc())
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
