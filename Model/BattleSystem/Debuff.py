from Model.BattleSystem.Effect import Effect
import Model.BattleSystem.EffectTypes as e
class Debuff():
    def __init__(self, name, turn_counter, type_key, modifier):
        self.name = name
        self.default_turn_counter = turn_counter
        self.turn_counter = turn_counter
        self.effect = Effect(type_key, modifier)

    def __repr__(self):
        return self.name + ": " + str(self.turn_counter)
    def getName(self):
        return self.name + ": " + str(self.turn_counter)
    def getTurnCounter(self):
        return self.turn_counter
    def counterDecrement(self, value = 1):
        self.turn_counter -= value
    def counterIncrement(self, value = 1):
        self.turn_counter += value
    def applyEffect(self, enemy):
        if self not in enemy.status:
            self.turn_counter = self.default_turn_counter
            effect_type = self.effect.getType()
            if effect_type == e._effect_types_map[0]:
                enemy.dot_damage.append(self.effect.getModifier())
            elif effect_type == e._effect_types_map[1]:
                enemy.take_more_damage.append(self.effect.getModifier())
            elif effect_type == e._effect_types_map[2]:
                enemy.weaken_attackPwr.append(self.effect.getModifier())
    def checkForEffectRemoval(self, entity):
        if self.turn_counter <= 0:
            entity.status.remove(self)
            effect_type = self.effect.getType()
            if effect_type == e._effect_types_map[0]:
                entity.dot_damage.remove(self.effect.getModifier())
            elif effect_type == e._effect_types_map[1]:
                entity.take_more_damage.remove(self.effect.getModifier())
            elif effect_type == e._effect_types_map[2]:
                entity.weaken_attackPwr.remove(self.effect.getModifier())
