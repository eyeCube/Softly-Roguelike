'''
    recipes.py
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


    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
            Information about recipes and crafting is as follows.

    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

data of key,values in key-value pairs of RECIPES dict:
    tuple of dictionaries where each dict is a recipe for making the item
        specified by the key string (one item can have multiple recipes).
data of nested recipe dict:
    key = result (name of object to create)
    values = 
    quantity   : number of instances of object to make (if output is quantifiable)
    table      : const. referring to which data table holds the object's info
    category   : const. referring to what skill is used in crafting this recipe
    construct  : action points (AP) it takes to create per recipe
    components : items used to craft the result, and the quantity needed
        ** material type determined by the first component-list in the tuple
    tools      : tools needed to craft the result, and the durability used (assuming hardness of tool's mat == hardness of item mat. Hardness determined by material. Metal vs. wood does not dull (damage) metal very much, but wood vs. metal destroys the wood easily.)
    using      : tools that will contain the product throughout the construction
                    e.g. a furnace which contains food that's cooking.
                    These tools have a quality as well as a quantity (capacity).
    byproducts : raw materials that are created in addition to the result (all are from the table RAWMATS, so table is not specified)
special additional data that can be provided:
        (if not provided, the default will be assumed)
    overhead   : AP it takes to create (static no matter how many you make)
    requires   : string, special requirements to craft this item
                    * default: "none"
    catalysts  : tools not needed, but which speed up process
    celsius    : temperature (if not room temperature) of the finished
                    product at the moment of completion (celsius)
    info       : extra information for the recipe (default, none)
                    * "auto" -- the recipe makes itself; only AP cost
                        for the PC is the overhead.
                    * "quantity-approximate" -- quantities of components
                        can be more or less than reported amounts. +/- 10%
                    * "quantity-lenient" -- like quantity-approximate,
                        but it's even more lenient. Ratios of spices etc.
                        are much more lenient in quantities than others
                        (can use 3x as much spice as recipe calls for and
                        it will still be fine, just extra spicy.)
                    * "components-by-mass" -- the components are quantified
                        in terms of their mass in KG.
                    * "byproducts-by-mass" -- the byproducts are quantified
                        in terms of their mass in KG.
                    * "ratios" -- the components are measured in terms of
                        the ratio of their masses rather than an absolute
                        quantity or mass. The output quantity depends on
                        the input quantity; if total mass of ingredients
                        adds up to e.g. 100g, then the total output (+ any
                        byproducts) together add up to 100g as well.
                    * "turn-up-the-heat" -- recipe requires that components
                        be cooked, but turning up the heat (by using a
                        higher quality furnace or stove) will reduce the
                        time it takes to make it.
    terrain    : string, what terrain type(s) the recipe must be built on
                    * default: 'any'
                    * "flat" - must be built on flat ground
                    * "pit" - must be built on a pit (hole)
                    * "water" - must be built in water
    sound      : int, amount of audible noise produced during crafting
                    * default: 0
    mass**     : string, special var indicating how the mass is calculated for the result.
                    * default: "sum-minus-byproducts" - total mass of
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
                    * default: "first-component" - the material of the first component becomes the material type of the result.
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
        * hack job: construct AP cut to 1/4
            x10 chance of failure.
            x15 chance to make crude items.
            x1/16 chance to make quality items.
            x0 chance - masterpiece
        * quick job: construct AP cut to 1/2
            x4 chance of failure.
            x6 chance to make crude items.
            x1/4 chance to make quality items.
            x0 chance - masterpiece
        * normal job: construct AP 100%
            x1 chance of failure.
            x1 chance to make crude items.
            x1 chance to make quality items.
            x0 chance - masterpiece
        * detailed job: construct AP x2 (skill level: 10+)
            x1/4 chance - failure
            x1/4 chance - crude
            x5 chance to make quality items.
            x1/16 chance - masterpiece
        * fine job: construct AP x4 (skill level: 20+)
            x1/16 chance - failure
            x1/16 chance - crude
            x10 chance to make quality items.
            x1 chance to make masterpiece items.
        * meticulous job: construct AP x8 (skill level: 40+)
            x1/64 chance - failure
            x1/64 chance - crude
            x20 chance to make at least quality items
            x5 chance to make masterpiece items.
        * thesis job: construct AP x16 (skill level: 60+)
            x1/256 chance - failure
            x1/256 chance - crude
            x50 chance to make at least quality items
            x25 chance to make masterpiece items.
        **Doing a detailed job or greater may require different recipes.
            It may also require:
                - adequate skill in the relevant crafting technique
                - quality ingredients (extremely hard to make a masterpiece w/ shit ingredients, it's tough to make quality items with standard items, and crude ingredients tend to yield crude results; yet you never truly NEED quality ingredients....)
                - quality tools (see quality ingredients)
                - increased patience (monsters will rarely do long jobs)
                - no stress or distractions (quality work environment)
                - vision and light level to be at a certain value or higher
                - specialist skills
            IDEA: what constitutes a "quality" or "masterpiece" item
                also depends on the skill of the artisan.
                Quality for a skill-level 10 artisan is a +1 item;
                for a level-100 master, a quality item can be +3, +5, etc.
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



'''


from const import *


RECIPES={

    
##'column of wood':({
##    'quantity'  : 1,
##    'table'     : CRT_STUFF,
##    'category'  : CRC_ASSEMBLY,
##    'construct' : 3,
##    'destruct'  : 0,
##    'components': (
##        [ ('wooden plank', 3,), ],
##        [ ('glue', 2,), ],
##        ),
##    'tools'     : (),
##    'byproducts': (),
##    'recycling' : ( ('wooden plank', 3,) ,),
##    },),
    
'':({
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_ASSEMBLY,1,),),
    'sound'     : 0,
    'construct' : 0,
    'requires'  : (),
    'components': (
        [ ('', 1,), ],
        ),
    'tools'     : (),
    'using'     : (),
    'byproducts': (),
    },),






    #--------------------------#
    #        Raw Mats          #
    #--------------------------#



    # wood
##'wooden plank':({
##    'quantity'  : 20,
##    'table'     : CRT_RAWMATS,
##    'category'  : CRC_WOOD,
##    'construct' : 48,
##    'components': ( [ ('slab of wood', 1,), ], ),
##    'tools'     : ( [ (cmp.Tool_Saw, 4,), ], ),
##    'byproducts': (),
##    },),
##'slab of wood':({ # harvestable instead of recipe
##    'quantity'  : 2,
##    'table'     : CRT_RAWMATS,
##    'category'  : CRC_WOOD,
##    'construct' : 48,
##    'components': ( [ ('log', 1,), ], ),
##    'tools'     : ( [ (cmp.Tool_Saw, 4,), ], ),
##    'byproducts': (
##        ('chunk of wood', 4,), ('piece of wood', 4,),
##        ('parcel of wood', 4,), ('scrap wood', 4,), ),
##    },),

    # cloth
'scrap cloth':({
    'quantity'  : 1,
    'table'     : CRT_RAWMATS,
    'skills'    : ((SKL_SEWING,1,),),
    'construct' : 18,
    'components': ( [ ('string', 9,), ], ),
    'tools'     : ( [ (cmp.Tool_Sew, 3,), ], ),
    'using'     : (),
    'byproducts': (),
    },),
'parcel of cloth':({
    'quantity'  : 1,
    'table'     : CRT_RAWMATS,
    'skills'    : ((SKL_SEWING,2,),),
    'construct' : 18,
    'components': ( [ ('scrap cloth', 5,), ], ),
    'tools'     : ( [ (cmp.Tool_Sew, 3,), ], ),
    'using'     : (),
    'byproducts': (),
    },),
'piece of cloth':({
    'quantity'  : 1,
    'table'     : CRT_RAWMATS,
    'skills'    : ((SKL_SEWING,3,),),
    'construct' : 24,
    'components': ( [ ('parcel of cloth', 5,), ], ),
    'tools'     : ( [ (cmp.Tool_Sew, 3,), ], ),
    'using'     : (),
    'byproducts': (),
    },),
'chunk of cloth':({
    'quantity'  : 1,
    'table'     : CRT_RAWMATS,
    'skills'    : ((SKL_SEWING,4,),),
    'construct' : 32,
    'components': ( [ ('piece of cloth', 5,), ], ),
    'tools'     : ( [ (cmp.Tool_Sew, 3,), ], ),
    'using'     : (),
    'byproducts': (),
    },),

    # metal
'scrap metal':({
    'quantity'  : 1,
    'table'     : CRT_RAWMATS,
    'skills'    : ((SKL_METAL,1,),),
    'construct' : 12,
    'components': (
        [ ('metal ore', 1,), ],
        [ ('coke', 1,), ],
        ),
    'tools'     : ( [ (cmp.Tool_Tongs, 2,), ], ),
    'using'     : (
        [ (cmp.Tool_Furnace, 3,), ],
        [ (cmp.Tool_Crucible, 2,), ],
        ),
    'byproducts': ( ('slag', 1,), ),
    },),
'parcel of metal':({
    'quantity'  : 1,
    'table'     : CRT_RAWMATS,
    'skills'    : ((SKL_METAL,1,),),
    'construct' : 16,
    'components': ( [ ('scrap metal', 5,), ], ),
    'tools'     : ( [ (cmp.Tool_Tongs, 2,), ], ),
    'using'     : (
        [ (cmp.Tool_Furnace, 3,), ],
        [ (cmp.Tool_Crucible, 2,), ],
        ),
    'byproducts': (),
    },),
'shard of metal':({
    'quantity'  : 1,
    'table'     : CRT_RAWMATS,
    'skills'    : ((SKL_METAL,2,),),
    'construct' : 24,
    'components': ( [ ('parcel of metal', 1,), ], ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 3,), ],
        [ (cmp.Tool_Anvil, 2,), ],
        [ (cmp.Tool_Tongs, 2,), ],
        ),
    'using'     : ( [ (cmp.Tool_Furnace, 2,), ], ),
    'byproducts': (),
    },),
'piece of metal':({
    'quantity'  : 1,
    'table'     : CRT_RAWMATS,
    'skills'    : ((SKL_METAL,1,),),
    'construct' : 24,
    'components': ( [ ('scrap metal', 25,), ('parcel of metal', 5,), ], ),
    'tools'     : (
        [ (cmp.Tool_Tongs, 2,), ],
        ),
    'using'     : (
        [ (cmp.Tool_Furnace, 3,), ],
        [ (cmp.Tool_Crucible, 2,), ],
        ),
    'byproducts': (),
    },),
'chunk of metal':({
    'quantity'  : 1,
    'table'     : CRT_RAWMATS,
    'skills'    : ((SKL_METAL,2,),),
    'construct' : 32,
    'components': (
        [ ('scrap metal', 125,), ('parcel of metal', 25,),
          ('piece of metal', 5,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Tongs, 2,), ],
        ),
    'using'     : (
        [ (cmp.Tool_Furnace, 3,), ],
        [ (cmp.Tool_Crucible, 2,), ],
        ),
    'byproducts': (),
    },),
'slab of metal':({
    'quantity'  : 1,
    'table'     : CRT_RAWMATS,
    'skills'    : ((SKL_METAL,3,),),
    'construct' : 48,
    'components': (
        [ ('scrap metal', 625,), ('parcel of metal', 125,),
          ('piece of metal', 25,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Tongs, 3,), ],
        ),
    'using'     : (
        [ (cmp.Tool_Furnace, 4,), ],
        [ (cmp.Tool_Crucible, 3,), ],
        ),
    'byproducts': (),
    },),





    #--------------------------#
    #         Cooking          #
    #--------------------------#

    # Food

'dry dough':({
    'quantity'  : 1,
    'table'     : CRT_FOOD,
    'skills'    : ((SKL_COOKING,3,),),
    'construct' : 12,
    'overhead'  : 32,
    'info'      : ('quantity-lenient', 'components-by-mass',),
    'components': (
        [ ('flour', 0.100,), ], #100g
        [ ('water', 0.030,), ], #30g    drier than most bread -- half as much water as usual bread
        [ ('salt',  0.003,), ], #3g
        ),
    'tools'     : (),
    'using'     : ( [ (cmp.Tool_Bowl, 1,), ], ),
    'catalysts' : ( [ (cmp.Tool_RollingPin, 1,), ], ),
    'byproducts': (),
    },),
'dough':({
    'quantity'  : 1,
    'table'     : CRT_FOOD,
    'skills'    : ((SKL_COOKING,3,),),
    'construct' : 16,
    'overhead'  : 32,
    'info'      : ('quantity-lenient', 'components-by-mass',),
    'components': (
        [ ('flour', 0.100,), ], #100g
        [ ('water', 0.060,), ], #60g
        [ ('salt',  0.003,), ], #3g
        ),
    'tools'     : (),
    'using'     : ( [ (cmp.Tool_Bowl, 1,), ], ),
    'catalysts' : ( [ (cmp.Tool_RollingPin, 1,), ], ),
    'byproducts': (),
    },),
'hard tack':({
    'quantity'  : 1,
    'table'     : CRT_FOOD,
    'skills'    : ((SKL_COOKING,8,),),
    'construct' : 7200,
    'overhead'  : 2,
    'info'      : ('auto',),
    'celsius'   : 140,
    'components': ( [ ('dry dough', 1,), ], ),
    'tools'     : (),
    'using'     : (
        [ (cmp.Tool_Furnace, 2,), ],
        [ (cmp.Tool_Tray, 2,), ],
        ),
    'byproducts': (),
    },),
'bread loaf':({
    'quantity'  : 1,
    'table'     : CRT_FOOD,
    'skills'    : ((SKL_COOKING,6,),),
    'construct' : 1800,
    'overhead'  : 2,
    'celcius'   : 90,
    'info'      : ('auto',),
    'components': ( [ ('dough', 4,), ], ),
    'tools'     : (),
    'using'     : (
        [ (cmp.Tool_Furnace, 1,), ],
        [ (cmp.Tool_LoafPan, 1,), ],
        ),
    'byproducts': (),
    },),
'beef strip':({
    'quantity'  : 8,
    'table'     : CRT_FOOD,
    'skills'    : ((SKL_COOKING,8,),(SKL_KNIVES,5,),),
    'construct' : 64,
    'info'      : ('auto', 'byproducts-by-mass',),
    'components': ( [ ('parcel of beef', 1,), ], ),
    'tools'     : ( [ (cmp.Tool_Cut, 5,), ], ),
    'using'     : ( [ (cmp.Tool_ChoppingBlock, 1,), ], ),
    'byproducts': ( [ ('fat', 0.05,), ], ),
    },
'dried beef':({ # using oven
    'quantity'  : 1,
    'table'     : CRT_FOOD,
    'skills'    : ((SKL_COOKING,10,),),
    'construct' : 1800,
    'overhead'  : 4,
    'celsius'   : 80,
    'info'      : ('auto',),
    'components': ( [ ('beef strip', 1,), ], ),
    'tools'     : (),
    'using'     : (
        [ (cmp.Tool_Furnace, 1,), ],
        [ (cmp.Tool_Tray, 1,), ],
        ),
    'byproducts': (),
    },
              { # using dehydrator
    'quantity'  : 1,
    'table'     : CRT_FOOD,
    'skills'    : ((SKL_COOKING,2,),),
    'construct' : 1800,
    'overhead'  : 4,
    'info'      : ('auto',),
    'components': ( [ ('beef strip', 1,), ], ),
    'tools'     : (),
    'using'     : ( [ (cmp.Tool_Dehydrator, 1,), ], ),
    'byproducts': (),
    },),
'melted fat':({
    'quantity'  : 1,
    'table'     : CRT_FOOD,
    'skills'    : ((SKL_COOKING,5,),),
    'construct' : 144,
    'overhead'  : 16,
    'info'      : ('turn-up-the-heat',),
    'components': ( [ ('fat', 1,), ], ),
    'tools'     : (),
    'using'     : (
        [ (cmp.Tool_Stove, 1,), (cmp.Tool_Furnace, 1,), ],
        [ (cmp.Tool_Pot, 1,), ],
        ),
    'byproducts': (),
    },),
'pemmican':({
    'quantity'  : 1,
    'table'     : CRT_FOOD,
    'skills'    : ((SKL_COOKING,2,),),
    'construct' : 144,
    'overhead'  : 2,
    'info'      : ('ratios',
                   'quantity-lenient',),
    'components': (
        [ ('dried beef', 8,), ],
        [ ('melted suet', 8,), ],
        [ ('dried blueberry', 1,), ],
        ),
    'tools'     : (),
    'using'     : (),
    'byproducts': (),
    },),





    #--------------------------#
    #          Stuff           #
    #--------------------------#


    # MISC. STUFF

    # mixtures of materials
'tinder':({
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_ASSEMBLY,1,),),
    'construct' : 1,
    'components': (
        [ ('scrap wood', 1,), ('twig', 1,), ],
        [ ('foliage', 1,), ('string', 1,), ('paper', 1,), ],
        ),
    'tools'     : (),
    'using'     : (),
    'byproducts': (),
    },),
