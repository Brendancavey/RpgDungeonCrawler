from Model.Entities.Entity import Entity
from Model.Entities.Enemy.EnemyAttackPattern import EnemyAttackPattern
from Controller.ObjectsList import armor_list, potion_list, weapons_list, accessories_list, items_list0
import random


class Enemy(Entity):
    def __init__(self, name, hp, power, default_attack_pattern_list, encounter_sound,
                 attack_sound, image = None):
        super().__init__(name, hp, power)
        self.attack_pattern = EnemyAttackPattern(default_attack_pattern_list)
        self.image = image
        self.encounter_sound = encounter_sound
        self.attack_sound = attack_sound
        self.loot = [random.randint(1, 5), items_list0[random.randint(0, len(items_list0)-1)]]
    def getAttack(self, index):
        return self.attack_pattern.getAttack(index)
    def getAttackPattern(self):
        return self.attack_pattern.getAttackPattern()

    def getImage(self):
        return self.image

