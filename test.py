
import esper
import time
import random

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
        return max(0, self._dfn)
    @dfn.setter
    def dfn(self, val: int) -> int:
        self._dfn = val
        
    @property
    def dmg(self) -> int:
        return max(0, self._dmg)
    @dmg.setter
    def dmg(self, val: int) -> int:
        self._dmg = val
        
    @property
    def arm(self) -> int:
        return max(0, self._arm)
    @arm.setter
    def arm(self, val: int) -> int:
        self._arm = val
        
              
class DataCollectorProcessor(esper.Processor):
    def __init__(self):
        super().__init__()

        self.data=[]
        self.g=[]
        for i in range(100):
            self.g.append(i)

    def process(self):
##        for i in range(3):
##            d = self.g[int(random.random()*98)]
        for ent,h in self.world.get_component(set):
            self.data.append((ent, h,))
            print(ent, h)
    
    
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

    pc=world.create_entity(comp.Name("Bob"),comp.Position(5,6),Stats(),set())
    f=world.create_entity(comp.Name("4 of destiny"),comp.Position(5,6))
    foe=world.create_entity(comp.Name("zombie"),comp.Position(2,8),Stats())

    b=[]
    for i in range(100):
        b.append((Stats(),comp.Health(),comp.Resistances(),comp.Name("b"),
                  comp.CanEquipBody(),comp.CanEquipAmmo(),comp.CanEquipBack(),
                comp.CanEquipMainhand(),comp.CanEquipOffhand(),comp.CanEquipHead()
                  ))
        a=world.create_entity(comp.Name("a"),Stats(),comp.Health(1,1),comp.Resistances(),
                              comp.CanEquipBody(),comp.CanEquipAmmo(),comp.CanEquipBack(),
                              comp.CanEquipMainhand(),comp.CanEquipOffhand(),comp.CanEquipHead())

    d=[]
    print("Starting...")
    tt=time.time()
    for ll in b:
        for i in ll:
            if isinstance(i, Stats):
                d.append(i)
    tr=time.time() - tt
    print("done. t = ",tr)

    print("Starting...")
    tt=time.time()
    world.process()
    tr=time.time() - tt
    print("done. t = ",tr)



if __name__ == "__main__":
    main()



