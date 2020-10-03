import random
import os

import pygame as pg
from sprites import *
from pygame.locals import (
    RLEACCEL,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

PLAYER_SPEED = 5
PLAYER_LIVES = 5

FPS = 60

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

    clock.tick(FPS)

pg.quit()
