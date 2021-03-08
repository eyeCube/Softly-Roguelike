
# body parts pieces

i=1;
BPP_MUSCLE      =i;i+=1;
BPP_SKIN        =i;i+=1;
BPP_BONE        =i;i+=1;
BPP_HEART       =i;i+=1;
BPP_LUNG        =i;i+=1;
BPP_GUTS        =i;i+=1;
BPP_BRAIN       =i;i+=1;
BPP_TEETH       =i;i+=1;
BPP_VISUAL      =i;i+=1;
BPP_AUDITORY    =i;i+=1;
BPP_GUSTATORY   =i;i+=1;
BPP_OLFACTORY   =i;i+=1;
BPP_ARTERY      =i;i+=1;
BPP_FACE        =i;i+=1;
BPP_HAIR        =i;i+=1;

# body part statuses

# rule: the higher the value of the constant, the higher priority it has
#   when deciding whether to overwrite a status with another

i=0;
BONESTATUS_NORMAL       =i;i+=1;
BONESTATUS_DAMAGED      =i;i+=1; # bone is damaged, susceptible to fracture or breakage
BONESTATUS_FRACTURED    =i;i+=1; # hairline fracture
BONESTATUS_CRACKED      =i;i+=1; # badly cracked
BONESTATUS_BROKEN       =i;i+=1; # fully broken in two
BONESTATUS_MULTIBREAKS  =i;i+=1; # fully broken in multiple places
BONESTATUS_SHATTERED    =i;i+=1; # shattered; broken into several pieces
BONESTATUS_MANGLED      =i;i+=1; # mullered; bone is in utter ruin
NBONESTATUSES           = i - 1; # don't count the normal status
BONEFLAG_DISLOCATED = 1 # bone is out of socket

i=0;
MUSCLESTATUS_NORMAL     =i;i+=1;
MUSCLESTATUS_SORE       =i;i+=1; # muscle is sore from a workout or from massaging out knots
MUSCLESTATUS_KNOTTED    =i;i+=1; # muscle has knots that need massage
MUSCLESTATUS_CONTUSION  =i;i+=1; # bruised
MUSCLESTATUS_STRAINED   =i;i+=1; # muscle mildly torn
MUSCLESTATUS_TORN       =i;i+=1; # muscle badly torn
MUSCLESTATUS_BURNED     =i;i+=1; # surface muscle burn
MUSCLESTATUS_RIPPED     =i;i+=1; # muscle is mostly ripped in half
MUSCLESTATUS_DEEPBURNED =i;i+=1; # deep / widespread muscle burn
MUSCLESTATUS_RUPTURED   =i;i+=1; # ruptured tendon or fully ripped in half muscle belly
MUSCLESTATUS_MANGLED    =i;i+=1; # muscle is in utter ruin
NMUSCLESTATUSES         = i - 1; # don't count the normal status
MUSCLEFLAG_DAMAGED = 1 # muscle is damaged, prone to injury
MUSCLEFLAG_SCARRED = 2 # scarred from damage

i=0;
ARTERYSTATUS_NORMAL     =i;i+=1;
ARTERYSTATUS_CLOGGED    =i;i+=1; # clogged, not working at full capacity
ARTERYSTATUS_OPEN       =i;i+=1; # artery opened, causing massive bleeding
ARTERYSTATUS_CUT        =i;i+=1; # fully cut, requiring urgent surgery
ARTERYSTATUS_MANGLED    =i;i+=1; # fully ruined
NARTERYSTATUSES         = i - 1; # don't count the normal status

i=0;
SKINSTATUS_NORMAL       =i;i+=1;
SKINSTATUS_RASH         =i;i+=1; # irritation / inflammation
SKINSTATUS_BLISTER      =i;i+=1; # severe inflammation / sore or pus/fluid sac
SKINSTATUS_SCRAPED      =i;i+=1; # very mild abrasion (a boo-boo)
SKINSTATUS_MINORABRASION=i;i+=1; # mild abrasion
SKINSTATUS_CUT          =i;i+=1; # cut open
SKINSTATUS_MAJORABRASION=i;i+=1; # serious deep and/or wide-ranging scrape
SKINSTATUS_BURNED       =i;i+=1; # skin is burned at the surface level (overwrite cuts and abrasions)
SKINSTATUS_DEEPCUT      =i;i+=1; # deeply cut to the muscle
SKINSTATUS_MULTIDEEPCUTS=i;i+=1; # deeply cut to the muscle in several places
SKINSTATUS_SKINNED      =i;i+=1; # skin is partially removed
SKINSTATUS_DEEPBURNED   =i;i+=1; # skin is burned at a deep level (overwrite all of the above)
SKINSTATUS_FULLYSKINNED =i;i+=1; # skin is fully / almost fully removed
SKINSTATUS_MANGLED      =i;i+=1; # skin is fully ruined
NSKINSTATUSES           = i - 1; # don't count the normal status
SKINFLAG_CALLOUSES = 1 # toughened up from work
SKINFLAG_THICC_CALLOUSES = 2 # GREATLY toughened up from work (having both 1&2 indicates leather-like skin)
SKINFLAG_SCARRED = 4 # scarred from damage

i=0;
BRAINSTATUS_NORMAL      =i;i+=1; # swelling brain is a status effect, not a brain status
BRAINSTATUS_CONTUSION   =i;i+=1; # brain bruise - mild injury
BRAINSTATUS_CONCUSSION  =i;i+=1; # concussion - altered mental state maybe unconciousness
BRAINSTATUS_DAMAGE      =i;i+=1; # temporary brain damage
BRAINSTATUS_PERMDAMAGE  =i;i+=1; # permanent brain damage
BRAINSTATUS_MAJORDAMAGE =i;i+=1; # MAJOR permanent brain damage
BRAINSTATUS_DEAD        =i;i+=1; # braindead
BRAINSTATUS_MANGLED     =i;i+=1; # ruined
NBRAINSTATUSES          = i - 1; # don't count the normal status

