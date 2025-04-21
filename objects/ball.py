import random

import pygame as pg

from config import WINDOW_WIDTH, WINDOW_HEIGHT

WALL_WIDTH = WINDOW_WIDTH / 50

class Ball(pg.sprite.Sprite):
    def __init__(self, color, radius, speed, sounds):
        super().__init__()
        self.original_speed = speed
        self.sticky = False
        self.image = pg.Surface((radius * 2, radius * 2), pg.SRCALPHA)
        pg.draw.circle(self.image, color, (radius, radius), radius)
        self.rect = self.image.get_rect()
        self.rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        self.speed = speed
        self.dx = 0
        self.dy = 0
        self.sounds = sounds

    def launch(self):
        self.dy = -self.speed
        self.dx = random.uniform(-1.0, 1.0) * self.speed

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

        # Wall collisions
        if self.rect.left <= WALL_WIDTH or self.rect.right >= WINDOW_WIDTH - WALL_WIDTH:
            self.dx *= -1
            if self.sounds:
                self.sounds['wall'].play()

        if self.rect.top <= 50:  # Top boundary
            self.dy *= -1
            if self.sounds:
                self.sounds['wall'].play()
    def reset_speed(self):
        self.dx = self.original_speed * (abs(self.dx)/self.dx if self.dx != 0 else 1)
        self.dy = self.original_speed * (abs(self.dy)/self.dy if self.dy != 0 else 1)