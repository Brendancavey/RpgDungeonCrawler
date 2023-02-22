from Model.Item import Item

class Potion(Item):
    def __init__(self, name, type, recovery_amt):
        super().__init__(name, type)
        self._recovery_amt = recovery_amt

    def getRecoveryAmt(self):
        return self._recovery_amt
    def getDescription(self):
        description = "Heals for " + str(self.getRecoveryAmt()) + " HP"
        return description