i=0;
HAIRSTATUS_NORMAL       =i;i+=1;
HAIRSTATUS_SINGED       =i;i+=1; # minor burn
HAIRSTATUS_BURNED       =i;i+=1; # badly burned
HAIRSTATUS_DAMAGE       =i;i+=1; # minor damage to hair
HAIRSTATUS_PERMDAMAGE   =i;i+=1; # permanent follicle damage
HAIRSTATUS_MANGLED      =i;i+=1; # ruined
# removed hair == no hair (status==NORMAL and length==0)
NHAIRSTATUSES           = i - 1; # don't count the normal status

i=0;
HEARTSTATUS_NORMAL      =i;i+=1;
HEARTSTATUS_SCARRED     =i;i+=1;
HEARTSTATUS_DAMAGE      =i;i+=1; # temporary damage
HEARTSTATUS_PERMDAMAGE  =i;i+=1; # permanent damage
HEARTSTATUS_MAJORDAMAGE =i;i+=1; # major permanent damage
HEARTSTATUS_MANGLED     =i;i+=1; # ruined
NHEARTSTATUSES          = i - 1; # don't count the normal status

i=0;
LUNGSTATUS_NORMAL       =i;i+=1;
LUNGSTATUS_IRRITATED    =i;i+=1; # lung inflamed
LUNGSTATUS_CLOGGED      =i;i+=1; # can't breathe; lung clogged up with something
LUNGSTATUS_DAMAGE       =i;i+=1; # temporary damage
LUNGSTATUS_PERMDAMAGE   =i;i+=1; # permanent damage
LUNGSTATUS_MAJORDAMAGE  =i;i+=1; # major permanent damage
LUNGSTATUS_MANGLED      =i;i+=1; # ruined
NLUNGSTATUSES           = i - 1; # don't count the normal status

i=0;
GUTSSTATUS_NORMAL       =i;i+=1;
GUTSSTATUS_UPSET        =i;i+=1; # might cause vomiting / diarrhea
GUTSSTATUS_SICK         =i;i+=1; # likely to cause vomiting / diarrhea
GUTSSTATUS_ILL          =i;i+=1; # guaranteed to cause vomiting / diarrhea
GUTSSTATUS_DAMAGE       =i;i+=1; # temporary damage
GUTSSTATUS_PERMDAMAGE   =i;i+=1; # permanent damage
GUTSSTATUS_MAJORDAMAGE  =i;i+=1; # major permanent damage
GUTSSTATUS_MANGLED      =i;i+=1; # ruined
NGUTSSTATUSES           = i - 1; # don't count the normal status

# string names for body part statuses

BONESTATUSES={
BONESTATUS_DAMAGED      : "damaged",
BONESTATUS_FRACTURED    : "fractured",
BONESTATUS_CRACKED      : "cracked",
BONESTATUS_BROKEN       : "broken",
BONESTATUS_MULTIBREAKS  : "multiple breaks",
BONESTATUS_SHATTERED    : "shattered",
BONESTATUS_MANGLED      : "mutilated",
}
BONEFLAGS={
BONEFLAG_DISLOCATED     : "dislocated",
}
MUSCLESTATUSES={
MUSCLESTATUS_SORE       : "sore",
MUSCLESTATUS_KNOTTED    : "knotted",
MUSCLESTATUS_CONTUSION  : "bruised",
MUSCLESTATUS_STRAINED   : "strained",
MUSCLESTATUS_TORN       : "torn",
MUSCLESTATUS_RIPPED     : "severely torn",
MUSCLESTATUS_RUPTURED   : "ruptured",
MUSCLESTATUS_BURNED     : "burned",
MUSCLESTATUS_DEEPBURNED : "severely burned",
MUSCLESTATUS_MANGLED    : "mutilated",
}
MUSCLEFLAGS={
MUSCLEFLAG_DAMAGED      : "damaged",
MUSCLEFLAG_SCARRED      : "scarred",
}
ARTERYSTATUSES={
ARTERYSTATUS_CLOGGED    : "clogged",
ARTERYSTATUS_OPEN       : "cut open",
ARTERYSTATUS_CUT        : "severed",
ARTERYSTATUS_MANGLED    : "mutilated",
}
SKINSTATUSES={
SKINSTATUS_RASH         : "inflamed",
SKINSTATUS_BLISTER      : "blistered",
SKINSTATUS_SCRAPED      : "scraped",
SKINSTATUS_MINORABRASION: "abrased",
SKINSTATUS_CUT          : "cut",
SKINSTATUS_MAJORABRASION: "severely abrased",
SKINSTATUS_BURNED       : "burned",
SKINSTATUS_DEEPCUT      : "deep cut",
SKINSTATUS_MULTIDEEPCUTS: "multiple deep cuts",
SKINSTATUS_SKINNED      : "skinned",
SKINSTATUS_DEEPBURNED   : "severely burned",
SKINSTATUS_FULLYSKINNED : "fully skinned",
SKINSTATUS_MANGLED      : "mutilated",
}
SKINFLAGS={
SKINFLAG_CALLOUSES      : "calloused",
SKINFLAG_THICC_CALLOUSES: "calloused",
SKINFLAG_SCARRED        : "scarred",
}
BRAINSTATUSES={
BRAINSTATUS_CONTUSION   : "bruised",
BRAINSTATUS_CONCUSSION  : "concussed",
BRAINSTATUS_DAMAGE      : "damaged",
BRAINSTATUS_PERMDAMAGE  : "permanently damaged",
BRAINSTATUS_MAJORDAMAGE : "severely permanently damaged",
BRAINSTATUS_DEAD        : "dead",
BRAINSTATUS_MANGLED     : "mutilated",
}
HAIRSTATUSES={
HAIRSTATUS_SINGED       : "singed or shaved",
HAIRSTATUS_BURNED       : "burned",
HAIRSTATUS_DAMAGE       : "temporary follicle damage",
HAIRSTATUS_PERMDAMAGE   : "permanent follicle damage",
HAIRSTATUS_MANGLED      : "mutilated",
}
HEARTSTATUSES={
HEARTSTATUS_SCARRED     : "scarred",
HEARTSTATUS_DAMAGE      : "damaged",
HEARTSTATUS_PERMDAMAGE  : "permanently damaged",
HEARTSTATUS_MAJORDAMAGE : "severely permanently damaged",
HEARTSTATUS_MANGLED     : "mutilated",
}
LUNGSTATUSES={
LUNGSTATUS_IRRITATED    : "irritated",
LUNGSTATUS_CLOGGED      : "inflamed",
LUNGSTATUS_DAMAGE       : "damaged",
LUNGSTATUS_PERMDAMAGE   : "permanently damaged",
LUNGSTATUS_MAJORDAMAGE  : "severely permanently damaged",
LUNGSTATUS_MANGLED      : "mutilated",
}
GUTSSTATUSES={
GUTSSTATUS_UPSET        : "upset",
GUTSSTATUS_SICK         : "sick",
GUTSSTATUS_ILL          : "severely sick",
GUTSSTATUS_DAMAGE       : "damaged",
GUTSSTATUS_PERMDAMAGE   : "permanently damaged",
GUTSSTATUS_MAJORDAMAGE  : "severely permanently damaged",
GUTSSTATUS_MANGLED      : "mutilated",
}


