from Controller import GameData
from Controller.GameData import locations, player
from Controller.Setting import screen_width, screen_height
from Model.BattleSystem.BattleSystem import BattleSystem
import Model.Entities.Enemy.Enemy
import Model.Inventory.Item
from pygame import mixer
import pygame
class Location:
    def __init__(self, current_location, surface, create_overworld, remaining_enemies, enemy_locations, visited_locations,
                 treasure_locations, npc_locations):
        #location setup
        self.display_surface = surface
        self.current_location = current_location
        location_data = GameData.locations[current_location]
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
        self.win_time = 0
        self.win = False

    def run(self):
        current_time = pygame.time.get_ticks()
        if not self.location_content:
            self.create_overworld(self.current_location, self.new_available_locations, self.remaining_enemies,
                                  self.enemy_locations,
                                  self.visited_locations, self.treasure_locations, self.npc_locations)
        if isinstance(self.location_content, Model.Entities.Enemy.Enemy.Enemy):
            self.battle.start()
            if not self.location_content.isAlive():
                if not self.win:
                    win_sound = mixer.Sound('../Controller/Sounds/Jingle_Achievement_00.wav')
                    win_sound.play()
                    self.win_time = pygame.time.get_ticks()
                    self.win = True

                if current_time - self.win_time >= 1500 and self.win:
                    GameData.defeated_enemies += 1
                    #go back to overworld
                    print("going back to overworld")
                    if self.current_location == 9 and GameData.level == 0:
                        GameData.locations[4]['content'] = None
                        GameData.chad.setDialogue("There has to be a way out of the dungeon!")
                        GameData.locations[8]['content'] = GameData.chad
                        #GameData.player.max_ap += 1
                    if self.current_location == 9 and GameData.level == 1:
                        #GameData.locations[4]['content'] = None
                        GameData.chad.setDialogue("Thanks for saving me from the goblin! Now I must find a way out!")
                        GameData.chad.quest += 1
                        #GameData.locations[8]['content'] = GameData.chad
                    if self.current_location == 7 and GameData.level == 2 and GameData.chad.quest == 1:
                        GameData.chad.setDialogue("This makes twice now. Thank you for saving my life. I'll be right behind you.")
                        GameData.chad.quest += 1
                    self.create_overworld(self.current_location, self.new_available_locations, self.remaining_enemies,
                                          self.enemy_locations,
                                          self.visited_locations, self.treasure_locations, self.npc_locations)
                    #reinitialize enemy for reuse
                    print("reinitialized enemy")
                    self.location_content.__init__(self.location_content.getName(), self.location_content.getMaxHp(),
                                                   self.location_content.getPower(),
                                                   self.location_content.getAttackPattern(),
                                                   self.location_content.image)
            if not player.isAlive():
                lose_sound = mixer.Sound('../Controller/Sounds/lose sound 1_0.wav')
                lose_sound.play()
                print("you lose!")
                print(self.enemy_locations)
                self.create_overworld(self.current_location, self.new_available_locations, self.remaining_enemies,
                                      self.enemy_locations,
                                      self.visited_locations, self.treasure_locations, self.npc_locations)
