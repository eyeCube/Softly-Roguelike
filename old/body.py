








#--------------------------------------------#
# ~~~~~~~~~~~~~~~~ ROGUE.PY ~~~~~~~~~~~~~~~~ #
#--------------------------------------------#


# damage body part (inflict wound)
def damagebp(bptarget, dmgtype, hitpp):
    '''
        bptarget   BP_ (Body Part) component object instance to damage
        dmgtype    DMGTYPE_ const
        hitpp      1 to 9: damage value -- how high of a priority of
                    status is inflicted? 9 is most severe, 1 least severe.
                    Note not all statuses have up to 9 quality levels.
    '''
        
    # abrasions
    if dmgtype==DMGTYPE_ABRASION:
        cd=cmp.BP_BPPS[type(bptarget)]
        if BPP_SKIN in cd:
            damagebpp(
                bptarget.skin, BPP_SKIN, SKINSTATUSES_ABRASION[hitpp])
            # deep skin abrasions may result in muscle abrasion
            if ( BPP_MUSCLE in cd and
                 bptarget.skin.status >= SKINSTATUS_MAJORABRASION ):
                damagebpp(
                    bptarget.muscle, BPP_MUSCLE, MUSCLESTATUSES_ABRASION[hitpp])
    # burns
    elif dmgtype==DMGTYPE_BURN:
        cd=cmp.BP_BPPS[type(bptarget)]
        if BPP_SKIN in cd:
            damagebpp(
                bptarget.skin, BPP_SKIN, SKINSTATUSES_BURN[hitpp])
            # deep skin burns may result in muscle burns
            if ( BPP_MUSCLE in cd and
                 bptarget.skin.status >= SKINSTATUS_DEEPBURNED ):
                damagebpp(
                    bptarget.muscle, BPP_MUSCLE, MUSCLESTATUSES_BURN[hitpp])
    # lacerations
    elif dmgtype==DMGTYPE_CUT:
        cd=cmp.BP_BPPS[type(bptarget)]
        if BPP_SKIN in cd:
            damagebpp(
                bptarget.skin, BPP_SKIN, SKINSTATUSES_CUT[hitpp])
        if BPP_MUSCLE in cd:
            damagebpp(
                bptarget.muscle, BPP_MUSCLE, MUSCLESTATUSES_CUT[hitpp])
    # puncture wounds
    elif dmgtype==DMGTYPE_PIERCE:
        cd=cmp.BP_BPPS[type(bptarget)]
        if BPP_SKIN in cd:
            damagebpp(
                bptarget.skin, BPP_SKIN, SKINSTATUSES_PUNCTURE[hitpp])
        if BPP_MUSCLE in cd:

            damagebpp(
                bptarget.muscle, BPP_MUSCLE, MUSCLESTATUSES_PUNCTURE[hitpp])
        # organ damage is handled separately.
    # hacking / picking damage
    elif dmgtype==DMGTYPE_HACK:
        cd=cmp.BP_BPPS[type(bptarget)]
        if BPP_SKIN in cd:
            damagebpp(
                bptarget.skin, BPP_SKIN, SKINSTATUS_DEEPCUT)
        if BPP_MUSCLE in cd:
            damagebpp(
                bptarget.muscle, BPP_MUSCLE, MUSCLESTATUS_STRAINED)
        if BPP_BONE in cd:
            damagebpp(
                bptarget.bone, BPP_BONE, BONESTATUSES_BLUNT[hitpp])
    # blunt / crushing damage
    elif dmgtype==DMGTYPE_BLUNT:
        cd=cmp.BP_BPPS[type(bptarget)]
        if BPP_MUSCLE in cd:
            damagebpp(
                bptarget.muscle, BPP_MUSCLE, MUSCLESTATUSES_BLUNT[hitpp])
        if BPP_BONE in cd:
            damagebpp(
                bptarget.bone, BPP_BONE, BONESTATUSES_BLUNT[hitpp])
    # mace-like weapons
    elif dmgtype==DMGTYPE_SPUDS:            
        cd=cmp.BP_BPPS[type(bptarget)]
        if BPP_SKIN in cd:
            damagebpp(
                bptarget.skin, BPP_SKIN, SKINSTATUSES_SPUDS[hitpp])
        if BPP_MUSCLE in cd:
            damagebpp(
                bptarget.muscle, BPP_MUSCLE, MUSCLESTATUSES_BLUNT[hitpp])
        if BPP_BONE in cd:
            damagebpp(
                bptarget.bone, BPP_BONE, BONESTATUSES_BLUNT[hitpp])
    # morning-star like long-spiked weapons
    elif dmgtype==DMGTYPE_SPIKES:
        cd=cmp.BP_BPPS[type(bptarget)]
        if BPP_SKIN in cd:
            damagebpp(
                bptarget.skin, BPP_SKIN, SKINSTATUSES_SPIKES[hitpp])
        if BPP_MUSCLE in cd:
            damagebpp(
                bptarget.muscle, BPP_MUSCLE, MUSCLESTATUSES_BLUNT[hitpp])
        if BPP_BONE in cd:
            damagebpp(
                bptarget.bone, BPP_BONE, BONESTATUSES_BLUNT[hitpp])
# end def

def attackbp(
    attkr:int,bptarget:int,weap:int,dmgIndex:int,skill_type:int,dmgtype=-1
    ):
    ''' entity attkr attacks bp bptarget with weapon weap '''
    world=Rogue.world
    if dmgtype!=-1: # force a damage type
        if (not weap or not world.has_component(weap, cmp.DamageTypeMelee)):
            return False
        compo = world.component_for_entity(weap, cmp.DamageTypeMelee)
        if dmgtype not in compo.types:
            return False
        dmgIndex += compo.types[dmgtype]
    else: # get damage type
        dmgtype = get_dmgtype(attkr,weap,skill_type)
        if (weap and world.has_component(weap, cmp.DamageTypeMelee)):
            compo = world.component_for_entity(weap, cmp.DamageTypeMelee)
            dmgIndex += compo.types[dmgtype]
    # end get damage type
    
    #  TESTING
    print("dmgIndex is ",dmgIndex)
    #
    
    if dmgIndex < 0:
        return False
    
    # deal body damage
    damagebp(bptarget, dmgtype, dmgIndex)
    
    # organ damage (TODO) # how should this be done..?
    # criticals only?
    return True
# end if


# body part piece damage & healing (inflict / remove BPP status)
def curebpp(bpp): #<flags> cure BPP status clear BPP status bpp_clear_status clear_bpp_status clear bpp status bpp clear status
    bpp.status = 0 # revert to normal status
def healbpp(bpp, bpptype, quality=1): #<flags> heal BPP object
    pass #TODO
