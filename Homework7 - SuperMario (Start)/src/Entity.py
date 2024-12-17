import sys
import pygame

from src.Math import Vec2D
from src.Animation import Animation
from src.Camera import Camera
from src.Collider import Collider
from src.EntityCollider import EntityCollider
from src.EventHandler import get_event_handler
from src.Trait import GoTrait, JumpTrait, BounceTrait, LeftRightWalkTrait


class Entity(object):
    def __init__(self, x, y, gravity):
        self.velocity = Vec2D()
        self.rect = pygame.Rect(x * 32, y * 32, 32, 32)
        self.gravity = gravity
        self.traits = None
        self.alive = True
        self.active = True
        self.bouncing = False
        self.time_after_death = 3
        self.timer = 0
        self.type = ''
        self.on_ground = False
        self.obey_gravity = True
        
    def apply_gravity(self):
        if self.obey_gravity:
            self.velocity.y += self.gravity

    def update_traits(self):
        for trait in self.traits.values():
            if isinstance(trait, (GoTrait, BounceTrait, LeftRightWalkTrait)):
                trait.update()
      
    def get_pos_index(self):
        return Vec2D(self.rect.x // 32, self.rect.y // 32)
    
    def get_pos_index_as_float(self):
        return Vec2D(self.rect.x / 32.0, self.rect.y / 32.0)
    


class Mario(Entity):
    def __init__(self, x, y, world, screen, sound, sprites, gravity=0.8):
        super().__init__(x, y, gravity)
        self.screen = screen
        self.camera = Camera(self.rect, self)
        self.sound = sound
        self.in_air = False
        self.in_jump = False
        self.event_handler = get_event_handler(self)
        self.images = {
            'mario_run1': sprites['mario_run1'].image,
            'mario_run2': sprites['mario_run2'].image,
            'mario_run3': sprites['mario_run3'].image,
            'mario_idle': sprites['mario_idle'].image,
            'mario_jump': sprites['mario_jump'].image,
        }
        self.animation = Animation(
            [
                self.images['mario_run1'],
                self.images['mario_run2'],
                self.images['mario_run3'],
            ],
            self.images['mario_idle'],
            self.images['mario_jump'],
        )
        self.traits = {
            'jump': JumpTrait(self),
            'go': GoTrait(self.animation, screen, self.camera, self),
            'bounce': BounceTrait(self),
        }
        self.world = world
        self.collision = Collider(self, world)
        self.entity_collider = EntityCollider(self)
        self.restart = False

    def update(self):
        self.update_traits()
        self.move()
        self.camera.move()
        self.apply_gravity()
        self.check_entity_collision()
        self.event_handler()

    def move(self):
        self.rect.y += self.velocity.y
        self.collision.check_y()
        self.rect.x += self.velocity.x
        self.collision.check_x()

    def check_entity_collision(self):
        for entity in self.world.entities:
            collision_state = self.entity_collider.check(entity)
            if collision_state.is_colliding:
                if entity.type == 'Mob':
                    self._collision_mob(entity, collision_state)

    def _collision_mob(self, mob, collision_state):
        if collision_state.is_top and mob.alive:
            self.sound.play_sfx(self.sound.stomp)
            self.rect.bottom = mob.rect.top
            self.bounce()
            self.kill_mob(mob)

        elif collision_state.is_colliding and mob.alive:
            self.game_over()
            
    def bounce(self):
        self.traits['bounce'].jump = True

    def kill_mob(self, mob):
        mob.alive = False

    def game_over(self):
        srf = pygame.Surface((640, 480))
        srf.set_colorkey((255, 255, 255), pygame.RLEACCEL)
        srf.set_alpha(128)
        self.sound.music_channel.stop()
        self.sound.music_channel.play(self.sound.death)

        for i in range(800, 20, -1):
            srf.fill((0, 0, 0))
            pygame.draw.circle(
                srf,
                (255, 255, 255),
                (int(self.camera.x + self.rect.x) + 16, self.rect.y + 16),
                i,
            )
            self.screen.blit(srf, (0, 0))
            pygame.display.update()
        
        pygame.quit()
        sys.exit()

    def get_pos(self):
        return self.camera.x + self.rect.x, self.rect.y

    def set_pos(self, x, y):
        self.rect.x = x
        self.rect.y = y


class Goomba(Entity):
    def __init__(self, x, y, screen, sprites, world, sound):
        super().__init__(y, x - 1, 1.25)
        self.world = world
        self.sound = sound
        self.screen = screen
        self.type = 'Mob'
        self.images = {
            'goomba-1': sprites['goomba-1'].image,
            'goomba-2': sprites['goomba-2'].image,
            'goomba-flat': sprites['goomba-flat'].image,
        }
        self.animation = Animation([
            self.images['goomba-1'],
            self.images['goomba-2'],
        ])
        self.left_right_trait = LeftRightWalkTrait(self, world)
        self.collision = Collider(self, world)
        self.entity_collider = EntityCollider(self)

    def update(self, camera):
        if self.alive:
            self.apply_gravity()
            self.draw(camera)
            self.left_right_trait.update()
            self.check_entity_collision()
        else:
            self.on_dead(camera)

    def draw(self, camera):
        self.screen.blit(self.animation.image, (self.rect.x + camera.x, self.rect.y))
        self.animation.update()
 
    def on_dead(self, camera):
        if self.timer < self.time_after_death:
            self.draw_flat(camera)
        else:
            self.alive = None
        self.timer += 0.1

    def draw_flat(self, camera):
        self.screen.blit(
            self.images['goomba-flat'],
            (self.rect.x + camera.x, self.rect.y),
        )

    def check_entity_collision(self):
        for ent in self.world.entities:
            collision_state = self.entity_collider.check(ent)
            if collision_state.is_colliding:
                if ent.type == 'Mob':
                    self._collision_mob(ent, collision_state)

    def _collision_mob(self, mob, collision_state):
        if collision_state.is_colliding and mob.bouncing:
            self.alive = False
            self.sound.play_sfx(self.sound.brick_bump)
