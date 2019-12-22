
WEAPONS={ #melee weapons, 1H, 2H and 1/2H

    # TODO:
        # give all weapons more defensive capability
        # skill in varying levels - how do?
        #   IDEA: when you have level 10 skill, you gain stats equal to those in the table.
        #       every 10 levels you gain is worth that same linear growth value for those stats.
        
    # IDEA: weapon class (skill type) affects various things in combat
        # bludgeons do increased damage to armored foes
        # swords do increased damage to unarmored foes

    # 1-handed weapons #

    # cudgels             $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,TYPE,script
"plastic cudgel"        :(2,    1.4, 220, PLAS,9, 2, (2,  2,  5,  0,  1,  1,  -15,9,  -5, 1,  18,),SKL_BLUDGEONS,_pCudgel,),
"wooden cudgel"         :(13,   1.35,375, WOOD,8, 2, (3,  4,  5,  0,  1,  1,  -9, 9,  -5, 1,  17,),SKL_BLUDGEONS,_wCudgel,),
"stone cudgel"          :(10,   1.2, 340, WOOD,7, 2, (3,  6,  6,  0,  1,  1,  -9, 9,  -5, 1,  15,),SKL_BLUDGEONS,_sCudgel,),
"bone cudgel"           :(16,   1.3, 300, WOOD,7, 2, (3,  5,  5,  0,  1,  1,  -9, 9,  -5, 1,  16,),SKL_BLUDGEONS,_bCudgel,),
"glass cudgel"          :(18,   1.3, 5,   WOOD,6, 3, (3,  9,  4,  0,  0,  0,  -6, 9,  -5, 1,  16,),SKL_BLUDGEONS,_gCudgel,),
"metal cudgel"          :(32,   1.2, 650, WOOD,8, 2, (3,  7,  7,  0,  1,  1,  -6, 9,  -5, 1,  15,),SKL_BLUDGEONS,_mCudgel,),
    # clubs               $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,TYPE,script
"plastic club"          :(2,    1.55,275, PLAS,10,2, (2,  3,  4,  0,  2,  1,  -21,9,  -5, 1,  20,),SKL_BLUDGEONS,_pClub,),
"wooden club"           :(10,   1.45,420, WOOD,9, 2, (3,  6,  5,  0,  2,  1,  -15,9,  -5, 1,  18,),SKL_BLUDGEONS,_wClub,),
"stone club"            :(12,   1.3, 500, STON,8, 2, (3,  7,  6,  0,  2,  1,  -12,9,  -5, 1,  18,),SKL_BLUDGEONS,_sClub,),
"bone club"             :(22,   1.4, 365, BONE,8, 2, (4,  7,  7,  0,  2,  1,  -12,9,  -5, 1,  18,),SKL_BLUDGEONS,_bClub,),
"glass club"            :(32,   1.2, 1,   GLAS,7, 3, (3,  10, 5,  0,  0,  0,  -9, 9,  -5, 1,  16,),SKL_BLUDGEONS,_gClub,),
"metal club"            :(59,   1.15,950, METL,9, 2, (3,  8,  8,  0,  1,  1,  -12,9,  -5, 1,  16,),SKL_BLUDGEONS,_mClub,),
    # spiked clubs        $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,TYPE,script
"plastic spiked club"   :(2,    1.6, 50,  PLAS,9, 4, (1,  6,  5,  0,  2,  1,  -36,15, -8, 1,  22,),SKL_BLUDGEONS,_pSpikedClub,),
"wooden spiked club"    :(10,   1.5, 120, WOOD,9, 4, (2,  9,  6,  0,  2,  1,  -33,15, -8, 1,  20,),SKL_BLUDGEONS,_wSpikedClub,),
    # maces               $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,TYPE,script
"plastic mace"          :(2,    1.45,75,  PLAS,8, 3, (2,  6,  5,  0,  1,  1,  -33,12, -6, 1,  18,),SKL_BLUDGEONS,_pMace,),
"wooden mace"           :(20,   1.35,160, WOOD,7, 3, (3,  9,  7,  0,  1,  1,  -27,12, -6, 1,  16,),SKL_BLUDGEONS,_wMace,),
"stone mace"            :(24,   1.3, 220, WOOD,7, 3, (3,  12, 8,  0,  1,  1,  -24,12, -6, 1,  16,),SKL_BLUDGEONS,_sMace,),
"bone mace"             :(27,   1.3, 100, WOOD,7, 3, (4,  10, 9,  0,  1,  1,  -24,12, -6, 1,  16,),SKL_BLUDGEONS,_bMace,),
"glass mace"            :(65,   1.4, 3,   WOOD,7, 4, (3,  24, 7,  0,  0,  0,  -30,12, -6, 1,  14,),SKL_BLUDGEONS,_gMace,),
"metal mace"            :(72,   1.35,325, WOOD,7, 3, (4,  14, 10, 0,  1,  1,  -27,12, -6, 1,  16,),SKL_BLUDGEONS,_mMace,),
    # morning stars       $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,TYPE,script
"metal morning star"    :(75,   1.25,240, METL,7, 2, (4,  16, 12, 0,  1,  1,  -39,12, -7, 1,  20,),SKL_BLUDGEONS,_mMace,),
    # warhammers          $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,TYPE,script
"plastic warhammer"     :(2,    1.4, 190, PLAS,8, 4, (1,  4,  10, 0,  0,  0,  -24,6,  -5, 1,  18,),SKL_HAMMERS,_pWarhammer,),
"wooden warhammer"      :(24,   1.35,280, WOOD,8, 4, (2,  5,  13, 0,  0,  0,  -21,6,  -5, 1,  16,),SKL_HAMMERS,_wWarhammer,),
"stone warhammer"       :(18,   1.3, 200, WOOD,7, 4, (2,  7,  15, 0,  0,  0,  -21,6,  -5, 1,  18,),SKL_HAMMERS,_sWarhammer,),
"bone warhammer"        :(28,   1.15,260, WOOD,7, 4, (2,  6,  14, 0,  0,  0,  -15,6,  -5, 1,  16,),SKL_HAMMERS,_bWarhammer,),
"metal warhammer"       :(51,   1.25,500, WOOD,7, 4, (2,  8,  16, 0,  0,  0,  -18,6,  -5, 1,  16,),SKL_HAMMERS,_mWarhammer,),
    # war axes            $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,TYPE,script
"plastic war axe"       :(2,    1.35,60,  PLAS,6, 5, (1,  8,  4,  1,  0,  0,  -12,9,  -2, 2,  18,),SKL_AXES,_pWarAxe,),
"wooden war axe"        :(26,   1.3, 90,  WOOD,6, 5, (2,  10, 7,  1,  0,  0,  -9, 9,  -2, 2,  16,),SKL_AXES,_wWarAxe,),
"stone war axe"         :(22,   1.25,120, WOOD,6, 5, (2,  12, 8,  1,  0,  0,  -15,9,  -2, 2,  18,),SKL_AXES,_sWarAxe,),
"bone war axe"          :(32,   1.25,180, WOOD,6, 5, (2,  11, 9,  1,  0,  0,  -6, 9,  -2, 2,  16,),SKL_AXES,_bWarAxe,),
"metal war axe"         :(62,   1.2, 260, WOOD,6, 5, (3,  14, 10, 1,  0,  0,  -12,9,  -2, 2,  15,),SKL_AXES,_mWarAxe,),
    # tomahawks           $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,TYPE,script
"plastic tomahawk"      :(2,    1.1, 20,  PLAS,5, 5, (1,  6,  7,  1,  0,  0,  -21,6,  -2, 3,  16,),SKL_AXES,_pTomahawk,),
"wooden tomahawk"       :(12,   0.9, 40,  WOOD,4, 6, (2,  7,  9,  1,  0,  0,  -18,6,  -2, 3,  15,),SKL_AXES,_wTomahawk,),
"stone tomahawk"        :(16,   1.1, 80,  WOOD,5, 5, (2,  9,  10, 1,  0,  0,  -24,6,  -2, 3,  16,),SKL_AXES,_sTomahawk,),
"bone tomahawk"         :(23,   0.95,60,  WOOD,4, 6, (2,  8,  11, 1,  0,  0,  -18,6,  -2, 3,  15,),SKL_AXES,_bTomahawk,),
"metal tomahawk"        :(40,   1.0, 120, WOOD,4, 6, (2,  11, 12, 1,  0,  0,  -21,6,  -2, 3,  14,),SKL_AXES,_mTomahawk,),
    # Shivs               $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,TYPE,script
"plastic shiv"          :(0,    0.3, 15,  PLAS,1, 4, (2,  2,  7,  0,  0,  0,  42, 1,  -5, 1,  5,),SKL_KNIVES,_pShiv,),
"wooden shiv"           :(0,    0.3, 20,  WOOD,1, 4, (2,  3,  8,  0,  0,  0,  48, 1,  -5, 1,  4,),SKL_KNIVES,_wShiv,),
"stone shiv"            :(0,    0.25,40,  STON,1, 4, (3,  4,  9,  0,  0,  0,  45, 1,  -5, 1,  5,),SKL_KNIVES,_sShiv,),
"bone shiv"             :(0,    0.2, 35,  BONE,1, 4, (3,  4,  10, 0,  0,  0,  51, 1,  -5, 1,  4,),SKL_KNIVES,_bShiv,),
"glass shiv"            :(1,    0.15,1,   GLAS,1, 5, (5,  6,  8,  0,  0,  0,  63, 1,  -5, 1,  2,),SKL_KNIVES,_gShiv,),
"metal shiv"            :(6,    0.2, 50,  METL,1, 4, (4,  4,  12, 0,  0,  0,  54, 1,  -5, 1,  3,),SKL_KNIVES,_mShiv,),
"ceramic shiv"          :(2,    0.22,10,  CERA,1, 5, (5,  8,  9,  0,  0,  0,  60, 1,  -5, 1,  2,),SKL_KNIVES,_cShiv,),#"a ceramic knife will shatter if dropped on the ground."
    # knives              $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,TYPE,script
"plastic knife"         :(0,    0.2, 35,  PLAS,1, 2, (3,  2,  10, 0,  0,  0,  48, 1,  -3, 2,  7,),SKL_KNIVES,_pKnife,),
"wooden knife"          :(2,    0.15,60,  WOOD,1, 2, (3,  3,  14, 0,  0,  0,  54, 1,  -3, 2,  5,),SKL_KNIVES,_wKnife,),
"stone knife"           :(6,    0.15,110, STON,1, 2, (4,  5,  16, 0,  0,  0,  51, 1,  -3, 2,  6,),SKL_KNIVES,_sKnife,),
"bone knife"            :(5,    0.12,90,  BONE,1, 3, (4,  5,  18, 0,  0,  0,  57, 1,  -3, 2,  5,),SKL_KNIVES,_bKnife,),
"glass knife"           :(12,   0.08,1,   GLAS,1, 4, (6,  8,  12, 0,  0,  0,  66, 1,  -3, 2,  3,),SKL_KNIVES,_gKnife,),
"metal knife"           :(14,   0.15,200, METL,1, 3, (5,  5,  20, 0,  0,  0,  60, 1,  -3, 3,  4,),SKL_KNIVES,_mKnife,),
"ceramic knife"         :(20,   0.12,15,  CERA,1, 4, (6,  10, 14, 0,  0,  0,  66, 1,  -3, 2,  3,),SKL_KNIVES,_cKnife,),#"a ceramic knife will shatter if dropped on the ground."
    # serrated knives     $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,TYPE,script
"plastic serrated knife":(0,    0.18,15,  PLAS,1, 4, (2,  3,  8,  0,  0,  0,  24, 1,  -4, 2,  8,),SKL_KNIVES,_pSerrated,),
"wooden serrated knife" :(4,    0.13,35,  WOOD,1, 4, (2,  4,  11, 0,  0,  0,  30, 1,  -4, 2,  6,),SKL_KNIVES,_wSerrated,),
"stone serrated knife"  :(8,    0.13,60,  STON,1, 4, (3,  6,  12, 0,  0,  0,  27, 1,  -4, 2,  7,),SKL_KNIVES,_sSerrated,),
"bone serrated knife"   :(7,    0.1, 45,  BONE,1, 5, (3,  6,  13, 0,  0,  0,  33, 1,  -4, 2,  6,),SKL_KNIVES,_bSerrated,),
"metal serrated knife"  :(18,   0.13,100, METL,1, 5, (4,  7,  15, 0,  0,  0,  30, 1,  -4, 3,  5,),SKL_KNIVES,_mSerrated,),
    # war knives          $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,TYPE,script
"plastic war knife"     :(1,    0.55,50,  PLAS,3, 6, (3,  3,  12, 1,  0,  0,  51, 1,  -2, 3,  6,),SKL_KNIVES,_pWarKnife,),
"wooden war knife"      :(5,    0.45,80,  WOOD,2, 7, (4,  4,  16, 1,  0,  0,  57, 1,  -2, 3,  5,),SKL_KNIVES,_wWarKnife,),
"bone war knife"        :(10,   0.5, 125, BONE,3, 8, (5,  6,  18, 1,  0,  0,  54, 1,  -2, 3,  5,),SKL_KNIVES,_bWarKnife,),
"glass war knife"       :(28,   0.32,10,  GLAS,2, 9, (7,  10, 16, 1,  0,  0,  78, 1,  -2, 4,  4,),SKL_KNIVES,_gWarKnife,),
"metal war knife"       :(26,   0.42,250, METL,2, 8, (6,  7,  20, 2,  0,  0,  69, 1,  -2, 5,  4,),SKL_KNIVES,_mWarKnife,),
"ceramic war knife"     :(35,   0.35,20,  CERA,2, 9, (7,  10, 16, 1,  0,  0,  78, 1,  -2, 4,  4,),SKL_KNIVES,_cWarKnife,),
    # daggers             $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,TYPE,script
"bone dagger"           :(10,   0.35,115, BONE,2, 4, (4,  6,  21, 1,  0,  0,  69, 2,  -2, 3,  5,),SKL_KNIVES,_bDagger,),
"glass dagger"          :(28,   0.22,5,   GLAS,2, 7, (6,  12, 18, 1,  0,  0,  90, 2,  -2, 3,  4,),SKL_KNIVES,_gDagger,),
"metal dagger"          :(30,   0.3, 190, METL,2, 6, (5,  7,  24, 2,  0,  0,  75, 2,  -2, 4,  4,),SKL_KNIVES,_mDagger,),
"rondel dagger"         :(70,   0.4, 320, METL,3, 7, (4,  8,  28, 2,  0,  0,  54, 2,  -2, 3,  5,),SKL_KNIVES,_rondelDagger,),#STEEL
    # bayonets            $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,TYPE,script
"plastic bayonet"       :(0,    0.45,40,  PLAS,3, 4, (2,  2,  10, 0,  0,  0,  36, 1,  -3, 2,  7,),SKL_KNIVES,_pBayonet,),
"wooden bayonet"        :(5,    0.4, 70,  WOOD,3, 4, (3,  3,  14, 0,  0,  0,  33, 1,  -3, 2,  6,),SKL_KNIVES,_wBayonet,),
"bone bayonet"          :(8,    0.3, 100, BONE,3, 4, (3,  5,  16, 0,  0,  0,  39, 1,  -3, 2,  5,),SKL_KNIVES,_bBayonet,),
"metal bayonet"         :(22,   0.35,225, METL,3, 5, (4,  5,  18, 0,  0,  0,  36, 1,  -3, 3,  6,),SKL_KNIVES,_mBayonet,),
    # javelins            $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,TYPE,script
"plastic javelin"       :(1,    0.85,35,  PLAS,7, 2, (6,  4,  7,  0,  0,  0,  -24,9,  -6, 3,  12,),SKL_JAVELINS,_pJavelin,),
"wooden javelin"        :(8,    0.9, 50,  WOOD,7, 2, (8,  6,  10, 0,  0,  0,  -27,9,  -6, 3,  10,),SKL_JAVELINS,_wJavelin,),
"metal javelin"         :(32,   0.5, 200, METL,5, 3, (9,  8,  12, 0,  0,  0,  -18,9,  -6, 3,  8,),SKL_JAVELINS,_mJavelin,),
    # shortspears         $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,TYPE,script
"plastic shortspear"    :(1,    1.0, 15,  PLAS,5, 1, (6,  5,  6,  0,  0,  0,  -12,9,  -8, 5,  8,),SKL_JAVELINS,_pShortSpear,),
"wooden shortspear"     :(5,    1.05,30,  WOOD,5, 1, (7,  7,  8,  0,  0,  0,  -12,9,  -8, 5,  8,),SKL_JAVELINS,_wShortSpear,),
"stone shortspear"      :(5,    1.1, 65,  WOOD,5, 1, (7,  9,  10, 0,  0,  0,  -15,9,  -8, 5,  9,),SKL_JAVELINS,_sShortSpear,),
"bone shortspear"       :(15,   1.05,100, WOOD,5, 2, (7,  8,  9,  0,  0,  0,  -12,9,  -8, 5,  8,),SKL_JAVELINS,_bShortSpear,),
"glass shortspear"      :(25,   0.9, 5,   WOOD,4, 3, (9,  12, 7,  0,  0,  0,  -9, 9,  -8, 5,  7,),SKL_JAVELINS,_gShortSpear,),
"metal shortspear"      :(22,   1.0, 135, WOOD,5, 2, (8,  10, 12, 0,  0,  0,  -12,9,  -8, 5,  8,),SKL_JAVELINS,_mShortSpear,),
"ceramic shortspear"    :(28,   0.95,10,  CERA,4, 3, (9,  14, 9,  0,  0,  0,  -9, 9,  -8, 5,  7,),SKL_JAVELINS,_cShortSpear,),
    # boomerangs          $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,TYPE,script
"plastic boomerang"     :(1,    0.7, 20,  PLAS,11,2, (2,  2,  3,  0,  0,  0,  -15,6,  -6, 1,  16,),SKL_BLUDGEONS,_pBoomerang,),
"wooden boomerang"      :(4,    0.5, 30,  WOOD,9, 3, (3,  4,  5,  0,  0,  0,  -12,6,  -4, 1,  16,),SKL_BLUDGEONS,_wBoomerang,),
"bone boomerang"        :(5,    0.45,25,  BONE,7, 4, (3,  4,  5,  0,  0,  0,  -9, 3,  -4, 1,  16,),SKL_BLUDGEONS,_bBoomerang,),
"glass boomerang"       :(22,   0.5, 1,   GLAS,6, 6, (5,  7,  4,  0,  0,  0,  -9, 3,  -4, 1,  10,),SKL_BLUDGEONS,_gBoomerang,),
"metal boomerang"       :(25,   0.4, 90,  METL,5, 5, (4,  5,  6,  0,  0,  0,  -6, 3,  -4, 2,  12,),SKL_BLUDGEONS,_mBoomerang,),
"ceramic boomerang"     :(38,   0.4, 1,   CERA,5, 6, (5,  8,  4,  0,  0,  0,  -9, 3,  -3, 1,  10,),SKL_BLUDGEONS,_cBoomerang,),
    # bucklers            $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,TYPE,script
"plastic buckler"       :(2,    1.7, 30,  PLAS,8, 3, (1,  1,  1,  5,  1,  1,  -9, 6,  -3, 3,  12,),SKL_SHIELDS,_buckler,),
"wooden buckler"        :(12,   1.65,75,  WOOD,8, 4, (1,  2,  3,  6,  1,  1,  -6, 6,  -3, 4,  12,),SKL_SHIELDS,_buckler,),
"bone buckler"          :(24,   0.8, 40,  BONE,5, 3, (2,  3,  4,  6,  1,  1,  -3, 6,  -2, 5,  9,),SKL_SHIELDS,_buckler,),#made of one large bone sculpted into shape + some leather
"metal buckler"         :(90,   1.5, 150, METL,7, 5, (2,  5,  5,  7,  2,  1,  -6, 6,  -3, 6,  10,),SKL_SHIELDS,_buckler,),
    # rotellas            $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,TYPE,script
"plastic rotella"       :(4,    4.0, 50,  PLAS,13,3, (2,  2,  1,  5,  2,  2,  -33,9,  -6, 4,  24,),SKL_SHIELDS,_rotella,),
"wooden rotella"        :(24,   3.6, 115, WOOD,12,3, (3,  3,  2,  6,  2,  2,  -27,9,  -5, 6,  24,),SKL_SHIELDS,_rotella,),
"bone rotella"          :(49,   3.4, 75,  BONE,12,3, (3,  5,  3,  5,  2,  2,  -24,9,  -4, 6,  22,),SKL_SHIELDS,_rotella,),#made of one, two or three big pieces of bone glued together. The pieces of bone (esp. for 1 or 2-piece rotellas) are difficult to acquire and manufacture for shield use so this is a relatively expensive item.
"metal rotella"         :(175,  3.0, 240, METL,11,4, (3,  7,  4,  6,  3,  2,  -18,9,  -4, 7,  22,),SKL_SHIELDS,_rotella,),
    # shields             $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,TYPE,script
"wicker shield"         :(20,   4.2, 35,  WOOD,13,2, (1,  2,  0,  4,  2,  2,  -36,12, -10,4,  30,),SKL_SHIELDS,_shield,),
"plastic shield"        :(7,    6.5, 80,  PLAS,18,2, (1,  3,  0,  3,  2,  3,  -54,12, -12,5,  38,),SKL_SHIELDS,_shield,),
"wooden shield"         :(75,   5.25,180, WOOD,16,3, (3,  5,  1,  4,  3,  3,  -45,12, -10,7,  32,),SKL_SHIELDS,_shield,),
"bone shield"           :(145,  6.2, 100, BONE,17,3, (2,  7,  2,  4,  4,  2,  -48,12, -8, 7,  36,),SKL_SHIELDS,_shield,),
"boiled leather shield" :(190,  5.05,120, BOIL,14,3, (3,  4,  1,  5,  4,  3,  -42,12, -12,6,  32,),SKL_SHIELDS,_shield,),
"metal shield"          :(380,  6.0, 360, METL,16,3, (2,  9,  3,  4,  5,  3,  -51,12, -6, 8,  36,),SKL_SHIELDS,_shield,),
    # scutums             $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,TYPE,script
"plastic scutum"        :(10,   9.8, 80,  PLAS,23,1, (-1, 2,  -6, 2,  3,  3,  -69,15, -12,6,  44,),SKL_SHIELDS,_scutum,),
"wooden scutum"         :(120,  8.7, 180, WOOD,21,1, (1,  4,  -5, 3,  4,  3,  -57,15, -10,7,  44,),SKL_SHIELDS,_scutum,),
"bone scutum"           :(255,  9.3, 100, BONE,22,1, (0,  5,  -2, 3,  5,  2,  -60,15, -8, 8,  48,),SKL_SHIELDS,_scutum,),
"boiled leather scutum" :(305,  7.7, 120, BOIL,19,1, (1,  4,  -3, 4,  5,  3,  -54,15, -12,8,  44,),SKL_SHIELDS,_scutum,),
"metal scutum"          :(495,  8.1, 360, METL,20,1, (0,  6,  -1, 3,  6,  3,  -63,15, -6, 8,  48,),SKL_SHIELDS,_scutum,),
    # tower shields       $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,TYPE,script
"plastic tower shield"  :(15,   13.5,140, PLAS,30,0, (-3, 2,  -12,-6, 4,  5,  -81,18, -32,7,  72,),SKL_SHIELDS,_towerShield,),
"wooden tower shield"   :(165,  12.0,400, WOOD,28,0, (-2, 2,  -12,-5, 5,  6,  -72,18, -30,8,  66,),SKL_SHIELDS,_towerShield,),
"bone tower shield"     :(360,  12.7,320, BONE,29,0, (-2, 3,  -6, -6, 6,  4,  -81,18, -28,9,  72,),SKL_SHIELDS,_towerShield,),
"metal tower shield"    :(620,  10.8,800, METL,26,0, (-1, 4,  -6, -4, 8,  6,  -75,18, -24,9,  62,),SKL_SHIELDS,_towerShield,),
"riot shield"           :(1060, 8.2, 250, PLAS,18,1, (0,  2,  -9, -3, 7,  6,  -69,18, -20,10, 52,),SKL_SHIELDS,_towerShield,),
    # whips / bullwhips   $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,TYPE,script
"rubber flail"          :(2,    0.1, 3,   RUBB,1, 3, (-8, 3,  2,  0,  0,  0,  -51,1,  -1, 0,  1,),None,_rubberBandWhip,),#2h only. This is a heavy metal ball attached to a rubber band like a primitive flail.
"rubber whip"           :(6,    0.3, 30,  RUBB,2, 5, (4,  1,  0,  0,  0,  0,  -15,1,  -10,1,  7,),SKL_BLUDGEONS,_whip,),
"plastic duel whip"     :(2,    1.6, 90,  PLAS,9, 2, (2,  2,  2,  0,  0,  0,  -30,3,  -6, 1,  16,),SKL_BLUDGEONS,_heavyWhip,),
"leather duel whip"     :(75,   1.45,150, LETH,7, 2, (2,  3,  4,  0,  0,  0,  -24,3,  -10,1,  20,),SKL_BLUDGEONS,_heavyWhip,),
"leather bullwhip"      :(40,   0.6, 60,  LETH,5, 12,(-5, 4,  2,  0,  0,  0,  -51,1,  -5, 0,  5,),SKL_BULLWHIPS,_bullWhip,),
"graphene bullwhip"     :(7500, 0.5, 1800,CARB,3, 16,(-2, 5,  5,  0,  0,  0,  -42,1,  -5, 0,  4,),SKL_BULLWHIPS,_bullWhip,),
    # swords              $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,TYPE,script
"plastic sword"         :(2,    1.2, 30,  PLAS,8, 5, (4,  3,  6,  1,  0,  0,  15, 6,  -7, 3,  12,),SKL_SWORDS,_pSword,),
"wooden sword"          :(22,   1.1, 50,  WOOD,7, 6, (6,  4,  9,  2,  0,  0,  24, 6,  -6, 4,  10,),SKL_SWORDS,_wSword,),
"bone sword"            :(51,   0.75,40,  BONE,4, 7, (5,  5,  12, 1,  0,  0,  21, 6,  -5, 4,  6,),SKL_SWORDS,_bSword,),
"metal sword"           :(65,   1.0, 120, METL,5, 8, (7,  6,  14, 2,  0,  0,  39, 6,  -4, 5,  8,),SKL_SWORDS,_mSword,),
"diamonite sword"       :(2650, 0.9, 400, METL,4, 12,(8,  9,  18, 3,  0,  0,  51, 6,  -4, 7,  7,),SKL_SWORDS,_dSword,),
"graphene sword"        :(11500,0.8, 1200,CARB,3, 10,(9,  12, 22, 3,  0,  0,  60, 3,  -3, 9,  8,),SKL_SWORDS,_grSword,),
    # other swords        $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,TYPE,script
"leaf blade"            :(45,   0.7, 180, METL,3, 10,(6,  6,  13, 2,  0,  0,  42, 3,  -3, 2,  8,),SKL_SWORDS,_leafSword,),
"hanger"                :(60,   0.8, 90,  METL,3, 6, (10, 4,  11, 4,  0,  0,  54, 6,  -3, 4,  6,),SKL_SWORDS,_hanger,),#POOR STEEL
"messer"                :(90,   1.4, 210, METL,6, 4, (5,  6,  10, 3,  1,  1,  30, 9,  -3, 3,  12,),SKL_SWORDS,_messer,),#POOR STEEL
"smallsword"            :(105,  0.4, 40,  METL,1, 12,(8,  3,  11, 4,  0,  0,  69, 3,  -6, 8,  4,),SKL_SWORDS,_smallSword,),#STEEL
"curved sword"          :(120,  1.1, 80,  METL,4, 16,(7,  6,  7,  3,  0,  0,  54, 9,  -2, 6,  8,),SKL_SWORDS,_curvedSword,),#POOR STEEL
"broadsword"            :(130,  1.3, 240, METL,7, 6, (5,  8,  12, 2,  0,  0,  24, 9,  -5, 2,  15,),SKL_SWORDS,_broadsword,),#POOR STEEL
"cutlass"               :(130,  1.35,450, METL,7, 10,(6,  6,  10, 3,  0,  1,  39, 9,  -2, 6,  15,),SKL_SWORDS,_cutlass,),#POOR STEEL, made entirely of metal (no wood)
"sabre"                 :(135,  1.25,200, METL,8, 12,(8,  6,  9,  4,  0,  0,  48, 9,  -4, 5,  12,),SKL_SWORDS,_sabre,),#POOR STEEL
"falchion"              :(160,  1.4, 345, METL,8, 8, (5,  8,  11, 1,  1,  0,  18, 9,  -5, 3,  16,),SKL_SWORDS,_falchion,),#POOR STEEL
"arming sword"          :(235,  1.35,260, METL,9, 14,(8,  7,  16, 2,  0,  0,  42, 9,  -4, 5,  10,),SKL_SWORDS,_armingSword,),#STEEL
"basket-hilted sword"   :(295,  1.45,220, METL,10,16,(9,  5,  12, 3,  1,  2,  51, 12, -6, 7,  14,),SKL_SWORDS,_basketHiltedSword,),#STEEL
"rapier"                :(345,  1.5, 110, METL,11,10,(11, 5,  15, 5,  0,  1,  60, 12, -7, 8,  20,),SKL_SWORDS,_rapier,),#STEEL
    # other misc weapons  $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,TYPE,script
    # knives
"kukri"                 :(70,   0.5, 90,  METL,3, 3, (4,  6,  8,  1,  0,  0,  51, 3,  -3, 5,  6,),SKL_KNIVES,_kukri,),#POOR STEEL
"metal throwing knife"  :(8,    0.1, 20,  METL,1, 8, (5,  3,  16, 0,  0,  0,  54, 1,  -8, 1,  4,),SKL_KNIVES,_mThrowingKnife,),
"metal butcher knife"   :(16,   0.3, 120, METL,3, 2, (2,  5,  3,  0,  0,  0,  12, 1,  -10,1,  8,),SKL_KNIVES,_butcherKnife,),
    # boxing weapons
"metal knuckles"        :(6,    0.1, 320, METL,2, 2, (2,  4,  4,  0,  0,  0,  18, 1,  -6, 0,  16,),SKL_BOXING,_knuckles,),
"metal spiked knuckles" :(14,   0.2, 150, METL,2, 2, (2,  5,  6,  0,  0,  0,  6,  1,  -8, 0,  24,),SKL_BOXING,_knuckles,),
"boxing wrap"           :(4,    0.25,20,  CLTH,2, 3, (2,  2,  1,  1,  0,  0,  33, 1,  -8, 2,  12,),SKL_BOXING,_boxingWraps,),
    # bludgeons
"metal baton"           :(25,   0.5, 175, METL,2, 3, (4,  3,  5,  1,  0,  0,  9,  3,  -2, 3,  4,),SKL_BLUDGEONS,_baton,),
"metal bat"             :(35,   0.7, 220, METL,4, 1, (3,  6,  6,  0,  1,  0,  -6, 6,  -8, 1,  8,),SKL_BLUDGEONS,_baton,),
"wooden truncheon"      :(4,    0.85,250, WOOD,4, 2, (3,  5,  6,  1,  0,  0,  -3, 3,  -6, 2,  12,),SKL_BLUDGEONS,_club,),
"metal truncheon"       :(46,   0.75,500, METL,4, 3, (3,  7,  8,  1,  0,  0,  6,  3,  -4, 2,  10,),SKL_BLUDGEONS,_club,),
    # misc
"metal push dagger"     :(30,   0.3, 180, METL,2, 4, (3,  9,  15, 0,  0,  0,  90, 1,  -12,0,  12,),SKL_PUSHDAGGERS,_pushDagger,), 
"crescent moon blade"   :(125,  0.3, 60,  METL,2, 14,(2,  4,  8,  1,  0,  0,  75, 1,  -4, 1,  4,),None,_crescentBlade,), 
##"scissors katar"     :(25,   0.3, 180, METL,2,(3,  9,  15, 0,  0,  0,  90, 0,  -12,0,  4,),SKL_PUSHDAGGERS,_pushDagger,), 

    # 2-handed weapons #

# Some weapons can only be built with steel, like longswords, greatswords.
#   So these are expensive, and have no material designation.
    # longswords          $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,TYPE,script
"bastard sword"         :(245,  1.55,300, METL,16,6, (4,  9,  12, 1,  1,  1,  15, 12, -10,6,  24,),SKL_LONGSWORDS,_bastardSword,),#STEEL # weapon is a longsword but can be wielded in 1 hand (which it is by default due to the mechanics in this game)
"longsword"             :(260,  1.6, 210, METL,7, 8, (10, 12, 18, 5,  3,  3,  51, 12, -8, 12, 12,),SKL_LONGSWORDS,_longSword,),#STEEL
"kriegsmesser"          :(265,  1.8, 250, METL,11,4, (9,  14, 14, 2,  3,  3,  36, 15, -12,9,  20,),SKL_LONGSWORDS,_kriegsmesser,),#STEEL
"katana"                :(285,  1.45,80,  METL,5, 10,(11, 11, 16, 3,  2,  2,  45, 9,  -8, 14, 9,),SKL_LONGSWORDS,_katana,),#STEEL # VERY DIFFICULT TO FIND RECIPE FOR THIS/VERY DIFFICULT TO MAKE! SO VERY EXPENSIVE
"estoc"                 :(305,  1.65,100, METL,6, 12,(12, 10, 20, 6,  1,  2,  60, 12, -8, 16, 16,),SKL_LONGSWORDS,_estoc,),#STEEL
    # greatswords         $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,TYPE,script
"greatsword"            :(540,  3.5, 450, METL,22,10,(9,  18, 15, 3,  3,  3,  -15,42, -10,10,26,),SKL_GREATSWORDS,_greatSword,),
"flamberge"             :(595,  3.3, 225, METL,21,12,(10, 16, 12, 2,  3,  3,  -12,42, -13,10, 25,),SKL_GREATSWORDS,_flamberge,),
    # short staves        $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,TYPE,script
"plastic staff"         :(1,    1.3, 100, PLAS,8, 8, (6,  5,  4,  4,  2,  3,  69, 18, -5, 13, 11,),SKL_STAVES,_staff,),
"wooden staff"          :(10,   1.2, 300, WOOD,8, 8, (7,  7,  6,  4,  4,  3,  75, 18, -4, 15, 10,),SKL_STAVES,_staff,),
"metal staff"           :(62,   1.0, 500, METL,8, 8, (8,  9,  8,  4,  3,  3,  81, 18, -3, 16, 9,),SKL_STAVES,_staff,),
    # longstaves          $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,TYPE,script
"plastic longstaff"     :(2,    2.45,150, PLAS,14,10,(8,  8,  6,  3,  2,  3,  54, 36, -24,5,  22,),SKL_POLEARMS,_longstaff,),
"wooden longstaff"      :(16,   2.25,400, WOOD,13,10,(9,  10, 8,  3,  4,  3,  57, 36, -21,6,  21,),SKL_POLEARMS,_longstaff,),
"metal longstaff"       :(88,   2.05,500, METL,12,10,(10, 12, 10, 3,  3,  3,  60, 36, -18,7,  20,),SKL_POLEARMS,_longstaff,),
    # spears              $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,TYPE,script
"plastic spear"         :(2,    2.1, 30,  PLAS,8, 8, (8,  10, 10, 3,  2,  3,  51, 30, -17,8,  16,),SKL_SPEARS,_pSpear,),
"wooden spear"          :(20,   2.05,60,  WOOD,8, 8, (10, 11, 12, 3,  3,  3,  48, 30, -15,9,  15,),SKL_SPEARS,_wSpear,),
"stone spear"           :(22,   2.15,100, WOOD,9, 8, (9,  13, 13, 3,  3,  3,  42, 30, -15,9,  16,),SKL_SPEARS,_bSpear,),
"bone spear"            :(25,   2.05,150, WOOD,8, 8, (10, 12, 14, 3,  3,  3,  45, 30, -16,10, 16,),SKL_SPEARS,_sSpear,),
"glass spear"           :(34,   1.9, 5,   WOOD,7, 9, (12, 22, 10, 3,  3,  3,  51, 30, -16,14, 14,),SKL_SPEARS,_gSpear,),
"metal spear"           :(32,   2.1, 200, WOOD,9, 8, (11, 14, 16, 3,  3,  3,  45, 30, -14,12, 16,),SKL_SPEARS,_mSpear,),
"metal winged spear"    :(40,   2.0, 300, WOOD,10,10,(10, 16, 15, 3,  3,  3,  36, 30, -8, 12, 20,),SKL_SPEARS,_mSpear,),
"ceramic spear"         :(36,   1.95,10,  WOOD,7, 9, (12, 24, 12, 3,  3,  3,  48, 30, -16,14, 14,),SKL_SPEARS,_cSpear,),
    # partizans           $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,TYPE,script
"metal partizan"        :(57,   2.2, 240, WOOD,14,6, (8,  18, 14, 2,  3,  3,  24, 36, -14,10, 22,),SKL_SPEARS,_mPartizan,),
    # naginatas           $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,TYPE,script
"metal naginata"        :(72,   2.6, 140, WOOD,15,8, (9,  12, 13, 2,  3,  2,  15, 45, -14,10, 22,),SKL_SPEARS,_mNaginata,),
    # bills               $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,TYPE,script
"metal bill"            :(84,   2.2, 160, WOOD,13,11,(12, 14, 18, 2,  3,  2,  24, 51, -10,10, 18,),SKL_POLEARMS,_mBill,),#requires some steel
    # halberds            $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,TYPE,script
"metal halberd"         :(75,   2.25,180, WOOD,15,10,(8,  18, 20, 2,  3,  2,  9,  54, -6, 6,  22,),SKL_POLEARMS,_mHalberd,),#all polearms have REACH
    # poleaxes            $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,TYPE,script
"metal poleaxe"         :(58,   2.35,300, WOOD,12,9, (7,  22, 20, 2,  3,  2,  -15,36, -6, 7,  24,),SKL_POLEARMS,_mPoleAxe,),
    # polehammers         $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,TYPE,script
"plastic polehammer"    :(3,    2.7, 110, PLAS,15,9, (4,  11, 16, 1,  2,  2,  -27,30, -14,3,  30,),SKL_POLEARMS,_pPoleHammer,),
"wooden polehammer"     :(18,   2.6, 200, WOOD,14,10,(5,  13, 16, 1,  2,  2,  -24,30, -12,4,  28,),SKL_POLEARMS,_wPoleHammer,),
"metal polehammer"      :(45,   2.4, 475, WOOD,13,11,(6,  16, 24, 1,  3,  2,  -21,30, -9, 5,  26,),SKL_POLEARMS,_mPoleHammer,),
    # war mallets         $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,TYPE,script
"plastic war mallet"    :(3,    2.4, 320, PLAS,12,3, (3,  11, 12, -1, 2,  2,  -45,24, -20,3,  28,),SKL_MALLETS,_1mallet,),
"wooden war mallet"     :(19,   2.3, 600, WOOD,11,3, (4,  13, 13, -1, 3,  2,  -42,24, -20,4,  25,),SKL_MALLETS,_1mallet,),
"stone war mallet"      :(22,   2.1, 400, WOOD,10,3, (5,  17, 14, 0,  3,  2,  -36,24, -16,4,  25,),SKL_MALLETS,_1mallet,),
"bone war mallet"       :(25,   2.2, 500, WOOD,10,3, (4,  15, 15, 0,  3,  2,  -39,24, -18,5,  25,),SKL_MALLETS,_1mallet,),
"metal war mallet"      :(72,   2.0, 800, WOOD,9, 3, (5,  19, 16, 0,  3,  2,  -39,24, -14,6,  22,),SKL_MALLETS,_2mallet,),
    # great clubs         $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,TYPE,script
"plastic great club"    :(3,    2.7, 450, PLAS,18,2, (5,  11, 7,  -1, 2,  2,  -33,33, -32,2,  32,),SKL_BLUDGEONS,_heavyClub,),
"wooden great club"     :(18,   2.6, 1000,WOOD,18,2, (6,  15, 9,  -1, 3,  2,  -27,33, -28,3,  29,),SKL_BLUDGEONS,_heavyClub,),
"stone great club"      :(22,   2.5, 280, STON,17,2, (7,  19, 10, -1, 3,  2,  -24,33, -28,4,  29,),SKL_BLUDGEONS,_heavyClub,),
"bone great club"       :(13,   1.75,360, BONE,15,2, (8,  14, 9,  0,  3,  2,  -15,33, -26,5,  26,),SKL_BLUDGEONS,_heavyClub,),
"metal great club"      :(95,   1.8, 1800,METL,16,2, (8,  21, 12, 0,  3,  2,  -18,33, -24,6,  26,),SKL_BLUDGEONS,_heavyClub,),
    # great axes          $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,TYPE,script
"plastic great axe"     :(3,    2.2, 110, PLAS,11,8, (2,  14, 9,  1,  2,  2,  -27,33, -16,3,  24,),SKL_GREATAXES,_pGreatAxe,),
"wooden great axe"      :(22,   1.9, 210, WOOD,10,8, (3,  18, 10, 2,  3,  2,  -21,33, -18,4,  23,),SKL_GREATAXES,_wGreatAxe,),
"stone great axe"       :(15,   2.0, 230, WOOD,10,8, (3,  24, 12, 1,  3,  2,  -27,33, -18,5,  23,),SKL_GREATAXES,_sGreatAxe,),
"bone great axe"        :(34,   1.85,290, WOOD,9, 8, (3,  22, 11, 2,  3,  2,  -21,33, -14,6,  22,),SKL_GREATAXES,_bGreatAxe,),
"glass great axe"       :(75,   1.65,10,  WOOD,7, 9, (5,  32, 10, 2,  3,  2,  -12,33, -18,7,  18,),SKL_GREATAXES,_gGreatAxe,),
"metal great axe"       :(92,   1.8, 420, WOOD,9, 8, (4,  28, 14, 2,  3,  2,  -24,33, -9, 8,  20,),SKL_GREATAXES,_mGreatAxe,),
    # battleaxes          $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,TYPE,script
    # misc 2-h weapons    $$$$, Kg,  Dur, Mat, St,Dx,(Acc,Dam,Pen,DV, AV, Pro,Asp,Enc,Gra,Ctr,Sta,TYPE,script
"dane axe"              :(175,  1.6, 300, WOOD,6, 12,(6,  22, 12, 3,  3,  3,  6,  24, -5, 12, 16,),SKL_GREATAXES,_daneAxe,),#STEEL and IRON
"executioner sword"     :(1180, 4.7, 665, METL,44,4, (2,  32, 8,  -4, 4,  1,  -75,45, -40,1,  96,),SKL_GREATSWORDS,_executionerSword,),#POOR STEEL
}
    
