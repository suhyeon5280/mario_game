import json
import pygame

from src.Animation import Animation

class Sprite:
    def __init__(self, image, colliding, animation=None):
        self.image = image
        self.colliding = colliding
        self.animation = animation

    def draw(self, x, y, screen):
        dimensions = (x * 32, y * 32)
        if self.animation is None:
            screen.blit(self.image, dimensions)
        else:
            self.animation.update()
            screen.blit(self.animation.image, dimensions)


class SpriteSheet:
    def __init__(self, filename):
        self.sheet = pygame.image.load(filename)
        if not self.sheet.get_alpha():
            self.sheet.set_colorkey((0, 0, 0))

    def image_at(self, 
                 x, 
                 y, 
                 scalingfactor, 
                 colorkey=None, 
                 ignore_tile_size=False,
                 x_tile_size=16, 
                 y_tile_size=16):
        
        if ignore_tile_size:
            rect = pygame.Rect(
                (x, y, x_tile_size, y_tile_size))
        else:
            rect = pygame.Rect(
                (x * x_tile_size, y * y_tile_size, x_tile_size, y_tile_size))
        
        image = pygame.Surface(rect.size)
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        image = pygame.transform.scale(
            image, 
            (x_tile_size * scalingfactor, y_tile_size * scalingfactor)
        )
        return image


def load_sprites(filenames):
    sprites = {}
    for filename in filenames.values():
        with open(filename) as file:
            data = json.load(file)
            sprite_sheet = SpriteSheet(data['path'])
            sprite_dict = {}
            if data['type'] == 'background':
                for sprite in data['sprites']:
                    colorkey = None
                    if 'colorkey' in sprite:
                        colorkey = sprite['colorkey']
                    sprite_dict[sprite['name']] = Sprite(
                        sprite_sheet.image_at(
                            sprite['x'],
                            sprite['y'],
                            sprite['scalefactor'],
                            colorkey,
                        ),
                        sprite['collision'],
                        None,
                    )
                sprites.update(sprite_dict)

            elif data['type'] == 'animation':
                for sprite in data['sprites']:
                    images = []
                    for image in sprite['images']:
                        images.append(
                            sprite_sheet.image_at(
                                image['x'],
                                image['y'],
                                image['scale'],
                                colorkey=sprite['colorkey'],
                            )
                        )
                    sprite_dict[sprite['name']] = Sprite(
                        None,
                        None,
                        animation=Animation(images, delta_time=sprite['deltaTime']),
                    )
                sprites.update(sprite_dict)
            
            elif data['type'] == 'character' or data['type'] == 'item':
                for sprite in data['sprites']:
                    colorkey = None
                    if 'colorkey' in sprite:
                        colorkey = sprite['colorkey']
                    x_size, y_size = data['size']
                    sprite_dict[sprite['name']] = Sprite(
                        sprite_sheet.image_at(
                            sprite['x'],
                            sprite['y'],
                            sprite['scalefactor'],
                            colorkey,
                            True,
                            x_tile_size=x_size,
                            y_tile_size=y_size,
                        ),
                        sprite['collision'],
                    )
                sprites.update(sprite_dict)

    return sprites
