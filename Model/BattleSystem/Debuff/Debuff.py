from Model.BattleSystem.Effect import Effect
from Model.BattleSystem.EffectTypes import _effect_types_map
class Debuff():
    def __init__(self, name, turn_counter, type_key, modifier, description, image = None):
        self.name = name
        self.default_turn_counter = turn_counter
        self.turn_counter = turn_counter
        self.effect = Effect(type_key, modifier)
        self.status_mod = (self.name, self.effect.getModifier())
        self.description = description
        self.image = image

    def __repr__(self):
        return self.name + ": " + str(self.turn_counter)
    def getName(self):
        return self.name + ": " + str(self.default_turn_counter)
    def getTurnCounter(self):
        return self.turn_counter
    def getDescription(self):
        return self.name + ": " + self.description
    def counterDecrement(self, value = 1):
        self.turn_counter -= value
    def counterIncrement(self, value = 1):
        self.turn_counter += value
    def applyEffect(self, enemy):
        if self not in enemy.status:
            self.turn_counter = self.default_turn_counter
            effect_type = self.effect.getType()
            if effect_type == _effect_types_map[0]:
                enemy.dot_damage.append(self.status_mod)
            elif effect_type == _effect_types_map[1]:
                enemy.take_more_damage.append(self.status_mod)
            elif effect_type == _effect_types_map[2]:
                enemy.weaken_attackPwr.append(self.status_mod)
            print("Inflicted " + enemy.getName() + " with " + self.name)
        else:
            print(enemy.getName() + " already afflicted with " + self.name)
    def checkForEffectRemoval(self, entity):
        if self.turn_counter <= 0:
            entity.status.remove(self)
            effect_type = self.effect.getType()
            if effect_type == _effect_types_map[0]:
                entity.dot_damage.remove(self.status_mod)
            elif effect_type == _effect_types_map[1]:
                entity.take_more_damage.remove(self.status_mod)
            elif effect_type == _effect_types_map[2]:
                entity.weaken_attackPwr.remove(self.status_mod)