# skin
ADDMODS_BPP_SKINSTATUS = { # stat : value
    # (intensity is the preference value: higher intensity overwrites lower intensity effects since only one can exist at a time.)
SKINSTATUS_RASH         :{'resbio':-1, 'respain':-2, 'resbleed':-1, 'resfire':-1,},
SKINSTATUS_SCRAPED      :{'resbio':-2, 'respain':-3, 'resbleed':-2, 'resfire':-1,},
SKINSTATUS_MINORABRASION:{'resbio':-3, 'respain':-5, 'resbleed':-3, 'resfire':-2,},
SKINSTATUS_CUT          :{'resbio':-6, 'respain':-5, 'resbleed':-6, 'resfire':-2,},
SKINSTATUS_MAJORABRASION:{'resbio':-6, 'respain':-10,'resbleed':-6, 'resfire':-3,},
SKINSTATUS_BURNED       :{'resbio':-6, 'respain':-10,'resbleed':-6, 'resfire':-6,},
SKINSTATUS_DEEPCUT      :{'resbio':-12,'respain':-10,'resbleed':-8, 'resfire':-6,},
SKINSTATUS_MULTIDEEPCUTS:{'resbio':-15,'respain':-15,'resbleed':-10,'resfire':-8,},
SKINSTATUS_SKINNED      :{'resbio':-15,'respain':-15,'resbleed':-10,'resfire':-10,},
SKINSTATUS_DEEPBURNED   :{'resbio':-18,'respain':-15,'resbleed':-10,'resfire':-20,},
SKINSTATUS_FULLYSKINNED :{'resbio':-20,'respain':-20,'resbleed':-15,'resfire':-20,},
SKINSTATUS_MANGLED      :{'resbio':-20,'respain':-20,'resbleed':-15,'resfire':-20,},
}

