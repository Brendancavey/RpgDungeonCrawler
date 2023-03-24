import pygame
import Model.Items.Potion
import Model.Items.Weapon
import Model.Items.Accessory
import Model.Items.Armor
from pygame import mixer
from Controller.GameData import player, inventory_slots
from Model.Overworld.Overworld import Icon

class InventoryUI():
    font = pygame.font.Font(None, 35)
    largeFont = pygame.font.Font(None, 65)
    smallFont = pygame.font.Font(None, 29)
    smallBold = pygame.font.Font(None, 30)
    smallBold.set_bold
    def __init__(self, screen):
        #setup
        self.screen = screen
        self.mouse_click_time = 0
        self.current_time = 0
        self.inventory_idx = 0

        #call setup
        self.setupInventory()
        self.updateInventory()

    def resetInventorySlots(self):
        for slots in inventory_slots.values():
            slots['content'] = None
    def resetInventory(self):
        self.weapons = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        self.armor = pygame.sprite.Group()
        self.accessories = pygame.sprite.Group()
        self.inv_quantity = pygame.sprite.Group()
        self.inventory_idx = 0
        self.updateInventory()
    def setupInventory(self):
        #inventory & equipment hud
        self.graphic_inventory = pygame.sprite.Group()
        self.graphic_equipment = pygame.sprite.Group()

        #update inventory slots
        """reset values to account for player using items in battle
        update current items via updateInventory()"""
        self.resetInventorySlots()

        #load inventory text
        self.title_surface = pygame.Surface ((150, 25))
        self.title_surface.fill('bisque4')
        self.title_text = self.font.render("Inventory", False, 'cornsilk3')

        #load inventory images
        inventory_layout = Icon((1110,275), image = pygame.image.load('../View/Graphics/inventory.png').convert_alpha())
        inventory_bar = Icon((1085, 422), image = pygame.image.load('../View/Graphics/inventory_bar.png').convert_alpha())
        inventory_icon = Icon((965, 419), image = pygame.image.load('../View/Graphics/backpack.png').convert_alpha())
        equipment_icon = Icon((1025, 419), image = pygame.image.load('../View/Graphics/armor.png').convert_alpha())
        self.graphic_inventory.add(inventory_layout)
        self.graphic_inventory.add(inventory_bar)
        self.graphic_inventory.add(inventory_icon)
        self.graphic_inventory.add(equipment_icon)

    def updateInventory(self):
        """reset values to account for player equipping or using items not in the
        order of inventory slots"""
        self.resetInventorySlots()
        self.inventory_idx = 0

        #inventory items/weapons
        self.items = pygame.sprite.Group()
        self.weapons = pygame.sprite.Group()
        self.armor = pygame.sprite.Group()
        self.accessories = pygame.sprite.Group()
        #quantity
        self.inv_quantity = pygame.sprite.Group()

        #find empty slot
        for inventory in player.getInventory():
            if isinstance(player.getInventory()[inventory], dict):
                for item in player.getInventory()[inventory]:
                    quantity = self.smallBold.render(str(player.getInventory()[inventory][item]), False, 'red')
                    for slot in inventory_slots.values():
                        if slot['content']:
                            if item.getName() == slot['content'].getName():
                                print("Same item")
                                break
                        else:
                            print("received")
                            slot['content'] = item
                            qnty_sprite = Icon((slot['slot_pos'][0] + 25, slot['slot_pos'][1] + 15), image = quantity)
                            self.inv_quantity.add(qnty_sprite)
                            break
        #update slot with graphic
        for idx, slot in enumerate(inventory_slots.values()):
            if idx == self.inventory_idx:
                if isinstance(slot['content'], Model.Items.Potion.Potion):
                    sprite = Icon(slot['slot_pos'], image = pygame.image.load('../View/Graphics/potionRed.png').convert_alpha(), idx= idx)
                    self.items.add(sprite)
                    self.inventory_idx += 1
                elif isinstance(slot['content'], Model.Items.Weapon.Weapon):
                    sprite = Icon(slot['slot_pos'], image = pygame.image.load('../View/Graphics/sword.png').convert_alpha(), idx= idx)
                    self.weapons.add(sprite)
                    self.inventory_idx += 1
                elif isinstance(slot['content'], Model.Items.Armor.Armor):
                    sprite = Icon(slot['slot_pos'], image = pygame.image.load('../View/Graphics/armor.png').convert_alpha(), idx= idx)
                    self.armor.add(sprite)
                    self.inventory_idx += 1
                elif isinstance(slot['content'], Model.Items.Accessory.Accessory):
                    sprite = Icon(slot['slot_pos'], image = pygame.image.load('../View/Graphics/scroll.png').convert_alpha(), idx= idx)
                    self.accessories.add(sprite)
                    self.inventory_idx += 1


    def timer(self):
        delay_time = 175
        if pygame.mouse.get_pressed()[0] == 1 and self.current_time > self.mouse_click_time + delay_time:
            self.mouse_click_time = pygame.time.get_ticks()
            self.clicked = False
        self.current_time = pygame.time.get_ticks()
    def showInventory(self):
        #reset equipment sprites
        self.graphic_equipment = pygame.sprite.Group()

        self.title_text = self.title_text = self.font.render("Inventory", None, 'cornsilk3')
        self.updateInventory()
    def showEquipment(self):
        wep_icon_pos = (1000, 220)
        armor_icon_pos = (1100, 220)
        acc_icon_pos = (1200, 220)
        #reset inventory sprites
        """prevent inventory items to appear in equipment panel"""
        self.weapons = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        self.armor = pygame.sprite.Group()
        self.accessories = pygame.sprite.Group()
        self.inv_quantity = pygame.sprite.Group()

        #reset inventory slot idx
        """have items appear in correct order when going back to inventory"""
        self.inventory_idx = 0
        self.title_text = self.font.render("Equipment", None, 'cornsilk3')

        player_weapon = Icon(wep_icon_pos, color='grey')
        player_armor = Icon(armor_icon_pos, color='grey')
        player_accessory = Icon(acc_icon_pos, color='grey')
        if player.getEquippedItems()['Weapon']:
            player_weapon = Icon(wep_icon_pos, image=pygame.image.load('../View/Graphics/sword.png').convert_alpha())
        if player.getEquippedItems()['Armor']:
            player_armor = Icon(armor_icon_pos, image=pygame.image.load('../View/Graphics/armor.png').convert_alpha())
        if player.getEquippedItems()['Accessory']:
            player_accessory = Icon(acc_icon_pos, image=pygame.image.load('../View/Graphics/scroll.png').convert_alpha())
        self.graphic_equipment.add(player_weapon)
        self.graphic_equipment.add(player_armor)
        self.graphic_equipment.add(player_accessory)

    def run(self):
        pos = pygame.mouse.get_pos()
        ui_text_pos = (900, 470)
        ui_text_pos2 = (1050, 520)
        ui_text_surface_pos = (900, 470)
        ui_text_surface = pygame.Surface((375,75))
        ui_text_surface.fill('bisque4')
        self.screen.blit(ui_text_surface, ui_text_surface_pos)

        # hover over items
        if self.items:
            for sprite in self.items.sprites():
                if sprite.rect.collidepoint(pos):
                    self.screen.blit(ui_text_surface, ui_text_surface_pos)
                    idx = self.items.sprites().index(sprite)
                    if isinstance(inventory_slots[sprite.idx]['content'], Model.Items.Potion.Potion):
                        if player.getHp() >= player.getMaxHp():
                            self.ui_text2 = self.smallFont.render("Player at max hp!", False, 'grey')
                        else:
                            self.ui_text2 = self.smallFont.render("Click to use", False, 'grey')
                        self.ui_text = self.font.render(list(player.getItems())[idx].getDescription(), False, "Green")
                        self.screen.blit(self.ui_text, ui_text_pos)
                        self.screen.blit(self.ui_text2, ui_text_pos2)
                        break
        if self.weapons:
            for sprite in self.weapons.sprites():
                if sprite.rect.collidepoint(pos):
                    self.screen.blit(ui_text_surface, ui_text_surface_pos)
                    idx = self.weapons.sprites().index(sprite)
                    if isinstance(inventory_slots[sprite.idx]['content'], Model.Items.Weapon.Weapon):
                        self.ui_text = self.font.render(list(player.getInventory()['Weapons'])[idx].getDescription(), False, "Green")
                        self.ui_text2 = self.smallFont.render("Click to equip", False, 'grey')
                        self.screen.blit(self.ui_text, ui_text_pos)
                        self.screen.blit(self.ui_text2, ui_text_pos2)
                        break
        if self.armor:
            for sprite in self.armor.sprites():
                if sprite.rect.collidepoint(pos):
                    self.screen.blit(ui_text_surface, ui_text_surface_pos)
                    idx = self.armor.sprites().index(sprite)
                    if isinstance(inventory_slots[sprite.idx]['content'], Model.Items.Armor.Armor):
                        self.ui_text = self.font.render(list(player.getInventory()['Armor'])[idx].getDescription(), False, "Green")
                        self.ui_text2 = self.smallFont.render("Click to equip", False, 'grey')
                        self.screen.blit(self.ui_text, ui_text_pos)
                        self.screen.blit(self.ui_text2, ui_text_pos2)
                        break
        if self.accessories:
            for sprite in self.accessories.sprites():
                if sprite.rect.collidepoint(pos):
                    self.screen.blit(ui_text_surface, ui_text_surface_pos)
                    idx = self.accessories.sprites().index(sprite)
                    if isinstance(inventory_slots[sprite.idx]['content'], Model.Items.Accessory.Accessory):
                        self.ui_text = self.font.render(list(player.getInventory()['Accessories'])[idx].getDescription(), False, "Green")
                        self.ui_text2 = self.smallFont.render("Click to equip", False, 'grey')
                        self.screen.blit(self.ui_text, ui_text_pos)
                        self.screen.blit(self.ui_text2, ui_text_pos2)
                        break
        if self.graphic_inventory:
            if self.graphic_inventory.sprites()[2].rect.collidepoint(pos):
                self.screen.blit(ui_text_surface, ui_text_surface_pos)
                self.ui_text = self.font.render("Inventory", False, "Green")
                self.ui_text2 = self.smallFont.render("Click to view", False, 'grey')
                self.screen.blit(self.ui_text, ui_text_pos)
                self.screen.blit(self.ui_text2, ui_text_pos2)
            elif self.graphic_inventory.sprites()[3].rect.collidepoint(pos):
                self.screen.blit(ui_text_surface, ui_text_surface_pos)
                self.ui_text = self.font.render("Equipment", False, "Green")
                self.ui_text2 = self.smallFont.render("Click to view", False, 'grey')
                self.screen.blit(self.ui_text, ui_text_pos)
                self.screen.blit(self.ui_text2, ui_text_pos2)
        if self.graphic_equipment:
            eqp_weapon_text = "Weapon: None"
            eqp_armor_text = "Armor: None"
            eqp_accessory_text = "Accessory: None"
            if self.graphic_equipment.sprites()[0].rect.collidepoint(pos):
                self.screen.blit(ui_text_surface, ui_text_surface_pos)
                if player.getEquippedItems()['Weapon']:
                    eqp_weapon_text = player.getEquippedItems()['Weapon'].getDescription()
                self.ui_text = self.smallFont.render(eqp_weapon_text,False, "Green")
                self.screen.blit(self.ui_text, ui_text_pos)
            elif self.graphic_equipment.sprites()[1].rect.collidepoint(pos):
                self.screen.blit(ui_text_surface, ui_text_surface_pos)
                if player.getEquippedItems()['Armor']:
                    eqp_armor_text = player.getEquippedItems()['Armor'].getDescription()
                self.ui_text = self.smallFont.render(eqp_armor_text,False, "Green")
                self.screen.blit(self.ui_text, ui_text_pos)
            elif self.graphic_equipment.sprites()[2].rect.collidepoint(pos):
                self.screen.blit(ui_text_surface, ui_text_surface_pos)
                if player.getEquippedItems()['Accessory']:
                    eqp_accessory_text = player.getEquippedItems()['Accessory'].getDescription()
                self.ui_text = self.smallFont.render(eqp_accessory_text,False, "Green")
                self.screen.blit(self.ui_text, ui_text_pos)

        #click on items
        if self.weapons:
            for sprite in self.weapons.sprites():
                if sprite.rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                    if isinstance(inventory_slots[sprite.idx]['content'], Model.Items.Weapon.Weapon):
                        weapon_sound = mixer.Sound('../Controller/Sounds/sword-unsheathe.wav')
                        weapon_sound.play()
                        self.clicked = True
                        player.equip(inventory_slots[sprite.idx]['content'])
                        inventory_slots[sprite.idx]['content'] = None
                        self.weapons.sprites().remove(sprite)
                        self.resetInventory()
                        break
        if self.armor:
            for sprite in self.armor.sprites():
                if sprite.rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                    if isinstance(inventory_slots[sprite.idx]['content'], Model.Items.Armor.Armor):
                        armor_sound = mixer.Sound('../Controller/Sounds/chainmail1.wav')
                        armor_sound.play()
                        self.clicked = True
                        player.equip(inventory_slots[sprite.idx]['content'])
                        inventory_slots[sprite.idx]['content'] = None
                        self.armor.sprites().remove(sprite)
                        self.resetInventory()
                        break
        if self.accessories:
            for sprite in self.accessories.sprites():
                if sprite.rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                    if isinstance(inventory_slots[sprite.idx]['content'], Model.Items.Accessory.Accessory):
                        acc_sound = mixer.Sound('../Controller/Sounds/Inventory_Open_01.wav')
                        acc_sound.play()
                        self.clicked = True
                        player.equip(inventory_slots[sprite.idx]['content'])
                        inventory_slots[sprite.idx]['content'] = None
                        self.accessories.sprites().remove(sprite)
                        self.resetInventory()
                        break
        if self.items:
            for sprite in self.items.sprites():
                if sprite.rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                    if isinstance(inventory_slots[sprite.idx]['content'], Model.Items.Potion.Potion):
                        potion_sound = mixer.Sound('../Controller/Sounds/bubble2.wav')
                        potion_sound.play()
                        self.clicked = True
                        if player.getHp() < player.getMaxHp():
                            player.itemUse(inventory_slots[sprite.idx]['content'])
                            inventory_slots[sprite.idx]['content'] = None
                            self.items.sprites().remove(sprite)
                            self.resetInventory()
                            break
        if pygame.mouse.get_pressed()[0] == 0:
            self.play_sound = False
        if self.graphic_inventory:
            if self.graphic_inventory.sprites()[2].rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] == 1:
                if not self.play_sound:
                    inventory_sound = mixer.Sound('../Controller/Sounds/cloth.wav')
                    inventory_sound.play()
                self.play_sound = True
                self.showInventory()
            elif self.graphic_inventory.sprites()[3].rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] == 1:
                if not self.play_sound:
                    equipment_sound = mixer.Sound('../Controller/Sounds/chainmail2.wav')
                    equipment_sound.play()
                    self.play_sound = True
                self.showEquipment()