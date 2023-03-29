import pygame
from Model.Entities.Enemy.AttackPatterns import attack_patterns
from Model.Entities.Enemy.Enemy import Enemy

enemy0 = Enemy("Enemy0", 10, 3, attack_patterns[0], pygame.image.load('../View/Graphics/goblin.png'))
enemy1 = Enemy("Enemy1", 20, 5, attack_patterns[1], pygame.image.load('../View/Graphics/goblin.png'))
enemy2 = Enemy("Enemy2", 30, 8, attack_patterns[2], pygame.image.load('../View/Graphics/goblin.png'))
enemy3 = Enemy("Enemy3", 30, 8, attack_patterns[3], pygame.image.load('../View/Graphics/goblin.png'))
enemy4 = Enemy("Enemy4", 30, 8, attack_patterns[4], pygame.image.load('../View/Graphics/goblin.png'))
enemy5 = Enemy("Enemy5", 50, 8, attack_patterns[1], pygame.image.load('../View/Graphics/goblin.png'))

enemy_list = [enemy0,
              enemy1,
              enemy2,
              enemy3,
              enemy4,
              enemy5,]