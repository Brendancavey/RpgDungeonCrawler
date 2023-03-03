import pygame
from Controller.GameData import locations

class Node(pygame.sprite.Sprite):
    def __init__(self, pos, status):
        super().__init__()
        self.image = pygame.Surface((100, 80))
        if status == 'available':
            self.image.fill('green')
        else:
            self.image.fill('red')
        self.rect = self.image.get_rect(center = pos)

class PlayerIcon(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((20,20))
        self.image.fill('blue')
        self.rect = self.image.get_rect(center = pos)
class Overworld():
    def __init__(self, start_location, max_location, surface):
        #setup
        self.display_surface = surface
        self.max_location = max_location
        self.current_location = start_location
        self.key_press_time = 0

        #sprites
        self.setupNodes()
        self.setupPlayerIcon()
    def setupPlayerIcon(self):
        self.player_icon = pygame.sprite.GroupSingle()
        icon_sprite = PlayerIcon(self.nodes.sprites()[self.current_location].rect.center)
        self.player_icon.add(icon_sprite)
    def setupNodes(self):
        self.nodes = pygame.sprite.Group()

        for idx, node in enumerate(locations.values()):
            if idx <= self.max_location:
                node_sprite = Node(node['node_pos'], 'available')
                self.nodes.add(node_sprite)
    def drawPaths(self):
        points = [node['node_pos'] for idx, node in enumerate(locations.values()) if idx <= self.max_location]
        pygame.draw.lines(self.display_surface, 'white', False, points, 6 )
        alt_point0 = locations[0]['node_pos']
        alt_point2 = locations[2]['node_pos']
        pygame.draw.lines(self.display_surface, 'white', False, (alt_point0, alt_point2), 6)

    def timer(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                self.key_press_time = pygame.get_ticks()
        self.current_time = pygame.time.get_ticks()
    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and self.current_location < self.max_location and self.current_time - self.key_press_time > 175:
            self.key_press_time = self.current_time
            print('move right')
            self.current_location += 1
        elif(keys[pygame.K_LEFT]) and self.current_location > 0 and self.current_time - self.key_press_time > 175:
            self.key_press_time = self.current_time
            print('move left')
            self.current_location -= 1
    def updatePlayerIconPos(self):
        self.player_icon.sprite.rect.center = self.nodes.sprites()[self.current_location].rect.center
    def run(self):
        self.timer()
        self.input()
        self.updatePlayerIconPos()
        self.drawPaths()
        self.nodes.draw(self.display_surface)
        self.player_icon.draw(self.display_surface)
