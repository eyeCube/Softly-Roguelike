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
    rog.Rogue.create_const_entities()
    
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
    pc = rog.pc()
    
    # TESTING
    # HELP THE PLAYER TO SEE
    rog.create_envlight(16)
##    rog.make(rog.pc(), NVISION)
    #


    # test monster

##    if not rog.wallat(xpos,ypos-2):
##        w=rog.create_monster('W',xpos,ypos-2)
##    elif not rog.wallat(xpos-2,ypos):
##        w=rog.create_monster('W',xpos-2,ypos)
##    elif not rog.wallat(xpos,ypos+2):
##        w=rog.create_monster('W',xpos,ypos+2)
##    elif not rog.wallat(xpos+2,ypos):
##        w=rog.create_monster('W',xpos+2,ypos)


    
##    rog.world().add_component(w, cmp.AttractedToMen())
##    rog.world().add_component(w, cmp.AttractedToWomen())
##    
##     #testing speech
##    rog.init_person(w)
    #
##    w2=rog.create_monster('W',xpos,ypos+1)
##    w3=rog.create_monster('W',xpos,ypos+2)
    
    ##    rog.setskill(pc, SKL_BOXING, 100)
##    rog.setskill(pc, SKL_PERSUASION, 0)
##    rog.setskill(pc, SKL_ARMOR, 100)
##    rog.sets(pc, 'dex', 12*MULT_STATS)
##    rog.sets(pc, 'int', 4*MULT_STATS)
##    rog.setskill(pc, SKL_UNARMORED, 40)

##    for x in range(20):
##        rog.create_monster("L", 1+x*5,1)
    
    
##    rog.alts(pc, 'sight', 50)
    weap=rog.create_weapon("sword", xpos,ypos, mat=MAT_METAL)
    weap=rog.create_weapon("buckler", xpos,ypos, mat=MAT_METAL)
##
##    rog.wound(pc, WOUND_BURN, 2)
    
##    rog.damage(weap, 200)
##    rog.fitgear(weap, pc)
##    print(rog.equip(
##        pc,weap,EQ_MAINHANDW
##        ))
##    rog.create_weapon("wooden club", xpos,ypos)
##    rog.create_weapon("estoc", xpos-1,ypos)
##    shield=rog.create_weapon("metal shield", 0,0)
##    rog.equip(
##        pc,shield,EQ_OFFHAND
##        )
##    rog.fitgear(shield, pc)
##    armor=rog.create_armor("metal gear", 0,0)
##    rog.equip(
##        pc,armor,EQ_FRONT
##        )
##    rog.fitgear(armor, pc)
##    helm=rog.create_headwear("metal helm", 0,0)
##    rog.equip(
##        pc,helm,EQ_MAINHEAD
##        )
##    rog.fitgear(helm, pc)
##    leg1=rog.create_legwear("metal mail legging", 0,0)
##    rog.equip(
##        pc,leg1,EQ_MAINLEG
##        )
##    rog.fitgear(leg1, pc)
##    leg2=rog.create_legwear("metal mail legging", 0,0)
##    rog.equip(
##        pc,leg2,EQ_OFFLEG
##        )
##    rog.fitgear(leg2, pc)
##    arm1=rog.create_armwear("metal vambrace", 0,0)
##    rog.equip(
##        pc,arm1,EQ_MAINARM
##        )
##    rog.fitgear(arm1, pc)
##    arm2=rog.create_armwear("metal vambrace", 0,0)
##    rog.equip(
##        pc,arm2,EQ_OFFARM
##        )
##    rog.fitgear(arm2, pc)
##    foot1=rog.create_footwear("metal boot", 0,0)
##    rog.equip(
##        pc,foot1,EQ_MAINFOOT
##        )
##    rog.fitgear(foot1, pc)
##    foot2=rog.create_footwear("metal boot", 0,0)
##    rog.equip(
##        pc,foot2,EQ_OFFFOOT
##        )
##    rog.fitgear(foot2, pc)
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
        
        # manually close game #
        if libtcod.console_is_window_closed():
            rog.end()
        
        # defeat conditions #
        if rog.on(rog.pc(), DEAD):
            rog.game_set_state("game over")
        
        # get input #
        pcInput=IO.get_raw_input()
        pcAct=IO.handle_mousekeys(pcInput).items()
        
        # commands that are available from anywhere #
        player.commands_const(rog.pc(), pcAct)
        
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
