import pygame


class PowerItem(pygame.sprite.Sprite):
    def __init__(self, x, y, effect_type, speed=3):
        super().__init__()
        self.effect_type = effect_type
        self.image = pygame.Surface((20, 20))
        if effect_type in ['laser', 'expand', 'sticky', 'extra_life']:
            self.image.fill((0, 255, 0))
        else:
            self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed

    def update(self):
        """Standard sprite update method that makes the item fall"""
        self.rect.y += self.speed

    def apply_effect(self, paddle, ball, game=None):
        if self.effect_type == 'expand':
            if not hasattr(paddle, "original_width"):
                paddle.original_width = paddle.rect.width
            paddle.image = pygame.transform.scale(paddle.image, (int(paddle.rect.width * 1.5), paddle.rect.height))
            paddle.rect = paddle.image.get_rect(center=paddle.rect.center)
            return 'expand'

        elif self.effect_type == 'shrink':
            if not hasattr(paddle, "original_width"):
                paddle.original_width = paddle.rect.width
            paddle.image = pygame.transform.scale(paddle.image, (int(paddle.rect.width * 0.6), paddle.rect.height))
            paddle.rect = paddle.image.get_rect(center=paddle.rect.center)
            return 'shrink'

        elif self.effect_type == 'extra_life' and game:
            game.game_stats['lives'] += 1
            return 'extra_life'

        elif self.effect_type == 'fast_ball':
            ball.dx *= 1.8
            ball.dy *= 1.8
            return 'fast_ball'

        elif self.effect_type == 'laser' and game:
            game.laser_mode = True
            return 'laser'

        elif self.effect_type == 'sticky':
            ball.sticky = True
            return 'sticky'

        elif self.effect_type == 'slow_paddle':
            paddle.slow = True
            return 'slow_paddle'

        elif self.effect_type == 'reverse_controls':
            paddle.reverse = True
            return 'reverse_controls'

        return None


class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y, color=(255, 0, 0), speed=10):
        super().__init__()
        self.image = pygame.Surface((4, 12))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()
