'''
    status.py
'''



def fire(ent):
    world = rog.world()
    stats = world.component_for_entity(ent, cmp.BasicStats)
    stats.hp -= 1
