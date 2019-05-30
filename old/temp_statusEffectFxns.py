
            # elemental damage #
    # cause status effects

#reduce temperature
def cooldown(obj, amt):
    obj.stats.temp = max(0, obj.stats.temp - amt)
    
#   SICK METER
#bio damage
def disease(obj, dmg):
    res = obj.stats.get('resbio')
    #increase sickness meter
    dmg = int( dmg*(1-(res/100)) )
    obj.stats.sick += max(0, dmg )
    if obj.stats.sick >= 100:
        obj.stats.sick = 100        #cap out sickness meter
        rog.set_status(obj, SICK)
#drunk damage
def intoxicate(obj, dmg):
    res = obj.stats.get('resbio')
    #increase sickness meter
    dmg = int( dmg*(1-(res/100)) )
    obj.stats.sick += max(0, dmg )
    if obj.stats.sick >= 100:
        obj.stats.sick = 100        #cap out sickness meter
        rog.set_status(obj, DRUNK)
        
#   RADS METER
#rad damage
def irradiate(obj, dmg):
    res = obj.stats.get('resbio')
    #increase rads meter
    dmg = int( dmg*(1-(res/100)) )
    obj.stats.rads += max(0, dmg )
    if obj.stats.rads >= 100:
        obj.stats.rads = 0 # reset rads meter after mutation
        rog.mutate(obj)
        
#   EXPOSURE METER
#chem damage
def exposure(obj, dmg):
    res = obj.stats.get('resbio')
    #increase exposure meter
    dmg = int( dmg*(1-(res/100)) )
    obj.stats.expo += max(0, dmg )
    if obj.stats.expo >= 100:
        obj.stats.expo = 0          #reset exposure meter
        rog.hurt(obj, CHEM_DAMAGE)  #instant damage when expo meter fills
        _random_chemical_effect(obj) #inflict chem status effect
#acid
def corrode(obj, dmg):
    res = obj.stats.get('resbio')
    dmg = int(dmg * (1-(res/100)) / 10)
    obj.stats.expo += max(0, dmg)
    if obj.stats.expo >= 100:
        obj.stats.expo = 0          #reset exposure meter
        rog.set_status(obj, ACID)
#coughing
def cough(obj, dmg):
    res = obj.stats.get('resbio')
    dmg = int(dmg * (1-(res/100)) / 10)
    obj.stats.expo += max(0, dmg)
    if obj.stats.expo >= 100:
        obj.stats.expo = 0          #reset exposure meter
        rog.set_status(obj, COUGH)
#vomiting
def vomit(obj, dmg):
    res = obj.stats.get('resbio')
    dmg = int(dmg * (1-(res/100)) / 10)
    obj.stats.expo += max(0, dmg)
    if obj.stats.expo >= 100:
        obj.stats.expo = 0          #reset exposure meter
        rog.set_status(obj, VOMIT)
#irritating
def irritate(obj, dmg):
    res = obj.stats.get('resbio')
    dmg = int(dmg * (1-(res/100)) / 10)
    obj.stats.expo += max(0, dmg)
    if obj.stats.expo >= 100:
        obj.stats.expo = 50 #leave some exposure
        rog.set_status(obj, IRRIT)
        
#   NON-METER ELEMENTAL DAMAGE
#elec damage  
def electrify(obj, dmg):
    res = obj.stats.get('reselec')
    dmg = int(dmg * (1-(res/100)) / 10)
    if dmg:
        rog.hurt(obj, dmg)
        rog.sap(obj, dmg)
    if dmg >= 5:
        rog.paralyze(obj, ELEC_PARALYZETIME) # paralysis from high damage

def mutate(obj):
    if not obj.isCreature: return False
    obj.mutations += 1
    if obj.mutations > 3:
        rog.kill(obj)
    return True
def paralyze(obj, turns):
    if not obj.isCreature: return False
    rog.set_paral(obj, turns)
    return True

# TEMP #

def burn(ent, dmg, maxTemp=FIRE_MAXTEMP):
    if on(ent, DEAD): return False
    if on(ent, WET):
        clear_status(ent, WET)
        #steam=create_fluid(ent.x, ent.y, "steam")
        return False
    res = obj.stats.get('resfire')
    if rog.on(obj, WET):    
        rog.clear_status(obj,WET)    #wet things get dried
        #steam=stuff.create("steam", obj.x, obj.y)
    #increase temperature
    dmg = int( dmg*(1-(res/100)) )
    obj.stats.temp += max(0, dmg )
    obj.stats.temp = min(maxTemp, obj.stats.temp)
    #set burning status
    if (not rog.on(obj, FIRE) and obj.stats.temp >= FIRE_TEMP): #should depend on material?
        rog.set_status(obj, FIRE)
    return True

def cooldown(ent, temp=999):
    if on(ent, DEAD): return False
    stuff.cooldown(ent, temp)

# BIO #

def disease(ent, dmg):
    if on(ent, DEAD): return False
    stuff.disease(ent, dmg)

# EXPOSURE #

def exposure(ent, dmg):
    if on(ent, DEAD): return False
    stuff.exposure(ent, dmg)

def corrode(ent, dmg):
    if on(ent, DEAD): return False
    stuff.corrode(ent, dmg)      #acid damage
def irradiate(ent, dmg):
    if on(ent, DEAD): return False
    stuff.irradiate(ent, dmg)  #rad damage
def intoxicate(ent, dmg):
    if on(ent, DEAD): return False
    stuff.intoxicate(ent, dmg)#drunk damage
def cough(ent, dmg): #coughing fit status
    if on(ent, DEAD): return False
    stuff.cough(ent, dmg)
def vomit(ent, dmg): #vomiting fit status
    if on(ent, DEAD): return False
    stuff.vomit(ent, dmg)

# ELEC #

def electrify(ent, dmg):
    if on(ent, DEAD): return False
    stuff.electrify(ent, dmg)
#paralyze
def paralyze(ent, turns):
    if on(ent, DEAD): return False
    stuff.paralyze(ent, turns)
#mutate
def mutate(ent):
    if on(ent, DEAD): return False
    stuff.mutate(ent)
