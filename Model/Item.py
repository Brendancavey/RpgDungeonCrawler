import itertools
class Item():
    _id_iter = itertools.count()

    def __init__(self, name, type, price):
        self._name = name
        self._type = type
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
        price = "value: " + str(self.getPrice()) + "G"
        return price
