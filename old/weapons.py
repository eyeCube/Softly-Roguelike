
<<<<<<< HEAD

##def create_steel_weapon(itemName, x, y) -> int:
##    '''
##        create a metal weapon and modify its values/name to resemble steel
##    '''
##    world=rog.world()
##    # create the weapon
##    weap=create_weapon(itemName, x, y)
##    # name
##    compo=world.component_for_entity(weap, cmp.Name)
##    if "metal " in compo.name:
##        compo.name = "steel {}".format(compo.name[6:])
##    else:
##        rog.add_prefix(item, "steel")
##    # value and mass
##    stats=world.component_for_entity(weap, cmp.Stats)
##    form=world.component_for_entity(weap, cmp.Form)
##    if form.material==MAT_METAL:
##        form.value = 1 + round(form.value * 5.1)
##        stats.mass = round(stats.mass * 0.95)
##    else:
##        form.value = 1 + round(form.value * 2.5)
##    # equipable stats
##    compo=world.component_for_entity(weap, cmp.EquipableInHoldSlot)
##    pen=compo.mods['pen']
##    compo.mods['dmg'] = round(compo.mods['dmg'] * 1.25)
##    compo.mods['pen'] = max(pen + 1, round(pen * 1.2))
##    # stats
##    compo=world.component_for_entity(weap, cmp.Stats)
##    compo.hpmax=compo.hpmax*1.5
##    compo.hp=compo.hpmax
##    compo.resrust=compo.resrust + 50
##    return weap
###



