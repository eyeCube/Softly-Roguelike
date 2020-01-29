'''
    observer.py
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

    TODO: implement this into new ECS system, but how...?
'''


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
        rog.update_game()
        rog.update_hud()
    




