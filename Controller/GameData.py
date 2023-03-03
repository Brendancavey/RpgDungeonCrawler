from Model.BattleSystem.BattleSystem import BattleSystem
from Model.Entities.Enemy.Enemy import Enemy
from Model.Entities.Player import Player
from Controller.Setting import screen_width, screen_height
from Model.Entities.Enemy.EnemyList import enemy_list

player = Player("Player", 100, 10)
enemy = enemy_list[0]
battle1 = BattleSystem(player, enemy, screen_width, screen_height)
location_0 = {'node_pos' : (110, 400), 'content' : battle1, 'unlock' : 1}
location_1 = {'node_pos' : (300, 220), 'content' : 'this is location 1', 'unlock' : 2}
location_2 = {'node_pos' : (480, 610), 'content' : 'this is location 2', 'unlock' : 3}
location_3 = {'node_pos' : (610, 350), 'content' : 'this is location 3', 'unlock' : 4}
location_4 = {'node_pos' : (880, 210), 'content' : 'this is location 4', 'unlock' : 5}
location_5 = {'node_pos' : (1050, 400), 'content' : 'this is location 5', 'unlock' : 5}

locations = {
    0 : location_0,
    1: location_1,
    2: location_2,
    3: location_3,
    4: location_4,
    5: location_5,
}