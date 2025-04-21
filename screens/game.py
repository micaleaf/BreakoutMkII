import pygame as pg
import os
pg.mixer.init()
from state_manager.states import States
from config import GRAY, WHITE, FONT, STARTING_LIVES, WINDOW_HEIGHT, WINDOW_WIDTH
from screens.gameScreen import create_bricks, Paddle, paddle_width, paddle_height, Ball, Debris
import random
from objects.power_item import PowerItem, Laser

wall_width = 16

class Game(States):
    def __init__(self):
        States.__init__(self)
        self.next = 'end'
        self.game_stats['lives'] = STARTING_LIVES
        self.game_stats['score'] = 0
        self.last_direction = None
        self.persist = {}
        self.ball_launched = False
        self.won = False

        self.lasers = pg.sprite.Group()
        self.laser_mode = False
        self.last_laser_time = 0
        self.laser_cooldown = 500

        self.active_effects = []
        self.power_items = pg.sprite.Group()
        self.particles = pg.sprite.Group()

        base_path = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.abspath(os.path.join(base_path, "..", "assets/images", "BG.jpg"))
        try:
            print("Loading game background image from:", image_path)
            self.background = pg.image.load(image_path).convert()
            self.background = pg.transform.scale(self.background, (WINDOW_WIDTH, WINDOW_HEIGHT))
        except Exception as e:
            print("Game background image failed to load:", e)
            self.background = pg.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            self.background.fill(WHITE)

    def cleanup(self):
        print("Cleaning Up Game")
        self.persist['score'] = self.game_stats['score']
        self.persist['won'] = self.won
        return self.persist

    def startup(self, persist):
        print("Starting Up Game")
        base_path = os.path.dirname(os.path.abspath(__file__))
        sound_path = lambda name: os.path.join(base_path, "..", "assets", "sounds", name)

        self.sounds = {
            'brick': pg.mixer.Sound(sound_path("hit_brick.wav")),
            'paddle': pg.mixer.Sound(sound_path("hit_paddle.wav")),
            'life_lost': pg.mixer.Sound(sound_path("lose_life.wav")),
            'game_over': pg.mixer.Sound(sound_path("game_over.wav")),
            'win': pg.mixer.Sound(sound_path("win.wav")),
            'wall': pg.mixer.Sound(sound_path("wall.wav")),
            'laser_fire': pg.mixer.Sound(sound_path("laser_fire.wav")),
            'power_up': pg.mixer.Sound(sound_path("power_up.wav")),
            'power_down': pg.mixer.Sound(sound_path("power_down.wav")),
        }

        self.persist = persist if persist is not None else {}
        self.all_sprites = pg.sprite.Group()
        self.brick_wall = create_bricks(5, 9)
        for brick in self.brick_wall:
            self.all_sprites.add(brick)

        self.ball = Ball((255, 0, 0), radius=10, speed=5, sounds=self.sounds)
        self.all_sprites.add(self.ball)

        self.paddle = Paddle((0, 255, 255), paddle_width, paddle_height)
        self.paddle.rect.x = (WINDOW_WIDTH - paddle_width) // 2
        self.paddle.rect.y = WINDOW_HEIGHT - 80
        self.ball_launched = False
        self.last_direction = None
        self.all_sprites.add(self.paddle)

    def get_event(self, event):
        if event.type == pg.KEYDOWN:
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
            elif event.key == pg.K_b:
                self.game_stats['score'] += 100 * len(self.brick_wall)
                self.brick_wall.empty()
                self.won = True
                self.done = True
                self.sounds['win'].play()
            elif event.key == pg.K_SPACE and not self.ball_launched:
                if hasattr(self.ball, "sticky") and self.ball.sticky:
                    self.ball.dx = 0
                    self.ball.dy = -self.ball.speed
                    print("Sticky ball launched straight up (space)")
                    self.ball.sticky = False
                else:
                    self.ball.launch()
                self.ball_launched = True
            elif event.key == pg.K_1:
                self.apply_effect_directly('expand')
            elif event.key == pg.K_2:
                self.apply_effect_directly('shrink')
            elif event.key == pg.K_3:
                self.apply_effect_directly('extra_life')
            elif event.key == pg.K_4:
                self.apply_effect_directly('fast_ball')
            elif event.key == pg.K_5:
                self.apply_effect_directly('laser')
            elif event.key == pg.K_6:
                self.apply_effect_directly('sticky')
            elif event.key == pg.K_7:
                self.apply_effect_directly('slow_paddle')
            elif event.key == pg.K_8:
                self.apply_effect_directly('reverse_controls')
        elif event.type == pg.KEYUP:
            if (event.key == pg.K_LEFT and self.last_direction == 'left') or \
               (event.key == pg.K_RIGHT and self.last_direction == 'right'):
                self.last_direction = None


    def update(self, screen, dt):
        hit_bricks = pg.sprite.spritecollide(self.ball, self.brick_wall, dokill=False)
        if hit_bricks:
            self.ball.dy *= -1

            for brick in hit_bricks:
                # Spawn particle debris
                for _ in range(8):
                    self.particles.add(Debris(brick.rect.center, brick.color))

                # Remove brick and update score
                self.brick_wall.remove(brick)
                self.all_sprites.remove(brick)
                self.game_stats['score'] += 100

                # 30% chance to spawn a power item
                roll = random.random()
                print(f"Random roll: {roll:.2f}")  # Print the roll result

                if roll < 0.3:
                    item_type = random.choice([
                        'expand', 'shrink', 'extra_life', 'fast_ball', 'laser',
                        'sticky', 'slow_paddle', 'reverse_controls'
                    ])
                    print(f"Spawning power item: {item_type}")
                    item = PowerItem(brick.rect.centerx, brick.rect.centery, item_type)
                    self.power_items.add(item)
                    self.all_sprites.add(item)
                else:
                    print("No power item spawned.")


            self.sounds['brick'].play()

        if pg.sprite.collide_rect(self.ball, self.paddle):
            if hasattr(self.ball, "sticky") and self.ball.sticky:
                self.ball.dx = 0
                self.ball.dy = 0
                self.ball.offset_x = self.ball.rect.centerx - self.paddle.rect.x  # NEW: save where it hit
                self.ball.rect.bottom = self.paddle.rect.top
                self.ball_launched = False
            else:
                self.ball.dy *= -1
                self.sounds['paddle'].play()
                offset = (self.ball.rect.centerx - self.paddle.rect.centerx) / (self.paddle.rect.width / 2)
                self.ball.dx += offset * 2
                self.ball.dx = max(-self.ball.speed, min(self.ball.dx, self.ball.speed))

        if self.last_direction == 'left':
            self.paddle.move_left(8)
        elif self.last_direction == 'right':
            self.paddle.move_right(8)

        # If sticky and ball is stuck to paddle, move ball with paddle
        if getattr(self.ball, "sticky", False) and not self.ball_launched:
            if hasattr(self.ball, "offset_x"):
                self.ball.rect.centerx = self.paddle.rect.x + self.ball.offset_x
            self.ball.rect.bottom = self.paddle.rect.top

        if self.laser_mode:
            now = pg.time.get_ticks()
            if now - self.last_laser_time >= self.laser_cooldown:
                left_x = self.paddle.rect.left + 5
                right_x = self.paddle.rect.right - 5
                y = self.paddle.rect.top

                left_laser = Laser(left_x, y)
                right_laser = Laser(right_x, y)

                self.lasers.add(left_laser, right_laser)
                self.all_sprites.add(left_laser, right_laser)
                self.last_laser_time = now

                self.sounds['laser_fire'].play()

        if not self.done:
            self.ball.update()

        self.particles.update()
        self.lasers.update()

        for laser in self.lasers:
            hits = pg.sprite.spritecollide(laser, self.brick_wall, dokill=True)
            if hits:
                laser.kill()
                self.all_sprites.remove(laser)
                self.lasers.remove(laser)
                self.game_stats['score'] += 100 * len(hits)
                for brick in hits:
                    for _ in range(8):
                        self.particles.add(Debris(brick.rect.center, brick.color))
                self.sounds['brick'].play()

        if self.ball.rect.bottom >= WINDOW_HEIGHT:
            self.game_stats['lives'] -= 1
            print("Ball lost! Lives left:", self.game_stats['lives'])
            self.sounds['life_lost'].play()
            if self.game_stats['lives'] <= 0:
                self.done = True
                self.sounds['game_over'].play()
            else:
                self.reset_ball_and_paddle()

        if len(self.brick_wall) == 0 and not self.done:
            self.won = True
            self.done = True
            self.sounds['win'].play()

        for item in self.power_items:
            item.move()

            if item.rect.colliderect(self.paddle.rect):
                effect = item.apply_effect(self.paddle, self.ball, self)
                if effect:
                    # Add timed effect
                    print(f"Collected effect: {effect}")
                    self.active_effects.append((effect, pg.time.get_ticks() + 5000))

                    # Play appropriate sound
                    if effect in ['expand', 'extra_life', 'laser', 'sticky']:
                        self.sounds['power_up'].play()
                        print("Playing power up sound")
                    else:  # 'shrink', 'slow_paddle', 'reverse_controls', 'fast_ball'
                        self.sounds['power_down'].play()
                        print("Playing power down sound")

                item.kill()

        current_time = pg.time.get_ticks()
        for effect, end_time in self.active_effects[:]:
            if current_time > end_time:
                print(f"Effect expired: {effect}")
                if effect in ['expand', 'shrink']:
                    width = getattr(self.paddle, "original_width", paddle_width)
                    self.paddle.image = pg.Surface((width, paddle_height))
                    self.paddle.image.fill((0, 255, 255))
                    self.paddle.rect = self.paddle.image.get_rect(center=self.paddle.rect.center)
                elif effect == 'fast_ball':
                    direction_x = 1 if self.ball.dx >= 0 else -1
                    direction_y = 1 if self.ball.dy >= 0 else -1
                    self.ball.dx = direction_x * self.ball.original_speed
                    self.ball.dy = direction_y * self.ball.original_speed
                elif effect == 'laser':
                    self.laser_mode = False
                elif effect == 'slow_paddle':
                    self.paddle.slow = False
                elif effect == 'reverse_controls':
                    self.paddle.reverse = False

                self.active_effects.remove((effect, end_time))


        self.draw(screen)

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        pg.draw.rect(screen, GRAY, (0, 0, WINDOW_WIDTH, 50))
        pg.draw.rect(screen, GRAY, (0, 0, wall_width, WINDOW_HEIGHT))
        pg.draw.rect(screen, GRAY, (WINDOW_WIDTH - wall_width, 0, wall_width, WINDOW_HEIGHT))
        self.all_sprites.draw(screen)
        self.particles.draw(screen)
        font = pg.font.SysFont(FONT, 30)
        lives_text = font.render(f"Lives: {self.game_stats['lives']}", True, (0, 0, 0))
        screen.blit(lives_text, (20, 10))
        score_text = font.render(f"Score: {self.game_stats['score']}", True, (0, 0, 0))
        screen.blit(score_text, score_text.get_rect(topright=(WINDOW_WIDTH - 20, 10)))

        # Draw active effects in the top gray bar (centered, left-to-right spacing)
        if self.active_effects:
            banner_font = pg.font.SysFont(FONT, 24)
            y = 18
            spacing = 20

            effect_surfaces = []
            for effect, _ in self.active_effects:
                color = (0, 200, 0) if effect in ['expand', 'extra_life', 'laser', 'sticky'] else (200, 0, 0)
                text = effect.replace('_', ' ').title()
                surface = banner_font.render(text, True, color)
                effect_surfaces.append(surface)

            total_width = sum(s.get_width() for s in effect_surfaces) + spacing * (len(effect_surfaces) - 1)
            start_x = (WINDOW_WIDTH - total_width) // 2

            x = start_x
            for surface in effect_surfaces:
                rect = surface.get_rect(midtop=(x + surface.get_width() // 2, y))
                screen.blit(surface, rect)
                x += surface.get_width() + spacing

    def reset_ball_and_paddle(self):
        self.paddle.rect.x = (WINDOW_WIDTH - paddle_width) // 2
        self.paddle.rect.y = WINDOW_HEIGHT - 80
        self.ball.rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        self.ball.dx = 0
        self.ball.dy = 0
        self.ball_launched = False
        self.last_direction = None

    def apply_effect_directly(self, effect):
        now = pg.time.get_ticks()
        MAX_ACTIVE_EFFECTS = 3

        if len(self.active_effects) >= MAX_ACTIVE_EFFECTS:
            print(f"Cannot apply '{effect}' — maximum number of effects reached.")
            return

        # Only apply effect if it's allowed
        if effect == 'expand':
            if not hasattr(self.paddle, "original_width"):
                self.paddle.original_width = self.paddle.rect.width
            self.paddle.image = pg.transform.scale(self.paddle.image,
                                                   (int(self.paddle.rect.width * 1.5), self.paddle.rect.height))
            self.paddle.rect = self.paddle.image.get_rect(center=self.paddle.rect.center)

        elif effect == 'shrink':
            if not hasattr(self.paddle, "original_width"):
                self.paddle.original_width = self.paddle.rect.width
            self.paddle.image = pg.transform.scale(self.paddle.image,
                                                   (int(self.paddle.rect.width * 0.6), self.paddle.rect.height))
            self.paddle.rect = self.paddle.image.get_rect(center=self.paddle.rect.center)

        elif effect == 'extra_life':
            self.game_stats['lives'] += 1

        elif effect == 'fast_ball':
            self.ball.dx *= 1.8
            self.ball.dy *= 1.8

        elif effect == 'laser':
            self.laser_mode = True

        elif effect == 'sticky':
            self.ball.sticky = True

        elif effect == 'slow_paddle':
            self.paddle.slow = True

        elif effect == 'reverse_controls':
            self.paddle.reverse = True

        self.active_effects.append((effect, now + 5000))



