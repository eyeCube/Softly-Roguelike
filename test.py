
import esper

import components as comp



class Stats:
    def __init__(self):
        self.atk=0
        self.dfn=0
        self.dmg=0
        self.arm=0
        
    @property
    def atk(self) -> int:
        return max(0, self._atk)
    @atk.setter
    def atk(self, val: int) -> int:
        self._atk = val
        
    @property
    def dfn(self) -> int:
        return self._dfn
    @dfn.setter
    def dfn(self, val: int) -> int:
        self._dfn = val
        
    @property
    def dmg(self) -> int:
        return self._dmg
    @dmg.setter
    def dmg(self, val: int) -> int:
        self._dmg = val
        
    @property
    def arm(self) -> int:
        return self._arm
    @arm.setter
    def arm(self, val: int) -> int:
        self._arm = val
        
              
class DataCollectorProcessor(esper.Processor):
    def __init__(self):
        super().__init__()

        self.data=[]

    def process(self):
        for ent,stats in self.world.get_component(Stats):
            print(ent, stats)
    
    
def statuses_add():
    ent, world.get_components()

def main():
    s=Stats()

    s.atk-=8
    print(s.atk)
    s.atk=8
    print(s.atk)
    s.atk+=2
    print(s.atk)


    '''
    s.base_dfn=5
    s.dfn=3
    print(s.dfn)
    s.dfn+=3
    print(s.dfn)
    print(s.base_dfn)
    '''

    world = esper.World()
    world.add_processor(DataCollectorProcessor())

    pc=world.create_entity(comp.Name("Jake"),comp.Position(5,6),Stats())
    f=world.create_entity(comp.Name("4 of destiny"),comp.Position(5,6))
    foe=world.create_entity(comp.Name("zombie"),comp.Position(2,8),Stats())

    #while True:
    world.process()



if __name__ == "__main__":
    main()



