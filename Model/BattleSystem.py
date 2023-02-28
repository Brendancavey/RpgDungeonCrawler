from Model.Sprites.Button import Button
import pygame
class BattleSystem():
    pygame.init()
    blue = (50, 153, 213)
    font = pygame.font.Font(None, 50)
    font2 = pygame.font.Font(None, 35)
    def __init__(self, player, enemy, screen_width, screen_height):
        # player
        self.player = player
        self.default_player_ap = 3
        self.player_ap = self.default_player_ap
        self.player_items = list(self.player.getItems())

        # enemy
        self.enemy = enemy
        self.enemy_attack_pattern_map = {"attack": enemy.attack, "guard": enemy.guard}
        self.enemy_attack_idx = 0

        #buttons
        self.button1 = Button(200, 50, screen_width//4, screen_height//1.5, "green", self.player.abilities[0])
        self.button2 = Button(200, 50, screen_width // 1.5, screen_height // 1.5, "green", self.player.abilities[1])
        self.button3 = Button(200, 50, screen_width // 4, screen_height // 2, "green", self.player.abilities[1])
        self.button4 = Button(200, 50, screen_width // 1.5, screen_height // 2, "green", self.player.abilities[1])
        self.buttons = [self.button1, self.button2, self.button3, self.button4]
        self.button_group = pygame.sprite.Group()
        for button in self.buttons:
            self.button_group.add(button)

        # screen and surface
        self.width = screen_width
        self.height = screen_height
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.surface = pygame.Surface((screen_width, screen_height))
        self.surface.fill(self.blue)
            #text info
        self.text_enemyHp = self.font.render(str(self.enemy.getName()) + " HP: " + str(self.enemy.getHp()), False, "black")
        self.text_enemy_intent = self.font.render(
            self.enemy.getAttack(self.enemy_attack_idx) + ": " + str(self.damageToInflict(self.enemy, self.player)),
            False, "red")
        self.text_playerAp = self.font.render("AP: " + str(self.getPlayerAp()), False, "black")
        self.text_playerHp = self.font.render(str(self.player.getName()) + " HP: " + str(self.player.getHp()), False, "black")
        self.text_interface = self.font.render(str(self.damageToInflict(self.player, self.enemy)), False, "green")

    def update(self):
        #update buttons
        self.button_group.update()

        #update screen
            #text info
        self.text_button1 = self.font2.render(self.button1.action_name.getName(), False, "black")
        self.text_button2 = self.font2.render(self.button2.action_name.getName(), False, "black")
        self.text_button3 = self.font2.render(self.button3.action_name.getName(), False, "black")
        self.text_button4 = self.font2.render(self.button4.action_name.getName(), False, "black")
        self.text_enemyHp = self.font.render(str(self.enemy.getName()) + " HP: " + str(self.enemy.getHp()), False, "black")
        if self.enemy_attack_idx < len(self.enemy.getAttackPattern()):
            self.text_enemy_intent = self.font.render(self.enemy.getAttack(self.enemy_attack_idx) + ": " + str(self.damageToInflict(self.enemy, self.player)), False, "red")
        else:
            self.text_enemy_intent = self.font.render(self.enemy.getAttack(0) + ": " + str(self.damageToInflict(self.enemy, self.player)), False, "red")
        self.text_playerAp = self.font.render("AP: " + str(self.getPlayerAp()), False, "black")
        self.text_playerHp = self.font.render(str(self.player.getName()) + " HP: " + str(self.player.getHp()), False,
                                              "black")

        #########text interface testing#######
        if self.button1.isHovered():
            self.text_interface = self.font.render(self.button1.action_name.getDescription(self.damageToInflict(self.player, self.enemy, self.button1.action_name.getElement(), self.button1.action_name.getDamageMod())), False,
                                                       "green")
        elif self.button2.isHovered():
            self.text_interface = self.font.render(self.button2.action_name.getDescription(self.damageToInflict(self.player, self.enemy, self.button2.action_name.getElement(), self.button2.action_name.getDamageMod())), False, "green")
        elif self.button3.isHovered():
            self.text_interface = self.font.render("Buff yourself with " + self.enemy.status_names[1], False, "green")
        #elif self.button4.isHovered():
            #self.text_interface = self.font.render("Use potion from inventory and heal: " + str(self.player._inventory._inventory["Supplies"]["Small Potion"].getRecoveryAmt()), False, "green")
        else:
            self.text_interface = self.font.render(str(self.damageToInflict(self.player, self.enemy)), False,
                                                   self.blue)

        ########################




            #blit to screen
        self.button_group.draw(self.surface)
        self.screen.blit(self.surface, (0, 0))
        self.screen.blit(self.text_enemyHp, (250, 50))
        self.screen.blit(self.text_enemy_intent, (250, 100))
        self.screen.blit(self.text_playerAp, (500, 600))
        self.screen.blit(self.text_playerHp, (200, 600))
        self.screen.blit(self.text_interface, (200, 650))
        self.screen.blit(self.text_button1, (self.width // 4 - 50, self.height // 1.5 - 15))
        self.screen.blit(self.text_button2, (self.width // 1.5 - 50, self.height // 1.5 - 15))
        self.screen.blit(self.text_button3, (self.width // 4 - 50, self.height // 2 - 15))
        self.screen.blit(self.text_button4, (self.width // 1.5 - 50, self.height // 2 - 15))

    def damageToInflict(self, attacker, target, element = None, attack_mod = None):
        if attack_mod:
            damage = attacker.getPower() * attack_mod
        else:
            damage = attacker.getPower()
        #if target.isWeak(element):
            #damage = damage * 2
        for status in target.status:
            damage *= target.status_map[status]
        return damage
    def getPlayerAp(self):
        return self.player_ap
    def playerAttacks(self, ability_mod):
        if self.getPlayerAp() > 0:
            self.player.attack(self.enemy, self.damageToInflict(self.player, self.enemy, ability_mod[0], ability_mod[1]))
            self.player_ap -= 1

    def playerTurnEnd(self):
        self.player_ap = self.default_player_ap
        print("\n")#formatting
        self.enemyAttacks()

    def enemyAttacks(self):
        if self.enemy_attack_idx >= len(self.enemy.getAttackPattern()) :
            self.enemy_attack_idx = 0
        enemy_next_move = self.enemy_attack_pattern_map[self.enemy.getAttack(self.enemy_attack_idx)](self.player, self.damageToInflict(self.enemy, self.player))
        enemy_next_move #perform enemy next move
        self.enemy_attack_idx += 1
        print("\n")#formatting

    def getCurrentAP(self):
        return self.player_ap
    def commenceBattle(self):
        for button in self.button_group:
            #player turn
            if button.isClicked():
                self.performAction(button)
            #enemy turn
            if self.player_ap == 0:
                self.playerTurnEnd()
        if not self.enemy.isAlive():
            print("You win!")

    def performAction(self, button):
        if button.action:
            ability_mod = button.action_name.useAbility(self.enemy)
            if button._id == 0:
                print("perform action 0 : attack")
                self.playerAttacks(ability_mod)
            if button._id == 1:
                #print("perform action 1 : inflict vulnerable")
                #self.enemy.status.add("vulnerable")
                self.playerAttacks(ability_mod)
            if button._id == 2:
                print("perform action 2: buff self critical")
                self.enemy.status.add("critical buff")
            if button._id == 3:
                if self.player_items:
                    print("perform action 3 : recover")
                    print(self.player_items)
                    self.player.itemUse(self.player_items[0])
                    self.player_items = list(self.player.getItems())
                else:
                    print("inventory empty")
            button.action_name.inflictDebuff(self.enemy)


        else:
            return
        button.action = False


