from Model.Entities.Player import Player
from Model.Entities.Enemy import Enemy
from Model.Entities.NPC import NPC
from Model.Items.Weapon import Weapon
from Model.Items.Potion import Potion
from Model.BattleSystem.BattleSystem import BattleSystem

player = Player("Player", 10, 7)
enemy = Enemy("Enemy", 100, 3)

#print(enemy.getHp())
chad = NPC("Chad", 10, 2)
battle1 = BattleSystem(player, enemy)
#battle1.playerAttacks()
#battle1.playerAttacks()
#print(enemy.getHp())
#battle1.commenceBattle()
#battle1.enemyAttacks()

player_sword = Weapon("Sharp Sword", 2, 10, 2)
player_axe = Weapon("Sharp Axe", 2, 12, 3)
print(player_axe.getDescription())
#player.modifyGold(20)
chad.itemObtain(player_sword)
chad.barter()
chad.playerPurchase(player, player_sword)
player.itemObtain(player_sword)
player.itemObtain(player_axe)
print(player.getInventory())
print(player.getEquippedItems())
print(player.getPower())
player.equip(player_sword)
print(player.getPower())
print(player.getInventory())
print(player.getEquippedItems())
player.modifyGold(5)
player.itemRemove(player_axe)
player.unequip(player_sword)
print(player.getEquippedItems())
print(player.getPower())

#player.inventory.inventoryEquip(player_axe)
player_potion = Potion("Small Healing Potion", 1, 5, 5)
player.itemObtain(player_potion)
print(player.getInventory())

