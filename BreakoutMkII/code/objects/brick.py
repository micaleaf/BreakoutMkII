import pygame as pg
class Brick(pg.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.color = color  # Store color for debris
        self.image = pg.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()