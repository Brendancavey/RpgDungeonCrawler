from Model.BattleSystem.Ability.Ability import Ability
from Model.Entities.Entity import Entity
from Model.BattleSystem.Ability.AbilityList import ability_list
class Player(Entity):
    def __init__(self, name, hp, power):
        super().__init__(name, hp, power)
        self.attk = Ability("Slash", "Normal", 1, cost=1)
        self.addAbility(self.attk)
        #self.addAbility(ability_list[0])
        #self.addAbility(ability_list[1])
        #self.addAbility(ability_list[3])
        self.max_ap = 1
        self.player_level = 1

    def _checkForDeath(self):
        if self.getHp() <= 0:
            super()._checkForDeath()
            print("Game over.")