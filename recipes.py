'''
    recipes.py
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


    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
            Information about recipes and crafting is as follows.

    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
data:
    key = result (name of object to create)
    values = 
    quantity   : number of instances of object to make
    table      : const. referring to which data table holds the object's info
    category   : const. referring to what skill is used in crafting this recipe
    construct  : total amount of action points it takes to create
    components : items used to craft the result, and the quantity needed
        ** material type determined by the first component-list in the tuple
    tools      : tools needed to craft the result, and the durability used (assuming hardness of tool's mat == hardness of item mat. Hardness determined by material. Metal vs. wood does not dull (damage) metal very much, but wood vs. metal destroys the wood easily.)
    byproducts : raw materials that are created in addition to the result (all are from the table RAWMATS, so table is not specified)
special additional data that can be provided:
        (if not provided, the default will be assumed)
    requires   : string, special requirements to craft this item
                    * default: "none"
    terrain    : string, what terrain type(s) the recipe must be built on
                    * default: "any"
                    * "flat" - must be built on flat ground
                    * "pit" - must be built on a pit (hole)
                    * "water" - must be built in water
    sound      : int, amount of audible noise produced during crafting
                    * default: 0
    mass**     : string, special var indicating how the mass is calculated for the result.
                    * default: "sum_minus_byproducts" - total mass of
                        all components, minus the byproducts.
                    * "sum" - total mass of all components.
                    * "sum_lower" - total mass of all components, minus a percentage.
                    * "sum_higher" - total mass of all components, plus a percentage.
                    * "fixed" - mass of the item in the table, regardless of component mass
                    * "fixed_lower" - table lookup minus a percentage
                    * "fixed_higher" - table lookup minus a percentage
            ** NOTE: in most cases, we divide by the quantity of results.
    durability : string, how is the durability calculated?
                    * default: "average" - the average Hp/HpMax is taken.
                        resulting percentage is applied to the durability looked up on the table.
                    * "loss" - average minus a percentage
                    * "gain" - average plus a little extra
                    * "weakest_link" - the minimum durability is taken.
                    * "sum" - simply add Hp/HpMax of all components.
                    * "fixed" - table lookup
                    * "fixed_lower" - table lookup minus a percentage
                    * "fixed_higher" - table lookup minus a percentage
                    * "forged" - metal durability becomes 100%, then do default value calculation from there.
                        - if you forge metal, the metal's damage gets taken away when it melts down and restores to maximum durability.
    value      : string, how is the value calculated?
                    * default: "loss" - sum of costs of raw mats
                        minus the byproducts' value, times 0.8 (lose some value)
                    * "gain" - sum of costs of raw mats plus a little extra
                    * "sum" - sum of costs of raw mats minus byproducts' value
                    * "fixed" - lookup from table
    material   : string, how is the primary material type decided?
                    * default: "first_component" - the material of the first component becomes the material type of the result.
                    * "fixed" - table lookup
    
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Let's view how the component data is arranged:
Components : (
        [ (itemName, quantity), OR (itemName, quantity), ],
            AND
        [ (itemName, quantity), OR (itemName, quantity), ],
    )
Tools are arranged in a similar way (note the distinction between quantity of items in the former and quality of tools in the latter):
        [ (Component, Quality), OR (Component, Quality), ],
            AND
        [ (Component, Quality), OR (Component, Quality), ],

When you break down an object, automatically send a free action to
    HARVEST the object. If the weapon satisfies the tool requirements
    for harvesting the object with the Harvestable component,
    then the object is harvested and you get whatever raw mats it drops.

    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To begin crafting, an entity assigns itself a crafting job.
    * First it decides to craft and chooses a recipe to follow (the result you want determines the recipe -- only one recipe per result)
    
    * Then it must choose whether to build 1 of these or more
        this determines how many components will be required

    * And it must choose how good of a job it wants to do on this crafting:**
        * hack job: construct AP cut to 1/3
            50% chance of failure.
            75% chance to make crude items.
        * quick job: construct AP cut to 2/3
            20% chance of failure.
            33% chance to make crude items.
        * normal job: construct AP 100%
            5% chance of failure.
            5% chance to make crude items.
            5% chance to make quality items.
        * detailed job: construct AP x2
            25% chance to make quality items.
        * fine job: construct AP x4
            50% chance to make quality items.
            1% chance to make masterpiece items.
        * meticulous job: construct AP x8
            100% chance to make at least quality items (provided you're using quality ingredients/tools).
            5% chance to make masterpiece items.
        * thesis job: construct AP x16
            100% chance to make at least quality items (provided you're using quality ingredients/tools).
            25% chance to make masterpiece items.
        **Doing a detailed job or greater may require different recipes.
            It may also require:
                - quality ingredients (can't make a masterpiece w/ shit ingredients, it's tough to make quality items with standard items, and crude ingredients tend to yield crude results; yet you never NEED masterpiece ingredients....)
                - quality tools (see quality ingredients)
                - increased patience (monsters will rarely do long jobs)
                - no stress or distractions (quality work environment)
                - vision and light level to be at a certain value or higher
                - specialist skills
        This may be unnecessary. It would be nice though. Maybe there's a simpler way to implement it.
            could be handled by flags e.g. CRUDE, QUALITY, and MASTER
            
    * Then it must choose which components to use (substitutions)

    * Then it must choose which tools to use
        * components or tools can be selected from either the world
            or from inventory
        * if among the requried tools are a hammer and chisel tool,
            the same tool cannot be used to fulfill both functions.
            Similarly, a single tool cannot be both a hammer and anvil
            for the purpose of a single crafting job.
    * Automatically determined:
        * where to place the completed objects (in the world, in inventory, inside a container, etc.), by default in the same tile as the crafter
        * tools are chosen automatically if the player wants (optional)
            - chooses the lowest quality, lowest durability tool that will satisfy the requirements

    ~~~

Then the crafting job begins:
    The total amount of energy needed to build the thing is recorded.
        this is determined by various factors, including:
            - construct time of the recipe
            - tool quality and durability
            - light level
            
    ~~~
    
While crafting,
    Each turn, the entity continues this job, spending its AP towards that total.
    Once the amount of energy to finish the job reaches 0, the job is complete.
    None of the components or tools can be wet, burning, corroding, etc.
        * Especially not dead
    You have to have at least 1 light level on your tile each turn or you fail to craft
    If the recipe makes sound, the entity has a chance to create a sound
        with a loudness up to the recipe's sound value.
        Chance is based on how shoddy a job the entity does (quick jobs==noisy jobs)
If you fail to craft,
    You have a chance to lose some or all of the raw mats used in the recipe.
    The result is not created.
    The tools may still lose some durability.
When you successfully finish crafting,
    The result(s) is/are created at the predetermined location,
        The result's material type, mass, value, durability are determined
            by the calculations indicated by the recipe data.
    The components are destroyed.
    The tools are damaged.

    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Qualities of crafted items:

    IDEA: instead of names, just do -1, +1, +2, etc. That way you don't
        need to change the beginning of the name of the thing, which would
        fuck with alphabetical organization.
        Aso this is more versatile.
            Blast armor should be able to go higher than +3, probably.
    IDEA: instead of implementing these stat buffs/debuffs on the fly,
        just do them once and change all the stats to the way you want.
        Why would we want to check quality every time we do anything?
        Makes things too complicated.

    Qualities does not affect Tool qualities
        or should it? How to handle that?

    OLD IDEAS:
        crude
            item has 1/4 durability, and -1 to all stats
                (stat penalty for qualities is implemented on the fly)
            item has full mass of the components
            item value is 75%
        standard - no change to name or stats
        quality
            item has 200% durability, and +1 to all stats
            item has 90% mass
            item value is 250%
        masterpiece
            item has 300% durability, and +2 to all stats
            item has 75% mass (80% for armor, 85% for weapons)
            item value is 1000%
        ancient (cannot craft this quality w/o a laboratory)
            item has 500% durability, and +3 to all stats
            item has 60% mass (50% for armor, 80% for weapons)
            item value is 10,000%


    TODO: change CRC_ "category" values to a dict of SKL_ constants
        { SKL_CONST : level_of_skill_required }

'''


from const import *


RECIPES={

    
##'column of wood':{
##    'quantity'  : 1,
##    'table'     : CRT_STUFF,
##    'category'  : CRC_ASSEMBLY,
##    'construct' : 300,
##    'destruct'  : 0,
##    'components': (
##        [ ('wooden plank', 3,), ],
##        [ ('glue', 2,), ],
##        ),
##    'tools'     : (),
##    'byproducts': (),
##    'recycling' : ( ('wooden plank', 3,) ,),
##    },
    
'':{
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_ASSEMBLY,1,),),
    'sound'     : 0,
    'construct' : 0,
    'requires'  : None,
    'components': (
        [ ('', 1,), ],
        ),
    'tools'     : (),
    'byproducts': (),
    },






    #--------------------------#
    #        Raw Mats          #
    #--------------------------#



    # wood
##'wooden plank':{
##    'quantity'  : 20,
##    'table'     : CRT_RAWMATS,
##    'category'  : CRC_WOOD,
##    'construct' : 4800,
##    'components': ( [ ('slab of wood', 1,), ], ),
##    'tools'     : ( [ (cmp.Tool_Saw, 4,), ], ),
##    'byproducts': (),
##    },
##'slab of wood':{ # harvestable instead of recipe
##    'quantity'  : 2,
##    'table'     : CRT_RAWMATS,
##    'category'  : CRC_WOOD,
##    'construct' : 4800,
##    'components': ( [ ('log', 1,), ], ),
##    'tools'     : ( [ (cmp.Tool_Saw, 4,), ], ),
##    'byproducts': (
##        ('chunk of wood', 4,), ('piece of wood', 4,),
##        ('parcel of wood', 4,), ('scrap wood', 4,), ),
##    },

    # cloth
'scrap cloth':{
    'quantity'  : 1,
    'table'     : CRT_RAWMATS,
    'skills'    : ((SKL_CLOTH,10,),),
    'construct' : 1800,
    'components': ( [ ('string', 9,), ], ),
    'tools'     : ( [ (cmp.Tool_Sew, 3,), ], ),
    'byproducts': (),
    },
'parcel of cloth':{
    'quantity'  : 1,
    'table'     : CRT_RAWMATS,
    'skills'    : ((SKL_CLOTH,10,),),
    'construct' : 1800,
    'components': ( [ ('scrap cloth', 5,), ], ),
    'tools'     : ( [ (cmp.Tool_Sew, 3,), ], ),
    'byproducts': (),
    },
'piece of cloth':{
    'quantity'  : 1,
    'table'     : CRT_RAWMATS,
    'skills'    : ((SKL_CLOTH,10,),),
    'construct' : 2400,
    'components': ( [ ('parcel of cloth', 5,), ], ),
    'tools'     : ( [ (cmp.Tool_Sew, 3,), ], ),
    'byproducts': (),
    },
'chunk of cloth':{
    'quantity'  : 1,
    'table'     : CRT_RAWMATS,
    'skills'    : ((SKL_CLOTH,10,),),
    'construct' : 3200,
    'components': ( [ ('piece of cloth', 5,), ], ),
    'tools'     : ( [ (cmp.Tool_Sew, 3,), ], ),
    'byproducts': (),
    },

    # metal
'scrap metal':{
    'quantity'  : 1,
    'table'     : CRT_RAWMATS,
    'skills'    : ((SKL_METAL,1,),),
    'construct' : 1200,
    'components': (
        [ ('metal ore', 1,), ],
        [ ('coke', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Furnace, 3,), ],
        [ (cmp.Tool_Crucible, 2,), ],
        [ (cmp.Tool_Tongs, 2,), ],
        ),
    'byproducts': ( ('slag', 1,), ),
    },
'parcel of metal':{
    'quantity'  : 1,
    'table'     : CRT_RAWMATS,
    'skills'    : ((SKL_METAL,1,),),
    'construct' : 1600,
    'components': ( [ ('scrap metal', 5,), ], ),
    'tools'     : (
        [ (cmp.Tool_Furnace, 3,), ],
        [ (cmp.Tool_Crucible, 2,), ],
        [ (cmp.Tool_Tongs, 2,), ],
        ),
    'byproducts': (),
    },
'shard of metal':{
    'quantity'  : 1,
    'table'     : CRT_RAWMATS,
    'skills'    : ((SKL_METAL,2,),),
    'construct' : 2400,
    'components': ( [ ('parcel of metal', 1,), ], ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 3,), ],
        [ (cmp.Tool_Furnace, 2,), ],
        [ (cmp.Tool_Anvil, 2,), ],
        [ (cmp.Tool_Tongs, 2,), ],
        ),
    'byproducts': (),
    },
'piece of metal':{
    'quantity'  : 1,
    'table'     : CRT_RAWMATS,
    'skills'    : ((SKL_METAL,1,),),
    'construct' : 2400,
    'components': ( [ ('scrap metal', 25,), ('parcel of metal', 5,), ], ),
    'tools'     : (
        [ (cmp.Tool_Furnace, 3,), ],
        [ (cmp.Tool_Crucible, 2,), ],
        [ (cmp.Tool_Tongs, 2,), ],
        ),
    'byproducts': (),
    },
'chunk of metal':{
    'quantity'  : 1,
    'table'     : CRT_RAWMATS,
    'skills'    : ((SKL_METAL,2,),),
    'construct' : 3200,
    'components': (
        [ ('scrap metal', 125,), ('parcel of metal', 25,),
          ('piece of metal', 5,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Furnace, 3,), ],
        [ (cmp.Tool_Crucible, 2,), ],
        [ (cmp.Tool_Tongs, 2,), ],
        ),
    'byproducts': (),
    },
'slab of metal':{
    'quantity'  : 1,
    'table'     : CRT_RAWMATS,
    'skills'    : ((SKL_METAL,3,),),
    'construct' : 4800,
    'components': (
        [ ('scrap metal', 625,), ('parcel of metal', 125,),
          ('piece of metal', 25,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Furnace, 4,), ],
        [ (cmp.Tool_Crucible, 3,), ],
        [ (cmp.Tool_Tongs, 3,), ],
        ),
    'byproducts': (),
    },




    #--------------------------#
    #          Stuff           #
    #--------------------------#


    # MISC. STUFF

    # mixtures of materials
'tinder':{
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_ASSEMBLY,1,),),
    'construct' : 100,
    'components': (
        [ ('scrap wood', 1,), ('twig', 1,), ],
        [ ('foliage', 1,), ('string', 1,), ('paper', 1,), ],
        ),
    'tools'     : (),
    'byproducts': (),
    },
'plastic stool':{
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_PLASTIC,1,),),
    'sound'     : 60,
    'construct' : 1000,
    'components': (
        [ ('chunk of plastic', 1,), ],
        [ ('stick of plastic', 3,), ('plastic tube', 3,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 2,), ],
        [ (cmp.Tool_Saw, 2,), ],
        [ (cmp.Tool_Weld, 1,), (cmp.Tool_Torch, 2,), ],
        ),
    'byproducts': (),
    },
'wooden stool':{
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_WOOD,2,),),
    'sound'     : 60,
    'construct' : 2000,
    'components': (
        [ ('chunk of wood', 1,), ],
        [ ('stick of wood', 3,), ],
        [ ('nail', 3,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 2,), ],
        [ (cmp.Tool_Saw, 2,), ],
        ),
    'byproducts': (
        ('piece of wood', 1,), ('parcel of wood', 1,), ('scrap wood', 1,),
        ),
    },
'metal stool':{
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_METAL,2,),),
    'sound'     : 120,
    'construct' : 3200,
    'components': (
        [ ('chunk of metal', 1,), ],
        [ ('stick of metal', 3,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 3,), ],
        [ (cmp.Tool_Weld, 3,), ],
        [ (cmp.Tool_Anvil, 3,), ],
        [ (cmp.Tool_Furnace, 2,), ],
        [ (cmp.Tool_Tongs, 2,), ],
        ),
    'byproducts': (),
    },
'plastic table':{
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_PLASTIC,1,),),
    'sound'     : 60,
    'construct' : 1400,
    'components': (
        [ ('slab of plastic', 1,), ],
        [ ('stick of plastic', 4,), ('plastic tube', 4,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Furnace, 2,), ],
        [ (cmp.Tool_Hammer, 2,), ],
        [ (cmp.Tool_Saw, 2,), ],
        [ (cmp.Tool_Tongs, 2,), ],
        [ (cmp.Tool_Weld, 1,), (cmp.Tool_Torch, 2,), ],
        [ (cmp.Tool_Crucible, 1,), ],
        [ (cmp.Mold_TablePlastic, 1,), ],
        ),
    'byproducts': (),
    },
'wooden table':{
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_WOOD,3,),),
    'sound'     : 60,
    'construct' : 4800,
    'components': (
        [ ('wooden plank', 6,), ],
        [ ('stick of wood', 4,), ],
        [ ('nail', 16,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 2,), ],
        [ (cmp.Tool_Saw, 2,), ],
        ),
    'byproducts': (),
    },
'metal table':{
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_METAL,5,),),
    'sound'     : 120,
    'construct' : 7200,
    'components': (
        [ ('slab of metal', 1,), ],
        [ ('stick of metal', 4,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Anvil, 3,), ],
        [ (cmp.Tool_Hammer, 3,), ],
        [ (cmp.Tool_Tongs, 3,), ],
        [ (cmp.Tool_Weld, 3,), ],
        [ (cmp.Tool_Furnace, 2,), ],
        ),
    'byproducts': (),
    },

    # gunsmithing
'musket stock':{
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_WOOD,7,), (SKL_GUNSMITH,3,),),
    'construct' : 7200,
    'components': ( [ ('slab of wood', 1,), ], ),
    'tools'     : (
        [ (cmp.Tool_Cut, 5,), ],
        [ (cmp.Tool_Chisel, 4,), ],
        [ (cmp.Tool_Hammer, 3,), ],
        [ (cmp.Tool_Saw, 3,), ],
        ),
    'byproducts': (
        ('chunk of wood', 2,),
        ('piece of wood', 2,),
        ('parcel of wood', 2,),
        ('scrap wood', 2,),
        ),
    },
