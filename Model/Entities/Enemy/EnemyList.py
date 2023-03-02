import Model.Entities.Enemy.AttackPatterns as a
from Model.Entities.Enemy.Enemy import Enemy

enemy0 = Enemy("Slime", 15, 3, a.attack_patterns[0])
enemy1 = Enemy("Goblin", 20, 4, a.attack_patterns[1])
enemy2 = Enemy("Troll", 50, 8, a.attack_patterns[0])
enemy3 = Enemy("Degenerate Slime", 100, 4, a.attack_patterns[3])

enemy_list = [enemy0,
              enemy1,
              enemy2,
              enemy3]