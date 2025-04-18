import pygame as pg
from BreakoutMkII.code.config import WINDOW_WIDTH
from BreakoutMkII.code.game import WALL_WIDTH

class Paddle(pg.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.image = pg.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()

    def move_left(self, pixels):
        self.rect.x -= pixels
        if self.rect.x < WALL_WIDTH:
            self.rect.x = WALL_WIDTH

    def move_right(self, pixels):
        self.rect.x += pixels
        if self.rect.x > WINDOW_WIDTH - WALL_WIDTH - self.rect.width:
            self.rect.x = WINDOW_WIDTH - WALL_WIDTH - self.rect.width