'caplock trigger mechanism':{
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_GUNSMITH,15,), (SKL_METAL,5,),),
    'construct' : 4800,
    'components': (
        [ ('scrap metal', 2,), ],
        [ ('parcel of metal', 1,), ],
        [ ('nail', 3,), ('screw', 3,), ],
        [ ('torsion spring, small', 1,), ('spring, small', 1,), ('spring', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Cut, 9,), ],
        [ (cmp.Tool_Pliers, 1,), ],
        ),
    'byproducts': (),
    },
'gun barrel, short':{
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_METAL,10,), (SKL_GUNSMITH,6,),),
    'construct' : 43200,
    'components': (
        [ ('metal bar', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Drill, 4,), ],
        [ (cmp.Tool_Hammer, 4,), ],
        [ (cmp.Tool_Anvil, 3,), ],
        [ (cmp.Tool_Furnace, 2,), ],
        [ (cmp.Tool_Mandril, 1,), ],
        [ (cmp.Tool_Swage, 1,), ],
        [ (cmp.Tool_Tongs, 1,), ],
        ),
    'byproducts': (),
    },
'gun barrel':{
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_METAL,5,), (SKL_GUNSMITH,5,),),
    'construct' : 9600,
    'components': ( [ ('gun barrel, short', 2,), ], ),
    'tools'     : (
        [ (cmp.Tool_Drill, 4,), ],
        [ (cmp.Tool_Hammer, 4,), ],
        [ (cmp.Tool_Sharpener, 3,), (cmp.Tool_File, 3,), ],
        [ (cmp.Tool_Furnace, 2,), (cmp.Tool_Weld, 3,), ],
        [ (cmp.Tool_Anvil, 2,), ],
        [ (cmp.Tool_Mandril, 1,), ],
        [ (cmp.Tool_Tongs, 1,), ],
        ),
    'byproducts': (),
    },
'gun barrel, long':{
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_METAL,5,), (SKL_GUNSMITH,5,),),
    'construct' : 9600,
    'components': ( [ ('gun barrel', 1,), ], [ ('gun barrel, short', 1,), ], ),
    'tools'     : (
        [ (cmp.Tool_Drill, 4,), ],
        [ (cmp.Tool_Hammer, 4,), ],
        [ (cmp.Tool_Sharpener, 3,), (cmp.Tool_File, 3,), ],
        [ (cmp.Tool_Furnace, 2,), (cmp.Tool_Weld, 3,), ],
        [ (cmp.Tool_Anvil, 2,), ],
        [ (cmp.Tool_Mandril, 1,), ],
        [ (cmp.Tool_Tongs, 1,), ],
        ),
    'byproducts': (),
    },

    # metal
'metal needle':{
    'quantity'  : 1,
    'table'     : CRT_RAWMATS,
    'skills'    : ((SKL_METAL,6,),),
    'construct' : 1800,
    'components': (
        [ ('paperclip', 1,), ('scrap metal', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Cut, 8,), ],
        [ (cmp.Tool_Hammer, 4,), ],
        [ (cmp.Tool_Anvil, 3,), ],
        ),
    'byproducts': (),
    },
'pop tab mail ring':{
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_METAL,1,),),
    'construct' : 50,
    'components': ( [ ('pop tab', 1,), ], ),
    'tools'     : (
        [ (cmp.Tool_Cut, 6,), ],
        [ (cmp.Tool_Pliers, 1,), ],
        ),
    'byproducts': (),
    },
'mail ring, riveted':{
    'quantity'  : 8,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_METAL,12,),),
    'construct' : 1600,
    'mass'      : 'fixed',
    'components': (
        [ ('metal wire', 1,), ],
        [ ('nail', 8,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Cut, 8,), ],
        [ (cmp.Tool_Hammer, 4,), ],
        [ (cmp.Tool_Pliers, 2,), ],
        ),
    'byproducts': ( ('scrap metal', 2,), ),
    },
'mail ring, welded':{
    'quantity'  : 4,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_METAL,4,),),
    'construct' : 800,
    'mass'      : 'fixed',
    'components': (
        [ ('metal wire', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Cut, 8,), ],
        [ (cmp.Tool_Pliers, 2,), ],
        [ (cmp.Tool_Weld, 1,), (cmp.Tool_Torch, 3,), ],
        ),
    'byproducts': (),
    },

    # arrowheads
'plastic arrowhead':{
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_PLASTIC,5,),),
    'sound'     : 60,
    'construct' : 300,
    'components': (
        [ ('shard of plastic', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Cut, 4,), ],
        [ (cmp.Tool_Sharpener, 1,), (cmp.Tool_File, 1,), ],
        ),
    'byproducts': ( ('scrap plastic', 1,), ),
    },
'wooden arrowhead':{
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_WOOD,5,),),
    'sound'     : 60,
    'construct' : 500,
    'components': (
        [ ('shard of wood', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Cut, 5,), ],
        [ (cmp.Tool_Sharpener, 1,), (cmp.Tool_File, 1,), ],
        ),
    'byproducts': ( ('scrap wood', 1,), ),
    },
'bone arrowhead':{
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_BONE,10,),),
    'sound'     : 60,
    'construct' : 800,
    'components': (
        [ ('shard of bone', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 3,), ],
        [ (cmp.Tool_Chisel, 2,), ],
        [ (cmp.Tool_Sharpener, 1,), (cmp.Tool_File, 1,), ],
        ),
    'byproducts': ( ('scrap bone', 1,), ),
    },
'stone arrowhead':{
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_STONE,10,),),
    'sound'     : 60,
    'construct' : 1200,
    'components': (
        [ ('shard of stone', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 3,), ],
        [ (cmp.Tool_Chisel, 3,), ],
        [ (cmp.Tool_Sharpener, 2,), (cmp.Tool_File, 2,), ],
        ),
    'byproducts': ( ('gravel', 1,), ),
    },
'metal arrowhead':{
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_METAL,15,),),
    'sound'     : 120,
    'construct' : 2000,
    'components': (
        [ ('shard of metal', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 3,), ],
        [ (cmp.Tool_Furnace, 2,), (cmp.Tool_Torch, 3,), ],
        [ (cmp.Tool_Anvil, 3,), ],
        [ (cmp.Tool_Sharpener, 2,), (cmp.Tool_File, 4,), ],
        [ (cmp.Tool_Tongs, 1,), ],
        ),
    'byproducts': (),
    },
'glass arrowhead':{
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_GLASS,20,),),
    'sound'     : 60,
    'construct' : 3000,
    'components': (
        [ ('shard of glass', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 4,), ],
        [ (cmp.Tool_Chisel, 4,), ],
        ),
    'byproducts': (),
    },


    # spearheads
'plastic spearhead':{
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_PLASTIC,5,),),
    'sound'     : 60,
    'construct' : 500,
    'components': (
        [ ('piece of plastic', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Cut, 4,), ],
        [ (cmp.Tool_Sharpener, 1,), (cmp.Tool_File, 1,), ],
        ),
    'byproducts': ( ('scrap plastic', 1,), ),
    },
'wooden spearhead':{
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_WOOD,6,),),
    'sound'     : 60,
    'construct' : 1000,
    'components': (
        [ ('piece of wood', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Cut, 4,), ],
        [ (cmp.Tool_Hammer, 2,), ],
        [ (cmp.Tool_Chisel, 2,), ],
        [ (cmp.Tool_Sharpener, 1,), (cmp.Tool_File, 1,), ],
        ),
    'byproducts': ( ('scrap wood', 1,), ),
    },
'bone spearhead':{
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_BONE,10,),),
    'sound'     : 60,
    'construct' : 1500,
    'components': (
        [ ('piece of bone', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 3,), ],
        [ (cmp.Tool_Chisel, 2,), ],
        [ (cmp.Tool_Sharpener, 1,), (cmp.Tool_File, 1,), ],
        ),
    'byproducts': ( ('scrap bone', 1,), ),
    },
'stone spearhead':{
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_STONE,12,),),
    'sound'     : 60,
    'construct' : 2200,
    'components': (
        [ ('piece of stone', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 3,), ],
        [ (cmp.Tool_Chisel, 3,), ],
        [ (cmp.Tool_Sharpener, 2,), (cmp.Tool_File, 2,), ],
        ),
    'byproducts': ( ('gravel', 1,), ),
    },
'metal spearhead':{
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_METAL,10,),),
    'sound'     : 120,
    'construct' : 3600,
    'components': (
        [ ('piece of metal', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 3,), ],
        [ (cmp.Tool_Furnace, 2,), (cmp.Tool_Torch, 3,), ],
        [ (cmp.Tool_Sharpener, 3,), (cmp.Tool_File, 4,), ],
        [ (cmp.Tool_Anvil, 2,), ],
        [ (cmp.Tool_Tongs, 1,), ],
        ),
    'byproducts': (),
    },
'glass spearhead':{
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_GLASS,15,),),
    'sound'     : 60,
    'construct' : 4200,
    'components': (
        [ ('piece of glass', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 4,), ],
        [ (cmp.Tool_Chisel, 4,), ],
        ),
    'byproducts': (),
    },

    # water filters / purifiers
# water qualities:
# waste water (requires industrial purification to be potable)
# dirty water (needs filtration, may need purification / distillation)
# filtered water (physically filtered off particulates)
    # drinkable, but may still make you sick
# purified water (chemically purified)
    # drinkable, but may still make you sick (lower chance than filtered)
# distilled water (evaporated)
    # drinkable, no risk of sickness
'plastic water filter':{
    # takes 10 minutes to filter 1 liter (1000g or 1KG of water)
    # 1 minute for 100g; 3 seconds for 5g
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_ASSEMBLY,10,), (SKL_PLASTIC,1,),),
    'construct' : 1200,
    'components': (
        [ ('plastic bottle', 2,), ],
        [ ('gravel', 500,), ], # filters the large particles
        [ ('sand', 100,), ], # filters the particulates
        [ ('powdered charcoal', 50,), ], # filters the toxins
        [ ('scrap cloth', 1,), ], # membrane
        [ ('rubber band', 1,), ],
        ),
    'tools'     : ( [ (cmp.Tool_Cut, 5,), ], ),
    'byproducts': ( ('scrap plastic', 4,), ),
    },
'water purification tablet':{ # stretches out the water purification agent
    # water purification agent is tetraglycerine hydroperiodide
    # acts in 5 minutes
    'quantity'  : 20,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_ASSEMBLY,15,),),
    'construct' : 4800,
    'components': (
        [ ('water purification agent', 1,), ],
        [ ('pill filler', 20,), ],
        ),
    'tools'     : (),
    'byproducts': (),
    },

    # light sources
'torch':{
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_ASSEMBLY,1,),),
    'construct' : 800,
    'components': (
        [ ('stick of wood', 1,), ('bone', 1,), ('stick of metal', 1,),
          ('metal tube', 1,), ],
        [ ('piece of cloth', 1,), ('seed pod', 1,), ], # pinecone or some other type of seed/plant? What setting are we playing in?
        [ ('oil', 1,), ('resin', 1,), ('grease', 1,), ],
        ),
    'tools'     : (),
    'byproducts': (),
    },
'torch, large':{
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_ASSEMBLY,1,),),
    'construct' : 1200,
    'components': (
        [ ('stick of wood', 1,), ('bone', 1,), ('stick of metal', 1,),
          ('metal tube', 1,), ],
        [ ('chunk of cloth', 1,), ],
        [ ('oil', 2,), ('resin', 2,), ('grease', 2,), ],
        ),
    'tools'     : (),
    'byproducts': (),
    },
'candle':{
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_ASSEMBLY,1,),),
    'construct' : 400,
    'components': (
        [ ('parcel of wood', 1,), ('parcel of bone', 1,), ('parcel of stone', 1,),
          ('parcel of glass', 1,), ('parcel of metal', 1,),
          ('metal can', 1,), ],
        [ ('string', 1,), ],
        [ ('oil', 1,), ('resin', 1,), ('grease', 1,), ],
        ),
    'tools'     : (),
    'byproducts': (),
    },
'paper lantern':{
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_ASSEMBLY,1,),),
    'construct' : 800,
    'components': (
        [ ('paper', 2,), ],
        [ ('string', 1,), ],
        [ ('oil', 1,), ('resin', 1,), ('grease', 1,), ],
        ),
    'tools'     : (),
    'byproducts': (),
    },
'metal lantern':{
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_METAL,8,), (SKL_ASSEMBLY,1,),),
    'sound'     : 60,
    'construct' : 3200,
    'components': (
        [ ('parcel of metal', 2,), ],
        [ ('metal wire', 2,), ],
        [ ('string', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Furnace, 2,), (cmp.Tool_Torch, 3,), ],
        [ (cmp.Tool_Pliers, 1,), (cmp.Tool_Hammer, 2,), ],
        [ (cmp.Tool_Tongs, 1,), ],
        ),
    'byproducts': (),
    },

    # furnaces
'plastic campfire':{ # Note: make campfire object itself have ReactsWithFire func where it creates a "charred plastic campfire" object that cannot be harvested for the plastic and stone
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_ASSEMBLY,1,),),
    'construct' : 600,
    'components': (
        [ ('chunk of plastic', 1,), ],
        [ ('piece of plastic', 3,), ('plastic bottle', 3,), ('stick of plastic', 3,), ],
        [ ('parcel of plastic', 5,), ('plastic cup', 5,), ],
        [ ('parcel of stone', 12,), ('piece of stone', 6,), ],
        [ ('tinder', 1,), ],
        ),
    'tools'     : ( (cmp.Tool_Torch, 1,), (cmp.Tool_FireStarter, 1,), ),
    'byproducts': (),
    },
'wooden campfire':{ # wooden campfire object could have a function that changes its name to "charred ..." and removes its Harvestable component
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_ASSEMBLY,1,),),
    'construct' : 600,
    'components': (
        [ ('chunk of wood', 1,), ],
        [ ('piece of wood', 3,), ('stick of wood', 3,), ],
        [ ('parcel of wood', 5,), ('twig', 5,), ],
        [ ('parcel of stone', 12,), ('piece of stone', 6,), ],
        [ ('tinder', 1,), ],
        ),
    'tools'     : ( (cmp.Tool_Torch, 1,), (cmp.Tool_FireStarter, 1,), ),
    'byproducts': (),
    },
'clay furnace':{ # level 2 furnace (level 3 furnaces are metal, and cannot be crafted (?) or require machinery to craft.
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_ASSEMBLY,3,),),
    'construct' : 3500,
    'components': (
        [ ('chunk of clay', 15,), ('chunk of stone', 15,), ('slab of clay', 3,), ],
        [ ('chunk of clay', 10,), ('slab of clay', 2,), ],
        [ ('stick of wood', 4,), ],
        ),
    'tools'     : (),
    'byproducts': (),
    },

    # valves
'plastic valve':{
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_ASSEMBLY,5,), (SKL_PLASTIC,1,),),
    'construct' : 2400,
    'durability': 'weakest_link',
    'components': (
        [ ('plastic bottlecap', 2,), ('plastic tube', 1,), ],
        [ ('parcel of tarp', 1,), ('duct tape', 1,), ('parcel of rubber', 1,),
          ('rubber balloon', 1,), ('rubber gasket', 1,), ],
        [ ('rubber band', 1,), ('glue', 1,), ],
        [ ('glue', 1,), ],
        ),
    'tools'     : ( [ (cmp.Tool_Cut, 5,), ], ),
    'byproducts': ( ('scrap plastic', 1,), ),
    },
'leather valve':{
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_ASSEMBLY,15,), (SKL_LEATHER,5,),),
    'construct' : 3600,
    'durability': 'weakest_link',
    'components': (
        [ ('metal tube', 1,), ],
        [ ('rubber gasket', 1,), ('leather gasket', 1,), ],
        [ ('rubber band', 1,), ('glue', 1,), ],
        [ ('glue', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Cut, 6,), ],
        [ (cmp.Tool_Saw, 3,), ],
        [ (cmp.Tool_Drill, 3,), ],
        [ (cmp.Tool_Weld, 1,), (cmp.Tool_Torch, 3,), ],
        ),
    'byproducts': ( ('scrap metal', 1,), ),
    },
'metal valve':{
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_METAL,15,),),
    'construct' : 8800,
    'durability': 'weakest_link',
    'components': (
        [ ('metal pipe', 1,), ],
        [ ('metal gasket', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Saw, 5,), ],
        [ (cmp.Tool_Drill, 4,), ],
        [ (cmp.Tool_Sharpener, 4,), (cmp.Tool_File, 3,), ],
        [ (cmp.Tool_Weld, 2,), ],
        ),
    'byproducts': (
        ('piece of metal', 1,),('parcel of metal', 1,),('scrap metal', 1,),
        ),
    },

    # fluid containers
'plastic tank':{
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_ASSEMBLY,1,), (SKL_PLASTIC,1,),),
    'construct' : 400,
    'durability': 'weakest_link',
    'components': (
        [ ('plastic bottle', 1,), ],
        [ ('rubber valve', 1,), ],
        [ ('glue', 1,), ],
        ),
    'tools'     : ( [ (cmp.Tool_Cut, 5,), ], ),
    'byproducts': (),
    },

    # motors, dynamos
'motor, small':{ # electric motor, gets power from battery
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_ASSEMBLY,2,), (SKL_PLASTIC,1,),),
    'construct' : 1200,
    'components': (
        [ ('plastic cup', 1,), ('parcel of plastic', 1,), ],
        [ ('magnet, weak', 2,), ],
        [ ('metal wire', 2,), ('insulated wire', 2,), ],
        [ ('paperclip', 2,), ('metal wire', 1,), ('insulated wire', 1,), ],
        [ ('glue', 1,),('rubber band', 2,),  ],
        ),
    'tools'     : ( [ (cmp.Tool_Cut, 4,), ], ),
    'byproducts': (),
    },
'dynamo, small':{ # outputs power when you turn the crank
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_ASSEMBLY,3,), (SKL_PLASTIC,3,), (SKL_WOOD,5,),),
    'construct' : 4800,
    'components': (
        [ ('piece of wood', 1,), ],
        [ ('scrap plastic', 2,), ],
        [ ('scrap wood', 2,), ],
        [ ('motor, small', 1,), ],
        [ ('gear, small', 2,), ],
        [ ('gear', 2,), ],
        [ ('glue', 4,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Cut, 6,), ],
        [ (cmp.Tool_Hammer, 3,), ],
        ),
    'byproducts': (),
    },

    # fluid compressors
