import pygame
from Controller.GameData import locations
from Controller.Setting import screen_height, screen_width
class Node(pygame.sprite.Sprite):
    def __init__(self, pos, status, icon_speed):
        node_size = (100,80)
        super().__init__()
        self.image = pygame.Surface(node_size)
        self.status = status
        if self.status == 'available':
            self.image.fill('grey')
        else:
            self.image.fill('black')
        self.rect = self.image.get_rect(center = pos)
        self.detection_zone = pygame.Rect(self.rect.centerx-(icon_speed/2),self.rect.centery-(icon_speed/2),icon_speed,icon_speed)
        self.pos = pos
    def getPos(self):
        return self.pos
class Icon(pygame.sprite.Sprite):
    def __init__(self, pos, color):
        size = (20, 20)
        super().__init__()
        self.pos = pos
        self.image = pygame.Surface(size)
        self.image.fill(color)
        self.rect = self.image.get_rect(center = pos)
    def update(self):
        self.rect.center = self.pos
class Overworld():
    def __init__(self, start_location, max_location, display_surface, create_location, enemies, enemy_locations, visited,
                treasure_locations):
        #setup
        self.display_surface = display_surface
        self.max_location = max_location
        self.current_location = start_location
        self.key_press_time = 0
        self.create_location = create_location

        #enemies
        self.enemy_icons = enemies
        self.enemy_locations = enemy_locations

        #treasure
        self.treasure_locations = treasure_locations

        #movement logic
        self.moving = False
        self.move_direction = pygame.math.Vector2(0,0)
        self.speed = 4

        #overworld map stack data structure
        self.visited = visited

        #screen and surface
        self.width = screen_width
        self.height = screen_height
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.surface = pygame.Surface((screen_width, screen_height))
        self.surface.fill("black")

        #sprites
        self.setupNodes()
        self.setupPlayerIcon()
        self.setupEnemyIcons()
        self.setupTreasureIcons()
    def getPrevNode(self):
        return self.visited.pop(-1)
    def getNextNode(self, direction):
        if direction == 'up':
            return self.current_location + 1
        elif direction == 'right':
            return self.current_location + 2
        elif direction == 'down':
            return self.current_location - 1
        elif direction == 'left':
            return self.current_location - 2
    def findNextNode(self, current_location, direction):
        if direction == 'up':
            return current_location + 1
        elif direction == 'right':
            return current_location + 2
    def setupPlayerIcon(self):
        self.player_icon = pygame.sprite.GroupSingle()
        for idx, location in enumerate(self.cur_adjaceny_list):
            if self.current_location == location:
                idx_of_nodes = idx
        current_node = self.nodes.sprites()[idx_of_nodes]
        icon_sprite = Icon(current_node.rect.center, 'blue')
        self.player_icon.add(icon_sprite)
    def setupEnemyIcons(self):
        icon_sprites = []
        self.enemy_icons = pygame.sprite.Group()
        for location in self.enemy_locations:
            if location in self.cur_adjaceny_list:
                idx = self.cur_adjaceny_list.index(location)
                icon = Icon(self.nodes.sprites()[idx].rect.center, 'red')
                icon_sprites.append(icon)
        for icon in icon_sprites:
            self.enemy_icons.add(icon)

        #destroy sprite on collision
        pygame.sprite.spritecollide(self.player_icon.sprite, self.enemy_icons, True)
    def setupTreasureIcons(self):
        icon_sprites = []
        self.treasure_icons = pygame.sprite.Group()
        for location in self.treasure_locations:
            if location in self.cur_adjaceny_list:
                idx = self.cur_adjaceny_list.index(location)
                icon = Icon(self.nodes.sprites()[idx].rect.center, 'yellow')
                icon_sprites.append(icon)
        for icon in icon_sprites:
            self.treasure_icons.add(icon)

        #destroy sprite on collision
        pygame.sprite.spritecollide(self.player_icon.sprite, self.treasure_icons, True)

    def setupNodes(self):
        self.nodes = pygame.sprite.Group()
        for idx, node in enumerate(locations.values()):
            if self.current_location == idx:
                adjacency_list = node['unlock']
                self.cur_adjaceny_list = adjacency_list
        for node in adjacency_list:
            node_sprite = Node(locations[node]['node_pos'], 'available', self.speed)
            self.nodes.add(node_sprite)

    def drawPaths(self):
        line_width = 6
        #points = [node['node_pos'] for idx, node in enumerate(locations.values())]
        self.current_point = locations[self.current_location]['node_pos']
        points = [node.getPos() for node in self.nodes if node.status == 'available']
        for point in points:
            pygame.draw.lines(self.display_surface, 'white', False, (self.current_point, point), line_width)

    def input(self):
        keys = pygame.key.get_pressed()
        location_data = locations[self.current_location]
        new_max_location = location_data['unlock']



        #collide with enemy
        if pygame.sprite.spritecollide(self.player_icon.sprite, self.enemy_icons, True):
            self.enemy_locations.remove(self.current_location)
            self.create_location(self.current_location, self.enemy_icons, self.enemy_locations, self.treasure_locations)

        #collide with treasure
        if pygame.sprite.spritecollide(self.player_icon.sprite, self.treasure_icons, True):
            self.treasure_locations.remove(self.current_location)
            print("You received a treasure!")
            self.create_location(self.current_location, self.enemy_icons, self.enemy_locations, self.treasure_locations)

        #player_icon movement
        if not self.moving:
            if keys[pygame.K_UP] and self.getNextNode('up') in self.max_location:
                self.visited.append(self.current_location)
                self.move_direction = self.getMovementData(self.getNextNode('up'))
            elif keys[pygame.K_DOWN] and self.getNextNode('down') in self.max_location:
                self.visited.append(self.current_location)
                self.move_direction = self.getMovementData(self.getNextNode('down'))
            elif keys[pygame.K_RIGHT] and self.getNextNode('right') in self.max_location:
                self.visited.append(self.current_location)
                self.move_direction = self.getMovementData(self.getNextNode('right'))
            elif(keys[pygame.K_LEFT]) and self.getNextNode('left') in self.max_location:
                self.visited.append(self.current_location)
                self.move_direction = self.getMovementData(self.getNextNode('left'))

        #update for new location
        self.max_location = new_max_location
        self.setupEnemyIcons()
        self.setupTreasureIcons()


    def getMovementData(self, end_location):
        #get current node
        for idx, location in enumerate(self.cur_adjaceny_list):
            if self.current_location == location:
                idx_of_nodes = idx
        current_node = self.nodes.sprites()[idx_of_nodes]
        start = pygame.math.Vector2(current_node.rect.center)

        #get end node
        for idx, location in enumerate(self.cur_adjaceny_list):
            if end_location == location:
                idx_of_nodes = idx
        end_node = self.nodes.sprites()[idx_of_nodes]
        end = pygame.math.Vector2(end_node.rect.center)

        #move icon
        self.current_location = end_location
        self.moving = True
        return(end - start).normalize()
    def updatePlayerIconPos(self):
        if self.moving and self.move_direction:
            self.player_icon.sprite.pos += self.move_direction * self.speed
            for idx, location in enumerate(self.cur_adjaceny_list):
                if self.current_location == location:
                    idx_of_nodes = idx
            target_node = self.nodes.sprites()[idx_of_nodes]
            if target_node.detection_zone.collidepoint(self.player_icon.sprite.pos):
                self.moving = False
                self.move_direction = pygame.math.Vector2(0,0)
    def run(self):
        self.screen.blit(self.surface, (0, 0))
        self.input()
        self.updatePlayerIconPos()
        self.setupNodes()
        self.drawPaths()
        self.player_icon.update()
        self.nodes.draw(self.display_surface)
        self.enemy_icons.draw(self.display_surface)
        self.player_icon.draw(self.display_surface)
        self.treasure_icons.draw(self.display_surface)