'plastic stool':({
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_PLASTIC,1,),),
    'sound'     : 60,
    'construct' : 10,
    'components': (
        [ ('chunk of plastic', 1,), ],
        [ ('stick of plastic', 3,), ('plastic tube', 3,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 2,), ],
        [ (cmp.Tool_Saw, 2,), ],
        [ (cmp.Tool_Weld, 1,), (cmp.Tool_Torch, 2,), ],
        ),
    'using'     : (),
    'byproducts': (),
    },),
'wooden stool':({
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_WOOD,2,),),
    'sound'     : 60,
    'construct' : 20,
    'components': (
        [ ('chunk of wood', 1,), ],
        [ ('stick of wood', 3,), ],
        [ ('nail', 3,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 2,), ],
        [ (cmp.Tool_Saw, 2,), ],
        ),
    'using'     : (),
    'byproducts': (
        ('piece of wood', 1,), ('parcel of wood', 1,), ('scrap wood', 1,),
        ),
    },),
'metal stool':({
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_METAL,2,),),
    'sound'     : 120,
    'construct' : 32,
    'components': (
        [ ('chunk of metal', 1,), ],
        [ ('stick of metal', 3,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 3,), ],
        [ (cmp.Tool_Weld, 3,), ],
        [ (cmp.Tool_Tongs, 2,), ],
        ),
    'using'     : (
        [ (cmp.Tool_Anvil, 3,), ],
        [ (cmp.Tool_Furnace, 2,), ],
        ),
    'byproducts': (),
    },),
'plastic table':({
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_PLASTIC,1,),),
    'sound'     : 60,
    'construct' : 14,
    'components': (
        [ ('slab of plastic', 1,), ],
        [ ('stick of plastic', 4,), ('plastic tube', 4,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 2,), ],
        [ (cmp.Tool_Saw, 2,), ],
        [ (cmp.Tool_Tongs, 2,), ],
        [ (cmp.Tool_Weld, 1,), (cmp.Tool_Torch, 2,), ],
        [ (cmp.Mold_TablePlastic, 1,), ],
        ),
    'using'     : (
        [ (cmp.Tool_Furnace, 2,), ],
        [ (cmp.Tool_Crucible, 1,), ],
        ),
    'byproducts': (),
    },),
'wooden table':({
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_WOOD,3,),),
    'sound'     : 60,
    'construct' : 48,
    'components': (
        [ ('wooden plank', 6,), ],
        [ ('stick of wood', 4,), ],
        [ ('nail', 16,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 2,), ],
        [ (cmp.Tool_Saw, 2,), ],
        ),
    'using'     : (),
    'byproducts': (),
    },),
'metal table':({
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_METAL,5,),),
    'sound'     : 120,
    'construct' : 72,
    'components': (
        [ ('slab of metal', 1,), ],
        [ ('stick of metal', 4,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 3,), ],
        [ (cmp.Tool_Tongs, 3,), ],
        [ (cmp.Tool_Weld, 3,), ],
        ),
    'using'     : (
        [ (cmp.Tool_Anvil, 3,), ],
        [ (cmp.Tool_Furnace, 2,), ],
        ),
    'byproducts': (),
    },),

    # gunsmithing
'musket stock':({
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_GUNSMITH,3,), (SKL_WOOD,7,),),
    'construct' : 72,
    'components': ( [ ('slab of wood', 1,), ], ),
    'tools'     : (
        [ (cmp.Tool_Cut, 5,), ],
        [ (cmp.Tool_Chisel, 4,), ],
        [ (cmp.Tool_Hammer, 3,), ],
        [ (cmp.Tool_Saw, 3,), ],
        ),
    'using'     : (),
    'byproducts': (
        ('chunk of wood', 2,),
        ('piece of wood', 2,),
        ('parcel of wood', 2,),
        ('scrap wood', 2,),
        ),
    },),
'caplock trigger mechanism':({
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_GUNSMITH,15,), (SKL_METAL,5,),),
    'construct' : 48,
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
    'using'     : (),
    'byproducts': (),
    },),
'gun barrel, short':({
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_GUNSMITH,6,), (SKL_METAL,10,),),
    'construct' : 432,
    'components': (
        [ ('metal bar', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Drill, 4,), ],
        [ (cmp.Tool_Hammer, 4,), ],
        [ (cmp.Tool_Mandril, 1,), ],
        [ (cmp.Tool_Swage, 1,), ],
        [ (cmp.Tool_Tongs, 1,), ],
        ),
    'using'     : (
        [ (cmp.Tool_Anvil, 3,), ],
        [ (cmp.Tool_Furnace, 3,), ],
        ),
    'byproducts': (),
    },),
'gun barrel':({
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_GUNSMITH,5,), (SKL_METAL,5,),),
    'construct' : 96,
    'components': ( [ ('gun barrel, short', 2,), ], ),
    'tools'     : (
        [ (cmp.Tool_Drill, 4,), ],
        [ (cmp.Tool_Hammer, 4,), ],
        [ (cmp.Tool_File, 5,), (cmp.Tool_Grinder, 4,), ],
        [ (cmp.Tool_Furnace, 3,), (cmp.Tool_Weld, 3,), ],
        [ (cmp.Tool_Anvil, 2,), ],
        [ (cmp.Tool_Mandril, 1,), ],
        [ (cmp.Tool_Tongs, 1,), ],
        ),
    'using'     : (),
    'byproducts': (),
    },),
'gun barrel, long':({
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_GUNSMITH,5,), (SKL_METAL,5,),),
    'construct' : 96,
    'components': ( [ ('gun barrel', 1,), ], [ ('gun barrel, short', 1,), ], ),
    'tools'     : (
        [ (cmp.Tool_Drill, 4,), ],
        [ (cmp.Tool_Hammer, 4,), ],
        [ (cmp.Tool_File, 5,), (cmp.Tool_Grinder, 4,), ],
        [ (cmp.Tool_Furnace, 3,), (cmp.Tool_Weld, 3,), ],
        [ (cmp.Tool_Anvil, 2,), ],
        [ (cmp.Tool_Mandril, 1,), ],
        [ (cmp.Tool_Tongs, 1,), ],
        ),
    'using'     : (),
    'byproducts': (),
    },),

    # metal
'metal needle':({
    'quantity'  : 1,
    'table'     : CRT_RAWMATS,
    'skills'    : ((SKL_METAL,6,),),
    'construct' : 18,
    'components': (
        [ ('paperclip', 1,), ('scrap metal', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Cut, 8,), ],
        [ (cmp.Tool_Hammer, 4,), ],
        [ (cmp.Tool_Anvil, 3,), ],
        ),
    'using'     : (),
    'byproducts': (),
    },),
'pop tab mail ring':({
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_METAL,1,),),
    'construct' : 50,
    'components': ( [ ('pop tab', 1,), ], ),
    'tools'     : (
        [ (cmp.Tool_Cut, 6,), ],
        [ (cmp.Tool_Pliers, 1,), ],
        ),
    'using'     : (),
    'byproducts': (),
    },),
'mail ring, riveted':({
    'quantity'  : 8,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_METAL,12,),),
    'construct' : 16,
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
    'using'     : (),
    'byproducts': ( ('scrap metal', 2,), ),
    },),
'mail ring, welded':({
    'quantity'  : 4,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_METAL,4,),),
    'construct' : 8,
    'mass'      : 'fixed',
    'components': (
        [ ('metal wire', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Cut, 8,), ],
        [ (cmp.Tool_Pliers, 2,), ],
        [ (cmp.Tool_Weld, 1,), (cmp.Tool_Torch, 3,), ],
        ),
    'using'     : (),
    'byproducts': (),
    },),

    # arrowheads
'plastic arrowhead':({
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_PLASTIC,5,),),
    'sound'     : 60,
    'construct' : 3,
    'components': (
        [ ('shard of plastic', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Cut, 4,), ],
        [ (cmp.Tool_Sharpener, 1,), (cmp.Tool_File, 1,), ],
        ),
    'using'     : (),
    'byproducts': ( ('scrap plastic', 1,), ),
    },),
'wooden arrowhead':({
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_WOOD,5,),),
    'sound'     : 60,
    'construct' : 5,
    'components': (
        [ ('shard of wood', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Cut, 5,), ],
        [ (cmp.Tool_Sharpener, 1,), (cmp.Tool_File, 2,), ],
        ),
    'using'     : (),
    'byproducts': ( ('scrap wood', 1,), ),
    },),
'bone arrowhead':({
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_BONE,10,),),
    'sound'     : 60,
    'construct' : 8,
    'components': (
        [ ('shard of bone', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 3,), ],
        [ (cmp.Tool_Chisel, 2,), ],
        [ (cmp.Tool_Sharpener, 1,), (cmp.Tool_File, 3,), ],
        ),
    'using'     : (),
    'byproducts': ( ('scrap bone', 1,), ),
    },),
'stone arrowhead':({
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_STONE,10,),),
    'sound'     : 60,
    'construct' : 12,
    'components': (
        [ ('shard of stone', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 3,), ],
        [ (cmp.Tool_Chisel, 3,), ],
        [ (cmp.Tool_Sharpener, 2,), (cmp.Tool_File, 4,), ],
        ),
    'using'     : (),
    'byproducts': ( ('gravel', 1,), ),
    },),
'metal arrowhead':({
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_METAL,15,),),
    'sound'     : 120,
    'construct' : 20,
    'components': (
        [ ('shard of metal', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 3,), ],
        [ (cmp.Tool_Furnace, 2,), (cmp.Tool_Torch, 3,), ],
        [ (cmp.Tool_Anvil, 3,), ],
        [ (cmp.Tool_Sharpener, 2,), (cmp.Tool_File, 5,), ],
        [ (cmp.Tool_Tongs, 1,), ],
        ),
    'using'     : (),
    'byproducts': (),
    },),
'glass arrowhead':({
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_GLASS,20,),),
    'sound'     : 60,
    'construct' : 30,
    'components': (
        [ ('shard of glass', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 4,), ],
        [ (cmp.Tool_Chisel, 4,), ],
        ),
    'using'     : (),
    'byproducts': (),
    },),


    # spearheads
'plastic spearhead':({
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_PLASTIC,5,),),
    'sound'     : 60,
    'construct' : 5,
    'components': (
        [ ('piece of plastic', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Cut, 4,), ],
        [ (cmp.Tool_Sharpener, 1,), (cmp.Tool_File, 1,), ],
        ),
    'using'     : (),
    'byproducts': ( ('scrap plastic', 1,), ),
    },),
'wooden spearhead':({
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_WOOD,6,),),
    'sound'     : 60,
    'construct' : 10,
    'components': (
        [ ('piece of wood', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Cut, 4,), ],
        [ (cmp.Tool_Hammer, 2,), ],
        [ (cmp.Tool_Chisel, 2,), ],
        [ (cmp.Tool_Sharpener, 1,), (cmp.Tool_File, 2,), ],
        ),
    'using'     : (),
    'byproducts': ( ('scrap wood', 1,), ),
    },),
'bone spearhead':({
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_BONE,10,),),
    'sound'     : 60,
    'construct' : 15,
    'components': (
        [ ('piece of bone', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 3,), ],
        [ (cmp.Tool_Chisel, 2,), ],
        [ (cmp.Tool_Sharpener, 1,), (cmp.Tool_File, 3,), ],
        ),
    'using'     : (),
    'byproducts': ( ('scrap bone', 1,), ),
    },),
'stone spearhead':({
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_STONE,12,),),
    'sound'     : 60,
    'construct' : 22,
    'components': (
        [ ('piece of stone', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 3,), ],
        [ (cmp.Tool_Chisel, 3,), ],
        [ (cmp.Tool_Sharpener, 2,), (cmp.Tool_File, 4,), ],
        ),
    'using'     : (),
    'byproducts': ( ('gravel', 1,), ),
    },),
'metal spearhead':({
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_METAL,10,),),
    'sound'     : 120,
    'construct' : 36,
    'components': (
        [ ('piece of metal', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 3,), ],
        [ (cmp.Tool_Furnace, 2,), (cmp.Tool_Torch, 3,), ],
        [ (cmp.Tool_Sharpener, 3,), (cmp.Tool_File, 5,), ],
        [ (cmp.Tool_Anvil, 2,), ],
        [ (cmp.Tool_Tongs, 1,), ],
        ),
    'using'     : (),
    'byproducts': (),
    },),
'glass spearhead':({
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_GLASS,15,),),
    'sound'     : 60,
    'construct' : 42,
    'components': (
        [ ('piece of glass', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 4,), ],
        [ (cmp.Tool_Chisel, 4,), ],
        ),
    'using'     : (),
    'byproducts': (),
    },),

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
'plastic water filter':({
    # takes 10 minutes to filter 1 liter (1000g or 1KG of water)
    # 1 minute for 100g; 3 seconds for 5g
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_ASSEMBLY,10,), (SKL_PLASTIC,1,),),
    'construct' : 12,
    'components': (
        [ ('plastic bottle', 2,), ],
        [ ('gravel', 0.5*MULT_MASS,), ], # filters the large particles
        [ ('sand', 0.1*MULT_MASS,), ], # filters the particulates
        [ ('powdered charcoal', 0.05*MULT_MASS,), ], # filters the toxins
        [ ('scrap cloth', 1,), ], # membrane
        [ ('rubber band', 1,), ],
        ),
    'tools'     : ( [ (cmp.Tool_Cut, 5,), ], ),
    'using'     : (),
    'byproducts': ( ('scrap plastic', 4,), ),
    },),
'water purification tablet':({ # stretches out the water purification agent
    # water purification agent is tetraglycerine hydroperiodide
    # acts in 5 minutes
    'quantity'  : 20,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_ASSEMBLY,2,),),
    'construct' : 48,
    'components': (
        [ ('water purification agent', 1,), ],
        [ ('pill filler', 20,), ],
        ),
    'tools'     : (),
    'using'     : (),
    'byproducts': (),
    },),
'crystal iodine':({
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_CHEMISTRY,10,),),
    'construct' : 4,
    'overhead'  : 24,
    'info'      : ('ratios',),
    'components': (
        [ ('potassium iodide', 8,), ],
        [ ('purified water', 40,), ],
        [ ('strong acid', 5,), ],
        [ ('bleach', 1,), ('hydrogen peroxide', 1,), ],
        ),
    'tools'     : ( [ (cmp.Tool_Flask, 1,), ], ),
    'using'     : (),
    'byproducts': (),
    },),

    # light sources
'torch':({
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_ASSEMBLY,1,),),
    'construct' : 8,
    'components': (
        [ ('stick of wood', 1,), ('bone', 1,), ('stick of metal', 1,),
          ('metal tube', 1,), ],
        [ ('piece of cloth', 1,), ('seed pod', 1,), ], # pinecone or some other type of seed/plant? What setting are we playing in?
        [ ('oil', 1,), ('resin', 1,), ('grease', 1,), ],
        ),
    'tools'     : (),
    'using'     : (),
    'byproducts': (),
    },),
