import os
import random
import pygame as pg
from config import (GRAY, CYAN, WHITE, WINDOW_WIDTH, WINDOW_HEIGHT,
                    FONT, STARTING_LIVES, IMAGE_PATHS)
from objects import *
from state_manager.menu_manager import MenuManager
from state_manager.states import States
from objects.power_item import PowerItem, Laser

# Constants
PADDLE_WIDTH = WINDOW_WIDTH // 5
PADDLE_HEIGHT = WINDOW_HEIGHT // 45
BRICK_WIDTH = 60
BRICK_HEIGHT = 15
X_GAP = 10
Y_GAP = 5
WALL_WIDTH = WINDOW_WIDTH / 50


def create_bricks(rows, columns):
    """Create a brick wall with the specified rows and columns."""
    total_inter_brick_gap = (columns - 1) * X_GAP
    available_brick_width = WINDOW_WIDTH - (2 * WALL_WIDTH) - total_inter_brick_gap
    brick_width = available_brick_width // columns
    total_brick_group_width = (columns * brick_width) + total_inter_brick_gap
    side_gap = (WINDOW_WIDTH - (2 * WALL_WIDTH) - total_brick_group_width) // 2

    brick_group = pg.sprite.Group()
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
    start_color = pg.Color(*start_rgb)
    end_color = pg.Color(*end_rgb)

    for row in range(rows):
        blend = row / max(rows - 1, 1)
        r = int(start_color.r + (end_color.r - start_color.r) * blend)
        g = int(start_color.g + (end_color.g - start_color.g) * blend)
        b = int(start_color.b + (end_color.b - start_color.b) * blend)
        row_color = (r, g, b)

        for col in range(columns):
            brick = Brick(row_color, brick_width, BRICK_HEIGHT)
            brick.rect.x = WALL_WIDTH + side_gap + col * (brick_width + X_GAP)
            brick.rect.y = start_y + row * (BRICK_HEIGHT + Y_GAP)
            brick_group.add(brick)

    return brick_group