'plastic compressor':{
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_ASSEMBLY,5,), (SKL_PLASTIC,2,),),
    'construct' : 1200,
    'components': (
        [ ('plastic bottle', 1,), ],
        [ ('plastic valve', 1,), ],
        [ ('motor, small', 1,), ],
        [ ('battery, small', 1,), ],
        [ ('rubber hose', 1,), ],
        [ ('metal wire', 1,), ('insulated wire', 1,), ],
        [ ('glue', 2,), ],
        ),
    'tools'     : ( [ (cmp.Tool_Cut, 5,), ], ),
    'byproducts': (),
    },
##'wooden air compressor':{ # uses wooden barrel or bucket, standard motor, standard battery, etc.

    # shelters
'shelter':{
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_ASSEMBLY,1,),),
    'sound'     : 30,
    'construct' : 4500,
    'components': (
        [ ('stick of plastic', 16,), ('stick of wood', 16,), ], # frame walls
        [ ('pole of plastic', 4,), ('pole of wood', 4,), ], # frame support
        [ ('foliage', 64,), ], # insulation
        [ ('foliage', 64,), ('moss clump', 64,), # water protection
          ('tarp', 4,), ('tarp, large', 1,), ],
        [ ('cordage', 8,), ('rope', 8,),  # connect
          ('zip tie', 32,), ('duct tape', 64,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 1,), ],
        [ (cmp.Tool_Saw, 2,), (cmp.Tool_Chop, 1,), ],
        ), 
    'byproducts': (),
    'recycling' : (),
    },
'wooden shed frame':{
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_WOOD,10,),),
    'sound'     : 120,
    'construct' : 12000,
    'components': (
        [ ('pole of wood', 4,), ],
        [ ('stick of wood', 4,), ],
        [ ('wooden plank', 16,), ('stick of wood', 16,),
          ('pole of wood', 8,), ],
        [ ('nail', 32,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 1,), ],
        [ (cmp.Tool_Saw, 3,), ],
        ), 
    'byproducts': (),
    'recycling' : (),
    },
'wooden shed':{
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_WOOD,10,),),
    'sound'     : 120,
    'construct' : 20000,
    'components': (
        [ ('wooden shed frame', 1,), ],
        [ ('wooden plank', 60,), ('pole of wood', 32,), ],
        [ ('nail', 96,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 1,), ],
        [ (cmp.Tool_Saw, 3,), ],
        ), 
    'byproducts': (),
    'recycling' : (),
    },
'metal shed frame':{
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_METAL,5,),),
    'sound'     : 120,
    'construct' : 12000,
    'components': (
        [ ('pole of metal', 4,), ],
        [ ('stick of metal', 4,), ],
        [ ('wooden plank', 16,), ],
        [ ('nail', 32,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 1,), ],
        [ (cmp.Tool_Saw, 3,), ],
        ), 
    'byproducts': (),
    'recycling' : (),
    },
'metal shed':{
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_METAL,5,),),
    'sound'     : 120,
    'construct' : 20000,
    'components': (
        [ ('metal shed frame', 1,), ],
        [ ('metal sheet', 4,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Cut, 8,), (cmp.Tool_Saw, 4,), ],
        [ (cmp.Tool_Weld, 2,), ],
        ), 
    'byproducts': (),
    'recycling' : (),
    },

    # baskets
'wooden basket':{
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_ASSEMBLY,5,),),
    'construct' : 2000,
    'components': ( [ ('twig', 16,), ], ), # ('frond', 16,),
    'tools'     : (),
    'byproducts': (),
    'recycling' : (),
    },

# NOTE: springs are fucking hard to make mate. They might be too precise to be made for the purposes of this crafting system.
##    # spring anvils
##'spring anvil':{ 
##    'quantity'  : 1,
##    'table'     : CRT_STUFF,
##    'category'  : CRC_METAL,
##    'construct' : 2400,
##    'components': (
##        [ ('metal tube', 1,), ],
##        [ ('scrap metal', 1,), ],
##        [ ('parcel of metal', 1,), ],
##        [ ('plastic table', 1,), ('wooden table', 1,), ('bone table', 1,),
##          ('stone table', 1,), ('metal table', 1,), ],
##        ),
##    'tools'     : (
##        [ (cmp.Tool_Pliers, 1,), ],
##        [ (cmp.Tool_Weld, 2,), ],
##        ),
##    'byproducts': (),
##    'recycling' : (),
##    },
##
##    # springs
##'torsion spring':{ 
##    'quantity'  : 1,
##    'table'     : CRT_STUFF,
##    'category'  : CRC_ASSEMBLY,
##    'construct' : 2400,
##    'components': (
##        [ ('metal wire, thick', 1,), ],
##        ),
##    'tools'     : (
##        [ (cmp.Tool_Pliers, 1,), ],
##        [ (cmp.Tool_SpringAnvil, 1,), ],
##        ),
##    'byproducts': (),
##    'recycling' : (),
##    },

    # traps
'trap, small':{ #maybe baiting is handled separately. You can bait any kind of bait on any trap and the type of bait influences what is attracted to it.
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_ASSEMBLY,1,),),
    'construct' : 300,
    'components': (
        [ ('wooden basket', 1,), ],
        [ ('twig', 1,), ],
##        [ ('corpse of bug', 1,), ],
        ),
    'tools'     : (), 
    'byproducts': (),
    'recycling' : (),
    },
'trap, net':{
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_ASSEMBLY,6,),),
    'construct' : 500,
    'components': (
        [ ('net', 1,), ],
        [ ('rope', 40,), ],
##        [ ('parcel of flesh', 1,), ],
        ),
    'tools'     : (), 
    'byproducts': (),
    'recycling' : (),
    },
'trap, pit':{ # large pit trap must be built inside of a pit
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_ASSEMBLY,8,),),
    'construct' : 3000,
    'terrain'   : 'pit',
    'components': (
        [ ('wooden stake', 6,),
          ('plastic javelin', 6,), ('wooden javelin', 6,), ('metal javelin', 6,),
          ('plastic shortspear', 6,), ('wooden shortspear', 6,), ('stone shortspear', 6,), ('bone shortspear', 6,), ('metal shortspear', 6,), ('glass shortspear', 6,),
          ('plastic spear', 6,), ('wooden spear', 6,), ('stone spear', 6,), ('bone spear', 6,), ('metal spear', 6,), ('glass spear', 6,), ],
        [ ('stick of wood', 6,), ],
        [ ('foliage', 12,), ],
##        [ ('hearty root', 1,), ], # bait for larger creatures
        ),
    'tools'     : (), 
    'byproducts': (),
    'recycling' : (),
    },

    # medicine
'bandage':{
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_ASSEMBLY,5,), (SKL_CLOTH,1,),),
    'construct' : 300,
    'components': (
        [ ('parcel of cloth', 1,), ],
        [ ('parcel of tarp', 1,), ('rubber balloon', 1,), ],
        [ ('glue', 1,), ],
        ),
    'tools'     : ( [ (cmp.Tool_Cut, 3,), ], ),
    'byproducts': (),
    },

    # string -> cordage -> rope -> cable
    # chains
'string':{ # thin cordage, supports 1kg (a single thread is not worth being an item, and it would support like 10g)
    'quantity'  : 3,
    'table'     : CRT_RAWMATS,
    'skills'    : ((SKL_ASSEMBLY,3,),),
    'construct' : 2400, # in reality takes several hours from start-finish.. But, this would make string-making from sinews pretty worthless.
    'mass'      : 'fixed', # mass irrespective of components
    'components': (
        [ ('sinew', 1,), ], #technically tendons should be dried.
        ),
    'tools'     : (
        [ (cmp.Tool_Cut, 6,), ],
        [ (cmp.Tool_Hammer, 3,), ],
        ),
    'byproducts': ( ('animal fat', 1,), ),
    },
'cordage':{ # thin rope, supports 10kg
    'quantity'  : 1,
    'table'     : CRT_RAWMATS,
    'skills'    : ((SKL_ASSEMBLY,3,),),
    'construct' : 1800,
    'mass'      : 'fixed', # mass irrespective of components
    'components': (
        [ ('fibrous leaf', 3,), ('twig', 6,), ('string', 9,), ],
        ),
    'tools'     : (),
    'byproducts': (),
    },
'rope':{ # rope, supports 150kg
    'quantity'  : 1,
    'table'     : CRT_RAWMATS,
    'skills'    : ((SKL_ASSEMBLY,4,),),
    'construct' : 2400,
    'mass'      : 'fixed', # mass irrespective of components
    'components': (
        [ ('cordage', 9,), ],
        ),
    'tools'     : (),
    'byproducts': (),
    },
'cable':{ # thick rope, supports 500kg
    'quantity'  : 1,
    'table'     : CRT_RAWMATS,
    'skills'    : ((SKL_ASSEMBLY,5,),),
    'construct' : 2400,
    'components': (
        [ ('rope', 3,), ],
        ),
    'tools'     : (),
    'byproducts': (),
    },
'chain link, small':{
    'quantity'  : 16,
    'table'     : CRT_RAWMATS,
    'skills'    : ((SKL_METAL,10,),),
    'sound'     : 120,
    'construct' : 500,
    'durability': 'fixed',
    'mass'      : 'fixed',
    'components': (
        [ ('parcel of metal', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 3,), ],
        [ (cmp.Tool_Crucible, 2,), ],
        [ (cmp.Tool_Anvil, 3,), ],
        [ (cmp.Tool_Tongs, 2,), ],
        [ (cmp.Tool_Furnace, 1,), (cmp.Tool_Torch, 2,), ],
        [ (cmp.Mold_ChainLinkLight, 1,), ],
        ),
    'byproducts': (),
    },
'chain, small':{ # light 5mm chain, supports 200kg
    'quantity'  : 1,
    'table'     : CRT_RAWMATS,
    'skills'    : ((SKL_METAL,8,),),
    'sound'     : 120,
    'construct' : 9600,
    'durability': 'weakest_link',
    'mass'      : 'fixed',
    'components': (
        [ ('chain link, small', 200,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 4,), ],
        [ (cmp.Tool_Weld, 3,), ],
        [ (cmp.Tool_Pliers, 2,), (cmp.Tool_Anvil, 3,), ],
        [ (cmp.Tool_Tongs, 1,), ],
        ),
    'byproducts': (),
    },
'chain link':{
    'quantity'  : 8,
    'table'     : CRT_RAWMATS,
    'skills'    : ((SKL_METAL,12,),),
    'sound'     : 120,
    'construct' : 600,
    'durability': 'fixed',
    'mass'      : 'fixed',
    'components': (
        [ ('parcel of metal', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Furnace, 2,), (cmp.Tool_Torch, 3,), ],
        [ (cmp.Tool_Anvil, 3,), ],
        [ (cmp.Tool_Hammer, 2,), ],
        [ (cmp.Tool_Crucible, 2,), ],
        [ (cmp.Tool_Tongs, 2,), ],
        [ (cmp.Mold_ChainLink, 1,), ],
        ),
    'byproducts': (),
    },
'chain':{ # standard 10mm chain, supports 1000kg
    'quantity'  : 1,
    'table'     : CRT_RAWMATS,
    'skills'    : ((SKL_METAL,10,),),
    'sound'     : 120,
    'construct' : 7200,
    'durability': 'weakest_link',
    'mass'      : 'fixed',
    'components': (
        [ ('chain link', 100,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 3,), ],
        [ (cmp.Tool_Furnace, 2,), (cmp.Tool_Weld, 2,), ],
        [ (cmp.Tool_Pliers, 2,), (cmp.Tool_Anvil, 3,), ],
        [ (cmp.Tool_Tongs, 1,), ],
        ),
    'byproducts': (),
    },
'chain link, large':{
    'quantity'  : 2,
    'table'     : CRT_RAWMATS,
    'skills'    : ((SKL_METAL,15,),),
    'sound'     : 120,
    'construct' : 800,
    'durability': 'fixed',
    'mass'      : 'fixed',
    'components': (
        [ ('parcel of metal', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Furnace, 3,), (cmp.Tool_Torch, 3,), ],
        [ (cmp.Tool_Hammer, 2,), ],
        [ (cmp.Tool_Crucible, 2,), ],
        [ (cmp.Tool_Tongs, 2,), ],
        [ (cmp.Tool_Anvil, 2,), ],
        [ (cmp.Mold_ChainLinkHeavy, 1,), ],
        ),
    'byproducts': (),
    },
'chain, large':{ # heavy duty 20mm chain, supports 5000kg
    'quantity'  : 1,
    'table'     : CRT_RAWMATS,
    'skills'    : ((SKL_METAL,12,),),
    'sound'     : 120,
    'construct' : 4800,
    'durability': 'weakest_link',
    'mass'      : 'fixed',
    'components': (
        [ ('chain link, large', 50,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Furnace, 2,), (cmp.Tool_Weld, 2,), ],
        [ (cmp.Tool_Hammer, 2,), ],
        [ (cmp.Tool_Anvil, 2,), (cmp.Tool_Pliers, 3,), ],
        [ (cmp.Tool_Tongs, 2,), ],
        ),
    'byproducts': (),
    },

    # fishing
'fishing hook':{
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_ASSEMBLY,1,),),
    'construct' : 500,
    'components': (
        [ ('fibrous leaf', 1,), ],
        ),
    'tools'     : ( (cmp.Tool_Cut, 5,), ),
    'byproducts': (),
    },
'plastic fishing hook':{
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_PLASTIC,5,),),
    'construct' : 400,
    'components': (
        [ ('scrap plastic', 1,), ('shard of plastic', 1,), ],
        ),
    'tools'     : ( (cmp.Tool_Cut, 4,), ),
    'byproducts': (),
    },
'wooden fishing hook':{
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_WOOD,15,),),
    'construct' : 800,
    'components': (
        [ ('scrap wood', 1,), ('shard of wood', 1,), ],
        ),
    'tools'     : ( (cmp.Tool_Cut, 5,), ),
    'byproducts': (),
    },
'stone fishing hook':{
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_STONE,35,),),
    'construct' : 1400,
    'components': (
        [ ('shard of stone', 1,), ],
        ),
    'tools'     : (
        (cmp.Tool_Chisel, 3,),
        (cmp.Tool_Drill, 3,),
        (cmp.Tool_Hammer, 2,),
        ),
    'byproducts': (),
    },
'bone fishing hook':{
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_BONE,25,),),
    'construct' : 1000,
    'components': (
        [ ('scrap bone', 1,), ('shard of bone', 1,), ],
        ),
    'tools'     : (
        (cmp.Tool_Chisel, 2,),
        (cmp.Tool_Drill, 2,),
        (cmp.Tool_Hammer, 2,),
        ),
    'byproducts': (),
    },
'metal fishing hook':{
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_METAL,10,),),
    'construct' : 1200,
    'components': (
        [ ('scrap metal', 1,), ('paperclip', 1,), ('pop tab', 1,),
          ('metal needle', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 4,), ],
        [ (cmp.Tool_Pliers, 2,), (cmp.Tool_Anvil, 1,), ],
        ),
    'byproducts': (),
    },
'fishing rod':{ # should fishing rod and baited fishing rod be different objects? And same with traps and baited traps? Or is it fine to just abstract baiting away?
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_ASSEMBLY,5,),),
    'durability': 'sum',
    'construct' : 600,
    'components': (
        [ ('pole of plastic', 1,), ('pole of wood', 1,),
          ('pole of metal', 1,), ],
        [ ('fishing hook', 1,),
          ('plastic fishing hook', 1,), ('wooden fishing hook', 1,),
          ('stone fishing hook', 1,), ('bone fishing hook', 1,),
          ('glass fishing hook', 1,), ('metal fishing hook', 1,), ],
        [ ('cordage', 5,), ('fishing wire', 1,), ],
        ),
    'tools'     : (),
    'byproducts': (),
    },

    # magnets
'magnet, weak':{ # cannot make a strong magnet, it's necessary to have neodymium which is too pure to craft
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_ASSEMBLY,1,),),
    'construct' : 1000,
    'components': (
        [ ('parcel of metal', 1,), ],
        [ ('magnet, weak', 1,), ('magnet, strong', 1,), ],
        ),
    'tools'     : (),
    'byproducts': (),
    },
'electromagnet':{ 
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_ASSEMBLY,8,),), # coil the wire around the metal, connect to battery (?)
    'construct' : 1500,
    'components': (
        [ ('parcel of metal', 1,), ],
        [ ('metal wire', 1,), ],
        [ ('battery, small', 1,), ],
        ),
    'tools'     : ( [ (cmp.Tool_Pliers, 1,), ], ),
    'byproducts': (),
    },






    #--------------------------#
    #         Headgear         #
    #--------------------------#

    # cloth
'padded coif':{
    'quantity'  : 1,
    'table'     : CRT_ARMOR,
    'skills'    : ((SKL_CLOTH,20,),),
    'construct' : 14400,
    'components': (
        [ ('chunk of cloth', 1,), ],
        [ ('piece of cloth', 2,), ],
        [ ('string', 24,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Cut, 6,), ],
        [ (cmp.Tool_Sew, 2,), ],
        ),
    'byproducts': (),
    },
'padded coif, heavy':{
    'quantity'  : 1,
    'table'     : CRT_ARMOR,
    'skills'    : ((SKL_CLOTH,25,),),
    'construct' : 24000,
    'components': (
        [ ('chunk of cloth', 3,), ],
        [ ('string', 32,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Cut, 6,), ],
        [ (cmp.Tool_Sew, 2,), ],
        ),
    'byproducts': (),
    },

    # plastic
'respirator':{
    'quantity'  : 1,
    'table'     : CRT_ARMOR,
    'skills'    : ((SKL_ASSEMBLY,15,),),
    'construct' : 4800,
    'components': (
        [ ('plastic mask', 1,), ('wooden mask', 1,), ('bone mask', 1,),
          ('leather mask', 1,), ('boiled leather mask', 1,), ],
        [ ('piece of cloth', 1,), ], # or some other porous sheet w/ tiny holes
        [ ('piece of rubber', 1,), ],
        [ ('metal can', 2,), ('plastic tube', 1,), ],
        [ ('activated carbon', 4,), ],
        [ ('glue', 2,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Cut, 7,), ],
        [ (cmp.Tool_Drill, 1,), ],
        ),
    'byproducts': (),
    },

    # metal
