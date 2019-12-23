

def _update_stats(ent): # PRIVATE, ONLY TO BE CALLED FROM getms(...)
    '''
        calculate modified stats
            building up from scratch (base stats)
            add any modifiers from equipment, status effects, etc.
        return the Modified Stats component
        after this is called, you can access the Modified Stats component
            and it will contain the right value, until something significant
            updates which would change the calculation, at which point the
            DIRTY_STATS flag for that entity must be set to True.
    '''
    # NOTE: apply all penalties (w/ limits) AFTER bonuses.
        # this is to ensure you don't end up with MORE during a
        #   penalty application; as in the case the value was negative
    world=Rogue.world
    base=world.component_for_entity(ent, cmp.Stats)
    modded=world.component_for_entity(ent, cmp.ModdedStats)
    if world.has_component(ent, cmp.Skills):
        skills=world.component_for_entity(ent, cmp.Skills)
        armorSkill = (skills.skills.get(SKL_ARMOR,0)) # armored skill value
        unarmored = (skills.skills.get(SKL_UNARMORED,0)) # unarmored skill
    else:
        skills=None
        armorSkill = 0
        unarmored = 0
    offhandItem = False
    addMods=[]
    multMods=[]
##    skilledInWeapons=(weap_skill in skills.skills)
    
    # local func for durability penalties (TODO: move all these nested functions and make it global private funcs)
    def append_mods(addMods, multMods, dadd, dmul):
        if dadd:
            addMods.append(dadd)
        if dmul:
            multMods.append(dmul)
    # for adding just 1 mod dict into dadd or dmul
    def _add(dadd, modDict):
        for stat,val in modDict.items():
            dadd[stat] = dadd.get(stat, 0) + val
    def _mult(dmul, modDict):
        for stat,val in modDict.items():
            dmul[stat] = dmul.get(stat, 1) * val
    # ADD DICT MULTIPLIER FUNCTIONS
    def _apply_durabilityPenalty_weapon(dadd, hp, hpMax):
        modf = 1 - (1 - (hp / hpMax))**2
        dadd['asp'] = min(dadd['asp'], dadd['asp'] * (0.75 + 0.25*modf))
        dadd['atk'] = min(dadd['atk'], dadd['atk'] * (0.5 + 0.5*modf))
        dadd['dmg'] = min(dadd['dmg'], dadd['dmg'] * (0.25 + 0.75*modf))
        dadd['pen'] = min(dadd['pen'], dadd['pen'] * modf)
        dadd['pro'] = min(dadd['pro'], dadd['pro'] * modf)
        dadd['arm'] = min(dadd['arm'], dadd['arm'] * (0.25 + 0.75*modf))
        dadd['dfn'] = min(dadd['dfn'], dadd['dfn'] * (0.5 + 0.5*modf))
    def _apply_durabilityPenalty_armor(dadd, hp, hpMax):
        modf = 1 - (1 - (hp / hpMax))**2
        dadd['pro'] = min(dadd['pro'], dadd['pro'] * modf)
        dadd['arm'] = min(dadd['arm'], dadd['arm'] * (0.25 + 0.75*modf))
        dadd['dfn'] = min(dadd['dfn'], dadd['dfn'] * (0.5 + 0.5*modf))

    # BPC
    
    def _update_from_bpc_heads(addMods, multMods, ent, bpc, armorSkill, unarmored):
        # TODO: MOVE elsewhere (outside the scope of this function and probably outside of rogue)
        for bpm in bpc.heads:
            dadd,dmul=_update_from_bp_head(ent, bpm.head, armorSkill, unarmored)
            append_mods(addMods, multMods, dadd, dmul)
            dadd,dmul=_update_from_bp_neck(ent, bpm.neck, armorSkill, unarmored)
            append_mods(addMods, multMods, dadd, dmul)
            dadd,dmul=_update_from_bp_face(ent, bpm.face, armorSkill, unarmored)
            append_mods(addMods, multMods, dadd, dmul)
            dadd,dmul=_update_from_bp_eyes(ent, bpm.eyes, armorSkill, unarmored)
            append_mods(addMods, multMods, dadd, dmul)
            dadd,dmul=_update_from_bp_ears(ent, bpm.ears, armorSkill, unarmored)
            append_mods(addMods, multMods, dadd, dmul)
            dadd,dmul=_update_from_bp_nose(ent, bpm.nose, armorSkill, unarmored)
            append_mods(addMods, multMods, dadd, dmul)
            dadd,dmul=_update_from_bp_mouth(ent, bpm.mouth, armorSkill, unarmored)
            append_mods(addMods, multMods, dadd, dmul)
    def _update_from_bpc_legs(addMods, ent, bpc, armorSkill, unarmored):
        for bpm in bpc.legs:
            dadd,dmul=_update_from_bp_foot(ent, bpm.foot, armorSkill, unarmored)
            append_mods(addMods, multMods, dadd, dmul)
            dadd,dmul=_update_from_bp_leg(ent, bpm.leg, armorSkill, unarmored)
            append_mods(addMods, multMods, dadd, dmul)
    def _update_from_bpc_arms(addMods, ent, bpc, armorSkill, unarmored):
        for bpm in bpc.arms:
            dadd,dmul=_update_from_bp_hand(ent, bpm.hand, armorSkill, unarmored)
            append_mods(addMods, multMods, dadd, dmul)
            dadd,dmul=_update_from_bp_arm(ent, bpm.arm, armorSkill, unarmored)
            append_mods(addMods, multMods, dadd, dmul)

    # BP
            
    def _update_from_bp_head(ent, head, armorSkill, unarmored):
        dadd={}
        dmul={}

        # equipment
        if head.slot.item:
            item=head.slot.item
            hp=rog.getms(item, "hp")
            hpmax=rog.getms(item, "hpmax")
            equipable=world.component_for_entity(item, cmp.EquipableInHeadSlot)
            for k,v in equipable.mods.items(): # collect add modifiers
                dadd.update({k:v})
            
            # bonuses
            # armor skill bonus
            if armorSkill:
                sm=armorSkill*SKILL_EFFECTIVENESS_MULTIPLIER
                dadd['pro'] = dadd.get('pro', 0)*SKLMOD_ARMOR_PRO*sm
                dadd['arm'] = dadd.get('arm', 0)*SKLMOD_ARMOR_AV*sm
                dadd['dfn'] = dadd.get('dfn', 0)*SKLMOD_ARMOR_DV*sm
            
            # penalties
            # durability penalty multiplier for the stats
            _apply_durabilityPenalty_armor(dadd, hp, hpmax)
                                    
        else: # unarmored combat
            if unarmored:
                am=unarmored*SKILL_EFFECTIVENESS_MULTIPLIER
                dadd['pro'] = dadd.get('pro', 0) + SKLMOD_UNARMORED_PRO*sm
                dadd['arm'] = dadd.get('arm', 0) + SKLMOD_UNARMORED_AV*sm
                dadd['dfn'] = dadd.get('dfn', 0) + SKLMOD_UNARMORED_DV*sm
        
        # examine body part
        
