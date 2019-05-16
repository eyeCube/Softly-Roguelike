
    def __init__(self):
        super(Manager_Status, self).__init__()

        self.statuses={}
        self.statMods={}
        #for every status, make a dict
        for k in STATUSES.keys():
            self.statuses.update( {k : {}} )
        #copy statuses into statMods so they look the same
        for k,v in self.statuses.items():
            self.statMods.update( {k : v} )
        

    #add a status effect to an object
    def add(self, ent, status, dur=-1):
        if dur == 0: return False
        if dur == -1:   #default duration
            dur = self._get_default_duration(status)
        curDur = self.statuses[status].get(ent, 0)
        if curDur:
            if dur <= curDur:   #don't override effect with a lesser duration
                return False    # but you CAN override with a greater duration
            self.remove(obj, status) #remove current status before overriding
        
        #apply the status effect
        self.statuses[status].update( {ent : dur} )
        rog.make(ent, status)   #add flag
        self._apply_statMods(ent, status) # apply attribute modifiers
        self._apply_auxEffects(ent, status) # auxiliary status effects
        self._apply_message(ent, status) #send a message
        return True
    
    #remove an object's status effect
    def remove(self, ent, status):
        if self.statuses[status].get(ent, None):
            del self.statuses[status][ent]
            #if rog.on(obj, status): # HACK
            rog.makenot(ent, status)    #remove flag
            self._remove_statMods(ent, status) # clear attribute modifiers
            self._apply_auxRemoveEffects(ent, status) #aux remove effects
            self._remove_message(ent, status) #send a message
            return True
        return False
    
    #remove all status effects on a given object
    def remove_all(self, ent):
        for status in self.statuses.keys():
            self.remove(ent, status)
        return True

    #run: iterate status effects and tick down status timers
    def process(self):
        super(Manager_Status, self).run()

        #iterate through only the things that have status effects,
        #   and do those effects
        for status,dic in self.statuses.items():
            for ent, dur in dic.items():
                self._tick(ent, status, dur)
                #tick down the timer by setting duration to current dur - 1
                self._updateTimer(ent, status, dur - 1)


    # private functions #
                
    def _get_default_duration(self, status):
        return STATUSES[status][0]
    def _get_verb1(self, status):
        return STATUSES[status][1]
    def _get_verb2(self, status):
        return STATUSES[status][2]
    def _should_write_message(self, ent):
        # TODO: OR pc has super observation and is in sight...
        return ent==rog.pc() 
    
    #change the timer for a status effect
    def _updateTimer(self, ent, status, dur):
        if dur <= 0:
            self.remove(ent, status)
        else:
            self.statuses[status].update( {ent : dur} )

    def _apply_statMods(self, ent, status):
        #stat mods
            
        if status == SPRINT:
            _id=rog.effect_add( {"msp" : SPRINT_SPEEDMOD} )
            self.statMods[status].update( {ent : _id} )
            
        elif status == HASTE:
            _id=rog.effect_add( {"spd" : HASTE_SPEEDMOD} )
            self.statMods[status].update( {ent : _id} )
            
        elif status == SLOW:
            _id=rog.effect_add( {"spd" : SLOW_SPEEDMOD} )
            self.statMods[status].update( {ent : _id} )
            
        elif status == COUGH:
            _id=rog.effect_add( {
                "atk" : COUGH_ATKMOD,
                "dfn" : COUGH_DFNMOD,
                } )
            self.statMods[status].update( {ent : _id} )
            
        elif status == IRRIT:
            _id=rog.effect_add( {
                "atk" : IRRIT_ATKMOD,
                "range" : IRRIT_RANGEMOD,
                "sight" : IRRIT_SIGHTMOD,
                } )
            self.statMods[status].update( {ent : _id} )
            
        elif status == BLIND:
            _id=rog.effect_add( {"sight" : BLIND_SIGHTMOD} )
            self.statMods[status].update( {ent : _id} )
            
        elif status == DEAF:
            _id=rog.effect_add( {"hearing" : DEAF_HEARINGMOD} )
            self.statMods[status].update( {ent : _id} )
            
        elif status == WET:
            _id=rog.effect_add( {"resfire" : WET_RESFIRE} )
            #"mass" : WET_EXTRAMASS*obj.mass
            self.statMods[status].update( {ent : _id} )
            