'torch, large':({
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_ASSEMBLY,1,),),
    'construct' : 12,
    'components': (
        [ ('stick of wood', 1,), ('bone', 1,), ('stick of metal', 1,),
          ('metal tube', 1,), ],
        [ ('chunk of cloth', 1,), ],
        [ ('oil', 2,), ('resin', 2,), ('grease', 2,), ],
        ),
    'tools'     : (),
    'using'     : (),
    'byproducts': (),
    },),
'candle':({
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_ASSEMBLY,1,),),
    'construct' : 4,
    'components': (
        [ ('parcel of wood', 1,), ('parcel of bone', 1,), ('parcel of stone', 1,),
          ('parcel of glass', 1,), ('parcel of metal', 1,),
          ('metal can', 1,), ],
        [ ('string', 1,), ],
        [ ('oil', 1,), ('resin', 1,), ('grease', 1,), ],
        ),
    'tools'     : (),
    'using'     : (),
    'byproducts': (),
    },),
'paper lantern':({
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_ASSEMBLY,1,),),
    'construct' : 8,
    'components': (
        [ ('paper', 2,), ],
        [ ('string', 1,), ],
        [ ('oil', 1,), ('resin', 1,), ('grease', 1,), ],
        ),
    'tools'     : (),
    'using'     : (),
    'byproducts': (),
    },),
'metal lantern':({
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_METAL,8,), (SKL_ASSEMBLY,1,),),
    'sound'     : 60,
    'construct' : 32,
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
    'using'     : (),
    'byproducts': (),
    },),

    # furnaces
'plastic campfire':({ # Note: make campfire object itself have ReactsWithFire func where it creates a "charred plastic campfire" object that cannot be harvested for the plastic and stone
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_ASSEMBLY,1,),),
    'construct' : 6,
    'components': (
        [ ('chunk of plastic', 1,), ],
        [ ('piece of plastic', 3,), ('plastic bottle', 3,), ('stick of plastic', 3,), ],
        [ ('parcel of plastic', 5,), ('plastic cup', 5,), ],
        [ ('parcel of stone', 12,), ('piece of stone', 6,), ],
        [ ('tinder', 1,), ],
        ),
    'tools'     : ( (cmp.Tool_Torch, 1,), (cmp.Tool_FireStarter, 1,), ),
    'using'     : (),
    'byproducts': (),
    },),
'wooden campfire':({ # wooden campfire object could have a function that changes its name to "charred ..." and removes its Harvestable component
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_ASSEMBLY,1,),),
    'construct' : 6,
    'components': (
        [ ('chunk of wood', 1,), ],
        [ ('piece of wood', 3,), ('stick of wood', 3,), ],
        [ ('parcel of wood', 5,), ('twig', 5,), ],
        [ ('parcel of stone', 12,), ('piece of stone', 6,), ],
        [ ('tinder', 1,), ],
        ),
    'tools'     : ( (cmp.Tool_Torch, 1,), (cmp.Tool_FireStarter, 1,), ),
    'using'     : (),
    'byproducts': (),
    },),
'clay furnace':({ # level 2 furnace (level 3 furnaces are metal, and cannot be crafted (?) or require machinery to craft.
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_ASSEMBLY,3,),),
    'construct' : 35,
    'components': (
        [ ('chunk of clay', 15,), ('chunk of stone', 15,), ('slab of clay', 3,), ],
        [ ('chunk of clay', 10,), ('slab of clay', 2,), ],
        [ ('stick of wood', 4,), ],
        ),
    'tools'     : (),
    'using'     : (),
    'byproducts': (),
    },),

    # valves
'plastic valve':({
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_ASSEMBLY,5,), (SKL_PLASTIC,1,),),
    'construct' : 24,
    'durability': 'weakest_link',
    'components': (
        [ ('plastic bottlecap', 2,), ('plastic tube', 1,), ],
        [ ('parcel of tarp', 1,), ('duct tape', 1,), ('parcel of rubber', 1,),
          ('rubber balloon', 1,), ('rubber gasket', 1,), ],
        [ ('rubber band', 1,), ('glue', 1,), ],
        [ ('glue', 1,), ],
        ),
    'tools'     : ( [ (cmp.Tool_Cut, 5,), ], ),
    'using'     : (),
    'byproducts': ( ('scrap plastic', 1,), ),
    },),
'leather valve':({
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_ASSEMBLY,15,), (SKL_LEATHER,5,),),
    'construct' : 36,
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
    'using'     : (),
    'byproducts': ( ('scrap metal', 1,), ),
    },),
'metal valve':({
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_METAL,15,),),
    'construct' : 88,
    'durability': 'weakest_link',
    'components': (
        [ ('metal pipe', 1,), ],
        [ ('metal gasket', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Saw, 5,), ],
        [ (cmp.Tool_Drill, 4,), ],
        [ (cmp.Tool_Sharpener, 4,), (cmp.Tool_File, 5,), ],
        [ (cmp.Tool_Weld, 2,), ],
        ),
    'using'     : (),
    'byproducts': (
        ('piece of metal', 1,),('parcel of metal', 1,),('scrap metal', 1,),
        ),
    },),

    # fluid containers
'plastic tank':({
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_ASSEMBLY,1,), (SKL_PLASTIC,1,),),
    'construct' : 4,
    'durability': 'weakest_link',
    'components': (
        [ ('plastic bottle', 1,), ],
        [ ('rubber valve', 1,), ],
        [ ('glue', 1,), ],
        ),
    'tools'     : ( [ (cmp.Tool_Cut, 5,), ], ),
    'using'     : (),
    'byproducts': (),
    },),

    # motors, dynamos
'motor, small':({ # electric motor, gets power from battery
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_ASSEMBLY,2,), (SKL_PLASTIC,1,),),
    'construct' : 12,
    'components': (
        [ ('plastic cup', 1,), ('parcel of plastic', 1,), ],
        [ ('magnet, weak', 2,), ],
        [ ('metal wire', 2,), ('insulated wire', 2,), ],
        [ ('paperclip', 2,), ('metal wire', 1,), ('insulated wire', 1,), ],
        [ ('glue', 1,),('rubber band', 2,),  ],
        ),
    'tools'     : ( [ (cmp.Tool_Cut, 4,), ], ),
    'using'     : (),
    'byproducts': (),
    },),
'dynamo, small':({ # outputs power when you turn the crank
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_ASSEMBLY,3,), (SKL_PLASTIC,3,), (SKL_WOOD,5,),),
    'construct' : 48,
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
    'using'     : (),
    'byproducts': (),
    },),

    # fluid compressors
'plastic compressor':({
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_ASSEMBLY,5,), (SKL_PLASTIC,2,),),
    'construct' : 12,
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
    'using'     : (),
    'byproducts': (),
    },),
##'wooden air compressor':({ # uses wooden barrel or bucket, standard motor, standard battery, etc.

    # shelters
'shelter':({
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_ASSEMBLY,1,),),
    'sound'     : 30,
    'construct' : 45,
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
    'using'     : (),
    'byproducts': (),
    'recycling' : (),
    },),
'wooden shed frame':({
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_WOOD,10,),),
    'sound'     : 120,
    'construct' : 120,
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
    'using'     : (),
    'byproducts': (),
    'recycling' : (),
    },),
'wooden shed':({
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_WOOD,10,),),
    'sound'     : 120,
    'construct' : 2,
    'components': (
        [ ('wooden shed frame', 1,), ],
        [ ('wooden plank', 60,), ('pole of wood', 32,), ],
        [ ('nail', 96,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 1,), ],
        [ (cmp.Tool_Saw, 3,), ],
        ), 
    'using'     : (),
    'byproducts': (),
    'recycling' : (),
    },),
'metal shed frame':({
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_METAL,5,),),
    'sound'     : 120,
    'construct' : 120,
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
    'using'     : (),
    'byproducts': (),
    'recycling' : (),
    },),
'metal shed':({
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_METAL,5,),),
    'sound'     : 120,
    'construct' : 2,
    'components': (
        [ ('metal shed frame', 1,), ],
        [ ('metal sheet', 4,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Cut, 8,), (cmp.Tool_Saw, 4,), ],
        [ (cmp.Tool_Weld, 2,), ],
        ), 
    'using'     : (),
    'byproducts': (),
    'recycling' : (),
    },),

    # baskets
'wooden basket':({
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_ASSEMBLY,5,),),
    'construct' : 20,
    'components': ( [ ('twig', 16,), ], ), # ('frond', 16,),
    'tools'     : (),
    'using'     : (),
    'byproducts': (),
    'recycling' : (),
    },),

# NOTE: springs are fucking hard to make mate. They might be too precise to be made for the purposes of this crafting system.
##    # spring anvils
##'spring anvil':({ 
##    'quantity'  : 1,
##    'table'     : CRT_STUFF,
##    'category'  : CRC_METAL,
##    'construct' : 24,
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
##    },),
##
##    # springs
##'torsion spring':({ 
##    'quantity'  : 1,
##    'table'     : CRT_STUFF,
##    'category'  : CRC_ASSEMBLY,
##    'construct' : 24,
##    'components': (
##        [ ('metal wire, thick', 1,), ],
##        ),
##    'tools'     : (
##        [ (cmp.Tool_Pliers, 1,), ],
##        [ (cmp.Tool_SpringAnvil, 1,), ],
##        ),
##    'byproducts': (),
##    'recycling' : (),
##    },),

    # traps
'trap, small':({ #maybe baiting is handled separately. You can bait any kind of bait on any trap and the type of bait influences what is attracted to it.
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_ASSEMBLY,1,),),
    'construct' : 3,
    'components': (
        [ ('wooden basket', 1,), ],
        [ ('twig', 1,), ],
##        [ ('corpse of bug', 1,), ],
        ),
    'tools'     : (), 
    'using'     : (),
    'byproducts': (),
    'recycling' : (),
    },),
'trap, net':({
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_ASSEMBLY,6,),),
    'construct' : 5,
    'components': (
        [ ('net', 1,), ],
        [ ('rope', 40,), ],
##        [ ('parcel of flesh', 1,), ],
        ),
    'tools'     : (), 
    'using'     : (),
    'byproducts': (),
    'recycling' : (),
    },),
'trap, pit':({ # large pit trap must be built inside of a pit
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_ASSEMBLY,8,),),
    'construct' : 30,
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
    'using'     : (),
    'byproducts': (),
    'recycling' : (),
    },),

    # medicine
'bandage':({
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_ASSEMBLY,5,), (SKL_SEWING,1,),),
    'construct' : 3,
    'components': (
        [ ('parcel of cloth', 1,), ],
        [ ('parcel of tarp', 1,), ('rubber balloon', 1,), ],
        [ ('glue', 1,), ],
        ),
    'tools'     : ( [ (cmp.Tool_Cut, 3,), ], ),
    'using'     : (),
    'byproducts': (),
    },),

    # string -> cordage -> rope -> cable
    # chains
'string':({ # thin cordage, supports 1kg (a single thread is not worth being an item, and it would support like 10g)
    'quantity'  : 3,
    'table'     : CRT_RAWMATS,
    'skills'    : ((SKL_ASSEMBLY,3,),),
    'construct' : 24, # in reality takes several hours from start-finish.. But, this would make string-making from sinews pretty worthless.
    'mass'      : 'fixed', # mass irrespective of components
    'components': (
        [ ('sinew', 1,), ], #technically tendons should be dried.
        ),
    'tools'     : (
        [ (cmp.Tool_Cut, 6,), ],
        [ (cmp.Tool_Hammer, 3,), ],
        ),
    'using'     : (),
    'byproducts': ( ('animal fat', 1,), ),
    },),
'cordage':({ # thin rope, supports 10kg
    'quantity'  : 1,
    'table'     : CRT_RAWMATS,
    'skills'    : ((SKL_ASSEMBLY,3,),),
    'construct' : 18,
    'mass'      : 'fixed', # mass irrespective of components
    'components': (
        [ ('fibrous leaf', 3,), ('twig', 6,), ('string', 9,), ],
        ),
    'tools'     : (),
    'using'     : (),
    'byproducts': (),
    },),
'rope':({ # rope, supports 150kg
    'quantity'  : 1,
    'table'     : CRT_RAWMATS,
    'skills'    : ((SKL_ASSEMBLY,4,),),
    'construct' : 24,
    'mass'      : 'fixed', # mass irrespective of components
    'components': (
        [ ('cordage', 9,), ],
        ),
    'tools'     : (),
    'using'     : (),
    'byproducts': (),
    },),
'cable':({ # thick rope, supports 500kg
    'quantity'  : 1,
    'table'     : CRT_RAWMATS,
    'skills'    : ((SKL_ASSEMBLY,5,),),
    'construct' : 24,
    'components': ( [ ('rope', 3,), ], ),
    'tools'     : (),
    'using'     : (),
    'byproducts': (),
    },),
'chain link, small':({
    'quantity'  : 16,
    'table'     : CRT_RAWMATS,
    'skills'    : ((SKL_METAL,10,),),
    'sound'     : 120,
    'construct' : 5,
    'celsius'   : 500,
    'durability': 'fixed',
    'mass'      : 'fixed',
    'components': ( [ ('parcel of metal', 1,), ], ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 3,), ],
        [ (cmp.Tool_Tongs, 2,), ],
        ),
    'using'     : (
        [ (cmp.Tool_Anvil, 3,), ],
        [ (cmp.Tool_Crucible, 2,), ],
        [ (cmp.Mold_ChainLinkLight, 1,), ],
        [ (cmp.Tool_Furnace, 1,), ],
        ),
    'byproducts': (),
    },),
'chain, small':({ # light 5mm chain, supports 200kg
    'quantity'  : 1,
    'table'     : CRT_RAWMATS,
    'skills'    : ((SKL_METAL,8,),),
    'sound'     : 120,
    'construct' : 96,
    'celsius'   : 300,
    'durability': 'weakest_link',
    'mass'      : 'fixed',
    'components': ( [ ('chain link, small', 200,), ], ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 4,), ],
        [ (cmp.Tool_Weld, 3,), ],
        [ (cmp.Tool_Pliers, 2,), (cmp.Tool_Anvil, 3,), ],
        [ (cmp.Tool_Tongs, 1,), ],
        ),
    'using'     : (),
    'byproducts': (),
    },),
'chain link':({
    'quantity'  : 8,
    'table'     : CRT_RAWMATS,
    'skills'    : ((SKL_METAL,12,),),
    'sound'     : 120,
    'construct' : 6,
    'celsius'   : 500,
    'durability': 'fixed',
    'mass'      : 'fixed',
    'components': ( [ ('parcel of metal', 1,), ], ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 2,), ],
        [ (cmp.Tool_Tongs, 2,), ],
        ),
    'using'     : (
        [ (cmp.Tool_Anvil, 3,), ],
        [ (cmp.Tool_Furnace, 2,), ],
        [ (cmp.Tool_Crucible, 2,), ],
        [ (cmp.Mold_ChainLink, 1,), ],
        ),
    'byproducts': (),
    },),
'chain':({ # standard 10mm chain, supports 1000kg
    'quantity'  : 1,
    'table'     : CRT_RAWMATS,
    'skills'    : ((SKL_METAL,10,),),
    'sound'     : 120,
    'construct' : 72,
    'celsius'   : 300,
    'durability': 'weakest_link',
    'mass'      : 'fixed',
    'components': ( [ ('chain link', 100,), ], ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 3,), ],
        [ (cmp.Tool_Furnace, 2,), (cmp.Tool_Weld, 2,), ],
        [ (cmp.Tool_Pliers, 2,), (cmp.Tool_Anvil, 3,), ],
        [ (cmp.Tool_Tongs, 1,), ],
        ),
    'using'     : (),
    'byproducts': (),
    },),
