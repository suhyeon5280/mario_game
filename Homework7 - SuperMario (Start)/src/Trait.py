import random

from pygame.transform import flip
from src.Collider import Collider

class GoTrait:
    def __init__(self, animation, screen, camera, entity):
        self.animation = animation
        self.direction = 0
        self.heading = 1
        self.accel_velocity = 0.4
        self.decrease_velocity = 0.25
        self.max_velocity = 3.0
        self.screen = screen
        self.camera = camera
        self.entity = entity

    def update(self):
        if abs(self.entity.velocity.x) > 3.2:
            self.entity.velocity.x = 3.2 * self.heading
        self.max_velocity = 3.2

        if self.direction != 0:
            self.heading = self.direction
            if self.heading == 1:
                if self.entity.velocity.x < self.max_velocity:
                    self.entity.velocity.x += self.accel_velocity * self.heading
            else:
                if self.entity.velocity.x > -self.max_velocity:
                    self.entity.velocity.x += self.accel_velocity * self.heading

            if not self.entity.in_air:
                self.animation.update()
            else:
                self.animation.in_air()

        else:
            self.animation.update()
            if self.entity.velocity.x >= 0:
                self.entity.velocity.x -= self.decrease_velocity
            else:
                self.entity.velocity.x += self.decrease_velocity
            if int(self.entity.velocity.x) == 0:
                self.entity.velocity.x = 0
                if self.entity.in_air:
                    self.animation.in_air()
                else:
                    self.animation.in_idle()

        self.draw()

    def update_animation(self, animation):
        self.animation = animation
        self.update()

    def draw(self):
        if self.heading == 1:
            self.screen.blit(self.animation.image, self.entity.get_pos())
        elif self.heading == -1:
            self.screen.blit(
                flip(self.animation.image, True, False), self.entity.get_pos()
            )

class JumpTrait:
    def __init__(self, entity):
        self.vertical_speed = -12
        self.jump_height = 120
        self.entity = entity
        self.initial_height = 384
        self.deacceleration_height = (
            self.jump_height 
            - ((self.vertical_speed**2) / (2*self.entity.gravity))
        )

    def jump(self, jump_event):
        if jump_event and self.entity.on_ground:
            self.entity.sound.play_sfx(self.entity.sound.jump)
            self.entity.velocity.y = self.vertical_speed
            self.entity.in_air = True
            self.initial_height = self.entity.rect.y
            self.entity.in_jump = True
            self.entity.obey_gravity = False  # always reach maximum height

        if self.entity.in_jump:
            if (((self.initial_height - self.entity.rect.y) 
                >= self.deacceleration_height) or self.entity.velocity.y == 0):
                self.entity.in_jump = False
                self.entity.obey_gravity = True

    def reset(self):
        self.entity.in_air = False


class BounceTrait:
    def __init__(self, entity):
        self.vel = 5
        self.jump = False
        self.entity = entity

    def update(self):
        if self.jump:
            self.entity.velocity.y = 0
            self.entity.velocity.y -= self.vel
            self.jump = False
            self.entity.in_air = True

    def reset(self):
        self.entity.in_air = False


class LeftRightWalkTrait:
    def __init__(self, entity, map):
        self.direction = random.choice([-1, 1])
        self.entity = entity
        self.collider = Collider(self.entity, map)
        self.speed = 1
        self.entity.velocity.x = self.speed * self.direction

    def update(self):
        if self.entity.velocity.x == 0:
            self.direction *= -1
        self.entity.velocity.x = self.speed * self.direction
        self.move()

    def move(self):
        self.entity.rect.y += self.entity.velocity.y
        self.collider.check_y()
        self.entity.rect.x += self.entity.velocity.x
        self.collider.check_x()