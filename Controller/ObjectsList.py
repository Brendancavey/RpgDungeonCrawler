from Model.Items.Potion import Potion
from Model.Items.Weapon import Weapon
from Model.Items.Armor import Armor
from Model.Items.Accessory import Accessory

#potions
potion0 = Potion("Small Potion", 1, 5, 5)
potion1 = Potion("Potion", 1, 10, 10)
potion2 = Potion("Large Potion", 1, 20, 20)
potion_list = [potion0, potion1, potion2]

#weapons
sword0 = Weapon("Dull Sword", 2, 10, 1)
sword1 = Weapon("Pointy Sword", 2, 15, 2)
sword2 = Weapon("Sharp Sword", 2, 20, 3)
weapons_list = [sword0, sword1, sword2]

#armor
armor0 = Armor("Basic Armor", 3, 10, 1)
armor1 = Armor("Hardened Armor", 3, 15, 2)
armor2 = Armor("Strong Armor", 3, 20, 3)
armor_list = [armor0, armor1, armor2]

#accessories
scroll0 = Accessory("Sharp Paper", 4, 10, 1)
scroll1 = Accessory("Scroll of Tiny Power ", 4, 15, 2)
scroll2 = Accessory("Scroll of Strength", 4, 20, 3)
accessories_list = [scroll0, scroll1, scroll2]