import pygame
import itertools

class Button(pygame.sprite.Sprite):
    #_id_iter = itertools.count()
    def __init__(self, width, height, pos_x, pos_y, color, action_name, id):
        super().__init__()
        self.width = width
        self.height = height
        self.color = color
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (pos_x, pos_y)
        #self._id = next(self._id_iter)
        self._id = id
        self.not_clicked = True
        self.action = False
        self.action_name = action_name

    def setId(self, new_id):
        self._id = new_id
    def update(self):
        #check for mouse over button hover
        self.isHovered()

        #check for button click
        self.isClicked()
    def isHovered(self):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            self.image.fill("aquamarine1")
            return True
        else:
            self.image.fill(self.color)
            return False
    def isClicked(self):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] == 1 and self.not_clicked:
            self.not_clicked = False
            self.action = True
            print("you clicked button " + str(self._id))
        if pygame.mouse.get_pressed()[0] == 0:
            self.not_clicked = True
        return self.action


