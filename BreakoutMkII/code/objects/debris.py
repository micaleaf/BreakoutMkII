import pygame as pg
import random

class Debris(pg.sprite.Sprite):
    def __init__(self, position, color):
        super().__init__()
        self.image = pg.Surface((4, 4), pg.SRCALPHA)
        self.image.fill(color)
        self.rect = self.image.get_rect(center=position)
        self.velocity = [random.uniform(-2, 2), random.uniform(-3, -1)]
        self.gravity = 0.1
        self.life = 30

    def update(self):
        self.velocity[1] += self.gravity
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        self.life -= 1
        if self.life <= 0:
            self.kill()
