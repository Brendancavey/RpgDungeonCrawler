import itertools
import Model.ItemTypes as i_type
import Model.InventoryMap as inv_map
class Item():
    _id_iter = itertools.count()

    def __init__(self, name, item_types_key, price):
        self._name = name
        self._type = i_type._item_types_map[item_types_key]
        self._price = price
        self._id = next(self._id_iter)
    def __repr__(self):
        return self._name
    def getItemType(self):
        return self._type
    def getId(self):
        return self._id
    def getPrice(self):
        return self._price
    def getDescription(self):
        price = "value: " + str(self.getPrice()) + inv_map._inventory_map[inv_map._gold][0]
        return price