'metal respirator':{
    'quantity'  : 1,
    'table'     : CRT_ARMOR,
    'skills'    : ((SKL_ASSEMBLY,15,), (SKL_METAL,10,),),
    'construct' : 9600,
    'components': (
        [ ('metal mask', 1,), ],
        [ ('piece of cloth', 1,), ],
        [ ('piece of rubber', 1,), ],
        [ ('metal can', 2,), ('metal tube', 1,), ],
        [ ('activated carbon', 4,), ],
        [ ('glue', 2,), ], # to connect the rubber to the mask to make an airtight seal
        ),
    'tools'     : (
        [ (cmp.Tool_Cut, 5,), ],
        [ (cmp.Tool_Drill, 2,), ],
        [ (cmp.Tool_Weld, 1,), (cmp.Tool_Torch, 3,), ],
        ),
    'byproducts': (),
    },






    #--------------------------#
    #          Armor           #
    #--------------------------#



    # cloth
't-shirt':{
    'quantity'  : 1,
    'table'     : CRT_ARMOR,
    'skills'    : ((SKL_CLOTH,5,),),
    'construct' : 800,
    'components': (
        [ ('piece of cloth', 1,), ],
        [ ('string', 8,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Cut, 4,), ],
        [ (cmp.Tool_Sew, 1,), ],
        ),
    'byproducts': ( ('parcel of cloth', 1,), ),
    },
'hoody':{
    'quantity'  : 1,
    'table'     : CRT_ARMOR,
    'skills'    : ((SKL_CLOTH,10,),),
    'construct' : 2400,
    'components': (
        [ ('piece of cloth', 4,), ],
        [ ('string', 24,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Cut, 4,), ],
        [ (cmp.Tool_Sew, 1,), ],
        ),
    'byproducts': ( ('parcel of cloth', 2,), ),
    },
'cloth vest':{
    'quantity'  : 1,
    'table'     : CRT_ARMOR,
    'skills'    : ((SKL_CLOTH,10,),),
    'construct' : 7200,
    'components': (
        [ ('piece of cloth', 3,), ],
        [ ('string', 16,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Cut, 5,), ],
        [ (cmp.Tool_Sew, 1,), ],
        ),
    'byproducts': (),
    },
'cloth vest, heavy':{
    'quantity'  : 1,
    'table'     : CRT_ARMOR,
    'skills'    : ((SKL_CLOTH,15,),),
    'construct' : 14400,
    'components': (
        [ ('chunk of cloth', 4,), ],
        [ ('string', 64,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Cut, 6,), ],
        [ (cmp.Tool_Sew, 1,), ],
        ),
    'byproducts': (),
    },
'padded jacket':{
    'quantity'  : 1,
    'table'     : CRT_ARMOR,
    'skills'    : ((SKL_CLOTH,20,),),
    'construct' : 28800,
    'components': (
        [ ('chunk of cloth', 5,), ], # ('t-shirt', 25,),
        [ ('string', 64,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Cut, 6,), ],
        [ (cmp.Tool_Sew, 2,), ],
        ),
    'byproducts': (),
    },
'padded jack':{
    'quantity'  : 1,
    'table'     : CRT_ARMOR,
    'skills'    : ((SKL_CLOTH,25,),),
    'construct' : 43200,
    'components': (
        [ ('chunk of cloth', 10,), ], #  ('t-shirt', 50,),
        [ ('string', 128,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Cut, 6,), ],
        [ (cmp.Tool_Sew, 2,), ],
        ),
    'byproducts': (),
    },
'gambeson':{
    'quantity'  : 1,
    'table'     : CRT_ARMOR,
    'skills'    : ((SKL_CLOTH,30,),),
    'construct' : 86400, #57600
    'components': (
        [ ('chunk of cloth', 16,), ], # ('t-shirt', 80,),
        [ ('string', 256,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Cut, 6,), ],
        [ (cmp.Tool_Sew, 2,), ],
        ),
    'byproducts': (),
    },
'arming doublet':{
    'quantity'  : 1,
    'table'     : CRT_ARMOR,
    'skills'    : ((SKL_LEATHER,10,), (SKL_CLOTH,5,), (SKL_ARMORSMITH,5,),),
    'construct' : 8000,
    'components': (
        [ ('padded jack', 1,), ],
        [ ('scrap leather', 16,), ],
        [ ('string', 16,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Cut, 6,), ],
        [ (cmp.Tool_Sew, 2,), ],
        ),
    'byproducts': (),
    },

    # leather
'leather jacket':{
    'quantity'  : 1,
    'table'     : CRT_ARMOR,
    'skills'    : ((SKL_LEATHER,15,),),
    'construct' : 14400,
    'components': (
        [ ('piece of leather', 8,), ('leather hide', 2,), ],
        [ ('string', 64,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Cut, 6,), ],
        [ (cmp.Tool_Hammer, 2,), ],
        [ (cmp.Tool_Sew, 2,), ],
        [ (cmp.Tool_Anvil, 1,), ],
        ),
    'byproducts': ( ('parcel of leather', 2,), ),
    },

    # boiled leather
'boiled leather gear':{
    'quantity'  : 1,
    'table'     : CRT_ARMOR,
    'skills'    : ((SKL_LEATHER,15,), (SKL_ARMORSMITH,10,),),
    'construct' : 86400,
    'components': (
        [ ('parcel of boiled leather', 150,), ],
        [ ('string', 128,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Cut, 6,), ],
        [ (cmp.Tool_Hammer, 2,), ],
        [ (cmp.Tool_Sew, 2,), ],
        [ (cmp.Tool_Anvil, 1,), ],
        ),
    'byproducts': ( ('parcel of boiled leather', 2,), ),
    },

    # plastic
'disposable PPE':{
    'quantity'  : 1,
    'table'     : CRT_ARMOR,
    'skills'    : ((SKL_ASSEMBLY,10,),),
    'construct' : 1600,
    'components': (
        [ ('tarp', 6,), ],
        ),
    'tools'     : ( [ (cmp.Tool_Cut, 3,), ], ),
    'byproducts': (),
    },
'plastic gear':{ # lamellar armor
    'quantity'  : 1,
    'table'     : CRT_ARMOR,
    'skills'    : ((SKL_ARMORSMITH,20,), (SKL_PLASTIC,15,),),
    'construct' : 57600,
    'components': (
        [ ('parcel of plastic', 75,), ],
        [ ('string', 128,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Cut, 6,), ],
        [ (cmp.Tool_Saw, 2,), ],
        [ (cmp.Tool_Hammer, 2,), ],
        [ (cmp.Tool_Drill, 2,), ],
        [ (cmp.Tool_Sew, 2,), ],
        [ (cmp.Tool_Chisel, 1,), ],
        ),
    'byproducts': (
        ('parcel of plastic', 5,), ('scrap plastic', 5,),
        ('parcel of cloth', 2,),
        ),
    },

    # wood
'wooden gear':{
    'quantity'  : 1,
    'table'     : CRT_ARMOR,
    'skills'    : ((SKL_ARMORSMITH,25,), (SKL_WOOD,20,),),
    'construct' : 86400,
    'components': (
        [ ('parcel of wood', 60,), ],
        [ ('piece of leather', 2,), ],
        [ ('string', 256,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Cut, 6,), ],
        [ (cmp.Tool_Saw, 2,), ],
        [ (cmp.Tool_Hammer, 2,), ],
        [ (cmp.Tool_Drill, 2,), ],
        [ (cmp.Tool_Sew, 2,), ],
        [ (cmp.Tool_Chisel, 1,), ],
        ),
    'byproducts': ( ('scrap wood', 5,), ),
    },

    # bone
'bone gear':{
    'quantity'  : 1,
    'table'     : CRT_ARMOR,
    'skills'    : ((SKL_ARMORSMITH,30,), (SKL_BONE,40,),),
    'construct' : 100800,
    'components': (
        [ ('parcel of bone', 120,), ],
        [ ('piece of leather', 2,), ],
        [ ('string', 256,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Cut, 6,), ],
        [ (cmp.Tool_Saw, 3,), ],
        [ (cmp.Tool_Hammer, 2,), ],
        [ (cmp.Tool_Drill, 2,), ],
        [ (cmp.Tool_Sew, 2,), ],
        [ (cmp.Tool_Chisel, 1,), ],
        ),
    'byproducts': ( ('scrap bone', 5,), ),
    },
'bone armor':{
    'quantity'  : 1,
    'table'     : CRT_ARMOR,
    'skills'    : ((SKL_ARMORSMITH,20,), (SKL_BONE,20,),),
    'construct' : 57600,
    'components': (
        [ ('piece of bone', 32,), ('bone', 64,), ],
        [ ('arming doublet', 1,), ('leather jacket, heavy', 1,), ],
        [ ('string', 128,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Saw, 3,), ],
        [ (cmp.Tool_Hammer, 2,), ],
        [ (cmp.Tool_Drill, 2,), ],
        [ (cmp.Tool_Sew, 2,), ],
        [ (cmp.Tool_Chisel, 1,), ],
        ),
    'byproducts': ( ('scrap bone', 5,), ),
    },

    # metal
'pop tab mail vest':{
    'quantity'  : 1,
    'table'     : CRT_ARMOR,
    'skills'    : ((SKL_ARMORSMITH,10,),),
    'construct' : 8800,
    'components': (
        [ ('pop tab mail ring', 768,), ],
        [ ('padded jack', 1,), ],
        ),
    'tools'     : (),
    'byproducts': (),
    },
'pop tab mail shirt':{
    'quantity'  : 1,
    'table'     : CRT_ARMOR,
    'skills'    : ((SKL_ARMORSMITH,10,),),
    'construct' : 7200,
    'components': (
        [ ('pop tab mail vest', 1,), ],
        [ ('pop tab mail ring', 512,), ],
        ),
    'tools'     : (),
    'byproducts': (),
    },
'metal mail vest':{
    'quantity'  : 1,
    'table'     : CRT_ARMOR,
    'skills'    : ((SKL_ARMORSMITH,25,),),
    'construct' : 14400,
    'components': (
        [ ('mail ring, riveted', 320,), ('mail ring, welded', 320,), ],
        [ ('padded jack', 1,), ],
        ),
    'tools'     : (),
    'byproducts': (),
    },
'metal mail shirt':{
    'quantity'  : 1,
    'table'     : CRT_ARMOR,
    'skills'    : ((SKL_ARMORSMITH,25,),),
    'construct' : 12000,
    'components': (
        [ ('metal mail vest', 1,), ],
        [ ('mail ring, riveted', 196,), ('mail ring, welded', 196,), ],
        ),
    'tools'     : (),
    'byproducts': (),
    },
'metal cap':{
    'quantity'  : 1,
    'table'     : CRT_ARMOR,
    'skills'    : ((SKL_ARMORSMITH,10,), (SKL_METAL,15,),),
    'sound'     : 120,
    'construct' : 8000,
    'components': (
        [ ('parcel of metal', 15,), ('piece of metal', 3,), ],
        [ ('chunk of cloth', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Anvil, 3,), ],
        [ (cmp.Tool_Hammer, 3,), ],
        [ (cmp.Tool_Crucible, 2,), ],
        [ (cmp.Tool_Furnace, 2,), ],
        [ (cmp.Tool_Tongs, 2,), ],
        ),
    'byproducts': (),
    },
'metal mask':{
    'quantity'  : 1,
    'table'     : CRT_ARMOR,
    'skills'    : ((SKL_ARMORSMITH,15,), (SKL_METAL,25,),),
    'sound'     : 120,
    'construct' : 24000,
    'components': (
        [ ('parcel of metal', 12,), ('piece of metal', 3,), ],
        [ ('parcel of leather', 3,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 5,), ],
        [ (cmp.Tool_Anvil, 3,), ],
        [ (cmp.Tool_Crucible, 2,), ],
        [ (cmp.Tool_Furnace, 2,), (cmp.Tool_Torch, 3,), ],
        [ (cmp.Tool_Tongs, 2,), ],
        ),
    'byproducts': (),
    },





    #--------------------------#
    #          Ammo            #
    #--------------------------#


    # arrows
'plastic primitive arrow':{ # arrow name and stats determined by the material type of the arrowhead, not the shaft. But, since the shaft is the first component, whatever material the shaft is will be the material type of the arrow itself, regardless of the name.
    'quantity'  : 1,
    'table'     : CRT_AMMO,
    'skills'    : ((SKL_ASSEMBLY,1,),),
    'construct' : 500,
    'components': (
        [ ('twig', 1,), ('plastic tube', 1,), ],
        [ ('plastic arrowhead', 1,), ],
        [ ('string', 1,), ('glue', 1,), ('rubber band', 1,),
          ('sinew', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Cut, 3,), ],
        ),
    'byproducts': (),
    },
'wooden primitive arrow':{
    'quantity'  : 1,
    'table'     : CRT_AMMO,
    'skills'    : ((SKL_ASSEMBLY,1,),),
    'construct' : 500,
    'components': (
        [ ('twig', 1,), ('plastic tube', 1,), ],
        [ ('wooden arrowhead', 1,), ],
        [ ('string', 1,), ('glue', 1,), ('rubber band', 1,),
          ('sinew', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Cut, 4,), ],
        ),
    'byproducts': (),
    },
'bone primitive arrow':{
    'quantity'  : 1,
    'table'     : CRT_AMMO,
    'skills'    : ((SKL_ASSEMBLY,1,),),
    'construct' : 500,
    'components': (
        [ ('twig', 1,), ('plastic tube', 1,), ],
        [ ('bone arrowhead', 1,), ],
        [ ('string', 1,), ('glue', 1,), ('rubber band', 1,),
          ('sinew', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Cut, 4,), ],
        ),
    'byproducts': (),
    },
'stone primitive arrow':{
    'quantity'  : 1,
    'table'     : CRT_AMMO,
    'skills'    : ((SKL_ASSEMBLY,1,),),
    'construct' : 500,
    'components': (
        [ ('twig', 1,), ('plastic tube', 1,), ],
        [ ('stone arrowhead', 1,), ],
        [ ('string', 1,), ('glue', 1,), ('sinew', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Cut, 4,), ],
        ),
    'byproducts': (),
    },
'metal primitive arrow':{
    'quantity'  : 1,
    'table'     : CRT_AMMO,
    'skills'    : ((SKL_ASSEMBLY,2,),),
    'construct' : 500,
    'components': (
        [ ('twig', 1,), ('plastic tube', 1,), ],
        [ ('metal arrowhead', 1,), ],
        [ ('string', 1,), ('sinew', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Cut, 4,), ],
        ),
    'byproducts': (),
    },
'glass primitive arrow':{
    'quantity'  : 1,
    'table'     : CRT_AMMO,
    'skills'    : ((SKL_ASSEMBLY,3,),),
    'construct' : 500,
    'components': (
        [ ('twig', 1,), ('plastic tube', 1,), ],
        [ ('glass arrowhead', 1,), ],
        [ ('string', 1,), ('glue', 1,), ('sinew', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Cut, 4,), ],
        ),
    'byproducts': (),
    },
'plastic arrow':{
    'quantity'  : 1,
    'table'     : CRT_AMMO,
    'skills'    : ((SKL_FLETCHER,5,), (SKL_PLASTIC,1,),),
    'construct' : 1000,
    'components': (
        [ ('twig', 1,), ('plastic tube', 1,), ],
        [ ('plastic arrowhead', 1,), ],
        [ ('scrap plastic', 1,), ('feather', 1,), ],
        [ ('string', 1,), ('sinew', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Cut, 4,), ],
        ),
    'byproducts': (),
    },
'wooden arrow':{
    'quantity'  : 1,
    'table'     : CRT_AMMO,
    'skills'    : ((SKL_FLETCHER,8,), (SKL_WOOD,3,),),
    'construct' : 1500,
    'components': (
        [ ('twig', 1,), ],
        [ ('wooden arrowhead', 1,), ],
        [ ('scrap plastic', 1,), ('feather', 1,), ],
        [ ('string', 1,), ('sinew', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Cut, 4,), ],
        ),
    'byproducts': (),
    },
'bone arrow':{
    'quantity'  : 1,
    'table'     : CRT_AMMO,
    'skills'    : ((SKL_FLETCHER,10,), (SKL_BONE,5,),),
    'construct' : 1500,
    'components': (
        [ ('twig', 1,), ],
        [ ('bone arrowhead', 1,), ],
        [ ('scrap plastic', 1,), ('feather', 1,), ],
        [ ('string', 1,), ('sinew', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Cut, 4,), ],
        ),
    'byproducts': (),
    },
'stone arrow':{
    'quantity'  : 1,
    'table'     : CRT_AMMO,
    'skills'    : ((SKL_FLETCHER,10,), (SKL_STONE,5,),),
    'construct' : 1500,
    'components': (
        [ ('twig', 1,), ],
        [ ('stone arrowhead', 1,), ],
        [ ('scrap plastic', 1,), ('feather', 1,), ],
        [ ('string', 1,), ('sinew', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Cut, 4,), ],
        ),
    'byproducts': (),
    },
'metal arrow':{
    'quantity'  : 1,
    'table'     : CRT_AMMO,
    'skills'    : ((SKL_FLETCHER,10,), (SKL_METAL,5,),),
    'construct' : 3000,
    'components': (
        [ ('twig', 1,), ],
        [ ('metal arrowhead', 1,), ],
        [ ('scrap plastic', 1,), ('feather', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Cut, 4,), ],
        [ (cmp.Tool_Hammer, 2,), ],
        ),
    'byproducts': (),
    },
'glass arrow':{
    'quantity'  : 1,
    'table'     : CRT_AMMO,
    'skills'    : ((SKL_FLETCHER,10,), (SKL_GLASS,3,),),
    'construct' : 2000,
    'components': (
        [ ('twig', 1,), ],
        [ ('glass arrowhead', 1,), ],
        [ ('scrap plastic', 1,), ('feather', 1,), ],
        [ ('string', 1,), ('sinew', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Cut, 4,), ],
        ),
    'byproducts': (),
    },

    # bullets
'metal bullet, small':{ 
    'quantity'  : 2,
    'table'     : CRT_AMMO,
    'skills'    : ((SKL_METAL,10,),),
    'construct' : 1000,
    'components': ( [ ('parcel of metal', 1,), ], ),
    'tools'     : (
        [ (cmp.Mold_BulletSmall, 1,), ], # should this be a tool or something else?
        [ (cmp.Tool_Furnace, 3,), ],
        [ (cmp.Tool_Crucible, 2,), ],
        [ (cmp.Tool_Tongs, 2,), ],
        ),
    'byproducts': (),
    },
