from Model.Entity import Entity
from Model.Items.Weapon import Weapon
from Model.Items.Potion import Potion

player = Entity("Player", 10, 7)
print("power is: " + str(player.getPower()))
player_sword = Weapon("Sharp Sword", "Weapon", 2)
player_axe = Weapon("Sharp Axe", "Weapon", 3)
print(player_sword.getId())
print(player_axe.getId())
print(player.showEquipedItems())
player.inventoryAdd(player_sword)
print(player.showInventory())
player.inventoryAdd(player_axe)
print(player.showInventory())
player.inventoryEquip(player_sword)
print(player.showInventory())
print(player.showEquipedItems())
print("power is: " + str(player.getPower()))
print(player_sword.getDescription())
player.inventoryEquip(player_axe)
print("power is: " + str(player.getPower()))
print(player.showInventory())
print(player.showEquipedItems())
player_potion = Potion("Small Healing Potion", "Item", 5)
player.inventoryAdd(player_potion)
print(player.showInventory())
print(player_potion.getDescription())