'chain link, large':({
    'quantity'  : 2,
    'table'     : CRT_RAWMATS,
    'skills'    : ((SKL_METAL,15,),),
    'sound'     : 120,
    'construct' : 8,
    'celsius'   : 500,
    'durability': 'fixed',
    'mass'      : 'fixed',
    'components': ( [ ('parcel of metal', 1,), ], ),
    'tools'     : ( [ (cmp.Tool_Tongs, 2,), ], ),
    'using'     : (
        [ (cmp.Tool_Furnace, 3,), ],
        [ (cmp.Tool_Hammer, 2,), ],
        [ (cmp.Tool_Crucible, 2,), ],
        [ (cmp.Tool_Anvil, 2,), ],
        [ (cmp.Mold_ChainLinkHeavy, 1,), ],
        ),
    'byproducts': (),
    },),
'chain, large':({ # heavy duty 20mm chain, supports 5000kg
    'quantity'  : 1,
    'table'     : CRT_RAWMATS,
    'skills'    : ((SKL_METAL,12,),),
    'sound'     : 120,
    'construct' : 48,
    'celsius'   : 300,
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
    'using'     : (),
    'byproducts': (),
    },),

    # fishing
'fishing hook':({
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_ASSEMBLY,1,),),
    'construct' : 5,
    'components': (
        [ ('fibrous leaf', 1,), ],
        ),
    'tools'     : ( (cmp.Tool_Cut, 5,), ),
    'using'     : (),
    'byproducts': (),
    },),
'plastic fishing hook':({
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_PLASTIC,5,),),
    'construct' : 4,
    'components': (
        [ ('scrap plastic', 1,), ('shard of plastic', 1,), ],
        ),
    'tools'     : ( (cmp.Tool_Cut, 4,), ),
    'using'     : (),
    'byproducts': (),
    },),
'wooden fishing hook':({
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_WOOD,15,),),
    'construct' : 8,
    'components': (
        [ ('scrap wood', 1,), ('shard of wood', 1,), ],
        ),
    'tools'     : ( (cmp.Tool_Cut, 5,), ),
    'using'     : (),
    'byproducts': (),
    },),
'stone fishing hook':({
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_STONE,35,),),
    'construct' : 14,
    'components': (
        [ ('shard of stone', 1,), ],
        ),
    'tools'     : (
        (cmp.Tool_Chisel, 3,),
        (cmp.Tool_Drill, 3,),
        (cmp.Tool_Hammer, 2,),
        ),
    'using'     : (),
    'byproducts': (),
    },),
'bone fishing hook':({
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_BONE,25,),),
    'construct' : 10,
    'components': (
        [ ('scrap bone', 1,), ('shard of bone', 1,), ],
        ),
    'tools'     : (
        (cmp.Tool_Chisel, 2,),
        (cmp.Tool_Drill, 2,),
        (cmp.Tool_Hammer, 2,),
        ),
    'using'     : (),
    'byproducts': (),
    },),
'metal fishing hook':({
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_METAL,10,),),
    'construct' : 12,
    'components': (
        [ ('scrap metal', 1,), ('paperclip', 1,), ('pop tab', 1,),
          ('metal needle', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 4,), ],
        [ (cmp.Tool_Pliers, 2,), (cmp.Tool_Anvil, 1,), ],
        ),
    'byproducts': (),
    },),
'fishing rod':({ # should fishing rod and baited fishing rod be different objects? And same with traps and baited traps? Or is it fine to just abstract baiting away?
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_ASSEMBLY,5,),),
    'durability': 'sum',
    'construct' : 6,
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
    'using'     : (),
    'byproducts': (),
    },),

    # magnets
'magnet, weak':({ # cannot make a strong magnet, it's necessary to have neodymium which is too pure to craft
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_ASSEMBLY,1,),),
    'construct' : 10,
    'components': (
        [ ('parcel of metal', 1,), ],
        [ ('magnet, weak', 1,), ('magnet, strong', 1,), ],
        ),
    'tools'     : (),
    'using'     : (),
    'byproducts': (),
    },),
'electromagnet':({ 
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_ASSEMBLY,8,),), # coil the wire around the metal, connect to battery (?)
    'construct' : 15,
    'components': (
        [ ('parcel of metal', 1,), ],
        [ ('metal wire', 1,), ],
        [ ('battery, small', 1,), ],
        ),
    'tools'     : ( [ (cmp.Tool_Pliers, 1,), ], ),
    'using'     : (),
    'byproducts': (),
    },),






    #--------------------------#
    #         Headgear         #
    #--------------------------#

    # cloth
'padded coif':({
    'quantity'  : 1,
    'table'     : CRT_ARMOR,
    'skills'    : ((SKL_SEWING,20,),),
    'construct' : 144,
    'components': (
        [ ('chunk of cloth', 1,), ],
        [ ('piece of cloth', 2,), ],
        [ ('string', 24,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Cut, 6,), ],
        [ (cmp.Tool_Sew, 2,), ],
        ),
    'using'     : (),
    'byproducts': (),
    },),
'padded coif, heavy':({
    'quantity'  : 1,
    'table'     : CRT_ARMOR,
    'skills'    : ((SKL_SEWING,25,),),
    'construct' : 240,
    'components': (
        [ ('chunk of cloth', 3,), ],
        [ ('string', 32,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Cut, 6,), ],
        [ (cmp.Tool_Sew, 2,), ],
        ),
    'using'     : (),
    'byproducts': (),
    },),

    # plastic
'respirator':({
    'quantity'  : 1,
    'table'     : CRT_ARMOR,
    'skills'    : ((SKL_ASSEMBLY,15,),),
    'construct' : 48,
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
    'using'     : (),
    'byproducts': (),
    },),

    # metal
'metal respirator':({
    'quantity'  : 1,
    'table'     : CRT_ARMOR,
    'skills'    : ((SKL_ASSEMBLY,15,), (SKL_METAL,10,),),
    'construct' : 96,
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
    'using'     : (),
    'byproducts': (),
    },),






    #--------------------------#
    #          Armor           #
    #--------------------------#



    # cloth
't-shirt':({
    'quantity'  : 1,
    'table'     : CRT_ARMOR,
    'skills'    : ((SKL_SEWING,5,),),
    'construct' : 8,
    'components': (
        [ ('piece of cloth', 1,), ],
        [ ('string', 8,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Cut, 4,), ],
        [ (cmp.Tool_Sew, 1,), ],
        ),
    'using'     : (),
    'byproducts': ( ('parcel of cloth', 1,), ),
    },),
'hoody':({
    'quantity'  : 1,
    'table'     : CRT_ARMOR,
    'skills'    : ((SKL_SEWING,10,),),
    'construct' : 24,
    'components': (
        [ ('piece of cloth', 4,), ],
        [ ('string', 24,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Cut, 4,), ],
        [ (cmp.Tool_Sew, 1,), ],
        ),
    'using'     : (),
    'byproducts': ( ('parcel of cloth', 2,), ),
    },),
'cloth vest':({
    'quantity'  : 1,
    'table'     : CRT_ARMOR,
    'skills'    : ((SKL_SEWING,10,),),
    'construct' : 72,
    'components': (
        [ ('piece of cloth', 3,), ],
        [ ('string', 16,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Cut, 5,), ],
        [ (cmp.Tool_Sew, 1,), ],
        ),
    'using'     : (),
    'byproducts': (),
    },),
'cloth vest, heavy':({
    'quantity'  : 1,
    'table'     : CRT_ARMOR,
    'skills'    : ((SKL_SEWING,15,),),
    'construct' : 144,
    'components': (
        [ ('chunk of cloth', 4,), ],
        [ ('string', 64,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Cut, 6,), ],
        [ (cmp.Tool_Sew, 1,), ],
        ),
    'using'     : (),
    'byproducts': (),
    },),
'padded jacket':({
    'quantity'  : 1,
    'table'     : CRT_ARMOR,
    'skills'    : ((SKL_SEWING,20,),),
    'construct' : 288,
    'components': (
        [ ('chunk of cloth', 5,), ], # ('t-shirt', 25,),
        [ ('string', 64,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Cut, 6,), ],
        [ (cmp.Tool_Sew, 2,), ],
        ),
    'using'     : (),
    'byproducts': (),
    },),
'padded jack':({
    'quantity'  : 1,
    'table'     : CRT_ARMOR,
    'skills'    : ((SKL_SEWING,25,),),
    'construct' : 432,
    'components': (
        [ ('chunk of cloth', 10,), ], #  ('t-shirt', 50,),
        [ ('string', 128,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Cut, 6,), ],
        [ (cmp.Tool_Sew, 2,), ],
        ),
    'using'     : (),
    'byproducts': (),
    },),
'gambeson':({
    'quantity'  : 1,
    'table'     : CRT_ARMOR,
    'skills'    : ((SKL_SEWING,30,),),
    'construct' : 864, #57600
    'components': (
        [ ('chunk of cloth', 16,), ], # ('t-shirt', 80,),
        [ ('string', 256,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Cut, 6,), ],
        [ (cmp.Tool_Sew, 2,), ],
        ),
    'using'     : (),
    'byproducts': (),
    },),
'arming doublet':({
    'quantity'  : 1,
    'table'     : CRT_ARMOR,
    'skills'    : ((SKL_LEATHER,10,), (SKL_SEWING,5,), (SKL_ARMORSMITH,5,),),
    'construct' : 80,
    'components': (
        [ ('padded jack', 1,), ],
        [ ('scrap leather', 16,), ],
        [ ('string', 16,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Cut, 6,), ],
        [ (cmp.Tool_Sew, 2,), ],
        ),
    'using'     : (),
    'byproducts': (),
    },),

    # leather
'leather jacket':({
    'quantity'  : 1,
    'table'     : CRT_ARMOR,
    'skills'    : ((SKL_LEATHER,15,),),
    'construct' : 144,
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
    'using'     : (),
    'byproducts': ( ('parcel of leather', 2,), ),
    },),

    # boiled leather
'boiled leather gear':({
    'quantity'  : 1,
    'table'     : CRT_ARMOR,
    'skills'    : ((SKL_LEATHER,15,), (SKL_ARMORSMITH,10,),),
    'construct' : 864,
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
    'using'     : (),
    'byproducts': ( ('parcel of boiled leather', 2,), ),
    },),

    # plastic
'disposable PPE':({
    'quantity'  : 1,
    'table'     : CRT_ARMOR,
    'skills'    : ((SKL_ASSEMBLY,10,),),
    'construct' : 16,
    'components': (
        [ ('tarp', 6,), ],
        ),
    'tools'     : ( [ (cmp.Tool_Cut, 3,), ], ),
    'using'     : (),
    'byproducts': (),
    },),
'plastic gear':({ # lamellar armor
    'quantity'  : 1,
    'table'     : CRT_ARMOR,
    'skills'    : ((SKL_ARMORSMITH,20,), (SKL_PLASTIC,15,),),
    'construct' : 576,
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
    'using'     : (),
    'byproducts': (
        ('parcel of plastic', 5,), ('scrap plastic', 5,),
        ('parcel of cloth', 2,),
        ),
    },),

    # wood
'wooden gear':({
    'quantity'  : 1,
    'table'     : CRT_ARMOR,
    'skills'    : ((SKL_ARMORSMITH,25,), (SKL_WOOD,20,),),
    'construct' : 864,
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
    'using'     : (),
    'byproducts': ( ('scrap wood', 5,), ),
    },),

    # bone
'bone gear':({
    'quantity'  : 1,
    'table'     : CRT_ARMOR,
    'skills'    : ((SKL_ARMORSMITH,30,), (SKL_BONE,40,),),
    'construct' : 1008,
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
    'using'     : (),
    'byproducts': ( ('scrap bone', 5,), ),
    },),
'bone armor':({
    'quantity'  : 1,
    'table'     : CRT_ARMOR,
    'skills'    : ((SKL_ARMORSMITH,20,), (SKL_BONE,20,),),
    'construct' : 576,
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
    'using'     : (),
    'byproducts': ( ('scrap bone', 5,), ),
    },),

    # metal
'pop tab mail vest':({
    'quantity'  : 1,
    'table'     : CRT_ARMOR,
    'skills'    : ((SKL_ARMORSMITH,10,),),
    'construct' : 88,
    'components': (
        [ ('pop tab mail ring', 768,), ],
        [ ('padded jack', 1,), ],
        [ ('piece of leather', 1,), ],
        ),
    'tools'     : (),
    'using'     : (),
    'byproducts': (),
    },),
'pop tab mail shirt':({
    'quantity'  : 1,
    'table'     : CRT_ARMOR,
    'skills'    : ((SKL_ARMORSMITH,10,),),
    'construct' : 72,
    'components': (
        [ ('pop tab mail vest', 1,), ],
        [ ('pop tab mail ring', 512,), ],
        [ ('piece of leather', 1,), ],
        ),
    'tools'     : (),
    'using'     : (),
    'byproducts': (),
    },),
'metal mail vest':({
    'quantity'  : 1,
    'table'     : CRT_ARMOR,
    'skills'    : ((SKL_ARMORSMITH,25,),),
    'construct' : 144,
    'components': (
        [ ('mail ring, riveted', 320,), ('mail ring, welded', 320,), ],
        [ ('padded jack', 1,), ],
        [ ('piece of leather', 1,), ],
        ),
    'tools'     : (),
    'using'     : (),
    'byproducts': (),
    },),
'metal mail shirt':({
    'quantity'  : 1,
    'table'     : CRT_ARMOR,
    'skills'    : ((SKL_ARMORSMITH,25,),),
    'construct' : 120,
    'components': (
        [ ('metal mail vest', 1,), ],
        [ ('mail ring, riveted', 196,), ('mail ring, welded', 196,), ],
        [ ('piece of leather', 1,), ],
        ),
    'tools'     : (),
    'using'     : (),
    'byproducts': (),
    },),
'metal cap':({
    'quantity'  : 1,
    'table'     : CRT_ARMOR,
    'skills'    : ((SKL_ARMORSMITH,10,), (SKL_METAL,15,),),
    'sound'     : 120,
    'construct' : 80,
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
    'using'     : (),
    'byproducts': (),
    },),
'metal mask':({
    'quantity'  : 1,
    'table'     : CRT_ARMOR,
    'skills'    : ((SKL_ARMORSMITH,15,), (SKL_METAL,25,),),
    'sound'     : 120,
    'construct' : 240,
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
    'using'     : (),
    'byproducts': (),
    },),





    #--------------------------#
    #          Ammo            #
    #--------------------------#


    # arrows
'plastic primitive arrow':({ # arrow name and stats determined by the material type of the arrowhead, not the shaft. But, since the shaft is the first component, whatever material the shaft is will be the material type of the arrow itself, regardless of the name.
    'quantity'  : 1,
    'table'     : CRT_AMMO,
    'skills'    : ((SKL_ASSEMBLY,1,),),
    'construct' : 5,
    'components': (
        [ ('twig', 1,), ('plastic tube', 1,), ],
        [ ('plastic arrowhead', 1,), ],
        [ ('string', 1,), ('glue', 1,), ('rubber band', 1,),
          ('sinew', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Cut, 3,), ],
        ),
    'using'     : (),
    'byproducts': (),
    },),
'wooden primitive arrow':({
    'quantity'  : 1,
    'table'     : CRT_AMMO,
    'skills'    : ((SKL_ASSEMBLY,1,),),
    'construct' : 5,
    'components': (
        [ ('twig', 1,), ('plastic tube', 1,), ],
        [ ('wooden arrowhead', 1,), ],
        [ ('string', 1,), ('glue', 1,), ('rubber band', 1,),
          ('sinew', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Cut, 4,), ],
        ),
    'using'     : (),
    'byproducts': (),
    },),
'bone primitive arrow':({
    'quantity'  : 1,
    'table'     : CRT_AMMO,
    'skills'    : ((SKL_ASSEMBLY,1,),),
    'construct' : 5,
    'components': (
        [ ('twig', 1,), ('plastic tube', 1,), ],
        [ ('bone arrowhead', 1,), ],
        [ ('string', 1,), ('glue', 1,), ('rubber band', 1,),
          ('sinew', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Cut, 4,), ],
        ),
    'using'     : (),
    'byproducts': (),
    },),
