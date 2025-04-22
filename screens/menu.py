import os

import pygame as pg

from config import WHITE, PINK, LINE_SPACING, FONT, FONT_SIZE, WINDOW_WIDTH, WINDOW_HEIGHT, IMAGE_PATHS
from state_manager.menu_manager import MenuManager
from state_manager.states import States


class Menu(States, MenuManager):
    """
    Main Menu state that handles the game's primary navigation interface.

    This hybrid state combines functionality from both States and MenuManager to:
    - Display the game's main menu options
    - Handle player menu navigation and selection
    - Manage transitions to other game screens
    - Provide visual feedback for menu interactions

    Inherits from:
        States: For state machine functionality and core game flow control
        MenuManager: For menu rendering and input handling capabilities

    Attributes:
        Inherits all attributes from both parent classes.
        options (list): Text labels for the menu options ['Play', 'Quit']
        next_list (list): Target screens corresponding to menu options ['game']
        from_bottom (int): Vertical offset from screen bottom for menu positioning (200px)
        spacer (int): Additional vertical spacing adjustment (LINE_SPACING * 4)
    """

    def __init__(self):
        """
        Initialize the Main Menu state with default configuration.

        Sets up:
        - Default next state ('game')
        - Menu option texts and their corresponding target screens
        - Menu visual presentation parameters
        - Calls pre-render for menu items
        """
        States.__init__(self)
        MenuManager.__init__(self)
        self.next = 'game'
        self.options = ['Play', 'Help', 'Quit']
        self.next_list = ['game', 'help']
        self.pre_render_options()
        self.from_bottom = 200
        self.spacer = LINE_SPACING * 4

        # Background Image on Start Screen
        try:
            image_path = IMAGE_PATHS["main_bg"]
            self.background = pg.image.load(image_path).convert()
            self.background = pg.transform.scale(self.background, (WINDOW_WIDTH, WINDOW_HEIGHT))
        except Exception as e:
            print("Failed to load background image:", e)
            self.background = pg.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            self.background.fill((WHITE)) 

    def cleanup(self):
        """
        Perform cleanup operations when leaving the Main Menu state.

        Currently outputs a debug message but could be extended to:
        - Free menu resources
        - Save menu configuration
        - Stop menu-specific audio
        """
        print('Cleaning Up Main Menu')

    def startup(self, persist):
        """
        Perform initialization when entering the Main Menu state.

        Currently outputs a debug message but could be extended to:
        - Play menu music
        - Initialize menu animations
        - Load menu assets
        """
        print('Starting Up Main Menu')
        self.persist = persist

    def get_event(self, event):
        """
        Handle all input events for the Main Menu state.

        Args:
            event (pygame.Event): The input event to process

        Processes:
        - System QUIT events (window closing)
        - Delegates menu-specific events to MenuManager
        """
        if event.type == pg.QUIT:
            self.quit = True
        self.get_event_menu(event)

    def update(self, screen, dt):
        """
        Update the menu state each frame.

        Args:
            screen (pygame.Surface): The display surface to render to
            dt (float): Time elapsed since last frame (delta time)

        Responsibilities:
        - Updates menu state through MenuManager
        - Triggers screen redraw
        """
        self.update_menu()
        self.draw(screen)

    def draw(self, screen):
        """
        Render all menu elements to the display surface.

        Args:
            screen (pygame.Surface): The target surface for rendering

        Draws:
        - Solid white background
        - Menu options through MenuManager's draw functionality
        """
        screen.blit(self.background, (0, 0))
        title_font = pg.font.SysFont(FONT, FONT_SIZE + 40, bold=True)

        # Text Drop Shadow 
        shadow = title_font.render("BREAKOUT", True, (100, 100, 100))
        screen.blit(shadow, shadow.get_rect(center=(WINDOW_WIDTH // 2 + 3, 103)))

        # Title Text Color and Position
        title_text = title_font.render("BREAKOUT", True, (PINK))
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 100))
        screen.blit(title_text, title_text.get_rect(center=(WINDOW_WIDTH // 2, 100)))
        self.draw_menu(screen)
