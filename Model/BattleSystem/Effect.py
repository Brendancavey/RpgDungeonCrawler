import Model.BattleSystem.EffectTypes as e
class Effect():
    def __init__(self, type_key, modifier):
        self._type = e._effect_types_map[type_key]
        self._modifier = modifier

    def getType(self):
        return self._type

    def getModifier(self):
        return self._modifier