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

'''
On primary vs. secondary crafting skill requirements:
    Do not technically NEED a certain level of crafting skill to craft
        an item. But, you are strongly recommended to have it, especially
        the primary skill (the first one in the list of skills used).
    Minor requirements are less mandatory, more guidelines.
        If you have more than required of a minor skill, it does not
        grant you any bonus to your ability to make the item. But, a
        deficiency in any minor skills WILL hurt your chances to succeed.
'''

from const import *
import entities as ents
import recipes

def get_component_name(components:tuple, index:int): return components[index][0]
def get_component_quantity(components:tuple, index:int): return components[index][1]

def get_craftjob_name(detail:int): return CRAFTJOBS[detail][0]
def get_craftjob_roll(detail:int): return CRAFTJOBS[detail][1]

def get_TABLES_create_function(crt_const): return TABLES[0]
def get_TABLES_material_function(crt_const): return TABLES[1]
def get_TABLES_mass_function(crt_const): return TABLES[2]
def get_TABLES_table(crt_const): return TABLES[3]

TABLES={
CRT_WEAPONS         :(ents.create_weapon, ents.get_weapon_mat, ents.get_weapon_mass, ents.WEAPONS,),
CRT_RANGED          :(ents.create_ranged_weapon, ents.get_ranged_mat, ents.get_ranged_mass, ents.RANGEDWEAPONS,),
CRT_ARMOR           :(ents.create_armor, ents.get_gear_mat, ents.get_gear_mass, ents.ARMOR,),
CRT_HEADWEAR        :(ents.create_headwear, ents.get_gear_mat, ents.get_gear_mass, ents.HEADWEAR,),
CRT_LEGWEAR         :(ents.create_legwear, ents.get_gear_mat, ents.get_gear_mass, ents.LEGARMOR,),
CRT_ARMWEAR         :(ents.create_armwear, ents.get_gear_mat, ents.get_gear_mass, ents.ARMARMOR,),
CRT_FOOTWEAR        :(ents.create_footwear, ents.get_gear_mat, ents.get_gear_mass, ents.FOOTARMOR,),
CRT_HANDWEAR        :(ents.create_handwear, ents.get_gear_mat, ents.get_gear_mass, ents.HANDARMOR,),
CRT_FACEWEAR        :(ents.create_facewear, ents.get_gear_mat, ents.get_gear_mass, ents.FACEWEAR,),
CRT_EYEWEAR         :(ents.create_eyewear, ents.get_gear_mat, ents.get_gear_mass, ents.EYEWEAR,),
CRT_EARWEAR         :(ents.create_earwear, ents.get_gear_mat, ents.get_gear_mass, ents.EARWEAR,),
CRT_ABOUTWEAR       :(ents.create_aboutarmor, ents.get_gear_mat, ents.get_gear_mass, ents.ABOUTARMOR,),
CRT_FOOD            :(ents.create_food, ents.get_food_mat, ents.get_food_mass, ents.FOOD,),
CRT_STUFF           :(ents.create_stuff, ents.get_stuff_mat, ents.get_stuff_mass, ents.STUFF,),
CRT_RAWMATS         :(ents.create_rawmat, ents.get_rawmat_mat, ents.get_rawmat_mass, ents.RAWMATERIALS,),
    }

class CraftingJob:
    # what about QueuedAction | QueuedJob ??? How do they factor in?
    def __init__(self):
        self.table      = None
        self.quantity   = None
        self.construct  = None
        self.overhead   = None
        self.sound      = None
        self.celsius    = None
        self.skills     = None
        self.components = None
        self.tools      = None
        self.using      = None
        self.byproducts = None
        self.info       = None
        self.requires   = None
        self.catalysts  = None
        self.terrain    = None
        self.mass       = None
        self.durability = None
        self.value      = None
        self.material   = None
        self.detailmod  = None
    

