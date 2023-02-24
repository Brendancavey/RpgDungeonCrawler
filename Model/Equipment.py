class Equipment():
    _equip_map = {"Armor" : "Armor",
                  "Weapon" : "Weapon",
                  "Accessory" : "Accessory"
                  }
    def __init__(self):
        self._equips = {self._equip_map["Armor"]: None,
                        self._equip_map["Weapon"]: None,
                        self._equip_map["Accessory"]: None}

    def getEquipedItems(self):
        return self._equips

    def getArmor(self):
        return self._equips[self._equip_map["Armor"]]

    def getWeapon(self):
        return self._equips[self._equip_map["Weapon"]]

    def getAccessory(self):
        return self._equips[self._equip_map["Accessory"]]

    def getNameArmor(self):
        return self._equip_map["Armor"]

    def getNameWeapon(self):
        return self._equip_map["Weapon"]

    def getNameAccessory(self):
        return self._equip_map["Accessory"]

    def equip(self, item):
        self._equips[item.getItemType()] = item

    def equipRemove(self, item):
        if self.equipSlotIsEmpty(item):
            return
        equip_type = item.getItemType()
        item_to_add_back_into_inventory = self._equips[equip_type]
        self._equips[equip_type] = None  # setting equipped item to None
        return item_to_add_back_into_inventory

    def equipSlotIsEmpty(self, item):
        return self._equips[item.getItemType()] == None