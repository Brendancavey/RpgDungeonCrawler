from Model.BattleSystem.EffectTypes import _effect_types_map
class Effect():
    def __init__(self, type_key, modifier):
        self._type = _effect_types_map[type_key]
        self._modifier = modifier

    def getType(self):
        return self._type

    def getModifier(self):
        return self._modifier