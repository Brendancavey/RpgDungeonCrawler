from Model.Entities.Entity import Entity

class Player(Entity):
    def __init__(self, name, hp, power):
        super().__init__(name, hp, power)

    def _checkForDeath(self):
        if self.getHp() <= 0:
            super()._checkForDeath()
            print("Game over.")