'stone primitive arrow':({
    'quantity'  : 1,
    'table'     : CRT_AMMO,
    'skills'    : ((SKL_ASSEMBLY,1,),),
    'construct' : 5,
    'components': (
        [ ('twig', 1,), ('plastic tube', 1,), ],
        [ ('stone arrowhead', 1,), ],
        [ ('string', 1,), ('glue', 1,), ('sinew', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Cut, 4,), ],
        ),
    'using'     : (),
    'byproducts': (),
    },),
'metal primitive arrow':({
    'quantity'  : 1,
    'table'     : CRT_AMMO,
    'skills'    : ((SKL_ASSEMBLY,2,),),
    'construct' : 5,
    'components': (
        [ ('twig', 1,), ('plastic tube', 1,), ],
        [ ('metal arrowhead', 1,), ],
        [ ('string', 1,), ('sinew', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Cut, 4,), ],
        ),
    'using'     : (),
    'byproducts': (),
    },),
'glass primitive arrow':({
    'quantity'  : 1,
    'table'     : CRT_AMMO,
    'skills'    : ((SKL_ASSEMBLY,3,),),
    'construct' : 5,
    'components': (
        [ ('twig', 1,), ('plastic tube', 1,), ],
        [ ('glass arrowhead', 1,), ],
        [ ('string', 1,), ('glue', 1,), ('sinew', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Cut, 4,), ],
        ),
    'using'     : (),
    'byproducts': (),
    },),
'plastic arrow':({
    'quantity'  : 1,
    'table'     : CRT_AMMO,
    'skills'    : ((SKL_FLETCHER,5,), (SKL_PLASTIC,1,),),
    'construct' : 10,
    'components': (
        [ ('twig', 1,), ('plastic tube', 1,), ],
        [ ('plastic arrowhead', 1,), ],
        [ ('scrap plastic', 1,), ('feather', 1,), ],
        [ ('string', 1,), ('sinew', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Cut, 4,), ],
        ),
    'using'     : (),
    'byproducts': (),
    },),
'wooden arrow':({
    'quantity'  : 1,
    'table'     : CRT_AMMO,
    'skills'    : ((SKL_FLETCHER,8,), (SKL_WOOD,3,),),
    'construct' : 15,
    'components': (
        [ ('twig', 1,), ],
        [ ('wooden arrowhead', 1,), ],
        [ ('scrap plastic', 1,), ('feather', 1,), ],
        [ ('string', 1,), ('sinew', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Cut, 4,), ],
        ),
    'using'     : (),
    'byproducts': (),
    },),
'bone arrow':({
    'quantity'  : 1,
    'table'     : CRT_AMMO,
    'skills'    : ((SKL_FLETCHER,10,), (SKL_BONE,5,),),
    'construct' : 15,
    'components': (
        [ ('twig', 1,), ],
        [ ('bone arrowhead', 1,), ],
        [ ('scrap plastic', 1,), ('feather', 1,), ],
        [ ('string', 1,), ('sinew', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Cut, 4,), ],
        ),
    'using'     : (),
    'byproducts': (),
    },),
'stone arrow':({
    'quantity'  : 1,
    'table'     : CRT_AMMO,
    'skills'    : ((SKL_FLETCHER,10,), (SKL_STONE,5,),),
    'construct' : 15,
    'components': (
        [ ('twig', 1,), ],
        [ ('stone arrowhead', 1,), ],
        [ ('scrap plastic', 1,), ('feather', 1,), ],
        [ ('string', 1,), ('sinew', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Cut, 4,), ],
        ),
    'using'     : (),
    'byproducts': (),
    },),
'metal arrow':({
    'quantity'  : 1,
    'table'     : CRT_AMMO,
    'skills'    : ((SKL_FLETCHER,10,), (SKL_METAL,5,),),
    'construct' : 30,
    'components': (
        [ ('twig', 1,), ],
        [ ('metal arrowhead', 1,), ],
        [ ('scrap plastic', 1,), ('feather', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Cut, 4,), ],
        [ (cmp.Tool_Hammer, 2,), ],
        ),
    'using'     : (),
    'byproducts': (),
    },),
'glass arrow':({
    'quantity'  : 1,
    'table'     : CRT_AMMO,
    'skills'    : ((SKL_FLETCHER,10,), (SKL_GLASS,3,),),
    'construct' : 20,
    'components': (
        [ ('twig', 1,), ],
        [ ('glass arrowhead', 1,), ],
        [ ('scrap plastic', 1,), ('feather', 1,), ],
        [ ('string', 1,), ('sinew', 1,), ],
        ),
    'tools'     : ( [ (cmp.Tool_Cut, 4,), ], ),
    'using'     : (),
    'byproducts': (),
    },),

    # bullets
'metal bullet, small':({ 
    'quantity'  : 2,
    'table'     : CRT_AMMO,
    'skills'    : ((SKL_METAL,10,),),
    'construct' : 10,
    'components': ( [ ('parcel of metal', 1,), ], ),
    'tools'     : ( [ (cmp.Tool_Tongs, 2,), ], ),
    'using'     : (
        [ (cmp.Mold_BulletSmall, 1,), ], # should this be a tool or something else?
        [ (cmp.Tool_Furnace, 3,), ],
        [ (cmp.Tool_Crucible, 2,), ],
        ),
    'byproducts': (),
    },),
'metal bullet':({
    'quantity'  : 1,
    'table'     : CRT_AMMO,
    'skills'    : ((SKL_METAL,8,),),
    'construct' : 10,
    'components': ( [ ('parcel of metal', 1,), ], ),
    'tools'     : ( [ (cmp.Tool_Tongs, 2,), ], ),
    'using'     : (
        [ (cmp.Mold_Bullet, 1,), ],
        [ (cmp.Tool_Furnace, 3,), ],
        [ (cmp.Tool_Crucible, 2,), ],
        ),
    'byproducts': (),
    },),
'metal bullet, large':({
    'quantity'  : 1,
    'table'     : CRT_AMMO,
    'skills'    : ((SKL_METAL,6,),),
    'construct' : 14,
    'components': ( [ ('parcel of metal', 2,), ], ),
    'tools'     : (
        [ (cmp.Mold_BulletLarge, 1,), ],
        [ (cmp.Tool_Furnace, 3,), ],
        [ (cmp.Tool_Crucible, 2,), ],
        [ (cmp.Tool_Tongs, 2,), ],
        ),
    'using'     : (),
    'byproducts': (),
    },),
'Minni ball':({
    'quantity'  : 1,
    'table'     : CRT_AMMO,
    'skills'    : ((SKL_METAL,16,),),
    'construct' : 10,
    'components': ( [ ('parcel of metal', 1,), ], ),
    'tools'     : ( [ (cmp.Tool_Tongs, 2,), ], ),
    'using'     : (
        [ (cmp.Mold_MinniBall, 1,), ],
        [ (cmp.Tool_Furnace, 3,), ],
        [ (cmp.Tool_Crucible, 2,), ],
        ),
    'byproducts': (),
    },),
'paper cartridge':({
    'quantity'  : 1,
    'table'     : CRT_AMMO,
    'skills'    : ((SKL_ASSEMBLY,6,),),
    'construct' : 8,
    'components': (
        [ ('metal bullet', 1,), ('Minni ball', 1,), ],
        [ ('paper', 1,), ],
        [ ('gunpowder', 1,), ],
        ),
    'tools'     : (),
    'using'     : (),
    'byproducts': (),
    },),





    #--------------------------#
    #          Tools           #
    #--------------------------#


    # anvils
'stone anvil':({ # anvil level 2
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_STONE,15,),),
    'construct' : 72,
    'components': (
        [ ('slab of stone', 1,), ('cuboid of stone', 1,), ('boulder', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Chisel, 3,), ],
        [ (cmp.Tool_Hammer, 2,), ],
        ),
    'using'     : (),
    'byproducts': ( ('slab of stone', 1,), ('chunk of stone', 1,), ),
    },),
'metal anvil, small':({ # anvil level 3
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_METAL,25,),),
    'sound'     : 120,
    'construct' : 576,
    'components': (
        [ ('parcel of metal', 100,), ('piece of metal', 20,), ],
        ),
    'tools'     : ( [ (cmp.Tool_Tongs, 3,), ], ),
    'using'     : (
        [ (cmp.Tool_Furnace, 3,), ],
        ),
    'byproducts': (),
    },),
'metal anvil':({ # anvil level 4
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_METAL,35,),),
    'sound'     : 120,
    'construct' : 864,
    'components': (
        [ ('parcel of metal', 500,), ('piece of metal', 100,), ],
        ),
    'tools'     : ( [ (cmp.Tool_Tongs, 3,), ], ),
    'using'     : (
        [ (cmp.Tool_Furnace, 4,), ],
        ),
    'byproducts': (),
    },),
'metal anvil, large':({ # anvil level 5
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_METAL,45,),),
    'sound'     : 120,
    'construct' : 1728,
    'components': (
        [ ('parcel of metal', 2000,), ('piece of metal', 400,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Furnace, 4,), ],
        [ (cmp.Tool_Crucible, 3,), ],
        [ (cmp.Tool_Tongs, 3,), ],
        [ (cmp.Mold_AnvilLarge, 1,), ],
        ),
    'using'     : (),
    'byproducts': (),
    },),

    # axes - plastic or wooden handle with a head of MATERIAL. Chopping implement with secondary chiseling, hammering ability. Distinct from HATCHETS, which are composed of entirely one material.
'plastic axe':({
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_PLASTIC,5,),),
    'sound'     : 60,
    'construct' : 24,
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
    'using'     : (),
    'byproducts': ( ('scrap plastic', 1), ),
    },),
'wooden axe':({
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_WOOD,5,),),
    'sound'     : 60,
    'construct' : 48,
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
    'using'     : (),
    'byproducts': ( ('parcel of wood', 1), ('scrap wood', 1), ),
    },),
'stone axe':({
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_STONE,5,),),
    'sound'     : 60,
    'construct' : 96,
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
    'using'     : (),
    'byproducts': ( ('parcel of stone', 2), ('gravel', 1), ),
    },),
'bone axe':({
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_BONE,5,),),
    'sound'     : 60,
    'construct' : 72,
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
    'using'     : (),
    'byproducts': ( ('parcel of bone', 1), ('scrap bone', 1), ),
    },),
'metal axe':({
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_METAL,5,),),
    'sound'     : 120,
    'construct' : 120,
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
    'using'     : (),
    'byproducts': ( ('parcel of wood', 2), ),
    },),

    # chisels
'plastic chisel':({ # chisel level 1
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_PLASTIC,2,),),
    'sound'     : 60,
    'construct' : 6,
    'components': (
        [ ('parcel of plastic', 1,), ('shard of plastic', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 1,), ],
        [ (cmp.Tool_Chisel, 1,), (cmp.Tool_Anvil, 1,), ],
        [ (cmp.Tool_Grinder, 1,), (cmp.Tool_File, 1,), ],
        ),
    'using'     : (),
    'byproducts': (),
    },),
'wooden chisel':({ # chisel level 2
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_WOOD,2,),),
    'sound'     : 60,
    'construct' : 10,
    'components': (
        [ ('parcel of wood', 1,), ('shard of wood', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 2,), ],
        [ (cmp.Tool_Chisel, 2,), (cmp.Tool_Anvil, 1,), ],
        [ (cmp.Tool_Grinder, 1,), (cmp.Tool_File, 2,), ],
        ),
    'using'     : (),
    'byproducts': ( ('scrap wood', 1), ),
    },),
'stone chisel':({ # chisel level 3
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_STONE,5,),),
    'sound'     : 60,
    'construct' : 18,
    'components': (
        [ ('parcel of stone', 1,), ('shard of stone', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 3,), ],
        [ (cmp.Tool_Chisel, 3,), (cmp.Tool_Anvil, 2,), ],
        [ (cmp.Tool_Grinder, 3,), (cmp.Tool_File, 4,), ],
        ),
    'using'     : (),
    'byproducts': ( ('gravel', 1), ),
    },),
'bone chisel':({ # chisel level 2
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_BONE,5,),),
    'sound'     : 60,
    'construct' : 12,
    'components': (
        [ ('parcel of bone', 1,), ('shard of bone', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 2,), ],
        [ (cmp.Tool_Chisel, 2,), (cmp.Tool_Anvil, 2,), ],
        [ (cmp.Tool_Grinder, 2,), (cmp.Tool_File, 3,), ],
        ),
    'using'     : (),
    'byproducts': ( ('scrap bone', 1), ),
    },),
'metal chisel':({ # chisel level 4
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_METAL,4,),),
    'sound'     : 120,
    'construct' : 24,
    'components': (
        [ ('parcel of metal', 1,), ('shard of metal', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_File, 5,), (cmp.Tool_Grinder, 4,), ],
        [ (cmp.Tool_Hammer, 3,), ],
        [ (cmp.Tool_Sharpener, 3,), ],
        [ (cmp.Tool_Furnace, 2,), (cmp.Tool_Torch, 3,), ],
        [ (cmp.Tool_Anvil, 3,), ],
        [ (cmp.Tool_Tongs, 1,), ],
        ),
    'using'     : (),
    'byproducts': ( ('scrap metal', 1), ),
    },),

    # cutting implements
'scissors':({ # cut level 7
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_METAL,10,),),
    'sound'     : 120,
    'construct' : 96,
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
    'using'     : (),
    'byproducts': (),
    },),
'wire cutters':({ # cut level 8
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_METAL,30,),),
    'sound'     : 120,
    'construct' : 120,
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
    'using'     : (),
    'byproducts': (),
    },),
'hedge trimmers':({ # cut level 9
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_METAL,40,),),
    'sound'     : 120,
    'construct' : 96,
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
    'using'     : (),
    'byproducts': (),
    },),

    # drilling implements
'hole puncher':({ # drill level 1
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_METAL,10,),),
    'sound'     : 120,
    'construct' : 96,
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
    'using'     : (),
    'byproducts': (),
    },),
##'hand drill':({ # drill level 2
##    'quantity'  : 1,
##    'table'     : CRT_TOOLS,
##    'category'  : CRC_METAL,
##    'sound'     : 120,
##    'construct' : 144,
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
##    },),
'electric drill':({ # drill level 2?
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_ASSEMBLY,15,),),
    'sound'     : 120,
    'construct' : 24,
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
    'using'     : (),
    'byproducts': (),
    },),

    # hammers
'plastic hammer':({ # hammer level 3
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_PLASTIC,5,),),
    'sound'     : 60,
    'construct' : 12,
    'components': (
        [ ('piece of plastic', 1,), ],
        [ ('stick of plastic', 1,), ('stick of wood', 1,), ],
        [ ('cordage', 2,), ('glue', 2,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 1,), ],
        [ (cmp.Tool_Chisel, 1,), ],
        ),
    'using'     : (),
    'byproducts': ( ('scrap plastic', 1), ),
    },),
'wooden hammer':({ # hammer level 3
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_WOOD,5,),),
    'sound'     : 60,
    'construct' : 18,
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
    'using'     : (),
    'byproducts': ( ('parcel of wood', 1,), ('scrap wood', 1,), ),
    },),
'stone hammer':({ # hammer level 3
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_STONE,5,),),
    'sound'     : 60,
    'construct' : 24,
    'components': (
        [ ('piece of stone', 1,), ],
        [ ('stick of plastic', 1,), ('stick of wood', 1,), ],
        [ ('cordage', 2,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 2,), ],
        [ (cmp.Tool_Chisel, 2,), ],
        ),
    'using'     : (),
    'byproducts': ( ('parcel of stone', 1,), ('gravel', 1,), ),
    },),
'bone hammer':({ # hammer level 3
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_BONE,5,),),
    'sound'     : 60,
    'construct' : 40,
    'components': (
        [ ('piece of bone', 2,), ],
        [ ('stick of plastic', 1,), ('stick of wood', 1,), ],
        [ ('cordage', 3,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 1,), ],
        [ (cmp.Tool_Chisel, 2,), ],
        ),
    'using'     : (),
    'byproducts': ( ('parcel of bone', 1,), ('scrap bone', 1,), ),
    },),
