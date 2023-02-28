from Model.Inventory.Inventory import Inventory
from Model.Inventory.Equipment import Equipment
from Model.BattleSystem.Ability import Ability
import Model.BattleSystem.EffectTypes as e
class Entity():
    def __init__(self, name, hp, power):
        #attributes
        self._name = name
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
        self.attk = Ability("Attack", "Normal", 1)
        self.abilities = []
        self.addAbility(self.attk)

    def addDebuff(self, debuff):
        self.status.add(debuff)
    def addAbility(self, ability):
        self.abilities.append(ability)
    def getName(self):
        return self._name
    def getHp(self):
        return int(self._hp)
    def getPower(self):
        return self._power
    def getAbilities(self):
        return self.abilities
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
        else:
            print("Item not in inventory. Unable to equip " + item)
    def unequip(self, item):
        removed_item = self._equips.equipRemove(item)
        self._inventory.inventoryAdd(removed_item) #add item back into inventory
        self.modifyPower(-removed_item.getPowerMod())  # modifying power to reflect removed item
    def takeDamage(self, value):
        self.modifyHp(-value)
    def attack(self, entity, damage):
        if self.getHp() > 0:
            print(self.getName() + " attacks " + entity.getName())
            entity.takeDamage(damage)
            if entity.isAlive():
                print(entity.getName() + " has " + str(entity.getHp()) + " HP left.")
            else:
                entity._checkForDeath()
    def guard(self, entity, damage):
        print(self.getName() + " defends")
    def isAlive(self):
        return self.getHp() > 0
    def _checkForDeath(self):
        if self.getHp() <= 0:
            self.setHp(0)
            print(self.getName() + " health has been reduced to 0.")
            print(self.getName() + " has been defeated.")
            return



