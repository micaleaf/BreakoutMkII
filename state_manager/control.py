import pygame as pg
"""
State Control is based on a design by metulburr from the Python forum:
    https://python-forum.io/thread-336-post-64464.html#pid64464
"""

class Control:
    """
    A finite state machine for managing game screens and controlling the main game loop.

    This class handles initialization of the game window, state management, event processing,
    and the main game loop. It allows for switching between different game screens
    (like menu, gameplay, pause screens) cleanly.

    Attributes:
        done (bool): Flag indicating when the main game loop should exit.
        fps (int): Target frames per second for the game.
        screen (pygame.Surface): The main display surface.
        screen_rect (pygame.Rect): Rectangle representing the screen dimensions.
        clock (pygame.time.Clock): Game clock for controlling frame rate.
        state_dict (dict): Dictionary mapping state names to state instances.
        state_name (str): Current state's name.
        state (object): Current state instance.
    """

    def __init__(self, settings):
        """
        Initialize the Control object with game settings.

        Args:
            settings (dict): Dictionary containing game settings with keys:
                - 'FPS': Target frames per second
                - 'SIZE': Tuple of (width, height) for screen dimensions
        """
        self.done = False
        self.fps = settings['FPS']
        self.screen = pg.display.set_mode(settings['SIZE'])
        self.screen_rect = self.screen.get_rect()
        self.clock = pg.time.Clock()

    def setup_states(self, state_dict, start_state):
        """
        Set up the game screens and initialize the starting state.

        Args:
            state_dict (dict): Dictionary mapping state names to state instances.
            start_state (str): Name of the initial state to start with.
        """
        self.state_dict = state_dict
        self.state_name = start_state
        self.state = self.state_dict[self.state_name]

    def flip_state(self):
        """
        Transition from the current state to the next state.

        Performs cleanup of the current state, switches to the next state,
        and initializes the new state. Also keeps track of the previous state.
        """
        self.state.done = False
        previous, self.state_name = self.state_name, self.state.next

        persist = self.state.cleanup()
        self.state = self.state_dict[self.state_name]
        self.state.previous = previous
        self.state.startup(persist)

    def update(self, dt):
        """
        Update the current state and handle state transitions.

        Args:
            dt (float): Delta time (time since last frame) in seconds.
        """
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.flip_state()
        self.state.update(self.screen, dt)

    def event_loop(self):
        """
        Process all events in the pygame event queue.

        Handles system events (like quitting) and passes all events to the current state.
        """
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            self.state.get_event(event)

    def main_game_loop(self):
        """
        Run the main game loop until the done flag is set.

        This loop:
        1. Calculates delta time
        2. Processes events
        3. Updates game state
        4. Updates the display
        """
        while not self.done:
            delta_time = self.clock.tick(self.fps) / 1000.0
            self.event_loop()
            self.update(delta_time)
            pg.display.update()
