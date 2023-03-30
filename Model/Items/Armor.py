from Model.Inventory.Item import Item

class Armor(Item):
    def __init__(self, name, item_type_idx, price, power_mod, special=None, passive=None):
        super().__init__(name, item_type_idx, price, special, passive)
        self._power_mod = power_mod

    def getPowerMod(self):
        return self._power_mod

    def getDescription(self):
        description = "Atk: +" + str(self._power_mod)
        description += super().getDescription()
        return description