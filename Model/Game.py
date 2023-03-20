from Model.Overworld.Overworld import Overworld
from Model.Overworld.Location import Location
from Controller.GameData import enemy_locations, treasure_locations, npc_locations
import pygame

class Game():
    def __init__(self, screen):
        self.available_locations = [-1, 0, 1, 2]
        self.start_location = 0
        self.visited_locations = []
        self.screen = screen
        self.enemies = pygame.sprite.Group()
        self.enemy_locations = enemy_locations
        self.treasure_locations = treasure_locations
        self.npc_locations = npc_locations
        self.overworld = Overworld(self.start_location, self.available_locations, self.screen, self.createLocation, self.enemies,
                                   self.enemy_locations, self.visited_locations, self.treasure_locations, self.npc_locations)
        self.screen_status = 'overworld'
        self.enemies = pygame.sprite.Group()
    def createLocation(self, current_location, remaining_enemies, enemy_locations, treasure_locations, npc_locations):
        self.enemy_locations = enemy_locations
        self.treasure_locations = treasure_locations
        self.npc_locations = npc_locations
        self.location = Location(current_location, self.screen, self.createOverworld, remaining_enemies, self.enemy_locations,
                                 self.visited_locations, self.treasure_locations, self.npc_locations)
        self.screen_status = 'level'

    def createOverworld(self, current_location, new_available_locations, remaining_enemies, enemy_locations, visited_locations,
                        treasure_locations, npc_locations):
        self.enemy_locations = enemy_locations
        self.enemies = remaining_enemies
        self.visited_locations = visited_locations
        self.treasure_locations = treasure_locations
        self.npc_locations = npc_locations
        #if new_available_locations > self.available_locations:
        #    self.available_locations = new_available_locations
        self.overworld = Overworld(current_location, self.available_locations, self.screen, self.createLocation, self.enemies,
                                   self.enemy_locations, self.visited_locations, self.treasure_locations, self.npc_locations)
        self.screen_status = 'overworld'

    def run(self):
        if self.screen_status == 'overworld':
            self.overworld.run()
        else:
            self.location.run()