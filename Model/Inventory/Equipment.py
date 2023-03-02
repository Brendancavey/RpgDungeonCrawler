import Model.Inventory.ItemTypes as i_type
class Equipment():
    _armor = i_type._item_types_map[3]
    _weapon = i_type._item_types_map[2]
    _accessory = i_type._item_types_map[4]

    _equip_map = {_armor : "Armor",
                  _weapon : "Weapon",
                  _accessory : "Accessory"
                  }

    def __init__(self):
        self._equips = {self._equip_map[self._armor]: None,
                        self._equip_map[self._weapon]: None,
                        self._equip_map[self._accessory]: None}

    def getEquipedItems(self):
        return self._equips

    def getArmor(self):
        return self.equip[self._equip_map[self._armor]]

    def getWeapon(self):
        return self.equip[self._equip_map[self._weapon]]

    def getAccessory(self):
        return self.equip[self._equip_map[self._accessory]]

    def getNameArmor(self):
        return self._equip_map[self._armor]

    def getNameWeapon(self):
        return self._equip_map[self._weapon]

    def getNameAccessory(self):
        return self._equip_map[self._accessory]

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