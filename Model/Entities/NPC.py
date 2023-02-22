from Model.Entity import Entity

class NPC(Entity):
    def __init__(self, name, hp, power):
        super().__init__(name, hp, power)

    def chat(self):
        dialogue = "Be careful of trolls!"
        return dialogue

    def barter(self):
        print(self.showInventory())
    def playerPurchase(self, player, item):
        if self._itemInInventory(item):
            if player.getGoldValue() >= item.getPrice():
                player.modifyGold(-item.getPrice())
                self.modifyGold(item.getPrice())
                self.inventoryUse(item)
                player.inventoryAdd(item)
            else:
                print("Insufficient Gold")
        else:
            print("Item not available")