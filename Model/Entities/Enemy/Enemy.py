from Model.Entities.Entity import Entity
from Model.Entities.Enemy.EnemyAttackPattern import EnemyAttackPattern
from Controller.ObjectsList import armor_list, potion_list, weapons_list, accessories_list, items_list0
import random


class Enemy(Entity):
    def __init__(self, name, hp, power, default_attack_pattern_list, image = None):
        super().__init__(name, hp, power)
        self.abilities = self.abilities + default_attack_pattern_list
        self.attack_pattern = EnemyAttackPattern(self.getAbilities())
        self.image = image
        self.loot = [random.randint(1, 5), armor_list[0], weapons_list[1], potion_list[2], items_list0[random.randint(0, len(items_list0)-1)]]
    def getAttack(self, index):
        return self.attack_pattern.getAttack(index)
    def getAttackPattern(self):
        return self.attack_pattern.getAttackPattern()

    def getImage(self):
        return self.image