def damagebpp(bpp, bpptype, status): #<flags> damage BPP object inflict BPP status BPP set status set_bpp_status bpp_set_status bpp set status set bpp status
    '''
        * Try to inflict a status on a BPP (body part piece) object
            (A BPP is a sub-component of a BP (body part)
             such as a muscle, bone, etc.)
        * Possibly inflict a higher level status if the intended status
            and the current status are equal.
        * Do not overwrite higher-priority statuses (the higher the
            integer value of the status constant, the higher priority).
        
        # return whether the BPP was damaged
        # Parameters:
        #   bpp     : the BPP_ component to be damaged
        #   bpptype : BPP_ const
        #   status  : the status you want to set on the BPP --
        #               indicates the type of damage to be dealt
    '''
    # progressive damage:
    # two applications of same status => next status up in priority (if of the same type of damage)
    if bpptype == BPP_MUSCLE:
        if (status == MUSCLESTATUS_SORE and bpp.status == status ):
            bpp.status = MUSCLESTATUS_KNOTTED
            return True
        if (status == MUSCLESTATUS_KNOTTED and bpp.status == status ):
            bpp.status = MUSCLESTATUS_CONTUSION
            return True
        if (status == MUSCLESTATUS_CONTUSION and bpp.status == status ):
            bpp.status = MUSCLESTATUS_STRAINED
            return True
        if (status == MUSCLESTATUS_STRAINED and bpp.status == status ):
            bpp.status = MUSCLESTATUS_TORN
            return True
        if (status == MUSCLESTATUS_TORN and bpp.status == status ):
            bpp.status = MUSCLESTATUS_RIPPED
            return True
        if (status == MUSCLESTATUS_RIPPED and bpp.status == status ):
            bpp.status = MUSCLESTATUS_RUPTURED
            return True
        if (status == MUSCLESTATUS_RUPTURED and bpp.status == status ):
            bpp.status = MUSCLESTATUS_MANGLED
            return True
    elif bpptype == BPP_BONE:
        if (status == BONESTATUS_DAMAGED and bpp.status == status ):
            bpp.status = BONESTATUS_FRACTURED
            return True
        if (status == BONESTATUS_FRACTURED and bpp.status == status ):
            bpp.status = BONESTATUS_CRACKED
            return True
        if (status == BONESTATUS_CRACKED and bpp.status == status ):
            bpp.status = BONESTATUS_BROKEN
            return True
        if (status == BONESTATUS_BROKEN and bpp.status == status ):
            bpp.status = BONESTATUS_MULTIBREAKS
            return True
        if (status == BONESTATUS_MULTIBREAKS and bpp.status == status ):
            bpp.status = BONESTATUS_SHATTERED
            return True
        if (status == BONESTATUS_SHATTERED and bpp.status == status ):
            bpp.status = BONESTATUS_MANGLED
            return True
    elif bpptype == BPP_SKIN:
        if (status == SKINSTATUS_RASH and bpp.status == status ):
            bpp.status = SKINSTATUS_BLISTER
            return True
        if (status == SKINSTATUS_BLISTER and bpp.status == status ):
            bpp.status = SKINSTATUS_SCRAPED
            return True
        if (status == SKINSTATUS_SCRAPED and bpp.status == status ):
            bpp.status = SKINSTATUS_MINORABRASION
            return True
        if (status == SKINSTATUS_MINORABRASION and bpp.status == status ):
            bpp.status = SKINSTATUS_MAJORABRASION
            return True
        if (status == SKINSTATUS_MAJORABRASION and bpp.status == status ):
            bpp.status = SKINSTATUS_SKINNED
            return True
        if (status == SKINSTATUS_SKINNED and bpp.status == status ):
            bpp.status = SKINSTATUS_FULLYSKINNED
            return True
        if (status == SKINSTATUS_FULLYSKINNED and bpp.status == status ):
            bpp.status = SKINSTATUS_MANGLED
            return True
        if (status == SKINSTATUS_BURNED and bpp.status == status ):
            bpp.status = SKINSTATUS_DEEPBURNED
            return True
        if (status == SKINSTATUS_DEEPBURNED and bpp.status == status ):
            bpp.status = SKINSTATUS_MANGLED
            return True
        if (status == SKINSTATUS_CUT and bpp.status == status ):
            bpp.status = SKINSTATUS_DEEPCUT
            return True
        if (status == SKINSTATUS_DEEPCUT and bpp.status == status ):
            bpp.status = SKINSTATUS_MULTIDEEPCUTS
            return True
        if (status == SKINSTATUS_MULTIDEEPCUTS and bpp.status == status ):
            bpp.status = SKINSTATUS_MANGLED
            return True
    
    # default
    if bpp.status >= status: 
        return False # don't overwrite lower priority statuses.
    # do exactly what the parameters intended
    bpp.status = status # just set the status
    return True
# end def




#--------------------------------------------#
# ~~~~~~~~~~~~~~ ENTITIES.PY ~~~~~~~~~~~~~~~ #
#--------------------------------------------#


# arm
def _update_from_bp_arm(ent, arm, armorSkill, unarmored):
    world = rog.world()
    dadd={}
    dmul={}
    eqdadd={}
    eqdmul={}
    
    cov = getcov(BP_ARM)
    
    # equipment
    slot = arm.slot
    if slot.item:
        item=slot.item
        equipable=world.component_for_entity(item, cmp.EquipableInArmSlot)
        
        eqdadd=get_addmods(world,item,equipable)
        
        armor_skillBonus(world,item,eqdadd,armorSkill,unarmored,cov)

        fittedBonus(world,slot,eqdadd)
        
        apply_penalties_armor(eqdadd, item)
        
        equip=__EQ(
            eqdadd['enc'], equipable.strReq, 0,
            eqdadd, eqdmul,
            BP_ARM
            )
    else: # unarmored combat
        equip=None
        _apply_skillBonus_unarmored(dadd, unarmored, cov)
        
    # examine body part
    if arm.bone.status:
        _add(dadd, ADDMODS_BPP_ARM_BONESTATUS.get(arm.bone.status, {}))
    if arm.muscle.status:
        _add(dadd, ADDMODS_BPP_ARM_MUSCLESTATUS.get(arm.muscle.status, {}))
    if arm.skin.status:
        _add(dadd, ADDMODS_BPP_SKINSTATUS.get(arm.skin.status, {}))
    return __BPS(dadd,dmul, equip)
# end def

