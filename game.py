import random
import os

import pygame as pg
from pygame.locals import (
    RLEACCEL,
    K_w,
    K_a,
    K_s,
    K_d,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

PLAYER_SPEED = 5
PLAYER_LIVES = 5

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


def spawn_enemy():
    if random.randint(1, 5) == 5:
        new_enemy = Enemy()
        enemies.add(new_enemy)
        all_sprites.add(new_enemy)

def player_enemy_collision(player, enemies):
    global PLAYER_LIVES
    global running
    if PLAYER_LIVES > 0:
        for enemy in enemies:
            if pg.sprite.collide_rect(player, enemy):
                enemy.kill()
        PLAYER_LIVES -= 1
    else:
        player.kill()
        print("Oh dear, you are dead")
        running = False

def update_all_sprites():
    global enemies
    global all_sprites
    global player

    pressed_keys = pg.key.get_pressed()
    player.update(pressed_keys)

    enemies.update()

pg.init()

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

ADDENEMY = pg.USEREVENT + 1
pg.time.set_timer(ADDENEMY, 250)

player = Player()

enemies = pg.sprite.Group()
all_sprites = pg.sprite.Group()
all_sprites.add(player)

running = True
clock = pg.time.Clock()
while running:
    for event in pg.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == ADDENEMY:
            spawn_enemy()
        elif event.type == QUIT:
            running = False

    update_all_sprites()

    screen.fill((0, 0, 0))

    surf = pg.Surface((50, 50))

    surf.fill((255, 255, 255))
    rect = surf.get_rect()

    surf_center = (
        (SCREEN_WIDTH - surf.get_width()) / 2,
        (SCREEN_HEIGHT - surf.get_height()) / 2
    )

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    if pg.sprite.spritecollideany(player, enemies):
        player_enemy_collision(player, enemies)

    pg.display.flip()

    clock.tick(60)

pg.quit()
