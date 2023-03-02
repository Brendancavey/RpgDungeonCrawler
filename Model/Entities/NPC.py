from Model.Entities.Entity import Entity

class NPC(Entity):
    def __init__(self, name, hp, power):
        super().__init__(name, hp, power)

    def chat(self):
        dialogue = "Be careful of trolls!"
        return dialogue

    def barter(self):
        print(self.getInventory())
    def playerPurchase(self, player, item):
        if self._inventory.itemInInventory(item):
            if player.getGoldValue() >= item.getPrice():
                player.modifyGold(-item.getPrice())
                self.modifyGold(item.getPrice())
                self.itemRemove(item)
                player.itemObtain(item)
            else:
                print("Insufficient " + self._inventory.getNameGold())
        else:
            print(str(item) + " not available")