def craft(
    ent:int, x:int, y:int, itemname:str, detail:int,
    tools=(), using=(), components=(), catalysts=(), recipe_id=0
    ) -> bool:  # return: success or failure
    ''' entity ent crafts item designated by name itemname in RECIPES
        x,y: position where item will be crafted (default: same pos. as
            the crafting entity, though some may need to be elsewhere).
        detail: level of detail (CRAFTJOB_ const)
        recipe_id: which version of the recipe to use? (if multiple
            recipes exist for one item)
        
        given components MUST be in same order as they are in RECIPES!!!
            format: (
                (entity_id,entity_id,),  # first line of components
                (...), # second line of components
                # etc...
                )
            e.g. for dry dough recipe, it would be like this:
                ((flour_entity,), (water_entity,), (salt_entity,),)
                    where each entity is the measured out quantity of
                        the respective ingredient.
    '''
    world = rog.world()
    entn = world.component_for_entity(ent, cmp.Name)
    
    recipe = recipes.RECIPES.get(itemname, {})
    if not recipe: return False
    job = CraftingJob()
    world.add_component(ent,cmp.Crafting(job))
    job.table      = recipe['table']
    job.quantity   = recipe.get('quantity', 1)
    job.construct  = recipe.get('construct', 1)*AVG_SPD
    job.overhead   = recipe.get('overhead', 0)*AVG_SPD
    job.sound      = recipe.get('sound', 0)*RECIPE_SOUND_MULTIPLIER
    job.celsius    = recipe.get('celsius', rog.roomtemp())
    job.skills     = recipe.get('skills', (SKL_ASSEMBLY,1,))
    job.components = recipe.get('components', ())
    job.tools      = recipe.get('tools', ())
    job.using      = recipe.get('using', ())
    job.byproducts = recipe.get('byproducts', ())
    job.info       = recipe.get('info', ())
    job.requires   = recipe.get('requires', ())
    job.catalysts  = recipe.get('catalysts', ())
    job.terrain    = recipe.get('terrain', 'any')
    job.mass       = recipe.get('mass', 'sum-minus-byproducts')
    job.durability = recipe.get('durability', 'average')
    job.value      = recipe.get('value', 'loss')
    job.material   = recipe.get('material', 'first-component')
    job.detailmod = smod = min_lv = 0
    
    # terrain
    if job.terrain=='any':
        pass
    elif job.terrain=='flat':
        pass
    elif job.terrain=='pit':
        if not rog.tileat(x,y)==PIT:
            return False
    elif job.terrain=='water':
        pass
        
    # get item info and creation function from appropriate table
    createfunc = get_TABLES_create_function(job.table)
    material_func = get_TABLES_material_function(job.table)
    datatable = get_TABLES_table(job.table)
    data = datatable.get(itemname, ())
    if not data: return False
    
    
    # craft job detail level
    detailmod = get_craftjob_roll(detail)
    # skill level adequate or deficient?
    if skills:
        primaryID       = skills[0][0]
        primary_min_lv  = skills[0][1]
        primary_skill_lv = rog.getskill(ent, primaryID)
        total_skill_lv = primary_skill_lv
        smod = primary_skill_lv
        # lower effective skill if any minor requirements not met.
        for skill in skills:
            skillID, reqLv = skill
            this_skill = rog.getskill(ent, skillID)
            delta = this_skill - reqLv
            if delta < 0: total_skill_lv += delta
    # end if
    # roll for success
    roll = dice.roll(20)
    roll += detailmod
    roll += SKILL_CRAFTING_ROLL*(smod - primary_min_lv)
    # inadequate primary skill -> big loss in chance to succeed
    if total_skill_lv < primary_min_lv:
        roll -= 20
    if roll < 0: result = 'fail'
    if roll < 10: result = 'crude'
    if roll < 20: result = 'standard'
    if roll < 40: result = 'quality'
    else: result = 'masterpiece'
    
    if result=='fail':
        rog.msg("{tp}{np} failed to craft {ti}{ni}.".format(
            tp=TITLES[entn.title],np=entn.name,
            ti=TITLES[itemn.title],ni=itemn.name))
        return False

    # info designates the way the recipe is created
    if job.info=='auto': # generated automatically, doesn't busy the crafter
        pass
    elif job.info=='quantity-approximate': # components +/- 10%
        pass
    elif job.info=='quantity-lenient': # component quantity +/- 200%
        pass
    elif job.info=='components-by-mass"': # components quantitied by KG
        pass
    elif job.info=='byproducts-by-mass': # byproducts quantified by KG
        pass
    elif job.info=='ratios': # components measured in terms of ratios, not absolute amounts
        pass
    elif job.info=='turn-up-the-heat': # increasing heat -> faster yield
        pass
    
    ap_cost_upfront = job.overhead

    def fn_craft_done

    world.add_component(ent, cmp.DelayedAction(
        JOB_CRAFTING, job.construct, craft_done, craft_cancel
        ))
    
    '''
        construct
        quantity
    tools
    using
    components
        ---
    catalysts
    sound
    info
    celsius
    requires
    '''
    
    return True # success if we made it this far
# end def

def craft_cancel(ent):
    ''' craft failure / stopped before we could finish '''
    compo = world.component_for_entity(ent, cmp.DelayedAction)
    ratio = compo.ap / compo.apmax
    fn_craft_done(ent, ratio_finished=ratio)