'metal bullet':{
    'quantity'  : 1,
    'table'     : CRT_AMMO,
    'skills'    : ((SKL_METAL,8,),),
    'construct' : 1000,
    'components': ( [ ('parcel of metal', 1,), ], ),
    'tools'     : (
        [ (cmp.Mold_Bullet, 1,), ],
        [ (cmp.Tool_Furnace, 3,), ],
        [ (cmp.Tool_Crucible, 2,), ],
        [ (cmp.Tool_Tongs, 2,), ],
        ),
    'byproducts': (),
    },
'metal bullet, large':{
    'quantity'  : 1,
    'table'     : CRT_AMMO,
    'skills'    : ((SKL_METAL,6,),),
    'construct' : 1400,
    'components': ( [ ('parcel of metal', 2,), ], ),
    'tools'     : (
        [ (cmp.Mold_BulletLarge, 1,), ],
        [ (cmp.Tool_Furnace, 3,), ],
        [ (cmp.Tool_Crucible, 2,), ],
        [ (cmp.Tool_Tongs, 2,), ],
        ),
    'byproducts': (),
    },
'Minni ball':{
    'quantity'  : 1,
    'table'     : CRT_AMMO,
    'skills'    : ((SKL_METAL,16,),),
    'construct' : 1000,
    'components': ( [ ('parcel of metal', 1,), ], ),
    'tools'     : (
        [ (cmp.Mold_MinniBall, 1,), ],
        [ (cmp.Tool_Furnace, 3,), ],
        [ (cmp.Tool_Crucible, 2,), ],
        [ (cmp.Tool_Tongs, 2,), ],
        ),
    'byproducts': (),
    },
'paper cartridge':{
    'quantity'  : 1,
    'table'     : CRT_AMMO,
    'skills'    : ((SKL_ASSEMBLY,6,),),
    'construct' : 800,
    'components': (
        [ ('metal bullet', 1,), ('Minni ball', 1,), ],
        [ ('paper', 1,), ],
        [ ('gunpowder', 1,), ],
        ),
    'tools'     : (),
    'byproducts': (),
    },





    #--------------------------#
    #          Tools           #
    #--------------------------#


    # anvils
'stone anvil':{ # anvil level 2
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_STONE,15,),),
    'construct' : 7200,
    'components': (
        [ ('slab of stone', 1,), ('cuboid of stone', 1,), ('boulder', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Chisel, 3,), ],
        [ (cmp.Tool_Hammer, 2,), ],
        ),
    'byproducts': ( ('slab of stone', 1,), ('chunk of stone', 1,), ),
    },
'metal anvil, small':{ # anvil level 3
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_METAL,25,),),
    'sound'     : 120,
    'construct' : 57600,
    'components': (
        [ ('parcel of metal', 100,), ('piece of metal', 20,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Furnace, 3,), ],
        [ (cmp.Tool_Crucible, 3,), ],
        [ (cmp.Tool_Tongs, 3,), ],
        ),
    'byproducts': (),
    },
'metal anvil':{ # anvil level 4
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_METAL,35,),),
    'sound'     : 120,
    'construct' : 86400,
    'components': (
        [ ('parcel of metal', 500,), ('piece of metal', 100,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Furnace, 4,), ],
        [ (cmp.Tool_Crucible, 3,), ],
        [ (cmp.Tool_Tongs, 3,), ],
        ),
    'byproducts': (),
    },
'metal anvil, large':{ # anvil level 5
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_METAL,45,),),
    'sound'     : 120,
    'construct' : 172800,
    'components': (
        [ ('parcel of metal', 2000,), ('piece of metal', 400,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Furnace, 4,), ],
        [ (cmp.Tool_Crucible, 3,), ],
        [ (cmp.Tool_Tongs, 3,), ],
        ),
    'byproducts': (),
    },

    # axes - plastic or wooden handle with a head of MATERIAL. Chopping implement with secondary chiseling, hammering ability. Distinct from HATCHETS, which are composed of entirely one material.
'plastic axe':{
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_PLASTIC,5,),),
    'sound'     : 60,
    'construct' : 2400,
    'components': (
        [ ('piece of plastic', 1,), ],
        [ ('stick of plastic', 1,), ('stick of wood', 1,), ],
        [ ('cordage', 2,), ('glue', 2,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 1,), ],
        [ (cmp.Tool_Chisel, 1,), (cmp.Tool_Furnace, 1,), (cmp.Tool_Torch, 3,), ],
        [ (cmp.Tool_Sharpener, 1,), ],
        ),
    'byproducts': ( ('scrap plastic', 1), ),
    },
'wooden axe':{
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_WOOD,5,),),
    'sound'     : 60,
    'construct' : 4800,
    'components': (
        [ ('piece of wood', 1,), ],
        [ ('stick of plastic', 1,), ('stick of wood', 1,), ],
        [ ('cordage', 2,), ('glue', 2,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 2,), ],
        [ (cmp.Tool_Chisel, 2,), ],
        [ (cmp.Tool_Chop, 1,), ],
        [ (cmp.Tool_Sharpener, 1,), ],
        ),
    'byproducts': ( ('parcel of wood', 1), ('scrap wood', 1), ),
    },
'stone axe':{
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_STONE,5,),),
    'sound'     : 60,
    'construct' : 9600,
    'components': (
        [ ('piece of stone', 1,), ],
        [ ('stick of plastic', 1,), ('stick of wood', 1,), ],
        [ ('cordage', 2,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 3,), ],
        [ (cmp.Tool_Chisel, 3,), ],
        [ (cmp.Tool_Sharpener, 1,), ],
        ),
    'byproducts': ( ('parcel of stone', 2), ('gravel', 1), ),
    },
'bone axe':{
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_BONE,5,),),
    'sound'     : 60,
    'construct' : 7200,
    'components': (
        [ ('piece of bone', 2,), ],
        [ ('stick of plastic', 1,), ('stick of wood', 1,), ],
        [ ('cordage', 3,), ('glue', 2,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 2,), ],
        [ (cmp.Tool_Chisel, 2,), (cmp.Tool_Chop, 2,), (cmp.Tool_Saw, 3,),
          (cmp.Tool_Cut, 6,), ],
        [ (cmp.Tool_Sharpener, 1,), ],
        ),
    'byproducts': ( ('parcel of bone', 1), ('scrap bone', 1), ),
    },
'metal axe':{
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_METAL,5,),),
    'sound'     : 120,
    'construct' : 12000,
    'components': (
        [ ('piece of metal', 2,), ],
        [ ('stick of wood', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 3,), ],
        [ (cmp.Tool_Sharpener, 3,), ],
        [ (cmp.Tool_Anvil, 2,), ],
        [ (cmp.Tool_Chisel, 2,), (cmp.Tool_Chop, 2,), (cmp.Tool_Saw, 3,),
          (cmp.Tool_Cut, 6,), ],
        [ (cmp.Tool_Furnace, 2,), ],
        [ (cmp.Tool_Tongs, 2,), ],
        ),
    'byproducts': ( ('parcel of wood', 2), ),
    },

    # chisels
'plastic chisel':{ # chisel level 1
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_PLASTIC,2,),),
    'sound'     : 60,
    'construct' : 600,
    'components': (
        [ ('parcel of plastic', 1,), ('shard of plastic', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 1,), ],
        [ (cmp.Tool_Chisel, 1,), (cmp.Tool_Anvil, 1,), ],
        [ (cmp.Tool_Sharpener, 1,), (cmp.Tool_File, 1,), ],
        ),
    'byproducts': (),
    },
'wooden chisel':{ # chisel level 2
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_WOOD,2,),),
    'sound'     : 60,
    'construct' : 1000,
    'components': (
        [ ('parcel of wood', 1,), ('shard of wood', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 2,), ],
        [ (cmp.Tool_Chisel, 2,), (cmp.Tool_Anvil, 1,), ],
        [ (cmp.Tool_Sharpener, 1,), (cmp.Tool_File, 1,), ],
        ),
    'byproducts': ( ('scrap wood', 1), ),
    },
'stone chisel':{ # chisel level 3
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_STONE,5,),),
    'sound'     : 60,
    'construct' : 1800,
    'components': (
        [ ('parcel of stone', 1,), ('shard of stone', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 3,), ],
        [ (cmp.Tool_Chisel, 3,), (cmp.Tool_Anvil, 2,), ],
        [ (cmp.Tool_Sharpener, 2,), (cmp.Tool_File, 2,), ],
        ),
    'byproducts': ( ('gravel', 1), ),
    },
'bone chisel':{ # chisel level 2
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_BONE,5,),),
    'sound'     : 60,
    'construct' : 1200,
    'components': (
        [ ('parcel of bone', 1,), ('shard of bone', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 2,), ],
        [ (cmp.Tool_Chisel, 2,), (cmp.Tool_Anvil, 2,), ],
        [ (cmp.Tool_Sharpener, 1,), (cmp.Tool_File, 1,), ],
        ),
    'byproducts': ( ('scrap bone', 1), ),
    },
'metal chisel':{ # chisel level 4
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_METAL,4,),),
    'sound'     : 120,
    'construct' : 2400,
    'components': (
        [ ('parcel of metal', 1,), ('shard of metal', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 3,), ],
        [ (cmp.Tool_Sharpener, 3,), ],
        [ (cmp.Tool_Furnace, 2,), (cmp.Tool_Torch, 3,), ],
        [ (cmp.Tool_Anvil, 3,), ],
        [ (cmp.Tool_Tongs, 1,), ],
        ),
    'byproducts': ( ('scrap metal', 1), ),
    },

    # cutting implements
'scissors':{ # cut level 7
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_METAL,10,),),
    'sound'     : 120,
    'construct' : 9600,
    'components': (
        [ ('shard of metal', 2,), ],
        [ ('nail', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 4,), ],
        [ (cmp.Tool_Sharpener, 3,), ],
        [ (cmp.Tool_Furnace, 2,), (cmp.Tool_Torch, 3,), ],
        [ (cmp.Tool_Anvil, 3,), ],
        [ (cmp.Tool_Tongs, 1,), ],
        ),
    'byproducts': (),
    },
'wire cutters':{ # cut level 8
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_METAL,30,),),
    'sound'     : 120,
    'construct' : 12000,
    'components': (
        [ ('shard of metal', 2,), ],
        [ ('parcel of metal', 2,), ],
        [ ('nail', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 5,), ],
        [ (cmp.Tool_Sharpener, 3,), ],
        [ (cmp.Tool_Furnace, 2,), (cmp.Tool_Torch, 3,), ],
        [ (cmp.Tool_Anvil, 3,), ],
        [ (cmp.Tool_Tongs, 1,), ],
        ),
    'byproducts': (),
    },
'hedge trimmers':{ # cut level 9
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_METAL,40,),),
    'sound'     : 120,
    'construct' : 9600,
    'components': (
        [ ('stick of metal', 2,), ],
        [ ('nail', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 5,), ],
        [ (cmp.Tool_Sharpener, 3,), ],
        [ (cmp.Tool_Anvil, 3,), ],
        [ (cmp.Tool_Furnace, 2,), ],
        [ (cmp.Tool_Tongs, 2,), ],
        ),
    'byproducts': (),
    },

    # drilling implements
'hole puncher':{ # drill level 1
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_METAL,10,),),
    'sound'     : 120,
    'construct' : 9600,
    'components': (
        [ ('parcel of metal', 2,), ],
        [ ('spring', 1,), ],
        [ ('nail', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 5,), ],
        [ (cmp.Tool_Furnace, 2,), (cmp.Tool_Torch, 3,), ],
        [ (cmp.Tool_Anvil, 3,), ],
        [ (cmp.Tool_Tongs, 1,), ],
        ),
    'byproducts': (),
    },
##'hand drill':{ # drill level 2
##    'quantity'  : 1,
##    'table'     : CRT_TOOLS,
##    'category'  : CRC_METAL,
##    'sound'     : 120,
##    'construct' : 14400,
##    'components': (
##        [ ('parcel of metal', 5,), ('piece of metal', 1,), ],
##        [ ('parcel of wood', 1,), ('parcel of bone', 1,),
##          ('parcel of stone', 1,), ('parcel of metal', 1,), ],
##        ),
##    'tools'     : (
##        [ (cmp.Tool_Anvil, 2,), ],
##        [ (cmp.Tool_Chisel, 2,), ],
##        [ (cmp.Tool_Furnace, 2,), ],
##        [ (cmp.Tool_Hammer, 2,), ],
##        [ (cmp.Tool_Pliers, 2,), ],
##        ),
##    'byproducts': (),
##    },
'electric drill':{ # drill level 2?
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_ASSEMBLY,15,),),
    'sound'     : 120,
    'construct' : 2400,
    'components': (
        [ ('metal can', 1,), ],
        [ ('parcel of wood', 1,), ('parcel of bone', 1,),
          ('parcel of stone', 1,), ('parcel of metal', 1,), ],
        [ ('motor', 1,), ],
        [ ('battery', 1,), ],
        [ ('metal wire', 2,), ('insulated wire', 2,), ],
        [ ('screw', 1,), ],
        [ ('glue', 3,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Cut, 7,), ],
        [ (cmp.Tool_Hammer, 5,), ],
        [ (cmp.Tool_Pliers, 2,), ],
        [ (cmp.Tool_Weld, 1,), (cmp.Tool_Torch, 3,), ],
        ),
    'byproducts': (),
    },

    # hammers
'plastic hammer':{ # hammer level 3
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_PLASTIC,5,),),
    'sound'     : 60,
    'construct' : 1200,
    'components': (
        [ ('piece of plastic', 1,), ],
        [ ('stick of plastic', 1,), ('stick of wood', 1,), ],
        [ ('cordage', 2,), ('glue', 2,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 1,), ],
        [ (cmp.Tool_Chisel, 1,), ],
        ),
    'byproducts': ( ('scrap plastic', 1), ),
    },
'wooden hammer':{ # hammer level 3
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_WOOD,5,),),
    'sound'     : 60,
    'construct' : 1800,
    'components': (
        [ ('piece of wood', 1,), ],
        [ ('stick of plastic', 1,), ('stick of wood', 1,), ],
        [ ('cordage', 2,), ('glue', 2,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Chop, 1,), ],
        [ (cmp.Tool_Hammer, 1,), ],
        [ (cmp.Tool_Chisel, 1,), (cmp.Tool_Anvil, 1,), ],
        ),
    'byproducts': ( ('parcel of wood', 1,), ('scrap wood', 1,), ),
    },
'stone hammer':{ # hammer level 3
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_STONE,5,),),
    'sound'     : 60,
    'construct' : 2400,
    'components': (
        [ ('piece of stone', 1,), ],
        [ ('stick of plastic', 1,), ('stick of wood', 1,), ],
        [ ('cordage', 2,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 2,), ],
        [ (cmp.Tool_Chisel, 2,), ],
        ),
    'byproducts': ( ('parcel of stone', 1,), ('gravel', 1,), ),
    },
'bone hammer':{ # hammer level 3
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_BONE,5,),),
    'sound'     : 60,
    'construct' : 4000,
    'components': (
        [ ('piece of bone', 2,), ],
        [ ('stick of plastic', 1,), ('stick of wood', 1,), ],
        [ ('cordage', 3,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 1,), ],
        [ (cmp.Tool_Chisel, 2,), ],
        ),
    'byproducts': ( ('parcel of bone', 1,), ('scrap bone', 1,), ),
    },
'metal hammer':{ # hammer level 4
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_METAL,10,),),
    'sound'     : 120,
    'construct' : 7200,
    'components': (
        [ ('piece of metal', 2,), ],
        [ ('stick of wood', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 3,), ],
        [ (cmp.Tool_Furnace, 2,), ],
        [ (cmp.Tool_Anvil, 2,), ],
        [ (cmp.Tool_Tongs, 2,), ],
        ),
    'byproducts': ( ('scrap wood', 1,), ),
    },
'fine hammer':{ # hammer level 5
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_METAL,35,),),
    'sound'     : 120,
    'construct' : 14400,
    'components': (
        [ ('piece of metal', 3,), ],
        [ ('stick of wood', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 4,), ],
        [ (cmp.Tool_Anvil, 3,), ],
        [ (cmp.Tool_Furnace, 2,), ],
        [ (cmp.Tool_Tongs, 2,), ],
        ),
    'byproducts': ( ('parcel of wood', 1,), ('scrap wood', 1,), ),
    },

    # machetes

'plastic machete':{
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_PLASTIC,10,),),
    'sound'     : 60,
    'construct' : 2000,
    'components': ( [ ('parcel of plastic', 10,), ], ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 1,), ],
        [ (cmp.Tool_Furnace, 1,), ],
        [ (cmp.Tool_Chisel, 1,), ],
        [ (cmp.Tool_Crucible, 1,), ],
        [ (cmp.Tool_Sharpener, 1,), ],
        [ (cmp.Tool_Anvil, 1,), ],
        [ (cmp.Tool_Tongs, 1,), ],
        [ (cmp.Mold_MachetePlastic, 1,), ],
        ),
    'byproducts': ( ('scrap plastic', 1,), ),
    },
##'stone machete':{
##    'quantity'  : 1,
##    'table'     : CRT_TOOLS,
##    'category'  : CRC_STONE,
##    'sound'     : 60,
##    'construct' : 14400,
##    'components': (
##        [ ('shard of stone', 5,), ],
##        [ ('stick of wood', 1,), ],
##        [ ('parcel of wood', 1,), ('bone', 1,), ('piece of bone', 1,), ],
##        ),
##    'tools'     : (
##        [ (cmp.Tool_Hammer, 4,), ],
##        [ (cmp.Tool_Chisel, 3,), ],
##        [ (cmp.Tool_Sharpener, 2,), ],
##        ),
##    'byproducts': (),
##    },
'wooden machete':{
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_WOOD,10,),),
    'sound'     : 60,
    'construct' : 3200,
    'components': (
        [ ('wooden plank', 2,), ],
        [ ('parcel of wood', 2,), ],
        [ ('glue', 2,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 2,), ],
        [ (cmp.Tool_Saw, 2,), ],
        [ (cmp.Tool_Sharpener, 1,), ],
        [ (cmp.Tool_Chisel, 1,), ],
        ),
    'byproducts': ( ('parcel of wood', 2,), ('scrap wood', 3,), ),
    },