class Game(States, MenuManager):
    """Main game state that handles the breakout gameplay with power-ups."""

    def __init__(self):
        States.__init__(self)
        MenuManager.__init__(self)
        self.next = 'end'
        self.game_stats['lives'] = STARTING_LIVES
        self.game_stats['score'] = 0
        self.last_direction = None
        self.ball_launched = False
        self.won = False
        self.persist = {}

        # Power-up related attributes
        self.lasers = pg.sprite.Group()
        self.laser_mode = False
        self.last_laser_time = 0
        self.laser_cooldown = 500  # ms between laser shots
        self.active_effects = []
        self.power_items = pg.sprite.Group()

        # Load background
        try:
            image_path = IMAGE_PATHS["game_bg"]
            self.background = pg.image.load(image_path).convert()
            self.background = pg.transform.scale(self.background, (WINDOW_WIDTH, WINDOW_HEIGHT))
        except Exception as e:
            print("Failed to load background image:", e)
            self.background = pg.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            self.background.fill((WHITE))

        # Initialize sounds and sprites in startup()
        self.sounds = None
        self.all_sprites = None
        self.particles = None
        self.brick_wall = None
        self.ball = None
        self.paddle = None

    def cleanup(self):
        """Prepare data to persist between screens."""
        print("Cleaning up Game state")
        self.persist['score'] = self.game_stats['score']
        self.persist['won'] = self.won
        return self.persist

    def startup(self, persist):
        """Initialize game objects and sounds."""
        print("Starting Game state")
        self.persist = persist if persist is not None else {}

        # Load sounds
        self._load_sounds()

        # Initialize sprite groups
        self.all_sprites = pg.sprite.Group()
        self.particles = pg.sprite.Group()

        # Create game objects
        self.brick_wall = create_bricks(5, 9)
        self.all_sprites.add(self.brick_wall)

        self.ball = Ball((255, 0, 0), radius=10, speed=5, sounds=self.sounds)
        self.all_sprites.add(self.ball)

        self.paddle = Paddle(CYAN, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.paddle.rect.x = (WINDOW_WIDTH - PADDLE_WIDTH) // 2
        self.paddle.rect.y = WINDOW_HEIGHT - 80
        self.all_sprites.add(self.paddle)

        self.ball_launched = False
        self.last_direction = None

    def _load_sounds(self):
        """Load all game sounds."""
        base_path = os.path.dirname(os.path.abspath(__file__))
        sound_path = os.path.join(base_path, "..", "assets", "sounds")

        self.sounds = {
            'brick': pg.mixer.Sound(os.path.join(sound_path, "hit_brick.wav")),
            'paddle': pg.mixer.Sound(os.path.join(sound_path, "hit_paddle.wav")),
            'life_lost': pg.mixer.Sound(os.path.join(sound_path, "lose_life.wav")),
            'game_over': pg.mixer.Sound(os.path.join(sound_path, "game_over.wav")),
            'win': pg.mixer.Sound(os.path.join(sound_path, "win.wav")),
            'wall': pg.mixer.Sound(os.path.join(sound_path, "wall.wav")),
            'power_up': pg.mixer.Sound(os.path.join(sound_path, "power_up.wav")),
            'power_down': pg.mixer.Sound(os.path.join(sound_path, "power_down.wav")),
            'laser_fire': pg.mixer.Sound(os.path.join(sound_path, "laser_fire.wav")),
        }

    def get_event(self, event):
        """Handle input events."""
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                self.last_direction = 'left'
                if not self.ball_launched and not getattr(self.ball, "sticky", False):
                    self.ball.launch()
                    self.ball_launched = True
            elif event.key == pg.K_RIGHT:
                self.last_direction = 'right'
                if not self.ball_launched and not getattr(self.ball, "sticky", False):
                    self.ball.launch()
                    self.ball_launched = True
            elif event.key == pg.K_ESCAPE:
                self.game_stats['lives'] = 0
                self.done = True
                self.sounds['game_over'].play()
            elif event.key == pg.K_b:  # Cheat key
                bricks_remaining = len(self.brick_wall)
                self.game_stats['score'] += 100 * bricks_remaining
                self.brick_wall.empty()
                self.won = True
                self.done = True
                self.sounds['win'].play()
            elif event.key == pg.K_SPACE:
                if not self.ball_launched and getattr(self.ball, "sticky", False):
                    self.ball.launch()
                    self.ball.sticky = False
                    self.ball_launched = True
                elif self.laser_mode:  # Only fire lasers if in laser mode
                    self._fire_lasers()  # New method to handle laser firing
            elif event.key == pg.K_1:
                self._apply_effect_directly('expand')
            elif event.key == pg.K_2:
                self._apply_effect_directly('shrink')
            elif event.key == pg.K_3:
                self._apply_effect_directly('extra_life')
            elif event.key == pg.K_4:
                self._apply_effect_directly('fast_ball')
            elif event.key == pg.K_5:
                self._apply_effect_directly('laser')
            elif event.key == pg.K_6:
                self._apply_effect_directly('sticky')
            elif event.key == pg.K_7:
                self._apply_effect_directly('slow_paddle')
            elif event.key == pg.K_8:
                self._apply_effect_directly('reverse_controls')
        elif event.type == pg.KEYUP:
            if (event.key == pg.K_LEFT and self.last_direction == 'left') or \
                    (event.key == pg.K_RIGHT and self.last_direction == 'right'):
                self.last_direction = None

    def _apply_effect_directly(self, effect):
        """Debug method to apply effects directly with keys."""
        now = pg.time.get_ticks()
        MAX_ACTIVE_EFFECTS = 3

        if len(self.active_effects) >= MAX_ACTIVE_EFFECTS:
            print(f"Cannot apply '{effect}' - maximum number of effects reached")
            return

        if effect == 'expand':
            self.paddle.image = pg.transform.scale(
                self.paddle.image,
                (int(self.paddle.rect.width * 1.5), self.paddle.rect.height)
            )
            self.paddle.rect = self.paddle.image.get_rect(center=self.paddle.rect.center)
        elif effect == 'shrink':
            self.paddle.image = pg.transform.scale(
                self.paddle.image,
                (int(self.paddle.rect.width * 0.5), self.paddle.rect.height)
            )
            self.paddle.rect = self.paddle.image.get_rect(center=self.paddle.rect.center)
        elif effect == 'extra_life':
            self.game_stats['lives'] += 1
        elif effect == 'fast_ball':
            self.ball.dx *= 1.5
            self.ball.dy *= 1.5
        elif effect == 'laser':
            self.laser_mode = True
        elif effect == 'sticky':
            self.ball.sticky = True
        elif effect == 'szlow_paddle':
            self.paddle.slow = True
        elif effect == 'reverse_controls':
            self.paddle.reverse = True

        self.active_effects.append((effect, now + 5000))  # 5 second duration
        sound = 'power_up' if effect in ['expand', 'extra_life', 'laser', 'sticky'] else 'power_down'
        self.sounds[sound].play()

    def update(self, screen, dt):
        """Update game state."""
        # Handle collisions
        self._handle_collisions()

        # Update paddle movement with possible reverse controls
        move_speed = 5 if getattr(self.paddle, 'slow', False) else 8
        if self.last_direction == 'left':
            direction = -1  # Left
        elif self.last_direction == 'right':
            direction = 1  # Right
        else:
            direction = 0

        if direction != 0:
            self.paddle.move(direction, move_speed)

        # Update game objects if game is still running
        if not self.done:
            self.ball.update()
            self.particles.update()
            self.power_items.update()
            self._update_lasers()

            # Check for ball loss
            if self.ball.rect.bottom >= WINDOW_HEIGHT:
                self._handle_ball_loss()

            # Check for win condition
            if len(self.brick_wall) == 0 and not self.done:
                self.won = True
                self.done = True
                self.sounds['win'].play()

            # Update active effects
            self._update_active_effects()
          
            # Keep sticky ball attached to paddle before launch
            if getattr(self.ball, 'sticky', False) and not self.ball_launched:
                self.ball.rect.midbottom = self.paddle.rect.midtop

        # Draw everything
        self.draw(screen)

    def _fire_lasers(self):
        """Fire lasers from paddle when space is pressed in laser mode."""
        now = pg.time.get_ticks()
        if now - self.last_laser_time >= self.laser_cooldown:
            left_laser = Laser(self.paddle.rect.left + 5, self.paddle.rect.top)
            right_laser = Laser(self.paddle.rect.right - 5, self.paddle.rect.top)
            self.lasers.add(left_laser, right_laser)
            self.all_sprites.add(left_laser, right_laser)
            self.last_laser_time = now
            self.sounds['laser_fire'].play()
            
    def _update_lasers(self):
        """Update laser positions and handle collisions."""
        # Update all lasers (this makes them move upward)
        self.lasers.update()

        # Check for laser-brick collisions
        hits = pg.sprite.groupcollide(
            self.lasers,
            self.brick_wall,
            True,  # Remove laser on collision
            True  # Remove brick on collision
        )

        # Handle collisions
        for laser, hit_bricks in hits.items():
            self.game_stats['score'] += 100 * len(hit_bricks)
            for brick in hit_bricks:
                for _ in range(8):
                    self.particles.add(Debris(brick.rect.center, brick.color))
            self.sounds['brick'].play()

    def _update_active_effects(self):
        """Check and remove expired effects."""
        ## Lasers Fire
        current_time = pg.time.get_ticks()
        for effect, end_time in self.active_effects[:]:
            if current_time > end_time:
                self._remove_effect(effect)
                self.active_effects.remove((effect, end_time))

    def _remove_effect(self, effect):
        """Revert an effect when it expires."""
        if effect == 'expand':
            self.paddle.reset_size()
        elif effect == 'shrink':
            self.paddle.reset_size()
        elif effect == 'fast_ball':
            self.ball.reset_speed()
        elif effect == 'laser':
            self.laser_mode = False
        elif effect == 'sticky':
            self.ball.sticky = False
        elif effect == 'slow_paddle':
            self.paddle.slow = False
        elif effect == 'reverse_controls':
            self.paddle.reverse = False

    def _handle_collisions(self):
        """Handle all collision detection and response."""
        # Brick collisions
        hit_bricks = pg.sprite.spritecollide(self.ball, self.brick_wall, False)
        if hit_bricks:
            self.ball.dy *= -1  # Bounce
            for brick in hit_bricks:
                # Create particles
                for _ in range(8):
                    particle = Debris(brick.rect.center, brick.color)
                    self.particles.add(particle)

                # 30% chance to spawn power item
                if random.random() < 0.3:
                    item_type = random.choice([
                        'expand', 'shrink', 'extra_life', 'fast_ball',
                        'laser', 'sticky', 'slow_paddle', 'reverse_controls'
                    ])
                    item = PowerItem(brick.rect.centerx, brick.rect.centery, item_type)
                    self.power_items.add(item)
                    self.all_sprites.add(item)

                # Remove brick and update score
                self.brick_wall.remove(brick)
                self.all_sprites.remove(brick)
                self.game_stats['score'] += 100
            self.sounds['brick'].play()

        # Power item collection
        for item in pg.sprite.spritecollide(self.paddle, self.power_items, True):
            effect = item.apply_effect(self.paddle, self.ball, self)
            if effect:
                self.active_effects.append((effect, pg.time.get_ticks() + 5000))
                sound = 'power_up' if effect in ['expand', 'extra_life', 'laser', 'sticky'] else 'power_down'
                self.sounds[sound].play()

        # Paddle collision
        if pg.sprite.collide_rect(self.ball, self.paddle):
            # Handle sticky ball
            if getattr(self.ball, 'sticky', False):
                self.ball.dx = 0
                self.ball.dy = 0
                self.ball.rect.midbottom = self.paddle.rect.midtop
                self.ball_launched = False
            else:
                self.ball.dy *= -1
                self.sounds['paddle'].play()
                # Add directional influence based on where ball hits paddle
                offset = (self.ball.rect.centerx - self.paddle.rect.centerx) / (self.paddle.rect.width / 2)
                self.ball.dx += offset * 2
                # Cap speed
                max_speed = self.ball.speed
                self.ball.dx = max(-max_speed, min(self.ball.dx, max_speed))

    def _handle_ball_loss(self):
        """Handle logic when ball is lost."""
        self.game_stats['lives'] -= 1
        self.sounds['life_lost'].play()

        if self.game_stats['lives'] <= 0:
            self.done = True
            self.sounds['game_over'].play()
        else:
            self._reset_ball_and_paddle()

    def _reset_ball_and_paddle(self):
        """Reset ball and paddle to starting positions."""
        self.paddle.reset_size()
        self.paddle.rect.x = (WINDOW_WIDTH - PADDLE_WIDTH) // 2
        self.paddle.rect.y = WINDOW_HEIGHT - 80
        self.ball.rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        self.ball.dx = 0
        self.ball.dy = 0
        self.ball_launched = False
        self.last_direction = None
        self.laser_mode = False
        self.active_effects = []

    def draw(self, screen):
        """Draw all game elements."""
        # Draw background and walls
        screen.blit(self.background, (0, 0))
        pg.draw.rect(screen, GRAY, (0, 0, WINDOW_WIDTH, 50))  # Top
        pg.draw.rect(screen, GRAY, (0, 0, WALL_WIDTH, WINDOW_HEIGHT))  # Left
        pg.draw.rect(screen, GRAY, (WINDOW_WIDTH - WALL_WIDTH, 0, WALL_WIDTH, WINDOW_HEIGHT))  # Right

        # Draw all sprites
        self.all_sprites.draw(screen)
        self.particles.draw(screen)

        # Draw HUD
        font = pg.font.SysFont(FONT, 30)
        lives_text = font.render(f"Lives: {self.game_stats['lives']}", True, (0, 0, 0))
        screen.blit(lives_text, (20, 10))

        score_text = font.render(f"Score: {self.game_stats['score']}", True, (0, 0, 0))
        score_rect = score_text.get_rect(topright=(WINDOW_WIDTH - 20, 10))
        screen.blit(score_text, score_rect)

        # Draw active effects
        if self.active_effects:
            effect_font = pg.font.SysFont(FONT, 24)
            y = 18
            spacing = 20

            effect_surfaces = []
            for effect, _ in self.active_effects:
                color = (0, 200, 0) if effect in ['expand', 'extra_life', 'laser', 'sticky'] else (200, 0, 0)
                text = effect.replace('_', ' ').title()
                surface = effect_font.render(text, True, color)
                effect_surfaces.append(surface)

            total_width = sum(s.get_width() for s in effect_surfaces) + spacing * (len(effect_surfaces) - 1)
            start_x = (WINDOW_WIDTH - total_width) // 2

            x = start_x
            for surface in effect_surfaces:
                rect = surface.get_rect(midtop=(x + surface.get_width() // 2, y))
                screen.blit(surface, rect)
                x += surface.get_width() + spacing
