import pygame
from Model.Entities.Enemy.AttackPatterns import attack_patterns
from Model.Entities.Enemy.Enemy import Enemy

enemy0 = Enemy("Slime", 15, 3, attack_patterns[0], pygame.image.load('../View/Graphics/goblin.png'))
enemy1 = Enemy("Goblin", 20, 4, attack_patterns[1], pygame.image.load('../View/Graphics/goblin.png'))
enemy2 = Enemy("Troll", 50, 8, attack_patterns[0], pygame.image.load('../View/Graphics/goblin.png'))
enemy3 = Enemy("Degenerate Slime", 1000, 4, attack_patterns[3], pygame.image.load('../View/Graphics/goblin.png'))

enemy_list = [enemy0,
              enemy1,
              enemy2,
              enemy3]