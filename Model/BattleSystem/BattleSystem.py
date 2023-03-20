from Model.Sprites.Button import Button
import pygame
class BattleSystem():
    pygame.init()
    blue = (50, 153, 213)
    bigFont = pygame.font.Font(None, 50)
    mediumFont = pygame.font.Font(None, 35)
    smallFont = pygame.font.Font(None, 23)
    text_color = 'white'
    def __init__(self, player, enemy, screen_width, screen_height):
        # player
        self.player = player
        self.default_player_ap = 3
        self.player_ap = self.default_player_ap
        self.player_items_list = list(self.player.getItems())
        self.player_items_map = self.player.getItems()
        self.player.resetDebuffs()
        self.player_image = pygame.image.load('../View/Graphics/player.png').convert_alpha()
        self.player_hp_bar_surface = pygame.Surface((100, 20))

        # enemy
        self.enemy = enemy
        self.enemy_attack_idx = 0
        self.enemy_image = enemy.getImage().convert_alpha()
        self.enemy_hp_bar_surface = pygame.Surface((100, 20))

        #buttons
        self.button1 = Button(200, 50, 200, 600, "green", self.player.abilities[0], 0)
        self.button2 = Button(200, 50, 500, 600, "green", self.player.abilities[1], 1)
        self.button3 = Button(200, 50, 800, 600, "green", self.player.abilities[2], 2)
        self.button4 = Button(200, 50, 1100, 600, "green", self.player.abilities[3], 3)
        self.button5 = Button(200, 50, 1150, 75, "green", self.player.abilities[3], 4)
        self.buttons = [self.button1, self.button2, self.button3, self.button4, self.button5]
        self.button_group = pygame.sprite.Group()
        for button in self.buttons:
            self.button_group.add(button)

        # screen and surface
        self.width = screen_width
        self.height = screen_height
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.background = pygame.image.load('../View/Graphics/dungeon.png').convert_alpha()
        self.ui_surface = pygame.Surface((1280, 300))
        self.ui_surface.fill('grey')
            #text info
        self.text_enemyHp = self.smallFont.render(str(self.enemy.getName()) + " HP: " + str(self.enemy.getHp()), False, self.text_color)
        self.text_enemy_intent = self.bigFont.render(
            str(self.enemy.getAttack(self.enemy_attack_idx)) + ": " + str(self.damageToInflict(self.enemy, self.player)),
            False, "red")
        self.text_playerAp = self.bigFont.render("AP: " + str(self.getPlayerAp()), False, "black")
        self.text_playerHp = self.smallFont.render(str(self.player.getName()) + " HP: " + str(self.player.getHp()), False, self.text_color)
        self.text_interface = self.bigFont.render(str(self.damageToInflict(self.player, self.enemy)), False, "green")

    def update(self):
        #update enemy info
        if self.enemy_attack_idx >= len(self.enemy.getAttackPattern()) :
            self.enemy_attack_idx = 0
        self.enemy_next_move = self.enemy.getAttack(self.enemy_attack_idx)
        enemy_mods = self.enemy_next_move.getModifiers()
        enemy_damage = self.damageToInflict(self.enemy, self.player, enemy_mods[0], enemy_mods[1])
        self.enemy_hp_bar = pygame.Surface((100 * self.enemy.getHp()/self.enemy.getMaxHp(), 20))
        self.enemy_hp_bar.fill('red')

        #update player info
        self.player_items_list = list(self.player.getItems())
        self.player_items_map = self.player.getItems()
        self.player_items_text = ", ".join((item.getName() + ": " + str(self.player_items_map[item]) for item in self.player_items_map))
        self.player_hp_bar = pygame.Surface((100 * self.player.getHp()/self.player.getMaxHp(), 20))
        self.player_hp_bar.fill('red')

        #update buttons
        self.button_group.update()

        #update screen
            #text info
        self.text_button1 = self.mediumFont.render(self.button1.action_name.getName(), False, "black")
        self.text_button2 = self.mediumFont.render(self.button2.action_name.getName(), False, "black")
        self.text_button3 = self.mediumFont.render(self.button3.action_name.getName(), False, "black")
        self.text_button4 = self.mediumFont.render(self.button4.action_name.getName(), False, "black")
        self.text_button5 = self.mediumFont.render("Items", False, "black")
        self.text_enemyHp = self.smallFont.render("HP: " + str(self.enemy.getHp()) + "/" + str(self.enemy.getMaxHp()), False, self.text_color)
        self.text_enemy_intent = self.mediumFont.render(str(self.enemy_next_move) + (": " + str(enemy_damage) if enemy_damage > 0 else ""), False, "red")
        self.text_playerAp = self.bigFont.render("AP: " + str(self.getPlayerAp()), False, self.text_color)
        self.text_playerHp = self.smallFont.render("HP: " + str(self.player.getHp()) + "/" + str(self.player.getMaxHp()), False,
                                                 self.text_color)

            #text interface
        if self.button1.isHovered():
            self.text_interface = self.bigFont.render(self.button1.action_name.getDescription(self.damageToInflict(self.player, self.enemy, self.button1.action_name.getElement(), self.button1.action_name.getDamageMod())), False,
                                                       "green")
        elif self.button2.isHovered():
            self.text_interface = self.bigFont.render(self.button2.action_name.getDescription(self.damageToInflict(self.player, self.enemy, self.button2.action_name.getElement(), self.button2.action_name.getDamageMod())), False, "green")
        elif self.button3.isHovered():
            self.text_interface = self.bigFont.render(self.button3.action_name.getDescription(self.damageToInflict(self.player, self.enemy, self.button3.action_name.getElement(), self.button3.action_name.getDamageMod())), False, "green")
        elif self.button4.isHovered():
            self.text_interface = self.bigFont.render(self.button4.action_name.getDescription(self.damageToInflict(self.player, self.enemy, self.button4.action_name.getElement(), self.button4.action_name.getDamageMod())), False, "green")
        elif self.button5.isHovered():
            self.text_interface = self.bigFont.render((self.player_items_text) if self.player_items_list else "Inventory is empty", False, "green")
        else:
            self.text_interface = self.bigFont.render("", False, 'green')

            #blit to screen
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.player_image, (self.width/4, self.height/2))
        self.screen.blit(self.enemy_image, (self.width/4 + 300, self.height/2))
        #self.screen.blit(self.ui_surface,(0,550))
        self.button_group.draw(self.background)
        self.screen.blit(self.enemy_hp_bar_surface, (self.width/4 + 300, self.height/2 + 50))
        self.screen.blit(self.enemy_hp_bar, (self.width/4 + 300, self.height/2 + 50))
        self.screen.blit(self.text_enemyHp, (self.width/4 + 300, self.height/2 + 55))
        self.screen.blit(self.text_enemy_intent, (self.width/4 + 300, self.height/2 - 50))
        self.screen.blit(self.text_playerAp, (1150, 650))
        self.screen.blit(self.player_hp_bar_surface, (self.width/4, self.height/2 + 50))
        self.screen.blit(self.player_hp_bar, (self.width/4, self.height/2 + 50))
        self.screen.blit(self.text_playerHp, (self.width/4, self.height/2 + 55))
        self.screen.blit(self.text_interface, (100, 650))
        self.screen.blit(self.text_button1, (120, 585))
        self.screen.blit(self.text_button2, (420, 585))
        self.screen.blit(self.text_button3, (720, 585))
        self.screen.blit(self.text_button4, (1020, 585))
        self.screen.blit(self.text_button5, (1120, 65))

    def damageToInflict(self, attacker, target, element = None, attack_mod = None):
        if attack_mod:
            damage = attacker.getPower() * attack_mod
        elif attack_mod == 0:
            damage = 0
        else:
            damage = attacker.getPower()
        #if target.isWeak(element):
            #damage = damage * 2
        for mod in target.take_more_damage:
            damage *= mod[1]
        for mod in attacker.weaken_attackPwr:
            damage -= round(damage * mod[1])
        return int(round(damage))
    def getPlayerAp(self):
        return self.player_ap
    def playerAttacks(self, ability):
        if self.getPlayerAp() > 0:
            self.player.attack(self.enemy, ability, self.damageToInflict(self.player, self.enemy, ability.getElement(), ability.getDamageMod()))
            if ability.hasDebuff():
                ability.inflictDebuff(self.enemy)
            self.player_ap -= 1

    def playerTurnEnd(self):
        #decrement player debuffs
        for dot in self.player.dot_damage:
            print(self.player.getName() + " suffers " + str(dot[1]) + " damage from " + str(dot[0]))
            self.player.takeDamage(dot[1])
        for debuff in self.player.status.copy():
            debuff.counterDecrement()
            debuff.checkForEffectRemoval(self.player)
        #commence enemy turn
        print("\n")#formatting
        self.enemyTurn()
        # reset player ap
        self.player_ap = self.default_player_ap

    def enemyTurn(self):
        #enemyAttacks
        if self.enemy_attack_idx >= len(self.enemy.getAttackPattern()) :
            self.enemy_attack_idx = 0

        enemy_next_move = self.enemy.getAttack(self.enemy_attack_idx)
        enemy_attack_mods = self.enemy.getAttack(self.enemy_attack_idx).getModifiers()#(self.player, self.damageToInflict(self.enemy, self.player))

        self.enemy.attack(self.player, enemy_next_move, self.damageToInflict(self.enemy, self.player, enemy_attack_mods[0], enemy_attack_mods[1]))
        enemy_next_move.inflictDebuff(self.player)

        #enemy turn end
        self.enemy_attack_idx += 1
        for dot in self.enemy.dot_damage:
            print(self.enemy.getName() + " suffers " + str(dot[1]) + " damage from " + str(dot[0]))
            self.enemy.takeDamage(dot[1])
        for debuff in self.enemy.status.copy():
            debuff.counterDecrement()
            debuff.checkForEffectRemoval(self.enemy)
        print("\n")#formatting

    def getCurrentAP(self):
        return self.player_ap
    def commenceBattle(self):
        for button in self.button_group:
            #player turn
            if button.isClicked():
                self.performAction(button)
                print(self.enemy.status)
                print(self.enemy.take_more_damage)
                print(self.enemy.weaken_attackPwr)
                print(self.enemy.dot_damage)
            #enemy turn
            if self.player_ap == 0:
                self.playerTurnEnd()
    def start(self):
        self.commenceBattle()
        self.update()
    def performAction(self, button):
        if button.action:
            # use potion action
            if button._id == 4:
                if self.player_items_list:
                    if self.player.isFullHp():
                        print(self.player.getName() + " is already at full HP!")
                    else:
                        print(self.player_items_list)
                        self.player.itemUse(self.player_items_list[0])
                        self.player_items_list = list(self.player.getItems())
                else:
                    print("inventory empty")
            else:
                ability = button.action_name
                self.playerAttacks(ability)
        else:
            return
        button.action = False