'bone machete':{
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_BONE,20,),),
    'sound'     : 60,
    'construct' : 9600,
    'components': (
        [ ('bone, large', 1,), ],
        [ ('parcel of wood', 1,), ('bone', 1,), ('piece of bone', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 3,), ],
        [ (cmp.Tool_Chisel, 2,), ],
        [ (cmp.Tool_Sharpener, 1,), ],
        ),
    'byproducts': ( ('parcel of bone', 1,), ('scrap bone', 4,), ),
    },
'metal machete':{
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_METAL,10,),),
    'sound'     : 120,
    'construct' : 7200,
    'components': (
        [ ('parcel of metal', 15,), ('piece of metal', 3,), ],
        [ ('parcel of wood', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 2,), ],
        [ (cmp.Tool_Furnace, 2,), ],
        [ (cmp.Tool_Chisel, 2,), ],
        [ (cmp.Tool_Crucible, 2,), ],
        [ (cmp.Tool_Tongs, 2,), ],
        [ (cmp.Tool_Anvil, 2,), ],
        [ (cmp.Tool_Sharpener, 1,), ],
        [ (cmp.Mold_MacheteMetal, 1,), ],
        ),
    'byproducts': (),
    },

    # mandrils
'metal mandril':{
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_METAL,30,),),
    'construct' : 4000,
    'components': (
        [ ('stick of metal', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 4,), ],
        [ (cmp.Tool_Furnace, 2,), cmp.Tool_Torch, 3,), ],
        [ (cmp.Tool_Anvil, 3,), ],
        [ (cmp.Tool_Swage, 2,), ],
        [ (cmp.Tool_Tongs, 1,), ],
        ),
    'byproducts': (),
    },

    # molds
# staff molds
'earthenware mold, metal staff':{
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_ASSEMBLY,20,),),
    'construct' : 2400,
    'components': (
        [ ('chunk of clay', 2,), ],
        ),
    'tools'     : ( [ (cmp.Tool_Furnace, 1,), ], ),
    'byproducts': (),
    },
# sword molds
'earthenware mold, plastic sword':{
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_ASSEMBLY,15,), (SKL_BLADESMITH,3,),),
    'construct' : 3200,
    'components': (
        [ ('chunk of clay', 3,), ],
        ),
    'tools'     : ( [ (cmp.Tool_Furnace, 1,), ], ),
    'byproducts': (),
    },
'earthenware mold, metal sword':{
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_ASSEMBLY,25,), (SKL_BLADESMITH,10,),),
    'construct' : 4800,
    'components': (
        [ ('chunk of clay', 3,), ],
        ),
    'tools'     : ( [ (cmp.Tool_Furnace, 1,), ], ),
    'byproducts': (),
    },
# dagger molds
'earthenware mold, metal dagger':{
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_ASSEMBLY,30,), (SKL_BLADESMITH,20,),),
    'construct' : 2400,
    'components': (
        [ ('chunk of clay', 1,), ],
        ),
    'tools'     : ( [ (cmp.Tool_Furnace, 1,), ], ),
    'byproducts': (),
    },
# ammunition molds
'earthenware mold, bullet, small':{
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_ASSEMBLY,6,),),
    'construct' : 800,
    'components': (
        [ ('piece of clay', 1,), ],
        ),
    'tools'     : ( [ (cmp.Tool_Furnace, 1,), ], ),
    'byproducts': (),
    },
'earthenware mold, bullet':{
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_ASSEMBLY,5,),),
    'construct' : 900,
    'components': (
        [ ('piece of clay', 1,), ],
        ),
    'tools'     : ( [ (cmp.Tool_Furnace, 1,), ], ),
    'byproducts': (),
    },
'earthenware mold, bullet, large':{
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_ASSEMBLY,4,),),
    'construct' : 1000,
    'components': (
        [ ('piece of clay', 1,), ],
        ),
    'tools'     : ( [ (cmp.Tool_Furnace, 1,), ], ),
    'byproducts': (),
    },
'earthenware mold, Minni ball':{
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_ASSEMBLY,15,),),
    'construct' : 1800,
    'components': (
        [ ('piece of clay', 1,), ],
        ),
    'tools'     : ( [ (cmp.Tool_Furnace, 1,), ], ),
    'byproducts': (),
    },

    # pliers
'pliers':{ # pliers level 2
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_METAL,8,),),
    'sound'     : 120,
    'construct' : 4800,
    'components': (
        [ ('parcel of metal', 3,), ],
        [ ('nail', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 3,), ],
        [ (cmp.Tool_Furnace, 2,), (cmp.Tool_Torch, 3,), ],
        [ (cmp.Tool_Anvil, 2,), ],
        [ (cmp.Tool_Tongs, 1,), ],
        ),
    'byproducts': ( ('scrap metal', 2,), ),
    },
'needle-nose pliers':{ # pliers level 3, also can cut as well as wire cutters
    # should the needle-nose property be an additional Tool component? Only if it's a unique property not fulfilled by any other tool...
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_METAL,25,),),
    'sound'     : 120,
    'construct' : 9600,
    'components': (
        [ ('shard of metal', 2,), ],
        [ ('parcel of metal', 1,), ],
        [ ('nail', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 5,), ],
        [ (cmp.Tool_Sharpener, 3,), ],
        [ (cmp.Tool_Anvil, 3,), ],
        [ (cmp.Tool_Furnace, 2,), (cmp.Tool_Torch, 3,), ],
        [ (cmp.Tool_Tongs, 1,), ],
        ),
    'byproducts': (),
    },

    # ramrods
'metal ramrod, long':{
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_METAL,20,),),
    'construct' : 7200,
    'components': (
        [ ('stick of metal', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 3,), ],
        [ (cmp.Tool_Anvil, 3,), ],
        [ (cmp.Tool_Furnace, 2,), cmp.Tool_Torch, 3,), ],
        [ (cmp.Tool_Swage, 2,), ],
        [ (cmp.Tool_Tongs, 1,), ],
        ),
    'byproducts': (),
    },

    # saws
'plastic saw':{ # saw level 1
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_PLASTIC,15,),),
    'construct' : 2000,
    'components': (
        [ ('piece of plastic', 1,), ],
        [ ('parcel of plastic', 1,), ('parcel of wood', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_File, 1,), (cmp.Tool_Saw, 1,), (cmp.Tool_Cut, 5,), ],
        [ (cmp.Tool_Hammer, 1,), ],
        [ (cmp.Tool_Chisel, 1,), ],
        ),
    'byproducts': ( ('scrap plastic', 1), ),
    },
'plastic saw, large':{ # saw level 2
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_PLASTIC,15,),),
    'sound'     : 60,
    'construct' : 3600,
    'components': (
        [ ('chunk of plastic', 1,), ],
        [ ('parcel of plastic', 2,), ('parcel of wood', 2,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 2,), ],
        [ (cmp.Tool_File, 1,), (cmp.Tool_Saw, 1,), (cmp.Tool_Cut, 5,), ],
        [ (cmp.Tool_Chisel, 1,), ],
        ),
    'byproducts': ( ('shard of plastic', 2), ('scrap plastic', 1), ),
    },
'bone saw':{ # saw level 2
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_BONE,35,),),
    'sound'     : 60,
    'construct' : 3200,
    'components': (
        [ ('bone', 1,), ],
        [ ('parcel of plastic', 2,), ('parcel of wood', 2,),
          ('piece of bone', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Saw, 3,), ],
        [ (cmp.Tool_Hammer, 2,), ],
        [ (cmp.Tool_File, 1,), (cmp.Tool_Saw, 4,), (cmp.Tool_Cut, 5,), ],
        [ (cmp.Tool_Chisel, 1,), ],
        ),
    'byproducts': ( ('shard of bone', 1), ),
    },
'bone saw, large':{ # saw level 3
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_BONE,35,),),
    'sound'     : 60,
    'construct' : 4800,
    'components': (
        [ ('bone, large', 1,), ],
        [ ('parcel of plastic', 2,), ('parcel of wood', 2,),
          ('piece of bone', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Saw, 3,), ],
        [ (cmp.Tool_Hammer, 2,), ],
        [ (cmp.Tool_File, 1,), (cmp.Tool_Saw, 4,),  (cmp.Tool_Cut, 5,),],
        [ (cmp.Tool_Chisel, 1,), ],
        ),
    'byproducts': ( ('shard of bone', 1), ('scrap bone', 1), ),
    },
'metal saw':{ # saw level 3
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_METAL,20,),),
    'sound'     : 120,
    'construct' : 6400,
    'components': (
        [ ('piece of metal', 1,), ],
        [ ('parcel of plastic', 1,), ('parcel of wood', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 4,), ],
        [ (cmp.Tool_File, 3,), (cmp.Tool_Saw, 5,),  (cmp.Tool_Cut, 9,),],
        [ (cmp.Tool_Anvil, 3,), ],
        [ (cmp.Tool_Furnace, 2,), ],
        [ (cmp.Tool_Chisel, 1,), ],
        [ (cmp.Tool_Tongs, 1,), ],
        ),
    'byproducts': (),
    },
'metal saw, large':{ # saw level 4
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_METAL,20,),),
    'sound'     : 120,
    'construct' : 7200,
    'components': (
        [ ('metal sheet', 1,), ],
        [ ('parcel of plastic', 2,), ('parcel of wood', 2,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Anvil, 5,), ],
        [ (cmp.Tool_Hammer, 4,), ],
        [ (cmp.Tool_File, 3,), (cmp.Tool_Saw, 5,),  (cmp.Tool_Cut, 9,),],
        [ (cmp.Tool_Chisel, 1,), ],
        ),
    'byproducts': ( ('parcel of metal', 1), ('shard of metal', 1), ('scrap metal', 1), ),
    },

    # sewing needles
'plastic sewing needle':{ # sewing level 1
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_PLASTIC,10,),),
    'sound'     : 60,
    'construct' : 1000,
    'components': (
        [ ('scrap plastic', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Torch, 1,), (cmp.Tool_Furnace, 1,), ],
        [ (cmp.Tool_Hammer, 1,), ],
        [ (cmp.Tool_Anvil, 1,), ],
        ),
    'byproducts': (),
    },
'bone sewing needle':{ # sewing level 2
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_BONE,20,),),
    'sound'     : 60,
    'construct' : 2400,
    'components': (
        [ ('scrap bone', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Chisel, 3,), ],
        [ (cmp.Tool_Hammer, 2,), ],
        [ (cmp.Tool_Anvil, 2,), ],
        [ (cmp.Tool_Sharpener, 1,), (cmp.Tool_File, 1,), ],
        ),
    'byproducts': (),
    },
'metal sewing needle':{ # sewing level 3
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_METAL,15,),),
    'sound'     : 120,
    'construct' : 2000,
    'components': (
        [ ('metal needle', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 5,), ],
        [ (cmp.Tool_Sharpener, 3,), (cmp.Tool_File, 3,), ],
        [ (cmp.Tool_Anvil, 3,), ],
        [ (cmp.Tool_Pliers, 2,), ],
        [ (cmp.Tool_Furnace, 1,), (cmp.Tool_Torch, 3,), ],
        [ (cmp.Tool_Tongs, 1,), ],
        ),
    'byproducts': (),
    },

    # swage blocks
'wooden swage block':{ # swage level 1
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_WOOD,40,),),
    'sound'     : 120,
    'construct' : 7200,
    'components': (
        [ ('chunk of wood', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Chisel, 4,), ],
        [ (cmp.Tool_Hammer, 3,), ],
        [ (cmp.Tool_Saw, 3,), ],
        ),
    'byproducts': ( ('scrap wood', 2,), ),
    },
'metal swage block':{ # swage level 2 (level 3 is difficult to fabricate.)
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_METAL,50,),),
    'sound'     : 120,
    'construct' : 57600,
    'components': (
        [ ('chunk of metal', 1,), ],
        [ ('metal pipe', 1,), ],
        [ ('stick of metal', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 4,), ],
        [ (cmp.Tool_Anvil, 4,), ],
        [ (cmp.Tool_Hammer, 3,), ],
        [ (cmp.Tool_Tongs, 3,), ],
        [ (cmp.Tool_Tongs, 3,), ],
        [ (cmp.Tool_Furnace, 2,), ],
        ),
    'byproducts': (
        ('metal pipe', 1,), ('stick of metal', 1,),
        ),
    },

    # tongs
'tongs':{ # tongs level 2
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_METAL,8,),),
    'sound'     : 120,
    'construct' : 7200,
    'components': (
        [ ('stick of metal', 2,), ],
        [ ('nail', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 3,), ],
        [ (cmp.Tool_Furnace, 2,), (cmp.Tool_Torch, 3,), ],
        [ (cmp.Tool_Anvil, 2,), ],
        ),
    'byproducts': (),
    },
'tongs, large':{ # tongs level 3
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_METAL,15,),),
    'sound'     : 120,
    'construct' : 9600,
    'components': (
        [ ('pole of metal', 2,), ],
        [ ('nail', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 3,), ],
        [ (cmp.Tool_Anvil, 3,), ],
        [ (cmp.Tool_Furnace, 2,), ],
        ),
    'byproducts': (),
    },
'fine tongs':{ # tongs level 4
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_METAL,20,),),
    'sound'     : 120,
    'construct' : 14400,
    'components': (
        [ ('stick of metal', 1,), ],
        [ ('nail', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Saw, 5,), (cmp.Tool_Pliers, 2,), ],
        [ (cmp.Tool_Hammer, 4,), ],
        [ (cmp.Tool_Anvil, 4,), ],
        [ (cmp.Tool_Furnace, 2,), (cmp.Tool_Torch, 3,), ],
        [ (cmp.Tool_Tongs, 1,), ],
        ),
    'byproducts': (),
    },





    #--------------------------#
    #         Weapons          #
    #--------------------------#



    # misc
'flamethrower':{
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_ASSEMBLY,35,),),
    'construct' : 4000,
    'components': (
        [ ('plastic bottle', 1,), ('glass bottle', 1,), ],
        [ ('plastic tube', 1,), ],
        [ ('rubber hose', 1,), ],
        [ ('plastic nozzle', 1,), ('syringe', 1,), ], # turkey baster? Plastic nozzle comes from a spray bottle.
        [ ('lighter', 1,), ],
        [ ('metal wire', 1,), ],
        [ ('glue', 1,), ],
        ),
    'tools'     : ( [ (cmp.Tool_Cut, 5,), ], ),
    'byproducts': ( ('scrap plastic', 1, ), ),
    },
'sling':{
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_ASSEMBLY,8,),),
    'construct' : 800,
    'components': (
        [ ('cordage', 3,), ],
        ),
    'tools'     : (),
    'byproducts': (),
    },
'slingshot':{
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_WOOD,5,),),
    'construct' : 1600,
    'components': (
        [ ('parcel of wood', 1,), ],
        [ ('rubber band', 3,), ],
        ),
    'tools'     : ( [ (cmp.Tool_Cut, 4,), ], ),
    'byproducts': ( ('scrap wood', 1,), ),
    },

    # shivs
'ceramic shiv':{
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_ASSEMBLY,5,),),
    'construct' : 800,
    'components': (
        [ ('shard of ceramic', 1,), ],
        [ ('parcel of plastic', 1,), ('parcel of wood', 1,),
          ('parcel of bone', 1,), ('parcel of stone', 1,),
          ('parcel of metal', 1,), ],
        [ ('duct tape', 2,), ('sinew', 1,), ],
        ),
    'tools'     : (),
    'byproducts': ( ('scrap plastic', 1,), ),
    },
'plastic shiv':{
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_ASSEMBLY,5,),),
    'construct' : 500,
    'components': (
        [ ('shard of plastic', 1,), ],
        [ ('parcel of plastic', 1,), ('parcel of wood', 1,),
          ('parcel of bone', 1,), ('parcel of stone', 1,),
          ('parcel of metal', 1,), ],
        [ ('duct tape', 2,), ('sinew', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Sharpener, 1,), (cmp.Tool_File, 1,), (cmp.Tool_Cut, 5,), ],
        ),
    'byproducts': ( ('scrap plastic', 1,), ),
    },
'wooden shiv':{
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_ASSEMBLY,5,),),
    'construct' : 600,
    'components': (
        [ ('shard of wood', 1,), ],
        [ ('parcel of plastic', 1,), ('parcel of wood', 1,),
          ('parcel of bone', 1,), ('parcel of stone', 1,),
          ('parcel of metal', 1,), ],
        [ ('duct tape', 2,), ('sinew', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Sharpener, 1,), (cmp.Tool_File, 1,), (cmp.Tool_Cut, 6,), ],
        ),
    'byproducts': ( ('scrap wood', 1,), ),
    },
'stone shiv':{
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_ASSEMBLY,5,),),
    'construct' : 800,
    'components': (
        [ ('shard of stone', 1,), ],
        [ ('parcel of plastic', 1,), ('parcel of wood', 1,),
          ('parcel of bone', 1,), ('parcel of stone', 1,),
          ('parcel of metal', 1,), ],
        [ ('duct tape', 2,), ('sinew', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Sharpener, 2,), (cmp.Tool_File, 2,), ],
        ),
    'byproducts': ( ('gravel', 1,), ),
    },
'bone shiv':{
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_ASSEMBLY,5,),),
    'construct' : 600,
    'components': (
        [ ('shard of bone', 1,), ],
        [ ('parcel of plastic', 1,), ('parcel of wood', 1,),
          ('parcel of bone', 1,), ('parcel of stone', 1,),
          ('parcel of metal', 1,), ],
        [ ('duct tape', 2,), ('sinew', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Sharpener, 1,), (cmp.Tool_File, 1,), ],
        ),
    'byproducts': ( ('scrap bone', 1,), ),
    },
'glass shiv':{
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_ASSEMBLY,5,),),
    'construct' : 800,
    'components': (
        [ ('shard of glass', 1,), ],
        [ ('parcel of plastic', 1,), ('parcel of wood', 1,),
          ('parcel of bone', 1,), ('parcel of stone', 1,),
          ('parcel of metal', 1,), ],
        [ ('duct tape', 2,), ('sinew', 1,), ],
        ),
    'tools'     : (),
    'byproducts': (),
    },
