import pygame as pg
import random

from pygame.locals import (
    K_w,
    K_s,
    K_a,
    K_d
)
vect = pg.math.Vector2

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Player(pg.sprite.Sprite):
    def __init__(self, lives, speed):
        super(Player, self).__init__()
        self.surf = pg.Surface((50, 50))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()
        self.rect.center = (
            random.randint(51, SCREEN_WIDTH - 51),
            random.randint(51, SCREEN_HEIGHT - 51),
        )
        self.pos = self.rect.center
        self.lives = lives
        self.speed = speed

    def update(self, pressed_keys):
        if pressed_keys[K_w]:
            self.rect.move_ip(0, (self.speed) * -1)
        if pressed_keys[K_s]:
            self.rect.move_ip(0, self.speed)
        if pressed_keys[K_a]:
            self.rect.move_ip((self.speed) * -1, 0)
        if pressed_keys[K_d]:
            self.rect.move_ip(self.speed, 0)

        self.pos = self.rect.center

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

class Enemy(pg.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pg.Surface((20, 20))
        self.surf.fill((80,80,80))
        self.rect = self.surf.get_rect(
            center = (
                random.randint(20, SCREEN_WIDTH - 20),
                random.randint(20, SCREEN_HEIGHT - 20),
            )
        )
        self.speed = random.randint(1, 5)

    def update(self):
        if self.rect.left < 0:
            self.kill()
        if self.rect.right > SCREEN_WIDTH:
            self.kill()
        if self.rect.top <= 0:
            self.kill()
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.kill()


class Bullet(pg.sprite.Sprite):
    def __init__(self, pos, direction, game):
        super(Bullet, self).__init__()
        self.surf = pg.Surface((2,2))
        self.surf.fill((255, 0, 0))
        self.rect = self.surf.get_rect()
        self.pos = vect(pos)
        self.rect.center = self.pos
        self.vel = direction * 250
        self.bullet_time = pg.time.get_ticks()
        self.game = game

    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos

        if self.rect.left < 0:
            self.kill()
        if self.rect.right > SCREEN_WIDTH:
            self.kill()
        if self.rect.top <= 0:
            self.kill()
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.kill()
