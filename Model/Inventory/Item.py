import itertools
import Model.Inventory.ItemTypes as i_type
import Model.Inventory.InventoryMap as inv_map
class Item():
    _id_iter = itertools.count()

    def __init__(self, name, item_types_key, price, special = None, passive = None, ap_mod = None,):
        self._name = name
        self._type = i_type._item_types_map[item_types_key]
        self._price = price
        self._id = next(self._id_iter)
        self.special_message = special
        self.passive = passive
        self.ap_mod = ap_mod

    def __repr__(self):
        return self._name
    def getName(self):
        return self._name
    def getItemType(self):
        return self._type
    def getId(self):
        return self._id
    def getPrice(self):
        return self._price
    def getPriceDescription(self):
        description = "value: " + str(self.getPrice()) + inv_map._inventory_map[inv_map._gold][0]
        return description
    def getDescription(self):
        description = ""
        if self.ap_mod:
            description += " |AP: + " + str(self.ap_mod)
        if self.special_message:
            description += "| " + self.special_message
        return description