# NOTE: status effect of getting hit in the head mimicks sickness
    # also restlessness, headache, speech skill penalty
    # status effect activastes when head hit hard; lasts long time
                
        if head.bone.status:
            _mult(dmul, MULTMODS_BPP_HEAD_BONESTATUS['stats'].get(head.bone.status, {}))
        if head.brain.status:
            _add(dadd, ADDMODS_BPP_BRAINSTATUS['stats'].get(head.brain.status, {}))
            _mult(dmul, MULTMODS_BPP_BRAINSTATUS['stats'].get(head.brain.status, {}))
        if head.skin.status:
            _add(dadd, ADDMODS_BPP_SKINSTATUS['stats'].get(head.skin.status, {}))
        return dadd,dmul
    
    def _update_from_bp_arm(ent, arm, armorSkill, unarmored):
        dadd={}
        dmul={}
        if arm.bone.status:
            _add(dadd, ADDMODS_BPP_ARM_BONESTATUS['stats'].get(arm.bone.status, {}))
        if arm.muscle.status:
            _add(dadd, ADDMODS_BPP_ARM_MUSCLESTATUS['stats'].get(arm.muscle.status, {}))
        if arm.skin.status:
            _add(dadd, ADDMODS_BPP_SKINSTATUS['stats'].get(arm.skin.status, {}))
        return dadd,dmul
    def _update_from_bp_hand(ent, hand, armorSkill, unarmored):
        _update_from_bp_arm(ent, hand, armorSkill, unarmored)
    def _update_from_bp_leg(ent, leg, armorSkill, unarmored):
        dadd={}
        dmul={}
        if leg.bone.status:
            _add(dadd, ADDMODS_BPP_LEG_BONESTATUS['stats'].get(leg.bone.status, {}))
            _mult(dmul, MULTMODS_BPP_LEG_BONESTATUS['stats'].get(leg.bone.status, {}))
        if leg.muscle.status:
            _add(dadd, ADDMODS_BPP_LEG_MUSCLESTATUS['stats'].get(leg.muscle.status, {}))
        if leg.skin.status:
            _add(dadd, ADDMODS_BPP_SKINSTATUS['stats'].get(leg.skin.status, {}))
        return dadd,dmul
    def _update_from_bp_foot(ent, foot, armorSkill, unarmored):
        _update_from_bp_leg(ent, foot, armorSkill, unarmored)
    def _update_from_bp_face(ent, face, armorSkill, unarmored):
        pass
    def _update_from_bp_neck(ent, neck, armorSkill, unarmored):
        pass
    def _update_from_bp_eyes(ent, eyes, armorSkill, unarmored):
        pass
    def _update_from_bp_ears(ent, ears, armorSkill, unarmored):
        pass
    def _update_from_bp_nose(ent, nose, armorSkill, unarmored):
        pass
    def _update_from_bp_mouth(ent, mouth, armorSkill, unarmored):
        pass
        

    # alter stats based on body status / equipped gear
    
    if world.has_component(ent, cmp.Body):
        body=world.component_for_entity(ent, cmp.Body)
    else:
        body=None
    
    if body and False: # TESTTTT!!!!! and False is to make it always false...
        keys = body.parts.keys()
        if cmp.BPC_Heads in keys:
            _update_from_bpc_heads(
                addMods,multMods,
                ent,
                body.parts[cmp.BPC_Heads],
                armorSkill,
                unarmored
                )
        if cmp.BPC_Arms in keys:
            _update_from_bpc_arms(
                addMods,multMods,
                ent,
                body.parts[cmp.BPC_Arms],
                armorSkill,
                unarmored
                )
        if cmp.BPC_Legs in keys:
            _update_from_bpc_legs(
                addMods,multMods,
                ent,
                body.parts[cmp.BPC_Legs],
                armorSkill,
                unarmored
                )
        if cmp.BPC_Pseudopods in keys:
            _update_from_bpc_pseudopods(
                addMods,multMods,
                ent,
                body.parts[cmp.BPC_Pseudopods],
                armorSkill,
                unarmored
                )
        if cmp.BPC_Wings in keys:
            _update_from_bpc_wings(
                addMods,multMods,
                ent,
                body.parts[cmp.BPC_Wings],
                armorSkill,
                unarmored
                )
        if cmp.BPC_Tails in keys:
            _update_from_bpc_tails(
                addMods,multMods,
                ent,
                body.parts[cmp.BPC_Tails],
                armorSkill,
                unarmored
                )
        if cmp.BPC_Genitals in keys:
            _update_from_bpc_genitals(
                addMods,multMods,
                ent,
                body.parts[cmp.BPC_Genitals],
                armorSkill,
                unarmored
                )

    
