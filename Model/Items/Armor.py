from Model.Inventory.Item import Item

class Armor(Item):
    def __init__(self, name, item_type_idx, price, power_mod):
        super().__init__(name, item_type_idx, price)
        self._power_mod = power_mod

    def getPowerMod(self):
        return self._power_mod

    def getDescription(self):
        description = self._name + ": Attack: +" + str(self._power_mod)
        return description