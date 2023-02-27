from Model.Sprites.Button import Button
import pygame
class BattleSystem():
    pygame.init()
    blue = (50, 153, 213)
    font = pygame.font.Font(None, 50)
    def __init__(self, player, enemy, screen_width, screen_height):
        # player
        self.player = player
        self.default_player_ap = 3
        self.player_ap = self.default_player_ap

        # enemy
        self.enemy = enemy
        self.enemy_attack_pattern_map = {"attack": enemy.attack, "guard": enemy.guard}
        self.enemy_attack_idx = 0

        #buttons
        self.button1 = Button(200, 50, screen_width//4, screen_height//1.5, "green")
        self.button2 = Button(200, 50, screen_width // 1.5, screen_height // 1.5, "green")
        self.button3 = Button(200, 50, screen_width // 4, screen_height // 2, "green")
        self.button4 = Button(200, 50, screen_width // 1.5, screen_height // 2, "green")
        self.buttons = [self.button1, self.button2, self.button3, self.button4]
        self.button_group = pygame.sprite.Group()
        for button in self.buttons:
            self.button_group.add(button)

        # screen and surface
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.surface = pygame.Surface((screen_width, screen_height))
        self.surface.fill(self.blue)
            #text info
        self.text_enemyHp = self.font.render(str(self.enemy.getName()) + " HP: " + str(self.enemy.getHp()), False, "black")
        self.text_playerAp = self.font.render("AP: " + str(self.getPlayerAp()), False, "black")
        self.text_playerHp = self.font.render(str(self.player.getName()) + " HP: " + str(self.player.getHp()), False, "black")

    def update(self):
        #update buttons
        self.button_group.update()

        #update screen
        self.text_enemyHp = self.font.render(str(self.enemy.getName()) + " HP: " + str(self.enemy.getHp()), False, "black")
        self.text_playerAp = self.font.render("AP: " + str(self.getPlayerAp()), False, "black")
        self.text_playerHp = self.font.render(str(self.player.getName()) + " HP: " + str(self.player.getHp()), False,
                                              "black")
        self.button_group.draw(self.surface)
        self.screen.blit(self.surface, (0, 0))
        self.screen.blit(self.text_enemyHp, (250, 50))
        self.screen.blit(self.text_playerAp, (500, 600))
        self.screen.blit(self.text_playerHp, (200, 600))
    def getPlayerAp(self):
        return self.player_ap
    def playerAttacks(self):
        if self.getPlayerAp() > 0:
            self.player.attack(self.enemy)
            self.player_ap -= 1

    def playerTurnEnd(self):
        self.player_ap = self.default_player_ap
        print("\n")#formatting
        self.enemyAttacks()

    def enemyAttacks(self):
        if self.enemy_attack_idx >= len(self.enemy.getAttackPattern()) :
            self.enemy_attack_idx = 0
        enemy_next_move = self.enemy_attack_pattern_map[self.enemy.getAttack(self.enemy_attack_idx)](self.player)
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
            if button._id == 0:
                print("perform action 0")
                self.playerAttacks()
            if button._id == 1:
                print("perform action 1")
                self.player.guard(self.enemy)
            if button._id == 2:
                print("perform action 2")
                print("Do some skill")
            if button._id == 3:
                print("perform action 3")
                print("Do some other skill")
        else:
            return
        button.action = False


