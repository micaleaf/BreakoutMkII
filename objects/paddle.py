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
        direction = -1 if not self.reverse else 1
        self.rect.x += direction * pixels
        self._constrain_to_screen()

    def move_right(self, pixels):
        direction = 1 if not self.reverse else -1
        self.rect.x += direction * pixels
        self._constrain_to_screen()

    def _constrain_to_screen(self):
        if self.rect.x < WALL_WIDTH:
            self.rect.x = WALL_WIDTH
        elif self.rect.right > WINDOW_WIDTH - WALL_WIDTH:
            self.rect.right = WINDOW_WIDTH - WALL_WIDTH
