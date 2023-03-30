import pygame
import Model.Inventory.Item
from Controller import GameData
from Controller.GameData import locations, inventory_slots, player, enemy_locations, treasure_locations, npc_locations
from Controller.Setting import screen_height, screen_width
from Model.BattleSystem.Ability.AbilityList import ability_list
from pygame import mixer
import Model.Entities.Enemy.Enemy
class Node(pygame.sprite.Sprite):
    def __init__(self, pos, status, icon_speed):
        icon_speed += 1
        node_size = (100,80)
        super().__init__()
        self.image = pygame.Surface(node_size)
        self.status = status
        if self.status == 'available':
            self.image.fill('grey')
        else:
            self.image.fill('black')
        self.rect = self.image.get_rect(center = pos)
        self.detection_zone = pygame.Rect(self.rect.centerx-(icon_speed/2),self.rect.centery-(icon_speed/2),icon_speed,icon_speed)
        self.pos = pos

    def getPos(self):
        return self.pos
class Icon(pygame.sprite.Sprite):
    def __init__(self, pos, color = None, image = None, size = (20,20), idx = 0, icon_type = None, icon_speed = 16):
        super().__init__()
        self.pos = pos
        if image == None and color == None:
            self.image = pygame.Surface(size)
            self.image.fill('pink')
        elif image == None:
            self.image = pygame.Surface(size)
            self.image.fill(color)
        else:
            self.image = image
        self.rect = self.image.get_rect(center = pos)
        self.detection_zone = pygame.Rect(self.rect.centerx-(icon_speed/2),self.rect.centery-(icon_speed/2),icon_speed,icon_speed)
        self.idx = idx
        self.icon_type = icon_type
    def update(self):
        self.rect.center = self.pos
