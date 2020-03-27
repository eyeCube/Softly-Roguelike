'''
    crafting.py
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

from const import *
import entities as ents
import recipes

def get_craftjob_name(detail:int): return CRAFTJOBS[detail][0]
def get_craftjob_fail(detail:int): return CRAFTJOBS[detail][1]
def get_craftjob_crude(detail:int): return CRAFTJOBS[detail][2]
def get_craftjob_quality(detail:int): return CRAFTJOBS[detail][3]
def get_craftjob_masterpiece(detail:int): return CRAFTJOBS[detail][4]
def get_craftjob_roll(detail:int): return CRAFTJOBS[detail][5]

TABLES={
CRT_WEAPONS         :(ents.create_weapon, ents.WEAPONS,),
CRT_RANGED          :(ents.create_ranged_weapon, ents.RANGEDWEAPONS,),
CRT_ARMOR           :(ents.create_armor, ents.ARMOR,),
CRT_HEADWEAR        :(ents.create_headwear, ents.HEADWEAR,),
CRT_LEGWEAR         :(ents.create_legwear, ents.LEGARMOR,),
CRT_ARMWEAR         :(ents.create_armwear, ents.ARMARMOR,),
CRT_FOOTWEAR        :(ents.create_footwear, ents.FOOTARMOR,),
CRT_HANDWEAR        :(ents.create_handwear, ents.HANDARMOR,),
CRT_FACEWEAR        :(ents.create_facewear, ents.FACEWEAR,),
CRT_EYEWEAR         :(ents.create_eyewear, ents.EYEWEAR,),
CRT_EARWEAR         :(ents.create_earwear, ents.EARWEAR,),
CRT_ABOUTWEAR       :(ents.create_aboutarmor, ents.ABOUTARMOR,),
CRT_TOOLS           :(ents.create_tool, ents.TOOLS,),
CRT_FOOD            :(ents.create_food, ents.FOOD,),
CRT_STUFF           :(ents.create_stuff, ents.STUFF,),
CRT_RAWMATS         :(ents.create_rawmat, ents.RAWMATERIALS,),
    }

def craft(
    ent:int, x:int, y:int, itemname:str, detail:int,
    recipe_id=0
    ) -> bool:  # return: success or failure
    ''' entity ent crafts item designated by name itemname in RECIPES
        x,y: position where item will be crafted (default: same pos. as
            the crafting entity, though some may need to be elsewhere).
        detail: level of detail (CRAFTJOB_ const)
        recipe_id: which version of the recipe to use? (if multiple
            recipes exist for one item)
    '''
    world = rog.world()
    entn = world.component_for_entity(ent, cmp.Name)
    
    recipe = recipes.RECIPES.get(itemname, {})
    if not recipe: return False
    table       = recipe['table']
    quantity    = recipe.get('quantity', 1)
    construct   = recipe.get('construct', 1)*AVG_SPD
    overhead    = recipe.get('overhead', 0)*AVG_SPD
    sound       = recipe.get('sound', 0)*RECIPE_SOUND_MULTIPLIER
    celsius     = recipe.get('celsius', rog.roomtemp())
    skills      = recipe.get('skills', (SKL_ASSEMBLY,1,))
    components  = recipe.get('components', ())
    tools       = recipe.get('tools', ())
    using       = recipe.get('using', ())
    byproducts  = recipe.get('byproducts', ())
    info        = recipe.get('info', ())
    requires    = recipe.get('requires', ())
    catalysts   = recipe.get('catalysts', ())
    terrain     = recipe.get('terrain', 'any')
    mass        = recipe.get('mass', 'sum-minus-byproducts')
    durability  = recipe.get('durability', 'average')
    value       = recipe.get('value', 'loss')
    material    = recipe.get('material', 'first-component')
    detailmod = smod = min_lv = 0
    
    # get item info and creation function from appropriate table
    createfunc = TABLES[table][0]
    datatable = TABLES[table][1]
    data = datatable.get(itemname, ())
    if not data: return False
    
    
    # craft job detail level
    detailmod = get_detailmod(detail)
    m_fail = get_craftjob_fail(detail)
    m_crude = get_craftjob_crude(detail)
    m_quality = get_craftjob_quality(detail)
    m_masterpiece = get_craftjob_masterpiece(detail)
    # skill level adequate or deficient?
    if skills:
        primaryID       = skills[0][0]
        primary_min_lv  = skills[0][1]
        total_skill_lv = rog.getskill(ent, primaryID)
        # lower effective skill if any minor requirements not met.
        for skill in skills:
            skillID, requiredLv = skill
            this_skill = rog.getskill(ent, skillID)
            delta = this_skill - requiredLv
            if delta < 0: total_skill_lv += delta
        # calculate a skill modifier
        smod = SKILL_CRAFTING_ROLL * skill_lv
    # end if
    # roll for success
    roll = dice.roll(20) + smod + detailmod - primary_min_lv
    # inadequate primary skill -> big loss in chance to succeed
    if total_skill_lv < primary_min_lv:
        roll -= 20
    if roll <= 0: result = 'fail'
    if roll <= 10: result = 'crude'
    if roll <= 20: result = 'standard'
    if roll <= 40: result = 'quality'
    else: result = 'masterpiece'
    
    if result=='fail':
        rog.msg("{tp}{np} failed to craft {ti}{ni}.".format(
            tp=TITLES[entn.title],np=entn.name,
            ti=TITLES[itemn.title],ni=itemn.name))
        return False
    
    
        #-----------------------------#
#~~~~~~~# SUCCESS! Create the item... #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
        #-----------------------------#
    
    
    # create the byproducts
    for rawmat in byproducts:
        entities.create_rawmat(rawmat, x,y)
    # create the crafted product
    condition = 1
    item = createfunc(itemname, x,y, condition=condition)
    
    # get item components
    itemn = world.component_for_entity(item, cmp.Name)
    
    # apply quality level modifier (TODO) (masterpiece, quality, crude etc.)
    
    # message about crafting
    # TODO: event instead of msg (if AIs will be able to craft things, too)
    rog.msg("{tp}{np} finished crafting {ti}{ni}.".format(
        tp=TITLES[entn.title],np=entn.name,
        ti=TITLES[itemn.title],ni=itemn.name
        ))
    return True
# end def







