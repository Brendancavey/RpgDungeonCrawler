from Model.Entities.Player import Player
from Model.Entities.Enemy.EnemyList import enemy_list
from Controller.ObjectsList import potion_list, weapons_list, armor_list, accessories_list
from Model.Entities.NPC import NPC
import Model.Entities.Enemy.Enemy
import Model.Inventory.Item
import Model.Entities.NPC


#testing
player = Player("Player", 100, 10)
chad = NPC("Stranger", 15, 5)

#overworld layout
start_width = 110
start_height = 400
cur_width = start_width
cur_height = start_height
gap_width = 190
gap_height = 200
level = 0

#even locations are on the horizontal plane.
#odd locations are on the vertical plane.
#level0
#location content
def determineLevel():
    if level == 0:
        location_00 = {'node_pos' : (110,400), 'content' : chad, 'unlock' : [-1, 0]}
        location_0 = {'node_pos' : (110,250), 'content' : None, 'unlock' : [-1, 0, 2]}
        location_1 = {'node_pos' : (110,100), 'content' : weapons_list[0], 'unlock' : [0, 1, 3]}
        location_2 = {'node_pos' : (300,400), 'content' : None, 'unlock' : [0, 2, 3, 4]}
        location_3 = {'node_pos' : (300,200), 'content' : enemy_list[0], 'unlock' : [1, 2, 3]}
        location_4 = {'node_pos' : (490,400), 'content' : enemy_list[0], 'unlock' : [2, 4, 5, 6]}
        location_5 = {'node_pos' : (490,200), 'content' : accessories_list[0], 'unlock' : [4, 5]}
        location_6 = {'node_pos' : (640,400), 'content' : enemy_list[1], 'unlock' : [4, 6, 7]}
        location_7 = {'node_pos' : (640,200), 'content' : potion_list[0], 'unlock' : [6, 7, 9]}
        location_8 = {'node_pos' : (820,600), 'content' : weapons_list[1], 'unlock' : [8, 9, 10]}
        location_9 = {'node_pos' : (820,200), 'content' : None, 'unlock' : [7, 8, 9]}
        location_10 = {'node_pos' : (1300,600), 'content' : None, 'unlock' : [8, 10]}
    elif level == 1:
        location_00 = {'node_pos': (200, 650), 'content': chad, 'unlock': [-1, 0]}
        location_0 = {'node_pos': (110, 600), 'content': None, 'unlock': [-1, 0, 1, 2]}
        location_1 = {'node_pos': (110, 100), 'content': enemy_list[2], 'unlock': [0, 1, 3]}
        location_2 = {'node_pos': (300, 400), 'content': armor_list[0], 'unlock': [0, 2, 3, 4]}
        location_3 = {'node_pos': (300, 200), 'content': weapons_list[0], 'unlock': [1, 2, 3]}
        location_4 = {'node_pos': (490, 400), 'content': enemy_list[0], 'unlock': [2, 4, 5, 6]}
        location_5 = {'node_pos': (490, 200), 'content': accessories_list[0], 'unlock': [4, 5]}
        location_6 = {'node_pos': (640, 400), 'content': enemy_list[1], 'unlock': [4, 6, 7]}
        location_7 = {'node_pos': (640, 200), 'content': potion_list[0], 'unlock': [6, 7, 9]}
        location_8 = {'node_pos': (820, 600), 'content': weapons_list[1], 'unlock': [8, 9, 10]}
        location_9 = {'node_pos': (820, 200), 'content': None, 'unlock': [7, 8, 9]}
        location_10 = {'node_pos': (1300, 600), 'content': None, 'unlock': [8, 10]}
    return {
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
locations = determineLevel()

def determineEnemyLocations():
    enemy_locations = []
    for location in locations.values():
        if isinstance(location['content'], Model.Entities.Enemy.Enemy.Enemy):
            for l in locations:
                if locations[l] == location:
                    enemy_locations.append(l)
    print(enemy_locations)
    return enemy_locations
def determineTreasureLocations():
    treasure_locations = []
    for location in locations.values():
        if isinstance(location['content'], Model.Inventory.Item.Item):
            for l in locations:
                if locations[l] == location:
                    treasure_locations.append(l)
    print(treasure_locations)
    return treasure_locations
def determineNpcLocations():
    npc_locations = []
    for location in locations.values():
        if isinstance(location['content'], Model.Entities.NPC.NPC):
            for l in locations:
                if locations[l] == location:
                    npc_locations.append(l)
    print(npc_locations)
    return npc_locations

enemy_locations = determineEnemyLocations()
treasure_locations = determineTreasureLocations()
npc_locations = determineNpcLocations()

#inventory grid
slot_0 = {'slot_pos' : (995,220), 'content' : None}
slot_1 = {'slot_pos' : (1070,220), 'content' : None}
slot_2 = {'slot_pos' : (1145,220), 'content' : None}
slot_3 = {'slot_pos' : (1215,220), 'content' : None}
slot_4 = {'slot_pos' : (995,300), 'content' : None}
slot_5 = {'slot_pos' : (1070,300), 'content' : None}
slot_6 = {'slot_pos' : (1145,300), 'content' : None}
slot_7 = {'slot_pos' : (1215,300), 'content' : None}

inventory_slots = {
    0: slot_0,
    1: slot_1,
    2: slot_2,
    3: slot_3,
    4: slot_4,
    5: slot_5,
    6: slot_6,
    7: slot_7
}