# hand
def _update_from_bp_hand(ent, hand, armorSkill, unarmored,
                         ismainhand=False, twoh=False,offw=False):
    ''' ismainhand: True if this is the dominant arm's hand.
        twoh: True if the weapon wielded in this hand is a two-handed weapon.
        offw: (if ismainhand) True if the respective offhand is holding something; False if it's free to assist the dominant hand.
    '''
    world = rog.world()
    dadd={}
    dmul={}
    eqdadd={}
    eqdmul={}
    
    cov = getcov(BP_HAND)
    
    skillsCompo=world.component_for_entity(ent, cmp.Skills)
    
    # equipment
    
    # armor
    slot = hand.slot
    if slot.item:
        item=slot.item
        equipable=world.component_for_entity(item, cmp.EquipableInHandSlot)
        
        eqdadd=get_addmods(world,item,equipable)
        
        armor_skillBonus(world,item,eqdadd,armorSkill,unarmored,cov)

        fittedBonus(world,slot,eqdadd)
        
        apply_penalties_armor(eqdadd, item)
        
        equip=__EQ(
            eqdadd['enc'], equipable.strReq, 0,
            eqdadd, eqdmul,
            BP_HAND
            )
    else: # unarmored combat
        equip=None
        _apply_skillBonus_unarmored(dadd, unarmored, cov)
    
    # held item (weapon)
    slot = hand.held
    if slot.item:
        item=slot.item
        weapClass=None
        equipable=world.component_for_entity(item, cmp.EquipableInHoldSlot)
        
        eqdadd=get_addmods(world,item,equipable)
        
        # weapon skill bonus for item-weapons (armed combat)
        if world.has_component(item, cmp.WeaponSkill):
            weapClass=world.component_for_entity(item, cmp.WeaponSkill).skill
            skillLv = rog._getskill(skillsCompo.skills.get(weapClass, 0))
            if skillLv in COMBATSKILLS:
                combatLv = rog._getskill(skillsCompo.skills.get(SKL_COMBAT, 0))
            elif skillLv in RANGEDSKILLS:
                rangedLv = rog._getskill(skillsCompo.skills.get(SKL_RANGED, 0))
            if ( (ismainhand and skillLv and weapClass!=SKL_SHIELDS)
                 or (not ismainhand and skillLv and weapClass==SKL_SHIELDS)
                 ):
                _apply_skillBonus_weapon(eqdadd, skillLv, weapClass)
                _apply_skillBonus_weapon(eqdadd, combatLv, SKL_COMBAT)
                _apply_skillBonus_weapon(eqdadd, rangedLv, SKL_RANGED)
        # end if
        
        fittedBonus(world,slot,eqdadd)
        
        # mainhand / offhand - specific stats
        if ismainhand:
            pass
        else: # offhand
            # offhand offensive penalty for offhand weapons
            eqdadd['reach'] = 0
            eqdadd['atk'] = 0
            eqdadd['dmg'] = 0
            eqdadd['pen'] = 0
            eqdadd['asp'] = 0
            eqdadd['gra'] = eqdadd.get('gra', 0) + OFFHAND_PENALTY_GRA
        # end if
        
        # defensive penalty for offhand (non-shield) weapons
        #   AND for shields held in mainhand.          
        if ( (not ismainhand and weapClass != SKL_SHIELDS) or
             (ismainhand and weapClass == SKL_SHIELDS) ):
            eqdadd['dfn'] = eqdadd.get('dfn', 0) * OFFHAND_PENALTY_DFNMOD
            eqdadd['arm'] = eqdadd.get('arm', 0) * OFFHAND_PENALTY_ARMMOD
            eqdadd['pro'] = eqdadd.get('pro', 0) * OFFHAND_PENALTY_PROMOD
        # end if
        
        # two-handed penalties and bonuses
        strReq = equipable.strReq
        if ismainhand: #(TODO: TEST ALL OF THIS (MOVED))
            # check for two-handed bonus to 1-h weapons
            if ( not twoh and not offw ):
                # TODO: apply MULT_2HANDBONUS_STAMINA in combat
                # adders
                eqdadd['atk'] = eqdadd.get('atk',0) + MOD_2HANDBONUS_ATK*MULT_STATS
                eqdadd['pen'] = eqdadd.get('pen',0) + MOD_2HANDBONUS_PEN*MULT_STATS
                eqdadd['dfn'] = eqdadd.get('dfn',0) + MOD_2HANDBONUS_DFN*MULT_STATS
                eqdadd['arm'] = eqdadd.get('arm',0) + MOD_2HANDBONUS_ARM*MULT_STATS
                eqdadd['pro'] = eqdadd.get('pro',0) + MOD_2HANDBONUS_PRO*MULT_STATS
                # multipliers
                strReq = round(strReq * MULT_2HANDBONUS_STRREQ)
                eqdadd['reach'] = eqdadd.get('reach',1) * MULT_2HANDPENALTY_REACH
                eqdadd['asp'] = eqdadd.get('asp',1) * MULT_2HANDBONUS_ASP
                eqdadd['dmg'] = eqdadd.get('dmg',1) * MULT_2HANDBONUS_DMG
            # check for penalty for wielding 2-h weapon in one hand
            elif ( twoh and offw ):
                # adders
                eqdadd['atk'] = eqdadd.get('atk',0) + MOD_1HANDPENALTY_ATK*MULT_STATS
                eqdadd['asp'] = eqdadd.get('asp',0) + MOD_1HANDPENALTY_ASP
                eqdadd['dfn'] = eqdadd.get('dfn',0) + MOD_1HANDPENALTY_DFN*MULT_STATS
                eqdadd['arm'] = eqdadd.get('arm',0) + MOD_1HANDPENALTY_ARM*MULT_STATS
                eqdadd['pro'] = eqdadd.get('pro',0) + MOD_1HANDPENALTY_PRO*MULT_STATS
                eqdadd['pen'] = eqdadd.get('pen',0) + MOD_1HANDPENALTY_PEN*MULT_STATS
                # multipliers
                strReq = rog.ceil(strReq * MULT_1HANDPENALTY_STRREQ)
                eqdadd['reach'] = eqdadd.get('reach',1) * MULT_1HANDBONUS_REACH
        # end if
        
        apply_penalties_weapon(eqdadd, item)
        
        # armed wrestling still grants you some Gra, but significantly
        #   less than if you were unarmed.
        wreLv = rog._getskill(skillsCompo.skills.get(SKL_WRESTLING, 0))
        wreLv = wreLv // 3 # penalty to effective skill Lv
        if not ismainhand:
            wreLv = wreLv * 0.5 # penalty for offhand
        _apply_skillBonus_weapon(eqdadd, wreLv, SKL_WRESTLING, enc=False)
        
        wield=__EQ(
            eqdadd['enc'], strReq, equipable.dexReq,
            eqdadd, eqdmul,
            BP_HAND, twoh=rog.on(item, 'TWOHANDS'),
            )
    else: # unarmed combat
        wield=None
        if ismainhand:
            _boxm = 0.6666667
            _wrem = 0.6666667
            _comm = 0.6666667
        else: # offhand
            _boxm = 0.3333334
            _wrem = 0.3333334
            _comm = 0.3333334
        # unarmed combat (hand-to-hand combat)
        boxLv = rog._getskill(skillsCompo.skills.get(SKL_BOXING, 0))
        boxLv = boxLv * _boxm
        _apply_skillBonus_weapon(dadd, boxLv, SKL_BOXING, enc=False)
        # wrestling unarmed
        wreLv = rog._getskill(skillsCompo.skills.get(SKL_WRESTLING, 0))
        wreLv = wreLv * _wrem
        _apply_skillBonus_weapon(dadd, wreLv, SKL_WRESTLING, enc=False)
        # melee combat skill bonus
        combatLv = rog._getskill(skillsCompo.skills.get(SKL_COMBAT, 0))
        combatLv = combatLv * _comm
        _apply_skillBonus_weapon(eqdadd, combatLv, SKL_COMBAT, enc=False)
    # end if
        
    # examine body part
    if hand.bone.status:
        _add(dadd, ADDMODS_BPP_HAND_BONESTATUS.get(hand.bone.status, {}))
    if hand.muscle.status:
        _add(dadd, ADDMODS_BPP_HAND_MUSCLESTATUS.get(hand.muscle.status, {}))
    if hand.skin.status:
        _add(dadd, ADDMODS_BPP_HAND_SKINSTATUS.get(hand.skin.status, {}))
    return __BPS(dadd,dmul, equip, wield=wield, limbweapon=hand.weapon)
# end def

# leg
def _update_from_bp_leg(ent, leg, armorSkill, unarmored):
    world = rog.world()
    dadd={}
    dmul={}
    eqdadd={}
    eqdmul={}
    
    cov = getcov(BP_LEG)
    
    # equipment
    slot = leg.slot
    if slot.item:
        item=slot.item
        equipable=world.component_for_entity(item, cmp.EquipableInLegSlot)
        
        eqdadd=get_addmods(world,item,equipable)
        
        armor_skillBonus(world,item,eqdadd,armorSkill,unarmored,cov)

        fittedBonus(world,slot,eqdadd)
        
        apply_penalties_armor(eqdadd, item)
        
        equip=__EQ(
            eqdadd['enc'], equipable.strReq, 0,
            eqdadd, eqdmul,
            BP_LEG
            )
                                
    else: # unarmored combat
        equip=None
        _apply_skillBonus_unarmored(dadd, unarmored, cov)
        
    # examine body part
    if leg.bone.status:
        _add(dadd, ADDMODS_BPP_LEG_BONESTATUS.get(leg.bone.status, {}))
        _mult(dmul, MULTMODS_BPP_LEG_BONESTATUS.get(leg.bone.status, {}))
    if leg.muscle.status:
        _add(dadd, ADDMODS_BPP_LEG_MUSCLESTATUS.get(leg.muscle.status, {}))
    if leg.skin.status:
        _add(dadd, ADDMODS_BPP_SKINSTATUS.get(leg.skin.status, {}))
    return __BPS(dadd,dmul, equip)