'metal hammer':({ # hammer level 4
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_METAL,10,),),
    'sound'     : 120,
    'construct' : 72,
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
    'using'     : (),
    'byproducts': ( ('scrap wood', 1,), ),
    },),
'fine hammer':({ # hammer level 5
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_METAL,35,),),
    'sound'     : 120,
    'construct' : 144,
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
    'using'     : (),
    'byproducts': ( ('parcel of wood', 1,), ('scrap wood', 1,), ),
    },),

    # machetes

'plastic machete':({
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_PLASTIC,10,),),
    'sound'     : 60,
    'construct' : 20,
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
    'using'     : (),
    'byproducts': ( ('scrap plastic', 1,), ),
    },),
##'stone machete':({
##    'quantity'  : 1,
##    'table'     : CRT_TOOLS,
##    'category'  : CRC_STONE,
##    'sound'     : 60,
##    'construct' : 144,
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
##    },),
'wooden machete':({
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_WOOD,10,),),
    'sound'     : 60,
    'construct' : 32,
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
    'using'     : (),
    'byproducts': ( ('parcel of wood', 2,), ('scrap wood', 3,), ),
    },),
'bone machete':({
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_BONE,20,),),
    'sound'     : 60,
    'construct' : 96,
    'components': (
        [ ('bone, large', 1,), ],
        [ ('parcel of wood', 1,), ('bone', 1,), ('piece of bone', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 3,), ],
        [ (cmp.Tool_Chisel, 2,), ],
        [ (cmp.Tool_Sharpener, 1,), ],
        ),
    'using'     : (),
    'byproducts': ( ('parcel of bone', 1,), ('scrap bone', 4,), ),
    },),

    # TODO: do all metal blade weapons in the following format:
        # (must make the blade first, then sharpen it, then make handle,
        #  then finally attach handle to blade)
'unfinished metal machete blade':({
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_METAL,10,),(SKL_BLADESMITH,10,),),
    'sound'     : 120,
    'construct' : 1440,
    'components': (
        [ ('parcel of metal', 15,), ('piece of metal', 3,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 2,), ],
        [ (cmp.Tool_Furnace, 2,), ],
        [ (cmp.Tool_Chisel, 2,), ],
        [ (cmp.Tool_Crucible, 2,), ],
        [ (cmp.Tool_Tongs, 2,), ],
        [ (cmp.Tool_Anvil, 2,), ],
        [ (cmp.Mold_MacheteMetal, 1,), ],
        ),
    'using'     : (),
    'byproducts': (),
    },),
'metal machete blade':({
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_BLADESMITH,5,),),
    'sound'     : 120,
    'construct' : 144,
    'components': (
        [ ('unfinished metal machete blade', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Grinder, 4,), ],
        [ (cmp.Tool_Sharpener, 4,), ],
        ),
    'using'     : (),
    'byproducts': (),
    },),
'wooden machete handle':({
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_WOOD,10,),),
    'sound'     : 120,
    'construct' : 72,
    'components': (
        [ ('parcel of wood', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_File, 2,), ],
        [ (cmp.Tool_Chisel, 2,), ],
        [ (cmp.Tool_Hammer, 1,), ],
        ),
    'using'     : (),
    'byproducts': (),
    },),
'metal machete':({ # wooden handle
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_WOOD,10,),(SKL_METAL,5,),),
    'sound'     : 120,
    'construct' : 72,
    'components': (
        [ ('metal machete blade', 1,), ],
        [ ('wooden machete handle', 1,), ],
        ),
    'tools'     : ( [ (cmp.Tool_Hammer, 2,), ], ),
    'using'     : (),
    'byproducts': (),
    },
                 { # plastic handle
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_PLASTIC,15,),(SKL_METAL,5,),),
    'sound'     : 120,
    'construct' : 72,
    'components': (
        [ ('metal machete blade', 1,), ],
        [ ('plastic machete handle', 1,), ],
        ),
    'tools'     : ( [ (cmp.Tool_Hammer, 2,), ], ),
    'using'     : (),
    'byproducts': (),
    },),

    # mandrils
'metal mandril':({
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_METAL,30,),),
    'construct' : 40,
    'components': (
        [ ('stick of metal', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 4,), ],
        [ (cmp.Tool_Furnace, 2,), (cmp.Tool_Torch, 3,), ],
        [ (cmp.Tool_Anvil, 3,), ],
        [ (cmp.Tool_Swage, 2,), ],
        [ (cmp.Tool_Tongs, 1,), ],
        ),
    'using'     : (),
    'byproducts': (),
    },),

    # molds
# staff molds
    # TODO: change all earthenware recipes to the following format
        # (requires two steps: making, then firing. making step is
        #   quick, easy. Firing is auto, takes longer, is harder to do)
'unfired earthenware mold, metal staff':({
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_CLAY,5,),),
    'construct' : 24,
    'info'      : ('auto',),
    'components': (
        [ ('chunk of clay', 2,), ],
        ),
    'tools'     : (),
    'using'     : (),
    'byproducts': (),
    },),
'earthenware mold, metal staff':({
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_CLAY,10,),),
    'construct' : 3600,
    'info'      : ('auto',),
    'components': (
        [ ('unfired earthenware mold, metal staff', 1,), ],
        ),
    'tools'     : (),
    'using'     : ( [ (cmp.Tool_Furnace, 1,), ], ),
    'byproducts': (),
    },),
# sword molds
'earthenware mold, plastic sword':({
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_ASSEMBLY,15,), (SKL_BLADESMITH,3,),),
    'construct' : 32,
    'components': (
        [ ('chunk of clay', 3,), ],
        ),
    'tools'     : (),
    'using'     : ( [ (cmp.Tool_Furnace, 1,), ], ),
    'byproducts': (),
    },),
'earthenware mold, metal sword':({
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_ASSEMBLY,25,), (SKL_BLADESMITH,10,),),
    'construct' : 48,
    'components': (
        [ ('chunk of clay', 3,), ],
        ),
    'tools'     : (),
    'using'     : ( [ (cmp.Tool_Furnace, 1,), ], ),
    'byproducts': (),
    },),
# dagger molds
'earthenware mold, metal dagger':({
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_ASSEMBLY,30,), (SKL_BLADESMITH,20,),),
    'construct' : 24,
    'components': (
        [ ('chunk of clay', 1,), ],
        ),
    'tools'     : (),
    'using'     : ( [ (cmp.Tool_Furnace, 1,), ], ),
    'byproducts': (),
    },),
# ammunition molds
'earthenware mold, bullet, small':({
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_ASSEMBLY,6,),),
    'construct' : 8,
    'components': (
        [ ('piece of clay', 1,), ],
        ),
    'tools'     : (),
    'using'     : ( [ (cmp.Tool_Furnace, 1,), ], ),
    'byproducts': (),
    },),
'earthenware mold, bullet':({
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_ASSEMBLY,5,),),
    'construct' : 9,
    'components': (
        [ ('piece of clay', 1,), ],
        ),
    'tools'     : (),
    'using'     : ( [ (cmp.Tool_Furnace, 1,), ], ),
    'byproducts': (),
    },),
'earthenware mold, bullet, large':({
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_ASSEMBLY,4,),),
    'construct' : 10,
    'components': (
        [ ('piece of clay', 1,), ],
        ),
    'tools'     : (),
    'using'     : ( [ (cmp.Tool_Furnace, 1,), ], ),
    'byproducts': (),
    },),
'earthenware mold, Minni ball':({
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_ASSEMBLY,15,),),
    'construct' : 18,
    'components': (
        [ ('piece of clay', 1,), ],
        ),
    'tools'     : (),
    'using'     : ( [ (cmp.Tool_Furnace, 1,), ], ),
    'byproducts': (),
    },),

    # pliers
'pliers':({ # pliers level 2
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_METAL,8,),),
    'sound'     : 120,
    'construct' : 48,
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
    'using'     : (),
    'byproducts': ( ('scrap metal', 2,), ),
    },),
'needle-nose pliers':({ # pliers level 3, also can cut as well as wire cutters
    # should the needle-nose property be an additional Tool component? Only if it's a unique property not fulfilled by any other tool...
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_METAL,25,),),
    'sound'     : 120,
    'construct' : 96,
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
    'using'     : (),
    'byproducts': (),
    },),

    # ramrods
'metal ramrod, long':({
    'quantity'  : 1,
    'table'     : CRT_STUFF,
    'skills'    : ((SKL_METAL,20,),),
    'construct' : 72,
    'components': (
        [ ('stick of metal', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 3,), ],
        [ (cmp.Tool_Anvil, 3,), ],
        [ (cmp.Tool_Furnace, 2,), (cmp.Tool_Torch, 3,), ],
        [ (cmp.Tool_Swage, 2,), ],
        [ (cmp.Tool_Tongs, 1,), ],
        ),
    'using'     : (),
    'byproducts': (),
    },),

    # saws
'plastic saw':({ # saw level 1
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_PLASTIC,15,),),
    'construct' : 20,
    'components': (
        [ ('piece of plastic', 1,), ],
        [ ('parcel of plastic', 1,), ('parcel of wood', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_File, 1,), (cmp.Tool_Saw, 1,), (cmp.Tool_Cut, 5,), ],
        [ (cmp.Tool_Hammer, 1,), ],
        [ (cmp.Tool_Chisel, 1,), ],
        ),
    'using'     : (),
    'byproducts': ( ('scrap plastic', 1), ),
    },),
'plastic saw, large':({ # saw level 2
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_PLASTIC,15,),),
    'sound'     : 60,
    'construct' : 36,
    'components': (
        [ ('chunk of plastic', 1,), ],
        [ ('parcel of plastic', 2,), ('parcel of wood', 2,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 2,), ],
        [ (cmp.Tool_File, 1,), (cmp.Tool_Saw, 1,), (cmp.Tool_Cut, 5,), ],
        [ (cmp.Tool_Chisel, 1,), ],
        ),
    'using'     : (),
    'byproducts': ( ('shard of plastic', 2), ('scrap plastic', 1), ),
    },),
'bone saw':({ # saw level 2
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_BONE,35,),),
    'sound'     : 60,
    'construct' : 32,
    'components': (
        [ ('bone', 1,), ],
        [ ('parcel of plastic', 2,), ('parcel of wood', 2,),
          ('piece of bone', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Saw, 3,), ],
        [ (cmp.Tool_Hammer, 2,), ],
        [ (cmp.Tool_File, 3,), (cmp.Tool_Saw, 4,), (cmp.Tool_Cut, 5,), ],
        [ (cmp.Tool_Chisel, 1,), ],
        ),
    'using'     : (),
    'byproducts': ( ('shard of bone', 1), ),
    },),
'bone saw, large':({ # saw level 3
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_BONE,35,),),
    'sound'     : 60,
    'construct' : 48,
    'components': (
        [ ('bone, large', 1,), ],
        [ ('parcel of plastic', 2,), ('parcel of wood', 2,),
          ('piece of bone', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Saw, 3,), ],
        [ (cmp.Tool_Hammer, 2,), ],
        [ (cmp.Tool_File, 3,), (cmp.Tool_Saw, 4,),  (cmp.Tool_Cut, 5,),],
        [ (cmp.Tool_Chisel, 1,), ],
        ),
    'using'     : (),
    'byproducts': ( ('shard of bone', 1), ('scrap bone', 1), ),
    },),
'metal saw':({ # saw level 3
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_METAL,20,),),
    'sound'     : 120,
    'construct' : 64,
    'components': (
        [ ('piece of metal', 1,), ],
        [ ('parcel of plastic', 1,), ('parcel of wood', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 4,), ],
        [ (cmp.Tool_File, 6,), (cmp.Tool_Saw, 5,),  (cmp.Tool_Cut, 9,),],
        [ (cmp.Tool_Anvil, 3,), ],
        [ (cmp.Tool_Furnace, 2,), ],
        [ (cmp.Tool_Chisel, 1,), ],
        [ (cmp.Tool_Tongs, 1,), ],
        ),
    'using'     : (),
    'byproducts': (),
    },),
'metal saw, large':({ # saw level 4
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_METAL,20,),),
    'sound'     : 120,
    'construct' : 72,
    'components': (
        [ ('metal sheet', 1,), ],
        [ ('parcel of plastic', 2,), ('parcel of wood', 2,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Anvil, 5,), ],
        [ (cmp.Tool_Hammer, 4,), ],
        [ (cmp.Tool_File, 5,), (cmp.Tool_Saw, 5,),  (cmp.Tool_Cut, 9,),],
        [ (cmp.Tool_Chisel, 1,), ],
        ),
    'using'     : (),
    'byproducts': ( ('parcel of metal', 1), ('shard of metal', 1), ('scrap metal', 1), ),
    },),

    # sewing needles
'plastic sewing needle':({ # sewing level 1
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_PLASTIC,10,),),
    'sound'     : 60,
    'construct' : 10,
    'components': (
        [ ('scrap plastic', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Torch, 1,), (cmp.Tool_Furnace, 1,), ],
        [ (cmp.Tool_Hammer, 1,), ],
        [ (cmp.Tool_Anvil, 1,), ],
        ),
    'using'     : (),
    'byproducts': (),
    },),
'bone sewing needle':({ # sewing level 2
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_BONE,20,),),
    'sound'     : 60,
    'construct' : 24,
    'components': (
        [ ('scrap bone', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Chisel, 3,), ],
        [ (cmp.Tool_Hammer, 2,), ],
        [ (cmp.Tool_Anvil, 2,), ],
        [ (cmp.Tool_Sharpener, 1,), (cmp.Tool_File, 3,), ],
        ),
    'using'     : (),
    'byproducts': (),
    },),
'metal sewing needle':({ # sewing level 3
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_METAL,15,),),
    'sound'     : 120,
    'construct' : 20,
    'components': (
        [ ('metal needle', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 5,), ],
        [ (cmp.Tool_File, 5,), ],
        [ (cmp.Tool_Sharpener, 3,), ],
        [ (cmp.Tool_Anvil, 3,), ],
        [ (cmp.Tool_Pliers, 2,), ],
        [ (cmp.Tool_Furnace, 1,), (cmp.Tool_Torch, 3,), ],
        [ (cmp.Tool_Tongs, 1,), ],
        ),
    'using'     : (),
    'byproducts': (),
    },),

    # swage blocks
'wooden swage block':({ # swage level 1
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_WOOD,40,),),
    'sound'     : 120,
    'construct' : 72,
    'components': (
        [ ('chunk of wood', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Chisel, 4,), ],
        [ (cmp.Tool_Hammer, 3,), ],
        [ (cmp.Tool_Saw, 3,), ],
        ),
    'using'     : (),
    'byproducts': ( ('scrap wood', 2,), ),
    },),
'metal swage block':({ # swage level 2 (level 3 is difficult to fabricate.)
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_METAL,50,),),
    'sound'     : 120,
    'construct' : 576,
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
    'using'     : (),
    'byproducts': (
        ('metal pipe', 1,), ('stick of metal', 1,),
        ),
    },),

    # tongs
'tongs':({ # tongs level 2
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_METAL,8,),),
    'sound'     : 120,
    'construct' : 72,
    'components': (
        [ ('stick of metal', 2,), ],
        [ ('nail', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 3,), ],
        [ (cmp.Tool_Furnace, 2,), (cmp.Tool_Torch, 3,), ],
        [ (cmp.Tool_Anvil, 2,), ],
        ),
    'using'     : (),
    'byproducts': (),
    },),
'tongs, large':({ # tongs level 3
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_METAL,15,),),
    'sound'     : 120,
    'construct' : 96,
    'components': (
        [ ('pole of metal', 2,), ],
        [ ('nail', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 3,), ],
        [ (cmp.Tool_Anvil, 3,), ],
        [ (cmp.Tool_Furnace, 2,), ],
        ),
    'using'     : (),
    'byproducts': (),
    },),
