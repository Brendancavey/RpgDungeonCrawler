from Model.Overworld.Overworld import Overworld
from Model.Overworld.Location import Location
from Controller.GameData import enemy_locations, treasure_locations, npc_locations, player
from Controller.Setting import screen_height, screen_width
import pygame

class Game():
    font = pygame.font.Font(None, 35)
    def __init__(self, screen):
        self.player = player
        self.screen = screen

        #overworld data
        self.available_locations = [-1, 0, 1, 2]
        self.start_location = 0
        self.visited_locations = []
        self.enemies = pygame.sprite.Group()
        self.enemy_locations = enemy_locations
        self.treasure_locations = treasure_locations
        self.npc_locations = npc_locations

        #player hud
        self.hud_surface = pygame.Surface((screen_width, 50))
        self.hud_surface.fill('darkslategrey')

        #background
        self.background = pygame.image.load('../View/Graphics/dungeon.png').convert_alpha()

        #create overworld
        self.overworld = Overworld(self.start_location, self.available_locations, self.screen, self.createLocation, self.enemies,
                                   self.enemy_locations, self.visited_locations, self.treasure_locations, self.npc_locations)
        self.screen_status = 'overworld'

    def displayBackground(self):
        self.screen.blit(self.background, (0, 0))
    def displayHud(self):
        self.hud_text_playerHp = self.font.render("HP: " + str(player.getHp()) + "/" + str(player.getMaxHp()), False,
                                                  'white')
        self.hud_text_playerPwr = self.font.render("Attack: " + str(player.getPower()), False, "white")
        self.screen.blit(self.hud_surface, (0, 0))
        self.screen.blit(self.hud_text_playerHp, (925, 15))
        self.screen.blit(self.hud_text_playerPwr, (1100, 15))

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
        self.displayBackground()
        self.displayHud()
        self.overworld.timer()
        self.background.blit(self.overworld.ui_inventory_title_surface, (940, 145))
        self.background.blit(self.overworld.ui_inventory_title_text, (940, 145))
        self.overworld.ui_inventory.draw(self.background)
        self.overworld.ui_equipment.draw(self.background)
        self.overworld.ui_items.draw(self.background)
        self.overworld.ui_weapons.draw(self.background)
        self.overworld.interactWithInventory()
        if self.screen_status == 'overworld':
            self.overworld.run()
        else:
            self.location.run()