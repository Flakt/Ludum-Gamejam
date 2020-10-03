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

BLACK = (0, 0, 0)

PLAYER_SPEED = 5
PLAYER_LIVES = 5

ADDENEMY = pg.USEREVENT + 1

FPS = 60

class Game():
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption("Ludum Gamejam")
        self.clock = pg.time.Clock()
        self.start_ticks = pg.time.get_ticks()
        self.font = pg.font.Font(None, 54)
        self.font_color = pg.Color('springgreen')

        pg.key.set_repeat(500, 100)

    def newGame(self):
        self.all_sprites = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.player = Player()
        self.all_sprites.add(self.player)

    def run(self):
        global ADDENEMY
        self.keepGoing = True
        pg.time.set_timer(ADDENEMY, 250)

        while self.keepGoing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()

    def update(self):
        pressed_keys = pg.key.get_pressed()
        self.player.update(pressed_keys)

        self.enemies.update()
        if pg.sprite.spritecollideany(self.player, self.enemies):
            player_enemy_collision(self.player, self.enemies)


    def events(self):
        for event in pg.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.quit()
            elif event.type == ADDENEMY:
                spawn_enemy(self)
            elif event.type == QUIT:
                self.quit()

    def draw(self):
        self.screen.fill(BLACK)

        for entity in self.all_sprites:
            self.screen.blit(entity.surf, entity.rect)

        pg.display.flip()

def spawn_enemy(game):
    if random.randint(1, 5) == 5:
        new_enemy = Enemy()
        game.enemies.add(new_enemy)
        game.all_sprites.add(new_enemy)

def player_enemy_collision(player, enemies):
    global PLAYER_LIVES
    if PLAYER_LIVES > 0:
        for enemy in enemies:
            if pg.sprite.collide_rect(player, enemy):
                enemy.kill()
        PLAYER_LIVES -= 1
    else:
        player.kill()
        print("Oh dear, you are dead")
        self.keepGoing = False


g = Game()

while True:
    g.newGame()
    g.run()

pg.quit()