# end def

# foot
def _update_from_bp_foot(ent, foot, armorSkill, unarmored):
    world = rog.world()
    dadd={}
    dmul={}
    eqdadd={}
    eqdmul={}

    # equipment
    slot = foot.slot
    if slot.item:
        item=slot.item
        equipable=world.component_for_entity(item, cmp.EquipableInFootSlot)
        
        eqdadd=get_addmods(world,item,equipable)

        fittedBonus(world,slot,eqdadd)
        
        apply_penalties_armor(eqdadd, item)
        
        equip=__EQ(
            eqdadd['enc'], equipable.strReq, 0,
            eqdadd, eqdmul,
            BP_FOOT
            )
    else:
        equip=None
        
    # examine body part
    if foot.bone.status:
        _add(dadd, ADDMODS_BPP_LEG_BONESTATUS.get(foot.bone.status, {}))
        _mult(dmul, MULTMODS_BPP_LEG_BONESTATUS.get(foot.bone.status, {}))
    if foot.muscle.status:
        _add(dadd, ADDMODS_BPP_LEG_MUSCLESTATUS.get(foot.muscle.status, {}))
    if foot.skin.status:
        _add(dadd, ADDMODS_BPP_SKINSTATUS.get(foot.skin.status, {}))
    return __BPS(dadd,dmul, equip)
# end def

# head  
def _update_from_bp_head(ent, head, armorSkill, unarmored):
    world = rog.world()
    dadd={}
    dmul={}
    eqdadd={}
    eqdmul={}
    
    cov = getcov(BP_HEAD)
    
    # equipment
    slot = head.slot
    if slot.item:
        item=slot.item
        equipable=world.component_for_entity(item, cmp.EquipableInHeadSlot)
        
        eqdadd=get_addmods(world,item,equipable)
        
        # automatically convert the sight and hearing modifiers
        #  into multipliers for headwear, facewear, eye/earwear, etc.
        if 'sight' in eqdadd.keys(): # sense mod acts as multiplier not adder
            dmul['sight'] = eqdadd['sight']
            del eqdadd['sight']
        if 'hearing' in eqdadd.keys(): # sense mod acts as multiplier not adder
            dmul['hearing'] = eqdadd['hearing']
            del eqdadd['hearing']
        
        armor_skillBonus(world,item,eqdadd,armorSkill,unarmored,cov)

        fittedBonus(world,slot,eqdadd)
        
        apply_penalties_armor(eqdadd, item)
        
        equip=__EQ(
            eqdadd['enc'], equipable.strReq, 0,
            eqdadd, eqdmul,
            BP_HEAD
            )
                                
    else: # unarmored combat
        equip=None
        _apply_skillBonus_unarmored(dadd, unarmored, cov)
    
    # examine body part                
    if head.bone.status: # skull
        _add(dadd, ADDMODS_BPP_HEAD_BONESTATUS.get(head.bone.status, {}))
        _mult(dmul, MULTMODS_BPP_HEAD_BONESTATUS.get(head.bone.status, {}))
    if head.brain.status: # brain
        _add(dadd, ADDMODS_BPP_BRAINSTATUS.get(head.brain.status, {}))
        _mult(dmul, MULTMODS_BPP_BRAINSTATUS.get(head.brain.status, {}))
    if head.skin.status: # scalp
        _add(dadd, ADDMODS_BPP_SKINSTATUS.get(head.skin.status, {}))
    return __BPS(dadd,dmul, equip)
# end def

# face
def _update_from_bp_face(ent, face, armorSkill, unarmored):
    world = rog.world()
    dadd={}
    dmul={}
    eqdadd={}
    eqdmul={}

    # equipment
    slot = face.slot
    if slot.item:
        item=slot.item
        equipable=world.component_for_entity(item, cmp.EquipableInFaceSlot)
        
        eqdadd=get_addmods(world,item,equipable)
        
        if 'sight' in eqdadd.keys(): # sense mod acts as multiplier not adder
            dmul['sight'] = eqdadd['sight']
            del eqdadd['sight']
        
        fittedBonus(world,slot,eqdadd)
        
        apply_penalties_armor(eqdadd, item)
        
        equip=__EQ(
            eqdadd['enc'], equipable.strReq, 0,
            eqdadd, eqdmul,
            BP_FACE
            )
    else:
        equip=None
        
    # examine body part
    if face.skin.status:
        _add(dadd, ADDMODS_BPP_FACE_SKINSTATUS.get(face.skin.status, {}))
    dadd['bea'] = dadd.get('bea', 0) + face.features.beauty
    dadd['idn']  = dadd.get('idn', 0) + face.features.scary
    return __BPS(dadd,dmul, equip)
# end def

# neck
def _update_from_bp_neck(ent, neck, armorSkill, unarmored):
    world = rog.world()
    dadd={}
    dmul={}
    eqdadd={}
    eqdmul={}

    # equipment
    slot = neck.slot
    if slot.item:
        item=slot.item
        equipable=world.component_for_entity(item, cmp.EquipableInNeckSlot)
        
        eqdadd=get_addmods(world,item,equipable)

        fittedBonus(world,slot,eqdadd)
        
        apply_penalties_armor(eqdadd, item)
        
        equip=__EQ(
            eqdadd['enc'], equipable.strReq, 0,
            eqdadd, eqdmul,
            BP_NECK
            )
    else:
        equip=None
        
    # examine body part
    if neck.skin.status:
        _add(dadd, ADDMODS_BPP_SKINSTATUS.get(neck.skin.status, {}))
    if neck.muscle.status:
        _add(dadd, ADDMODS_BPP_NECK_MUSCLESTATUS.get(neck.muscle.status, {}))
    if neck.bone.status:
        _add(dadd, ADDMODS_BPP_NECK_BONESTATUS.get(neck.bone.status, {}))
        _mult(dmul, MULTMODS_BPP_NECK_BONESTATUS.get(neck.bone.status, {}))
    return __BPS(dadd,dmul, equip)
# end def

# eyes
def _update_from_bp_eyes(ent, eyes, armorSkill, unarmored):
    world = rog.world()
    dadd={}
    dmul={}
    eqdadd={}
    eqdmul={}

    # equipment
    slot = eyes.slot
    if slot.item:
        item=slot.item
        equipable=world.component_for_entity(item, cmp.EquipableInEyesSlot)
        
        eqdadd=get_addmods(world,item,equipable)
        
        if 'sight' in eqdadd.keys(): # sense mod acts as multiplier not adder
            dmul['sight'] = eqdadd['sight']
            del eqdadd['sight']
        
        fittedBonus(world,slot,eqdadd)
        
        apply_penalties_armor(eqdadd, item)
        
        equip=__EQ(
            eqdadd['enc'], equipable.strReq, 0,
            eqdadd, eqdmul,
            BP_EYES
            )
    else:
        equip=None
        
    # examine body part
        # if eyes are open, add sight from eyes
    if (not rog.get_status(ent, cmp.StatusBlink) and eyes.open):
        dadd['sight'] = dadd.get('sight', 0) + eyes.visualSystem.quality
    return __BPS(dadd,dmul, equip)
