class Ability():
    def __init__(self, name, element, damage_mod, debuff = None, description = None):
        self.name = name
        self.element = element
        self.damage_mod = damage_mod
        self.debuff = debuff
        self.description = description

    def __repr__(self):
        return self.name
    def getName(self):
        return self.name
    def getElement(self):
        return self.element
    def getDamageMod(self):
        return self.damage_mod
    def getModifiers(self):
        return [self.getElement(), self.getDamageMod()]
    def getDescription(self, power):
        self.description = "Deal " + str(int(power)) + " damage"
        if self.debuff:
            self.description += ". Inflict " + self.debuff.getName()
        return self.description
    def inflictDebuff(self, enemy):
        if self.debuff:
            self.debuff.applyEffect(enemy)
            enemy.addDebuff(self.debuff)
    def hasDebuff(self):
        return self.debuff != None