# torso
ADDMODS_BPP_TORSO_MUSCLESTATUS = { # stat : value
MUSCLESTATUS_SORE       :{'respain':-3,},
MUSCLESTATUS_KNOTTED    :{'msp':-3,'asp':-3,'respain':-5,},
MUSCLESTATUS_CONTUSION  :{'msp':-3,'asp':-3,'respain':-5,'resbleed':-4,},
MUSCLESTATUS_STRAINED   :{'atk':-1,'dfn':-1,  'msp':-3, 'asp':-3, 'gra':-1,'respain':-5, 'resbleed':-4,},
MUSCLESTATUS_TORN       :{'atk':-2,'dfn':-1.5,'msp':-6, 'asp':-6, 'gra':-2,'respain':-10,'resbleed':-8,},
MUSCLESTATUS_BURNED     :{'atk':-2,'dfn':-1.5,'msp':-6, 'asp':-6, 'gra':-2,'respain':-15,'resbleed':-12,},
MUSCLESTATUS_RIPPED     :{'atk':-3,'dfn':-2,  'msp':-9, 'asp':-9, 'gra':-3,'respain':-15,'resbleed':-12,},
MUSCLESTATUS_DEEPBURNED :{'atk':-3,'dfn':-2,  'msp':-9, 'asp':-9, 'gra':-3,'respain':-20,'resbleed':-16,},
MUSCLESTATUS_RUPTURED   :{'atk':-4,'dfn':-2.5,'msp':-12,'asp':-12,'gra':-4,'respain':-20,'resbleed':-16,},
MUSCLESTATUS_MANGLED    :{'atk':-4,'dfn':-3,  'msp':-15,'asp':-15,'gra':-5,'respain':-25,'resbleed':-20,},
}
ADDMODS_BPP_TORSO_BONESTATUS = { # stat : value
BONESTATUS_FRACTURED    :{'respain':-10,},
BONESTATUS_CRACKED      :{'respain':-20,},
BONESTATUS_BROKEN       :{'respain':-40,},
BONESTATUS_MULTIBREAKS  :{'respain':-80,},
BONESTATUS_SHATTERED    :{'respain':-100,},
BONESTATUS_MANGLED      :{'respain':-100,},
}
ADDMODS_BPP_TORSO_BONEFLAGS = { # stat : value
BONEFLAG_DISLOCATED     :{'respain':-10,},
}
MULTMODS_BPP_TORSO_BONESTATUS = { # stat : value
BONESTATUS_FRACTURED    :{'agi':0.9,},
BONESTATUS_CRACKED      :{'agi':0.8,'asp':0.9,'msp':0.9,},
BONESTATUS_BROKEN       :{'agi':0.7,'asp':0.8,'msp':0.8,},
BONESTATUS_MULTIBREAKS  :{'agi':0.6,'asp':0.7,'msp':0.7,},
BONESTATUS_SHATTERED    :{'agi':0.5,'asp':0.6,'msp':0.6,},
BONESTATUS_MANGLED      :{'agi':0.5,'asp':0.6,'msp':0.6,},
}
MULTMODS_BPP_TORSO_BONEFLAGS = { # stat : value
BONEFLAG_DISLOCATED     :{'agi':0.9,'asp':0.9,'msp':0.9,},
}
# back
ADDMODS_BPP_BACK_MUSCLESTATUS = { # stat : value
MUSCLESTATUS_SORE       :{'respain':-5,},
MUSCLESTATUS_KNOTTED    :{'str':-1,'msp':-3,'asp':-3,'respain':-10,},
MUSCLESTATUS_CONTUSION  :{'str':-1,'msp':-3,'asp':-3,'respain':-10,'resbleed':-4,},
MUSCLESTATUS_STRAINED   :{'con':-1,'str':-2,'atk':-1,'dfn':-1,  'msp':-3, 'asp':-3, 'gra':-1,'respain':-10, 'resbleed':-4,},
MUSCLESTATUS_TORN       :{'con':-2,'str':-3,'atk':-2,'dfn':-1.5,'msp':-6, 'asp':-6, 'gra':-2,'respain':-10,'resbleed':-8,},
MUSCLESTATUS_BURNED     :{'con':-2,'str':-3,'atk':-2,'dfn':-1.5,'msp':-6, 'asp':-6, 'gra':-2,'respain':-15,'resbleed':-12,},
MUSCLESTATUS_RIPPED     :{'con':-4,'str':-4,'atk':-3,'dfn':-2,  'msp':-9, 'asp':-9, 'gra':-3,'respain':-15,'resbleed':-12,},
MUSCLESTATUS_DEEPBURNED :{'con':-4,'str':-4,'atk':-3,'dfn':-2,  'msp':-9, 'asp':-9, 'gra':-3,'respain':-20,'resbleed':-16,},
MUSCLESTATUS_RUPTURED   :{'con':-5,'str':-5,'atk':-4,'dfn':-2.5,'msp':-12,'asp':-12,'gra':-4,'respain':-20,'resbleed':-16,},
MUSCLESTATUS_MANGLED    :{'con':-6,'str':-6,'atk':-5,'dfn':-3,  'msp':-15,'asp':-15,'gra':-5,'respain':-25,'resbleed':-20,},
}
ADDMODS_BPP_BACK_BONESTATUS = { # stat : value
BONESTATUS_FRACTURED    :{'respain':-10,},
BONESTATUS_CRACKED      :{'bal':-2,'respain':-20,},
BONESTATUS_BROKEN       :{'bal':-4,'respain':-40,},
BONESTATUS_MULTIBREAKS  :{'bal':-6,'respain':-80,},
BONESTATUS_SHATTERED    :{'bal':-8,'respain':-100,},
BONESTATUS_MANGLED      :{'bal':-8,'respain':-100,},
}
ADDMODS_BPP_BACK_BONEFLAGS = { # stat : value
BONEFLAG_DISLOCATED     :{'respain':-10,},
}
MULTMODS_BPP_BACK_BONESTATUS = { # stat : value
BONESTATUS_FRACTURED    :{'agi':0.9,},
BONESTATUS_CRACKED      :{'agi':0.8,'asp':0.9,'msp':0.8,},
BONESTATUS_BROKEN       :{'agi':0.6,'asp':0.8,'msp':0.6,},
BONESTATUS_MULTIBREAKS  :{'agi':0.4,'asp':0.7,'msp':0.4,},
BONESTATUS_SHATTERED    :{'agi':0.2,'asp':0.6,'msp':0.2,},
BONESTATUS_MANGLED      :{'agi':0.2,'asp':0.6,'msp':0.2,},
}
MULTMODS_BPP_BACK_BONEFLAGS = { # stat : value
BONEFLAG_DISLOCATED     :{'agi':0.8,},
}

# head
ADDMODS_BPP_HEAD_BONESTATUS = { # stat : value
BONESTATUS_FRACTURED    :{'respain':-10,},
BONESTATUS_CRACKED      :{'respain':-20,},
BONESTATUS_BROKEN       :{'respain':-40,},
BONESTATUS_MULTIBREAKS  :{'respain':-60,},
BONESTATUS_SHATTERED    :{'respain':-80,},
BONESTATUS_MANGLED      :{'respain':-80,},
}
ADDMODS_BPP_HEAD_BONEFLAGS = { # stat : value
BONEFLAG_DISLOCATED     :{'respain':-10,},
}
MULTMODS_BPP_HEAD_BONESTATUS = { # stat : value
BONESTATUS_FRACTURED    :{'int':0.9,'end':0.9,'bal':0.9,'sight':0.9,'mpmax':0.9,},
BONESTATUS_CRACKED      :{'int':0.8,'end':0.8,'bal':0.8,'sight':0.8,'mpmax':0.8,},
BONESTATUS_BROKEN       :{'int':0.7,'end':0.7,'bal':0.7,'sight':0.7,'mpmax':0.7,},
BONESTATUS_MULTIBREAKS  :{'int':0.6,'end':0.6,'bal':0.6,'sight':0.6,'mpmax':0.6,},
BONESTATUS_SHATTERED    :{'int':0.5,'end':0.5,'bal':0.5,'sight':0.5,'mpmax':0.5,},
BONESTATUS_MANGLED      :{'int':0.5,'end':0.5,'bal':0.5,'sight':0.5,'mpmax':0.5,},
}
MULTMODS_BPP_HEAD_BONEFLAGS = { # stat : value
BONEFLAG_DISLOCATED     :{'int':0.9,'end':0.9,'bal':0.9,'sight':0.9,'mpmax':0.9,},
}

