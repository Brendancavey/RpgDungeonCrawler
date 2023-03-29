from Controller import GameData
from Controller.GameData import locations, player
from Controller.Setting import screen_width, screen_height
from Model.BattleSystem.BattleSystem import BattleSystem
from Model.Overworld.Overworld import Icon
from Model.Sprites.Button import Button
from Model.InventoryUI import InventoryUI
import Model.Entities.Enemy.Enemy
import Model.Inventory.Item
from pygame import mixer
import pygame
class Location:
    smallFont = pygame.font.Font(None, 22)
    smallFont.set_bold(True)
    mediumFont = pygame.font.Font(None, 35)
    def __init__(self, current_location, surface, create_overworld, remaining_enemies, enemy_locations, visited_locations,
                 treasure_locations, npc_locations, ui_inventory):
        #location setup
        self.display_surface = surface
        self.current_location = current_location
        location_data = GameData.locations[current_location]
        self.location_content = location_data['content']
        self.new_available_locations = location_data['unlock']

        #time
        self.click_time = pygame.time.get_ticks()
        self.current_time = pygame.time.get_ticks()

        #ui inventory
        self.ui_inventory = ui_inventory

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

        #loot
        self.picked_up_loot = False
        self.clicked = False
        self.loot = pygame.sprite.Group()
        self.width_offset = 200
        self.coin_quantity = self.smallFont.render("", True, 'black')
        self.setupLoot()
    def setupLoot(self):
        image_height_offset = 0
        self.loot = pygame.sprite.Group()
        self.complete_button = Button(75, 30, screen_width/2, screen_height/2 + 20, 'green', action_name= 'Done', id= 0)
        self.collect_button = Button(120, 30, screen_width/2 - 140, screen_height/2 + 20, 'green', action_name= 'Collect All', id= 1)
        self.button_group = pygame.sprite.Group()
        self.button_group.add(self.complete_button)
        self.button_group.add(self.collect_button)
        for loot in self.location_content.loot:
            image_pos = (screen_width / 2 - self.width_offset + 50, screen_height / 2 - self.width_offset + 80 + image_height_offset)
            if isinstance(loot, int):
                self.coin = Icon(image_pos, image=pygame.image.load('../View/Graphics/coin.png').convert_alpha())
                self.coin_quantity = self.smallFont.render("(" + str(loot) + ")", True, 'black')
                self.loot.add(self.coin)
            elif isinstance(loot, Model.Items.Potion.Potion):
                image = Icon(image_pos, image=pygame.image.load('../View/Graphics/potionRed.png').convert_alpha())
                self.loot.add(image)
            elif isinstance(loot, Model.Items.Armor.Armor):
                image = Icon(image_pos, image=pygame.image.load('../View/Graphics/armor.png').convert_alpha())
                self.loot.add(image)
            elif isinstance(loot, Model.Items.Weapon.Weapon):
                image = Icon(image_pos, image=pygame.image.load('../View/Graphics/sword.png').convert_alpha())
                self.loot.add(image)
            elif isinstance(loot, Model.Items.Accessory.Accessory):
                image = Icon(image_pos, image=pygame.image.load('../View/Graphics/scroll.png').convert_alpha())
                self.loot.add(image)
            image_height_offset += 50
    def showLoot(self):
        pos = pygame.mouse.get_pos()

        self.loot_surface = pygame.Surface((250,250))
        self.loot_surface.fill('bisque2')
        self.loot_title_text = self.mediumFont.render("Loot!", False, 'black')
        self.loot_title_image = pygame.image.load('../View/Graphics/chest_open.png').convert_alpha()
        self.display_surface.blit(self.loot_surface, (screen_width/2 - self.width_offset, screen_height/2 - self.width_offset))
        self.display_surface.blit(self.loot_title_text, (screen_width/2 - self.width_offset + 100, screen_height/2 - self.width_offset + 15))
        self.display_surface.blit(self.loot_title_image,
                                  (screen_width / 2 - self.width_offset + 50, screen_height / 2 - self.width_offset + 10))
        if self.coin in self.loot:
            self.display_surface.blit(self.coin_quantity,
                                      (screen_width / 2 - self.width_offset + 15,
                                       screen_height / 2 - self.width_offset + 74))
        self.loot.draw(self.display_surface)
        self.button_group.draw(self.display_surface)
        self.button_group.update()

        self.button_group.sprites()[0].renderButtonText(self.display_surface)
        self.button_group.sprites()[1].renderButtonText(self.display_surface, width_offset= -25)
        if self.button_group.sprites()[0].isClicked():
            self.picked_up_loot = True
        if self.button_group.sprites()[1].isClicked():
            for idx, sprite in enumerate(self.loot.sprites().copy()):
                if isinstance(self.location_content.loot[idx], int):
                    sound = mixer.Sound('../Controller/Sounds/Pickup_Gold_00.wav')
                    sound.play()
                    player.modifyGold(self.location_content.loot[idx])
                elif isinstance(self.location_content.loot[idx], Model.Items.Potion.Potion):
                    sound = mixer.Sound('../Controller/Sounds/bubble2.wav')
                    sound.play()
                    player.itemObtain(self.location_content.loot[idx])
                elif isinstance(self.location_content.loot[idx], Model.Items.Weapon.Weapon):
                    sound = mixer.Sound('../Controller/Sounds/sword-unsheathe5.wav')
                    sound.play()
                    player.itemObtain(self.location_content.loot[idx])
                elif isinstance(self.location_content.loot[idx], Model.Items.Armor.Armor):
                    sound = mixer.Sound('../Controller/Sounds/chainmail1.wav')
                    sound.play()
                    player.itemObtain(self.location_content.loot[idx])
                elif isinstance(self.location_content.loot[idx], Model.Items.Accessory.Accessory):
                    sound = mixer.Sound('../Controller/Sounds/Inventory_Open_01.wav')
                    sound.play()
                    player.itemObtain(self.location_content.loot[idx])
                self.ui_inventory.showInventory()
                pygame.time.wait(75)
            self.loot = pygame.sprite.Group()
        if self.loot:
            for sprite in self.loot.sprites():
                if sprite.rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                    idx = self.loot.sprites().index(sprite)
                    if isinstance(self.location_content.loot[idx], int):
                        sound = mixer.Sound('../Controller/Sounds/Pickup_Gold_00.wav')
                        sound.play()
                        player.modifyGold(self.location_content.loot[idx])
                        self.location_content.loot.pop(idx)
                        self.setupLoot()
                    elif isinstance(self.location_content.loot[idx], Model.Items.Potion.Potion):
                        sound = mixer.Sound('../Controller/Sounds/bubble2.wav')
                        sound.play()
                        player.itemObtain(self.location_content.loot[idx])
                        self.location_content.loot.pop(idx)
                        self.setupLoot()
                    elif isinstance(self.location_content.loot[idx], Model.Items.Weapon.Weapon):
                        sound = mixer.Sound('../Controller/Sounds/sword-unsheathe5.wav')
                        sound.play()
                        player.itemObtain(self.location_content.loot[idx])
                        self.location_content.loot.pop(idx)
                        self.setupLoot()
                    elif isinstance(self.location_content.loot[idx], Model.Items.Armor.Armor):
                        sound = mixer.Sound('../Controller/Sounds/chainmail1.wav')
                        sound.play()
                        player.itemObtain(self.location_content.loot[idx])
                        self.location_content.loot.pop(idx)
                        self.setupLoot()
                    elif isinstance(self.location_content.loot[idx], Model.Items.Accessory.Accessory):
                        sound = mixer.Sound('../Controller/Sounds/Inventory_Open_01.wav')
                        sound.play()
                        player.itemObtain(self.location_content.loot[idx])
                        self.location_content.loot.pop(idx)
                        self.setupLoot()
                    self.clicked = True
                    self.ui_inventory.showInventory()
    def timer(self):
        wait_time = 100
        if self.clicked and pygame.mouse.get_pressed()[0] == 1:
            self.click_time = pygame.time.get_ticks()
        self.current_time = pygame.time.get_ticks()
        if self.current_time - self.click_time >= wait_time:
            self.clicked = False

    def run(self):
        self.timer()
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

                if self.current_time - self.win_time >= 1500 and self.win:
                    self.showLoot()
                    self.loot.update()
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

                    if self.picked_up_loot:
                        GameData.defeated_enemies += 1
                        # go back to overworld
                        print("going back to overworld")
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
