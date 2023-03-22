from Controller.GameData import locations, player
from Controller.Setting import screen_width, screen_height
from Model.BattleSystem.BattleSystem import BattleSystem
import Model.Entities.Enemy.Enemy
import Model.Inventory.Item
class Location:
    def __init__(self, current_location, surface, create_overworld, remaining_enemies, enemy_locations, visited_locations,
                 treasure_locations, npc_locations):
        #location setup
        self.display_surface = surface
        self.current_location = current_location
        location_data = locations[current_location]
        self.location_content = location_data['content']
        self.new_available_locations = location_data['unlock']

        #methods from Game.py
        self.create_overworld = create_overworld

        #enemy overworld data
        self.remaining_enemies = remaining_enemies
        self.enemy_locations = enemy_locations

        #player overworld data
        self.visited_locations = visited_locations

        #treasure overworld data
        self.treasure_locations = treasure_locations

        #npc overworld data
        self.npc_locations = npc_locations

        #battle data
        if isinstance(self.location_content, Model.Entities.Enemy.Enemy.Enemy):
            self.battle = BattleSystem(player, self.location_content, screen_width, screen_height)

    def run(self):
        if not self.location_content:
            self.create_overworld(self.current_location, self.new_available_locations, self.remaining_enemies,
                                  self.enemy_locations,
                                  self.visited_locations, self.treasure_locations, self.npc_locations)
        if isinstance(self.location_content, Model.Entities.Enemy.Enemy.Enemy):
            self.battle.start()
            if not self.location_content.isAlive():
                print("you win!")
                self.create_overworld(self.current_location, self.new_available_locations, self.remaining_enemies,
                                      self.enemy_locations,
                                      self.visited_locations, self.treasure_locations, self.npc_locations)
            if not player.isAlive():
                print("you lose!")
                self.create_overworld(self.current_location, self.new_available_locations, self.remaining_enemies,
                                      self.enemy_locations,
                                      self.visited_locations, self.treasure_locations, self.npc_locations)