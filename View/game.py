import pygame
import random
import Model.Entities.Enemy.EnemyList as e
from sys import exit
from Model.Entities.Enemy.Enemy import Enemy
from Model.Entities.Player import Player
from Model.BattleSystem.BattleSystem import BattleSystem
from Model.Items.Potion import Potion
from Model.BattleSystem.Ability.Ability import Ability
from Model.BattleSystem.Debuff.Debuff import Debuff
from Controller.Setting import *
from Model.Game import Game
potion = Potion("Large Potion", 1,10, 100)
potion2 = Potion("Small Potion", 1, 2, 25)
player = Player("Player", 50, 5)
#enemy = Enemy("Sephiroth", 100, 5)
debuff1 = Debuff("Vulnerable", 2, 1, 2)
debuff2 = Debuff("Weakened", 2, 2, .25)
debuff3 = Debuff("Bleed", 2, 0, 2)
ability1 = Ability("Deep Stab", "Normal", 1.2, debuff1)
ability2 = Ability ("Tail Whip", "Normal", int(0), debuff2)
ability3 = Ability("Gashing Strike", "Normal", 1.1, debuff3)
player.addAbility(ability1)
player.addAbility(ability2)
player.addAbility(ability3)
player.itemObtain(potion)
player.itemObtain(potion2)
player.itemObtain(potion2)
print(player.getItems())
print(player.getAbilities())
pygame.init()
resolution = (screen_width, screen_height)

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
game = Game(screen)

test_surface = pygame.Surface(resolution)
test_surface.fill(blue)
#background = pygame.image.load('graphics/background.png').convert()

battle = BattleSystem(player, e.enemy_list[random.randint(0,len(e.enemy_list)-1)], width, height)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    game.run()
    #battle.commenceBattle()
    #battle.update()
    if not battle.enemy.isAlive():
        print("you win!")
        pygame.quit()
        exit()
    pygame.display.update()
    #screen.blit(background, (0,0))

    clock.tick(framerate)