'fine tongs':({ # tongs level 4
    'quantity'  : 1,
    'table'     : CRT_TOOLS,
    'skills'    : ((SKL_METAL,20,),),
    'sound'     : 120,
    'construct' : 144,
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
    'using'     : (),
    'byproducts': (),
    },),





    #--------------------------#
    #         Weapons          #
    #--------------------------#



    # misc
'flamethrower':({
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_ASSEMBLY,35,),),
    'construct' : 40,
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
    'using'     : (),
    'byproducts': ( ('scrap plastic', 1, ), ),
    },),
'sling':({
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_ASSEMBLY,8,),),
    'construct' : 8,
    'components': (
        [ ('cordage', 3,), ],
        ),
    'tools'     : (),
    'using'     : (),
    'byproducts': (),
    },),
'slingshot':({
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_WOOD,5,),),
    'construct' : 16,
    'components': (
        [ ('parcel of wood', 1,), ],
        [ ('rubber band', 3,), ],
        ),
    'tools'     : ( [ (cmp.Tool_Cut, 4,), ], ),
    'using'     : (),
    'byproducts': ( ('scrap wood', 1,), ),
    },),

    # shivs
'ceramic shiv':({
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_ASSEMBLY,5,),),
    'construct' : 8,
    'components': (
        [ ('shard of ceramic', 1,), ],
        [ ('parcel of plastic', 1,), ('parcel of wood', 1,),
          ('parcel of bone', 1,), ('parcel of stone', 1,),
          ('parcel of metal', 1,), ],
        [ ('duct tape', 2,), ('sinew', 1,), ],
        ),
    'tools'     : (),
    'using'     : (),
    'byproducts': ( ('scrap plastic', 1,), ),
    },),
'plastic shiv':({
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_ASSEMBLY,5,),),
    'construct' : 5,
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
    'using'     : (),
    'byproducts': ( ('scrap plastic', 1,), ),
    },),
'wooden shiv':({
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_ASSEMBLY,5,),),
    'construct' : 6,
    'components': (
        [ ('shard of wood', 1,), ],
        [ ('parcel of plastic', 1,), ('parcel of wood', 1,),
          ('parcel of bone', 1,), ('parcel of stone', 1,),
          ('parcel of metal', 1,), ],
        [ ('duct tape', 2,), ('sinew', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Sharpener, 1,), (cmp.Tool_File, 2,), (cmp.Tool_Cut, 6,), ],
        ),
    'using'     : (),
    'byproducts': ( ('scrap wood', 1,), ),
    },),
'stone shiv':({
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_ASSEMBLY,5,),),
    'construct' : 8,
    'components': (
        [ ('shard of stone', 1,), ],
        [ ('parcel of plastic', 1,), ('parcel of wood', 1,),
          ('parcel of bone', 1,), ('parcel of stone', 1,),
          ('parcel of metal', 1,), ],
        [ ('duct tape', 2,), ('sinew', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Sharpener, 2,), (cmp.Tool_File, 4,), ],
        ),
    'using'     : (),
    'byproducts': ( ('gravel', 1,), ),
    },),
'bone shiv':({
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_ASSEMBLY,5,),),
    'construct' : 6,
    'components': (
        [ ('shard of bone', 1,), ],
        [ ('parcel of plastic', 1,), ('parcel of wood', 1,),
          ('parcel of bone', 1,), ('parcel of stone', 1,),
          ('parcel of metal', 1,), ],
        [ ('duct tape', 2,), ('sinew', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Sharpener, 1,), (cmp.Tool_File, 3,), ],
        ),
    'using'     : (),
    'byproducts': ( ('scrap bone', 1,), ),
    },),
'glass shiv':({
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_ASSEMBLY,5,),),
    'construct' : 8,
    'components': (
        [ ('shard of glass', 1,), ],
        [ ('parcel of plastic', 1,), ('parcel of wood', 1,),
          ('parcel of bone', 1,), ('parcel of stone', 1,),
          ('parcel of metal', 1,), ],
        [ ('duct tape', 2,), ('sinew', 1,), ],
        ),
    'tools'     : (),
    'using'     : (),
    'byproducts': (),
    },),
'metal shiv':({
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_ASSEMBLY,5,),),
    'construct' : 10,
    'components': (
        [ ('shard of metal', 1,), ],
        [ ('parcel of plastic', 1,), ('parcel of wood', 1,),
          ('parcel of bone', 1,), ('parcel of stone', 1,),
          ('parcel of metal', 1,), ],
        [ ('duct tape', 2,), ('sinew', 1,), ],
        ),
    'tools'     : ( [ (cmp.Tool_Sharpener, 3,), (cmp.Tool_File, 5,), ], ),
    'using'     : (),
    'byproducts': (),
    },),

    # knives
'plastic knife':({
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_PLASTIC,5,),),
    'construct' : 20,
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
    'using'     : (),
    'byproducts': ( ('scrap plastic', 1,), ),
    },),
'wooden knife':({
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_WOOD,5,),),
    'construct' : 32,
    'components': (
        [ ('shard of wood', 1,), ],
        [ ('parcel of plastic', 1,), ('parcel of wood', 1,),
          ('parcel of bone', 1,), ],
        [ ('cordage', 1,), ('glue', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Cut, 6,), ],
        [ (cmp.Tool_Sharpener, 1,), (cmp.Tool_File, 2,), ],
        ),
    'using'     : (),
    'byproducts': ( ('scrap wood', 1,), ),
    },),
'stone knife':({
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_STONE,15,),),
    'sound'     : 60,
    'construct' : 40,
    'components': (
        [ ('shard of stone', 1,), ],
        [ ('parcel of plastic', 1,), ('parcel of wood', 1,),
          ('parcel of bone', 1,), ('parcel of stone', 1,), ],
        [ ('cordage', 1,), ('glue', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Chisel, 3,), ],
        [ (cmp.Tool_Hammer, 3,), ],
        [ (cmp.Tool_Sharpener, 2,), (cmp.Tool_File, 4,), ],
        ),
    'using'     : (),
    'byproducts': ( ('gravel', 1,), ),
    },),
'bone knife':({
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_BONE,10,),),
    'sound'     : 60,
    'construct' : 48,
    'components': (
        [ ('shard of bone', 1,), ],
        [ ('parcel of plastic', 1,), ('parcel of wood', 1,),
          ('parcel of bone', 1,), ('parcel of stone', 1,), ],
        [ ('cordage', 1,), ('glue', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 2,), ],
        [ (cmp.Tool_Chisel, 2,), ],
        [ (cmp.Tool_Sharpener, 1,), (cmp.Tool_File, 3,), ],
        ),
    'using'     : (),
    'byproducts': ( ('scrap bone', 1,), ),
    },),
'glass knife':({
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_GLASS,25,),),
    'sound'     : 60,
    'construct' : 144,
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
    'using'     : (),
    'byproducts': (),
    },),
'metal knife':({
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_METAL,10,),),
    'sound'     : 120,
    'construct' : 72,
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
    'using'     : (),
    'byproducts': (),
    },),

    # serrated knives
'plastic serrated knife':({
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_PLASTIC,10,),),
    'construct' : 18,
    'components': ( [ ('plastic knife', 1,), ], ),
    'tools'     : ( [ (cmp.Tool_File, 1,), ], ),
    'using'     : (),
    'byproducts': (),
    },),
'wooden serrated knife':({ # serrated knives: Dmg +2, Pen -2, Asp -15, Cut -1, Saw +1, Chisel -1
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_WOOD,15,),),
    'construct' : 32,
    'components': ( [ ('wooden knife', 1,), ], ),
    'tools'     : ( [ (cmp.Tool_File, 2,), (cmp.Tool_Saw, 5,), ], ),
    'using'     : (),
    'byproducts': (),
    },),
'stone serrated knife':({
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_STONE,40,),),
    'construct' : 72,
    'components': ( [ ('stone knife', 1,), ], ),
    'tools'     : ( [ (cmp.Tool_File, 4,), (cmp.Tool_Saw, 5,), ], ),
    'using'     : (),
    'byproducts': (),
    },),
'bone serrated knife':({
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_BONE,25,),),
    'construct' : 48,
    'components': ( [ ('bone knife', 1,), ], ),
    'tools'     : ( [ (cmp.Tool_File, 3,), (cmp.Tool_Saw, 5,), ], ),
    'using'     : (),
    'byproducts': (),
    },),
'metal serrated knife':({
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_METAL,30,),),
    'construct' : 96,
    'components': ( [ ('metal knife', 1,), ], ),
    'tools'     : ( [ (cmp.Tool_File, 5,), (cmp.Tool_Saw, 5,), ], ),
    'using'     : (),
    'byproducts': (),
    },),

    # daggers
'bone dagger':({
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_BONE,30,),),
    'sound'     : 60,
    'construct' : 96,
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
    'using'     : (),
    'byproducts': (),
    },),
'glass dagger':({
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_GLASS,50,),),
    'sound'     : 60,
    'construct' : 288,
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
    'using'     : (),
    'byproducts': (),
    },),
'metal dagger':({
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_METAL,20,),),
    'sound'     : 120,
    'construct' : 144,
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
    'using'     : (),
    'byproducts': (),
    },),

    # staves / staffs
'plastic staff':({
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_PLASTIC,6,),),
    'sound'     : 60,
    'construct' : 24,
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
    'using'     : (),
    'byproducts': ( ('scrap plastic', 2,), ),
    },),
'wooden staff':({
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_WOOD,12,),),
    'sound'     : 60,
    'construct' : 72,
    'components': (
        [ ('chunk of wood', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Saw, 3,), ],
        [ (cmp.Tool_Hammer, 2,), ],
        [ (cmp.Tool_Chisel, 1,), ],
        ),
    'using'     : (),
    'byproducts': (
        ('piece of wood', 2,),
        ('parcel of wood', 2,),
        ('scrap wood', 2,),
        ),
    },),
'bone staff':({
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_WOOD,20,),(SKL_BONE,10,),),
    'sound'     : 60,
    'construct' : 120,
    'components': (
        [ ('chunk of wood', 1,), ],
        [ ('bone', 2,), ],
        [ ('cordage', 2,), ('glue', 4,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Saw, 3,), ],
        [ (cmp.Tool_Hammer, 3,), ],
        [ (cmp.Tool_Chisel, 2,), ],
        ),
    'using'     : (),
    'byproducts': (
        ('piece of wood', 2,),
        ('parcel of wood', 2,),
        ('scrap wood', 2,),
        ('parcel of bone', 1,),
        ('scrap bone', 2,),
        ),
    },),
'metal staff':({
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_WOOD,15,),(SKL_METAL,10,),),
    'sound'     : 60,
    'construct' : 120,
    'components': (
        [ ('chunk of wood', 1,), ],
        [ ('parcel of metal', 3,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 3,), ],
        [ (cmp.Tool_Furnace, 2,), ],
        [ (cmp.Tool_Saw, 3,), ],
        [ (cmp.Tool_Anvil, 2,), ],
        [ (cmp.Tool_Chisel, 2,), ],
        [ (cmp.Tool_Crucible, 2,), ],
        [ (cmp.Tool_Tongs, 2,), ],
        ),
    'using'     : (),
    'byproducts': (
        ('piece of wood', 2,),
        ('parcel of wood', 2,),
        ('scrap wood', 2,),
        ),
    },),
'steel staff':({
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_METAL,20,),),
    'sound'     : 120,
    'construct' : 144,
    'components': (
        [ ('parcel of steel', 11,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 4,), ],
        [ (cmp.Tool_Furnace, 3,), ],
        [ (cmp.Tool_Crucible, 2,), ],
        [ (cmp.Tool_Anvil, 2,), ],
        [ (cmp.Tool_Swage, 1,), ],
        ),
    'using'     : (),
    'byproducts': (),
    },),

    # swords
'plastic sword':({
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_PLASTIC,10,), (SKL_BLADESMITH,5,),),
    'sound'     : 60,
    'construct' : 48,
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
    'using'     : (),
    'byproducts': (),
    },),
'wooden sword':({
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_WOOD,10,), (SKL_BLADESMITH,5,),),
    'sound'     : 60,
    'construct' : 120,
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
    'using'     : (),
    'byproducts': (
        ('piece of wood', 2,),
        ('parcel of wood', 2,),
        ('scrap wood', 4,),
        ),
    },),
'bone sword':({
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_BONE,20,), (SKL_BLADESMITH,10,),),
    'sound'     : 60,
    'construct' : 144,
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
    'using'     : (),
    'byproducts': (
        ('scrap wood', 1,),
        ('piece of bone', 1,),
        ('parcel of bone', 2,),
        ('scrap bone', 5,),
        ),
    },),
'glass sword':({ # glass is the hardest to work with, and making a whole sword out of it is very tough.
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_GLASS,30,), (SKL_BLADESMITH,20,),),
    'sound'     : 60,
    'construct' : 640,
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
    'using'     : (),
    'byproducts': ( ('scrap wood', 1,), ),
    },),
'metal sword blade':({
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_METAL,20,), (SKL_BLADESMITH,12,),),
    'sound'     : 120,
    'construct' : 384,
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
    'using'     : (),
    'byproducts': (),
    },),
'wooden sword hilt':({
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_WOOD,10,), (SKL_BLADESMITH,10,),),
    'construct' : 72,
    'components': (
        [ ('parcel of wood', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 3,), ],
        [ (cmp.Tool_Chisel, 2,), ],
        ),
    'using'     : (),
    'byproducts': ( ('scrap wood', 1,), ),
    },),
'unsharpened metal sword':({
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_METAL,5,), (SKL_BLADESMITH,5,),),
    'sound'     : 120,
    'construct' : 96,
    'components': (
        [ ('metal sword blade', 1,), ],
        [ ('plastic sword hilt', 1,), ('wooden sword hilt', 1,),
          ('bone sword hilt', 1,), ],
        [ ('brass rivet', 2,), ('nail', 2,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 5,), ],
        ),
    'using'     : (),
    'byproducts': (),
    },),
'metal sword':({
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_METAL,1,), (SKL_BLADESMITH,3,),),
    'sound'     : 120,
    'construct' : 128,
    'components': (
        [ ('unsharpened metal sword', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Sharpener, 3,), ],
        ),
    'using'     : (),
    'byproducts': (),
    },),

    # boomerangs
'plastic boomerang':({
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_PLASTIC,10,),),
    'sound'     : 60,
    'construct' : 24,
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
    'using'     : (),
    'byproducts': (),
    },),
'wooden boomerang':({
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_WOOD,10,),),
    'construct' : 32,
    'components': (
        [ ('piece of wood', 1,), ('stick of wood', 1,), ('root', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 2,), ],
        [ (cmp.Tool_Chisel, 2,), ],
        [ (cmp.Tool_Chop, 1,), ],
        [ (cmp.Tool_Sharpener, 1,), ],
        ),
    'using'     : (),
    'byproducts': ( ('shard of wood', 1,), ('scrap wood', 1,), ),
    },),
'bone boomerang':({
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_BONE,10,),),
    'construct' : 64,
    'components': (
        [ ('bone, large', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Chisel, 3,), ],
        [ (cmp.Tool_Hammer, 2,), ],
        [ (cmp.Tool_Sharpener, 1,), ],
        ),
    'using'     : (),
    'byproducts': ( ('piece of bone', 2,), ('shard of bone', 2,), ('scrap bone', 2,), ),
    },),
'metal boomerang':({
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_METAL,10,),),
    'sound'     : 120,
    'construct' : 48,
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
    'using'     : (),
    'byproducts': (),
    },),
'ceramic boomerang':({
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_CERAMIC,20,),),
    'construct' : 72,
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
    'using'     : (),
    'byproducts': (),
    },),

    # javelins
'plastic javelin':({
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_PLASTIC,3,),),
    'construct' : 10,
    'components': (
        [ ('stick of plastic', 1,), ('plastic tube', 2,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Furnace, 1,), (cmp.Tool_Torch, 1,), ],
        [ (cmp.Tool_Hammer, 1,), ],
        [ (cmp.Tool_Anvil, 1,), ],
        ),
    'using'     : (),
    'byproducts': (),
    },),