class Overworld():
    font = pygame.font.Font(None, 35)
    largeFont = pygame.font.Font(None, 65)
    smallFont = pygame.font.Font(None, 29)
    def __init__(self, start_location, available_locations, display_surface, background, create_location, enemies, enemy_locations, visited,
                 treasure_locations, npc_locations, ui_inventory):
        #setup
        self.display_surface = display_surface
        self.background = background
        self.cur_adjacency_list = available_locations
        self.current_location = start_location
        self.create_location = create_location
        self.ui_inventory = ui_inventory
        self.win_level = False
        self.level_up = False
        self.checkForLevelUp()

        #timer
        self.key_press_time = pygame.time.get_ticks()
        self.current_time = pygame.time.get_ticks()
        self.key_pressed = False

        #enemies
        self.enemy_icons = enemies
        self.enemy_locations = enemy_locations

        #treasure
        self.treasure_locations = treasure_locations

        #npc
        self.npc_locations = npc_locations

        #movement logic
        self.moving = False
        self.move_direction = pygame.math.Vector2(0,0)
        self.speed = 4

        #overworld map stack data structure
        self.visited = visited

        #screen and surface
        self.width = screen_width
        self.height = screen_height
        self.screen = pygame.display.set_mode((screen_width, screen_height))

        #call setup
        self.setupNodes()
        self.setupPlayerIcon()
        self.setupOverworldIcons()

    def getPrevNode(self):
        return self.visited.pop(-1)
    def getNextNode(self, direction):
        if direction == 'up':
            return self.current_location + 1
        elif direction == 'right':
            return self.current_location + 2
        elif direction == 'down':
            return self.current_location - 1
        elif direction == 'left':
            return self.current_location - 2
    def checkForLevelUp(self):
        print("defeated enemies: " + str(GameData.defeated_enemies))
        if GameData.defeated_enemies == 2 and player.player_level == 1:
            mixer.Channel(0).pause()
            level_up_sound = mixer.Sound('../Controller/Sounds/Jingle_Win_00.wav')
            level_up_sound.play()
            player.modifyMaxHp(player.getMaxHp() + 1)
            player.max_ap += 1
            player.player_level += 1
            player.addAbility(ability_list[1])
            self.level_up = True
        elif GameData.defeated_enemies == 5 and player.player_level == 2:
            pass
    def displayLevelUpMessage(self):
        if self.level_up and player.player_level == 2:
            level_up_text = self.largeFont.render("You've grown stronger!", False, 'green')
            textbox = pygame.Surface((1280, 200))
            textbox.fill('bisque')
            level_up_lvl = self.smallFont.render("Lvl: " + str(player.player_level), False, 'black')
            level_up_hp = self.smallFont.render("HP: +1", False, 'black')
            level_up_ap = self.smallFont.render("AP: +1", False, 'black')
            new_ability = self.smallFont.render("New ability unlocked: " + str(player.abilities[1]), False, 'black')
            self.screen.blit(level_up_text, (300, 100))
            self.screen.blit(textbox, (0, 550))
            self.screen.blit(level_up_lvl, (25, 565))
            self.screen.blit(level_up_hp, (25, 590))
            self.screen.blit(level_up_ap, (25, 615))
            self.screen.blit(new_ability, (25, 640))
        elif self.level_up and player.player_level == 3:
            pass
        else:
            mixer.Channel(0).unpause()
    def checkForWinCondition(self):
        if self.current_location == 10:
            self.win_level = True
    def displayWinMessage(self):
        if self.win_level == True:
            #demo purposes
            if GameData.level <= 2:
                GameData.level += 1
            if GameData.level >= 3:
                win_text = self.largeFont.render("Thank you for play testing!", False, "green")
                self.screen.blit(win_text, (300, 100))
            #advance to next stage
            else:
                GameData.locations = GameData.determineLevel()
                GameData.treasure_locations = GameData.determineTreasureLocations()
                GameData.enemy_locations = GameData.determineEnemyLocations()
                GameData.npc_locations = GameData.determineNpcLocations()
                next_stage_sound = mixer.Sound('../Controller/Sounds/win sound 1-2.wav')
                next_stage_sound.play()
                self.__init__(0, [-1, 0], self.display_surface, self.background, self.create_location,
                              self.enemy_icons, GameData.enemy_locations, [], GameData.treasure_locations, GameData.npc_locations, self.ui_inventory )
    def findNextNode(self, current_location, direction):
        if direction == 'up':
            return current_location + 1
        elif direction == 'right':
            return current_location + 2

    def setupPlayerIcon(self):
        self.player_icon = pygame.sprite.GroupSingle()
        idx_of_nodes = self.cur_adjacency_list.index(self.current_location)
        current_node = self.nodes.sprites()[idx_of_nodes]
        icon_sprite = Icon(current_node.rect.center, image = pygame.image.load('../View/Graphics/player.png').convert_alpha())
        self.player_icon.add(icon_sprite)
    def setupOverworldIcons(self):
        icon_sprites = []
        self.enemy_icons = pygame.sprite.Group()
        self.treasure_icons = pygame.sprite.Group()
        self.npc_icons = pygame.sprite.Group()

        #load graphic
        for idx, location in enumerate(self.cur_adjacency_list):
            if isinstance(GameData.locations[location]['content'], Model.Entities.Enemy.Enemy.Enemy):
                icon = Icon(self.nodes.sprites()[idx].rect.center,
                            image=GameData.locations[location]['content'].image,
                            icon_type='enemy')
                icon_sprites.append(icon)
            elif isinstance(GameData.locations[location]['content'], Model.Inventory.Item.Item):
                icon = Icon(self.nodes.sprites()[idx].rect.center,
                            image = pygame.image.load('../View/Graphics/chest.png').convert_alpha(),
                            icon_type = 'treasure')
                icon_sprites.append(icon)
            elif isinstance(GameData.locations[location]['content'], Model.Entities.NPC.NPC):
                icon = Icon(self.nodes.sprites()[idx].rect.center,
                            image = pygame.image.load('../View/Graphics/NPC1.png').convert_alpha(),
                            icon_type = 'npc')
                icon_sprites.append(icon)

        #add sprite to correct group
        for icon in icon_sprites:
            if icon.icon_type == 'enemy':
                self.enemy_icons.add(icon)
            elif icon.icon_type == 'treasure':
                self.treasure_icons.add(icon)
            elif icon.icon_type == 'npc':
                self.npc_icons.add(icon)

        #destroy sprite on collision
        pygame.sprite.spritecollide(self.player_icon.sprite, self.enemy_icons, True)
        pygame.sprite.spritecollide(self.player_icon.sprite, self.treasure_icons, True)

    def setupNodes(self):
        self.nodes = pygame.sprite.Group()
        self.cur_adjacency_list = GameData.locations[self.current_location]['unlock']
        for node in self.cur_adjacency_list:
            node_sprite = Node(GameData.locations[node]['node_pos'], 'available', self.speed)
            self.nodes.add(node_sprite)

    def drawPaths(self):
        line_width = 6
        self.current_point = GameData.locations[self.current_location]['node_pos']
        points = [node.getPos() for node in self.nodes if node.status == 'available']
        for point in points:
            pygame.draw.lines(self.display_surface, 'white', False, (self.current_point, point), line_width)

    def input(self):
        pos = pygame.mouse.get_pos()
        keys = pygame.key.get_pressed()
        location_data = GameData.locations[self.current_location]
        new_available_locations = location_data['unlock']

        #collide with enemy
        if pygame.sprite.spritecollide(self.player_icon.sprite, self.enemy_icons, True):
            enemy_sound = location_data['content'].encounter_sound
            enemy_sound.play()
            self.enemy_locations.remove(self.current_location)
            self.create_location(self.current_location, self.enemy_icons, self.enemy_locations, self.treasure_locations,
                                 self.npc_locations)
            location_data['content'] = None

        #collide with treasure
        if pygame.sprite.spritecollide(self.player_icon.sprite, self.treasure_icons, True):
            treasure_sound = mixer.Sound('../Controller/Sounds/swing2.wav')
            treasure_sound.play()
            self.treasure_locations.remove(self.current_location)
            print("You received a treasure!")
            location_content = location_data['content']
            player.interact(location_content)
            location_data['content'] = None
            self.ui_inventory.showInventory()

        #collide with npc
        if pygame.sprite.spritecollide(self.player_icon.sprite, self.npc_icons, False):
            location_content = location_data['content']
            player.interact(location_content, self.display_surface)

        #player_icon movement
        if not self.moving and not self.key_pressed:
            #mouse movement
            if self.nodes:
                for idx, node in enumerate(self.nodes.sprites()):
                    if node.rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] == 1 and self.current_location != self.cur_adjacency_list[idx]:
                        curr_node_idx = self.cur_adjacency_list.index(self.current_location)
                        start_node = self.nodes.sprites()[curr_node_idx]
                        end_node = self.nodes.sprites()[idx]
                        start = pygame.math.Vector2(start_node.rect.center)
                        end = pygame.math.Vector2(end_node.rect.center)
                        self.move_direction = (end-start).normalize()
                        self.moving = True
                        self.current_location = self.cur_adjacency_list[idx]
                        self.level_up = False
            #keyboard movement
            if keys[pygame.K_UP] and self.getNextNode('up') in self.cur_adjacency_list:
                self.visited.append(self.current_location)
                self.move_direction = self.getMovementData(self.getNextNode('up'))
                self.level_up = False
            elif keys[pygame.K_DOWN] and self.getNextNode('down') in self.cur_adjacency_list:
                self.visited.append(self.current_location)
                self.move_direction = self.getMovementData(self.getNextNode('down'))
                self.level_up = False
            elif keys[pygame.K_RIGHT] and self.getNextNode('right') in self.cur_adjacency_list:
                self.visited.append(self.current_location)
                self.move_direction = self.getMovementData(self.getNextNode('right'))
                self.level_up = False
            elif(keys[pygame.K_LEFT]) and self.getNextNode('left') in self.cur_adjacency_list:
                self.visited.append(self.current_location)
                self.move_direction = self.getMovementData(self.getNextNode('left'))
                self.level_up = False

        #update for new location
        self.cur_adjacency_list = new_available_locations
        self.setupOverworldIcons()

    def getMovementData(self, end_location):
        #get current node
        idx_of_nodes = self.cur_adjacency_list.index(self.current_location)
        current_node = self.nodes.sprites()[idx_of_nodes]
        start = pygame.math.Vector2(current_node.rect.center)

        #get end node
        idx_of_nodes = self.cur_adjacency_list.index(end_location)
        end_node = self.nodes.sprites()[idx_of_nodes]
        end = pygame.math.Vector2(end_node.rect.center)

        #move icon
        self.current_location = end_location
        self.moving = True
        return(end - start).normalize()
    def updatePlayerIconPos(self):
        if self.moving and self.move_direction:
            self.player_icon.sprite.pos += self.move_direction * (self.speed)
            idx_of_nodes = self.cur_adjacency_list.index(self.current_location)
            target_node = self.nodes.sprites()[idx_of_nodes]
            if target_node.detection_zone.collidepoint(self.player_icon.sprite.pos):
                self.moving = False
                self.move_direction = pygame.math.Vector2(0,0)
                self.checkForWinCondition()
    def run(self):
        self.updatePlayerIconPos()
        self.setupNodes()
        self.drawPaths()
        self.player_icon.update()
        self.nodes.draw(self.display_surface)
        self.enemy_icons.draw(self.display_surface)
        self.treasure_icons.draw(self.display_surface)
        self.npc_icons.draw(self.display_surface)
        self.player_icon.draw(self.display_surface)
        self.input()
        self.displayWinMessage()
        self.displayLevelUpMessage()