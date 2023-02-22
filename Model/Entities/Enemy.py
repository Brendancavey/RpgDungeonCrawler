from Model.Entity import Entity

class Enemy(Entity):
    def __init__(self, name, hp, power):
        super().__init__(name, hp, power)