# end def

# ears
def _update_from_bp_ears(ent, ears, armorSkill, unarmored):
    world = rog.world()
    dadd={}
    dmul={}
    eqdadd={}
    eqdmul={}
    # equipment (earplugs, earbuds, etc.)
    slot = ears.slot
    if slot.item:
        item=slot.item
        equipable=world.component_for_entity(item, cmp.EquipableInEarsSlot)
        
        eqdadd=get_addmods(world,item,equipable)
        
        if 'hearing' in eqdadd.keys(): # sense mod acts as multiplier not adder
            dmul['hearing'] = eqdadd['hearing']
            del eqdadd['hearing']
        
        fittedBonus(world,slot,eqdadd)
        
        apply_penalties_armor(eqdadd, item)
        
        equip=__EQ(
            eqdadd['enc'], equipable.strReq, 0,
            eqdadd, eqdmul,
            BP_EARS
            )
    else:
        equip=None
        
    # examine body part
    dadd['hearing'] = dadd.get('hearing', 0) + ears.auditorySystem.quality
    return __BPS(dadd,dmul, equip)
# end def

# nose
def _update_from_bp_nose(ent, nose, armorSkill, unarmored):
    dadd={}
    dmul={}
    eqdadd={}
    eqdmul={}
    # examine body part
    if nose.bone.status:
        _add(dadd, ADDMODS_BPP_FACE_BONESTATUS.get(mouth.bone.status, {}))
    return __BPS(dadd,dmul)
# end def

# mouth
def _update_from_bp_mouth(ent, mouth, armorSkill, unarmored):
    dadd={}
    dmul={}
    eqdadd={}
    eqdmul={}
    
    # TODO: holding things in the mouth
    
    # examine body part
    if mouth.bone.status:
        _add(dadd, ADDMODS_BPP_FACE_BONESTATUS.get(mouth.bone.status, {}))
    if mouth.muscle.status:
        _add(dadd, ADDMODS_BPP_FACE_MUSCLESTATUS.get(mouth.muscle.status, {}))
    return __BPS(dadd,dmul)
# end def

# torso core
def _update_from_bp_torsoCore(ent, core, armorSkill, unarmored):
    world = rog.world()
    dadd={}
    dmul={}
    eqdadd={}
    eqdmul={}
    
    cov = getcov(BP_CORE)
    
    # equipment
    slot = core.slot
    if slot.item:
        item=slot.item
        equipable=world.component_for_entity(item, cmp.EquipableInCoreSlot)
        
        eqdadd=get_addmods(world,item,equipable)
        
        armor_skillBonus(world,item,eqdadd,armorSkill,unarmored,cov)

        fittedBonus(world,slot,eqdadd)
        
        apply_penalties_armor(eqdadd, item)
        
        equip=__EQ(
            eqdadd['enc'], equipable.strReq, 0,
            eqdadd, eqdmul,
            BP_CORE
            )
                                
    else: # unarmored combat
        equip=None
        _apply_skillBonus_unarmored(dadd, unarmored, cov)
             
    # examine body part
    if core.skin.status:
        _add(dadd, ADDMODS_BPP_SKINSTATUS.get(core.skin.status, {}))
    if core.muscle.status:
        _add(dadd, ADDMODS_BPP_TORSO_MUSCLESTATUS.get(core.muscle.status, {}))
    if core.guts.status:
        _add(dadd, ADDMODS_BPP_GUTSSTATUS.get(core.guts.status, {}))
    return __BPS(dadd,dmul, equip)
# end def

# torso front
def _update_from_bp_torsoFront(ent, front, armorSkill, unarmored):
    world = rog.world()
    dadd={}
    dmul={}
    eqdadd={}
    eqdmul={}
    
    cov = getcov(BP_FRONT)
    cov += 0.1 * len(front.slot.covers)
    
    # equipment
    slot = front.slot
    if slot.item:
        item=slot.item
        equipable=world.component_for_entity(item, cmp.EquipableInFrontSlot)
        
        eqdadd=get_addmods(world,item,equipable)
        
        armor_skillBonus(world,item,eqdadd,armorSkill,unarmored,cov)

        fittedBonus(world,slot,eqdadd)
        
        apply_penalties_armor(eqdadd, item)
        
        equip=__EQ(
            eqdadd['enc'], equipable.strReq, 0,
            eqdadd, eqdmul,
            BP_FRONT
            )
                                
    else: # unarmored combat
        equip=None
        _apply_skillBonus_unarmored(dadd, unarmored, cov)
             
    # examine body part
    if front.skin.status:
        _add(dadd, ADDMODS_BPP_SKINSTATUS.get(front.skin.status, {}))
    if front.muscle.status:
        _add(dadd, ADDMODS_BPP_TORSO_MUSCLESTATUS.get(front.muscle.status, {}))
    if front.bone.status:
        _add(dadd, ADDMODS_BPP_TORSO_BONESTATUS.get(front.bone.status, {}))
        _mult(dmul, MULTMODS_BPP_TORSO_BONESTATUS.get(front.bone.status, {}))
    return __BPS(dadd,dmul, equip)
# end def

# torso back
def _update_from_bp_torsoBack(ent, back, armorSkill, unarmored):
    world = rog.world()
    dadd={}
    dmul={}
    eqdadd={}
    eqdmul={}
    
    cov = getcov(BP_BACK)
    
    # equipment
    slot = back.slot
    if slot.item:
        item=slot.item
        equipable=world.component_for_entity(item, cmp.EquipableInBackSlot)
        
        eqdadd=get_addmods(world,item,equipable)
        
        armor_skillBonus(world,item,eqdadd,armorSkill,unarmored,cov)

        fittedBonus(world,slot,eqdadd)
        
        apply_penalties_armor(eqdadd, item)
        
        equip=__EQ(
            eqdadd['enc'], equipable.strReq, 0,
            eqdadd, eqdmul,
            BP_BACK
            )
                                
    else: # unarmored combat
        equip=None
        _apply_skillBonus_unarmored(dadd, unarmored, cov)
             
    # examine body part
    if back.skin.status:
        _add(dadd, ADDMODS_BPP_SKINSTATUS.get(back.skin.status, {}))
    if back.muscle.status:
        _add(dadd, ADDMODS_BPP_BACK_MUSCLESTATUS.get(back.muscle.status, {}))
    if back.bone.status:
        _add(dadd, ADDMODS_BPP_BACK_BONESTATUS.get(back.bone.status, {}))
        _mult(dmul, MULTMODS_BPP_BACK_BONESTATUS.get(back.bone.status, {}))
    return __BPS(dadd,dmul, equip)
# end def

