from Model.BattleSystem.Debuff.Debuff import Debuff
import pygame
pygame.init()
debuff0 = Debuff("Vulnerable", 2, 1, 2, "Receive 100% additional incoming direct-damage.",
                 image = pygame.image.load('../View/Graphics/debuff_vulnerable.png'))
debuff1 = Debuff("Weakened", 2, 2, .25, "Outdoing direct damage is reduced by 25%.",
                 image = pygame.image.load('../View/Graphics/debuff_weaken.png'))
debuff2 = Debuff("Bleed", 2, 0, 2, "Receive 2 damage to hp per turn.",
                 image = pygame.image.load('../View/Graphics/debuff_bleed.png'))
debuff3 = Debuff("Poison", 10, 0, 1, "Receive 1 damage to hp per turn.",
                 image = pygame.image.load('../View/Graphics/debuff_poison.png'))
debuff4 = Debuff("Open Wound", 3, 1, 1.5, "Receive 50% additional incoming direct-damage.",
                 image = pygame.image.load('../View/Graphics/debuff_wound.png'))
debuff_list = [debuff0,
               debuff1,
               debuff2,
               debuff3,
               debuff4]