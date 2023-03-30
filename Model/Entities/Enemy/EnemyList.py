import pygame
from Model.Entities.Enemy.AttackPatterns import attack_patterns
from Model.Entities.Enemy.Enemy import Enemy
from pygame import mixer

goblin0 = Enemy("Goblin0", 10, 3, attack_patterns[0], image= pygame.image.load('../View/Graphics/goblin0.png'),
                encounter_sound=mixer.Sound('../Controller/Sounds/ogre2.wav'),
                attack_sound=mixer.Sound('../Controller/Sounds/sword-unsheathe5.wav'))
goblin1 = Enemy("Goblin1", 20, 5, attack_patterns[1], image= pygame.image.load('../View/Graphics/goblin1.png'),
                encounter_sound=mixer.Sound('../Controller/Sounds/wolfman.wav'),
                attack_sound=mixer.Sound('../Controller/Sounds/sword-unsheathe5.wav'))
goblin2 = Enemy("Goblin2", 30, 8, attack_patterns[2], image= pygame.image.load('../View/Graphics/goblin2.png'),
                encounter_sound=mixer.Sound('../Controller/Sounds/mnstr6.wav'),
                attack_sound=mixer.Sound('../Controller/Sounds/sword-unsheathe2.wav'))
goblin3 = Enemy("Goblin3", 30, 8, attack_patterns[3], image= pygame.image.load('../View/Graphics/goblin3.png'),
                encounter_sound=mixer.Sound('../Controller/Sounds/mnstr7.wav'),
                attack_sound=mixer.Sound('../Controller/Sounds/sword-unsheathe4.wav'))
goblin4 = Enemy("Goblin4", 30, 8, attack_patterns[4], image= pygame.image.load('../View/Graphics/goblin4.png'),
                encounter_sound=mixer.Sound('../Controller/Sounds/mnstr9.wav'),
                attack_sound=mixer.Sound('../Controller/Sounds/interface3.wav'))
skeleton0 = Enemy("Skeleton0", 50, 8, attack_patterns[1], image= pygame.image.load('../View/Graphics/skeleton0.png'),
               encounter_sound=mixer.Sound('../Controller/Sounds/wood-small.wav'),
               attack_sound=mixer.Sound('../Controller/Sounds/interface5.wav'))

enemy_list = [goblin0,
              goblin1,
              goblin2,
              goblin3,
              goblin4,
              skeleton0, ]