'metal shiv':{
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_ASSEMBLY,5,),),
    'construct' : 1000,
    'components': (
        [ ('shard of metal', 1,), ],
        [ ('parcel of plastic', 1,), ('parcel of wood', 1,),
          ('parcel of bone', 1,), ('parcel of stone', 1,),
          ('parcel of metal', 1,), ],
        [ ('duct tape', 2,), ('sinew', 1,), ],
        ),
    'tools'     : ( [ (cmp.Tool_Sharpener, 3,), (cmp.Tool_File, 3,), ], ),
    'byproducts': (),
    },

    # knives
'plastic knife':{
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_PLASTIC,5,),),
    'construct' : 2000,
    'components': (
        [ ('shard of plastic', 1,), ],
        [ ('parcel of plastic', 1,), ('parcel of wood', 1,),
          ('parcel of bone', 1,), ],
        [ ('cordage', 1,), ('glue', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Cut, 5,), ],
        [ (cmp.Tool_Furnace, 1,), (cmp.Tool_Torch, 1,), ],
        [ (cmp.Tool_Sharpener, 1,), (cmp.Tool_File, 1,), ],
        ),
    'byproducts': ( ('scrap plastic', 1,), ),
    },
'wooden knife':{
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_WOOD,5,),),
    'construct' : 3200,
    'components': (
        [ ('shard of wood', 1,), ],
        [ ('parcel of plastic', 1,), ('parcel of wood', 1,),
          ('parcel of bone', 1,), ],
        [ ('cordage', 1,), ('glue', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Cut, 6,), ],
        [ (cmp.Tool_Sharpener, 1,), (cmp.Tool_File, 1,), ],
        ),
    'byproducts': ( ('scrap wood', 1,), ),
    },
'stone knife':{
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_STONE,15,),),
    'sound'     : 60,
    'construct' : 4000,
    'components': (
        [ ('shard of stone', 1,), ],
        [ ('parcel of plastic', 1,), ('parcel of wood', 1,),
          ('parcel of bone', 1,), ('parcel of stone', 1,), ],
        [ ('cordage', 1,), ('glue', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Chisel, 3,), ],
        [ (cmp.Tool_Hammer, 3,), ],
        [ (cmp.Tool_Sharpener, 2,), (cmp.Tool_File, 2,), ],
        ),
    'byproducts': ( ('gravel', 1,), ),
    },
'bone knife':{
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_BONE,10,),),
    'sound'     : 60,
    'construct' : 4800,
    'components': (
        [ ('shard of bone', 1,), ],
        [ ('parcel of plastic', 1,), ('parcel of wood', 1,),
          ('parcel of bone', 1,), ('parcel of stone', 1,), ],
        [ ('cordage', 1,), ('glue', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 2,), ],
        [ (cmp.Tool_Chisel, 2,), ],
        [ (cmp.Tool_Sharpener, 1,), (cmp.Tool_File, 1,), ],
        ),
    'byproducts': ( ('scrap bone', 1,), ),
    },
'glass knife':{
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_GLASS,25,),),
    'sound'     : 60,
    'construct' : 14400,
    'components': (
        [ ('shard of glass', 1,), ],
        [ ('parcel of plastic', 1,), ('parcel of wood', 1,),
          ('parcel of bone', 1,), ('parcel of stone', 1,), ],
        [ ('cordage', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Chisel, 4,), ],
        [ (cmp.Tool_Hammer, 4,), ],
        ),
    'byproducts': (),
    },
'metal knife':{
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_METAL,10,),),
    'sound'     : 120,
    'construct' : 7200,
    'components': (
        [ ('shard of metal', 1,), ],
        [ ('parcel of plastic', 1,), ('parcel of wood', 1,),
          ('parcel of bone', 1,), ('parcel of stone', 1,),
          ('parcel of metal', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 5,), ],
        [ (cmp.Tool_Sharpener, 3,), ],
        [ (cmp.Tool_Anvil, 3,), ],
        [ (cmp.Tool_Chisel, 2,), ],
        [ (cmp.Tool_Furnace, 2,), (cmp.Tool_Torch, 3,), ],
        [ (cmp.Tool_Tongs, 1,), ],
        ),
    'byproducts': (),
    },

    # serrated knives
'plastic serrated knife':{
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_PLASTIC,10,),),
    'construct' : 1800,
    'components': ( [ ('plastic knife', 1,), ], ),
    'tools'     : ( [ (cmp.Tool_File, 1,), ], ),
    'byproducts': (),
    },
'wooden serrated knife':{ # serrated knives: Dmg +2, Pen -2, Asp -15, Cut -1, Saw +1, Chisel -1
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_WOOD,15,),),
    'construct' : 3200,
    'components': ( [ ('wooden knife', 1,), ], ),
    'tools'     : ( [ (cmp.Tool_File, 1,), (cmp.Tool_Saw, 5,), ], ),
    'byproducts': (),
    },
'stone serrated knife':{
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_STONE,40,),),
    'construct' : 7200,
    'components': ( [ ('stone knife', 1,), ], ),
    'tools'     : ( [ (cmp.Tool_File, 2,), (cmp.Tool_Saw, 5,), ], ),
    'byproducts': (),
    },
'bone serrated knife':{
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_BONE,25,),),
    'construct' : 4800,
    'components': ( [ ('bone knife', 1,), ], ),
    'tools'     : ( [ (cmp.Tool_File, 1,), (cmp.Tool_Saw, 5,), ], ),
    'byproducts': (),
    },
'metal serrated knife':{
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_METAL,30,),),
    'construct' : 9600,
    'components': ( [ ('metal knife', 1,), ], ),
    'tools'     : ( [ (cmp.Tool_File, 3,), (cmp.Tool_Saw, 5,), ], ),
    'byproducts': (),
    },

    # daggers
'bone dagger':{
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_BONE,30,),),
    'sound'     : 60,
    'construct' : 9600,
    'components': (
        [ ('bone', 1,), ],
        [ ('parcel of wood', 1,), ('parcel of bone', 1,),
          ('parcel of stone', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 3,), ],
        [ (cmp.Tool_Chisel, 2,), ],
        [ (cmp.Tool_Sharpener, 1,), ],
        ),
    'byproducts': (),
    },
'glass dagger':{
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_GLASS,50,),),
    'sound'     : 60,
    'construct' : 28800,
    'components': (
        [ ('parcel of glass', 3,), ('sand', 3,), ('quartz', 3,), ],
        [ ('parcel of wood', 1,), ('parcel of bone', 1,),
          ('parcel of stone', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 5,), ],
        [ (cmp.Tool_Chisel, 5,), ],
        [ (cmp.Tool_Crucible, 2,), ],
        [ (cmp.Tool_Furnace, 2,), ],
        [ (cmp.Tool_Tongs, 1,), ],
        [ (cmp.Mold_GlassDagger, 1,), ],
        ),
    'byproducts': (),
    },
'metal dagger':{
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_METAL,20,),),
    'sound'     : 120,
    'construct' : 14400,
    'components': (
        [ ('parcel of metal', 2,), ('shard of metal', 2,), ],
        [ ('parcel of wood', 1,), ('parcel of bone', 1,),
          ('parcel of stone', 1,), ('parcel of metal', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 5,), ],
        [ (cmp.Tool_Chisel, 3,), ],
        [ (cmp.Tool_Furnace, 3,), ],
        [ (cmp.Tool_Sharpener, 3,), ],
        [ (cmp.Tool_Anvil, 3,), ],
        [ (cmp.Tool_Crucible, 2,), ],
        [ (cmp.Tool_Tongs, 1,), ],
        [ (cmp.Mold_MetalDagger, 1,), ],
        ),
    'byproducts': (),
    },

    # staves / staffs
'plastic staff':{
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_PLASTIC,5,),),
    'sound'     : 60,
    'construct' : 2400,
    'components': (
        [ ('parcel of plastic', 8,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Tongs, 2,), ],
        [ (cmp.Tool_Hammer, 1,), ],
        [ (cmp.Tool_Chisel, 1,), ],
        [ (cmp.Tool_Furnace, 1,), ],
        [ (cmp.Tool_Crucible, 1,), ],
        [ (cmp.Mold_PlasticStaff, 1,), ],
        ),
    'byproducts': ( ('scrap plastic', 2,), ),
    },
'wooden staff':{
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_WOOD,10,),),
    'sound'     : 60,
    'construct' : 7200,
    'components': (
        [ ('chunk of wood', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Saw, 3,), ],
        [ (cmp.Tool_Hammer, 2,), ],
        [ (cmp.Tool_Chisel, 1,), ],
        ),
    'byproducts': (
        ('piece of wood', 2,),
        ('parcel of wood', 2,),
        ('scrap wood', 2,),
        ),
    },
'metal staff':{
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_METAL,10,),),
    'sound'     : 120,
    'construct' : 12000,
    'components': (
        [ ('parcel of metal', 10,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Furnace, 2,), ],
        [ (cmp.Tool_Hammer, 2,), ],
        [ (cmp.Tool_Crucible, 2,), ],
        [ (cmp.Tool_Anvil, 2,), ],
        [ (cmp.Tool_Swage, 1,), ],
        [ (cmp.Mold_StaffMetal, 1,), ],
        ),
    'byproducts': (),
    },

    # swords
'plastic sword':{
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_PLASTIC,10,), (SKL_BLADESMITH,5,),),
    'sound'     : 60,
    'construct' : 4800,
    'components': (
        [ ('parcel of plastic', 6,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Furnace, 2,), ],
        [ (cmp.Tool_Tongs, 2,), ],
        [ (cmp.Tool_Saw, 1,), (cmp.Tool_Cut, 4,), ],
        [ (cmp.Tool_Crucible, 1,), ],
        [ (cmp.Tool_Sharpener, 1,), ],
        [ (cmp.Mold_SwordPlastic, 1,), ],
        ),
    'byproducts': (),
    },
'wooden sword':{
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_WOOD,10,), (SKL_BLADESMITH,5,),),
    'sound'     : 60,
    'construct' : 12000,
    'components': (
        [ ('chunk of wood', 1,), ],
        [ ('parcel of wood', 1,), ('bone', 1,), ('piece of bone', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Saw, 3,), ],
        [ (cmp.Tool_Hammer, 2,), ],
        [ (cmp.Tool_Chisel, 2,), ],
        [ (cmp.Tool_Sharpener, 1,), ],
        ),
    'byproducts': (
        ('piece of wood', 2,),
        ('parcel of wood', 2,),
        ('scrap wood', 4,),
        ),
    },
'bone sword':{
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_BONE,20,), (SKL_BLADESMITH,10,),),
    'sound'     : 60,
    'construct' : 14400,
    'components': (
        [ ('bone, large', 1,), ],
        [ ('parcel of wood', 1,), ('parcel of bone', 1,), ],
        [ ('parcel of wood', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 3,), ],
        [ (cmp.Tool_Chisel, 2,), ],
        [ (cmp.Tool_Sharpener, 1,), ],
        ),
    'byproducts': (
        ('scrap wood', 1,),
        ('piece of bone', 1,),
        ('parcel of bone', 2,),
        ('scrap bone', 5,),
        ),
    },
'glass sword':{ # glass is the hardest to work with, and making a whole sword out of it is very tough.
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_GLASS,30,), (SKL_BLADESMITH,20,),),
    'sound'     : 60,
    'construct' : 64000,
    'components': (
        [ ('parcel of glass', 25,), ('sand', 25,), ('quartz', 25,), ],
        [ ('parcel of wood', 1,), ('parcel of metal', 1,), ],
        [ ('parcel of wood', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Chisel, 4,), ],
        [ (cmp.Tool_Hammer, 4,), ],
        [ (cmp.Tool_Anvil, 4,), ],
        [ (cmp.Tool_Furnace, 3,), ],
        [ (cmp.Tool_Crucible, 2,), ],
        [ (cmp.Tool_Tongs, 2,), ],
        [ (cmp.Mold_GlassSword, 1,), ],
        ),
    'byproducts': ( ('scrap wood', 1,), ),
    },
'metal sword blade':{
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_METAL,20,), (SKL_BLADESMITH,12,),),
    'sound'     : 120,
    'construct' : 38400,
    'components': (
        [ ('parcel of metal', 11,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 5,), ],
        [ (cmp.Tool_Furnace, 3,), ],
        [ (cmp.Tool_Grinder, 3,), ],
        [ (cmp.Tool_Anvil, 3,), ],
        [ (cmp.Tool_Crucible, 2,), ],
        [ (cmp.Tool_Tongs, 2,), ],
        [ (cmp.Mold_SwordMetal, 1,), ],
        ),
    'byproducts': (),
    },
'wooden sword hilt':{
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_WOOD,10,), (SKL_BLADESMITH,10,),),
    'construct' : 7200,
    'components': (
        [ ('parcel of wood', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 3,), ],
        [ (cmp.Tool_Chisel, 2,), ],
        ),
    'byproducts': ( ('scrap wood', 1,), ),
    },
'unsharpened metal sword':{
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_METAL,5,), (SKL_BLADESMITH,5,),),
    'sound'     : 120,
    'construct' : 9600,
    'components': (
        [ ('metal sword blade', 1,), ],
        [ ('plastic sword hilt', 1,), ('wooden sword hilt', 1,),
          ('bone sword hilt', 1,), ],
        [ ('brass rivet', 2,), ('nail', 2,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 5,), ],
        ),
    'byproducts': (),
    },
'metal sword':{
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_METAL,1,), (SKL_BLADESMITH,3,),),
    'sound'     : 120,
    'construct' : 12800,
    'components': (
        [ ('unsharpened metal sword', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Sharpener, 3,), ],
        ),
    'byproducts': (),
    },

    # boomerangs
'plastic boomerang':{
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_PLASTIC,10,),),
    'sound'     : 60,
    'construct' : 2400,
    'components': (
        [ ('parcel of plastic', 4,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 2,), ],
        [ (cmp.Tool_Tongs, 2,), ],
        [ (cmp.Tool_Chisel, 1,), ],
        [ (cmp.Tool_Furnace, 1,), ],
        [ (cmp.Tool_Crucible, 1,), ],
        [ (cmp.Tool_Sharpener, 1,), ],
        [ (cmp.Mold_BoomerangPlastic, 1,), ],
        ),
    'byproducts': (),
    },
'wooden boomerang':{
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_WOOD,10,),),
    'construct' : 3200,
    'components': (
        [ ('piece of wood', 1,), ('stick of wood', 1,), ('root', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 2,), ],
        [ (cmp.Tool_Chisel, 2,), ],
        [ (cmp.Tool_Chop, 1,), ],
        [ (cmp.Tool_Sharpener, 1,), ],
        ),
    'byproducts': ( ('shard of wood', 1,), ('scrap wood', 1,), ),
    },
'bone boomerang':{
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_BONE,10,),),
    'construct' : 6400,
    'components': (
        [ ('bone, large', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Chisel, 3,), ],
        [ (cmp.Tool_Hammer, 2,), ],
        [ (cmp.Tool_Sharpener, 1,), ],
        ),
    'byproducts': ( ('piece of bone', 2,), ('shard of bone', 2,), ('scrap bone', 2,), ),
    },
'metal boomerang':{
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_METAL,10,),),
    'sound'     : 120,
    'construct' : 4800,
    'components': (
        [ ('piece of metal', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 4,), ],
        [ (cmp.Tool_Sharpener, 3,), ],
        [ (cmp.Tool_Anvil, 2,), ],
        [ (cmp.Tool_Crucible, 2,), ],
        [ (cmp.Tool_Furnace, 2,), ],
        [ (cmp.Tool_Tongs, 2,), ],
        [ (cmp.Mold_BoomerangMetal, 1,), ],
        ),
    'byproducts': (),
    },
'ceramic boomerang':{
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_CERAMIC,20,),),
    'construct' : 7200,
    'durability': 'fixed',
    'mass'      : 'fixed',
    'components': (
        [ ('parcel of clay', 4,), ],
        [ ('sand', 16,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Sharpener, 5,), ],
        [ (cmp.Tool_Tongs, 2,), ],
        [ (cmp.Tool_Crucible, 1,), ],
        [ (cmp.Tool_Furnace, 1,), ],
        [ (cmp.Mold_BoomerangCeramic, 1,), ],
        ),
    'byproducts': (),
    },

    # javelins
'plastic javelin':{
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_PLASTIC,3,),),
    'construct' : 1000,
    'components': (
        [ ('stick of plastic', 1,), ('plastic tube', 2,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Furnace, 1,), (cmp.Tool_Torch, 1,), ],
        [ (cmp.Tool_Hammer, 1,), ],
        [ (cmp.Tool_Anvil, 1,), ],
        ),
    'byproducts': (),
    },
'wooden javelin':{
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_WOOD,3,),),
    'construct' : 1000,
    'components': (
        [ ('stick of wood', 1,), ],
        ),
    'tools'     : ( [ (cmp.Tool_Furnace, 1,), (cmp.Tool_Cut, 4,), ], ),
    'byproducts': (),
    },
'metal javelin':{
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_METAL,5,),),
    'sound'     : 120,
    'construct' : 2000,
    'components': (
        [ ('stick of metal', 1,), ('metal tube', 2,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 3,), ],
        [ (cmp.Tool_Furnace, 2,), (cmp.Tool_Torch, 3,), ],
        [ (cmp.Tool_Anvil, 2,), ],
        [ (cmp.Tool_Sharpener, 2,), (cmp.Tool_File, 3,), ],
        [ (cmp.Tool_Tongs, 1,), ],
        ),
    'byproducts': (),
    },

    # shortspears
'plastic shortspear':{
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_ASSEMBLY,3,),),
    'construct' : 600,
    'components': (
        [ ('stick of plastic', 1,), ('plastic pipe', 1,), ('stick of wood', 1,), ],
        [ ('plastic spearhead', 1,), ],
        [ ('string', 1,), ('glue', 1,), ('sinew', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 1,), ],
        [ (cmp.Tool_Chisel, 1,), ],
        ),
    'byproducts': (),
    },
'wooden shortspear':{
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_ASSEMBLY,5,),),
    'construct' : 800,
    'components': (
        [ ('stick of plastic', 1,), ('plastic pipe', 1,), ('stick of wood', 1,), ],
        [ ('wooden spearhead', 1,), ],
        [ ('string', 1,), ('glue', 1,), ('sinew', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 1,), ],
        [ (cmp.Tool_Chisel, 1,), ],
        ),
    'byproducts': (),
    },
