import pygame as pg

from config import WHITE, LINE_SPACING, STARTING_LIVES, WINDOW_WIDTH, FONT, FONT_SIZE
from menu_manager import MenuManager
from states import States


class End(States, MenuManager):
    """
    End game state that displays game over options and handles player choices.

    This state combines functionality from both States and MenuManager to:
    - Present end-game options to the player
    - Handle navigation and selection of menu items
    - Reset game statistics when leaving the state
    - Transition to appropriate next states based on player choice

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
        - Menu option texts and corresponding target states
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

        Args:
            screen (pygame.Surface): The display surface to draw on.

        Draws:
        - White background
        - Menu options (through MenuManager)
        """
        screen.fill(WHITE)

        font = pg.font.SysFont(FONT, FONT_SIZE)

        # Show "YOU WIN!" or "Game Over"
        title = "YOU WIN!" if self.won else "Game Over"
        title_color = (0, 200, 0) if self.won else (0, 0, 0)
        title_text = font.render(title, True, title_color)
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 60))
        screen.blit(title_text, title_rect)

        # Show Final Score
        score_text = font.render(f"Final Score: {self.score}", True, (0, 0, 0))
        score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, 150))
        screen.blit(score_text, score_rect)
        self.draw_menu(screen)
