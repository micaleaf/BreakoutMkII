from config import STARTING_LIVES, SETTINGS
from .control import Control
"""
State Control is based on a design by metulburr from the Python forum:
    https://python-forum.io/thread-336-post-64464.html#pid64464
"""

class States(Control):
    """
    Base class for game screens, inheriting from Control to provide state management functionality.

    This class serves as the foundation for all game screens in a finite state machine system.
    It maintains common game statistics and state transition flags that are shared across
    all game screens.

    Attributes:
        game_stats (dict): Dictionary tracking persistent game statistics across screens.
            Contains:
                - 'lives': Number of remaining player lives
                - 'score': Current player score
        done (bool): Flag indicating if the current state should transition to next state.
        next (str): Name of the next state to transition to.
        quit (bool): Flag indicating if the game should exit.
        previous (str): Name of the previous state (for return navigation).
    """

    # Class-level game statistics shared across all screens
    game_stats = {
        'lives': STARTING_LIVES,
        'score': 0
    }

    def __init__(self):
        """
        Initialize the base state with common settings and transition flags.

        Sets up the control system with game settings and initializes state transition flags.
        """
        Control.__init__(self, SETTINGS)
        self.done = False
        self.next = None
        self.quit = False
        self.previous = None
