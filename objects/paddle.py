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
        ## Reset Color
        self.image.fill(self.original_color)

    def move(self, direction, speed):
        """Move paddle with direction (-1=left, 1=right) and speed"""
        if self.reverse:
            direction *= -1  # Flip direction if reversed

        self.rect.x += direction * speed
        # Boundary checking
        if self.rect.left < WALL_WIDTH:
            self.rect.left = WALL_WIDTH
        if self.rect.right > WINDOW_WIDTH - WALL_WIDTH:
            self.rect.right = WINDOW_WIDTH - WALL_WIDTH