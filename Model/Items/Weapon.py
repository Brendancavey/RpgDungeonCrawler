from Model.Item import Item

class Weapon(Item):
    def __init__(self, name, type, price, power_mod):
        super().__init__(name, type, price)
        self._power_mod = power_mod

    def getPowerMod(self):
        return self._power_mod
    def getDescription(self):
        description = "Power: +" + str(self._power_mod)
        return super().getDescription() + "\n" + description