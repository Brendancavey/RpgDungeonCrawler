from Model.BattleSystem.BattleSystem import BattleSystem
from Model.Entities.Enemy.Enemy import Enemy
from Model.Entities.Player import Player
from Controller.Setting import screen_width, screen_height
from Model.Entities.Enemy.EnemyList import enemy_list
from Model.Items.Potion import Potion
from Model.Entities.NPC import NPC
from Model.Items.Weapon import *

#testing
player = Player("Player", 100, 10)
enemy = enemy_list[0]
enemy1 = enemy_list[1]
enemy2 = enemy_list[2]
enemy3 = enemy_list[3]
enemy4 = enemy_list[3]
potion = Potion("Large Potion", 1,10, 100)
potion2 = Potion("Small Potion", 1,5, 5)
potion3 = Potion("Potion", 1,10, 7)
weapon1 = Weapon("Sharp Sword", 2, 10, 5)
chad = NPC("Chad", 15, 5)
battle1 = BattleSystem(player, enemy, screen_width, screen_height)
battle2 = BattleSystem(player, enemy1, screen_width, screen_height)
battle3 = BattleSystem(player, enemy2, screen_width, screen_height)
battle4 = BattleSystem(player, enemy3, screen_width, screen_height)

#overworld layout
start_width = 110
start_height = 400
cur_width = start_width
cur_height = start_height
gap_width = 190
gap_height = 200

#even locations are on the horizontal plane.
#odd locations are on the vertical plane.
#location content
location_00 = {'node_pos' : (110,400), 'content' : chad, 'unlock' : [-1, 0]}
location_0 = {'node_pos' : (110,250), 'content' : None, 'unlock' : [-1, 0, 1, 2]}
location_1 = {'node_pos' : (110,100), 'content' : battle1, 'unlock' : [0, 1, 3]}
location_2 = {'node_pos' : (300,400), 'content' : potion, 'unlock' : [0, 2, 3, 4]}
location_3 = {'node_pos' : (300,200), 'content' : weapon1, 'unlock' : [1, 2, 3]}
location_4 = {'node_pos' : (490,400), 'content' : battle2, 'unlock' : [2, 4, 5, 6]}
location_5 = {'node_pos' : (490,200), 'content' : potion3, 'unlock' : [4, 5]}
location_6 = {'node_pos' : (680,400), 'content' : battle4, 'unlock' : [4, 6, 7]}
location_7 = {'node_pos' : (680,200), 'content' : None, 'unlock' : [6, 7, 9]}
location_8 = {'node_pos' : (870,400), 'content' : None, 'unlock' : [8, 9, 10]}
location_9 = {'node_pos' : (870,200), 'content' : None, 'unlock' : [7, 8, 9]}
location_10 = {'node_pos' : (1100,400), 'content' : None, 'unlock' : [8, 10]}

locations = {
    -1: location_00,
    0 : location_0,
    1: location_1,
    2: location_2,
    3: location_3,
    4: location_4,
    5: location_5,
    6: location_6,
    7: location_7,
    8: location_8,
    9: location_9,
    10: location_10
}

#locations
enemy_locations = [1, 4, 6]
treasure_locations = [2, 3, 5]
npc_locations = [-1]

#inventory grid
slot_0 = {'slot_pos' : (1075,220), 'content' : None}
slot_1 = {'slot_pos' : (1150,220), 'content' : None}
slot_2 = {'slot_pos' : (1225,220), 'content' : None}
slot_3 = {'slot_pos' : (1075,320), 'content' : None}

inventory_slots = {
    0: slot_0,
    1: slot_1,
    2: slot_2,
    3: slot_3
}



