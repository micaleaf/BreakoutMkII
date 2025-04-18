import pygame as pg

from config import FONT, FONT_SIZE, BLACK, GRAY, WHITE


class MenuManager:
    """
    A menu management system for creating and handling interactive menus in Pygame.

    This class provides functionality for rendering, navigating, and selecting menu options
    with both keyboard and mouse input. It handles button sizing, positioning, rendering,
    and event management for menu interactions.

    Attributes:
        selected_index (int): Index of currently selected menu option.
        buttons (list): List of button dictionaries containing text and rect information.
        button_height (int): Height of each menu button in pixels.
        button_padding (int): Horizontal padding inside buttons in pixels.
        button_spacing (int): Vertical spacing between buttons in pixels.
        font (pygame.font.Font): Font used for rendering menu text.
        options (list): List of menu option text strings.
        next_list (list): List of state names or actions corresponding to menu options.
        quit (bool): Flag indicating if the quit option was selected.
        done (bool): Flag indicating if a menu selection was made.
        next (str): Name of the next state to transition to.
    """

    def __init__(self):
        """
        Initialize the MenuManager with default values.
        """
        self.selected_index = 0
        self.buttons = []
        self.button_height = 100
        self.button_padding = 50
        self.button_spacing = 15
        self.font = pg.font.SysFont(FONT, FONT_SIZE)

    def draw_menu(self, screen):
        """
        Draw all menu buttons on the specified surface.

        Args:
            screen (pygame.Surface): The surface to draw the menu on.

        The selected button is drawn with a different background color and text color
        for visual feedback. Each button has a white border.
        """
        for i, button in enumerate(self.buttons):
            # Draw button background
            bg_color = BLACK if i == self.hover_index else GRAY
            pg.draw.rect(screen, bg_color, button['rect'])
            pg.draw.rect(screen, WHITE, button['rect'], 2)  # Border

            # Draw button text
            text_color = WHITE if i == self.hover_index else BLACK
            text_surf = self.font.render(button['text'], True, text_color)
            text_rect = text_surf.get_rect(center=button['rect'].center)
            screen.blit(text_surf, text_rect)

    def update_menu(self):
        """
        Update the hover_index based on current mouse position.
        """
        mouse_pos = pg.mouse.get_pos()
        self.hover_index = -1
        for i, button in enumerate(self.buttons):
            if button['rect'].collidepoint(mouse_pos):
                self.hover_index = i
                break

    def get_event_menu(self, event):
        """
        Handle menu navigation and selection events.

        Args:
            event (pygame.Event): The event to process.

        Processes keyboard navigation (up/down/enter) and mouse interactions
        (clicks and hover effects).
        """
        if event.type == pg.KEYDOWN:
            if event.key in [pg.K_UP, pg.K_w]:
                self.change_selected_option(-1)
            elif event.key in [pg.K_DOWN, pg.K_s]:
                self.change_selected_option(1)
            elif event.key == pg.K_RETURN:
                self.select_option(self.selected_index)
        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            self.mouse_menu_click(event)
        elif event.type == pg.MOUSEMOTION:
            self.mouse_menu_hover(event)

    def mouse_menu_click(self, event):
        """
        Handle mouse clicks on menu buttons.

        Args:
            event (pygame.Event): The mouse button down event.

        When a button is clicked, it becomes selected and its action is triggered.
        """
        for i, button in enumerate(self.buttons):
            if button['rect'].collidepoint(event.pos):
                self.selected_index = i
                self.select_option(i)
                break

    def mouse_menu_hover(self, event):
        """
        Update menu selection based on mouse hover position.

        Args:
            event (pygame.Event): The mouse motion event.

        Highlights the button under the mouse cursor without requiring a click.
        """
        for i, button in enumerate(self.buttons):
            if button['rect'].collidepoint(event.pos):
                self.selected_index = i
                break

    def pre_render_options(self):
        """
        Create properly sized and positioned buttons based on text content.

        Calculates button dimensions based on the longest text option and positions
        all buttons either centered on screen or at a specified position.
        The menu can be positioned from the top or from the bottom of the screen.
        """
        self.buttons = []
        max_width = 0

        # Calculate maximum text width
        for option in self.options:
            text_width = self.font.render(option, True, BLACK).get_width()
            max_width = max(max_width, text_width)

        # Calculate button width with padding
        button_width = max_width + self.button_padding * 2

        # Calculate total menu height
        total_height = len(self.options) * (self.button_height + self.button_spacing) - self.button_spacing

        # Calculate starting position
        start_y = 200
        if hasattr(self, 'screen_rect') and hasattr(self, 'from_bottom'):
            start_y = self.screen_rect.height - self.from_bottom - total_height

        # Create buttons
        for i, option in enumerate(self.options):
            button_rect = pg.Rect(0, 0, button_width, self.button_height)
            button_rect.centerx = self.screen_rect.centerx if hasattr(self, 'screen_rect') else 400
            button_rect.y = start_y + i * (self.button_height + self.button_spacing)

            self.buttons.append({
                'text': option,
                'rect': button_rect
            })

    def select_option(self, i):
        """
        Handle selection of a menu option.

        Args:
            i (int): Index of the selected option.

        If the selected index matches the length of next_list, the quit flag is set.
        Otherwise, the next state is set from next_list and the done flag is set.
        """
        if i == len(self.next_list):
            self.quit = True
        else:
            self.next = self.next_list[i]
            self.done = True
            self.selected_index = 0

    def change_selected_option(self, op=0):
        """
        Change the currently selected menu option.

        Args:
            op (int): Direction to move selection (-1 for up, 1 for down).

        Handles wrapping around when moving past the first or last option.
        """
        if op:
            self.selected_index += op
            max_ind = len(self.buttons) - 1
            if self.selected_index < 0:
                self.selected_index = max_ind
            elif self.selected_index > max_ind:
                self.selected_index = 0
