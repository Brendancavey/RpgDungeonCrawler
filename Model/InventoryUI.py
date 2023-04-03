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
    smallFont = pygame.font.Font(None, 25)
    smallBold = pygame.font.Font(None, 30)
    smallBold.set_bold
    def __init__(self, screen):
        #setup
        self.screen = screen
        self.mouse_click_time = 0
        self.current_time = 0
        self.inventory_idx = 0

        #sounds
        self.weapon_sound = mixer.Sound('../Controller/Sounds/sword-unsheathe.wav')
        self.armor_sound = mixer.Sound('../Controller/Sounds/chainmail1.wav')
        self.acc_sound = mixer.Sound('../Controller/Sounds/Inventory_Open_01.wav')

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
        self.graphic_abilities = pygame.sprite.Group()
        self.graphic_ability_icons = pygame.sprite.Group()
        self.graphic_ability_checkmarks = pygame.sprite.Group()
        self.graphic_coin = pygame.sprite.GroupSingle()
        self.ability_qnty = pygame.sprite.GroupSingle()

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
        ability_icon = Icon((1086, 419), image = pygame.image.load('../View/Graphics/tome.png').convert_alpha())
        coin_icon = Icon((1175, 419), image = pygame.image.load('../View/Graphics/coin.png').convert_alpha())
        self.graphic_inventory.add(inventory_layout)
        self.graphic_inventory.add(inventory_bar)
        self.graphic_inventory.add(inventory_icon)
        self.graphic_inventory.add(equipment_icon)
        self.graphic_inventory.add(ability_icon)
        self.graphic_coin.add(coin_icon)

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
                            #print("received")
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
        self.graphic_ability_icons = pygame.sprite.Group()
        self.graphic_ability_checkmarks = pygame.sprite.Group()
        self.ability_qnty = pygame.sprite.GroupSingle()


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
        self.graphic_ability_icons = pygame.sprite.Group()
        self.graphic_ability_checkmarks = pygame.sprite.Group()
        self.ability_qnty = pygame.sprite.GroupSingle()

        #reset graphic equipment
        self.graphic_equipment = pygame.sprite.Group()

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

    def showAbilities(self):
        """prevent inventory/equipment items to appear in abilities panel"""
        self.weapons = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        self.armor = pygame.sprite.Group()
        self.accessories = pygame.sprite.Group()
        self.inv_quantity = pygame.sprite.Group()
        self.graphic_equipment = pygame.sprite.Group()
        self.graphic_ability_icons = pygame.sprite.Group()
        self.graphic_ability_checkmarks = pygame.sprite.Group()
        self.ability_qnty = pygame.sprite.GroupSingle()

        # reset inventory slot idx
        """have items appear in correct order when going back to inventory"""
        self.inventory_idx = 0
        self.title_text = self.font.render("Abilities", None, 'cornsilk3')
        self.ability_qnty_text = Icon((1225, 350), image = self.font.render(str(len(player.ability_loadout)) + "/4", False, "black"))
        self.ability_qnty.add(self.ability_qnty_text)

        height_gap = 215
        for ability in player.all_abilities:
            ability_icon = Icon((1005,height_gap), image = self.smallFont.render(ability.getName(), False, 'black'))
            self.graphic_ability_icons.add(ability_icon)
            if ability in player.ability_loadout:
                checkmark = Icon((ability_icon.rect.right + 10, height_gap - 4), image = pygame.image.load("../View/Graphics/Check13.png"))
                self.graphic_ability_checkmarks.add(checkmark)
            height_gap += 25

    def run(self):
        pos = pygame.mouse.get_pos()
        ui_text_pos = (900, 495)
        ui_text_pos1 = (900, 470)
        ui_text_pos2 = (1050, 520)
        ui_text_surface_pos = (900, 470)
        ui_text_surface = pygame.Surface((375,75))
        ui_text_surface.fill('bisque4')
        self.screen.blit(ui_text_surface, ui_text_surface_pos)

        #player gold
        gold_amt = self.smallFont.render(str(player.getGoldValue()), True, 'black')
        self.graphic_coin.draw(self.screen)
        self.screen.blit(gold_amt, (self.graphic_coin.sprite.rect.x + 60, self.graphic_coin.sprite.rect.y + 23))

        #hover over icons
        #inventory
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
                        self.ui_text = self.smallFont.render(list(player.getInventory()['Weapons'])[idx].getDescription(), False, "Green")
                        self.ui_text2 = self.smallFont.render("Click to equip", False, 'grey')
                        self.ui_text1 = self.font.render(list(player.getInventory()['Weapons'])[idx].getName(), False, "green")
                        self.screen.blit(self.ui_text1, ui_text_pos1)
                        self.screen.blit(self.ui_text, ui_text_pos)
                        self.screen.blit(self.ui_text2, ui_text_pos2)
                        break
        if self.armor:
            for sprite in self.armor.sprites():
                if sprite.rect.collidepoint(pos):
                    self.screen.blit(ui_text_surface, ui_text_surface_pos)
                    idx = self.armor.sprites().index(sprite)
                    if isinstance(inventory_slots[sprite.idx]['content'], Model.Items.Armor.Armor):
                        self.ui_text = self.smallFont.render(list(player.getInventory()['Armor'])[idx].getDescription(), False, "Green")
                        self.ui_text2 = self.smallFont.render("Click to equip", False, 'grey')
                        self.ui_text1 = self.font.render(list(player.getInventory()['Armor'])[idx].getName(), False,
                                                         "green")
                        self.screen.blit(self.ui_text1, ui_text_pos1)
                        self.screen.blit(self.ui_text, ui_text_pos)
                        self.screen.blit(self.ui_text2, ui_text_pos2)
                        break
        if self.accessories:
            for sprite in self.accessories.sprites():
                if sprite.rect.collidepoint(pos):
                    self.screen.blit(ui_text_surface, ui_text_surface_pos)
                    idx = self.accessories.sprites().index(sprite)
                    if isinstance(inventory_slots[sprite.idx]['content'], Model.Items.Accessory.Accessory):
                        self.ui_text = self.smallFont.render(list(player.getInventory()['Accessories'])[idx].getDescription(), False, "Green")
                        self.ui_text2 = self.smallFont.render("Click to equip", False, 'grey')
                        self.ui_text1 = self.font.render(list(player.getInventory()['Accessories'])[idx].getName(), False,
                                                         "green")
                        self.screen.blit(self.ui_text1, ui_text_pos1)
                        self.screen.blit(self.ui_text, ui_text_pos)
                        self.screen.blit(self.ui_text2, ui_text_pos2)
                        break
        #coin
        if self.graphic_coin:
            if self.graphic_coin.sprite.rect.collidepoint(pos):
                self.ui_text = self.font.render("Gold: " + str(player.getGoldValue()), False, "Green")
                self.ui_text2 = self.smallFont.render("Used to purchase items and abilities.", False, 'grey')
                self.screen.blit(self.ui_text, ui_text_pos1)
                self.screen.blit(self.ui_text2, (ui_text_pos2[0] - 150, ui_text_pos2[1]))
        #ui icons
        if self.graphic_inventory:
            if self.graphic_inventory.sprites()[2].rect.collidepoint(pos):
                self.screen.blit(ui_text_surface, ui_text_surface_pos)
                self.ui_text = self.font.render("Inventory", False, "Green")
                self.ui_text2 = self.smallFont.render("Click to view", False, 'grey')
                self.screen.blit(self.ui_text, ui_text_pos1)
                self.screen.blit(self.ui_text2, ui_text_pos2)
            elif self.graphic_inventory.sprites()[3].rect.collidepoint(pos):
                self.screen.blit(ui_text_surface, ui_text_surface_pos)
                self.ui_text = self.font.render("Equipment", False, "Green")
                self.ui_text2 = self.smallFont.render("Click to view", False, 'grey')
                self.screen.blit(self.ui_text, ui_text_pos1)
                self.screen.blit(self.ui_text2, ui_text_pos2)
            elif self.graphic_inventory.sprites()[4].rect.collidepoint(pos):
                self.screen.blit(ui_text_surface, ui_text_surface_pos)
                self.ui_text = self.font.render("Abilities", False, "Green")
                self.ui_text2 = self.smallFont.render("Click to view", False, 'grey')
                self.screen.blit(self.ui_text, ui_text_pos1)
                self.screen.blit(self.ui_text2, ui_text_pos2)
        #equipment
        if self.graphic_equipment:
            eqp_weapon_text = "Weapon: None"
            eqp_weapon_name = ""
            eqp_armor_text = "Armor: None"
            eqp_armor_name = ""
            eqp_accessory_text = "Accessory: None"
            eqp_accessory_name = ""
            if self.graphic_equipment.sprites()[0].rect.collidepoint(pos):
                self.screen.blit(ui_text_surface, ui_text_surface_pos)
                if player.getEquippedItems()['Weapon']:
                    eqp_weapon_text = player.getEquippedItems()['Weapon'].getDescription()
                    eqp_weapon_name = player.getEquippedItems()['Weapon'].getName()
                    self.ui_text2 = self.smallFont.render("Click to unequip", False, 'grey')
                    self.screen.blit(self.ui_text2, ui_text_pos2)
                self.ui_text = self.smallFont.render(eqp_weapon_text,False, "Green")
                self.ui_text1 = self.font.render(eqp_weapon_name, False,
                                                 "green")
                self.screen.blit(self.ui_text1, ui_text_pos1)
                self.screen.blit(self.ui_text, ui_text_pos)
            elif self.graphic_equipment.sprites()[1].rect.collidepoint(pos):
                self.screen.blit(ui_text_surface, ui_text_surface_pos)
                if player.getEquippedItems()['Armor']:
                    eqp_armor_text = player.getEquippedItems()['Armor'].getDescription()
                    eqp_armor_name = player.getEquippedItems()['Armor'].getName()
                    self.ui_text2 = self.smallFont.render("Click to unequip", False, 'grey')
                    self.screen.blit(self.ui_text2, ui_text_pos2)
                self.ui_text = self.smallFont.render(eqp_armor_text,False, "Green")
                self.ui_text1 = self.font.render(eqp_armor_name, False,
                                                 "green")
                self.screen.blit(self.ui_text1, ui_text_pos1)
                self.screen.blit(self.ui_text, ui_text_pos)
            elif self.graphic_equipment.sprites()[2].rect.collidepoint(pos):
                self.screen.blit(ui_text_surface, ui_text_surface_pos)
                if player.getEquippedItems()['Accessory']:
                    eqp_accessory_text = player.getEquippedItems()['Accessory'].getDescription()
                    eqp_accessory_name = player.getEquippedItems()['Accessory'].getName()
                    self.ui_text2 = self.smallFont.render("Click to unequip", False, 'grey')
                    self.screen.blit(self.ui_text2, ui_text_pos2)
                self.ui_text1 = self.font.render(eqp_accessory_name, False,
                                                 "green")
                self.ui_text = self.smallFont.render(eqp_accessory_text,False, "Green")
                self.screen.blit(self.ui_text1, ui_text_pos1)
                self.screen.blit(self.ui_text, ui_text_pos)
        #abilities
        if self.graphic_ability_icons:
            for idx, sprite in enumerate(self.graphic_ability_icons.sprites()):
                if sprite.rect.collidepoint(pos):
                    self.screen.blit(ui_text_surface, ui_text_surface_pos)
                    ui_text_0 = self.font.render(str(player.all_abilities[idx].cost) + " AP", False, 'grey')
                    if player.all_abilities[idx].debuff:
                        self.ui_text = self.smallFont.render(player.all_abilities[idx].getDebuffDescription(), False,
                                                              'green')
                    elif player.all_abilities[idx].special_message:
                        self.ui_text = self.smallFont.render(player.all_abilities[idx].getSpecialDescription(), False,
                                                             "Green")
                    self.screen.blit(self.ui_text, (ui_text_pos[0], ui_text_pos[1] + 22))
                    self.ui_text = self.smallFont.render("", False, "Green")
                    self.ui_text1 = self.smallFont.render(player.all_abilities[idx].getPowerDescription(player.getPower()), False,
                                                     "green")
                    self.screen.blit(ui_text_0, ui_text_pos1)
                    self.screen.blit(self.ui_text1, (ui_text_pos1[0], ui_text_pos1[1] + 25))
                    #self.screen.blit(self.ui_text2, (ui_text_pos2[0] - 150, ui_text_pos2[1] + 22))
                    break

        #click on icons
        #abilities
        if self.graphic_ability_icons:
            for idx, sprite in enumerate(self.graphic_ability_icons.sprites()):
                if sprite.rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                    self.clicked = True
                    if player.all_abilities[idx] in player.ability_loadout:
                        if len(player.ability_loadout) > 1:
                            ability_sound = mixer.Sound('../Controller/Sounds/Inventory_Open_00.wav')
                            ability_sound.play()
                            player.removeAbility((player.all_abilities[idx]))
                            self.showAbilities()
                            break
                        else:
                            ability_sound = mixer.Sound('../Controller/Sounds/interface6.wav')
                            ability_sound.play()
                            break
                    elif len(player.ability_loadout) >= 4:
                        ability_sound = mixer.Sound('../Controller/Sounds/interface6.wav')
                        ability_sound.play()
                        break
                    elif player.all_abilities[idx] not in player.ability_loadout:
                        ability_sound = mixer.Sound('../Controller/Sounds/Menu_Select_00.wav')
                        ability_sound.play()
                        player.addAbility(player.all_abilities[idx])
                        self.showAbilities()
                        break

        #inventory
        if self.weapons:
            for sprite in self.weapons.sprites():
                if sprite.rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                    if isinstance(inventory_slots[sprite.idx]['content'], Model.Items.Weapon.Weapon):
                        self.weapon_sound.play()
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
                        self.armor_sound.play()
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
                        self.acc_sound.play()
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
                        self.clicked = True
                        if player.getHp() < player.getMaxHp():
                            potion_sound = mixer.Sound('../Controller/Sounds/bubble2.wav')
                            potion_sound.play()
                            player.itemUse(inventory_slots[sprite.idx]['content'])
                            inventory_slots[sprite.idx]['content'] = None
                            self.items.sprites().remove(sprite)
                            self.resetInventory()
                            break
                        else:
                            potion_sound = mixer.Sound('../Controller/Sounds/interface6.wav')
                            potion_sound.play()
        #equipment
        if self.graphic_equipment:
            if player.getEquippedItems()['Weapon'] and self.graphic_equipment.sprites()[0].rect.collidepoint(pos) \
                    and pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.weapon_sound.play()
                self.clicked = True
                equipped_item = player.getEquippedItems()['Weapon']
                player.unequip(equipped_item)
                self.showEquipment()

            elif player.getEquippedItems()['Armor'] and self.graphic_equipment.sprites()[1].rect.collidepoint(pos) and \
                    pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.armor_sound.play()
                self.clicked = True
                equipped_item = player.getEquippedItems()['Armor']
                player.unequip(equipped_item)
                self.showEquipment()

            elif player.getEquippedItems()['Accessory'] and self.graphic_equipment.sprites()[2].rect.collidepoint(pos) \
                    and pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.acc_sound.play()
                self.clicked = True
                equipped_item = player.getEquippedItems()['Accessory']
                player.unequip(equipped_item)
                self.showEquipment()

        #ui icons
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
            elif self.graphic_inventory.sprites()[4].rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] == 1:
                if not self.play_sound:
                    abilities_sound = mixer.Sound('../Controller/Sounds/cloth-heavy.wav')
                    abilities_sound.play()
                    self.play_sound = True
                self.showAbilities()
        if self.graphic_coin:
            if self.graphic_coin.sprite.rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] == 1:
                if not self.play_sound:
                    coin_sound = mixer.Sound('../Controller/Sounds/Pickup_Gold_00.wav')
                    coin_sound.play()
                    self.play_sound = True
