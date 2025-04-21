import pygame as pg

from config import WINDOW_WIDTH

WALL_WIDTH = WINDOW_WIDTH / 50

class Paddle(pg.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.original_width = width
        self.image = pg.Surface((width, height))
        self.original_color = color
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.slow = False
        self.reverse = False

    def reset_size(self):
        self.image = pg.Surface((self.original_width, self.rect.height))
        self.rect = self.image.get_rect(center=self.rect.center)
        self.image.fill(self.original_color)

    def move_left(self, pixels):
        self.rect.x -= pixels
        if self.rect.x < WALL_WIDTH:
            self.rect.x = WALL_WIDTH

    def move_right(self, pixels):
        self.rect.x += pixels
        if self.rect.x > WINDOW_WIDTH - WALL_WIDTH - self.rect.width:
            self.rect.x = WINDOW_WIDTH - WALL_WIDTH - self.rect.width
