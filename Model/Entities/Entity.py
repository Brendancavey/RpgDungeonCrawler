import Model.Inventory.Item
from Model.Inventory.Inventory import Inventory
from Model.Inventory.Equipment import Equipment
from Model.BattleSystem.Ability.Ability import Ability
from Model.BattleSystem.Debuff.DebuffList import debuff_list


class Entity():
    def __init__(self, name, hp, power):
        #attributes
        self._name = name
        self._maxHp = hp
        self._hp = hp
        self._power = power
        #inventory
        self._inventory = Inventory()
        self._equips = Equipment()
        #debuffs
        self.status = set()
        self.dot_damage = []
        self.weaken_attackPwr = []
        self.take_more_damage = []
        #abilities
        self.all_abilities = []
        self.ability_loadout = []
        self.ability = None #ability used in Battle System
        self.max_ap = 2
        #passives
        self.passive_buffs = []


    def addDebuff(self, debuff):
        self.status.add(debuff)
    def resetDebuffs(self):
        self.status = set()
        self.dot_damage = []
        self.weaken_attackPwr = []
        self.take_more_damage = []
    def addAbility(self, ability):
        self.ability_loadout.append(ability)
    def removeAbility(self, ability):
        self.ability_loadout.remove(ability)
    def learnAbility(self, ability):
        if ability not in self.all_abilities:
            self.all_abilities.append(ability)
    def unlearnAbility(self, ability):
        if ability in self.all_abilities:
            self.all_abilities.remove(ability)
    def getName(self):
        return self._name
    def getHp(self):
        return int(self._hp)
    def getMaxHp(self):
        return int(self._maxHp)
    def getPower(self):
        return self._power
    def getAbilities(self):
        return self.ability_loadout
    def getGoldValue(self):
        return self._inventory.getGoldValue()
    def getInventory(self):
        return self._inventory.getInventory()
    def getItems(self):
        return self._inventory.getItems()
    def getEquippedItems(self):
        return self._equips.getEquipedItems()
    def modifyHp(self, value):
        self._hp += value
        if self._hp > self._maxHp:
            self.setHp(self._maxHp)
    def modifyMaxHp(self, newMaxHp):
        self._maxHp = newMaxHp
    def modifyPower(self, value):
        self._power += value
    def modifyGold(self, value):
        self._inventory.modifyGold(value)
    def setHp(self, value):
        self._hp = value
    def setPower(self, value):
        self._power = value
    def setGold(self, value):
        self._inventory.setGold(value)
    def interact(self, interactable, display_surface = None):
        if isinstance(interactable, Model.Inventory.Item.Item):
            self.itemObtain(interactable)
            print("received " + str(interactable))
            print(self.getInventory())
        elif isinstance(interactable, int):
            self.modifyGold(interactable)
            print("received " + str(interactable) + " gold!")
        elif isinstance(interactable, Model.Entities.NPC.NPC):
            interactable.chat(display_surface)
    def itemObtain(self, item):
        self._inventory.inventoryAdd(item)
    def itemUse(self, item):
        self.modifyHp(self._inventory.inventoryUse(item))
    def itemRemove(self, item):
        self._inventory.inventoryRemove(item)
    def equip(self, item):
        if self._inventory.itemInInventory(item):
            if not self._equips.equipSlotIsEmpty(item):
                self.unequip(item)
            self._inventory.inventoryRemove(item)  # Use item from inventory to reflect removal from inventory
            self._equips.equip(item) #asking equipment to equip item
            self.modifyPower(item.getPowerMod())
            print("equipping " + str(item))
            if item.passive:
                self.passive_buffs.append(item.passive)
            if item.ap_mod:
                self.max_ap += item.ap_mod

        else:
            print("Item not in inventory. Unable to equip " + item)
    def unequip(self, item):
        removed_item = self._equips.equipRemove(item)
        self._inventory.inventoryAdd(removed_item) #add item back into inventory
        self.modifyPower(-removed_item.getPowerMod())  # modifying power to reflect removed item
        if removed_item.passive:
            self.passive_buffs.remove(removed_item.passive)
        if removed_item.ap_mod:
            self.max_ap -= removed_item.ap_mod
    def takeDamage(self, value):
        self.modifyHp(-value)
    def attack(self, entity, ability, damage):
        if self.getHp() > 0:
            print(self.getName() + " uses " + str(ability) + " on " + entity.getName())
            entity.takeDamage(damage)
            if entity.isAlive():
                print(entity.getName() + " has " + str(entity.getHp()) + " HP left.")
            else:
                entity._checkForDeath()

    def isWeakAgainst(self, element):
        return False #testing
    def guard(self, entity, damage):
        print(self.getName() + " defends")
    def isAlive(self):
        return self.getHp() > 0
    def isFullHp(self):
        return self._hp == self._maxHp
    def _checkForDeath(self):
        if self.getHp() <= 0:
            self.setHp(0)
            print(self.getName() + " health has been reduced to 0.")
            print(self.getName() + " has been defeated.")
            return



