from Model.Sprites.Button import Button
from Model.Overworld.Overworld import Icon
from Model.BattleSystem.Debuff.DebuffList import debuff_list
from pygame import mixer
import Model.Entities.Enemy.Enemy
import pygame
class BattleSystem():
    pygame.init()
    blue = (50, 153, 213)
    bigFont = pygame.font.Font(None, 50)
    mediumFont = pygame.font.Font(None, 35)
    smallFont = pygame.font.Font(None, 23)
    small_font_bold = pygame.font.Font(None, 25)
    small_font_bold.set_bold(True)
    text_color = 'white'
    def __init__(self, player, enemy, screen_width, screen_height):
        #time
        self.player_end_turn_time = pygame.time.get_ticks()
        self.current_time = pygame.time.get_ticks()

        #screen and surface
        self.width = screen_width
        self.height = screen_height
        self.screen = pygame.display.set_mode((screen_width, screen_height))

        #player
        self.player = player
        self.default_player_ap = self.player.max_ap
        self.player_ap = self.default_player_ap
        self.player.resetDebuffs()
        self.player_image = pygame.image.load('../View/Graphics/player.png').convert_alpha()
        self.player_icon = Icon((self.width/4 + 25, self.height/2 + 20), image = pygame.image.load('../View/Graphics/player.png').convert_alpha())
        self.player_sprite = pygame.sprite.GroupSingle()
        self.player_sprite.add(self.player_icon)
        self.player_hp_bar_surface = pygame.Surface((100, 20))
        self.player_status_icon = pygame.sprite.Group()
        self.player_end_turn = False

        #animation
        self.playing_player_animation = False
        self.play_player_animation = pygame.math.Vector2(0, 0)
        self.playing_enemy_animation = False
        self.play_enemy_animation = pygame.math.Vector2(0,0)

        #enemy
        self.enemy = enemy
        self.enemy_attack_idx = 0
        self.enemy_image = enemy.getImage().convert_alpha()
        self.enemy_hp_bar_surface = pygame.Surface((100, 20))
        self.enemy_status_icon = pygame.sprite.Group()
        self.enemy_turn = False
        self.enemy_icon = Icon((self.width/4 + 320, self.height/2 + 25), image = self.enemy_image)
        self.enemy_sprite = pygame.sprite.GroupSingle()
        self.enemy_sprite.add(self.enemy_icon)

        #buttons
        self.cur_button_gap = 200
        self.text_button_gap = 200
        self.buttons = []
        self.text_buttons = []
        self.ability_costs = []
        self.display_text_interface = False
        self.button_group = pygame.sprite.Group()
        for idx in range(len(self.player.abilities)):
            self.button = Button(200, 50, self.cur_button_gap, 600, 'green', self.player.abilities[idx], idx)
            self.ability_cost = self.small_font_bold.render(str(self.player.abilities[idx].cost), False, 'purple')
            self.ability_costs.append(self.ability_cost)
            self.cur_button_gap += 300
            self.buttons.append(self.button)
        for button in self.buttons:
            self.button_group.add(button)

        #text info
        self.text_enemyHp = self.smallFont.render(str(self.enemy.getName()) + " HP: " + str(self.enemy.getHp()), False, self.text_color)
        self.text_enemy_intent = self.bigFont.render(
            str(self.enemy.getAttack(self.enemy_attack_idx)) + ": " + str(self.damageToInflict(self.enemy, self.player)),
            False, "red")
        self.text_playerAp = self.bigFont.render("AP: " + str(self.getPlayerAp()), False, "black")
        self.text_playerHp = self.smallFont.render(str(self.player.getName()) + " HP: " + str(self.player.getHp()), False, self.text_color)
        self.text_interface = self.bigFont.render("", False, "green")
        self.text_interface2 = self.mediumFont.render("", False, 'grey')

    def update(self):
        self.timer()
        #update enemy info
        if self.enemy.isAlive():
            if self.enemy_attack_idx >= len(self.enemy.getAttackPattern()) :
                self.enemy_attack_idx = 0
            self.enemy_next_move = self.enemy.getAttack(self.enemy_attack_idx)
            self.enemy_mods = self.enemy_next_move.getModifiers()
            self.enemy_damage = self.damageToInflict(self.enemy, self.player, self.enemy_mods[0], self.enemy_mods[1])
            self.enemy_hp_bar = pygame.Surface((int(100 * self.enemy.getHp()//self.enemy.getMaxHp()), 20))
            self.enemy_hp_bar.fill('red')
            self.enemy_sprite.draw(self.screen)
            self.enemy_status_icon.draw(self.screen)
            self.screen.blit(self.enemy_hp_bar_surface, (self.width / 4 + 300, self.height / 2 + 50))
            self.screen.blit(self.enemy_hp_bar, (self.width / 4 + 300, self.height / 2 + 50))
            self.screen.blit(self.text_enemyHp, (self.width / 4 + 300, self.height / 2 + 55))
            self.screen.blit(self.text_enemy_intent, (self.width / 4 + 300, self.height / 2 - 50))
            self.animateEnemy()
            self.enemy_sprite.update()
        else:
            self.enemy_sprite = pygame.sprite.GroupSingle()

        #update player info
        if self.player.isAlive():
            self.player_hp_bar = pygame.Surface((int(100 * self.player.getHp()//self.player.getMaxHp()), 20))
            self.player_hp_bar.fill('red')
            self.animatePlayer()
            self.player_sprite.update()

        #update buttons
        self.button_group.update()

        #update text info
        for button in self.button_group:
            self.text_button = self.mediumFont.render(button.action_name.getName(), False, "black")
            self.text_buttons.append(self.text_button)
        self.text_enemyHp = self.smallFont.render("HP: " + str(self.enemy.getHp()) + "/" + str(self.enemy.getMaxHp()), False, self.text_color)
        self.text_enemy_intent = self.mediumFont.render(str(self.enemy_next_move) + (": " + str(self.enemy_damage) if self.enemy_damage > 0 else ""), False, "red")
        self.text_playerAp = self.bigFont.render("AP: " + str(self.getPlayerAp()), False, self.text_color)
        self.text_playerHp = self.smallFont.render("HP: " + str(self.player.getHp()) + "/" + str(self.player.getMaxHp()), False,
                                                 self.text_color)
        #text interface
        for button in self.button_group:
            if button.isHovered():
                self.text_interface = self.bigFont.render(button.action_name.getDescription(
                    self.damageToInflict(self.player, self.enemy, button.action_name.getElement(),
                                         button.action_name.getDamageMod())), False,
                                                          "green")
                if button.action_name.cost > self.player_ap:
                    self.text_interface2 = self.mediumFont.render(
                        "Cost: " + str(button.action_name.cost) + "AP. Not enough AP.", False, 'grey')
                elif button.action_name.cost <= self.player_ap:
                    self.text_interface2 = self.mediumFont.render("Cost: " + str(button.action_name.cost) + "AP", False,
                                                                  'grey')
            self.screen.blit(self.text_interface, (100, 650))
            self.screen.blit(self.text_interface2, (100, 685))
        self.text_interface = self.bigFont.render("", False, 'green')
        self.text_interface2 = self.mediumFont.render("", False, 'grey')

        #blit to screen
        self.hoverStatusIcon()
        self.player_sprite.draw(self.screen)
        self.button_group.draw(self.screen)
        self.player_status_icon.draw(self.screen)
        self.screen.blit(self.text_playerAp, (1150, 650))
        self.screen.blit(self.player_hp_bar_surface, (self.width/4, self.height/2 + 50))
        self.screen.blit(self.player_hp_bar, (self.width/4, self.height/2 + 50))
        self.screen.blit(self.text_playerHp, (self.width/4, self.height/2 + 55))
        #display text for buttons
        for idx, text in enumerate(self.text_buttons):
            if len(self.button_group.sprites()) > idx:
                pos_x = self.button_group.sprites()[idx].pos_x
                self.screen.blit(text, (pos_x - 80, 585))
                pos_x_cost = pos_x + 85
                self.screen.blit(self.ability_costs[idx], (pos_x_cost, 580))

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

    def checkForStatusIcon(self, entity):
        if isinstance(entity, Model.Entities.Enemy.Enemy.Enemy):
            self.enemy_status_icon = pygame.sprite.Group()
            distance = 300
        else:
            self.player_status_icon = pygame.sprite.Group()
            distance = 0
        if entity.status:
            self.cur_width_gap = 5
            for status in entity.status:
                if status == debuff_list[0]:
                    image = pygame.image.load('../View/Graphics/debuff_vulnerable.png').convert_alpha()
                elif status == debuff_list[1]:
                    image = pygame.image.load('../View/Graphics/debuff_weaken.png').convert_alpha()
                elif status == debuff_list[2]:
                    image = pygame.image.load('../View/Graphics/debuff_bleed.png').convert_alpha()
                elif status == debuff_list[3]:
                    image = pygame.image.load('../View/Graphics/debuff_poison.png').convert_alpha()
                icon = Icon((self.width/4 + distance + self.cur_width_gap, self.height/2 + 85), image = image)
                self.cur_width_gap += 25
                if isinstance(entity, Model.Entities.Enemy.Enemy.Enemy):
                    self.enemy_status_icon.add(icon)
                else:
                    self.player_status_icon.add(icon)
    def hoverStatusIcon(self):
        def showStatus(entity):
            status_description = list(entity.status)[idx].getDescription()
            turn_counter = list(entity.status)[idx].getTurnCounter()
            self.text_interface = self.bigFont.render(status_description, False, 'green')
            self.text_interface2 = self.mediumFont.render("Remaining turns: " + str(turn_counter), False, 'grey')

        pos = pygame.mouse.get_pos()
        for idx, icon in enumerate(self.enemy_status_icon.sprites()):
            if icon.rect.collidepoint(pos):
                showStatus(self.enemy)
                break
        for idx, icon in enumerate(self.player_status_icon.sprites()):
            if icon.rect.collidepoint(pos):
                showStatus(self.player)
                break
    def animatePlayer(self):
        if not self.playing_player_animation:
            self.play_player_sound = False
            self.player_origin_point = self.player_sprite.sprite.pos
        if self.playing_player_animation and self.play_player_animation:
            if not self.play_player_sound:
                self.play_player_sound = True
                movement_sound = mixer.Sound('../Controller/Sounds/melee sound.wav')
                movement_sound.play()
            self.player_sprite.sprite.pos += self.play_player_animation * 16
            if self.enemy_sprite.sprite.detection_zone.collidepoint(self.player_sprite.sprite.pos):
                attack_sound = mixer.Sound('../Controller/Sounds/Trap_00.wav')
                attack_sound.play()
                self.playerDealDamage()
                self.player_sprite.sprite.pos = self.player_origin_point
                self.playing_player_animation = False

    def animateEnemy(self):
        if not self.playing_enemy_animation:
            self.play_enemy_sound = False
            self.enemy_origin_point = self.enemy_sprite.sprite.pos
        if self.playing_enemy_animation and self.play_enemy_animation and self.enemy_turn:
            if not self.play_enemy_sound:
                self.play_enemy_sound = True
                movement_sound = mixer.Sound('../Controller/Sounds/swing.wav')
                movement_sound.play()
            self.enemy_sprite.sprite.pos += self.play_enemy_animation * 16
            if self.player_sprite.sprite.detection_zone.collidepoint(self.enemy_sprite.sprite.pos):
                attack_sound = mixer.Sound('../Controller/Sounds/sword-unsheathe5.wav')
                attack_sound.play()
                self.enemyDealDamage()
                self.enemy_sprite.sprite.pos = self.enemy_origin_point
                self.playing_enemy_animation = False
    def enemyDealDamage(self):
        # enemyAttacks
        if self.enemy_attack_idx >= len(self.enemy.getAttackPattern()):
            self.enemy_attack_idx = 0

        enemy_next_move = self.enemy.getAttack(self.enemy_attack_idx)
        enemy_attack_mods = self.enemy.getAttack(
            self.enemy_attack_idx).getModifiers()

        self.enemy.attack(self.player, enemy_next_move,
                          self.damageToInflict(self.enemy, self.player, enemy_attack_mods[0], enemy_attack_mods[1]))
        enemy_next_move.inflictDebuff(self.player)

        #enemy turn end
        self.enemy_attack_idx += 1
        for dot in self.enemy.dot_damage:
            print(self.enemy.getName() + " suffers " + str(dot[1]) + " damage from " + str(dot[0]))
            self.enemy.takeDamage(dot[1])
        for debuff in self.enemy.status.copy():
            debuff.counterDecrement()
            debuff.checkForEffectRemoval(self.enemy)
        self.checkForStatusIcon(self.player)
        self.checkForStatusIcon(self.enemy)
        self.enemy_turn = False
        self.enableButtons()

    def enableButtons(self):
        for button in self.button_group:
            button.enable()
    def disableButtons(self):
        for button in self.button_group:
            button.disable()
    def playerAttacks(self):
        self.playing_player_animation = True
        self.play_player_animation = (pygame.math.Vector2(self.enemy_sprite.sprite.rect.center) - pygame.math.Vector2(self.player_sprite.sprite.rect.center)).normalize()

    def playerDealDamage(self):
        self.player.attack(self.enemy, self.ability,
                           self.damageToInflict(self.player, self.enemy, self.ability.getElement(), self.ability.getDamageMod()))
        if self.ability.hasDebuff():
            self.ability.inflictDebuff(self.enemy)

        self.player_ap -= self.ability.cost

        self.checkForStatusIcon(self.player)
        self.checkForStatusIcon(self.enemy)
        self.enableButtons()
        if not self.enemy.isAlive():
            self.disableButtons()
    def playerTurnEnd(self):
        #commence enemy turn
        if self.enemy_turn:
            # decrement player debuffs
            for dot in self.player.dot_damage:
                print(self.player.getName() + " suffers " + str(dot[1]) + " damage from " + str(dot[0]))
                self.player.takeDamage(dot[1])
            for debuff in self.player.status.copy():
                debuff.counterDecrement()
                debuff.checkForEffectRemoval(self.player)
            if self.enemy.isAlive():
                self.enemyTurn()
            # reset player ap
            self.player_ap = self.default_player_ap

    def enemyTurn(self):
        self.playing_enemy_animation = True
        self.play_enemy_animation = (pygame.math.Vector2(self.player_sprite.sprite.rect.center) - pygame.math.Vector2(
            self.enemy_sprite.sprite.rect.center)).normalize()
        print("\n")#formatting
    def timer(self):
        wait_time = 1000
        if self.player_ap <= 0 and self.player_end_turn == False:
            #disable buttons
            for button in self.button_group:
                button.disable()

            self.player_end_turn_time = pygame.time.get_ticks()
            self.player_end_turn = True
        self.current_time = pygame.time.get_ticks()

        if self.current_time - self.player_end_turn_time >= wait_time and self.player_end_turn:
            self.enemy_turn = True
            self.player_end_turn = False
            self.player_end_turn_time = self.current_time
    def commenceBattle(self):

        for button in self.button_group:
            #player turn
            if not self.playing_player_animation or not self.playing_enemy_animation:
                if button.isClicked() and button.action_name.cost <= self.getPlayerAp():
                    self.performAction(button)
                    print(self.enemy.status)
                    print(self.enemy.take_more_damage)
                    print(self.enemy.weaken_attackPwr)
                    print(self.enemy.dot_damage)
            #enemy turn
            if self.player_ap <= 0:
                self.playerTurnEnd()
    def start(self):
        self.commenceBattle()
        self.update()
    def performAction(self, button):
        if button.action:
            self.ability = button.action_name
            self.playerAttacks()
        else:
            return
        button.action = False


