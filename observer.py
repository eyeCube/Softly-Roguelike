#
# observer
#


import rogue as rog






# generic classes #


class Observer():
    def update(self):
        pass


##class Observable():
##    
##    def __init__(self):
##        super(Observable,self).__init__()
##        
##        self.observers = []
    
def observers_clear(self):      self.observers_delete()
def observers_delete(self):     self.observers = []
    
def observers_notify(self, *args,**kwargs): #update all observers
    for observer in self.observers:
        observer.update(*args,**kwargs)
        
def observer_add(self,obs):
    if obs in self.observers: return False
    self.observers.append(obs)
    return True
def observer_remove(self,obs):
    if obs in self.observers:
        self.observers.remove(obs)
        return True
    return False



# specific observers #


# the code running this needs work. It updates too often, unnecessarily.
class Observer_playerChange(Observer):
    def update(self, *args,**kwargs):
        super(Observer_playerChange, self).update()
        '''if not args: return
        print(args)
        if (args[0] == 'x'
            or args[0] == 'y'
            or args[0] == 'stats.nrg'
        ): '''
        rog.update_game()
        rog.update_hud()
    




