from control import Control
from constants import STARTING_LIVES, SETTINGS


class States(Control):
    """
    Base class for game states, inheriting from Control to provide state management functionality.

    This class serves as the foundation for all game states in a finite state machine system.
    It maintains common game statistics and state transition flags that are shared across
    all game states.

    Attributes:
        game_stats (dict): Dictionary tracking persistent game statistics across states.
            Contains:
                - 'lives': Number of remaining player lives
                - 'score': Current player score
        done (bool): Flag indicating if the current state should transition to next state.
        next (str): Name of the next state to transition to.
        quit (bool): Flag indicating if the game should exit.
        previous (str): Name of the previous state (for return navigation).
    """

    # Class-level game statistics shared across all states
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