'wooden javelin':({
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_WOOD,3,),),
    'construct' : 10,
    'components': (
        [ ('stick of wood', 1,), ],
        ),
    'tools'     : ( [ (cmp.Tool_Furnace, 1,), (cmp.Tool_Cut, 4,), ], ),
    'using'     : (),
    'byproducts': (),
    },),
'metal javelin':({
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_METAL,5,),),
    'sound'     : 120,
    'construct' : 20,
    'components': (
        [ ('stick of metal', 1,), ('metal tube', 2,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_File, 5,), (cmp.Tool_Grinder, 4,), ],
        [ (cmp.Tool_Hammer, 3,), ],
        [ (cmp.Tool_Furnace, 2,), (cmp.Tool_Torch, 3,), ],
        [ (cmp.Tool_Anvil, 2,), ],
        [ (cmp.Tool_Sharpener, 2,), ],
        [ (cmp.Tool_Tongs, 1,), ],
        ),
    'using'     : (),
    'byproducts': (),
    },),

    # shortspears
'plastic shortspear':({
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_ASSEMBLY,3,),),
    'construct' : 6,
    'components': (
        [ ('stick of plastic', 1,), ('plastic pipe', 1,), ('stick of wood', 1,), ],
        [ ('plastic spearhead', 1,), ],
        [ ('string', 1,), ('glue', 1,), ('sinew', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 1,), ],
        [ (cmp.Tool_Chisel, 1,), ],
        ),
    'using'     : (),
    'byproducts': (),
    },),
'wooden shortspear':({
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_ASSEMBLY,5,),),
    'construct' : 8,
    'components': (
        [ ('stick of plastic', 1,), ('plastic pipe', 1,), ('stick of wood', 1,), ],
        [ ('wooden spearhead', 1,), ],
        [ ('string', 1,), ('glue', 1,), ('sinew', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 1,), ],
        [ (cmp.Tool_Chisel, 1,), ],
        ),
    'using'     : (),
    'byproducts': (),
    },),
'stone shortspear':({
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_ASSEMBLY,6,),),
    'construct' : 8,
    'components': (
        [ ('stick of plastic', 1,), ('plastic pipe', 1,), ('stick of wood', 1,), ],
        [ ('stone spearhead', 1,), ],
        [ ('string', 1,), ('sinew', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 1,), ],
        [ (cmp.Tool_Chisel, 1,), ],
        ),
    'using'     : (),
    'byproducts': (),
    },),
'bone shortspear':({
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_ASSEMBLY,7,),),
    'construct' : 8,
    'components': (
        [ ('stick of plastic', 1,), ('plastic pipe', 1,), ('stick of wood', 1,), ],
        [ ('bone spearhead', 1,), ],
        [ ('string', 1,), ('glue', 1,), ('sinew', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 1,), ],
        [ (cmp.Tool_Chisel, 1,), ],
        ),
    'using'     : (),
    'byproducts': (),
    },),
'metal shortspear':({
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_METAL,6,),),
    'sound'     : 120,
    'construct' : 12,
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
    'using'     : (),
    'byproducts': (),
    },),
'glass shortspear':({
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_ASSEMBLY,9,),),
    'construct' : 8,
    'components': (
        [ ('stick of plastic', 1,), ('plastic pipe', 1,), ('stick of wood', 1,), ],
        [ ('glass spearhead', 1,), ],
        [ ('string', 1,), ('sinew', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 2,), ],
        [ (cmp.Tool_Chisel, 1,), ],
        ),
    'using'     : (),
    'byproducts': (),
    },),

    # spears
'plastic spear':({
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_ASSEMBLY,3,),),
    'construct' : 6,
    'components': (
        [ ('pole of plastic', 1,), ('pole of wood', 1,), ],
        [ ('plastic spearhead', 1,), ],
        [ ('string', 1,), ('glue', 1,), ('sinew', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 1,), ],
        [ (cmp.Tool_Chisel, 1,), ],
        ),
    'using'     : (),
    'byproducts': (),
    },),
'wooden spear':({
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_ASSEMBLY,5,),),
    'construct' : 12,
    'components': (
        [ ('pole of plastic', 1,), ('pole of wood', 1,), ],
        [ ('wooden spearhead', 1,), ],
        [ ('string', 1,), ('glue', 1,), ('sinew', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 1,), ],
        [ (cmp.Tool_Chisel, 1,), ],
        ),
    'using'     : (),
    'byproducts': (),
    },),
'stone spear':({
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_ASSEMBLY,6,),),
    'construct' : 12,
    'components': (
        [ ('pole of plastic', 1,), ('pole of wood', 1,), ],
        [ ('stone spearhead', 1,), ],
        [ ('string', 1,), ('sinew', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 1,), ],
        [ (cmp.Tool_Chisel, 1,), ],
        ),
    'using'     : (),
    'byproducts': (),
    },),
'bone spear':({
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_ASSEMBLY,7,),),
    'construct' : 12,
    'components': (
        [ ('pole of plastic', 1,), ('pole of wood', 1,), ],
        [ ('bone spearhead', 1,), ],
        [ ('string', 1,), ('glue', 1,), ('sinew', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 1,), ],
        [ (cmp.Tool_Chisel, 1,), ],
        ),
    'using'     : (),
    'byproducts': (),
    },),
'metal spear':({
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_METAL,6,),),
    'sound'     : 120,
    'construct' : 12,
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
    'using'     : (),
    'byproducts': (),
    },),
'glass spear':({
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_ASSEMBLY,9,),),
    'construct' : 12,
    'components': (
        [ ('pole of plastic', 1,), ('pole of wood', 1,), ],
        [ ('glass spearhead', 1,), ],
        [ ('string', 1,), ('sinew', 1,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 1,), ],
        [ (cmp.Tool_Chisel, 1,), ],
        ),
    'using'     : (),
    'byproducts': (),
    },),

    # cudgels    
'plastic cudgel':({
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_PLASTIC,2,),),
    'sound'     : 60,
    'construct' : 10,
    'components': (
        [ ('chunk of plastic', 1,), ],
        [ ('stick of wood', 1,), ('stick of plastic', 1,), ],
        [ ('cordage', 1,), ('glue', 1,), ],
        ),
    'tools'     : ( [(cmp.Tool_Hammer, 1),], [(cmp.Tool_Chisel, 1),], ),
    'using'     : (),
    'byproducts': ( ('piece of plastic', 2,), ('shard of plastic', 4,), ('scrap plastic', 1,), ),
    },),
'wooden cudgel':({
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_WOOD,3,),),
    'sound'     : 60,
    'construct' : 30,
    'components': (
        [ ('chunk of wood', 1,), ],
        [ ('stick of wood', 1,), ],
        [ ('cordage', 1,), ('glue', 1,), ],
        ),
    'tools'     : ( [(cmp.Tool_Hammer, 2),], [(cmp.Tool_Chisel, 2),], ),
    'using'     : (),
    'byproducts': ( ('piece of wood', 2,), ('shard of wood', 4,), ('scrap wood', 1,), ),
    },),
'bone cudgel':({
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_BONE,5,), (SKL_WOOD,2,),),
    'sound'     : 60,
    'construct' : 40,
    'components': (
        [ ('chunk of bone', 1,), ],
        [ ('stick of wood', 1,), ],
        [ ('cordage', 1,), ('glue', 1,), ],
        ),
    'tools'     : ( [(cmp.Tool_Hammer, 2),], [(cmp.Tool_Chisel, 3),], ),
    'using'     : (),
    'byproducts': ( ('shard of bone', 4,), ('scrap bone', 1,), ),
    },),
'stone cudgel':({
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_STONE,8,), (SKL_WOOD,4,),),
    'sound'     : 60,
    'construct' : 50,
    'components': (
        [ ('chunk of stone', 1,), ],
        [ ('stick of wood', 1,), ],
        ),
    'tools'     : ( [(cmp.Tool_Hammer, 3),], [(cmp.Tool_Chisel, 4),], ),
    'using'     : (),
    'byproducts': ( ('piece of stone', 2,), ('shard of stone', 4,), ('gravel', 1,), ),
    },),
'metal cudgel':({
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_METAL,5,), (SKL_WOOD,5,),),
    'sound'     : 120,
    'construct' : 50,
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
    'using'     : (),
    'byproducts': ( ('parcel of metal', 1,), ),
    },),

    # clubs
'bone heavy club':({
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_BONE,10,),),
    'sound'     : 60,
    'construct' : 40,
    'components': (
        [ ('bone, large', 1,), ],
        ),
    'tools'     : ( [(cmp.Tool_Hammer, 2),], [(cmp.Tool_Chisel, 3),], ),
    'using'     : (),
    'byproducts': ( ('shard of bone', 4,), ('scrap bone', 1,), ),
    },),


    # warhammers
'plastic warhammer':({ # hammer level 2
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_PLASTIC,10,),),
    'sound'     : 60,
    'construct' : 20,
    'components': (
        [ ('piece of plastic', 1,), ],
        [ ('stick of plastic', 1,), ('stick of wood', 1,), ],
        [ ('cordage', 2,), ('glue', 3,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 1,), ],
        [ (cmp.Tool_Chisel, 1,), ],
        ),
    'using'     : (),
    'byproducts': ( ('parcel of plastic', 2,), ('scrap plastic', 1,), ),
    },),
'wooden warhammer':({ # hammer level 2
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_WOOD,10,),),
    'sound'     : 60,
    'construct' : 32,
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
    'using'     : (),
    'byproducts': ( ('parcel of wood', 1,), ('scrap wood', 1,), ),
    },),
'stone warhammer':({ # hammer level 2
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_STONE,10,),),
    'sound'     : 60,
    'construct' : 48,
    'components': (
        [ ('piece of stone', 1,), ],
        [ ('stick of plastic', 1,), ('stick of wood', 1,), ],
        [ ('cordage', 2,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 2,), ],
        [ (cmp.Tool_Chisel, 2,), ],
        ),
    'using'     : (),
    'byproducts': ( ('parcel of stone', 2,), ('gravel', 1,), ),
    },),
'bone warhammer':({ # hammer level 2
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_BONE,10,),),
    'sound'     : 60,
    'construct' : 64,
    'components': (
        [ ('piece of bone', 1,), ],
        [ ('stick of plastic', 1,), ('stick of wood', 1,), ],
        [ ('cordage', 3,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Hammer, 1,), ],
        [ (cmp.Tool_Chisel, 2,), ],
        ),
    'using'     : (),
    'byproducts': ( ('scrap bone', 1,), ('scrap wood', 1,), ),
    },),
'metal warhammer':({ # hammer level 3
    'quantity'  : 1,
    'table'     : CRT_WEAPONS,
    'skills'    : ((SKL_METAL,10,),),
    'sound'     : 120,
    'construct' : 108,
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
    'using'     : (),
    'byproducts': ( ('scrap wood', 1,), ),
    },),







    #--------------------------#
    #      Ranged Weapons      #
    #--------------------------#



    # bows
'plastic bow':({
    'quantity'  : 1,
    'table'     : CRT_RANGED,
    'skills'    : ((SKL_PLASTIC,6,),),
    'construct' : 48,
    'components': (
        [ ('plastic pipe', 1,), ],
        [ ('cordage', 2,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Cut, 3,), ],
        [ (cmp.Tool_Furnace, 1,), ],
        ),
    'using'     : (),
    'byproducts': (),
    },),
'wooden bow':({
    'quantity'  : 1,
    'table'     : CRT_RANGED,
    'skills'    : ((SKL_BOWYER,10,), (SKL_WOOD,5,),),
    'construct' : 96, # should we have a requirement for wetting the wood first?
    'components': (
        [ ('stick of wood', 1,), ],
        [ ('cordage', 2,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Cut, 4,), ],
        [ (cmp.Tool_Chop, 2,), ],
        ),
    'using'     : (),
    'byproducts': (),
    },),
'wooden longbow':({
    'quantity'  : 1,
    'table'     : CRT_RANGED,
    'skills'    : ((SKL_BOWYER,20,), (SKL_WOOD,15,),),
    'construct' : 120,
    'components': (
        [ ('pole of wood', 1,), ],
        [ ('cordage', 3,), ],
        ),
    'tools'     : (
        [ (cmp.Tool_Cut, 4,), ],
        [ (cmp.Tool_Chop, 2,), ],
        ),
    'using'     : (),
    'byproducts': (),
    },),
'unfinished composite bow':({ # note: must dry to finish (takes a long time).
    #Note: must wax (or grease?) bow to give it resistance to water
    'quantity'  : 1,
    'table'     : CRT_RANGED,
    'skills'    : ((SKL_BOWYER,40,), (SKL_WOOD,5), (SKL_BONE,10),),
    'construct' : 272,
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
    'using'     : (),
    'byproducts': (),
    },),

    # caplock guns
'caplock pistol':({
    'quantity'  : 1,
    'table'     : CRT_RANGED,
    'skills'    : ((SKL_GUNSMITH,10,),),
    'construct' : 48,
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
    'using'     : (),
    'byproducts': (),
    },),
'caplock musketoon':({ # short musket. Regular sized barrel. Fat barreled musketoons existed, too, and should maybe be another item.
    'quantity'  : 1,
    'table'     : CRT_RANGED,
    'skills'    : ((SKL_GUNSMITH,8,),),
    'construct' : 72,
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
    'using'     : (),
    'byproducts': (),
    },),
'caplock musket':({
    'quantity'  : 1,
    'table'     : CRT_RANGED,
    'skills'    : ((SKL_GUNSMITH,6,),),
    'construct' : 96,
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
    'using'     : (),
    'byproducts': (),
    },),

}
# end RECIPES





# other recipes that might should be handled differently or just not used


##'pipe gun':({ # shoots larger shots than musketoon/pistol/musket. 
##    'quantity'  : 1,
##    'table'     : CRT_RANGED,
##    'category'  : CRC_GUNSMITH,
##    'construct' : 48,
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
##    },),



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
##'parcel of plastic':({
##    'quantity'  : 1,
##    'table'     : CRT_RAWMATS,
##    'category'  : CRC_BREAKINGDOWN,
##    'construct' : 1,
##    'destruct'  : 0,
##    'components': (
##        [ ('plastic cup', 1,), ],
##        ),
##    'tools'     : (
##        ( (CUTS, 1,), ),
##        ),
##    'byproducts': (),
##    'recycling' : (),
##    },),
##
##'piece of plastic':({
##    'quantity'  : 1,
##    'table'     : CRT_RAWMATS,
##    'category'  : CRC_BREAKINGDOWN,
##    'construct' : 1,
##    'destruct'  : 0,
##    'components': (
##        [ ('plastic stick', 1,), ('plastic bottle', 1,), ],
##        ),
##    'tools'     : (
##        ( (CUTS, 5,), ),
##        ),
##    'byproducts': (),
##    'recycling' : (),
##    },),
##
##'parcel of wood':({
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
##    },),
##
##'piece of wood':({
##    'quantity'  : 1,
##    'table'     : CRT_RAWMATS,
##    'category'  : CRC_BREAKINGDOWN,
##    'construct' : 1,
##    'destruct'  : 0,
##    'components': (
##        [ ('wooden stick', 1,), ],
##        ),
##    'tools'     : (
##        ( (CHOPS, 5,), ),
##        ),
##    'byproducts': ( ('wooden splinters', 1,), ),
##    'recycling' : (),
##    },),
##
##'chunk of wood':({
##    'quantity'  : 1,
##    'table'     : CRT_RAWMATS,
##    'category'  : CRC_BREAKINGDOWN,
##    'construct' : 3,
##    'destruct'  : 0,
##    'components': (
##        [ ('log', 1,), ],
##        ),
##    'tools'     : (
##        ( (CHOPS, 10,), ),
##        ),
##    'byproducts': ( ('parcel of wood', 3,), ),
##    'recycling' : (),
##    },),
##
