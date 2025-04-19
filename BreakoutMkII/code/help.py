import pygame as pg
from menu_manager import MenuManager
from states import States
from constants import WHITE, LINE_SPACING, WINDOW_WIDTH, WINDOW_HEIGHT, FONT, FONT_SIZE, GREEN, BLACK

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
        #Background Image
        self.background = pg.image.load("../assets/images/blurredBG.png").convert()
        self.background = pg.transform.scale(self.background, (WINDOW_WIDTH, WINDOW_HEIGHT))

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

     #  Title at Top
        title_text = font.render("Help", True, BLACK)
        screen.blit(title_text, title_text.get_rect(center=(WINDOW_WIDTH // 2, 80)))

        # Help instructions
        lines = [
            "Use LEFT and RIGHT arrows to move the paddle",
            "The ball bounces about autonomously",
            "Try to keep it on-screen as long as possible",
            "Break all bricks to win the game (or press B)",
            "Press Esc return to menu",
            ""
        ]

        # Layout Configuration 
        start_y = 150
        red = [0, 120, 30, 30]
        blue = [0, 30, 30, 150]
        line_spacing = LINE_SPACING + 15
        text_offset = 20
        text_area_x = 100  # shift text right a little
        text_max_width = WINDOW_WIDTH - 2 * text_area_x

        # Draw instructions 
        for i, line in enumerate(lines):
            y = start_y + i * line_spacing

            if i == 0:
                # Draw Paddle to the Left of Instructions
                paddle_width = 100
                paddle_height = 15
                paddle_x = text_area_x
                paddle_y = y + 5
                pg.draw.rect(screen, "purple", pg.Rect(paddle_x, paddle_y, paddle_width, paddle_height))

                # Adjust text position to the right of the paddle
                text_x = paddle_x + paddle_width + text_offset
            elif i == 1:
                pg.draw.circle(screen, (255, 0, 0), (text_area_x + 500, y + 11.5), 10)
                text_x = text_area_x + text_offset
            elif i == 2:
                text_x = text_area_x + text_offset
            elif i == 3:
                pg.draw.rect(screen, (30, 30, 150), pg.Rect(text_area_x, y, 60, 15))
                text_x = text_area_x + 60 + text_offset
            elif i == 4:
                blend = (2) / max((4) - 1, 1)
                r = int(blue[1] + (red[1] - blue[1]) * blend)
                g = int(blue[2] + (red[2] - blue[2]) * blend)
                b = int(blue[3] + (red[3] - blue[3]) * blend)
                pg.draw.rect(screen, (r, g, b), pg.Rect(text_area_x, y, 60, 15))
                text_x = text_area_x + 60 + text_offset
            elif i == 5:
                pg.draw.rect(screen, (red[1], red[2], 30), pg.Rect(text_area_x, y, 60, 15))
                text_x = text_area_x + 60 + text_offset
            else:
                # Align remaining lines with the same text_x
                text_x = text_area_x + paddle_width + text_offset

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
