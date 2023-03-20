from Model.Entities.Entity import Entity
from Model.BattleSystem.Ability.AbilityList import ability_list
class Player(Entity):
    def __init__(self, name, hp, power):
        super().__init__(name, hp, power)
        self.addAbility(ability_list[0])
        self.addAbility(ability_list[1])
        self.addAbility(ability_list[2])

    def _checkForDeath(self):
        if self.getHp() <= 0:
            super()._checkForDeath()
            print("Game over.")