# hips
def _update_from_bp_hips(ent, hips, armorSkill, unarmored):
    world = rog.world()
    dadd={}
    dmul={}
    eqdadd={}
    eqdmul={}
    
    cov = getcov(BP_HIPS)
    
    # equipment
    slot = hips.slot
    if slot.item:
        item=slot.item
        equipable=world.component_for_entity(item, cmp.EquipableInHipsSlot)
        
        eqdadd=get_addmods(world,item,equipable)
        
        armor_skillBonus(world,item,eqdadd,armorSkill,unarmored,cov)

        fittedBonus(world,slot,eqdadd)
        
        apply_penalties_armor(eqdadd, item)
        
        equip=__EQ(
            eqdadd['enc'], equipable.strReq, 0,
            eqdadd, eqdmul,
            BP_HIPS
            )
                                
    else: # unarmored combat
        equip=None
        _apply_skillBonus_unarmored(dadd, unarmored, cov)
             
    # examine body part
    if hips.skin.status:
        _add(dadd, ADDMODS_BPP_SKINSTATUS.get(hips.skin.status, {}))
    if hips.muscle.status:
        _add(dadd, ADDMODS_BPP_TORSO_MUSCLESTATUS.get(hips.muscle.status, {}))
    if hips.bone.status:
        _add(dadd, ADDMODS_BPP_TORSO_BONESTATUS.get(hips.bone.status, {}))
        _mult(dmul, MULTMODS_BPP_TORSO_BONESTATUS.get(hips.bone.status, {}))
    return __BPS(dadd,dmul, equip)
# end def

# wing
def _update_from_bp_wing(ent, wing, armorSkill, unarmored):
    pass
# end def

# tail
def _update_from_bp_tail(ent, tail, armorSkill, unarmored):
    pass
# end def

# genitals
def _update_from_bp_genitals(ent, wing, armorSkill, unarmored):
    pass
# end def

# tentacle
def _update_from_bp_tentacle(ent, tentacle, armorSkill, unarmored):
    pass
# end def

# pseudopod
def _update_from_bp_pseudopod(ent, pseudopod, armorSkill, unarmored):
    pass
# end def

# ameboid
def _update_from_bp_ameboid(ent, ameboid, armorSkill, unarmored):
    pass
# end def

# appendage
def _update_from_bp_appendage(ent, appendage, armorSkill, unarmored):
    pass
# end def




#--------------------------------------------#
# ~~~~~~~~~~~~~ COMPONENTS.PY ~~~~~~~~~~~~~~ #
#--------------------------------------------#


    #--------------#
    #     Body     #
    #--------------#

class Slot:
    __slots__=['item','fit','covers','covered']
    def __init__(self, item=None, fit=0, covers=()):
        self.item=item
        self.fit=fit        # how well this item is secured in its slot currently
        self.covers=covers  # tuple of additional component instances
        self.covered=False  # covered by the item in this slot

class Body:
    '''
        contains information about the physical geometrical makeup
            of a multi-part body/entity
    plan        int constant, refers to the type of body
                    e.g. humanoid which has 2 arms, 2 legs, a torso and a head.
    slot        the "About" slot which is for wearing things over your body
    core        the BPC sub-component of the core (where the hearts are)
    parts       dict of all other BPC sub-components {compoClass : instance}
    position    int refers to an int const corresponding to predefined position
    bodyfat     int, total mass of fat in the whole body
    blood       int, total mass of blood in the whole body / bloodMax=maximum
    hydration   int, total mass of water in the whole body / maximum
    satiation   int, units of hunger satisfaction / maximum
    sleep       int, units of sleep satisfaction / maximum
    '''
    __slots__=[
        'plan','slot','covered',
        'core','parts','height','position',
        'blood','bloodMax','bodyfat',
        'hydration','hydrationMax',
        'satiation','satiationMax',
        'fatigue','fatigueMax'
        ]
    def __init__(self, plan, core, parts={}, height=175, blood=0, fat=0, hydration=0, satiation=0, sleep=0):
        self.plan=plan      # int constant
        self.slot=Slot()    # 'about' slot
        self.core=core      # core body component (BPC core)
        self.parts=parts        # dict of BPC objects other than the core
        self.bodyfat=fat        # total mass of body fat : floating point
        self.blood=blood                # mass of blood in the body
        self.bloodMax=blood             #   (7% of total mass of the body for humans)
        self.satiation=satiation        # calories available to the body
        self.satiationMax=satiation  
        self.hydration=hydration        # mass of water in the body != satisfaction of hydration
        self.hydrationMax=hydration  
        self.fatigue=0                  # accrued fatigue (how tired/sleepy you are)
        self.fatigueMax=sleep           # amount of fatigue that results in falling asleep uncontrollably / loss of cognition / hallucinations etc.
        self.height=height              # int = height in centimeters
        self.position=0     # body pos.: standing, crouched, prone, etc.
    # end def
# end class
        
'''
    Body Part Containers (BPC)*
    contain only BP_ / BPM_ objects or lists of BP_ / BPM_ objects
    * this is the high-level objects that are sub-components of
        the Body component
'''
# cores
class BPC_SingleCore: # core=BP_Ameboid()
    __slots__=['core']
    def __init__(self, core):
        self.core=core
class BPC_Torso:
    __slots__=['core','front','back','hips','hearts','lungs','guts']
    def __init__(self):
        self.core=BP_TorsoCore()
        self.front=BP_TorsoFront()
        self.back=BP_TorsoBack()
        self.hips=BP_Hips()
        self.hearts=BPM_Hearts()
        self.lungs=BPM_Lungs()
# others
class BPC_Heads:
    __slots__=['heads']
    def __init__(self, *args):
        self.heads=[]
        for arg in args:
            self.heads.append(arg)
class BPC_Arms:
    __slots__=['arms'] # expected to have at least 2 items. Use None for N/A
    def __init__(self, *args):
        self.arms=[] if args else [None,None,] # None == No arm
        for arg in args: # the arm in slot 0 is dominant. If only one arm exists and it is the off-arm, then it should go in slot 1, and slot 0 should be None.
            self.arms.append(arg)
class BPC_Legs: # see BPC_Arms
    __slots__=['legs']
    def __init__(self, *args):
        self.legs=[] if args else [None,None,]
        for arg in args:
            self.legs.append(arg)
class BPC_Pseudopods:
    __slots__=['pseudopods']
    def __init__(self, *args):
        self.pseudopods=[]
        for arg in args:
            self.pseudopods.append(arg)
class BPC_Wings:
    __slots__=['wings']
    def __init__(self, *args):
        self.wings=[]
        for arg in args:
            self.wings.append(arg)
class BPC_Tails:
    __slots__=['tails']
    def __init__(self, *args):
        self.tails=[]
        for arg in args:
            self.tails.append(arg)
##class BPC_Genitals:
##    __slots__=['genitals']
##    def __init__(self):
##        self.genitals=BP_Genitals()

'''
    Body Parts Meta (BPM)
    contain BP sub-components
    * This is the intermediate level of abstraction which are
        contained in lists in BPC components
'''
class BPM_Head:
    __slots__=['head','neck','face','eyes','ears','nose','mouth']
    def __init__(self):
        self.head=BP_Head()
        self.face=BP_Face()
        self.neck=BP_Neck()
        self.eyes=BP_Eyes()
        self.ears=BP_Ears()
        self.nose=BP_Nose()
        self.mouth=BP_Mouth()
class BPM_Arm:
    __slots__=['hand','arm']
    def __init__(self):
        self.arm=BP_Arm()
        self.hand=BP_Hand()
class BPM_Leg:
    __slots__=['leg','foot']
    def __init__(self):
        self.leg=BP_Leg()
        self.foot=BP_Foot()
class BPM_Lungs:
    __slots__=['lungs']
    def __init__(self):
        self.lungs=[]
class BPM_Hearts:
    __slots__=['hearts']
    def __init__(self):
        self.hearts=[]
       
'''
    Body Parts (BP)
    usually contain a slot, and optional BPP sub-components
    DO NOT have a STATUS
'''
class BP_TorsoCore: # abdomen
    __slots__=['slot','artery','muscle','skin','guts']
    WEAR_TYPE = EQ_CORE
    HOLD_TYPE = EQ_NONE
    def __init__(self):
        self.slot=Slot()
        self.artery=BPP_Artery()
        self.muscle=BPP_Muscle() # abs
        self.skin=BPP_Skin()
        self.guts=BPP_Guts()
