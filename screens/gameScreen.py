import pygame
import random

pygame.init()
from config import WINDOW_HEIGHT, WINDOW_WIDTH, BLACK, GRAY, WHITE, SETTINGS



window_size = (WINDOW_WIDTH, WINDOW_HEIGHT)

screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Group 3 Breakout Game")
clock = pygame.time.Clock()
FPS = SETTINGS['FPS']

# Colors
CYAN = (0, 255, 255)

paddle_width = WINDOW_WIDTH / 5
paddle_height = WINDOW_HEIGHT / 45

all_sprites_list = pygame.sprite.Group()



brick_width = 60
brick_height = 15
x_gap = 10
y_gap = 5
wall_width = 16
# Paddle


class Paddle(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.slow = False
        self.reverse = False

    def move_left(self, pixels):
        if getattr(self, 'reverse', False):
            pixels = -pixels
        if getattr(self, 'slow', False):
            pixels = pixels // 2
        self.rect.x -= pixels
        if self.rect.left < wall_width:
            self.rect.left = wall_width
        if self.rect.right > WINDOW_WIDTH - wall_width:
            self.rect.right = WINDOW_WIDTH - wall_width

    def move_right(self, pixels):
        if getattr(self, 'reverse', False):
            pixels = -pixels
        if getattr(self, 'slow', False):
            pixels = pixels // 2
        self.rect.x += pixels
        if self.rect.left < wall_width:
            self.rect.left = wall_width
        if self.rect.right > WINDOW_WIDTH - wall_width:
            self.rect.right = WINDOW_WIDTH - wall_width

    def reset_size(self):
        self.image = pygame.Surface((self.original_width, self.rect.height))
        self.image.fill((0, 255, 255))
        self.rect = self.image.get_rect(center=self.rect.center)


paddle = Paddle(CYAN, paddle_width, paddle_height)
paddle.rect.x = int((WINDOW_WIDTH - paddle_width) / 2)
paddle.rect.y = WINDOW_HEIGHT - 80

class Brick(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.color = color  # Store color for debris
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()


def create_bricks(rows, columns):
    total_inter_brick_gap = (columns - 1) * x_gap
    available_brick_width = WINDOW_WIDTH - (2 * wall_width) - total_inter_brick_gap
    brick_width = available_brick_width // columns
    total_brick_group_width = (columns * brick_width) + total_inter_brick_gap
    side_gap = (WINDOW_WIDTH - (2 * wall_width) - total_brick_group_width) // 2

    brick_group = pygame.sprite.Group()
    start_y = 100

    # Predefined contrasting dark color pairs
    color_pairs = [
        ((120, 30, 30), (30, 30, 150)),  # red → blue
        ((30, 120, 30), (140, 30, 140)),  # green → violet
        ((80, 80, 180), (180, 120, 60)),  # blue → gold
        ((60, 60, 60), (160, 0, 160)),  # gray → magenta
    ]

    # Pick one contrasting pair
    start_rgb, end_rgb = random.choice(color_pairs)
    start_color = pygame.Color(*start_rgb)
    end_color = pygame.Color(*end_rgb)

    for row in range(rows):
        blend = row / max(rows - 1, 1)
        r = int(start_color.r + (end_color.r - start_color.r) * blend)
        g = int(start_color.g + (end_color.g - start_color.g) * blend)
        b = int(start_color.b + (end_color.b - start_color.b) * blend)
        row_color = (r, g, b)

        for col in range(columns):
            brick = Brick(row_color, brick_width, brick_height)
            brick.rect.x = wall_width + side_gap + col * (brick_width + x_gap)
            brick.rect.y = start_y + row * (brick_height + y_gap)
            all_sprites_list.add(brick)
            brick_group.add(brick)

    return brick_group


# Create bricks (5 rows, 9 columns fits better)
brick_wall = create_bricks(5, 9)

class Ball(pygame.sprite.Sprite):
    def __init__(self, color, radius, speed, sounds=None):
        super().__init__()
        self.image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (radius, radius), radius)
        self.rect = self.image.get_rect()
        self.rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

        self.speed = speed
        self.original_speed = speed
        self.dx = 0
        self.dy = 0
        self.sounds = sounds

    def launch(self):
        self.dy = -self.speed  # Always go upward
        self.dx = random.uniform(-1.0, 1.0) * self.speed  # Random left or right
        print(f"Ball launched! dx: {self.dx}, dy: {self.dy}")

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

        # Side walls Collison
        if self.rect.left <= wall_width or self.rect.right >= WINDOW_WIDTH - wall_width:
            self.dx *= -1
            if self.sounds and 'wall' in self.sounds:
                self.sounds['wall'].play()

        # Top Wall Collision
        if self.rect.top <= 50:
            self.dy *= -1
            if self.sounds and 'wall' in self.sounds:
                self.sounds['wall'].play()


class Debris(pygame.sprite.Sprite):
    def __init__(self, position, color):
        super().__init__()
        self.image = pygame.Surface((4, 4), pygame.SRCALPHA)
        self.image.fill(color)
        self.rect = self.image.get_rect(center=position)
        self.velocity = [random.uniform(-2, 2), random.uniform(-3, -1)]
        self.gravity = 0.1
        self.life = 30  # frames

    def update(self):
        self.velocity[1] += self.gravity
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        self.life -= 1
        if self.life <= 0:
            self.kill()

def main():
    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        all_sprites_list.update()

        # Drawing
        screen.fill(WHITE)
        # Draw walls
        pygame.draw.line(screen, GRAY, [0, 20], [WINDOW_WIDTH, 20], 50)
        pygame.draw.line(screen, GRAY, [(wall_width / 2) - 1, 0],
                         [(wall_width / 2) - 1, WINDOW_HEIGHT], wall_width)
        pygame.draw.line(screen, GRAY, [(WINDOW_WIDTH - wall_width / 2) - 1, 0],
                         [(WINDOW_WIDTH - wall_width / 2) - 1, WINDOW_HEIGHT], wall_width)

        all_sprites_list.draw(screen)
        pygame.display.update()



    pygame.quit()