#-------------------------------------------------------#
# TODO: finish updating all these to the new Body class format!! #
# Switch itemStats to 
##            hp=rog.getms(item, "hp")
##            hpmax=rog.getms(item, "hpmax")
#-------------------------------------------------------#

# THIS IS ALL OBSELETE CODE!!!!!!!!!
    '''
    #
    # armor
    if world.has_component(ent, cmp.EquipArmor):
        compo=world.component_for_entity(ent, cmp.EquipArmor)
        if compo.item:
            item=compo.item
            itemStats=world.component_for_entity(item, cmp.Stats)
            slot=world.component_for_entity(item, cmp.EquipableInArmorSlot)
            dadd={}
            for k,v in slot.mods.items(): # collect add modifiers
                dadd.update({k:v})

            # bonuses
            # armor skill bonus
            if armorSkill:
                dadd['pro'] = dadd['pro']*SKLMOD_ARMOR_PRO
                dadd['arm'] = dadd['arm']*SKLMOD_ARMOR_AV
                dadd['dfn'] = dadd['dfn']*SKLMOD_ARMOR_DV

            # penalties
            # durability penalty
            _apply_durabilityPenalty_armor(dadd, itemStats.hp, itemStats.hpMax)

            addMods.append(dadd)

        else: # unarmored combat
            pass
    #
    # offhand
    if world.has_component(ent, cmp.EquipHand2):
        compo=world.component_for_entity(ent, cmp.EquipHand2)
        if compo.item:
            offhandItem = True
            item=compo.item
            itemStats=world.component_for_entity(item, cmp.Stats)
            slot=world.component_for_entity(item, cmp.EquipableInHandSlot)
            dadd={}
            for k,v in slot.mods.items(): # collect add modifiers
                dadd.update({k:v})

            # bonuses

            # weapon skill bonus
            if world.has_component(item, cmp.WeaponSkill):
                weaponSkill=world.component_for_entity(item, cmp.WeaponSkill)
                if weaponSkill.skill in skills.skills:
                    skill=weaponSkill.skill # THIS IS OBSELETE W/ NUMBERED SKILL SYSTEM
                    statdata=SKILL_WEAPSTATDATA[skill]
                    for _var, _modf in statdata:
                        dadd[_var] = dadd[_var] + _modf

            # penalties

            # durability penalty
            _apply_durabilityPenalty_weapon(dadd, itemStats.hp, itemStats.hpMax)
            
            # offhand penalty
            dadd['atk'] = 0
            dadd['dmg'] = 0
            dadd['pen'] = 0
            dadd['asp'] = 0
            # penalty to defensive capability
            #   applies to all weapons except shields and knives
            if ( weaponsSkill==SKL_SHIELDS
                 or weaponSkill==SKL_KNIVES ):
                pass
            else:
                dadd['dfn'] = min( dadd['dfn'],
                    dadd['dfn'] * OFFHAND_PENALTY_DFN )
                dadd['arm'] = min( dadd['arm'],
                    dadd['arm'] * OFFHAND_PENALTY_ARM )
                dadd['pro'] = min( dadd['pro'],
                    dadd['pro'] * OFFHAND_PENALTY_PRO )

            addMods.append(dadd)
            
        else: # unarmed combat
            pass
    #
    # main hand
    if world.has_component(ent, cmp.EquipHand1):
        compo=world.component_for_entity(ent, cmp.EquipHand1)
        if compo.item:
            item=compo.item
            itemStats=world.component_for_entity(item, cmp.Stats)
            slot=world.component_for_entity(item, cmp.EquipableInHandSlot)
            dadd={}
            for k,v in slot.mods.items(): # collect add modifiers
                dadd.update({k:v})
            
            # bonuses

            # weapon skill bonus
            if world.has_component(item, cmp.WeaponSkill):
                weaponSkill=world.component_for_entity(item, cmp.WeaponSkill)
                if weaponSkill.skill in skills.skills:
                    skill=weaponSkill.skill
                    statdata=SKILL_WEAPSTATDATA[skill]
                    for _var, _modf in statdata:
                        dadd[_var] = dadd[_var] + _modf
            
            # 2-handed / 1-handed
            twoh=on(item, TWOHANDS)
            # apply bonus for wielding a 1-h weap in 2 hands (or w/ free hand)
            if (not twoh and not offhandItem):
                dadd['dfn'] = dadd['dfn'] + MOD_2HANDBONUS_DFN
                dadd['arm'] = dadd['arm'] + MOD_2HANDBONUS_ARM
                dadd['pro'] = dadd['pro'] + MOD_2HANDBONUS_PRO
                dadd['atk'] = dadd['atk'] + MOD_2HANDBONUS_ATK
                dadd['asp'] = dadd['asp'] + MOD_2HANDBONUS_ASP
                dadd['dmg'] = dadd['dmg']*MULT_2HANDBONUS_DMG # IDEA: don't increase damage, but when you attack you engage muscles in both arms, adding to the final damage that hits the foe.
                dadd['pen'] = dadd['pen'] + MOD_2HANDBONUS_PEN
            
            # penalties

            # durability penalty
            _apply_durabilityPenalty_weapon(dadd, itemStats.hp, itemStats.hpMax)

            # apply penalty for wielding a 2-h weap in 1 hand
            if (twoh and offhandItem):
                dadd['dfn'] = min(1, dadd['dfn'] - MOD_1HANDPENALTY_DFN)
                dadd['arm'] = min(1, dadd['arm'] - MOD_1HANDPENALTY_ARM)
                dadd['pro'] = min(1, dadd['pro'] - MOD_1HANDPENALTY_PRO)
                dadd['atk'] = dadd['atk'] - MOD_1HANDPENALTY_ATK
                dadd['asp'] = dadd['asp'] - MOD_1HANDPENALTY_ASP
                dadd['dmg'] = dadd['dmg']*MULT_1HANDPENALTY_DMG
                dadd['pen'] = dadd['pen']*MULT_1HANDPENALTY_PEN

            addMods.append(dadd)
                        
        else: # unarmed combat
            pass
   
'''
    #
    
    # calculate modded stats #

    # reset all modded stats to their base
    for k,v in base.__dict__.items():
        modded.__dict__[k] = v
    
    # apply mods -- add mods
    for mod in addMods:
        for k,v in mod.items():
            modded.__dict__[k] = v + modded.__dict__[k]
    
    # apply mods -- mult mods
    for k,v in multMods:
        for k,v in mod.items():
            modded.__dict__[k] = v * modded.__dict__[k]
    
    # round values
    for k,v in modded.__dict__.items():
        modded.__dict__[k] = around(v)
    # TODO: incorporate rounding with the min step. 
    modded.dfn = max(0, modded.dfn) 
    
    return modded
# end def

# create and initialize the ModdedStats component
def create_moddedStats(ent):
    world=Rogue.world
    modded=cmp.ModdedStats()
    base=world.component_for_entity(ent, cmp.Stats)
    for k in base.__dict__.keys():
        modded.__dict__.update({ k : 0 })
    world.add_component(ent, modded)
    make(ent, DIRTY_STATS)
    return modded


