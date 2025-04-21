import os

import pygame as pg

from config import LINE_SPACING, WINDOW_WIDTH, WINDOW_HEIGHT, FONT, FONT_SIZE, BLACK, WHITE, IMAGE_PATHS
from state_manager.menu_manager import MenuManager
from state_manager.states import States


class Help(States, MenuManager):
    """
    Help screen state that shows game instructions.
    """

    def __init__(self):
        States.__init__(self)
        MenuManager.__init__(self)

        self.options = ['Back']
        self.next_list = ['menu']
        self.from_bottom = 180
        self.spacer = LINE_SPACING * 2
        self.pre_render_options()
        self.next = 'menu'
        # Background Image

        # Load background using centralized path from settings.json
        try:
            image_path = IMAGE_PATHS["blurred_bg"]
            self.background = pg.image.load(image_path).convert()
            self.background = pg.transform.scale(self.background, (WINDOW_WIDTH, WINDOW_HEIGHT))
        except Exception as e:
            print("Failed to load background image:", e)
            self.background = pg.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            self.background.fill((WHITE))

    def startup(self, persist=None):
        print("Starting Help Screen")
        self.persist = persist

    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        self.get_event_menu(event)

    def update(self, screen, dt):
        self.update_menu()
        self.draw(screen)

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        font = pg.font.SysFont(FONT, FONT_SIZE)
        small_font = pg.font.SysFont(FONT, 28)

        # Title at Top
        title_text = font.render("Help", True, BLACK)
        screen.blit(title_text, title_text.get_rect(center=(WINDOW_WIDTH // 2, 80)))

        # Help instructions
        lines = [
            "Use LEFT and RIGHT arrows to move the paddle",
            "The ball bounces about autonomously",
            "Try to keep it on-screen as long as possible",
            "Break all bricks to win the game (or press B)",
            "Power-Ups come in all shapes and sizes!",
            "Catch one with your paddle, and see what happens!",
            "Press Esc return to menu",
            ""
        ]

        # Layout Configuration
        start_y = 150
        line_spacing = LINE_SPACING + 15
        text_offset = 20
        text_area_x = 100  # shift text right a little
        paddle_width = 100

        # Drawing functions for specific lines
        def draw_paddle_line(y):
            paddle_height = 15
            paddle_x = text_area_x
            paddle_y = y + 5
            pg.draw.rect(screen, "purple", pg.Rect(paddle_x, paddle_y, paddle_width, paddle_height))
            return paddle_x + paddle_width + text_offset

        def draw_ball_line(y):
            pg.draw.circle(screen, (255, 0, 0), (text_area_x + 500, y + 11.5), 10)
            return text_area_x + text_offset

        def draw_brick_line(y):
            brick_color = (30, 30, 150)
            pg.draw.rect(screen, brick_color, pg.Rect(text_area_x, y, 60, 15))
            return text_area_x + 60 + text_offset

        def draw_esc_line(y):
            # Simplified color calculation
            r, g, b = 0, 120, 30  # red color components
            pg.draw.rect(screen, (r, g, b), pg.Rect(text_area_x, y, 60, 15))
            return text_area_x + 60 + text_offset

        # Map line indices to their specific drawing functions
        line_drawers = {
            0: draw_paddle_line,
            1: draw_ball_line,
            3: draw_brick_line,
            4: draw_esc_line
        }

        # Default drawing behavior (for lines without special handling)
        def default_draw(y):
            return text_area_x + text_offset

        # Draw instructions
        for i, line in enumerate(lines):
            y = start_y + i * line_spacing
            draw_func = line_drawers.get(i, default_draw)
            text_x = draw_func(y)

            text = small_font.render(line, True, BLACK)
            screen.blit(text, (text_x, y))

        # Draw the Back Button 
        self.draw_menu(screen)

    def cleanup(self):
        """
        Cleanup for Help screen.
        Required by state management system.
        """
        return self.persist
