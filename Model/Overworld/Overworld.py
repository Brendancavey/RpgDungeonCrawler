import pygame
import Model.Inventory.Item
from Controller.GameData import locations, inventory_slots, player
from Controller.Setting import screen_height, screen_width
import Model.Entities.Enemy.Enemy
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
    def __init__(self, pos, color = None, image = None, size = (20,20), inventory_slot = 0, icon_type = None):
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
        self.icon_type = icon_type
    def update(self):
        self.rect.center = self.pos
class Overworld():
    font = pygame.font.Font(None, 35)
    largeFont = pygame.font.Font(None, 65)
    smallFont = pygame.font.Font(None, 29)
    def __init__(self, start_location, available_locations, display_surface, create_location, enemies, enemy_locations, visited,
                 treasure_locations, npc_locations):
        #setup
        self.display_surface = display_surface
        self.cur_adjacency_list = available_locations
        self.current_location = start_location
        self.create_location = create_location
        self.mouse_click_time = 0
        self.current_time = 0
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
        self.background = pygame.image.load('../View/Graphics/dungeon.png').convert_alpha()

        #sprites
        self.setupNodes()
        self.setupPlayerIcon()
        self.setupOverworldIcons()
        self.setupInventory()
        self.updateInventory()
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
    def checkForNextStage(self):
        if self.current_location == 10:
            self.win_game = True
    def displayWinMessage(self):
        if self.win_game == True:
            win_text = self.largeFont.render("Thank you for play testing!", False, "green")
            self.screen.blit(win_text, (300, 100))
    def findNextNode(self, current_location, direction):
        if direction == 'up':
            return current_location + 1
        elif direction == 'right':
            return current_location + 2
    def resetInventorySlots(self):
        for slots in inventory_slots.values():
            slots['content'] = None
    def setupInventory(self):
        #inventory & equipment hud
        self.ui_inventory = pygame.sprite.Group()
        self.ui_equipment = pygame.sprite.Group()

        #update inventory slots
        """reset values to account for player using items in battle
        update current items via updateInventory()"""
        self.resetInventorySlots()

        #load inventory text
        self.ui_inventory_title_surface = pygame.Surface ((150, 25))
        self.ui_inventory_title_surface.fill('bisque4')
        self.ui_inventory_title_text = self.font.render("Inventory", False, 'cornsilk3')

        #load inventory images
        inventory_layout = Icon((1110,275), image = pygame.image.load('../View/Graphics/inventory.png').convert_alpha())
        inventory_bar = Icon((1085, 422), image = pygame.image.load('../View/Graphics/inventory_bar.png').convert_alpha())
        inventory_icon = Icon((965, 419), image = pygame.image.load('../View/Graphics/backpack.png').convert_alpha())
        equipment_icon = Icon((1025, 419), image = pygame.image.load('../View/Graphics/armor.png').convert_alpha())
        self.ui_inventory.add(inventory_layout)
        self.ui_inventory.add(inventory_bar)
        self.ui_inventory.add(inventory_icon)
        self.ui_inventory.add(equipment_icon)

    def updateInventory(self):
        """reset values to account for player equipping or using items not in the
        order of inventory slots"""
        self.resetInventorySlots()
        self.inventory_idx = 0

        #inventory items/weapons
        self.ui_items = pygame.sprite.Group()
        self.ui_weapons = pygame.sprite.Group()

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

    def updateHud(self):
        self.hud_text_playerHp = self.font.render("HP: " + str(player.getHp()) + "/" + str(player.getMaxHp()), False, 'red')
        self.hud_text_playerPwr = self.font.render("Attack: " + str(player.getPower()), False, "white")
        self.screen.blit(self.hud_text_playerHp,(1100,50))
        self.screen.blit(self.hud_text_playerPwr,(1100,100))
    def interactWithInventory(self):
        pos = pygame.mouse.get_pos()
        ui_text_pos = (900, 470)
        ui_text_pos2 = (1050, 520)
        ui_text_surface_pos = (900, 470)
        ui_text_surface = pygame.Surface((375,75))
        ui_text_surface.fill('bisque4')
        self.screen.blit(ui_text_surface, ui_text_surface_pos)

        # hover over items
        if self.ui_items:
            for sprite in self.ui_items.sprites():
                if sprite.rect.collidepoint(pos):
                    self.screen.blit(ui_text_surface, ui_text_surface_pos)
                    idx = self.ui_items.sprites().index(sprite)
                    if isinstance(inventory_slots[sprite.inventory_slot]['content'], Model.Items.Potion.Potion):
                        if player.getHp() >= player.getMaxHp():
                            self.ui_text2 = self.smallFont.render("Player at max hp!", False, 'grey')
                        else:
                            self.ui_text2 = self.smallFont.render("Click to use", False, 'grey')
                        self.ui_text = self.font.render(list(player.getItems())[idx].getDescription(), False, "Green")
                        self.screen.blit(self.ui_text, ui_text_pos)
                        self.screen.blit(self.ui_text2, ui_text_pos2)
                        break
        if self.ui_weapons:
            for sprite in self.ui_weapons.sprites():
                if sprite.rect.collidepoint(pos):
                    self.screen.blit(ui_text_surface, ui_text_surface_pos)
                    idx = self.ui_weapons.sprites().index(sprite)
                    if isinstance(inventory_slots[sprite.inventory_slot]['content'], Model.Items.Weapon.Weapon):
                        self.ui_text = self.font.render(list(player.getInventory()['Weapons'])[idx].getDescription(), False, "Green")
                        self.ui_text2 = self.smallFont.render("Click to equip", False, 'grey')
                        self.screen.blit(self.ui_text, ui_text_pos)
                        self.screen.blit(self.ui_text2, ui_text_pos2)
                        break
        if self.ui_inventory:
            if self.ui_inventory.sprites()[2].rect.collidepoint(pos):
                self.screen.blit(ui_text_surface, ui_text_surface_pos)
                self.ui_text = self.font.render("Inventory", False, "Green")
                self.ui_text2 = self.smallFont.render("Click to view", False, 'grey')
                self.screen.blit(self.ui_text, ui_text_pos)
                self.screen.blit(self.ui_text2, ui_text_pos2)
            elif self.ui_inventory.sprites()[3].rect.collidepoint(pos):
                self.screen.blit(ui_text_surface, ui_text_surface_pos)
                self.ui_text = self.font.render("Equipment", False, "Green")
                self.ui_text2 = self.smallFont.render("Click to view", False, 'grey')
                self.screen.blit(self.ui_text, ui_text_pos)
                self.screen.blit(self.ui_text2, ui_text_pos2)
        if self.ui_equipment:
            eqp_weapon_text = "Weapon: None"
            eqp_armor_text = "Armor: None"
            eqp_accessory_text = "Accessory: None"
            if self.ui_equipment.sprites()[0].rect.collidepoint(pos):
                self.screen.blit(ui_text_surface, ui_text_surface_pos)
                if player.getEquippedItems()['Weapon']:
                    eqp_weapon_text = "Weapon: " + player.getEquippedItems()['Weapon'].getDescription()
                self.ui_text = self.smallFont.render(eqp_weapon_text,False, "Green")
                self.screen.blit(self.ui_text, ui_text_pos)
            elif self.ui_equipment.sprites()[1].rect.collidepoint(pos):
                self.screen.blit(ui_text_surface, ui_text_surface_pos)
                if player.getEquippedItems()['Armor']:
                    eqp_armor_text = "Armor: " + player.getEquippedItems()['Armor'].getDescription()
                self.ui_text = self.smallFont.render(eqp_armor_text,False, "Green")
                self.screen.blit(self.ui_text, ui_text_pos)
            elif self.ui_equipment.sprites()[2].rect.collidepoint(pos):
                self.screen.blit(ui_text_surface, ui_text_surface_pos)
                if player.getEquippedItems()['Accessory']:
                    eqp_accessory_text = "Accessory: " + player.getEquippedItems()['Accessory'].getDescription()
                self.ui_text = self.smallFont.render(eqp_accessory_text,False, "Green")
                self.screen.blit(self.ui_text, ui_text_pos)

        #click on items
        if self.ui_weapons:
            for sprite in self.ui_weapons.sprites():
                if sprite.rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                    if isinstance(inventory_slots[sprite.inventory_slot]['content'], Model.Items.Weapon.Weapon):
                        self.clicked = True
                        player.equip(inventory_slots[sprite.inventory_slot]['content'])
                        inventory_slots[sprite.inventory_slot]['content'] = None
                        self.ui_weapons.sprites().remove(sprite)
                        #reset inventory icons
                        self.showEquipment()
                        self.showInventory()
                        break
        if self.ui_items:
            for sprite in self.ui_items.sprites():
                if sprite.rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                    if isinstance(inventory_slots[sprite.inventory_slot]['content'], Model.Items.Potion.Potion):
                        self.clicked = True
                        if player.getHp() < player.getMaxHp():
                            player.itemUse(inventory_slots[sprite.inventory_slot]['content'])
                            inventory_slots[sprite.inventory_slot]['content'] = None
                            self.ui_items.sprites().remove(sprite)
                            # reset inventory icons
                            self.showEquipment()
                            self.showInventory()
                            break
        if self.ui_inventory:
            if self.ui_inventory.sprites()[2].rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] == 1:
                self.showInventory()
            elif self.ui_inventory.sprites()[3].rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] == 1:
                self.showEquipment()
    def timer(self):
        delay_time = 175
        if pygame.mouse.get_pressed()[0] == 1 and self.current_time > self.mouse_click_time + delay_time:
            self.mouse_click_time = pygame.time.get_ticks()
            self.clicked = False
        self.current_time = pygame.time.get_ticks()
    def showInventory(self):
        #reset equipment sprites
        self.ui_equipment = pygame.sprite.Group()

        self.ui_inventory_title_text = self.ui_inventory_title_text = self.font.render("Inventory", None, 'cornsilk3')
        self.updateInventory()
    def showEquipment(self):
        wep_icon_pos = (1000, 220)
        armor_icon_pos = (1100, 220)
        acc_icon_pos = (1200, 220)
        #reset inventory sprites
        """prevent inventory items to appear in equipment panel"""
        self.ui_weapons = pygame.sprite.Group()
        self.ui_items = pygame.sprite.Group()

        #reset inventory slot idx
        """have items appear in correct order when going back to inventory"""
        self.inventory_idx = 0
        self.ui_inventory_title_text = self.font.render("Equipment", None, 'cornsilk3')

        player_weapon = Icon(wep_icon_pos, color='grey')
        player_armor = Icon(armor_icon_pos, color='grey')
        player_accessory = Icon(acc_icon_pos, color='grey')
        if player.getEquippedItems()['Weapon']:
            player_weapon = Icon(wep_icon_pos, image=pygame.image.load('../View/Graphics/sword.png').convert_alpha())
        if player.getEquippedItems()['Armor']:
            player_armor = Icon(armor_icon_pos, image=pygame.image.load('../View/Graphics/armor.png').convert_alpha())
        if player.getEquippedItems()['Accessory']:
            player_accessory = Icon(acc_icon_pos, image=pygame.image.load('../View/Graphics/helmet.png').convert_alpha())
        self.ui_equipment.add(player_weapon)
        self.ui_equipment.add(player_armor)
        self.ui_equipment.add(player_accessory)
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
            if isinstance(locations[location]['content'], Model.Entities.Enemy.Enemy.Enemy):
                icon = Icon(self.nodes.sprites()[idx].rect.center,
                            image = pygame.image.load('../View/Graphics/goblin.png').convert_alpha(),
                            icon_type = 'enemy')
                icon_sprites.append(icon)
            elif isinstance(locations[location]['content'], Model.Inventory.Item.Item):
                icon = Icon(self.nodes.sprites()[idx].rect.center,
                            image = pygame.image.load('../View/Graphics/chest.png').convert_alpha(),
                            icon_type = 'treasure')
                icon_sprites.append(icon)
            elif isinstance(locations[location]['content'], Model.Entities.NPC.NPC):
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
        self.cur_adjacency_list = locations[self.current_location]['unlock']
        for node in self.cur_adjacency_list:
            node_sprite = Node(locations[node]['node_pos'], 'available', self.speed)
            self.nodes.add(node_sprite)

    def drawPaths(self):
        line_width = 6
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
            self.showInventory()
            location_data['content'] = None

        #collide with npc
        if pygame.sprite.spritecollide(self.player_icon.sprite, self.npc_icons, False):
            location_content = location_data['content']
            player.interact(location_content, self.display_surface)

        #player_icon movement
        if not self.moving:
            if keys[pygame.K_UP] and self.getNextNode('up') in self.cur_adjacency_list:
                self.visited.append(self.current_location)
                self.move_direction = self.getMovementData(self.getNextNode('up'))
            elif keys[pygame.K_DOWN] and self.getNextNode('down') in self.cur_adjacency_list:
                self.visited.append(self.current_location)
                self.move_direction = self.getMovementData(self.getNextNode('down'))
            elif keys[pygame.K_RIGHT] and self.getNextNode('right') in self.cur_adjacency_list:
                self.visited.append(self.current_location)
                self.move_direction = self.getMovementData(self.getNextNode('right'))
            elif(keys[pygame.K_LEFT]) and self.getNextNode('left') in self.cur_adjacency_list:
                self.visited.append(self.current_location)
                self.move_direction = self.getMovementData(self.getNextNode('left'))

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
            self.player_icon.sprite.pos += self.move_direction * self.speed
            idx_of_nodes = self.cur_adjacency_list.index(self.current_location)
            target_node = self.nodes.sprites()[idx_of_nodes]
            if target_node.detection_zone.collidepoint(self.player_icon.sprite.pos):
                self.moving = False
                self.move_direction = pygame.math.Vector2(0,0)
                self.checkForNextStage()

    def run(self):
        self.screen.blit(self.background, (0, 0))
        self.timer()
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
        self.updateHud()
        self.ui_inventory.draw(self.display_surface)
        self.ui_equipment.draw(self.display_surface)
        self.screen.blit(self.ui_inventory_title_surface, (940, 145))
        self.screen.blit(self.ui_inventory_title_text,(940, 145))
        self.ui_items.draw(self.display_surface)
        self.ui_weapons.draw(self.display_surface)
        self.interactWithInventory()
        self.displayWinMessage()