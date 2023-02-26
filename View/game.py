import pygame
from sys import exit
from Model.Entities.Enemy import Enemy
from Model.Sprites.Button import Button
enemy = Enemy("Sephiroth", 100, 25)
pygame.init()
resolution = (720, 720)

clock = pygame.time.Clock()
framerate = 60
green = (0, 255, 0)
blue = (50, 153, 213)
font = pygame.font.Font(None, 50)
#font = pygame.font.font('font/fontstyle.ttf, font-size)

screen = pygame.display.set_mode(resolution)
pygame.display.set_caption("Simple RPG")
width = screen.get_width()
height = screen.get_height()

test_surface = pygame.Surface(resolution)
test_surface.fill(blue)
#background = pygame.image.load('graphics/background.png').convert()


#player_rect = pygame.draw.rect(test_surface, "green", (width//8,height-(height//2),200,50))
button1 = Button(200, 50, width//4, height//1.5, "green")
button2 = Button(200, 50, width//1.5, height//1.5, "green")
button3 = Button(200, 50, width//4, height//2, "green")
button4 = Button(200, 50, width//1.5, height//2, "green")
buttons = [button1, button2, button3, button4]
button_group = pygame.sprite.Group()
for button in buttons:
    button_group.add(button)


text_surface = font.render(str(enemy.getHp()), False, "black")


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    button_group.update()
    if button1.isClicked():
        button1.performAction(None)
    pygame.display.update()
    #screen.blit(background, (0,0))
    screen.blit(test_surface, (0,0))
    screen.blit(text_surface, (300,50))
    button_group.draw(test_surface)


    clock.tick(framerate)