# neck
ADDMODS_BPP_NECK_MUSCLESTATUS = { # stat : value
MUSCLESTATUS_SORE       :{'respain':-8,},
MUSCLESTATUS_KNOTTED    :{'asp':-8,'respain':-15,},
MUSCLESTATUS_CONTUSION  :{'asp':-4,'respain':-15,'resbleed':-8,},
MUSCLESTATUS_STRAINED   :{'atk':-2,'dfn':-1,'asp':-5,'gra':-1,'respain':-15,'resbleed':-4,},
MUSCLESTATUS_TORN       :{'atk':-4,'dfn':-2,'asp':-10,'gra':-2,'respain':-20,'resbleed':-8,},
MUSCLESTATUS_BURNED     :{'atk':-4,'dfn':-2,'asp':-10,'gra':-2,'respain':-25,'resbleed':-12,},
MUSCLESTATUS_RIPPED     :{'atk':-6,'dfn':-3,'asp':-15,'gra':-3,'respain':-25,'resbleed':-12,},
MUSCLESTATUS_DEEPBURNED :{'atk':-6,'dfn':-3,'asp':-15,'gra':-3,'respain':-30,'resbleed':-16,},
MUSCLESTATUS_RUPTURED   :{'atk':-8,'dfn':-4,'asp':-20,'gra':-4,'respain':-30,'resbleed':-16,},
MUSCLESTATUS_MANGLED    :{'atk':-10,'dfn':-5,'asp':-25,'gra':-5,'respain':-35,'resbleed':-20,},
MUSCLESTATUS_MANGLED    :{'atk':-10,'dfn':-5,'asp':-25,'gra':-5,'respain':-35,'resbleed':-20,},
}
ADDMODS_BPP_NECK_BONESTATUS = { # stat : value
BONESTATUS_FRACTURED    :{'respain':-20,},
BONESTATUS_CRACKED      :{'respain':-40,},
BONESTATUS_BROKEN       :{'respain':-60,},
BONESTATUS_MULTIBREAKS  :{'respain':-80,},
BONESTATUS_SHATTERED    :{'respain':-100,},
BONESTATUS_MANGLED      :{'respain':-100,},
}
ADDMODS_BPP_NECK_BONEFLAGS = { # stat : value
BONEFLAG_DISLOCATED     :{'respain':-20,},
}
MULTMODS_BPP_NECK_BONESTATUS = { # stat : value
BONESTATUS_FRACTURED    :{'agi':0.9,},
BONESTATUS_CRACKED      :{'agi':0.8,'asp':0.9,'msp':0.9,},
BONESTATUS_BROKEN       :{'agi':0.7,'asp':0.8,'msp':0.8,},
BONESTATUS_MULTIBREAKS  :{'agi':0.6,'asp':0.7,'msp':0.7,},
BONESTATUS_SHATTERED    :{'agi':0.5,'asp':0.6,'msp':0.6,},
BONESTATUS_MANGLED      :{'agi':0.5,'asp':0.6,'msp':0.6,},
}
MULTMODS_BPP_NECK_BONEFLAGS = { # stat : value
BONEFLAG_DISLOCATED     :{'agi':0.9,},
}

# face & mouth & nose
ADDMODS_BPP_FACE_SKINSTATUS = { # stat : value
SKINSTATUS_RASH         :{'beauty':-6, 'intimidation':1, 'resbio':-4, 'respain':-2, 'resbleed':-2, 'resfire':-2,},
SKINSTATUS_SCRAPED      :{'beauty':-2, 'intimidation':1, 'resbio':-6, 'respain':-3, 'resbleed':-4, 'resfire':-3,},
SKINSTATUS_MINORABRASION:{'beauty':-3, 'intimidation':1, 'resbio':-8, 'respain':-5, 'resbleed':-6, 'resfire':-4,},
SKINSTATUS_CUT          :{'beauty':-3, 'intimidation':2, 'resbio':-12,'respain':-5, 'resbleed':-10,'resfire':-4,},
SKINSTATUS_MAJORABRASION:{'beauty':-12,'intimidation':1, 'resbio':-12,'respain':-10,'resbleed':-10,'resfire':-6,},
SKINSTATUS_BURNED       :{'beauty':-12,'intimidation':8, 'resbio':-12,'respain':-10,'resbleed':-10,'resfire':-10,},
SKINSTATUS_DEEPCUT      :{'beauty':-24,'intimidation':8, 'resbio':-25,'respain':-10,'resbleed':-15,'resfire':-6,},
SKINSTATUS_MULTIDEEPCUTS:{'beauty':-32,'intimidation':12,'resbio':-36,'respain':-10,'resbleed':-20,'resfire':-8,},
SKINSTATUS_SKINNED      :{'beauty':-32,'intimidation':16,'resbio':-36,'respain':-10,'resbleed':-20,'resfire':-10,},
SKINSTATUS_DEEPBURNED   :{'beauty':-32,'intimidation':16,'resbio':-36,'respain':-20,'resbleed':-20,'resfire':-20,},
SKINSTATUS_FULLYSKINNED :{'beauty':-64,'intimidation':32,'resbio':-50,'respain':-20,'resbleed':-25,'resfire':-20,},
SKINSTATUS_MANGLED      :{'beauty':-96,'intimidation':48,'resbio':-50,'respain':-20,'resbleed':-25,'resfire':-20,},
}
ADDMODS_BPP_FACE_BONESTATUS = { # stat : value
BONESTATUS_FRACTURED    :{'respain':-16,},
BONESTATUS_CRACKED      :{'respain':-32,'intimidation':-4,'beauty':-8},
BONESTATUS_BROKEN       :{'respain':-48,'intimidation':-8,'beauty':-16,},
BONESTATUS_MULTIBREAKS  :{'respain':-64,'intimidation':-8,'beauty':-24,},
BONESTATUS_SHATTERED    :{'respain':-96,'intimidation':-8,'beauty':-32,},
BONESTATUS_MANGLED      :{'respain':-96,'intimidation':-8,'beauty':-32,},
}
ADDMODS_BPP_FACE_BONEFLAGS = { # stat : value
BONEFLAG_DISLOCATED     :{'respain':-16,'intimidation':-4,'beauty':-8,},
}
ADDMODS_BPP_FACE_MUSCLESTATUS = { # muscles around the face
MUSCLESTATUS_SORE       :{'respain':-5,},
MUSCLESTATUS_KNOTTED    :{'respain':-15,},
MUSCLESTATUS_CONTUSION  :{'respain':-15,'resbleed':-5,},
MUSCLESTATUS_STRAINED   :{'respain':-20,'resbleed':-6,},
MUSCLESTATUS_TORN       :{'respain':-25,'resbleed':-9,},
MUSCLESTATUS_BURNED     :{'respain':-30,'resbleed':-12,},
MUSCLESTATUS_RIPPED     :{'respain':-30,'resbleed':-12,},
MUSCLESTATUS_DEEPBURNED :{'respain':-35,'resbleed':-15,},
MUSCLESTATUS_RUPTURED   :{'respain':-35,'resbleed':-15,},
MUSCLESTATUS_MANGLED    :{'respain':-40,'resbleed':-18,},
}

