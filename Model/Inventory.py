class Inventory():

    _inventory_map = {"Gold" : "Money",
                      "Item": "Supplies",
                      "Weapon": "Weapons",
                      "Armor": "Armor",
                      "Accessory": "Accessories"
                      }

    def __init__(self):
        self._inventory = {self._inventory_map["Gold"]: 0,
                           self._inventory_map["Item"]: {},
                           self._inventory_map["Weapon"]: {},
                           self._inventory_map["Armor"]: {},
                           self._inventory_map["Accessory"]: {}
                           }
    def getInventory(self):
        return self._inventory
    def getGoldValue(self):
        return self._inventory[self._inventory_map["Gold"]]
    def getItems(self):
        return self._inventory[self._inventory_map["Item"]]
    def getWeapons(self):
        return self._inventory[self._inventory_map["Weapon"]]
    def getArmor(self):
        return self._inventory[self._inventory_map["Armor"]]
    def getAccessories(self):
        return self._inventory[self._inventory_map["Accessory"]]
    def getNameGold(self):
        return self._inventory_map["Gold"]
    def getNameItem(self):
        return self._inventory_map["Item"]
    def getNameWeapon(self):
        return self._inventory_map["Weapon"]
    def getNameArmor(self):
        return self._inventory_map["Armor"]
    def getNameAccessory(self):
        return self._inventory_map["Accessory"]

    def modifyGold(self, value):
        self._inventory[self._inventory_map["Gold"]] += value

    def setGold(self, value):
        self._inventory[self._inventory_map["Gold"]] = value

    def inventoryAdd(self, item):
        item_inventory_type = self._inventory_map[item.getItemType()]
        corresponding_inventory = self._inventory[item_inventory_type]
        if item not in corresponding_inventory:
            corresponding_inventory[item] = 1
        else:
            corresponding_inventory[item] += 1
        self._inventory[item_inventory_type] = corresponding_inventory
    def inventoryUse(self, item):
        pass
        #if self.itemInInventory(item):


    def inventoryRemove(self, item):
        item_inventory_type = self._inventory_map[item.getItemType()]
        corresponding_inventory = self._inventory[item_inventory_type]
        if item not in corresponding_inventory:
            return
        else:
            corresponding_inventory[item] -= 1
        if corresponding_inventory[item] <= 0:
            corresponding_inventory.pop(item)
        self._inventory[item_inventory_type] = corresponding_inventory

    def itemInInventory(self, item):
        item_inventory_type = self._inventory_map[item.getItemType()]
        corresponding_inventory = self._inventory[item_inventory_type]
        if item in corresponding_inventory:
            return True
        return False