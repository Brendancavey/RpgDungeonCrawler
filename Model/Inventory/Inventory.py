import Model.Inventory.InventoryMap as inv_map
class Inventory():
    def __init__(self):
        self._inventory = {inv_map._inventory_map[inv_map._gold]: 0,
                           inv_map._inventory_map[inv_map._item]: {},
                           inv_map._inventory_map[inv_map._weapon]: {},
                           inv_map._inventory_map[inv_map._armor]: {},
                           inv_map._inventory_map[inv_map._accessory]: {}
                           }
    def getInventory(self):
        return self._inventory
    def getGoldValue(self):
        return self._inventory[inv_map._inventory_map[inv_map._gold]]
    def getItems(self):
        return self._inventory[inv_map._inventory_map[inv_map._item]]
    def getWeapons(self):
        return self._inventory[inv_map._inventory_map[inv_map._weapon]]
    def getArmor(self):
        return self._inventory[inv_map._inventory_map[inv_map._armor]]
    def getAccessories(self):
        return self._inventory[inv_map._inventory_map[inv_map._accessory]]
    def getNameGold(self):
        return inv_map._inventory_map[inv_map._gold]
    def getNameItem(self):
        return inv_map._inventory_map[inv_map._item]
    def getNameWeapon(self):
        return inv_map._inventory_map[inv_map._weapon]
    def getNameArmor(self):
        return inv_map._inventory_map[inv_map._armor]
    def getNameAccessory(self):
        return inv_map._inventory_map[inv_map._accessory]

    def modifyGold(self, value):
        self._inventory[inv_map._inventory_map[inv_map._gold]] += value

    def setGold(self, value):
        self._inventory[inv_map._inventory_map[inv_map._gold]] = value

    def inventoryAdd(self, item):
        item_inventory_type = inv_map._inventory_map[item.getItemType()]
        corresponding_inventory = self._inventory[item_inventory_type]
        if item not in corresponding_inventory:
            corresponding_inventory[item] = 1
        else:
            corresponding_inventory[item] += 1
        self._inventory[item_inventory_type] = corresponding_inventory
    def inventoryUse(self, item):
        if self.itemInInventory(item):
            self.inventoryRemove(item)
            return item.getRecoveryAmt()
        return 0
        #if self.itemInInventory(item):


    def inventoryRemove(self, item):
        item_inventory_type = inv_map._inventory_map[item.getItemType()]
        corresponding_inventory = self._inventory[item_inventory_type]
        if item not in corresponding_inventory:
            return
        else:
            corresponding_inventory[item] -= 1
        if corresponding_inventory[item] <= 0:
            corresponding_inventory.pop(item)
        self._inventory[item_inventory_type] = corresponding_inventory

    def itemInInventory(self, item):
        item_inventory_type = inv_map._inventory_map[item.getItemType()]
        corresponding_inventory = self._inventory[item_inventory_type]
        if item in corresponding_inventory:
            return True
        return False