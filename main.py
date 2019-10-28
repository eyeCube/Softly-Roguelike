'''
    main.py
    Part of Softly Into the Night, a roguelike by Jacob Wharton.
    Copyright 2019.
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
    rog.Rogue.create_map(160,80)
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
    rog.map().init_specialGrids()
    rog.map().init_terrain()

    # init player
    rog.Rogue.create_player(0,0) # is this the right position?

    #TODO: create light so player can see!!!!!!!!!
##    log=rog.create_stuff(THG.LOG, 18,18)
##    rog.burn(log,200)

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
