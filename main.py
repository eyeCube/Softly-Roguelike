'''
    main.py
    Softly Into the Night, a sci-fi/Lovecraftian roguelike
    Copyright (C) 2019 Jacob Wharton.

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

# TESTING
from colors import COLORS as COL
import debug
import entities
#

#



#------------------------------------------------#
                    # main #
#------------------------------------------------#

def main():
    
#------------------------------------------------#
    # INIT
#------------------------------------------------#

    # new way to init
    rog.Rogue.create_settings() # later controllers might depend on settings
    rog.Rogue.create_window()
    rog.Rogue.create_consoles()
    rog.Rogue.create_world()
    rog.Rogue.create_controller()
    rog.Rogue.create_data()
    rog.Rogue.create_map(ROOMW,ROOMH)
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
        
    rog.Rogue.create_player(xpos, ypos) # create player
    
    rog.make(rog.pc(), NVISION)
##    rog.setskill(rog.pc(), SKL_WRESTLING, 25)
    rog.setskill(rog.pc(), SKL_SWORDS, 36)
    rog.equip(
        rog.pc(),rog.create_weapon("metal sword", 0,0),EQ_MAINHAND
        )
##    rog.equip(
##        rog.pc(),rog.create_armor("bone cuirass", 0,0),EQ_FRONT
##        )
##    rog.equip(
##        rog.pc(),rog.create_headwear("plastic helm", 0,0),EQ_MAINHEAD
##        )
##    rog.equip(
##        rog.pc(),rog.create_legwear("metal mail legging", 0,0),EQ_MAINLEG
##        )
    
    # test body part statuses
##    import components as cmp
##    body = rog.world().component_for_entity(rog.pc(), cmp.Body)
##    body.core.core.muscle.status = MUSCLESTATUS_CONTUSION
##    body.parts[cmp.BPC_Arms].arms[0].hand.bone.status = BONESTATUS_FRACTURED
##    body.parts[cmp.BPC_Arms].arms[1].hand.bone.status = BONESTATUS_FRACTURED
##    body.parts[cmp.BPC_Arms].arms[1].hand.skin.status = SKINSTATUS_BURNED
##    body.parts[cmp.BPC_Legs].legs[0].leg.bone.status = BONESTATUS_BROKEN
##    body.parts[cmp.BPC_Legs].legs[1].leg.bone.status = BONESTATUS_DAMAGED
##    body.parts[cmp.BPC_Legs].legs[0].leg.muscle.status = 3
##    body.parts[cmp.BPC_Heads].heads[0].head.bone.status = 3
##    body.parts[cmp.BPC_Heads].heads[0].head.brain.status = 3
##    rog.damagebpp(body.parts[cmp.BPC_Heads].heads[0].head.skin,
##                  BPP_SKIN, SKINSTATUS_BURNED)
##    rog.damagebpp(body.parts[cmp.BPC_Heads].heads[0].head.skin,
##                  BPP_SKIN, SKINSTATUS_BURNED)
    #
    
    # create light so player can see
    log=rog.create_rawmat("log", 18,18)
    rog.burn(log,500)
    #
    # /TESTING /TEMPORARY
    #

    # TODO: heat dispersion with walls?? How to???
    #   no wind indoors where there are walls/roofs
    #   the walls absorb heat??
    #   More general: terrain affects heat dispersion, but how...? 

    # TODO: map_generate function!!    
##    rog.map_generate(rog.map(),rog.dlvl())

    # TODO?: observer for player
##    obs=observer.Observer_playerChange()
##    pc.observer_add(obs)
    
##    
##    ##TESTING
##    rog.gain(pc,"hpmax",100)
##    log=rog.create_stuff(THG.LOG, 18,18)
##    rog.burn(log,200)
##    box=rog.create_stuff(THG.BOX,20,18)
##    #fluids.smoke(16,16)
##    '''pc.stats.hpmax      = 20
##    pc.stats.mpmax      = 20
##    pc.stats.sight      = 20
##    pc.stats.spd        = 100
##    pc.stats.nvision    = False'''
##        #LIGHT
##    pc.light=rog.create_light(pc.x,pc.y, 5, owner=pc)
##        #HEAL
##    rog.givehp(pc)
##    rog.givemp(pc)
##        #EQUIP
##    #print(pc.stats.get('atk'))
##    item=gear.create_weapon("sword",pc.x,pc.y)
##    rog.equip(pc, item, EQ_MAINHAND)
##    #print(pc.stats.get('atk'))
##    #rog.deequip(pc,EQ_MAINHAND)
##    #print(pc.stats.get('atk'))
##        #BUFF
##    #rog.effect_add(pc,{'atk':5})
##    #rog.effect_add(pc,{'dmg':5})
##    #rog.effect_add(pc,{'arm':0})
##    #rog.effect_add(pc,{'msp':15})
##    #rog.effect_add(pc,{'msp':-50})'''
##    '''
##    z = rog.create_monster('Z',15,16)
##    rog.effect_add(z,{'arm':1})
##    rog.effect_add(z,{'dfn':4})
##    rog.effect_add(z,{'atk':3})
##    rog.effect_add(z,{'dmg':3})
##    rog.givehp(z)'''
##    z=rog.create_monster('z',13,19,COL['ltblue'])
##    a=rog.create_monster('a',12,13,COL['scarlet'])
##    o=rog.create_monster('U',19,18,COL['red'])
##    a=rog.create_monster('a',15,17,COL['scarlet'])
##    W=rog.create_monster('W',20,15,COL['purple'])
##    '''import dice
##    for x in range(ROOMW):
##        for y in range(ROOMH):
##            if dice.roll(100) > 98:
##                if not (rog.wallat(x,y)
##                        or rog.monat(x,y) ):
##                    r=rog.create_monster('r',x,y)
##                    r.color=COL['ltgray']
##    print("num monsters: ", len(rog.list_creatures()))
##    '''
    
        

    
#-----------------------------------------------#
#               # MAIN GAME LOOP #              #
#-----------------------------------------------#

    rog.game_set_state("normal")
##    # temporary...
##    rog.update_base()
##    rog.update_game()
##    rog.update_final()

##    # initialize fov for creatures with sight
##    # IS THIS NOT WORKING???? WHAT'S GOING ON?
##    for creat in rog.list_creatures():
##        if creat.stats.sight > 0:
##            rog.fov_compute(creat)
    
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
        # other game states #
        #
        elif (gameState == "move view"
                or gameState == "look"
                or gameState == "busy"
                or gameState == "message history"
                or gameState == "character page"
                ):
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
