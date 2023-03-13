from Model.BattleSystem.BattleSystem import BattleSystem
from Model.Entities.Enemy.Enemy import Enemy
from Model.Entities.Player import Player
from Controller.Setting import screen_width, screen_height
from Model.Entities.Enemy.EnemyList import enemy_list

player = Player("Player", 100, 10)
enemy = enemy_list[0]
enemy1 = enemy_list[1]
enemy2 = enemy_list[2]
enemy3 = enemy_list[3]
enemy4 = enemy_list[3]

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

location_0 = {'node_pos' : (110,400), 'content' : None, 'unlock' : [0, 1, 2]}
location_1 = {'node_pos' : (110,200), 'content' : battle1, 'unlock' : [0, 1, 3]}
location_2 = {'node_pos' : (300,400), 'content' : None, 'unlock' : [0, 2, 3, 4]}
location_3 = {'node_pos' : (300,200), 'content' : None, 'unlock' : [1, 2, 3]}
location_4 = {'node_pos' : (490,400), 'content' : battle2, 'unlock' : [2, 4, 5, 6]}
location_5 = {'node_pos' : (490,200), 'content' : None, 'unlock' : [4, 5]}
location_6 = {'node_pos' : (680,400), 'content' : battle4, 'unlock' : [4, 6]}

locations = {
    0 : location_0,
    1: location_1,
    2: location_2,
    3: location_3,
    4: location_4,
    5: location_5,
    6: location_6
}

#enemy locations
enemy_locations = [1, 4]