# brain
ADDMODS_BPP_BRAINSTATUS = { # stat : value
BRAINSTATUS_CONTUSION   :{'atk':-2,'dfn':-2,},
BRAINSTATUS_CONCUSSION  :{'atk':-4,'dfn':-4,},
BRAINSTATUS_DAMAGE      :{'atk':-6,'dfn':-6,},
BRAINSTATUS_PERMDAMAGE  :{'atk':-6,'dfn':-6,},
BRAINSTATUS_MAJORDAMAGE :{'atk':-12,'dfn':-12,},
BRAINSTATUS_MANGLED     :{'atk':-20,'dfn':-20,},
BRAINSTATUS_DEAD        :{'atk':-24,'dfn':-24,},
}
MULTMODS_BPP_BRAINSTATUS = { # stat : value
BRAINSTATUS_CONTUSION   :{'int':0.9,'bal':0.9,'sight':0.9,'hearing':0.9,'mpmax':0.9,},
BRAINSTATUS_CONCUSSION  :{'int':0.8,'bal':0.8,'sight':0.8,'hearing':0.8,'mpmax':0.8,},
BRAINSTATUS_DAMAGE      :{'int':0.7,'bal':0.7,'sight':0.7,'hearing':0.7,'mpmax':0.7,},
BRAINSTATUS_PERMDAMAGE  :{'int':0.6,'bal':0.6,'sight':0.6,'hearing':0.6,'mpmax':0.6,},
BRAINSTATUS_MAJORDAMAGE :{'int':0.3,'bal':0.3,'sight':0.3,'hearing':0.3,'mpmax':0.3,},
BRAINSTATUS_MANGLED     :{'int':0.1,'bal':0.1,'sight':0.1,'hearing':0.1,'mpmax':0.1,},
BRAINSTATUS_DEAD        :{'int':0,'bal':0,'sight':0,'hearing':0,'mpmax':0.1,},
}

# hand
# Hand is more sensitive than most BPs, and adds dex penalty for damage.
# Less resbleed penalty as result of less blood in extremities.
# Hand skin damage -> double resbio penalty than normal.
ADDMODS_BPP_HAND_SKINSTATUS = { # stat : value
SKINSTATUS_RASH         :{'resbio':-2, 'respain':-4, 'resbleed':-1, 'resfire':-1,},
SKINSTATUS_SCRAPED      :{'resbio':-4, 'respain':-6, 'resbleed':-1, 'resfire':-1,},
SKINSTATUS_MINORABRASION:{'resbio':-6, 'respain':-10, 'resbleed':-2, 'resfire':-2,},
SKINSTATUS_CUT          :{'resbio':-12, 'respain':-10, 'resbleed':-3, 'resfire':-2,},
SKINSTATUS_MAJORABRASION:{'dex':-1,'resbio':-12, 'respain':-20,'resbleed':-3, 'resfire':-3,},
SKINSTATUS_BURNED       :{'dex':-1,'resbio':-12, 'respain':-20,'resbleed':-3, 'resfire':-6,},
SKINSTATUS_DEEPCUT      :{'dex':-2,'resbio':-24,'respain':-20,'resbleed':-4, 'resfire':-6,},
SKINSTATUS_MULTIDEEPCUTS:{'dex':-2,'resbio':-30,'respain':-25,'resbleed':-5, 'resfire':-8,},
SKINSTATUS_SKINNED      :{'dex':-2,'resbio':-30,'respain':-30,'resbleed':-5,'resfire':-10,},
SKINSTATUS_DEEPBURNED   :{'dex':-3,'resbio':-36,'respain':-30,'resbleed':-5,'resfire':-20,},
SKINSTATUS_FULLYSKINNED :{'dex':-3,'resbio':-40,'respain':-40,'resbleed':-7,'resfire':-20,},
SKINSTATUS_MANGLED      :{'dex':-3,'resbio':-40,'respain':-40,'resbleed':-9,'resfire':-20,},
}
ADDMODS_BPP_HAND_BONESTATUS = { # stat : value
BONESTATUS_FRACTURED    :{'dex':-1,'atk':-1,'dfn':-1,'gra':-2,'respain':-5,},
BONESTATUS_CRACKED      :{'dex':-2,'atk':-2,'dfn':-2,'gra':-4,'respain':-10,},
BONESTATUS_BROKEN       :{'dex':-3,'atk':-3,'dfn':-3,'gra':-6,'respain':-20,},
BONESTATUS_MULTIBREAKS  :{'dex':-4,'atk':-4,'dfn':-4,'gra':-8,'respain':-30,},
BONESTATUS_SHATTERED    :{'dex':-5,'atk':-5,'dfn':-5,'gra':-10,'respain':-40,},
BONESTATUS_MANGLED      :{'dex':-5,'atk':-5,'dfn':-5,'gra':-10,'respain':-50,},
}
ADDMODS_BPP_HAND_BONEFLAGS = { # stat : value
BONEFLAG_DISLOCATED     :{'dex':-1,'atk':-1,'dfn':-1,'gra':-2,'respain':-5,},
}
ADDMODS_BPP_HAND_MUSCLESTATUS = { # stat : value
MUSCLESTATUS_SORE       :{'respain':-1,},
MUSCLESTATUS_KNOTTED    :{'asp':-3,'respain':-3,},
MUSCLESTATUS_CONTUSION  :{'asp':-3,'respain':-3,'resbleed':-2,},
MUSCLESTATUS_STRAINED   :{'dex':-1,'atk':-1,'dfn':-1,'asp':-5,'gra':-1,'respain':-5,'resbleed':-1,},
MUSCLESTATUS_TORN       :{'dex':-2,'atk':-2,'dfn':-2,'asp':-10,'gra':-2,'respain':-10,'resbleed':-3,},
MUSCLESTATUS_RIPPED     :{'dex':-3,'atk':-3,'dfn':-3,'asp':-15,'gra':-3,'respain':-20,'resbleed':-5,},
MUSCLESTATUS_RUPTURED   :{'dex':-4,'atk':-4,'dfn':-4,'asp':-20,'gra':-4,'respain':-30,'resbleed':-7,},
MUSCLESTATUS_MANGLED    :{'dex':-5,'atk':-5,'dfn':-5,'asp':-25,'gra':-5,'respain':-40,'resbleed':-9,},
}

