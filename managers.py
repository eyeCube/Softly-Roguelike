'''
    managers.py

'''

'''
#
# abstract Manager class
#
# 
# A manager is an object that has functions for handling a complex task,
# which is carried out using its 'run()' function.
# give it some starting data, then call 'run()' inside a while loop.
# check the output of the manager with the property 'result'.
# finish the execution by calling 'close()'.
#
#     * Only the 'run', 'close', and 'result' functions should be called
    outside of the manager.
      * The manager only accesses its own functions through its 'run' method.
      * You can intercept the 'run' function at the end of each iteration
    in your while loop, simply by writing code following the 'run()' call.
    This is one of the useful things about managers.
#
'''
class Manager(object):
    
    def __init__(self):
        self._result=None
    def set_result(self,new):       self._result=new
    @property
    def result(self):           return self._result
    def run(self, *args,**kwargs):
        self.set_result(None)
    def close(self):
        pass
#

class GameStateManager(Manager):
    
    def __init__(self):
        super(GameStateManager,self).__init__()
        self._resume_game_state="normal"
    def close(self):
        super(GameStateManager,self).close()
        self.resume_game_state()
    def set_resume_state(self,new): self._resume_game_state=new
    def resume_game_state(self): rog.game_set_state(self._resume_game_state)
#