'stone shortspear':{
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_ASSEMBLY,6,),),
    'construct' : 800,
    'components': (
        [ ('stick of plastic', 1,), ('plastic pipe', 1,), ('stick of wood', 1,), ],
        [ ('stone spearhead', 1,), ],
        [ ('string', 1,), ('sinew', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 1,), ],
        [ (cmp.Tool_Chisel, 1,), ],
        ),
    'byproducts': (),
    },
'bone shortspear':{
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_ASSEMBLY,7,),),
    'construct' : 800,
    'components': (
        [ ('stick of plastic', 1,), ('plastic pipe', 1,), ('stick of wood', 1,), ],
        [ ('bone spearhead', 1,), ],
        [ ('string', 1,), ('glue', 1,), ('sinew', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 1,), ],
        [ (cmp.Tool_Chisel, 1,), ],
        ),
    'byproducts': (),
    },
'metal shortspear':{
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_METAL,6,),),
    'sound'     : 120,
    'construct' : 1200,
    'components': (
        [ ('stick of wood', 1,), ],
        [ ('metal spearhead', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 2,), ],
        [ (cmp.Tool_Furnace, 1,), (cmp.Tool_Torch, 3,), ],
        [ (cmp.Tool_Chisel, 1,), ],
        [ (cmp.Tool_Tongs, 1,), ],
        ),
    'byproducts': (),
    },
'glass shortspear':{
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_ASSEMBLY,9,),),
    'construct' : 800,
    'components': (
        [ ('stick of plastic', 1,), ('plastic pipe', 1,), ('stick of wood', 1,), ],
        [ ('glass spearhead', 1,), ],
        [ ('string', 1,), ('sinew', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 2,), ],
        [ (cmp.Tool_Chisel, 1,), ],
        ),
    'byproducts': (),
    },

    # spears
'plastic spear':{
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_ASSEMBLY,3,),),
    'construct' : 600,
    'components': (
        [ ('pole of plastic', 1,), ('pole of wood', 1,), ],
        [ ('plastic spearhead', 1,), ],
        [ ('string', 1,), ('glue', 1,), ('sinew', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 1,), ],
        [ (cmp.Tool_Chisel, 1,), ],
        ),
    'byproducts': (),
    },
'wooden spear':{
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_ASSEMBLY,5,),),
    'construct' : 1200,
    'components': (
        [ ('pole of plastic', 1,), ('pole of wood', 1,), ],
        [ ('wooden spearhead', 1,), ],
        [ ('string', 1,), ('glue', 1,), ('sinew', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 1,), ],
        [ (cmp.Tool_Chisel, 1,), ],
        ),
    'byproducts': (),
    },
'stone spear':{
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_ASSEMBLY,6,),),
    'construct' : 1200,
    'components': (
        [ ('pole of plastic', 1,), ('pole of wood', 1,), ],
        [ ('stone spearhead', 1,), ],
        [ ('string', 1,), ('sinew', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 1,), ],
        [ (cmp.Tool_Chisel, 1,), ],
        ),
    'byproducts': (),
    },
'bone spear':{
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_ASSEMBLY,7,),),
    'construct' : 1200,
    'components': (
        [ ('pole of plastic', 1,), ('pole of wood', 1,), ],
        [ ('bone spearhead', 1,), ],
        [ ('string', 1,), ('glue', 1,), ('sinew', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 1,), ],
        [ (cmp.Tool_Chisel, 1,), ],
        ),
    'byproducts': (),
    },
'metal spear':{
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_METAL,6,),),
    'sound'     : 120,
    'construct' : 1200,
    'components': (
        [ ('pole of wood', 1,), ],
        [ ('metal spearhead', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Furnace, 1,), (cmp.Tool_Torch, 3,), ],
        [ (cmp.Tool_Hammer, 1,), ],
        [ (cmp.Tool_Chisel, 1,), ],
        [ (cmp.Tool_Tongs, 1,), ],
        ),
    'byproducts': (),
    },
'glass spear':{
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_ASSEMBLY,9,),),
    'construct' : 1200,
    'components': (
        [ ('pole of plastic', 1,), ('pole of wood', 1,), ],
        [ ('glass spearhead', 1,), ],
        [ ('string', 1,), ('sinew', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 1,), ],
        [ (cmp.Tool_Chisel, 1,), ],
        ),
    'byproducts': (),
    },

    # cudgels    
'plastic cudgel':{
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_PLASTIC,2,),),
    'sound'     : 60,
    'construct' : 1000,
    'components': (
        [ ('chunk of plastic', 1,), ],
        [ ('stick of wood', 1,), ('stick of plastic', 1,), ],
        [ ('cordage', 1,), ('glue', 1,), ],
        ),
    'tools'     : ( [(cmp.Tool_Hammer, 1),], [(cmp.Tool_Chisel, 1),], ),
    'byproducts': ( ('piece of plastic', 2,), ('shard of plastic', 4,), ('scrap plastic', 1,), ),
    },
'wooden cudgel':{
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_WOOD,3,),),
    'sound'     : 60,
    'construct' : 3000,
    'components': (
        [ ('chunk of wood', 1,), ],
        [ ('stick of wood', 1,), ],
        [ ('cordage', 1,), ('glue', 1,), ],
        ),
    'tools'     : ( [(cmp.Tool_Hammer, 2),], [(cmp.Tool_Chisel, 2),], ),
    'byproducts': ( ('piece of wood', 2,), ('shard of wood', 4,), ('scrap wood', 1,), ),
    },
'bone cudgel':{
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_BONE,5,), (SKL_WOOD,2,),),
    'sound'     : 60,
    'construct' : 4000,
    'components': (
        [ ('chunk of bone', 1,), ],
        [ ('stick of wood', 1,), ],
        [ ('cordage', 1,), ('glue', 1,), ],
        ),
    'tools'     : ( [(cmp.Tool_Hammer, 2),], [(cmp.Tool_Chisel, 3),], ),
    'byproducts': ( ('shard of bone', 4,), ('scrap bone', 1,), ),
    },
'stone cudgel':{
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_STONE,8,), (SKL_WOOD,4,),),
    'sound'     : 60,
    'construct' : 5000,
    'components': (
        [ ('chunk of stone', 1,), ],
        [ ('stick of wood', 1,), ],
        ),
    'tools'     : ( [(cmp.Tool_Hammer, 3),], [(cmp.Tool_Chisel, 4),], ),
    'byproducts': ( ('piece of stone', 2,), ('shard of stone', 4,), ('gravel', 1,), ),
    },
'metal cudgel':{
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_METAL,5,), (SKL_WOOD,5,),),
    'sound'     : 120,
    'construct' : 5000,
    'components': (
        [ ('piece of metal', 3,), ],
        [ ('stick of wood', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Furnace, 3,), ],
        [ (cmp.Tool_Hammer, 3,), ],
        [ (cmp.Tool_Anvil, 2,), ],
        [ (cmp.Tool_Tongs, 1,), ],
        ),
    'byproducts': ( ('parcel of metal', 1,), ),
    },

    # clubs
'bone heavy club':{
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_BONE,10,),),
    'sound'     : 60,
    'construct' : 4000,
    'components': (
        [ ('bone, large', 1,), ],
        ),
    'tools'     : ( [(cmp.Tool_Hammer, 2),], [(cmp.Tool_Chisel, 3),], ),
    'byproducts': ( ('shard of bone', 4,), ('scrap bone', 1,), ),
    },


    # warhammers
'plastic warhammer':{ # hammer level 2
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_PLASTIC,10,),),
    'sound'     : 60,
    'construct' : 2000,
    'components': (
        [ ('piece of plastic', 1,), ],
        [ ('stick of plastic', 1,), ('stick of wood', 1,), ],
        [ ('cordage', 2,), ('glue', 3,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 1,), ],
        [ (cmp.Tool_Chisel, 1,), ],
        ),
    'byproducts': ( ('parcel of plastic', 2,), ('scrap plastic', 1,), ),
    },
'wooden warhammer':{ # hammer level 2
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_WOOD,10,),),
    'sound'     : 60,
    'construct' : 3200,
    'components': (
        [ ('piece of wood', 1,), ],
        [ ('stick of plastic', 1,), ('stick of wood', 1,), ],
        [ ('cordage', 2,), ('glue', 3,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Chop, 1,), ],
        [ (cmp.Tool_Hammer, 1,), ],
        [ (cmp.Tool_Chisel, 1,), (cmp.Tool_Anvil, 1,), ],
        ),
    'byproducts': ( ('parcel of wood', 1,), ('scrap wood', 1,), ),
    },
'stone warhammer':{ # hammer level 2
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_STONE,10,),),
    'sound'     : 60,
    'construct' : 4800,
    'components': (
        [ ('piece of stone', 1,), ],
        [ ('stick of plastic', 1,), ('stick of wood', 1,), ],
        [ ('cordage', 2,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 2,), ],
        [ (cmp.Tool_Chisel, 2,), ],
        ),
    'byproducts': ( ('parcel of stone', 2,), ('gravel', 1,), ),
    },
'bone warhammer':{ # hammer level 2
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_BONE,10,),),
    'sound'     : 60,
    'construct' : 6400,
    'components': (
        [ ('piece of bone', 1,), ],
        [ ('stick of plastic', 1,), ('stick of wood', 1,), ],
        [ ('cordage', 3,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 1,), ],
        [ (cmp.Tool_Chisel, 2,), ],
        ),
    'byproducts': ( ('scrap bone', 1,), ('scrap wood', 1,), ),
    },
'metal warhammer':{ # hammer level 3
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_METAL,10,),),
    'sound'     : 120,
    'construct' : 10800,
    'components': (
        [ ('piece of metal', 1,), ],
        [ ('stick of wood', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 3,), ],
        [ (cmp.Tool_Furnace, 2,), ],
        [ (cmp.Tool_Anvil, 2,), ],
        [ (cmp.Tool_Tongs, 2,), ],
        ),
    'byproducts': ( ('scrap wood', 1,), ),
    },







    #--------------------------#
    #      Ranged Weapons      #
    #--------------------------#



    # bows
'plastic bow':{
    'quantity'  : 1,
    'table'     : CRT_RANGED,
    'skills'    : ((SKL_PLASTIC,6,),),
    'construct' : 4800,
    'components': (
        [ ('plastic pipe', 1,), ],
        [ ('cordage', 2,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Cut, 3,), ],
        [ (cmp.Tool_Furnace, 1,), ],
        ),
    'byproducts': (),
    },
'wooden bow':{
    'quantity'  : 1,
    'table'     : CRT_RANGED,
    'skills'    : ((SKL_BOWYER,10,), (SKL_WOOD,5,),),
    'construct' : 9600, # should we have a requirement for wetting the wood first?
    'components': (
        [ ('stick of wood', 1,), ],
        [ ('cordage', 2,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Cut, 4,), ],
        [ (cmp.Tool_Chop, 2,), ],
        ),
    'byproducts': (),
    },
'wooden longbow':{
    'quantity'  : 1,
    'table'     : CRT_RANGED,
    'skills'    : ((SKL_BOWYER,20,), (SKL_WOOD,15,),),
    'construct' : 12000,
    'components': (
        [ ('pole of wood', 1,), ],
        [ ('cordage', 3,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Cut, 4,), ],
        [ (cmp.Tool_Chop, 2,), ],
        ),
    'byproducts': (),
    },
'unfinished composite bow':{ # note: must dry to finish (takes a long time).
    #Note: must wax (or grease?) bow to give it resistance to water
    'quantity'  : 1,
    'table'     : CRT_RANGED,
    'skills'    : ((SKL_BOWYER,40,), (SKL_WOOD,5), (SKL_BONE,10),),
    'construct' : 27200,
    'components': (
        [ ('horn', 1,), ],
        [ ('sinew', 1,), ],
        [ ('stick of wood', 1,), ],
        [ ('parcel of plastic', 1,), ],
        [ ('glue', 4,), ],
        [ ('cordage', 2,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Cut, 6,), ],
        [ (cmp.Tool_Chop, 2,), ],
        ),
    'byproducts': (),
    },

    # caplock guns
'caplock pistol':{
    'quantity'  : 1,
    'table'     : CRT_RANGED,
    'skills'    : ((SKL_GUNSMITH,10,),),
    'construct' : 4800,
    'components': (
        [ ('caplock pistol grip', 1,), ],
        [ ('gun barrel, short', 1,), ],
        [ ('caplock trigger mechanism', 1,), ],
        [ ('screw', 2,), ],
        [ ('glue', 1,), ('nail', 2,), ('duct tape', 5,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Drill, 3,), ],
        [ (cmp.Tool_Furnace, 2,), (cmp.Tool_Weld, 2,), ],
        [ (cmp.Tool_Hammer, 2,), ],
        [ (cmp.Tool_Pliers, 1,), (cmp.Tool_Screwdriver, 1,), ],
        ),
    'byproducts': (),
    },
'caplock musketoon':{ # short musket. Regular sized barrel. Fat barreled musketoons existed, too, and should maybe be another item.
    'quantity'  : 1,
    'table'     : CRT_RANGED,
    'skills'    : ((SKL_GUNSMITH,8,),),
    'construct' : 7200,
    'components': (
        [ ('musketoon stock', 1,), ],
        [ ('gun barrel', 1,), ],
        [ ('caplock trigger mechanism', 1,), ],
        [ ('screw', 2,), ],
        [ ('glue', 1,), ('nail', 2,), ('duct tape', 5,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Drill, 3,), ],
        [ (cmp.Tool_Furnace, 2,), (cmp.Tool_Weld, 2,), ],
        [ (cmp.Tool_Hammer, 2,), ],
        [ (cmp.Tool_Pliers, 1,), (cmp.Tool_Screwdriver, 1,), ],
        ),
    'byproducts': (),
    },
'caplock musket':{
    'quantity'  : 1,
    'table'     : CRT_RANGED,
    'skills'    : ((SKL_GUNSMITH,6,),),
    'construct' : 9600,
    'components': (
        [ ('musket stock', 1,), ],
        [ ('gun barrel, long', 1,), ],
        [ ('caplock trigger mechanism', 1,), ],
        [ ('screw', 2,), ],
        [ ('glue', 1,), ('nail', 2,), ('duct tape', 5,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Drill, 3,), ],
        [ (cmp.Tool_Furnace, 2,), (cmp.Tool_Weld, 2,), ],
        [ (cmp.Tool_Hammer, 2,), ],
        [ (cmp.Tool_Pliers, 1,), (cmp.Tool_Screwdriver, 1,), ],
        ),
    'byproducts': (),
    },

}
# end RECIPES





# other recipes that might should be handled differently or just not used


##'pipe gun':{ # shoots larger shots than musketoon/pistol/musket. 
##    'quantity'  : 1,
##    'table'     : CRT_RANGED,
##    'category'  : CRC_GUNSMITH,
##    'construct' : 4800,
##    'components': (
##        [ ('musketoon stock', 1,), ],
##        [ ('metal pipe', 1,), ],
##        [ ('caplock trigger mechanism', 1,), ],
##        [ ('screw', 2,), ],
##        [ ('glue', 1,), ('nail', 2,), ('duct tape', 5,), ],
##        ),
##    'tools'     : (
##        [ (cmp.Tool_Drill, 3,), ],
##        [ (cmp.Tool_Furnace, 2,), (cmp.Tool_Weld, 2,), ],
##        [ (cmp.Tool_Hammer, 2,), ],
##        [ (cmp.Tool_Pliers, 1,), (cmp.Tool_Screwdriver, 1,), ],
##        ),
##    'byproducts': (),
##    },



'''
    Should all of this be simply handled by destruction of things?
    When you attack a twig and destroy it, it gives you a parcel of wood.
    This would be simpler, easier, more intuitive.
'''

##
##    #--------------------------#
##    # Raw materials / Raw mats #
##    #--------------------------#
##
##
##
##'parcel of plastic':{
##    'quantity'  : 1,
##    'table'     : CRT_RAWMATS,
##    'category'  : CRC_BREAKINGDOWN,
##    'construct' : 100,
##    'destruct'  : 0,
##    'components': (
##        [ ('plastic cup', 1,), ],
##        ),
##    'tools'     : (
##        ( (CUTS, 1,), ),
##        ),
##    'byproducts': (),
##    'recycling' : (),
##    },
##
##'piece of plastic':{
##    'quantity'  : 1,
##    'table'     : CRT_RAWMATS,
##    'category'  : CRC_BREAKINGDOWN,
##    'construct' : 100,
##    'destruct'  : 0,
##    'components': (
##        [ ('plastic stick', 1,), ('plastic bottle', 1,), ],
##        ),
##    'tools'     : (
##        ( (CUTS, 5,), ),
##        ),
##    'byproducts': (),
##    'recycling' : (),
##    },
##
##'parcel of wood':{
##    'quantity'  : 1,
##    'table'     : CRT_RAWMATS,
##    'category'  : CRC_BREAKINGDOWN,
##    'construct' : 10,
##    'destruct'  : 0,
##    'components': (
##        [ ('twig', 1,), ],
##        ),
##    'tools'     : (
##        ( (CHOPS, 1,), ),
##        ),
##    'byproducts': (),
##    'recycling' : (),
##    },
##
##'piece of wood':{
##    'quantity'  : 1,
##    'table'     : CRT_RAWMATS,
##    'category'  : CRC_BREAKINGDOWN,
##    'construct' : 100,
##    'destruct'  : 0,
##    'components': (
##        [ ('wooden stick', 1,), ],
##        ),
##    'tools'     : (
##        ( (CHOPS, 5,), ),
##        ),
##    'byproducts': ( ('wooden splinters', 1,), ),
##    'recycling' : (),
##    },
##
##'chunk of wood':{
##    'quantity'  : 1,
##    'table'     : CRT_RAWMATS,
##    'category'  : CRC_BREAKINGDOWN,
##    'construct' : 300,
##    'destruct'  : 0,
##    'components': (
##        [ ('log', 1,), ],
##        ),
##    'tools'     : (
##        ( (CHOPS, 10,), ),
##        ),
##    'byproducts': ( ('parcel of wood', 3,), ),
##    'recycling' : (),
##    },
##
