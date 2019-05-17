

    def process(self):
        #get data
        removals=[]
        fireHP=[]
        fireTimers=[]
        fireEnts=[]
        for ent, cc in self.world.get_component(cmp.StatusBurning):
            hp = self.world.component_for_entity(ent, cmp.BasicStats).hp
            timer = cc.timer
            fireEnts.append(ent)
            fireHP.append(hp)
            fireTimers.append(timer)
            
        #convert data into numpy arrays
        npFireStats = np.array(fireStats)
        npFireTimers = np.array(fireTimers)
        
        #update data
        np.subtract(npFireHP, 1)
        np.subtract(npFireTimers, 1)
        
        #distribute data
        i=0
        for ent in fireEnts:
            hp = fireHP[i]
            timer = fireTimers[i]
            if hp <= 0:
                rog.kill(ent)
                continue
            if timer <= 0:
                removals.update({ent, cmp.StatusBurning})
                continue
            stats = self.world.component_for_entity(ent, cmp.BasicStats)
            status = self.world.component_for_entity(ent, cmp.StatusBurning)
            stats.hp = hp
            status.timer = timer
            i+=1

        #remove expired status effects
        for ent, component in removals:
            self.status_remove(ent, component)