# arm
ADDMODS_BPP_ARM_BONESTATUS = { # stat : value
BONESTATUS_FRACTURED    :{'atk':-1,'dfn':-1,'gra':-2,'respain':-5,},
BONESTATUS_CRACKED      :{'atk':-2,'dfn':-2,'gra':-4,'respain':-10,},
BONESTATUS_BROKEN       :{'atk':-3,'dfn':-3,'gra':-6,'respain':-15,},
BONESTATUS_MULTIBREAKS  :{'atk':-4,'dfn':-4,'gra':-8,'respain':-20,},
BONESTATUS_SHATTERED    :{'atk':-4,'dfn':-4,'gra':-8,'respain':-25,},
BONESTATUS_MANGLED      :{'atk':-4,'dfn':-4,'gra':-8,'respain':-30,},
}
ADDMODS_BPP_ARM_BONEFLAGS = { # stat : value
BONEFLAG_DISLOCATED     :{'atk':-1,'dfn':-1,'gra':-2,'respain':-5,},
}
ADDMODS_BPP_ARM_MUSCLESTATUS = { # stat : value
MUSCLESTATUS_SORE       :{'respain':-1,},
MUSCLESTATUS_KNOTTED    :{'asp':-3,'respain':-3,},
MUSCLESTATUS_CONTUSION  :{'asp':-3,'respain':-3,'resbleed':-2,},
MUSCLESTATUS_STRAINED   :{'atk':-1,'dfn':-1,'asp':-5,'gra':-1,'respain':-5,'resbleed':-3,},
MUSCLESTATUS_TORN       :{'atk':-2,'dfn':-2,'asp':-10,'gra':-2,'respain':-10,'resbleed':-6,},
MUSCLESTATUS_RIPPED     :{'atk':-3,'dfn':-3,'asp':-15,'gra':-3,'respain':-15,'resbleed':-9,},
MUSCLESTATUS_RUPTURED   :{'atk':-4,'dfn':-4,'asp':-20,'gra':-4,'respain':-20,'resbleed':-12,},
MUSCLESTATUS_MANGLED    :{'atk':-4,'dfn':-4,'asp':-20,'gra':-4,'respain':-25,'resbleed':-15,},
}

# leg
ADDMODS_BPP_LEG_BONESTATUS = { # stat : value
BONESTATUS_FRACTURED    :{'atk':-1,'dfn':-1,'gra':-2,'respain':-10,},
BONESTATUS_CRACKED      :{'atk':-2,'dfn':-2,'gra':-4,'respain':-15,},
BONESTATUS_BROKEN       :{'atk':-3,'dfn':-3,'gra':-6,'respain':-20,},
BONESTATUS_MULTIBREAKS  :{'atk':-4,'dfn':-4,'gra':-8,'respain':-25,},
BONESTATUS_SHATTERED    :{'atk':-4,'dfn':-4,'gra':-8,'respain':-30,},
BONESTATUS_MANGLED      :{'atk':-4,'dfn':-4,'gra':-8,'respain':-35,},
}
ADDMODS_BPP_LEG_BONEFLAGS = { # stat : value
BONEFLAG_DISLOCATED     :{'atk':-1,'dfn':-3,'gra':-3,'respain':-10,},
}
MULTMODS_BPP_LEG_BONESTATUS = { # stat : value
BONESTATUS_FRACTURED    :{'bal':0.9,'msp':0.96,},
BONESTATUS_CRACKED      :{'bal':0.8,'msp':0.8333334,},
BONESTATUS_BROKEN       :{'bal':0.6,'msp':0.6666667,},
BONESTATUS_MULTIBREAKS  :{'bal':0.4,'msp':0.5,},
BONESTATUS_SHATTERED    :{'bal':0.3333334,'msp':0.4,},
BONESTATUS_MANGLED      :{'bal':0.3333334,'msp':0.4,},
}
MULTMODS_BPP_LEG_BONEFLAGS = { # stat : value
BONEFLAG_DISLOCATED     :{'bal':0.8,'msp':0.9,},
}
ADDMODS_BPP_LEG_MUSCLESTATUS = { # stat : value
MUSCLESTATUS_SORE       :{'respain':-1,},
MUSCLESTATUS_KNOTTED    :{'msp':-3,'respain':-3,},
MUSCLESTATUS_CONTUSION  :{'msp':-3,'respain':-3,'resbleed':-2,},
MUSCLESTATUS_STRAINED   :{'bal':-1,'atk':-1,'dfn':-1,'msp':-8,'gra':-1,'respain':-5,'resbleed':-2},
MUSCLESTATUS_TORN       :{'bal':-2,'atk':-2,'dfn':-2,'msp':-16,'gra':-2,'respain':-10,'resbleed':-4},
MUSCLESTATUS_BURNED     :{'bal':-2,'atk':-2,'dfn':-2,'msp':-16,'gra':-2,'respain':-15,'resbleed':-6},
MUSCLESTATUS_RIPPED     :{'bal':-3,'atk':-3,'dfn':-3,'msp':-24,'gra':-3,'respain':-15,'resbleed':-6},
MUSCLESTATUS_DEEPBURNED :{'bal':-3,'atk':-3,'dfn':-3,'msp':-24,'gra':-3,'respain':-20,'resbleed':-8},
MUSCLESTATUS_RUPTURED   :{'bal':-4,'atk':-4,'dfn':-4,'msp':-32,'gra':-4,'respain':-20,'resbleed':-8},
MUSCLESTATUS_MANGLED    :{'bal':-5,'atk':-4,'dfn':-5,'msp':-40,'gra':-5,'respain':-25,'resbleed':-16},
}

    # BPP statuses alt effects #
    