=======
>>>>>>> a253651713a50b14700a04ca20998632ff26e5e9
WEAPONS={ #melee weapons
    # $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,For,Gp,Ba,),TYPE,script,ID,
    # cost, mass, maxHP, material, strength required, dexterity requied, 
    # (Enc = Encumberance, Sta = Stamina cost to attack with, Rea = Reach;..., Force, Grip, Bal,),
    # SKL_ type const, script to run when created, ID_ const for identification purposes.
    
    # 1-handed weapons #

    # cudgels             $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,For,Gp,Ba,),TYPE,script,ID,
"plastic cudgel"        :(2,    1.4, 220, PLAS,10,2, (2,  2,  5,  0,  1,  1,  -15,5,  -5, 1,  18, 1,  5,  6, 0, ),SKL_BLUDGEONS,_pCudgel,ID_CLUB,),
"wooden cudgel"         :(13,   1.35,375, WOOD,10,2, (3,  4,  5,  0,  1,  1,  -9, 5,  -5, 1,  17, 1,  6,  6, 0, ),SKL_BLUDGEONS,_wCudgel,ID_CLUB,),
"stone cudgel"          :(10,   1.2, 340, WOOD,10,2, (3,  6,  6,  0,  1,  1,  -9, 5,  -5, 1,  15, 1,  8,  6, 0, ),SKL_BLUDGEONS,_sCudgel,ID_CLUB,),
"bone cudgel"           :(16,   1.3, 300, WOOD,10,2, (3,  5,  5,  0,  1,  1,  -9, 5,  -5, 1,  16, 1,  7,  6, 0, ),SKL_BLUDGEONS,_bCudgel,ID_CLUB,),
"glass cudgel"          :(18,   1.3, 10,  WOOD,10,3, (3,  9,  4,  0,  0,  0,  -6, 5,  -5, 1,  16, 1,  10, 6, 0, ),SKL_BLUDGEONS,_gCudgel,ID_CLUB,),
"metal cudgel"          :(32,   1.2, 650, WOOD,10,2, (3,  7,  7,  0,  1,  1,  -6, 5,  -5, 1,  15, 1,  9,  6, 0, ),SKL_BLUDGEONS,_mCudgel,ID_CLUB,),
    # clubs               $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,For,Gp,Ba,),TYPE,script,ID,
"plastic club"          :(2,    1.55,275, PLAS,13,2, (2,  3,  4,  0,  2,  1,  -21,6,  -5, 1,  20, 1,  6,  6, 0, ),SKL_BLUDGEONS,_pClub,ID_CLUB,),
"wooden club"           :(10,   1.45,420, WOOD,12,2, (3,  6,  5,  0,  2,  1,  -15,6,  -5, 1,  18, 1,  7,  6, 0, ),SKL_BLUDGEONS,_wClub,ID_CLUB,),
"stone club"            :(12,   1.3, 500, STON,11,2, (3,  7,  6,  0,  2,  1,  -12,5,  -5, 1,  18, 1,  9,  6, 0, ),SKL_BLUDGEONS,_sClub,ID_CLUB,),
"bone club"             :(22,   1.4, 365, BONE,12,2, (4,  7,  7,  0,  2,  1,  -12,5,  -5, 1,  18, 1,  8,  6, 0, ),SKL_BLUDGEONS,_bClub,ID_CLUB,),
"glass club"            :(32,   1.2, 3,   GLAS,10,3, (3,  10, 5,  0,  0,  0,  -9, 4,  -5, 1,  16, 1,  11, 6, 0, ),SKL_BLUDGEONS,_gClub,ID_CLUB,),
"metal club"            :(59,   1.15,950, METL,11,2, (3,  8,  8,  0,  1,  1,  -12,4,  -5, 1,  16, 1,  10, 6, 0, ),SKL_BLUDGEONS,_mClub,ID_CLUB,),
    # spiked clubs        $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,For,Gp,Ba,),TYPE,script,ID,
"plastic spiked club"   :(2,    1.6, 50,  PLAS,14,4, (1,  6,  5,  0,  2,  1,  -36,7,  -8, 1,  22, 1,  3,  6, 0, ),SKL_BLUDGEONS,_pSpikedClub,ID_MACE,),
"wooden spiked club"    :(10,   1.5, 120, WOOD,14,4, (2,  9,  6,  0,  2,  1,  -33,7,  -8, 1,  20, 1,  4,  6, 0, ),SKL_BLUDGEONS,_wSpikedClub,ID_MACE,),
    # maces               $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,For,Gp,Ba,),TYPE,script,ID,
"plastic mace"          :(2,    1.45,75,  PLAS,12,3, (2,  6,  5,  0,  1,  1,  -33,6,  -6, 1,  18, 1,  7,  6, 0, ),SKL_BLUDGEONS,_pMace,ID_MACE,),
"wooden mace"           :(20,   1.35,160, WOOD,12,3, (3,  9,  7,  0,  1,  1,  -27,6,  -6, 1,  16, 1,  8,  6, 0, ),SKL_BLUDGEONS,_wMace,ID_MACE,),
"stone mace"            :(24,   1.3, 220, WOOD,12,3, (3,  12, 8,  0,  1,  1,  -24,6,  -6, 1,  16, 1,  10, 6, 0, ),SKL_BLUDGEONS,_sMace,ID_MACE,),
"bone mace"             :(27,   1.3, 100, WOOD,12,3, (4,  10, 9,  0,  1,  1,  -24,6,  -6, 1,  16, 1,  9,  6, 0, ),SKL_BLUDGEONS,_bMace,ID_MACE,),
"glass mace"            :(65,   1.4, 5,   WOOD,12,4, (3,  24, 7,  0,  0,  0,  -30,5,  -6, 1,  14, 1,  12, 6, 0, ),SKL_BLUDGEONS,_gMace,ID_MACE,),
"metal mace"            :(72,   1.35,325, WOOD,12,3, (4,  14, 10, 0,  1,  1,  -27,5,  -6, 1,  16, 1,  11, 6, 0, ),SKL_BLUDGEONS,_mMace,ID_MACE,),
    # morning stars       $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,For,Gp,Ba,),TYPE,script,ID,
"metal morning star"    :(75,   1.25,240, METL,12,2, (4,  16, 12, 0,  1,  1,  -39,8,  -7, 1,  20, 1,  8,  6, 0, ),SKL_BLUDGEONS,_mMace,ID_MACE,),
    # warhammers          $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,For,Gp,Ba,),TYPE,script,ID,
"plastic warhammer"     :(2,    1.4, 190, PLAS,12,4, (1,  4,  10, 0,  0,  0,  -24,4,  -5, 1,  18, 1,  2,  6, 0, ),SKL_HAMMERS,_pWarhammer,ID_HAMMER,),
"wooden warhammer"      :(24,   1.35,280, WOOD,12,4, (2,  5,  13, 0,  0,  0,  -21,4,  -5, 1,  16, 1,  3,  6, 0, ),SKL_HAMMERS,_wWarhammer,ID_HAMMER,),
"stone warhammer"       :(18,   1.3, 200, WOOD,12,4, (2,  7,  15, 0,  0,  0,  -21,4,  -5, 1,  18, 1,  5,  6, 0, ),SKL_HAMMERS,_sWarhammer,ID_HAMMER,),
"bone warhammer"        :(28,   1.15,260, WOOD,10,4, (2,  6,  14, 0,  0,  0,  -15,4,  -5, 1,  16, 1,  4,  6, 0, ),SKL_HAMMERS,_bWarhammer,ID_HAMMER,),
"metal warhammer"       :(51,   1.25,500, WOOD,10,4, (2,  8,  16, 0,  0,  0,  -18,4,  -5, 1,  16, 1,  6,  6, 0, ),SKL_HAMMERS,_mWarhammer,ID_HAMMER,),
    # war axes            $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,For,Gp,Ba,),TYPE,script,ID,
"plastic war axe"       :(2,    1.35,60,  PLAS,11,5, (1,  8,  4,  1,  0,  0,  -12,5,  -2, 2,  18, 1,  4,  6, 0, ),SKL_AXES,_pWarAxe,ID_AXE,),
"wooden war axe"        :(26,   1.3, 90,  WOOD,11,5, (2,  10, 7,  1,  0,  0,  -9, 5,  -2, 2,  16, 1,  3,  6, 0, ),SKL_AXES,_wWarAxe,ID_AXE,),
"stone war axe"         :(22,   1.25,120, WOOD,11,5, (2,  12, 8,  1,  0,  0,  -15,5,  -2, 2,  18, 1,  1,  6, 0, ),SKL_AXES,_sWarAxe,ID_AXE,),
"bone war axe"          :(32,   1.25,180, WOOD,11,5, (2,  11, 9,  1,  0,  0,  -6, 5,  -2, 2,  16, 1,  2,  6, 0, ),SKL_AXES,_bWarAxe,ID_AXE,),
"metal war axe"         :(62,   1.2, 260, WOOD,11,5, (3,  14, 10, 1,  0,  0,  -12,5,  -2, 2,  15, 1,  0,  6, 0, ),SKL_AXES,_mWarAxe,ID_AXE,),
    # tomahawks           $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,For,Gp,Ba,),TYPE,script,ID,
"plastic tomahawk"      :(2,    1.1, 20,  PLAS,10,5, (1,  6,  7,  1,  0,  0,  -21,3,  -2, 3,  16, 1,  1,  6, 0, ),SKL_AXES,_pTomahawk,ID_AXE,),
"wooden tomahawk"       :(12,   0.9, 40,  WOOD,9, 6, (2,  7,  9,  1,  0,  0,  -18,3,  -2, 3,  16, 1,  0,  6, 0, ),SKL_AXES,_wTomahawk,ID_AXE,),
"stone tomahawk"        :(16,   1.1, 80,  WOOD,9, 5, (2,  9,  10, 1,  0,  0,  -24,3,  -2, 3,  15, 1,  -2, 6, 0, ),SKL_AXES,_sTomahawk,ID_AXE,),
"bone tomahawk"         :(23,   0.95,60,  WOOD,8, 6, (2,  8,  11, 1,  0,  0,  -18,3,  -2, 3,  15, 1,  -1, 6, 0, ),SKL_AXES,_bTomahawk,ID_AXE,),
"metal tomahawk"        :(40,   1.0, 120, WOOD,8, 6, (2,  11, 12, 1,  0,  0,  -21,3,  -2, 3,  14, 1,  -4, 6, 0, ),SKL_AXES,_mTomahawk,ID_AXE,),
    # Shivs               $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,For,Gp,Ba,),TYPE,script,ID,
"plastic shiv"          :(0,    0.3, 15,  PLAS,2, 4, (2,  2,  7,  0,  0,  0,  42, 2,  -5, 1,  9,  0,  -7, 7, 0, ),SKL_KNIVES,_pShiv,ID_KNIFE,),
"wooden shiv"           :(0,    0.3, 20,  WOOD,2, 4, (2,  3,  8,  0,  0,  0,  48, 2,  -5, 1,  8,  0,  -6, 7, 0, ),SKL_KNIVES,_wShiv,ID_KNIFE,),
"stone shiv"            :(0,    0.25,40,  STON,2, 4, (3,  4,  9,  0,  0,  0,  45, 2,  -5, 1,  7,  0,  -5, 7, 0, ),SKL_KNIVES,_sShiv,ID_KNIFE,),
"bone shiv"             :(0,    0.2, 35,  BONE,2, 4, (3,  4,  10, 0,  0,  0,  51, 2,  -5, 1,  7,  0,  -4, 7, 0, ),SKL_KNIVES,_bShiv,ID_KNIFE,),
"glass shiv"            :(1,    0.15,3,   GLAS,2, 5, (5,  6,  8,  0,  0,  0,  63, 2,  -5, 1,  5,  0,  -10,7, 0, ),SKL_KNIVES,_gShiv,ID_KNIFE,),
"metal shiv"            :(6,    0.2, 50,  METL,2, 4, (4,  4,  12, 0,  0,  0,  54, 2,  -5, 1,  6,  0,  -8, 7, 0, ),SKL_KNIVES,_mShiv,ID_KNIFE,),
"ceramic shiv"          :(2,    0.22,10,  CERA,2, 5, (5,  8,  9,  0,  0,  0,  60, 2,  -5, 1,  5,  0,  -10,7, 0, ),SKL_KNIVES,_cShiv,ID_KNIFE,),
    # knives              $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,For,Gp,Ba,),TYPE,script,ID,
"plastic knife"         :(0,    0.2, 35,  PLAS,2, 2, (3,  2,  10, 0,  0,  0,  48, 2,  -3, 2,  9,  0,  -12,8, 0, ),SKL_KNIVES,_pKnife,ID_KNIFE,),
"wooden knife"          :(2,    0.15,60,  WOOD,2, 2, (3,  3,  14, 0,  0,  0,  54, 2,  -3, 2,  8,  0,  -11,8, 0, ),SKL_KNIVES,_wKnife,ID_KNIFE,),
"stone knife"           :(6,    0.15,110, STON,2, 2, (4,  5,  16, 0,  0,  0,  51, 2,  -3, 2,  7,  0,  -10,8, 0, ),SKL_KNIVES,_sKnife,ID_KNIFE,),
"bone knife"            :(5,    0.12,90,  BONE,1, 3, (4,  5,  18, 0,  0,  0,  57, 2,  -3, 2,  7,  0,  -10,8, 0, ),SKL_KNIVES,_bKnife,ID_KNIFE,),
"glass knife"           :(12,   0.08,3,   GLAS,1, 5, (6,  8,  12, 0,  0,  0,  66, 2,  -3, 3,  5,  0,  -15,8, 0, ),SKL_KNIVES,_gKnife,ID_KNIFE,),
"metal knife"           :(14,   0.15,200, METL,1, 4, (5,  5,  20, 0,  0,  0,  60, 2,  -3, 3,  6,  0,  -12,8, 0, ),SKL_KNIVES,_mKnife,ID_KNIFE,),
"ceramic knife"         :(20,   0.12,15,  CERA,1, 5, (6,  10, 14, 0,  0,  0,  63, 2,  -3, 3,  5,  0,  -15,8, 0, ),SKL_KNIVES,_cKnife,ID_KNIFE,),
    # serrated knives     $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,For,Gp,Ba,),TYPE,script,ID,
"plastic serrated knife":(0,    0.18,15,  PLAS,2, 4, (2,  3,  8,  0,  0,  0,  24, 2,  -4, 1,  12, 0,  -4, 8, 0, ),SKL_KNIVES,_pSerrated,ID_KNIFE,),
"wooden serrated knife" :(4,    0.13,35,  WOOD,2, 4, (2,  4,  11, 0,  0,  0,  30, 2,  -4, 1,  11, 0,  -5, 8, 0, ),SKL_KNIVES,_wSerrated,ID_KNIFE,),
"stone serrated knife"  :(8,    0.13,60,  STON,2, 4, (3,  6,  12, 0,  0,  0,  27, 2,  -4, 1,  10, 0,  -6, 8, 0, ),SKL_KNIVES,_sSerrated,ID_KNIFE,),
"bone serrated knife"   :(7,    0.1, 45,  BONE,2, 5, (3,  6,  13, 0,  0,  0,  33, 2,  -4, 1,  10, 0,  -6, 8, 0, ),SKL_KNIVES,_bSerrated,ID_KNIFE,),
"metal serrated knife"  :(18,   0.13,100, METL,2, 6, (4,  7,  15, 0,  0,  0,  30, 2,  -4, 2,  9,  0,  -6, 8, 0, ),SKL_KNIVES,_mSerrated,ID_KNIFE,),
    # war knives          $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,For,Gp,Ba,),TYPE,script,ID,
"plastic war knife"     :(1,    0.55,50,  PLAS,5, 6, (3,  3,  12, 1,  0,  0,  51, 2.5,-2, 5,  12, 0,  0,  7, 0, ),SKL_KNIVES,_pWarKnife,ID_KNIFE,),
"wooden war knife"      :(5,    0.45,80,  WOOD,4, 7, (4,  4,  16, 1,  0,  0,  57, 2.5,-2, 6,  11, 0,  -1, 7, 0, ),SKL_KNIVES,_wWarKnife,ID_KNIFE,),
"bone war knife"        :(10,   0.5, 125, BONE,4, 8, (5,  6,  18, 1,  0,  0,  54, 2.5,-2, 7,  10, 0,  0,  7, 0, ),SKL_KNIVES,_bWarKnife,ID_KNIFE,),
"glass war knife"       :(28,   0.32,10,  GLAS,3, 9, (7,  10, 15, 0,  0,  0,  78, 2.5,-2, 6,  8,  0,  -7, 7, 0, ),SKL_KNIVES,_gWarKnife,ID_KNIFE,),
"metal war knife"       :(26,   0.42,250, METL,4, 8, (6,  7,  20, 2,  0,  0,  69, 2.5,-2, 9,  9,  0,  0,  7, 0, ),SKL_KNIVES,_mWarKnife,ID_KNIFE,),
"ceramic war knife"     :(35,   0.35,20,  CERA,3, 9, (7,  11, 16, 0,  0,  0,  75, 2.5,-2, 7,  8,  0,  -7, 7, 0, ),SKL_KNIVES,_cWarKnife,ID_KNIFE,),
    # daggers             $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,For,Gp,Ba,),TYPE,script,ID,
"bone dagger"           :(10,   0.35,115, BONE,3, 4, (4,  6,  21, 1,  0,  0,  69, 3,  -2, 5,  14, 0,  -2, 9, 0, ),SKL_KNIVES,_bDagger,ID_DAGGER,),
"glass dagger"          :(28,   0.22,5,   GLAS,2, 7, (6,  12, 18, 1,  0,  0,  90, 3,  -2, 7,  11, 0,  -4, 9, 0, ),SKL_KNIVES,_gDagger,ID_DAGGER,),
"metal dagger"          :(30,   0.3, 190, METL,3, 6, (5,  7,  24, 2,  0,  0,  75, 3,  -2, 6,  12, 0,  -1, 9, 0, ),SKL_KNIVES,_mDagger,ID_DAGGER,),
"rondel dagger"         :(70,   0.4, 320, METL,4, 7, (4,  8,  28, 2,  0,  0,  54, 3,  -2, 6,  15, 0,  0,  10,0, ),SKL_KNIVES,_rondelDagger,ID_DAGGER,),#STEEL
    # bayonets            $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,For,Gp,Ba,),TYPE,script,ID,
"plastic bayonet"       :(0,    0.45,40,  PLAS,5, 4, (2,  2,  10, 0,  0,  0,  36, 3,  -3, 2,  12, 0,  0,  2, 0, ),SKL_KNIVES,_pBayonet,ID_KNIFE,),
"wooden bayonet"        :(5,    0.4, 70,  WOOD,4, 4, (3,  3,  14, 0,  0,  0,  33, 3,  -3, 2,  11, 0,  0,  2, 0, ),SKL_KNIVES,_wBayonet,ID_KNIFE,),
"bone bayonet"          :(8,    0.3, 100, BONE,3, 4, (3,  5,  16, 0,  0,  0,  39, 3,  -3, 2,  10, 0,  0,  2, 0, ),SKL_KNIVES,_bBayonet,ID_KNIFE,),
"metal bayonet"         :(22,   0.35,225, METL,4, 5, (4,  5,  18, 0,  0,  0,  36, 3,  -3, 3,  9,  0,  0,  2, 0, ),SKL_KNIVES,_mBayonet,ID_KNIFE,),
    # javelins            $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,For,Gp,Ba,),TYPE,script,ID,
"plastic javelin"       :(1,    0.75,35,  PLAS,7, 2, (6,  4,  7,  0,  0,  0,  -24,7,  -6, 3,  18, 2,  0,  6, 2, ),SKL_JAVELINS,_pJavelin,ID_JAVELIN,),
"wooden javelin"        :(5,    0.7, 50,  WOOD,7, 2, (8,  6,  10, 0,  0,  0,  -27,7,  -6, 3,  16, 2,  -1, 6, 2, ),SKL_JAVELINS,_wJavelin,ID_JAVELIN,),
"metal javelin"         :(32,   0.5, 200, METL,6, 3, (9,  8,  12, 0,  0,  0,  -18,7,  -6, 3,  14, 2,  -2, 6, 2, ),SKL_JAVELINS,_mJavelin,ID_JAVELIN,),
    # shortspears         $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,For,Gp,Ba,),TYPE,script,ID,
"plastic shortspear"    :(1,    1.0, 15,  PLAS,12,1, (6,  5,  6,  0,  0,  0,  -12,8,  -8, 5,  16, 2.5,2,  6, 2, ),SKL_JAVELINS,_pShortSpear,ID_JAVELIN,),
"wooden shortspear"     :(8,    1.05,30,  WOOD,12,1, (7,  7,  8,  0,  0,  0,  -12,8,  -8, 5,  16, 2.5,1,  6, 2, ),SKL_JAVELINS,_wShortSpear,ID_JAVELIN,),
"stone shortspear"      :(8,    1.1, 65,  WOOD,13,1, (7,  9,  10, 0,  0,  0,  -15,8,  -8, 5,  16, 2.5,0,  6, 2, ),SKL_JAVELINS,_sShortSpear,ID_JAVELIN,),
"bone shortspear"       :(15,   1.05,100, WOOD,12,2, (7,  8,  9,  0,  0,  0,  -12,8,  -8, 5,  16, 2.5,0,  6, 2, ),SKL_JAVELINS,_bShortSpear,ID_JAVELIN,),
"glass shortspear"      :(25,   0.95,5,   WOOD,9, 3, (9,  12, 7,  0,  0,  0,  -9, 8,  -8, 5,  16, 2.5,-1, 6, 2, ),SKL_JAVELINS,_gShortSpear,ID_JAVELIN,),
"metal shortspear"      :(22,   1.05,135, WOOD,11,2, (8,  10, 12, 0,  0,  0,  -12,8,  -8, 5,  16, 2.5,1,  6, 2, ),SKL_JAVELINS,_mShortSpear,ID_JAVELIN,),
"ceramic shortspear"    :(28,   0.95,10,  CERA,9, 3, (9,  14, 9,  0,  0,  0,  -9, 8,  -8, 5,  16, 2.5,-1, 6, 2, ),SKL_JAVELINS,_cShortSpear,ID_JAVELIN,),
    # boomerangs          $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,For,Gp,Ba,),TYPE,script,ID,
"plastic boomerang"     :(1,    0.7, 20,  PLAS,10,2, (2,  2,  3,  0,  0,  0,  -15,6,  -6, 1,  16, 1,  8,  4, 0, ),SKL_BLUDGEONS,_pBoomerang,ID_BOOMERANG,),
"wooden boomerang"      :(4,    0.5, 30,  WOOD,9, 3, (3,  4,  5,  0,  0,  0,  -12,6,  -4, 1,  16, 1,  5,  4, 0, ),SKL_BLUDGEONS,_wBoomerang,ID_BOOMERANG,),
"bone boomerang"        :(5,    0.45,25,  BONE,8, 4, (3,  4,  5,  0,  0,  0,  -9, 5,  -4, 1,  14, 1,  6,  4, 0, ),SKL_BLUDGEONS,_bBoomerang,ID_BOOMERANG,),
"glass boomerang"       :(22,   0.5, 2,   GLAS,7, 6, (4,  7,  4,  0,  0,  0,  -9, 5,  -4, 1,  14, 1,  8,  4, 0, ),SKL_BLUDGEONS,_gBoomerang,ID_BOOMERANG,),
"metal boomerang"       :(25,   0.4, 90,  METL,8, 5, (5,  5,  6,  0,  0,  0,  -6, 5,  -4, 2,  14, 1,  7,  4, 0, ),SKL_BLUDGEONS,_mBoomerang,ID_BOOMERANG,),
"ceramic boomerang"     :(38,   0.5, 1,   CERA,7, 6, (4,  8,  4,  0,  0,  0,  -9, 5,  -3, 1,  14, 1,  8,  4, 0, ),SKL_BLUDGEONS,_cBoomerang,ID_BOOMERANG,),
    # bucklers            $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,For,Gp,Ba,),TYPE,script,ID,
"plastic buckler"       :(2,    1.7, 30,  PLAS,17,12,(1,  1,  1,  5,  1,  1,  -9, 4,  -3, 3,  16, 0.2,6,  12,1, ),SKL_SHIELDS,_buckler,ID_SHIELD,),
"wooden buckler"        :(12,   1.65,75,  WOOD,16,12,(1,  2,  3,  6,  1,  1,  -6, 4,  -3, 4,  16, 0.2,7,  12,1, ),SKL_SHIELDS,_buckler,ID_SHIELD,),
"bone buckler"          :(24,   1.4, 40,  BONE,14,12,(2,  3,  4,  6,  1,  1,  -3, 4,  -2, 5,  12, 0.2,7,  12,1, ),SKL_SHIELDS,_buckler,ID_SHIELD,),#made of one large bone sculpted into shape + some leather
"metal buckler"         :(90,   1.5, 150, METL,15,12,(2,  5,  5,  7,  2,  1,  -6, 4,  -3, 6,  16, 0.2,8,  12,1, ),SKL_SHIELDS,_buckler,ID_SHIELD,),
    # rotellas            $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,For,Gp,Ba,),TYPE,script,ID,
"plastic rotella"       :(4,    4.0, 50,  PLAS,24,8, (2,  2,  1,  5,  2,  2,  -33,6,  -6, 4,  32, 0.4,10, 16,-1,),SKL_SHIELDS,_rotella,ID_SHIELD,),
"wooden rotella"        :(24,   3.6, 115, WOOD,22,8, (3,  3,  2,  6,  2,  2,  -27,6,  -5, 6,  30, 0.4,11, 16,-1,),SKL_SHIELDS,_rotella,ID_SHIELD,),
"bone rotella"          :(49,   3.4, 75,  BONE,20,8, (3,  5,  3,  5,  2,  2,  -24,6,  -4, 6,  28, 0.4,12, 16,-1,),SKL_SHIELDS,_rotella,ID_SHIELD,),#made of one, two or three big pieces of bone glued together. The pieces of bone (esp. for 1 or 2-piece rotellas) are difficult to acquire and manufacture for shield use so this is a relatively expensive item.
"metal rotella"         :(175,  3.0, 240, METL,18,8, (3,  7,  4,  6,  3,  2,  -18,6,  -4, 7,  26, 0.4,13, 16,-1,),SKL_SHIELDS,_rotella,ID_SHIELD,), # one stamina cost for each 100g, +2 for being metal. - some percentage b/c shields are easy to attack with. Encumbering non-weapons should get *1.5 stamina cost or some shit. Auto-generated of course.
    # shields             $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,For,Gp,Ba,),TYPE,script,ID,
"wicker shield"         :(20,   4.2, 35,  WOOD,18,6, (1,  2,  0,  4,  2,  2,  -36,7,  -10,4,  44, 0.6,2,  12,-2,),SKL_SHIELDS,_shield,ID_SHIELD,),
"plastic shield"        :(7,    6.5, 80,  PLAS,22,6, (1,  3,  0,  3,  2,  3,  -54,7,  -12,5,  52, 0.6,14, 12,-3,),SKL_SHIELDS,_shield,ID_SHIELD,),
"wooden shield"         :(75,   5.25,180, WOOD,20,6, (3,  5,  1,  4,  3,  3,  -45,7,  -10,7,  44, 0.6,13, 12,-3,),SKL_SHIELDS,_shield,ID_SHIELD,),
"bone shield"           :(145,  6.2, 100, BONE,22,6, (2,  7,  2,  4,  4,  2,  -48,7,  -8, 7,  52, 0.6,14, 12,-3,),SKL_SHIELDS,_shield,ID_SHIELD,),
"boiled leather shield" :(190,  5.05,120, BOIL,20,6, (3,  4,  1,  5,  4,  3,  -42,7,  -12,6,  44, 0.6,12, 12,-3,),SKL_SHIELDS,_shield,ID_SHIELD,),
"metal shield"          :(380,  6.0, 360, METL,22,6, (2,  9,  3,  4,  5,  3,  -51,7,  -6, 8,  48, 0.6,15, 12,-3,),SKL_SHIELDS,_shield,ID_SHIELD,),
    # scutums             $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,For,Gp,Ba,),TYPE,script,ID,
"plastic scutum"        :(10,   9.8, 80,  PLAS,29,4, (-1, 2,  -6, 2,  3,  3,  -69,9,  -12,6,  76, 0.3,14, 12,-5,),SKL_SHIELDS,_scutum,ID_SHIELD,),
"wooden scutum"         :(120,  8.7, 180, WOOD,27,4, (1,  4,  -5, 3,  4,  3,  -57,9,  -10,7,  66, 0.3,14, 12,-5,),SKL_SHIELDS,_scutum,ID_SHIELD,),
"bone scutum"           :(255,  9.3, 100, BONE,28,4, (0,  5,  -2, 3,  5,  2,  -60,9,  -8, 8,  72, 0.3,14, 12,-5,),SKL_SHIELDS,_scutum,ID_SHIELD,),
"boiled leather scutum" :(305,  7.7, 120, BOIL,24,4, (1,  4,  -3, 4,  5,  3,  -54,9,  -12,8,  66, 0.3,14, 12,-5,),SKL_SHIELDS,_scutum,ID_SHIELD,),
"metal scutum"          :(495,  8.1, 360, METL,26,4, (0,  6,  -1, 3,  6,  3,  -63,9,  -6, 8,  72, 0.3,14, 12,-5,),SKL_SHIELDS,_scutum,ID_SHIELD,),
    # tower shields       $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,For,Gp,Ba,),TYPE,script,ID,
"plastic tower shield"  :(15,   13.5,140, PLAS,33,1, (-3, 2,  -12,-6, 4,  5,  -81,10, -32,7,  120,0.1,14, 8, -7,),SKL_SHIELDS,_towerShield,ID_SHIELD,),
"wooden tower shield"   :(165,  12.0,400, WOOD,31,1, (-2, 2,  -12,-5, 5,  6,  -72,10, -30,8,  100,0.1,14, 8, -7,),SKL_SHIELDS,_towerShield,ID_SHIELD,),
"bone tower shield"     :(360,  12.7,320, BONE,32,1, (-2, 3,  -6, -6, 6,  4,  -81,10, -28,9,  100,0.1,14, 8, -7,),SKL_SHIELDS,_towerShield,ID_SHIELD,),
"metal tower shield"    :(620,  10.8,800, METL,30,1, (-1, 4,  -6, -4, 8,  6,  -75,10, -24,9,  90, 0.1,14, 8, -6,),SKL_SHIELDS,_towerShield,ID_SHIELD,),
"riot shield"           :(1060, 8.2, 250, PLAS,24,1, (0,  2,  -9, -3, 7,  6,  -69,8,  -20,10, 70, 0.1,14, 8, -5,),SKL_SHIELDS,_towerShield,ID_SHIELD,),
    # whips / flails      $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,For,Gp,Ba,),TYPE,script,ID,
"rubber flail"          :(2,    0.1, 3,   RUBB,1, 3, (-8, 3,  2,  0,  0,  0,  -51,3,  -1, 0,  1,  0,  -19,0, -1,),None,_rubberBandWhip,ID_RUBBERBAND,),#2h only. This is a heavy metal ball attached to a rubber band like a primitive flail.
"rubber whip"           :(6,    0.3, 30,  RUBB,3, 5, (4,  1,  0,  0,  0,  0,  -15,2,  -10,1,  7,  1,  -19,-4,0,),SKL_BLUDGEONS,_whip,ID_BATON,),
"plastic duel whip"     :(2,    1.6, 90,  PLAS,12,2, (2,  2,  2,  0,  0,  0,  -30,3,  -6, 1,  16, 1,  1,  6, 0,),SKL_BLUDGEONS,_heavyWhip,ID_BATON,),
"leather duel whip"     :(75,   1.45,150, LETH,12,2, (2,  3,  4,  0,  0,  0,  -24,3,  -10,1,  20, 1,  0,  6, 0,),SKL_BLUDGEONS,_heavyWhip,ID_BATON,),
"metal whip"            :(90,   0.8, 250, METL,8, 6, (0,  3,  6,  0,  0,  0,  -9, 3,  -12,2,  12, 1,  0,  8, -1,),SKL_BLUDGEONS,_metalWhip,ID_WHIP,),#stinger whip -- for causing pain
    # bullwhips           $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,For,Gp,Ba,),TYPE,script,ID,
"leather bullwhip"      :(40,   0.6, 60,  LETH,4, 16,(-5, 4,  2,  0,  0,  0,  -51,2.5,-5, 0,  8,  3,  -15,6, 0,),SKL_BULLWHIPS,_bullWhip,ID_BULLWHIP,),
"graphene bullwhip"     :(7500, 0.5, 1800,CARB,3, 20,(-2, 5,  5,  0,  0,  0,  -42,2.5,-5, 1,  8,  3,  -16,8, 0,),SKL_BULLWHIPS,_bullWhip,ID_BULLWHIP,),
    # swords              $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,For,Gp,Ba,),TYPE,script,ID,
"plastic sword"         :(2,    1.15,20,  PLAS,11,6, (4,  3,  6,  1,  0,  0,  15, 5,  -7, 3,  14, 1,  -1, 6, 0,),SKL_SWORDS,_pSword,ID_SWORD,),
"wooden sword"          :(22,   1.05,40,  WOOD,10,8, (6,  4,  9,  2,  0,  0,  24, 4,  -6, 4,  12, 1,  -2, 7, 0.5,),SKL_SWORDS,_wSword,ID_SWORD,),
"bone sword"            :(51,   0.75,60,  BONE,7, 10,(5,  5,  12, 1,  0,  0,  21, 3,  -5, 4,  8,  1,  -3, 7, 0,),SKL_SWORDS,_bSword,ID_SWORD,),
"metal sword"           :(65,   1.0, 120, METL,9, 12,(7,  6,  14, 2,  0,  0,  39, 4,  -4, 5,  10, 1,  -3, 8, 1,),SKL_SWORDS,_mSword,ID_SWORD,),
"diamonite sword"       :(2650, 0.9, 400, CARB,7, 15,(8,  9,  18, 3,  0,  0,  51, 4,  -4, 7,  9,  1,  0,  9, 1,),SKL_SWORDS,_dSword,ID_SWORD,),
"graphene sword"        :(11500,0.8, 1200,CARB,5, 18,(9,  12, 22, 3,  0,  0,  60, 3,  -3, 12, 8,  2,  -4, 9, 1,),SKL_SWORDS,_grSword,ID_SWORD,),
    # other swords        $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,For,Gp,Ba,),TYPE,script,ID,
"gladius"               :(45,   0.7, 180, METL,6, 10,(5,  6,  15, 2,  0,  0,  42, 3,  -2, 2,  8,  1,  -8, 8, 0.5,),SKL_SWORDS,_leafSword,ID_SWORD,),
"hanger"                :(60,   0.8, 90,  METL,8, 8, (10, 4,  11, 4,  0,  0.5,54, 4,  -3, 4,  10, 1,  -12,9, 0.5,),SKL_SWORDS,_hanger,ID_SWORD,),#POOR STEEL
"messer"                :(90,   1.4, 210, METL,12,6, (6,  6,  12, 3,  1,  1,  33, 6,  -4, 3,  14, 1.2,0,  9, 1,),SKL_SWORDS,_messer,ID_SWORD,),#POOR STEEL
"smallsword"            :(105,  0.4, 40,  METL,5, 13,(8,  3,  11, 4,  0,  0,  69, 3,  -6, 8,  8,  1,  -16,9, 0.5,),SKL_SWORDS,_smallSword,ID_SWORD,),#STEEL
"scimitar"              :(120,  1.1, 120, METL,8, 14,(8,  6,  12, 3,  0.5,0,  54, 5,  -3, 6,  10, 1,  -8, 9, 1,),SKL_SWORDS,_curvedSword,ID_SWORD,),#POOR STEEL
"falx"                  :(120,  1.2, 300, METL,10,15,(5,  8,  16, 2,  1,  0.5,15, 6,  -2, 9,  14, 1,  0,  8, 1,),SKL_SWORDS,_curvedSword,ID_SWORD,),#POOR STEEL # -reverse curved blade
"broadsword"            :(130,  1.3, 240, METL,12,7, (5,  8,  15, 2,  1,  0,  30, 5,  -5, 3,  14, 1,  1,  8, 1,),SKL_SWORDS,_broadsword,ID_SWORD,),#POOR STEEL
"cutlass"               :(130,  1.35,450, METL,13,12,(7,  7,  12, 3,  1,  1,  39, 5,  -2, 6,  12, 1,  -4, 9, 1,),SKL_SWORDS,_cutlass,ID_SWORD,),#POOR STEEL, made entirely of metal (no wood)
"sabre"                 :(135,  1.25,200, METL,12,12,(9,  6,  11, 4,  0.5,0.5,48, 5,  -4, 5,  12, 1.2,-4, 9, 1,),SKL_SWORDS,_sabre,ID_SWORD,),#POOR STEEL
"falchion"              :(160,  1.4, 345, METL,14,10,(5,  8,  11, 1,  1,  0,  24, 5.5,-5, 4,  16, 1,  2,  8, 1.5,),SKL_SWORDS,_falchion,ID_SWORD,),#POOR STEEL
"arming sword"          :(235,  1.35,260, METL,12,14,(8,  7,  18, 2,  1,  0.5,42, 6,  -4, 5,  14, 1.8,-2, 8, 2,),SKL_SWORDS,_armingSword,ID_SWORD,),#STEEL
"basket-hilted sword"   :(295,  1.45,220, METL,14,16,(9,  6,  14, 3,  1,  1.5,51, 7,  -6, 7,  16, 1.5,-8, 12,1.5,),SKL_SWORDS,_basketHiltedSword,ID_SWORD,),#STEEL
"rapier"                :(345,  1.5, 110, METL,16,16,(11, 5,  14, 4,  1,  1,  60, 7,  -7, 8,  18, 2.2,-16,10,2,),SKL_SWORDS,_rapier,ID_SWORD,),#STEEL
    # other misc weapons  $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,For,Gp,Ba,),TYPE,script,ID,
    # knives
"kukri"                 :(70,   0.5, 90,  METL,5, 14,(4,  6,  8,  1,  0,  0,  51, 2.5,-2, 10, 10, 0.4,-10,8, 0.5,),SKL_KNIVES,_kukri,ID_KNIFE,),#POOR STEEL
"metal throwing knife"  :(8,    0.1, 20,  METL,1, 16,(5,  3,  16, 0,  0,  0,  54, 1.5,-8, 1,  6,  0.1,-16,4, 0,),SKL_KNIVES,_mThrowingKnife,ID_KNIFE,),
"metal butcher knife"   :(16,   0.3, 120, METL,3, 8, (2,  5,  3,  0,  0,  0,  12, 4,  -10,1,  14, 0.2,-8, 6, 0,),SKL_KNIVES,_butcherKnife,ID_KNIFE,),
    # boxing weapons
"metal knuckles"        :(6,    0.1, 320, METL,2, 2, (2,  4,  4,  0,  0,  0,  18, 2,  -6, 0,  20, 0,  3,  20,0,),SKL_BOXING,_knuckles,ID_KNUCKLES,),
"metal spiked knuckles" :(14,   0.2, 150, METL,2, 2, (2,  5,  6,  0,  0,  0,  6,  3,  -8, 0,  20, 0,  2,  20,0,),SKL_BOXING,_knuckles,ID_KNUCKLES,),
"boxing wrap"           :(4,    0.25,20,  CLTH,2, 6, (2,  2,  1,  1,  0,  0,  33, 1,  -8, 2,  20, 0,  1,  24,0,),SKL_BOXING,_boxingWraps,ID_BANDAGE,),
    # bludgeons
"metal baton"           :(25,   0.5, 175, METL,4, 3, (4,  3,  5,  1,  0,  0,  9,  2,  -2, 3,  10, 0.5,-2, 8, 0,),SKL_BLUDGEONS,_baton,ID_BATON,),
"metal bat"             :(35,   0.7, 220, METL,7, 1, (3,  6,  6,  0,  1,  0,  -6, 5,  -8, 1,  12, 0.5,3,  6, 0,),SKL_BLUDGEONS,_baton,ID_BATON,),
"wooden truncheon"      :(4,    0.85,250, WOOD,8, 2, (3,  5,  6,  1,  0,  0,  -3, 5,  -6, 2,  14, 1,  4,  6, 0,),SKL_BLUDGEONS,_club,ID_BATON,),
"metal truncheon"       :(46,   0.75,500, METL,8, 3, (3,  7,  8,  1,  0,  0,  6,  5,  -4, 2,  14, 1,  5,  6, 0,),SKL_BLUDGEONS,_club,ID_BATON,),
    # misc
"metal push dagger"     :(30,   0.3, 180, METL,6, 4, (3,  9,  15, 0,  0,  0,  90, 4,  -12,0,  18, 0.2,-2, 14,0,),SKL_PUSHDAGGERS,_pushDagger,ID_PUSHDAGGER,),
"crescent moon blade"   :(125,  0.3, 60,  METL,3, 14,(2,  4,  8,  1,  0,  0,  75, 6,  -4, 1,  8,  0.3,-7, 4, 0,),None,_crescentBlade,ID_KNIFE,),
##"scissors katar"     :(25,   0.3, 180, METL,2,(3,  9,  15, 0,  0,  0,  90, 0,  -12,0,  4,),SKL_PUSHDAGGERS,_pushDagger,), 

    # 2-handed weapons #

# Some weapons can only be built with steel, like longswords, greatswords.
#   So these are expensive, and have no material designation.
    # longswords          $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,For,Gp,Ba,),TYPE,script,ID,
"bastard sword"         :(245,  1.55,300, METL,18,14,(4,  9,  12, 1,  1,  1,  15, 6,  -5, 6,  24, 1.8,2,  7, 1,),SKL_LONGSWORDS,_bastardSword,ID_LONGSWORD,),#STEEL # weapon is a longsword but can be wielded in 1 hand (which it is by default due to the mechanics in this game (just by not having the TWOHANDS flag, it is a one-handed weapon that can be wielded with two hands alternatively.))
"longsword"             :(260,  1.6, 210, METL,10,12,(10, 12, 18, 5,  3,  3,  51, 6,  -6, 12, 16, 2.2,0,  10,2,),SKL_LONGSWORDS,_longSword,ID_LONGSWORD,),#STEEL
"kriegsmesser"          :(265,  1.8, 250, METL,14,8, (9,  14, 14, 2,  3,  3,  36, 8,  -16,9,  20, 2,  -6, 8, 1,),SKL_LONGSWORDS,_kriegsmesser,ID_LONGSWORD,),#STEEL
"katana"                :(285,  1.45,80,  METL,8, 14,(12, 11, 16, 3,  2,  2,  45, 6,  -12,14, 14, 1.6,-12,10,1,),SKL_LONGSWORDS,_katana,ID_LONGSWORD,),#STEEL # VERY DIFFICULT TO FIND RECIPE FOR THIS/VERY DIFFICULT TO MAKE! SO VERY EXPENSIVE
"estoc"                 :(305,  1.65,100, METL,10,16,(11, 10, 20, 6,  1,  2,  60, 7,  -12,16, 18, 2.4,-14,10,2,),SKL_LONGSWORDS,_estoc,ID_LONGSWORD,),#STEEL
    # greatswords         $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,For,Gp,Ba,),TYPE,script,ID,
"greatsword"            :(540,  3.5, 450, METL,26,12,(9,  18, 15, 3,  3,  3,  -15,18, -6, 10, 36, 4,  6,  10,1,),SKL_GREATSWORDS,_greatSword,ID_GREATSWORD,),
"flamberge"             :(595,  3.3, 225, METL,24,14,(10, 16, 12, 2,  3,  3,  -12,18, -10,10, 32, 3.2,8,  10,1,),SKL_GREATSWORDS,_flamberge,ID_GREATSWORD,),
    # short staves        $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,For,Gp,Ba,),TYPE,script,ID,
"plastic staff"         :(1.5,  1.5, 100, PLAS,11,10,(6,  5,  4,  2,  2,  2.5,66, 8,  -7, 13, 16, 3,  6,  8, 3,),SKL_STAVES,_staff,ID_STAFF,),
"wooden staff"          :(11,   1.3, 300, WOOD,9, 10,(7,  7,  6,  4,  4,  3,  75, 8,  -5, 15, 14, 3,  7,  8, 4,),SKL_STAVES,_staff,ID_STAFF,),
"bone staff"            :(20,   1.4, 200, WOOD,12,10,(5,  9,  7,  2,  4,  3,  51, 10, -3, 11, 18, 3,  8,  8, 3,),SKL_STAVES,_staff,ID_STAFF,), # bone-headed staff (wooden staff with bone tip)
"metal staff"           :(30,   1.2, 250, WOOD,11,10,(6,  9,  8,  3,  4,  3,  66, 8,  -5, 13, 14, 3,  10, 8, 4,),SKL_STAVES,_staff,ID_STAFF,), # metal-headed staff (metal not tough enough to make a staff fully made of metal)
"steel staff"           :(142,  1.1, 500, METL,10,10,(8,  10, 9,  4,  3,  3,  81, 8,  -5, 16, 14, 3,  12, 8, 4,),SKL_STAVES,_staff,ID_STAFF,), # regular metal cannot make an entire staff shaft, but steel can.
    # longstaves          $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,For,Gp,Ba,),TYPE,script,ID,
"plastic longstaff"     :(3,    3.1, 150, PLAS,24,8, (9,  8,  6,  3,  2,  2,  54, 24, -18,5,  32, 6,  12, 8, 5,),SKL_POLEARMS,_longstaff,ID_LONGSTAFF,),
"wooden longstaff"      :(24,   2.7, 400, WOOD,22,8, (10, 10, 8,  3,  4,  2.5,57, 24, -18,6,  28, 6,  13, 8, 6,),SKL_POLEARMS,_longstaff,ID_LONGSTAFF,),
"steel longstaff"       :(88,   2.6, 500, METL,22,8, (11, 12, 10, 3,  3,  2.5,60, 24, -18,7,  26, 6,  14, 8, 6,),SKL_POLEARMS,_longstaff,ID_LONGSTAFF,),
    # spears              $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,For,Gp,Ba,),TYPE,script,ID,
"plastic spear"         :(2,    2.1, 30,  PLAS,12,8, (8,  10, 10, 3,  2,  3,  51, 10, -12,8,  20, 4.1,4,  8, 3,),SKL_SPEARS,_pSpear,ID_SPEAR,),
"wooden spear"          :(20,   2.05,60,  WOOD,11,8, (10, 11, 12, 3,  3,  3,  48, 10, -12,9,  20, 4.1,3,  8, 3,),SKL_SPEARS,_wSpear,ID_SPEAR,),
"stone spear"           :(22,   2.15,100, WOOD,12,8, (9,  13, 13, 3,  3,  3,  42, 10, -12,9,  20, 4.1,1,  8, 3,),SKL_SPEARS,_bSpear,ID_SPEAR,),
"bone spear"            :(25,   2.05,150, WOOD,11,8, (10, 12, 14, 3,  3,  3,  45, 10, -12,10, 20, 4,  2,  8, 3,),SKL_SPEARS,_sSpear,ID_SPEAR,),
"glass spear"           :(34,   1.9, 5,   WOOD,9, 12,(12, 22, 10, 3,  3,  3,  51, 10, -12,14, 18, 4,  -1, 8, 3,),SKL_SPEARS,_gSpear,ID_SPEAR,),
"metal spear"           :(32,   2.1, 200, WOOD,11,10,(11, 14, 16, 3,  3,  3,  45, 10, -12,12, 20, 4.2,0,  8, 3,),SKL_SPEARS,_mSpear,ID_SPEAR,),
"metal winged spear"    :(40,   2.15,300, WOOD,14,12,(10, 16, 15, 3,  3,  3.5,36, 10, -8, 12, 20, 4,  6,  8, 4,),SKL_SPEARS,_mSpear,ID_SPEAR,),
"ceramic spear"         :(36,   1.95,10,  WOOD,9, 12,(12, 24, 12, 3,  3,  3,  48, 10, -12,14, 18, 4,  -1, 8, 3,),SKL_SPEARS,_cSpear,ID_SPEAR,),
    # partizans           $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,For,Gp,Ba,),TYPE,script,ID,
"metal partizan"        :(65,   2.2, 240, WOOD,14,6, (8,  18, 14, 2,  3,  3,  24, 16, -12,10, 22, 5,  2,  8, 2,),SKL_SPEARS,_mPartizan,ID_SPEAR,),
    # naginatas           $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,For,Gp,Ba,),TYPE,script,ID,
"metal naginata"        :(80,   2.6, 120, WOOD,18,10,(9,  12, 13, 2,  3,  2,  15, 20, -14,8,  26, 5,  -8, 8, 1,),SKL_SPEARS,_mNaginata,ID_SPEAR,),
    # bills               $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,For,Gp,Ba,),TYPE,script,ID,
"metal bill"            :(110,  2.2, 80,  WOOD,16,14,(12, 14, 18, 2,  3,  2,  24, 18, -4, 10, 22, 4.5,12, 8, 2,),SKL_POLEARMS,_mBill,ID_POLEARM,),#requires some steel
    # halberds            $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,For,Gp,Ba,),TYPE,script,ID,
"metal halberd"         :(135,  2.25,280, WOOD,15,12,(8,  18, 20, 2,  3,  2,  9,  19, -6, 8,  22, 5.3,-2, 8, 2,),SKL_POLEARMS,_mHalberd,ID_POLEARM,),
    # poleaxes            $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,For,Gp,Ba,),TYPE,script,ID,
"metal poleaxe"         :(150,  2.35,450, WOOD,14,13,(7,  22, 20, 2,  4,  2,  -15,12, -4, 6,  24, 3,  10, 10,0,),SKL_GREATAXES,_mPoleAxe,ID_GREATAXE,),
    # polehammers         $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,For,Gp,Ba,),TYPE,script,ID,
"plastic polehammer"    :(3,    2.7, 110, PLAS,18,9, (4,  11, 16, 1,  2,  2,  -27,12, -9, 3,  30, 2.5,12, 10,0,),SKL_MALLETS,_pPoleHammer,ID_GREATHAMMER,),
"wooden polehammer"     :(18,   2.6, 200, WOOD,17,10,(5,  13, 16, 1,  3,  2,  -24,12, -9, 4,  28, 2.5,12, 10,0,),SKL_MALLETS,_wPoleHammer,ID_GREATHAMMER,),
"metal polehammer"      :(105,  2.4, 675, WOOD,16,11,(6,  16, 24, 1,  3,  2,  -21,12, -9, 5,  26, 2.5,12, 10,0,),SKL_MALLETS,_mPoleHammer,ID_GREATHAMMER,),
    # war mallets         $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,For,Gp,Ba,),TYPE,script,ID,
"plastic war mallet"    :(3,    2.4, 320, PLAS,16,3, (3,  11, 12, -1, 2,  2,  -45,14, -14,3,  28, 2,  16, 8, -1,),SKL_MALLETS,_1mallet,ID_GREATHAMMER,),
"wooden war mallet"     :(19,   2.3, 600, WOOD,16,3, (4,  13, 13, -1, 3,  2,  -42,14, -14,4,  25, 2,  16, 8, -1,),SKL_MALLETS,_1mallet,ID_GREATHAMMER,),
"stone war mallet"      :(22,   2.1, 400, WOOD,15,3, (5,  17, 14, 0,  3,  2,  -36,14, -14,4,  25, 2,  16, 8, -1,),SKL_MALLETS,_1mallet,ID_GREATHAMMER,),
"bone war mallet"       :(25,   2.2, 500, WOOD,15,3, (4,  15, 15, 0,  3,  2,  -39,14, -14,5,  25, 2,  16, 8, -1,),SKL_MALLETS,_1mallet,ID_GREATHAMMER,),
"metal war mallet"      :(72,   2.0, 950, WOOD,15,3, (5,  19, 16, 0,  4,  2,  -39,14, -14,6,  22, 2,  16, 8, -1,),SKL_MALLETS,_2mallet,ID_GREATHAMMER,),
    # great clubs         $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,For,Gp,Ba,),TYPE,script,ID,
"plastic great club"    :(3,    2.7, 450, PLAS,26,2, (5,  11, 7,  -2, 2,  2,  -33,12, -26,2,  32, 1.4,18, 6, -2,),SKL_BLUDGEONS,_heavyClub,ID_GREATCLUB,),
"wooden great club"     :(18,   2.6, 1000,WOOD,24,2, (6,  15, 9,  -2, 3,  2,  -27,12, -26,3,  29, 1.4,18, 6, -2,),SKL_BLUDGEONS,_heavyClub,ID_GREATCLUB,),
"stone great club"      :(22,   2.5, 280, STON,26,2, (7,  19, 10, -2, 3,  2,  -24,12, -26,4,  29, 1.0,18, 6, -2,),SKL_BLUDGEONS,_heavyClub,ID_GREATCLUB,),
"bone great club"       :(13,   1.75,360, BONE,22,2, (8,  14, 9,  -1, 3,  2,  -15,12, -26,5,  26, 1.2,18, 6, -2,),SKL_BLUDGEONS,_heavyClub,ID_GREATCLUB,),
"metal great club"      :(95,   1.8, 1900,METL,24,2, (8,  21, 12, -1, 3,  2,  -18,12, -26,6,  26, 1.2,18, 6, -2,),SKL_BLUDGEONS,_heavyClub,ID_GREATCLUB,),
    # great axes          $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,For,Gp,Ba,),TYPE,script,ID,
"plastic great axe"     :(3,    2.2, 110, PLAS,14,8, (2,  14, 9,  1,  2,  2,  -27,12, -6, 3,  24, 2.5,4,  6, -3,),SKL_GREATAXES,_pGreatAxe,ID_GREATAXE,),
"wooden great axe"      :(22,   1.9, 210, WOOD,12,8, (3,  18, 10, 2,  3,  2,  -21,12, -6, 4,  23, 2.5,4,  6, -3,),SKL_GREATAXES,_wGreatAxe,ID_GREATAXE,),
"stone great axe"       :(15,   2.0, 230, WOOD,12,9, (3,  24, 12, 1,  3,  2,  -27,12, -6, 5,  23, 2.5,3,  6, -3,),SKL_GREATAXES,_sGreatAxe,ID_GREATAXE,),
"bone great axe"        :(34,   1.85,290, WOOD,12,9, (3,  22, 11, 2,  3,  2,  -21,12, -6, 6,  22, 2.5,3,  6, -3,),SKL_GREATAXES,_bGreatAxe,ID_GREATAXE,),
"glass great axe"       :(75,   1.65,10,  WOOD,12,11,(5,  32, 10, 2,  3,  2,  -12,12, -6, 7,  18, 2.5,1,  6, -3,),SKL_GREATAXES,_gGreatAxe,ID_GREATAXE,),
"metal great axe"       :(92,   1.8, 420, WOOD,12,10,(4,  28, 14, 2,  3,  2,  -24,12, -6, 8,  20, 2.5,2,  6, -3,),SKL_GREATAXES,_mGreatAxe,ID_GREATAXE,),
    # battleaxes          $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,For,Gp,Ba,),TYPE,script,ID,
    # misc 2-h weapons    $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,For,Gp,Ba,),TYPE,script,ID,
"dane axe"              :(275,  1.6, 300, WOOD,10,12,(6,  22, 12, 3,  3,  3,  6,  8,  -2, 12, 16, 2,  0,  8, 1,),SKL_GREATAXES,_daneAxe,ID_GREATAXE,),#STEEL and IRON
"executioner sword"     :(380,  3.1, 665, METL,28,4, (2,  20, 8,  0,  4,  1,  -45,22, -12,1,  32, 2.4,10, 4, -4,),SKL_LONGSWORDS,_executionerSword,ID_GREATSWORD,),#POOR STEEL

# TOOLS #

# misc                    $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,For,Gp,Ba,),TYPE,script,ID,
'scalpel'               :(30,   0.02,10,  METL,1, 10,(0,  3,  12, 0,  0,  0,  0,  2,  -9, 0,  4,  0,  -20,2, 0,),SKL_SURGERY,_scalpel,ID_SCALPEL,),
"sharpening stone"      :(10,   2.5, 200, STON,24,8, (0,  3,  3,  0,  0,  0,  -60,3,  -12,0,  24, 0,  0,  0, 0,),None,_sChunk,ID_WHETSTONE,),
# scissors                $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,For,Gp,Ba,),TYPE,script,ID,
'scissors'              :(11,   0.16,140, METL,1, 8, (0,  4,  5,  0,  0,  0,  0,  2,  -9, 0,  8,  0,  -6, 2, 0,),None,_scissors,ID_SCISSORS,),
# pliers                  $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,For,Gp,Ba,),TYPE,script,ID,
'pliers'                :(24,   0.3, 650, METL,3, 6, (-2, 2,  4,  0,  0,  0,  -36,2,  -9, 0,  8,  0,  -2, 2, 0,),None,_pliers,ID_PLIERS,),
'needle-nose pliers'    :(32,   0.3, 500, METL,2, 6, (-2, 1,  3,  0,  0,  0,  -36,2,  -9, 0,  8,  0,  -4, 2, 0,),None,_needleNosePliers,ID_PLIERS,),
# screwdrivers            $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,For,Gp,Ba,),TYPE,script,ID,
'metal screwdriver'     :(16,   0.25,250, METL,3, 4, (0,  3,  4,  0,  0,  0,  0,  2,  -9, 0,  8,  0,  -2, 4, 0,),None,_screwdriver,ID_SCREWDRIVER,),
# Allen wrenches          $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,For,Gp,Ba,),TYPE,script,ID,
'metal Allen wrench'    :(8,    0.1, 300, METL,1, 8, (0,  1,  2,  0,  0,  0,  0,  1,  -12,0,  4,  0,  -20,0, 0,),None,_allenwrench,ID_TOOL,),
# shovels                 $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,For,Gp,Ba,),TYPE,script,ID,
"metal shovel"          :(45,   1.8, 400, WOOD,20,2, (-2, 10, 8,  0,  2,  1,  -60,12, -8, 0,  24, 2.6,8,  8, 0,),None,_mShovel,ID_SHOVEL,),
# pickaxes                $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,For,Gp,Ba,),TYPE,script,ID,
"metal pickaxe"         :(59,   1.4, 800, WOOD,16,6, (-8, 12, 14, 0,  2,  0.5,-84,14, -6, 0,  36, 1.4,2,  8, 0,),None,_mPickaxe,ID_PICKAXE,),
# hammers                 $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,For,Gp,Ba,),TYPE,script,ID,
"plastic hammer"        :(1.5,  1.4, 200, PLAS,14,2, (1,  3,  6,  0,  0,  0,  -15,4,  -10,0,  18, 1,  4,  6, 0,),SKL_HAMMERS,_1hammer,ID_HAMMER,),
"wooden hammer"         :(12,   1.3, 260, WOOD,13,2, (1,  4,  7,  0,  0,  0,  -12,4,  -8, 0,  17, 1,  4,  6, 0,),SKL_HAMMERS,_2hammer,ID_HAMMER,),
"stone hammer"          :(8,    1.2, 300, WOOD,12,4, (1,  5,  8,  0,  0,  0,  -12,4,  -8, 0,  16, 1,  4,  6, 0,),SKL_HAMMERS,_2hammer,ID_HAMMER,),
"bone hammer"           :(16,   1.1, 350, WOOD,11,4, (1,  4,  9,  0,  0,  0,  -9, 4,  -6, 0,  16, 1,  4,  6, 0,),SKL_HAMMERS,_2hammer,ID_HAMMER,),
"metal hammer"          :(44,   1.0, 500, WOOD,10,6, (2,  7,  11, 0,  0,  0,  -9, 4,  -4, 0,  15, 1,  4,  6, 0,),SKL_HAMMERS,_3hammer,ID_HAMMER,),
"metal smithing hammer" :(95,   1.6, 990, METL,16,8, (2,  7,  11, 0,  0,  0,  -9, 4,  -10,0,  20, 1,  5,  6, 0,),SKL_HAMMERS,_4hammer,ID_HAMMER,),# to get higher hammer levels, make higher quality versions of this item
# axes                    $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,For,Gp,Ba,),TYPE,script,ID,
"plastic axe"           :(4,    1.9, 80,  PLAS,18,3, (0,  6,  4,  0,  0,  0,  -51,6,  -5, 0,  18, 1,  2,  6, 0,),SKL_AXES,_pAxe,ID_AXE,),
"wooden axe"            :(22,   1.8, 120, WOOD,17,4, (0,  8,  5,  0,  0,  0,  -48,6,  -5, 0,  17, 1,  2,  6, 0,),SKL_AXES,_wAxe,ID_AXE,),
"stone axe"             :(18,   1.75,200, WOOD,16,5, (0,  10, 6,  0,  0,  0,  -42,6,  -5, 0,  17, 1,  1,  6, 0,),SKL_AXES,_sAxe,ID_AXE,),
"bone axe"              :(26,   1.85,160, WOOD,16,6, (0,  9,  6,  0,  0,  0,  -45,6,  -5, 0,  18, 1,  1,  6, 0,),SKL_AXES,_bAxe,ID_AXE,),
"metal axe"             :(42,   1.7, 420, WOOD,15,8, (1,  12, 7,  0,  0,  0,  -36,6,  -5, 0,  16, 1,  0,  6, 0,),SKL_AXES,_mAxe,ID_AXE,),
# machetes                $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,Rea,For,Gp,Ba,),TYPE,script,ID,
"plastic machete"       :(5,    1.8, 70,  PLAS,17,6, (2,  3,  3,  0,  0,  0,  3,  6,  -7, 0,  20, 1,  -2, 7, 0,),SKL_SWORDS,_pMachete,ID_MACHETE,),
"wooden machete"        :(13,   1.7, 90,  WOOD,16,7, (3,  4,  5,  0,  0,  0,  6,  6,  -7, 0,  18, 1,  -3, 7, 0,),SKL_SWORDS,_wMachete,ID_MACHETE,),
"bone machete"          :(16,   1.6, 60,  BONE,15,8, (3,  5,  7,  0,  0,  0,  9,  5,  -7, 0,  14, 1,  -5, 7, 0,),SKL_SWORDS,_bMachete,ID_MACHETE,),
"metal machete"         :(20,   1.5, 260, METL,14,9, (4,  6,  9,  1,  0,  0,  15, 5,  -7, 0,  14, 1,  -6, 7, 0,),SKL_SWORDS,_mMachete,ID_MACHETE,),
}
