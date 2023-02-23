from Model.Entity import Entity

class Enemy(Entity):
    def __init__(self, name, hp, power):
        super().__init__(name, hp, power)
        self.attack_pattern = ["attack", "attack", "guard"]

    def getAttack(self, index):
        return self.attack_pattern[index]
    def getAttackPattern(self):
        return self.attack_pattern