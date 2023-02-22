import itertools
class Item():
    _id_iter = itertools.count()

    def __init__(self, name, type):
        self._name = name
        self._type = type
        self._id = next(self._id_iter)
    def __repr__(self):
        return self._name
    def getItemType(self):
        return self._type
    def getId(self):
        return self._id