class BP_TorsoFront: # thorax front (chest)
    __slots__=['slot','bone','artery','muscle','skin']
    WEAR_TYPE = EQ_FRONT
    HOLD_TYPE = EQ_NONE
    def __init__(self):
        self.slot=Slot()
        self.artery=BPP_Artery()
        self.bone=BPP_Bone() # ribs
        self.muscle=BPP_Muscle() # pecs
        self.skin=BPP_Skin()
class BP_TorsoBack: # thorax back
    __slots__=['slot','bone','artery','muscle','skin']
    WEAR_TYPE = EQ_BACK
    HOLD_TYPE = EQ_NONE
    def __init__(self):
        self.slot=Slot()
        self.artery=BPP_Artery()
        self.bone=BPP_Bone() # spine
        self.muscle=BPP_Muscle()
        self.skin=BPP_Skin()
class BP_Hips: # pelvic region
    __slots__=['slot','bone','artery','muscle','skin']
    WEAR_TYPE = EQ_HIPS
    HOLD_TYPE = EQ_NONE
    def __init__(self):
        self.slot=Slot()
        self.artery=BPP_Artery()
        self.bone=BPP_Bone() # pelvis
        self.muscle=BPP_Muscle()
        self.skin=BPP_Skin()
class BP_Cell:
    __slots__=['slot']
    WEAR_TYPE = EQ_CELL
    HOLD_TYPE = EQ_NONE
    def __init__(self):
        self.slot=Slot()
class BP_Head:
    __slots__=['slot','bone','brain','skin','hair']
    WEAR_TYPE = EQ_MAINHEAD
    HOLD_TYPE = EQ_NONE
    def __init__(self):
        self.slot=Slot()
        self.bone=BPP_Bone() # skull
        self.brain=BPP_Brain()
        self.skin=BPP_Skin()
        self.hair=BPP_Hair()
class BP_Neck:
    __slots__=['slot','artery','bone','muscle','skin']
    WEAR_TYPE = EQ_MAINNECK
    HOLD_TYPE = EQ_NONE
    def __init__(self):
        self.slot=Slot()
        self.bone=BPP_Bone()
        self.artery=BPP_Artery()
        self.muscle=BPP_Muscle()
        self.skin=BPP_Skin()
class BP_Face:
    __slots__=['slot','features','skin']
    WEAR_TYPE = EQ_MAINFACE
    HOLD_TYPE = EQ_NONE
    def __init__(self):
        self.slot=Slot()
        self.features=BPP_FacialFeatures()
        self.skin=BPP_Skin()
class BP_Mouth:
    __slots__=['held','bone','muscle','teeth','gustatorySystem','weapon']
    WEAR_TYPE = EQ_NONE
    HOLD_TYPE = EQ_MAINMOUTH
    def __init__(self, taste=20): # quality of taste system
        self.held=Slot() # grabbed slot (weapon equip, etc.) (TODO: mouth holding / equipping items/weapons)
        self.bone=BPP_Bone()
        self.muscle=BPP_Muscle()
        self.teeth=BPP_Teeth()
        self.weapon=LIMBWPN_TEETH
        self.gustatorySystem=BPP_GustatorySystem(quality=taste)
class BP_Eyes:
    __slots__=['slot','visualSystem','open']
    WEAR_TYPE = EQ_MAINEYES
    HOLD_TYPE = EQ_NONE
    def __init__(self, quantity=2, quality=20): #numEyes; vision;
        self.slot=Slot()        # eyewear for protecting eyes
        self.visualSystem=BPP_VisualSystem(quantity=quantity,quality=quality)
        self.open=True #eyelids open or closed?
class BP_Ears:
    __slots__=['slot','auditorySystem']
    WEAR_TYPE = EQ_MAINEARS
    HOLD_TYPE = EQ_NONE
    def __init__(self, quantity=2, quality=60):
        self.slot=Slot()        # earplugs, for protecting ears
        self.auditorySystem=BPP_AuditorySystem(quantity=quantity,quality=quality)
class BP_Nose:
    __slots__=['bone','olfactorySystem']
    WEAR_TYPE = EQ_NONE
    HOLD_TYPE = EQ_NONE
    def __init__(self, quality=10):
        self.bone=BPP_Bone()
        self.olfactorySystem=BPP_OlfactorySystem(quality=quality)
class BP_Arm: # upper / middle arm and shoulder
    __slots__=['slot','bone','artery','muscle','skin','covered']
    WEAR_TYPE = EQ_MAINARM
    HOLD_TYPE = EQ_NONE
    def __init__(self):
        self.slot=Slot()
        self.artery=BPP_Artery()
        self.bone=BPP_Bone()
        self.muscle=BPP_Muscle()
        self.skin=BPP_Skin()
class BP_Hand: # hand and lower forearm
    __slots__=['slot','held','bone','artery','muscle','skin',
               'grip','weapon']
    WEAR_TYPE = EQ_MAINHAND
    HOLD_TYPE = EQ_MAINHANDW
    def __init__(self, grip=10):
        self.slot=Slot() # armor slot (gloves etc.)
        self.held=Slot() # grabbed slot (weapon equip, etc.)
        self.artery=BPP_Artery()
        self.bone=BPP_Bone()
        self.muscle=BPP_Muscle()
        self.skin=BPP_Skin()
        self.weapon=LIMBWPN_HAND # bare limb damage type w/ no weapon equipped (LIMBWPN_ const)
        self.grip=grip # grip your bare hand has
class BP_Leg: # thigh and knee
    __slots__=['slot','bone','artery','muscle','skin','covered']
    WEAR_TYPE = EQ_MAINLEG
    HOLD_TYPE = EQ_NONE
    def __init__(self):
        self.slot=Slot()
        self.artery=BPP_Artery()
        self.bone=BPP_Bone()
        self.muscle=BPP_Muscle()
        self.skin=BPP_Skin()
        self.covered=False
class BP_Foot: # foot, ankle and lower leg
    __slots__=['slot','bone','artery','muscle','skin','covered','grip']
    WEAR_TYPE = EQ_MAINFOOT
    HOLD_TYPE = EQ_NONE
    def __init__(self, grip=10):
        self.slot=Slot()
        self.artery=BPP_Artery()
        self.bone=BPP_Bone()
        self.muscle=BPP_Muscle()
        self.skin=BPP_Skin()
        self.grip=grip # grip your bare foot has
        self.covered=False
class BP_InsectThorax:
    __slots__=['slot','exoskeleton','muscle','covered']
    WEAR_TYPE = EQ_ITHORAX
    HOLD_TYPE = EQ_NONE
    def __init__(self):
        self.slot=Slot()
        self.muscle=BPP_Muscle()
        self.exoskeleton=BPP_Exoskeleton()
        self.covered=False
class BP_InsectAbdomen:
    __slots__=['slot','exoskeleton','heart','guts','covered']
    WEAR_TYPE = EQ_IABDOMEN
    HOLD_TYPE = EQ_NONE
    def __init__(self):
        self.slot=Slot()
        self.heart=BPP_Heart()
        self.guts=BPP_Guts()
        self.exoskeleton=BPP_Exoskeleton()
        self.covered=False