##        elif status == TRAUMA:
##            _id=rog.effect_add( {"resfire" : TRAUMA_} )
##            #"mass" : WET_EXTRAMASS*ent.mass
##            self.statMods[status].update( {ent : _id} ) 

    #statuses that cause other statuses when they begin
    def _apply_auxEffects(self, ent, status):
        if status == DRUNK: #getting drunk is the best therapy
            self.remove(ent, TRAUMA)

    #write a message about the status being applied if we should do so
    def _apply_message(self, ent, status):
        if self._should_write_message(ent):
            entn = rog.world().component_for_entity(ent, cmp.Name)
            rog.msg("{t}{n} {v1} {v2}.".format(
                t=entn.title,n=entn.name,
                v1=self._get_verb1(status),
                v2=self._get_verb2(status))
                    )

    #statuses that cause other statuses when elapsed
    def _apply_auxRemoveEffects(self, ent, status):
        if status == SPRINT: #after done sprinting, get tired
            self.add(ent, TIRED) 
        if status == PARAL: #after getting unparalyzed, temporarily slowed down you become
            self.add(ent, SLOW)
##        if status == DRUNK:
##            self.add(obj, HUNGOVER)

    #remove any stat mods for the associated status status on object obj
    def _remove_statMods(self, ent, status):
        if self.statMods[status].get(ent, None):
            rog.effect_remove( self.statMods[status][ent] )
            del self.statMods[status][ent]

    #write a message about the status being removed if we should do so
    def _remove_message(self, ent, status):
        if self._should_write_message(ent):
            entn = rog.world().component_for_entity(ent, cmp.Name)
            rog.msg("{t}{n} is no longer {v2}.".format(
                t=entn.title,n=entn.name,
                v2=self._get_verb2(status))
                    )
            
#do an effect to an object. Only check the objects that need checking
    def _tick(self, ent, status, time):
        world = rog.world()
        
        if status == SICK:
            pass
        
        elif status == SPRINT:
            pass #chance to trip while sprinting
##            if dice.roll(100) < SPRINT_TRIP_CHANCE:
##                rog.knockdown(obj)
        
        elif status == FIRE:
            stats = world.component_for_entity(ent, cmp.BasicStats)
            if stats.temp < FIRE_TEMP: #cooled down too much to keep burning
                self.remove(ent, status)
##                print("removing fire due to low temp for {} at {},{}".format(obj.name,obj.x,obj.y))
                return
            #damage is based on temperature of the object
            dmg = max( 1, int(stats.temp / 100) )
            rog.hurt(ent, dmg)
            #create a fire at the location of burning things
            if world.has_component(ent, cmp.Position):
                pos = world.component_for_entity(ent, cmp.Position)
                rog.set_fire(pos.x,pos.y)
            
        elif status == ACID:
            #damage is based on time remaining, more time = more dmg
            dmg = max( 1, dice.roll(2) - 2 + math.ceil(math.sqrt(time-1)) )
            rog.hurt(obj, dmg)
            
        elif status == IRRIT:
            pass
        
        elif status == PARAL:
            if dice.roll(20) <= PARAL_ROLLSAVE:
                self.remove(obj, status)
                
        elif status == COUGH:
            pass #chance to stop in a coughing fit (waste your turn)
##            if dice.roll(20) <= COUGH_CHANCE:
##                rog.queue_action(obj, action.cough)
        
        elif status == VOMIT:
            pass #chance to stop in a vomiting fit (waste your turn)
##            if dice.roll(20) <= VOMIT_CHANCE:
##                rog.queue_action(obj, action.cough)
        
        elif status == BLIND:
            pass
        
        elif status == DEAF:
            pass
        
