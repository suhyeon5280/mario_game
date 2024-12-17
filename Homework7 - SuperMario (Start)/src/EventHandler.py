import sys
import pygame

from pygame.locals import *

def get_event_handler(entity):
    def event_handler():
        events = pygame.event.get()
        handle_keyboard_event(entity)
        handle_quit_event(events)
    return event_handler


def handle_keyboard_event(entity):
    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[K_LEFT] and not pressed_keys[K_RIGHT]:
        entity.traits['go'].direction = -1
    elif pressed_keys[K_RIGHT] and not pressed_keys[K_LEFT]:
        entity.traits['go'].direction = 1
    else:
        entity.traits['go'].direction = 0
    
    jump_event = pressed_keys[K_SPACE]
    entity.traits['jump'].jump(jump_event)


def handle_quit_event(events):
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()