class BP_InsectHead:
    __slots__=['slot','exoskeleton','brain','antennae','visualSystem',
               'covered']
    WEAR_TYPE = EQ_IHEAD
    HOLD_TYPE = EQ_NONE
    def __init__(self):
        self.slot=Slot()
        self.exoskeleton=BPP_Exoskeleton()
        self.brain=BPP_Brain()
        self.antennae=BPP_Antennae()
        self.visualSystem=BPP_VisualSystem()
        self.covered=False
class BP_Mandible:
    __slots__=['held','exoskeleton','muscle','holding','weapon']
    WEAR_TYPE = EQ_IMANDIBLE
    HOLD_TYPE = EQ_NONE
    def __init__(self):
        self.held=Slot()
        self.exoskeleton=BPP_Exoskeleton()
        self.muscle=BPP_Muscle()
        self.weapon=LIMBWPN_PINCER # bare limb damage type w/ no weapon equipped (LIMBWPN_ const)
        self.holding=False
class BP_InsectLeg:
    __slots__=['slot','exoskeleton','muscle','covered']
    WEAR_TYPE = EQ_IMAINLEG
    HOLD_TYPE = EQ_NONE
    def __init__(self):
        self.slot=Slot()
        self.muscle=BPP_Muscle()
        self.exoskeleton=BPP_Exoskeleton()
        self.covered=False
class BP_Tentacle: # arm and "hand" in one, can grasp things like a hand can
    __slots__=['slot','held','artery','muscle','skin','stickies',
               'covered','holding','weapon']
    WEAR_TYPE = EQ_1TENTACLE
    HOLD_TYPE = EQ_1TENTACLEW
    def __init__(self, stickies=0):
        self.slot=Slot()
        self.held=Slot()
        self.artery=BPP_Artery()
        self.muscle=BPP_Muscle()
        self.skin=BPP_Skin()
        self.weapon=LIMBWPN_TENTACLE # bare limb damage type w/ no weapon equipped (LIMBWPN_ const)
        self.stickies=stickies      # number/quality of suction cups on the tentacles (or other sticky thingies)
        self.covered=False
        self.holding=False
class BP_Pseudopod:
    __slots__=['slot','covered','weapon']
    WEAR_TYPE = EQ_NONE
    HOLD_TYPE = EQ_PSEUDOPOD
    def __init__(self):
        self.slot=Slot()
        self.weapon=LIMBWPN_PSEUDOPOD # bare limb damage type w/ no weapon equipped (LIMBWPN_ const)
        self.covered=False
class BP_Ameboid:
    __slots__=['slot','nucleus','covered']
    WEAR_TYPE = EQ_AMEBOID
    HOLD_TYPE = EQ_NONE
    def __init__(self):
        self.slot=Slot()
        self.nucleus=BPP_Nucleus()
        self.covered=False
class BP_Wing:
    __slots__=['slot','bone','muscle','skin','covered']
    WEAR_TYPE = EQ_MAINWING
    HOLD_TYPE = EQ_NONE
    def __init__(self):
        self.slot=Slot()
        self.bone=BPP_Bone()
        self.muscle=BPP_Muscle()
        self.skin=BPP_Skin()
        self.covered=False
class BP_Tail:
    __slots__=['slot','bone','artery','muscle','skin','covered']
    WEAR_TYPE = EQ_1TAIL
    HOLD_TYPE = EQ_NONE
    def __init__(self):
        self.slot=Slot()
        self.artery=BPP_Artery()
        self.bone=BPP_Bone()
        self.muscle=BPP_Muscle()
        self.skin=BPP_Skin()
        self.covered=False
class BP_Genitals:
    __slots__=['genitals','covered']
    WEAR_TYPE = EQ_GENITALS
    HOLD_TYPE = EQ_NONE
    def __init__(self):
        self.genitals=BPP_Genitals()
        self.covered=False
class BP_Appendage: #worthless appendage (small boneless, musclesless tails, etc.)
    __slots__=['kind','covered']
    WEAR_TYPE = EQ_NONE
    HOLD_TYPE = EQ_NONE
    def __init__(self, kind):
        self.kind=kind # int const referring to a pre-conceived name in a pre-defined dict
        self.covered=False

'''
    Body Parts Piece (BPP)
    piece of body parts, sub-components of BP_ objects
    do NOT contain slots
    contain a STATUS
'''
class BPP_Skin: # 16% of total body mass
    __slots__=['status','material','flags']
    def __init__(self, mat=-1):
        if mat==-1: mat=MAT_FLESH
        self.material=mat
        self.status=0
        self.flags=bytes(0)
class BPP_Hair:
    __slots__=['status','length','flags']
    def __init__(self, length=1):
        self.status=0
        self.length=length
        self.flags=bytes(0)
class BPP_Artery:
    __slots__=['status']
    def __init__(self):
        self.status=0
class BPP_Bone:
    __slots__=['material','status','flags']
    def __init__(self, mat=-1):
        if mat==-1: mat=MAT_BONE
        self.material=mat # determines Strength of the bone
        self.status=0
        self.flags=bytes(0)
class BPP_Exoskeleton:
    __slots__=['material','status']
    def __init__(self, mat=-1):
        if mat==-1: mat=MAT_CHITIN
        self.material=mat
        self.status=0
class BPP_Shell: # chitinous shell
    __slots__=['material','status']
    def __init__(self, mat=-1):
        if mat==-1: mat=MAT_CHITIN
        self.material=mat
        self.status=0
class BPP_Muscle:
    __slots__=['status','str','flags']#,'fatigue','fatigueMax'
    def __init__(self, _str=1000):
        self.str=_str # strength of muscle (as a ratio 0 to 1000?)
        self.status=0
        self.flags=bytes(0)
class BPP_Brain:
    __slots__=['status','quality','flags']
    def __init__(self, quality=1):
        self.status=0
        self.quality=quality
        self.flags=bytes(0)
class BPP_VisualSystem:
    __slots__=['quantity','quality']
    def __init__(self, quantity=2, quality=20):
        self.quantity=quantity
        self.quality=quality    # combined quality of all eyes
class BPP_AuditorySystem:
    __slots__=['quantity','quality']
    def __init__(self, quantity=2, quality=60):
        self.quantity=quantity
        self.quality=quality    # combined quality of all ears
class BPP_OlfactorySystem:
    __slots__=['quality']
    def __init__(self, quality=20):
        self.quality=quality
class BPP_GustatorySystem:
    __slots__=['quality']
    def __init__(self, quality=20):
        self.quality=quality
class BPP_FacialFeatures:
    __slots__=['beauty','scary']
    def __init__(self, beauty=32, scary=32):
        self.beauty=beauty
        self.scary=scary
class BPP_Teeth:
    __slots__=['quantity','quality','material']
    def __init__(self, quantity=26, quality=2, mat=-1):
        if mat==-1: mat=MAT_BONE
        self.quantity=quantity
        self.quality=quality
        self.material=mat
class BPP_Heart:
    __slots__=['status','str']
    def __init__(self, _str=1):
        self.str=_str
        self.status=0
class BPP_Lung:
    __slots__=['status','capacity']
    def __init__(self, cap=1):
        self.capacity=cap
        self.status=0
class BPP_Guts:
    __slots__=['status']
    def __init__(self):
        self.status=0
class BPP_Genitals:
    __slots__=['status']
    def __init__(self):
        self.status=0
class BPP_Nucleus:
    __slots__=['status']
    def __init__(self):
        self.status=0
##        self.dna=(2,1,3, 2,3,1, 0,0,2, 0,0,2, 0,1,1,)
##class BPP_Fat:
##    __slots__=['mass','status']
##    def __init__(self, mass=1):
##        self.mass=mass
##        self.status=0
