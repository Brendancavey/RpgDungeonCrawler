from Model.Inventory.Item import Item

class Potion(Item):
    def __init__(self, name, type, price, recovery_amt):
        super().__init__(name, type, price)
        self._recovery_amt = recovery_amt

    def getRecoveryAmt(self):
        return self._recovery_amt
    def getDescription(self):
        description = self._name + ": Heals for " + str(self.getRecoveryAmt()) + " HP"
        return description
