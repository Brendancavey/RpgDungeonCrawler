from Model.Entities.Entity import Entity
from Model.Entities.Enemy.EnemyAttackPattern import EnemyAttackPattern

class Enemy(Entity):
    def __init__(self, name, hp, power, default_attack_pattern_list):
        super().__init__(name, hp, power)
        #self.attack_pattern = ["attack", "attack", "guard"]
        self.abilities = self.abilities + default_attack_pattern_list
        self.attack_pattern = EnemyAttackPattern(self.getAbilities())

    def getAttack(self, index):
        return self.attack_pattern.getAttack(index)
    def getAttackPattern(self):
        return self.attack_pattern.getAttackPattern()