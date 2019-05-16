
        
    @property
    def hp(self) -> int:
        return max(0, self._hp)
    @hp.setter
    def hp(self, val: int) -> int:
        self._hp = val
    @property
    def mp(self) -> int:
        return max(0, self._mp)
    @mp.setter
    def mp(self, val: int) -> int:
        self._mp = val
    @property
    def hpmax(self) -> int:
        return max(0, self._hpmax)
    @hpmax.setter
    def hpmax(self, val: int) -> int:
        self._hpmax = val
    @property
    def mpmax(self) -> int:
        return max(0, self._mpmax)
    @mpmax.setter
    def mpmax(self, val: int) -> int:
        self._mpmax = val
        
    @property
    def resFire(self) -> int:
        return max(0, self._resFire)
    @resFire.setter
    def resFire(self, val: int) -> int:
        self._resFire = val
    @property
    def resBio(self) -> int:
        return max(0, self._resBio)
    @resBio.setter
    def resBio(self, val: int) -> int:
        self._resBio = val
    @property
    def resElec(self) -> int:
        return max(0, self._resElec)
    @resElec.setter
    def resElec(self, val: int) -> int:
        self._resElec = val
    @property
    def resPhys(self) -> int:
        return max(0, self._resPhys)
    @resPhys.setter
    def resPhys(self, val: int) -> int:
        self._resPhys = val
        
    @property
    def temp(self) -> int:
        return max(0, self._temp)
    @temp.setter
    def temp(self, val: int) -> int:
        self._temp = val
    @property
    def sick(self) -> int:
        return max(0, self._sick)
    @sick.setter
    def sick(self, val: int) -> int:
        self._sick = val
    @property
    def expo(self) -> int:
        return max(0, self._expo)
    @expo.setter
    def expo(self, val: int) -> int:
        self._expo = val
    @property
    def rads(self) -> int:
        return max(0, self._rads)
    @rads.setter
    def rads(self, val: int) -> int:
        self._rads = val
