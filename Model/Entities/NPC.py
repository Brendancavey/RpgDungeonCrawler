from Model.Entities.Entity import Entity
import pygame
pygame.init()
class NPC(Entity):
    font = pygame.font.Font(None, 35)
    def __init__(self, name, hp, power, dialogue):
        super().__init__(name, hp, power)
        #self._done_chatting = False
        self.dialogue = dialogue
        self.quest = 0

    def chat(self, display_surface):
        #setup
        self._done_chatting = False
        keys = pygame.key.get_pressed()

        #user input
        if keys[pygame.K_SPACE]:
            self._done_chatting = True

        #screen and textbox
        self.screen = display_surface
        self.textbox = pygame.Surface((1280, 200))
        self.textbox.fill('bisque')

        # update screen
            #text info
        self.text_npcName = self.font.render(self.getName() + ": ", False, 'black')
        self.text_dialogue = self.font.render(self.dialogue, False, 'black')

        # blit to screen
        self.screen.blit(self.textbox, (0, 550))
        self.screen.blit(self.text_npcName, (60, 560))
        self.screen.blit(self.text_dialogue, (90, 595))
    def setDialogue(self, new_dialogue):
        self.dialogue = new_dialogue

    def doneChatting(self):
        return self._done_chatting

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