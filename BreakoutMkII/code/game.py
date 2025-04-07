import pygame as pg
import pygame.mixer
import os
pg.mixer.init()
from states import States
from constants import GRAY, WHITE, FONT, FONT_SIZE, LINE_SPACING, STARTING_LIVES, WINDOW_HEIGHT, WINDOW_WIDTH
from gameScreen import create_bricks, Brick, Paddle, paddle_width, paddle_height, Ball, Debris

wall_width = 16


class Game(States):
    """
    Main game state class that handles gameplay logic and rendering.

    This state represents the active gameplay screen where the core game interaction occurs.
    It inherits from the base States class and implements game-specific behavior including:
    - Game initialization and cleanup
    - Event handling for game interactions
    - Game statistics management (lives and score)
    - Screen rendering and updates

    Attributes:
        Inherits all attributes from States class.
        next (str): Automatically set to 'end' state for transition after gameplay.
    """

    def __init__(self):
        """
        Initialize the Game state with default values.

        Sets up:
        - Next state to transition to ('end')
        - Initial game statistics (lives and score)
        """
        States.__init__(self)
        self.next = 'end'
        self.game_stats['lives'] = STARTING_LIVES
        self.game_stats['score'] = 0
        self.last_direction = None  # can be 'left', 'right', or None
        self.persist = {}
        self.ball_launched = False
        self.won = False  # Track if the player won

        # Load Game Screen Background iImage
        """Image was downloaded from: 
        https://www.freepik.com/free-vector/abstract-pixel-rain-background_6148356.htm#fromView=search&page=1&position=39&uuid=1c7b579c-f59d-46ec-be47-aae2a84ceb5a&query=Retro+Game+Background"""
        
        base_path = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.abspath(os.path.join(base_path, "..", "assets/images", "BackGround.jpg"))
        try:
            print("Loading game background image from:", image_path)
            self.background = pg.image.load(image_path).convert()
            self.background = pg.transform.scale(self.background, (WINDOW_WIDTH, WINDOW_HEIGHT))
        except Exception as e:
            print("Game background image failed to load:", e)
            self.background = pg.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            self.background.fill(WHITE)

    def cleanup(self):
        """
        Perform cleanup operations when leaving the Game state.

        Currently prints a debug message but can be extended to handle:
        - Releasing resources
        - Saving temporary game data
        - Resetting volatile game elements
        """
        print("Cleaning Up Game")
        self.persist['score'] = self.game_stats['score']
        self.persist['won'] = self.won  # Pass win status to End screen
        return self.persist

    def startup(self, persist):
        """
        Perform initialization operations when entering the Game state.

        Currently prints a debug message but can be extended to handle:
        - Loading level data
        - Initializing game objects
        - Preparing audio/visual assets
        """
        print("Starting Up Game")

        # Sounds
        base_path = os.path.dirname(os.path.abspath(__file__))
        sound_path = lambda name: os.path.join(base_path, "..", "assets", "sounds", name)

        # Load sounds
        self.sounds = {
            'brick': pg.mixer.Sound(sound_path("hit_brick.wav")),
            'paddle': pg.mixer.Sound(sound_path("hit_paddle.wav")),
            'life_lost': pg.mixer.Sound(sound_path("lose_life.wav")),
            'game_over': pg.mixer.Sound(sound_path("game_over.wav")),
            'win': pg.mixer.Sound(sound_path("win.wav")),
            'wall': pg.mixer.Sound(sound_path("wall.wav")),
        }

        self.persist = persist if persist is not None else {}

        self.all_sprites = pg.sprite.Group()

        # animation
        self.particles = pg.sprite.Group()

        # Create the brick wall
        self.brick_wall = create_bricks(5, 9)

        # Add bricks to sprite group
        for brick in self.brick_wall:
            self.all_sprites.add(brick)

        # ball
        self.ball = Ball((255, 0, 0), radius=10, speed=5, sounds=self.sounds)
        self.all_sprites.add(self.ball)

        self.paddle = Paddle((0, 255, 255), paddle_width, paddle_height)
        self.paddle.rect.x = (WINDOW_WIDTH - paddle_width) // 2
        self.paddle.rect.y = WINDOW_HEIGHT - 80


        self.ball_launched = False
        self.last_direction = None

        self.all_sprites.add(self.paddle)

    def get_event(self, event):
        """
    Handle incoming events for the Game state.

    Args:
        event (pygame.Event): The event to process.

    Handles:
    - Paddle movement direction
    - Ball launch on first arrow key press
    - ESC or mouse click to end game
    """
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                self.last_direction = 'left'
                if not self.ball_launched:
                    self.ball.launch()
                    self.ball_launched = True

            elif event.key == pg.K_RIGHT:
                self.last_direction = 'right'
                if not self.ball_launched:
                    self.ball.launch()
                    self.ball_launched = True

            elif event.key == pg.K_ESCAPE:
                self.game_stats['lives'] = 0
                self.game_stats['score'] += 500
                self.done = True
                self.sounds['game_over'].play()

            elif event.key == pg.K_b:  # Break all bricks instantly
                bricks_remaining = len(self.brick_wall)
                self.game_stats['score'] += 100 * bricks_remaining  # award the score!
                self.brick_wall.empty()
                self.won = True
                self.done = True
                self.sounds['win'].play()

        elif event.type == pg.KEYUP:
            if (event.key == pg.K_LEFT and self.last_direction == 'left') or \
                    (event.key == pg.K_RIGHT and self.last_direction == 'right'):
                self.last_direction = None

    def update(self, screen, dt):
        """
        Update game state and handle rendering.

        Args:
            screen (pygame.Surface): The surface to draw on.
            dt (float): Delta time since last frame (unused in current implementation).

        Currently delegates all drawing to the draw() method but could be extended to:
        - Handle game logic updates
        - Process AI movements
        - Manage game timers
        """

        # Check for collision with bricks
        hit_bricks = pg.sprite.spritecollide(self.ball, self.brick_wall, dokill=False)

        if hit_bricks:
            # Only bounce once per collision pass
            self.ball.dy *= -1

            for brick in hit_bricks:
                # Spawn particles
                for _ in range(8):
                    particle = Debris(brick.rect.center, brick.color)
                    self.particles.add(particle)

                # Remove brick
                self.brick_wall.remove(brick)
                self.all_sprites.remove(brick)

                self.game_stats['score'] += 100

            self.sounds['brick'].play()

        # Ball–Paddle collision
        if pg.sprite.collide_rect(self.ball, self.paddle):
            self.ball.dy *= -1  # Bounce upward
            self.sounds['paddle'].play()

            # Add horizontal change based on where the ball hit the paddle
            offset = (self.ball.rect.centerx - self.paddle.rect.centerx) / (self.paddle.rect.width / 2)
            self.ball.dx += offset * 2  # tweak the multiplier for more/less curve

            # Cap the max horizontal speed
            max_speed = self.ball.speed
            self.ball.dx = max(-max_speed, min(self.ball.dx, max_speed))


        if self.last_direction == 'left':
            self.paddle.move_left(8)
        elif self.last_direction == 'right':
            self.paddle.move_right(8)

        if not self.done:
            self.ball.update()

        # animation
        self.particles.update()

        if self.ball.rect.bottom >= WINDOW_HEIGHT:
            self.game_stats['lives'] -= 1
            print("Ball lost! Lives left:", self.game_stats['lives'])
            self.sounds['life_lost'].play()

            if self.game_stats['lives'] <= 0:
                self.done = True  # Go to end screen
                self.sounds['game_over'].play()
            else:
                self.reset_ball_and_paddle()

        # If all bricks are gone, mark win and stop the game
        if len(self.brick_wall) == 0 and not self.done:
            self.won = True
            self.done = True
            self.sounds['win'].play()

        self.draw(screen)



    def draw(self, screen):
        """
        Render all game elements to the screen.

        Args:
            screen (pygame.Surface): The surface to draw on.

        Draws:
        - Gray background
        - Title text ("Game Screen") centered
        - Instructions text ("Press anything to exit...") below title
        """
        screen.blit(self.background, (0, 0))
        pg.draw.rect(screen, GRAY, (0, 0, WINDOW_WIDTH, 50))

        # Top wall
        pg.draw.rect(screen, GRAY, (0, 0, WINDOW_WIDTH, 50))

        # Left wall
        pg.draw.rect(screen, GRAY, (0, 0, wall_width, WINDOW_HEIGHT))

        # Right wall
        pg.draw.rect(screen, GRAY, (WINDOW_WIDTH - wall_width, 0, wall_width, WINDOW_HEIGHT))

        # Draw bricks
        self.all_sprites.draw(screen)

        # animation
        self.particles.draw(screen)

        # Font setup
        font = pg.font.SysFont(FONT, 30)

        # Render lives (top-left)
        lives_text = font.render(f"Lives: {self.game_stats['lives']}", True, (0, 0, 0))
        screen.blit(lives_text, (20, 10))

        # Render score (top-right)
        score_text = font.render(f"Score: {self.game_stats['score']}", True, (0, 0, 0))
        score_rect = score_text.get_rect(topright=(WINDOW_WIDTH - 20, 10))
        screen.blit(score_text, score_rect)

    def reset_ball_and_paddle(self):
        # Reset paddle position
        self.paddle.rect.x = (WINDOW_WIDTH - paddle_width) // 2
        self.paddle.rect.y = WINDOW_HEIGHT - 80

        # Reset ball position
        self.ball.rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        self.ball.dx = 0
        self.ball.dy = 0
        self.ball_launched = False
        self.last_direction = None
