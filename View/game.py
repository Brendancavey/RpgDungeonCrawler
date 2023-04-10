import pygame
from sys import exit
from Controller.Setting import *
from Model.Game import Game

pygame.init()
resolution = (screen_width, screen_height)

clock = pygame.time.Clock()


framerate = 60
green = (0, 255, 0)
blue = (50, 153, 213)
font = pygame.font.Font(None, 50)

screen = pygame.display.set_mode(resolution)
pygame.display.set_caption("RPG Dungeon Crawler")
width = screen.get_width()
height = screen.get_height()
game = Game(screen)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    game.run()
    pygame.display.update()

    clock.tick(framerate)