import pygame
from sys import exit
from Model.Entities.Enemy import Enemy
from Model.Entities.Player import Player
from Model.BattleSystem.BattleSystem import BattleSystem
from Model.Items.Potion import Potion
from Model.BattleSystem.Ability import Ability
from Model.BattleSystem.Debuff import Debuff

potion = Potion("Small Potion", 1,10, 100)
player = Player("Player", 50, 10)
enemy = Enemy("Sephiroth", 100, 25)
no_debuff = Debuff()
vulnerable = Ability("Deep Stab", "Normal", 1.2, "vulnerable")
player.addAbility(vulnerable)
player.itemObtain(potion)
print(player.getItems())
print(player.getAbilities())
pygame.init()
resolution = (720, 720)

clock = pygame.time.Clock()
framerate = 60
green = (0, 255, 0)
blue = (50, 153, 213)
font = pygame.font.Font(None, 50)
#font = pygame.font.font('font/fontstyle.ttf, font-size)

screen = pygame.display.set_mode(resolution)
pygame.display.set_caption("Simple RPG")
width = screen.get_width()
height = screen.get_height()

test_surface = pygame.Surface(resolution)
test_surface.fill(blue)
#background = pygame.image.load('graphics/background.png').convert()

battle = BattleSystem(player, enemy, width, height)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    battle.commenceBattle()
    battle.update()
    pygame.display.update()
    #screen.blit(background, (0,0))

    clock.tick(framerate)