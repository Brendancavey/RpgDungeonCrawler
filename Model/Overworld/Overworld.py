import pygame

import Model.Inventory.Item
from Controller.GameData import locations, inventory_slots, player
from Controller.Setting import screen_height, screen_width
class Node(pygame.sprite.Sprite):
    def __init__(self, pos, status, icon_speed):
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
    def __init__(self, pos, color = None, image = None, size = (20,20), inventory_slot = 0):
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
        self.inventory_slot = inventory_slot
    def update(self):
        self.rect.center = self.pos
class Overworld():
    font = pygame.font.Font(None, 35)
    largeFont = pygame.font.Font(None, 65)
    def __init__(self, start_location, available_locations, display_surface, create_location, enemies, enemy_locations, visited,
                 treasure_locations, npc_locations):
        #setup
        self.display_surface = display_surface
        self.available_locations = available_locations
        self.current_location = start_location
        self.create_location = create_location
        self.win_game = False

        #inventory
        self.inventory_idx = 0

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
        self.surface = pygame.Surface((screen_width, screen_height))
        self.surface.fill("black")

        #sprites
        self.setupNodes()
        self.setupPlayerIcon()
        self.setupEnemyIcons()
        self.setupTreasureIcons()
        self.setupNPCIcons()
        self.setupInventory()
        self.updateInventory()
    def getPrevNode(self):
        return self.visited.pop(-1)
    def getNextNode(self, direction):
        print("was at " + str(self.current_location))
        if direction == 'up':
            return self.current_location + 1
        elif direction == 'right':
            return self.current_location + 2
        elif direction == 'down':
            return self.current_location - 1
        elif direction == 'left':
            return self.current_location - 2
    def checkForNextStage(self):
        if self.current_location == 10:
            self.win_game = True
            """self.__init__(0, [-1, 0, 1, 2], self.display_surface, self.create_location,
                          self.enemy_icons, self.enemy_locations, self.visited, self.treasure_locations,
                          self.npc_locations)"""
    def displayWinMessage(self):
        if self.win_game == True:
            win_text = self.largeFont.render("thank you for playtesting!", False, "green")
            self.screen.blit(win_text, (300, 100))
    def findNextNode(self, current_location, direction):
        if direction == 'up':
            return current_location + 1
        elif direction == 'right':
            return current_location + 2
    def setupInventory(self):
        self.ui_inventory = pygame.sprite.GroupSingle()
        self.ui_items = pygame.sprite.Group()
        self.ui_weapons = pygame.sprite.Group()
        #reset values to account for player using items in battle
        #update values via updateInventory()
        for slots in inventory_slots.values():
            slots['content'] = None

        sprite = Icon((1150,350), color = 'cornsilk4', size = (275, 400))
        self.ui_inventory.add(sprite)

    def updateInventory(self):
        #find empty slot
        for inventory in player.getInventory():
            if isinstance(player.getInventory()[inventory], dict):
                for item in player.getInventory()[inventory]:
                    for slot in inventory_slots.values():
                        if slot['content']:
                            if item.getId() == slot['content'].getId():
                                break
                        else:
                            slot['content'] = item
                            break

        #update slot with graphic
        for idx, slot in enumerate(inventory_slots.values()):
            if idx == self.inventory_idx:
                if isinstance(slot['content'], Model.Items.Potion.Potion):
                    sprite = Icon(slot['slot_pos'], image = pygame.image.load('../View/Graphics/potionRed.png').convert_alpha(), inventory_slot = idx)
                    self.ui_items.add(sprite)
                    self.inventory_idx += 1
                elif isinstance(slot['content'], Model.Items.Weapon.Weapon):
                    sprite = Icon(slot['slot_pos'], image = pygame.image.load('../View/Graphics/sword.png').convert_alpha(), inventory_slot = idx)
                    self.ui_weapons.add(sprite)
                    self.inventory_idx += 1

    def updateHudPlayer(self):
        self.hud_text_playerHp = self.font.render("HP: " + str(player.getHp()) + "/" + str(player.getMaxHp()), False, 'red')
        self.hud_text_playerPwr = self.font.render("Attack: " + str(player.getPower()), False, "white")
        self.screen.blit(self.hud_text_playerHp,(1100,50))
        self.screen.blit(self.hud_text_playerPwr,(1100,100))
    def interactWithInventory(self):
        pos = pygame.mouse.get_pos()
        # hover over items
        if self.ui_items:
            for sprite in self.ui_items.sprites():
                if sprite.rect.collidepoint(pos):
                    idx = self.ui_items.sprites().index(sprite)
                    if isinstance(inventory_slots[sprite.inventory_slot]['content'], Model.Items.Potion.Potion):
                        self.ui_text = self.font.render(list(player.getItems())[idx].getDescription(), False, "Green")
                        self.screen.blit(self.ui_text, (900, 600))
                        break
        if self.ui_weapons:
            for sprite in self.ui_weapons.sprites():
                if sprite.rect.collidepoint(pos):
                    idx = self.ui_weapons.sprites().index(sprite)
                    if isinstance(inventory_slots[sprite.inventory_slot]['content'], Model.Items.Weapon.Weapon):
                        self.ui_text = self.font.render(list(player.getInventory()['Weapons'])[idx].getDescription(), False, "Green")
                        self.screen.blit(self.ui_text, (900, 600))
                        break

        #click on items
        if self.ui_weapons:
            for sprite in self.ui_weapons.sprites():
                if sprite.rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] == 1:
                    if isinstance(inventory_slots[sprite.inventory_slot]['content'], Model.Items.Weapon.Weapon):
                        player.equip(inventory_slots[sprite.inventory_slot]['content'])
                        inventory_slots[sprite.inventory_slot]['content'] = None
                        self.ui_weapons.sprites().remove(sprite)
                        #reinitialize self to reset inventory icons
                        self.__init__(self.current_location, self.available_locations, self.display_surface, self.create_location,
                                      self.enemy_icons, self.enemy_locations, self.visited, self.treasure_locations, self.npc_locations)
                        break
        if self.ui_items:
            for sprite in self.ui_items.sprites():
                if sprite.rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] == 1:
                    if isinstance(inventory_slots[sprite.inventory_slot]['content'], Model.Items.Potion.Potion):
                        if player.getHp() >= player.getMaxHp():
                            print("Player at max hp!")
                        else:
                            player.itemUse(inventory_slots[sprite.inventory_slot]['content'])
                            inventory_slots[sprite.inventory_slot]['content'] = None
                            self.ui_items.sprites().remove(sprite)
                            #reinitialize self to reset inventory icons
                            self.__init__(self.current_location, self.available_locations, self.display_surface, self.create_location,
                                          self.enemy_icons, self.enemy_locations, self.visited, self.treasure_locations, self.npc_locations)
                            break
    def setupPlayerIcon(self):
        self.player_icon = pygame.sprite.GroupSingle()
        for idx, location in enumerate(self.cur_adjaceny_list):
            if self.current_location == location:
                idx_of_nodes = idx
        current_node = self.nodes.sprites()[idx_of_nodes]
        icon_sprite = Icon(current_node.rect.center, 'blue', pygame.image.load('../View/Graphics/player.png').convert_alpha())
        self.player_icon.add(icon_sprite)
    def setupEnemyIcons(self):
        icon_sprites = []
        self.enemy_icons = pygame.sprite.Group()
        for location in self.enemy_locations:
            if location in self.cur_adjaceny_list:
                idx = self.cur_adjaceny_list.index(location)
                icon = Icon(self.nodes.sprites()[idx].rect.center, 'red', pygame.image.load('../View/Graphics/goblin.png').convert_alpha())
                icon_sprites.append(icon)
        for icon in icon_sprites:
            self.enemy_icons.add(icon)

        #destroy sprite on collision
        pygame.sprite.spritecollide(self.player_icon.sprite, self.enemy_icons, True)
    def setupTreasureIcons(self):
        icon_sprites = []
        self.treasure_icons = pygame.sprite.Group()
        for location in self.treasure_locations:
            if location in self.cur_adjaceny_list:
                idx = self.cur_adjaceny_list.index(location)
                icon = Icon(self.nodes.sprites()[idx].rect.center, 'yellow', pygame.image.load('../View/Graphics/chest.png').convert_alpha())
                icon_sprites.append(icon)
        for icon in icon_sprites:
            self.treasure_icons.add(icon)

        #destroy sprite on collision
        pygame.sprite.spritecollide(self.player_icon.sprite, self.treasure_icons, True)
    def setupNPCIcons(self):
        icon_sprites = []
        self.npc_icons = pygame.sprite.Group()
        for location in self.npc_locations:
            if location in self.cur_adjaceny_list:
                idx = self.cur_adjaceny_list.index(location)
                icon = Icon(self.nodes.sprites()[idx].rect.center, 'green', pygame.image.load('../View/Graphics/NPC1.png').convert_alpha())
                icon_sprites.append(icon)
        for icon in icon_sprites:
            self.npc_icons.add(icon)

        #destroy sprite on collision to prevent continuous loop of sprite collision.
        #npc is redrawn upon reentering overworld
        #pygame.sprite.spritecollide(self.player_icon.sprite, self.npc_icons, True)

    def setupNodes(self):
        self.nodes = pygame.sprite.Group()
        for key in locations:
            if self.current_location == key:
                adjacency_list = locations[key]['unlock']
                self.cur_adjaceny_list = adjacency_list
        for node in adjacency_list:
            node_sprite = Node(locations[node]['node_pos'], 'available', self.speed)
            self.nodes.add(node_sprite)

    def drawPaths(self):
        line_width = 6
        #points = [node['node_pos'] for idx, node in enumerate(locations.values())]
        self.current_point = locations[self.current_location]['node_pos']
        points = [node.getPos() for node in self.nodes if node.status == 'available']
        for point in points:
            pygame.draw.lines(self.display_surface, 'white', False, (self.current_point, point), line_width)

    def input(self):
        keys = pygame.key.get_pressed()
        location_data = locations[self.current_location]
        new_available_locations = location_data['unlock']


        #collide with enemy
        if pygame.sprite.spritecollide(self.player_icon.sprite, self.enemy_icons, True):
            self.enemy_locations.remove(self.current_location)
            self.create_location(self.current_location, self.enemy_icons, self.enemy_locations, self.treasure_locations,
                                 self.npc_locations)
            location_data['content'] = None


        #collide with treasure
        if pygame.sprite.spritecollide(self.player_icon.sprite, self.treasure_icons, True):
            self.treasure_locations.remove(self.current_location)
            print("You received a treasure!")
            location_content = location_data['content']
            player.interact(location_content)
            self.updateInventory()
            location_data['content'] = None

            """self.create_location(self.current_location, self.enemy_icons, self.enemy_locations, self.treasure_locations,
                                 self.npc_locations)"""

        #collide with npc
        if pygame.sprite.spritecollide(self.player_icon.sprite, self.npc_icons, False):
            location_content = location_data['content']
            player.interact(location_content, self.display_surface)
            """self.create_location(self.current_location, self.enemy_icons, self.enemy_locations, self.treasure_locations,
                                 self.npc_locations)"""

        #player_icon movement
        if not self.moving:
            if keys[pygame.K_UP] and self.getNextNode('up') in self.available_locations:
                self.visited.append(self.current_location)
                self.move_direction = self.getMovementData(self.getNextNode('up'))
            elif keys[pygame.K_DOWN] and self.getNextNode('down') in self.available_locations:
                self.visited.append(self.current_location)
                self.move_direction = self.getMovementData(self.getNextNode('down'))
            elif keys[pygame.K_RIGHT] and self.getNextNode('right') in self.available_locations:
                self.visited.append(self.current_location)
                self.move_direction = self.getMovementData(self.getNextNode('right'))
            elif(keys[pygame.K_LEFT]) and self.getNextNode('left') in self.available_locations:
                self.visited.append(self.current_location)
                self.move_direction = self.getMovementData(self.getNextNode('left'))

        #update for new location
        self.available_locations = new_available_locations
        self.setupEnemyIcons()
        self.setupTreasureIcons()
        self.setupNPCIcons()


    def getMovementData(self, end_location):
        #get current node
        for idx, location in enumerate(self.cur_adjaceny_list):
            if self.current_location == location:
                idx_of_nodes = idx
        current_node = self.nodes.sprites()[idx_of_nodes]
        start = pygame.math.Vector2(current_node.rect.center)

        #get end node
        for idx, location in enumerate(self.cur_adjaceny_list):
            if end_location == location:
                idx_of_nodes = idx
        end_node = self.nodes.sprites()[idx_of_nodes]
        end = pygame.math.Vector2(end_node.rect.center)

        #move icon
        self.current_location = end_location
        self.moving = True
        return(end - start).normalize()
    def updatePlayerIconPos(self):
        if self.moving and self.move_direction:
            self.player_icon.sprite.pos += self.move_direction * self.speed
            for idx, location in enumerate(self.cur_adjaceny_list):
                if self.current_location == location:
                    idx_of_nodes = idx
            target_node = self.nodes.sprites()[idx_of_nodes]
            if target_node.detection_zone.collidepoint(self.player_icon.sprite.pos):
                self.moving = False
                self.move_direction = pygame.math.Vector2(0,0)
                self.checkForNextStage()

    def run(self):
        self.screen.blit(self.surface, (0, 0))
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
        self.updateHudPlayer()



        #testing
        self.ui_inventory.draw(self.display_surface)
        self.ui_items.draw(self.display_surface)
        self.ui_weapons.draw(self.display_surface)
        self.interactWithInventory()
        self.displayWinMessage()

