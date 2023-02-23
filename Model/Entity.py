class Entity():
    inventory_map = {"Item" : "Items", "Weapon" : "Weapons", "Accessory" : "Accessories" , "Armor" : "Armor"}
    def __init__(self, name, hp, power):
        self._name = name
        self._hp = hp
        self._power = power
        self._inventory = {"Gold": 0, "Items": {}, "Weapons": {}, "Armor": {}, "Accessories": {}}
        self._equips = {"Armor": None, "Weapon": None, "Accessory": None}

    def getName(self):
        return self._name
    def getHp(self):
        return self._hp
    def getPower(self):
        return self._power
    def getGoldValue(self):
        return self._inventory["Gold"]
    def modifyGold(self, value):
        self._inventory["Gold"] += value
    def modifyHp(self, value):
        self._hp += value
    def modifyPower(self, value):
        self._power += value
    def setHp(self, value):
        self._hp = value
    def setPower(self, value):
        self._power = value
    def isAlive(self):
        return self.getHp() > 0
    def inventoryAdd(self, item):
        item_inventory_type = self.inventory_map[item.getItemType()]
        corresponding_inventory = self._inventory[item_inventory_type]
        if item not in corresponding_inventory:
            corresponding_inventory[item] = 1
        else:
            corresponding_inventory[item] += 1
        self._inventory[item_inventory_type] = corresponding_inventory
    def inventoryUse(self, item):
        item_inventory_type = self.inventory_map[item.getItemType()]
        corresponding_inventory = self._inventory[item_inventory_type]
        if item not in corresponding_inventory:
            return
        else:
            corresponding_inventory[item] -= 1
        if corresponding_inventory[item] <= 0:
            corresponding_inventory.pop(item)
        self._inventory[item_inventory_type] = corresponding_inventory
    def inventoryEquip(self, item):
        if not self._itemInInventory(item):
            return
        else:
            if self._equips[item.getItemType()] != None: #check for equipped item
                self.equipRemove(item.getItemType())
            self.inventoryUse(item) #Use item from inventory to reflect removal from inventory
            self._equips[item.getItemType()] = item #equip new item
            self.modifyPower(item.getPowerMod()) #modifying power to reflect equiped item
    def equipRemove(self, equipType):
        if self._equips[equipType] == None:
            return
        self.modifyPower(-self._equips[equipType].getPowerMod()) #modifying power to reflect removed item
        self.inventoryAdd(self._equips[equipType]) #remove equipped item and add to inventory
        self._equips[equipType] = None#setting equipped item to None

    def showInventory(self):
        return self._inventory
    def showEquipedItems(self):
        return self._equips
    def attack(self, entity):
        if self.getHp() > 0:
            print(self.getName() + " attacks " + entity.getName())
            entity.modifyHp(-self.getPower())
            print(entity.getName() + " has " + str(entity.getHp()) + " HP left.")
            entity._checkForDeath()
    def guard(self, entity):
        print(self.getName() + " defends")
    def _itemInInventory(self, item):
        item_inventory_type = self.inventory_map[item.getItemType()]
        corresponding_inventory = self._inventory[item_inventory_type]
        if item in corresponding_inventory:
            return True
        return False
    def _checkForDeath(self):
        if self.getHp() <= 0:
            self.setHp(0)
            print(self.getName() + " has been defeated.")
            return