LUNGSTATUS_CAPACITY={
LUNGSTATUS_NORMAL       : 1,
LUNGSTATUS_IRRITATED    : 0.9,
LUNGSTATUS_CLOGGED      : 0.75,
LUNGSTATUS_DAMAGE       : 0.67,
LUNGSTATUS_PERMDAMAGE   : 0.67,
LUNGSTATUS_MAJORDAMAGE  : 0.33,
LUNGSTATUS_MANGLED      : 0,
}

# damage types -> bpp statuses constants | dmgtypes -> bppstatus
# progressive level of damage as index increases
SKINSTATUSES_SPIKES=(
    SKINSTATUS_MAJORABRASION, SKINSTATUS_CUT,
    SKINSTATUS_DEEPCUT, SKINSTATUS_MULTIDEEPCUTS,
    SKINSTATUS_FULLYSKINNED, SKINSTATUS_MANGLED,
    )
SKINSTATUSES_SPUDS=(
    SKINSTATUS_SCRAPED, SKINSTATUS_MINORABRASION,
    SKINSTATUS_MAJORABRASION, SKINSTATUS_SKINNED,
    SKINSTATUS_FULLYSKINNED, SKINSTATUS_MANGLED,
    )
SKINSTATUSES_CUT=(
    SKINSTATUS_MINORABRASION, SKINSTATUS_CUT,
    SKINSTATUS_DEEPCUT, SKINSTATUS_SKINNED,
    SKINSTATUS_FULLYSKINNED, SKINSTATUS_MANGLED,
    )
MUSCLESTATUSES_CUT=(
    MUSCLESTATUS_STRAINED, MUSCLESTATUS_TORN,
    MUSCLESTATUS_RIPPED, MUSCLESTATUS_RUPTURED,
    MUSCLESTATUS_RUPTURED, MUSCLESTATUS_MANGLED,
    )
SKINSTATUSES_PUNCTURE=(
    SKINSTATUS_CUT, SKINSTATUS_DEEPCUT,
    SKINSTATUS_DEEPCUT, SKINSTATUS_DEEPCUT,
    SKINSTATUS_MULTIDEEPCUTS, SKINSTATUS_MULTIDEEPCUTS,
    )
MUSCLESTATUSES_PUNCTURE=(
    MUSCLESTATUS_KNOTTED, MUSCLESTATUS_STRAINED,
    MUSCLESTATUS_TORN, MUSCLESTATUS_RIPPED,
    MUSCLESTATUS_RUPTURED, MUSCLESTATUS_MANGLED,
    )
MUSCLESTATUSES_BLUNT=(
    MUSCLESTATUS_SORE, MUSCLESTATUS_KNOTTED,
    MUSCLESTATUS_CONTUSION, MUSCLESTATUS_STRAINED,
    MUSCLESTATUS_TORN, MUSCLESTATUS_RIPPED,
    )
BONESTATUSES_BLUNT=(
    BONESTATUS_FRACTURED, BONESTATUS_CRACKED,
    BONESTATUS_BROKEN, BONESTATUS_MULTIBREAKS,
    BONESTATUS_SHATTERED, BONESTATUS_MANGLED,
    )
SKINSTATUSES_BURN=(
    SKINSTATUS_BLISTER, SKINSTATUS_BURNED,
    SKINSTATUS_DEEPBURNED, SKINSTATUS_DEEPBURNED,
    SKINSTATUS_FULLYSKINNED, SKINSTATUS_MANGLED,
    )
MUSCLESTATUSES_BURN=(
    MUSCLESTATUS_SORE, MUSCLESTATUS_BURNED,
    MUSCLESTATUS_DEEPBURNED, MUSCLESTATUS_DEEPBURNED,
    MUSCLESTATUS_MANGLED, MUSCLESTATUS_MANGLED,
    )
SKINSTATUSES_ABRASION=(
    SKINSTATUS_SCRAPED, SKINSTATUS_MINORABRASION,
    SKINSTATUS_MAJORABRASION, SKINSTATUS_SKINNED,
    SKINSTATUS_FULLYSKINNED, SKINSTATUS_MANGLED,
    )
MUSCLESTATUSES_ABRASION=(
    MUSCLESTATUS_CONTUSION, MUSCLESTATUS_STRAINED,
    MUSCLESTATUS_TORN, MUSCLESTATUS_RIPPED,
    MUSCLESTATUS_RUPTURED, MUSCLESTATUS_MANGLED,
    )

