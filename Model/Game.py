from Controller import GameData
from Model.Overworld.Overworld import Overworld
from Model.Overworld.Location import Location
from Model.InventoryUI import InventoryUI
from Controller.GameData import enemy_locations, treasure_locations, npc_locations, player, locations
from Controller.Setting import screen_height, screen_width
from pygame import mixer
import pygame
class Game():
    font = pygame.font.Font(None, 35)
    def __init__(self, screen):
        self.player = player
        self.screen = screen
        mixer.Channel(0).play(mixer.Sound('../Controller/Sounds/TheLoomingBattle.OGG'))
        #mixer.Channel(0).play(-1)
        mixer.Channel(1).play(mixer.Sound('../Controller/Sounds/Ambience_Cave_00.wav'))
        #mixer.Channel(1).play(-1)
        #mixer.music.load('../Controller/Sounds/TheLoomingBattle.OGG')
        #mixer.music.play(-1)
        #mixer.music.set_volume(0.80)
        #mixer.music.load('../Controller/Sounds/Ambience_Cave_00.wav')
        #mixer.music.play(-1)

        #overworld data
        self.available_locations = [-1, 0, 1, 2]
        self.start_location = -1
        self.visited_locations = []
        self.enemies = pygame.sprite.Group()
        self.enemy_locations = enemy_locations
        self.treasure_locations = treasure_locations
        self.npc_locations = npc_locations

        #player hud
        self.hud_surface = pygame.Surface((screen_width, 50))
        self.hud_surface.fill('darkslategrey')
        self.ui_inventory = InventoryUI(self.screen)

        #background
        self.background = pygame.image.load('../View/Graphics/dungeon.png').convert_alpha()

        #create overworld
        self.overworld = Overworld(self.start_location, self.available_locations, self.screen, self.background, self.createLocation, self.enemies,
                                   self.enemy_locations, self.visited_locations, self.treasure_locations, self.npc_locations, self.ui_inventory)
        self.screen_status = 'overworld'

    def displayBackground(self):
        self.screen.blit(self.background, (0, 0))

    def displayHud(self):
        self.hud_text_playerHp = self.font.render("HP: " + str(player.getHp()) + "/" + str(player.getMaxHp()), False,
                                                  'white')
        self.hud_text_playerPwr = self.font.render("Attack: " + str(player.getPower()), False, "white")
        self.hud_text_level = self.font.render("Stage: " + str(GameData.level), False, 'white')
        self.screen.blit(self.hud_surface, (0, 0))
        self.screen.blit(self.hud_text_level, (50, 15))
        self.screen.blit(self.hud_text_playerHp, (925, 15))
        self.screen.blit(self.hud_text_playerPwr, (1100, 15))

    def displayInventory(self):
        self.ui_inventory.timer()
        self.background.blit(self.ui_inventory.title_surface, (940, 145))
        self.background.blit(self.ui_inventory.title_text, (940, 145))
        self.ui_inventory.graphic_inventory.draw(self.background)
        self.ui_inventory.graphic_equipment.draw(self.background)
        self.ui_inventory.items.draw(self.background)
        self.ui_inventory.weapons.draw(self.background)
        self.ui_inventory.armor.draw(self.background)
        self.ui_inventory.accessories.draw(self.background)
        self.ui_inventory.inv_quantity.draw(self.background)
        self.ui_inventory.run()
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
        self.overworld = Overworld(current_location, self.available_locations, self.screen, self.background, self.createLocation, self.enemies,
                                   self.enemy_locations, self.visited_locations, self.treasure_locations, self.npc_locations, self.ui_inventory)
        self.screen_status = 'overworld'

    def run(self):
        self.displayBackground()
        self.displayHud()
        self.displayInventory()
        if self.screen_status == 'overworld':
            self.overworld.run()
        else:
            self.location.run()