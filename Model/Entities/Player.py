from Model.BattleSystem.Ability.Ability import Ability
from Model.Entities.Entity import Entity
from Model.BattleSystem.Ability.AbilityList import ability_list
class Player(Entity):
    def __init__(self, name, hp, power):
        super().__init__(name, hp, power)
        self.addAbility(ability_list[0])
        self.learnAbility(ability_list[0])
        self.learnAbility(ability_list[4])
        self.learnAbility(ability_list[3])
        self.learnAbility(ability_list[5])
        self.learnAbility(ability_list[6])
        self.player_level = 1

    def _checkForDeath(self):
        if self.getHp() <= 0:
            super()._checkForDeath()
            print("Game over.")