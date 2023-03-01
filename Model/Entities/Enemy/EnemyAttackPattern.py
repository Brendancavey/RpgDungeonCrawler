class EnemyAttackPattern():
    def __init__(self, attack_pattern_list):
        self.attack_pattern_list = attack_pattern_list

    def getAttack(self, index):
        return self.attack_pattern_list[index]

    def getAttackPattern(self):
        return self.attack_pattern_list

    def newAttackPattern(self, new_attack_list):
        self.attack_pattern_list = new_attack_list