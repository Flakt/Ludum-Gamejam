import random
import os
import math

import pygame as pg
from sprites import *
from pygame.locals import (
    RLEACCEL,
    K_ESCAPE,
    MOUSEBUTTONDOWN,
    KEYDOWN,
    QUIT,
)
vect = pg.math.Vector2

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

BLACK = (0, 0, 0)

PLAYER_LIVES = 5
PLAYER_SPEED = 5

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
        self.load_data()

    def newGame(self):
        global PLAYER_LIVES, PLAYER_SPEED
        self.all_sprites = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.player = Player(PLAYER_LIVES, PLAYER_SPEED)
        self.all_sprites.add(self.player)

    def load_data(self):
        game_folder = os.path.dirname(__file__)
        self.map_data = []

        self.level_cross_img = pg.image.load(os.path.join("level_cross.bmp"))
        # self.level_left_T_img = pg.image.load(os.path.join(game_folder/assets, LEVEL[1]))

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
        self.bullets.update()

        if pg.sprite.spritecollideany(self.player, self.enemies):
            player_enemy_collision(self.player, self.enemies)

        for bullet in self.bullets:
            enemy_hit = pg.sprite.spritecollideany(bullet, self.enemies)
            if enemy_hit is not None:
                bullet.kill()
                enemy_hit.kill()

    def player_shoot(self):
        mouse_x, mouse_y = pg.mouse.get_pos()
        angle = self.get_mouse_angle(mouse_x, mouse_y)
        bullet_vect = vect(1, 0).rotate(-angle)
        new_bullet = Bullet(self.player.pos, bullet_vect, self)
        self.bullets.add(new_bullet)
        self.all_sprites.add(new_bullet)
        # new_bullet = Bullet(self.player.pos, normalized_vect, self)
        # self.bullets.add(new_bullet)
        # self.all_sprites.add(new_bullet)

    def events(self):
        for event in pg.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.quit()
            elif event.type == MOUSEBUTTONDOWN:
                self.player_shoot()
            elif event.type == ADDENEMY:
                self.spawn_enemy()
            elif event.type == QUIT:
                self.quit()

    def draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.level_cross_img, self.level_cross_img.get_rect())

        for entity in self.all_sprites:
            self.screen.blit(entity.surf, entity.rect)

        self.screen.blit(self.player.surf, self.player.rect)

        pg.display.flip()

    def spawn_enemy(self):
        if random.randint(1, 5) == 5:
            new_enemy = Enemy()
            self.enemies.add(new_enemy)
            self.all_sprites.add(new_enemy)

    def get_mouse_angle(self, mouse_x, mouse_y):
        offset = (mouse_y - self.player.rect.centery,
                  mouse_x - self.player.rect.centerx)
        angle = -math.degrees(math.atan2(*offset))
        return angle

def player_enemy_collision(player, enemies):
    if player.lives > 0:
        for enemy in enemies:
            if pg.sprite.collide_rect(player, enemy):
                enemy.kill()
        player.lives -= 1
    else:
        player.kill()
        print("Oh dear, you are dead")
        self.keepGoing = False


g = Game()

while True:
    g.newGame()
    g.run()

pg.quit()
