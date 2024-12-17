import pygame

from src.World import World
from src.Entity import Mario
from src.Sound import Sound
from src.Sprite import load_sprites
from config import *


def main():
    pygame.mixer.pre_init(44100, -16, 2, 4096)
    pygame.init()
    screen = pygame.display.set_mode(GAME_WINDOW_SIZE)
    clock = pygame.time.Clock()
    
    sound = Sound(RESOUECE_SOUND)
    sound.music_channel.play(sound.main_theme, loops=-1)
    sprites = load_sprites(RESOUECE_SPRITE)
    world = World(screen, sound, sprites, RESOUECE_WORLD)
    mario = Mario(0, 0, world, screen, sound, sprites)
    
    while True:
        world.draw(mario.camera)
        mario.update()
        pygame.display.update()
        clock.tick(GAME_FPS)

if __name__ == '__main__':
    main()
