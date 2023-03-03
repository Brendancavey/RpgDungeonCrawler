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
class Overworld:
    def __init__(self, start_location, max_location, surface):
        #setup
        self.display_surface = surface
        self.max_location = max_location
        self.current_location = start_location

        #sprites
        self.setupNodes()

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
    def run(self):
        self.drawPaths()
        self.nodes.draw(self.display_surface)
