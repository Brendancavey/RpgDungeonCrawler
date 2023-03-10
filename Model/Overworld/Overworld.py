import pygame
from Controller.GameData import locations
from Controller.Setting import screen_height, screen_width

class Node(pygame.sprite.Sprite):
    def __init__(self, pos, status):
        node_size = (100,80)
        super().__init__()
        self.image = pygame.Surface(node_size)
        if status == 'available':
            self.image.fill('green')
        else:
            self.image.fill('grey')
        self.rect = self.image.get_rect(center = pos)

class Icon(pygame.sprite.Sprite):
    def __init__(self, pos, color):
        size = (20, 20)
        super().__init__()
        self.image = pygame.Surface(size)
        self.image.fill(color)
        self.rect = self.image.get_rect(center = pos)
class Overworld():
    def __init__(self, start_location, max_location, display_surface, create_location, enemies, enemy_locations):
        #setup
        self.display_surface = display_surface
        self.max_location = max_location
        self.current_location = start_location
        self.key_press_time = 0
        self.create_location = create_location
        self.enemy_icons = enemies
        self.enemy_locations = enemy_locations

            # screen and surface
        self.width = screen_width
        self.height = screen_height
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.surface = pygame.Surface((screen_width, screen_height))
        self.surface.fill("black")

        #sprites
        self.setupNodes()
        self.setupPlayerIcon()
        self.setupEnemyIcons()
    def setupPlayerIcon(self):
        self.player_icon = pygame.sprite.GroupSingle()
        icon_sprite = Icon(self.nodes.sprites()[self.current_location].rect.center, 'blue')
        self.player_icon.add(icon_sprite)
    def setupEnemyIcons(self):
        icon_sprites = []
        for location in self.enemy_locations:
            print(location)
            icon = Icon(self.nodes.sprites()[location].rect.center, 'red')
            icon_sprites.append(icon)
        for icon in icon_sprites:
            self.enemy_icons.add(icon)
        pygame.sprite.spritecollide(self.player_icon.sprite, self.enemy_icons, True)
    def setupNodes(self):
        self.nodes = pygame.sprite.Group()

        for idx, node in enumerate(locations.values()):
            if idx <= self.max_location:
                node_sprite = Node(node['node_pos'], 'available')
                self.nodes.add(node_sprite)
    def drawPaths(self):
        line_width = 6
        points = [node['node_pos'] for idx, node in enumerate(locations.values()) if idx <= self.max_location]
        horizontal_points = [node['node_pos'] for idx, node in enumerate(locations.values()) if idx <= self.max_location and idx % 2 == 0]
        pygame.draw.lines(self.display_surface, 'white', False, points, line_width )
        pygame.draw.lines(self.display_surface, 'white', False, horizontal_points, line_width)



    def timer(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                self.key_press_time = pygame.time.get_ticks()
        self.current_time = pygame.time.get_ticks()
    def input(self):
        keys = pygame.key.get_pressed()
        delay_time = 175

        if pygame.sprite.spritecollide(self.player_icon.sprite, self.enemy_icons, True):
            self.enemy_locations.remove(self.current_location)
            self.create_location(self.current_location, self.enemy_icons, self.enemy_locations)
       # if keys[pygame.K_SPACE]:
        elif keys[pygame.K_UP] and self.current_location < self.max_location and self.current_time - self.key_press_time > delay_time:
            self.key_press_time = self.current_time
            self.current_location += 1
        elif keys[pygame.K_DOWN] and self.current_location < self.max_location and self.current_time - self.key_press_time > delay_time and self.current_location % 2 != 0:
            self.key_press_time = self.current_time
            self.current_location += 1
        elif keys[pygame.K_RIGHT] and self.current_location < self.max_location and self.current_time - self.key_press_time > delay_time and self.current_location % 2 == 0:
            self.key_press_time = self.current_time
            self.current_location += 2
        elif(keys[pygame.K_LEFT]) and self.current_location > 0 and self.current_time - self.key_press_time > delay_time:
            self.key_press_time = self.current_time
            if self.current_location % 2 == 0:
                self.current_location -= 2
            else:
                self.current_location -= 1


    def updatePlayerIconPos(self):
        self.player_icon.sprite.rect.center = self.nodes.sprites()[self.current_location].rect.center
    def run(self):
        self.screen.blit(self.surface, (0, 0))
        self.timer()
        self.input()
        self.updatePlayerIconPos()
        self.drawPaths()
        self.nodes.draw(self.display_surface)
        self.enemy_icons.draw(self.display_surface)
        self.player_icon.draw(self.display_surface)
