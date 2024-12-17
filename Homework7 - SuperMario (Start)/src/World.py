import json
import pygame

from src.Entity import Goomba


class Tile:
    def __init__(self, sprite, rect):
        self.sprite = sprite
        self.rect = rect

    def draw(self, screen):
        pygame.draw.rect(screen, pygame.Color(255, 0, 0), self.rect, 1)


class World:
    def __init__(self, screen, sound, sprites, filename):
        self.sprites = sprites
        self.sound = sound
        self.screen = screen
        self.entities = []
        self.load_map(filename)
        
    def load_map(self, filename):
        with open(filename) as file:
            data = json.load(file)
            self.load_layers(data)
            self.load_objects(data)
            self.load_entities(data)
            self.map_length = data['length']

    def load_layers(self, data):
        layers = []
        map_x_min, map_x_max = data['layers']['sky']['x']
        sky_y_min, sky_y_max = data['layers']['sky']['y']
        ground_y_min, ground_y_max = data['layers']['ground']['y']
        for x in range(map_x_min, map_x_max):
            layer = []
            for y in range(sky_y_min, sky_y_max):
                layer.append(Tile(self.sprites['sky'], None))
            for y in range(ground_y_min, ground_y_max):
                layer.append(Tile(
                    self.sprites['ground'], 
                    pygame.Rect(x * 32, (y - 1) * 32, 32, 32),
                ))
            layers.append(layer)
        self.map = list(map(list, zip(*layers)))

    def load_objects(self, data):
        if 'bush' in data['objects']:
            for x, y in data['objects']['bush']:
                self.add_bush_sprite(x, y)

        if 'cloud' in data['objects']:
            for x, y in data['objects']['cloud']:
                self.add_cloud_sprite(x, y)

        if 'pipe' in data['objects']:
            for x, y, z in data['objects']['pipe']:
                self.add_pipe_sprite(x, y, z)

        if 'sky' in data['objects']:
            for x, y in data['objects']['sky']:
                self.map[y][x] = Tile(self.sprites['sky'], None)

        if 'ground' in data['objects']:                
            for x, y in data['objects']['ground']:
                self.map[y][x] = Tile(
                    self.sprites['ground'],
                    pygame.Rect(x * 32, y * 32, 32, 32),
                )

    def load_entities(self, data):
        for x, y in data["entities"]["Goomba"]:
            self.add_goomba(x, y)

    def update_entities(self, camera):
        for entity in self.entities:
            entity.update(camera)
            if entity.alive is None:
                self.entities.remove(entity)

    def draw(self, camera):
        for y in range(0, 15):
            for x in range(0 - int(camera.pos.x + 1), 20 - int(camera.pos.x - 1)):
                if self.map[y][x].sprite is not None:
                    self.screen.blit(
                        self.sprites['sky'].image,
                        ((x + camera.pos.x) * 32, y * 32),
                    )
                    self.map[y][x].sprite.draw(x + camera.pos.x, y, self.screen)
        self.update_entities(camera)

    def add_cloud_sprite(self, x, y):
        for i in range(2):
            for j in range(3):
                self.map[y+i][x+j] = Tile(
                    self.sprites[f'cloud_{i+1}_{j+1}'], None,
                )

    def add_pipe_sprite(self, x, y, length=2):
        # add pipe head
        self.map[y][x] = Tile(
            self.sprites['pipe_1_1'],
            pygame.Rect(x * 32, y * 32, 32, 32),
        )
        self.map[y][x+1] = Tile(
            self.sprites['pipe_1_2'],
            pygame.Rect((x + 1) * 32, y * 32, 32, 32),
        )

        # add pipe body
        for i in range(1, length + 20):
            if y+i >= len(self.map):
                break
            self.map[y+i][x] = Tile(
                self.sprites['pipe_2_1'],
                pygame.Rect(x * 32, (y + i) * 32, 32, 32),
            )
            self.map[y+i][x+1] = Tile(
                self.sprites['pipe_2_2'],
                pygame.Rect((x + 1) * 32, (y + i) * 32, 32, 32),
            )

    def add_bush_sprite(self, x, y):
        self.map[y][x] = Tile(self.sprites['bush_1'], None)
        self.map[y][x+1] = Tile(self.sprites['bush_2'], None)
        self.map[y][x+2] = Tile(self.sprites['bush_3'], None)

    def add_goomba(self, x, y):
        self.entities.append(
            Goomba(x, y, self.screen, self.sprites, self, self.sound)
        )