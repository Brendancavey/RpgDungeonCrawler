from Model.Overworld.Overworld import Overworld
from Model.Overworld.Location import Location
from Controller.GameData import enemy_locations
import pygame

class Game():
    def __init__(self, screen):
        self.max_location = 6
        self.screen = screen
        self.enemies = pygame.sprite.Group()
        self.enemy_locations = enemy_locations
        self.overworld = Overworld(0, self.max_location, self.screen, self.createLocation, self.enemies, self.enemy_locations)
        self.screen_status = 'overworld'
        self.enemies = pygame.sprite.Group()
    def createLocation(self, current_location, remaining_enemies, enemy_locations):
        self.enemy_locations = enemy_locations
        self.location = Location(current_location, self.screen, self.createOverworld, remaining_enemies, self.enemy_locations)
        self.screen_status = 'level'

    def createOverworld(self, current_location, new_max_location, remaining_enemies, enemy_locations):
        self.enemy_locations = enemy_locations
        self.enemies = remaining_enemies
        if new_max_location > self.max_location:
            self.max_location = new_max_location
        self.overworld = Overworld(current_location, self.max_location, self.screen, self.createLocation, self.enemies, self.enemy_locations)
        self.screen_status = 'overworld'

    def run(self):
        if self.screen_status == 'overworld':
            self.overworld.run()
        else:
            self.location.run()