def craft_done(ent, ratio_finished=1):
    ''' success function -- create finished product, byproducts,
        and apply any changes like tool durability etc.
        
        ratio_finished: 1 (100%) for completed job. Incompleted job:
            Don't make the finished item, instead make a portion of
            byproducts and make either an "unfinished version" of the
            item or return the components, possibly losing some of them
            (TODO: implement this!)
            
    '''
    compo = world.component_for_entity(first_component,cmp.Crafting)
    job = compo.job
    
    # material
    if job.material=='first-component':
        # get material from first component
        first_component = get_component_name(job.components, 0)
        mat=world.component_for_entity(first_component,cmp.Form).material
    elif job.material=='fixed':
        # get from TABLE
        mat=material_func(datatable[itemname])
        
        
    
    # create the byproducts
    created_byproducts=[]
    for rawmat in job.byproducts:
        created_byproducts.append(entities.create_rawmat(rawmat, x,y))
    # create the crafted product
    condition = 1
    item = createfunc(itemname, x,y, condition=condition)
    world.component_for_entity(item, cmp.Form).material = mat
    
    # mass
    if job.mass = 'sum-minus-byproducts':
        newmass = rog.getms(item, 'mass')
        for ii in created_byproducts:
            newmass -= rog.getms(ii, 'mass')
    elif job.mass = 'sum':
        newmass = 0
        for ii in components:
            newmass += rog.getms(ii, 'mass')
    elif job.mass = 'sum-higher':
        newmass = 0
        for ii in components:
            newmass += rog.getms(ii, 'mass')
        newmass *= 1.1
    elif job.mass = 'sum-lower':
        newmass = 0
        for ii in components:
            newmass += rog.getms(ii, 'mass')
        newmass *= 0.9
    elif job.mass = 'fixed':
        newmass=mass_func(datatable[itemname])
    elif job.mass = 'fixed-higher':
        newmass=mass_func(datatable[itemname])
        newmass *= 1.1
    elif job.mass = 'fixed-lower':
        newmass=mass_func(datatable[itemname])
        newmass *= 0.9
    else: # no change
        newmass = rog.getms(item, 'mass')
    rog.sets(item, 'mass', newmass)

    # durability
    dur_ratio = 1
    if job.durability=='average':
        percent_total = n = 0
        for ii in components:
            percent_total + rog.getms(ii, 'hp')/rog.getms(ii, 'hpmax')
            n += 1
        dur_ratio = percent_total / n
    elif job.durability=='loss':
        percent_total = n = 0
        for ii in components:
            percent_total + rog.getms(ii, 'hp')/rog.getms(ii, 'hpmax')
            n += 1
        dur_ratio = percent_total / n
        dur_ratio *= 0.9
    elif job.durability=='gain':
        percent_total = n = 0
        for ii in components:
            percent_total + rog.getms(ii, 'hp')/rog.getms(ii, 'hpmax')
            n += 1
        dur_ratio = percent_total / n
        dur_ratio *= 1.1
    elif job.durability=='weakest-link':
        for ii in components:
            percent = rog.getms(ii, 'hp')/rog.getms(ii, 'hpmax')
            if percent < dur_ratio:
                dur_ratio = percent
    elif job.durability=='fixed':
        newhp = rog.getms(item, 'hpmax')
    elif job.durability=='fixed-higher':
        rog.sets(item, 'hpmax', 1.1*rog.getms(item, 'hpmax'))
    elif job.durability=='fixed-lower':
        rog.sets(item, 'hpmax', 0.9*rog.getms(item, 'hpmax'))
    newhp = round(dur_ratio * rog.getms(item, 'hpmax'))
    rog.sets(item, 'hp', min(rog.getms(item, 'hpmax', newhp)))

    # value
    total_value=0
    if job.value=='loss':
        for ii in components:
            total_value += rog.get_value(ii)
        for ii in byproducts:
            total_value -= rog.get_value(ii)
        val = 0.8*total_value
    elif job.value=='gain':
        for ii in components:
            total_value += rog.get_value(ii)
        for ii in byproducts:
            total_value -= rog.get_value(ii)
        val = 1.1*total_value
    elif job.value=='sum':
        for ii in components:
            total_value += rog.get_value(ii)
        for ii in byproducts:
            total_value -= rog.get_value(ii)
        val = total_value
    elif job.value=='fixed':
        val = rog.get_value(item)
    world.component_for_entity(item, cmp.Form).value = val
    
    # get item components
    itemn = world.component_for_entity(item, cmp.Name)
    
    # apply quality level modifier (TODO) (masterpiece, quality, crude etc.)
    
    # consume used components (TODO)
    
    # damage tools (TODO)
    
    # message about crafting
    # TODO: event instead of msg (if AIs will be able to craft things, too)
    rog.msg("{tp}{np} finished crafting {ti}{ni}.".format(
        tp=TITLES[entn.title],np=entn.name,
        ti=TITLES[itemn.title],ni=itemn.name
        ))
    return True
# end def







