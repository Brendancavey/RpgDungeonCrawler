from math import ceil
class Ability():
    def __init__(self, name, element, damage_mod, debuff = None, description = None, cost = None, special_message = None,
                 sound_effect = None, attack_times = 1):
        self.name = name
        self.element = element
        self.damage_mod = damage_mod
        self.debuff = debuff
        self.description = description
        self.cost = cost
        self.special_message = special_message
        self.default_special_message = special_message
        self.sound_effect = sound_effect
        self.attack_times = attack_times

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
        #self.description = "Deal " + str(int(power)) + " damage"
        self.description = ""
        if self.special_message:
            self.description += ". " + self.special_message
        if self.debuff:
            self.description += ". Inflict " + self.debuff.getName()
        return self.description
    def getPowerDescription(self, power):
        return "Deal " + str(ceil(power * self.damage_mod)) + " damage"
    def getSpecialDescription(self):
        if self.special_message:
            return self.special_message
    def getDebuffDescription(self):
        if self.debuff:
            return "Inflict " + self.debuff.getName()
    def inflictDebuff(self, enemy):
        if self.debuff:
            self.debuff.applyEffect(enemy)
            enemy.addDebuff(self.debuff)
    def hasDebuff(self):
        return self.debuff != None

