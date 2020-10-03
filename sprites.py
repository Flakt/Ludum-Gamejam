import pygame as pg
import random

from pygame.locals import (
    K_w,
    K_s,
    K_a,
    K_d
)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

PLAYER_SPEED = 5

class Player(pg.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pg.Surface((50, 50))
        self.surf.fill((75, 75, 75))
        self.rect = self.surf.get_rect()

    def update(self, pressed_keys):
        if pressed_keys[K_w]:
            self.rect.move_ip(0, (PLAYER_SPEED) * -1)
        if pressed_keys[K_s]:
            self.rect.move_ip(0, PLAYER_SPEED)
        if pressed_keys[K_a]:
            self.rect.move_ip((PLAYER_SPEED) * -1, 0)
        if pressed_keys[K_d]:
            self.rect.move_ip(PLAYER_SPEED, 0)

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
        self.surf.fill((255,0,0))
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
