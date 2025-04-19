import os
import pygame as pg

from config import WHITE, DARKGREEN, GREEN, LINE_SPACING, STARTING_LIVES, WINDOW_WIDTH, FONT, FONT_SIZE, IMAGE_PATHS
from state_manager.menu_manager import MenuManager
from state_manager.states import States


class End(States, MenuManager):
    """
    End game state that displays game over options and handles player choices.

    This state combines functionality from both States and MenuManager to:
    - Present end-game options to the player
    - Handle navigation and selection of menu items
    - Reset game statistics when leaving the state
    - Transition to appropriate next screens based on player choice

    Inherits from:
        States: For state machine functionality and game statistics
        MenuManager: For menu display and interaction handling

    Attributes:
        Inherits attributes from both States and MenuManager.
        options (list): Text labels for menu options.
        next_list (list): Corresponding state names for menu options.
        from_bottom (int): Vertical offset from bottom of screen for menu placement.
        spacer (int): Additional spacing adjustment for menu positioning.
    """

    def __init__(self):
        """
        Initialize the End state with menu configuration and default transitions.

        Sets up:
        - Default next state ('main menu')
        - Menu option texts and corresponding target screens
        - Menu positioning parameters
        """
        States.__init__(self)
        MenuManager.__init__(self)
        self.next = 'main menu'
        self.options = ['Play Again', 'Main Menu', 'Quit']
        self.next_list = ['game', 'menu']
        self.pre_render_options()
        self.from_bottom = 200
        self.spacer = LINE_SPACING * 4
        self.won = False
        self.integer = 3

        # Load background using centralized path from settings.json
        try:
            image_path = IMAGE_PATHS["blurred_bg"]
            self.background = pg.image.load(image_path).convert()
            self.background = pg.transform.scale(self.background, (WINDOW_WIDTH, WINDOW_HEIGHT))
        except Exception as e:
            print("Failed to load background image:", e)
            self.background = pg.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            self.background.fill(WHITE)

    def cleanup(self):
        """
        Reset game statistics when leaving the End state.

        Resets:
        - Player score to 0
        - Player lives to starting value
        """
        self.game_stats['score'] = 0
        self.game_stats['lives'] = STARTING_LIVES

    def startup(self, persist):
        """
        Perform initialization when entering the End state.

        Currently prints a debug message but could be extended to:
        - Play sound effects
        - Show animations
        - Load high scores
        """
        print('Starting End Screen')
        self.persist = persist
        self.score = self.persist.get('score', 0)
        self.won = self.persist.get('won', False)  # Get win status from Game
        if self.won:
            self.integer = self.game_stats["lives"]
            if self.integer == 3:
                self.score = self.score + 2000
            elif self.integer == 2:
                self.score = self.score + 1000
            else:
                self.score = self.score + 500

    def get_event(self, event):
        """
        Handle incoming events for the End state.

        Args:
            event (pygame.Event): The event to process.

        Processes:
        - QUIT events (closing the window)
        - Delegates menu-related events to MenuManager
        """
        if event.type == pg.QUIT:
            self.quit = True
        self.get_event_menu(event)

    def update(self, screen, dt):
        """
        Update the End state each frame.

        Args:
            screen (pygame.Surface): The display surface to draw on.
            dt (float): Delta time since last frame (unused in current implementation).

        Performs:
        - Menu updates (through MenuManager)
        - Screen drawing
        """
        self.update_menu()
        self.draw(screen)

    def draw(self, screen):
        """
        Render all End state elements to the screen.
        """
        screen.fill(WHITE)
        font = pg.font.SysFont(FONT, FONT_SIZE)

        # Show "YOU WIN!" or "Game Over"
        title = "YOU WIN!" if self.won else "Game Over"
        title_color = (DARKGREEN) if self.won else (0, 0, 0)
        title_text = font.render(title, True, title_color)
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 60))
        screen.blit(title_text, title_rect)

        # Calculate Final Score
        base_path = os.path.dirname(os.path.abspath(__file__))
        heart_path = os.path.join(base_path, "..", "assets", "images", "heart.gif")

        if self.won:
            try:
                # Load and scale heart image
                heart_img = pg.image.load(heart_path).convert_alpha()
                heart_img = pg.transform.scale(heart_img, (50, 50))  # Scale to reasonable size
                heart_img.set_colorkey((255, 255, 255)) # Give White Background

                if self.integer == 3:
                    screen.blit(heart_img, (WINDOW_WIDTH // 4 - 25, 700))
                    screen.blit(heart_img, (WINDOW_WIDTH // 2 - 25, 700))
                    screen.blit(heart_img, (WINDOW_WIDTH * 3 // 4 - 25, 700))
                    reward_text = font.render("Perfect! 4500 + 2000", True, (GREEN))
                elif self.integer == 2:
                    screen.blit(heart_img, (WINDOW_WIDTH // 4 - 25, 700))
                    screen.blit(heart_img, (WINDOW_WIDTH // 2 - 25, 700))
                    reward_text = font.render("Not Bad! 4500 + 1000", True, (GREEN))
                elif self.integer == 1:
                    screen.blit(heart_img, (WINDOW_WIDTH // 4 - 25, 700))
                    reward_text = font.render("You Did it! 4500 + 500", True, (GREEN))

                reward_rect = reward_text.get_rect(center=(WINDOW_WIDTH // 2, 600))
                screen.blit(reward_text, reward_rect)

            except Exception as e:
                print(f"Could not load heart image: {e}")
                # Fallback: Draw red circles if image fails to load
                if self.integer == 3:
                    pg.draw.circle(screen, (255, 0, 0), (WINDOW_WIDTH // 4, 725), 25)
                    pg.draw.circle(screen, (255, 0, 0), (WINDOW_WIDTH // 2, 725), 25)
                    pg.draw.circle(screen, (255, 0, 0), (WINDOW_WIDTH * 3 // 4, 725), 25)
                elif self.integer == 2:
                    pg.draw.circle(screen, (255, 0, 0), (WINDOW_WIDTH // 4, 725), 25)
                    pg.draw.circle(screen, (255, 0, 0), (WINDOW_WIDTH // 2, 725), 25)
                elif self.integer == 1:
                    pg.draw.circle(screen, (255, 0, 0), (WINDOW_WIDTH // 4, 725), 25)

        # Show Final Score
        score_text = font.render(f"Final Score: {self.score}", True, (0, 0, 0))
        score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, 150))
        screen.blit(score_text, score_rect)
        self.draw_menu(screen)
