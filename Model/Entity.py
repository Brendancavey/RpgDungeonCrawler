class Entity():
    def __init__(self, name, hp, power):
        self._name = name
        self._hp = hp
        self._power = power
        self._inventory = {}
        self._equips = {"Armor": None, "Weapon": None, "Accessory": None}

    def getName(self):
        return self._name
    def getHp(self):
        return self._hp
    def getPower(self):
        return self.getPower()
    def getEquippedItem(self, item):
        return self._equips[item.getEquipType()]
    def modifyHp(self, value):
        self._hp += value
    def modifyPower(self, value):
        self._power += value
    def setHp(self, value):
        self._hp = value
    def setPower(self, value):
        self._power = value
    def inventoryAdd(self, item):
        if item not in self._inventory:
            self._inventory[item] = 1
        else:
            self._inventory[item] += 1
    def inventoryUse(self, item):
        if item not in self._inventory:
            return
        else:
            self._inventory[item] -= 1
        if self._inventory[item] <= 0:
            self._inventory.remove(item)
    def inventoryEquip(self, item):
        if item not in self._inventory:
            return
        else:
            if self.getEquippedItem(item) != None:
                self.inventoryAdd(self.equips[item.getEquipType()]) #remove equipped item and add to inventory
            self._equips[item.getEquipType()] = item
