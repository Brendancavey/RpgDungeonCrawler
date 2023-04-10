from Model.BattleSystem.Debuff.Debuff import Debuff
import pygame
pygame.init()
debuff0 = Debuff("Vulnerable", 2, 1, 2, "Receive 100% additional incoming direct-damage. Stacks duration.",
                 image = pygame.image.load('../View/Graphics/debuff_vulnerable.png'))
debuff1 = Debuff("Weakened", 2, 2, .25, "Outdoing direct damage is reduced by 25%. Stacks duration",
                 image = pygame.image.load('../View/Graphics/debuff_weaken.png'))
debuff2 = Debuff("Bleed", 10, 0, 1, "Receive 1 damage to hp at start of turn. Stacks effectiveness.",
                 image = pygame.image.load('../View/Graphics/debuff_bleed.png'))
debuff3 = Debuff("Poison", 10, 0, 1, "Receive 1 damage to hp at start of turn. Stacks effectiveness.",
                 image = pygame.image.load('../View/Graphics/debuff_poison.png'))
debuff4 = Debuff("Open Wound", 3, 1, 1.5, "Receive 50% additional incoming direct-damage. Stacks duration.",
                 image = pygame.image.load('../View/Graphics/debuff_wound.png'))
debuff5 = Debuff("Bleed-Hemorrhage", 4, 0, 5, "Receive 5 damage to hp per turn. Stacks effectiveness.",
                 image = pygame.image.load('../View/Graphics/debuff_bleed.png'))
debuff_list = [debuff0,
               debuff1,
               debuff2,
               debuff3,
               debuff4,
               debuff5]