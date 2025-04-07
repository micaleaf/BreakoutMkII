import pygame as pg
from control import Control
from constants import SETTINGS
from menu import Menu
from game import Game
from end import End
from help import Help

"""
State Control is based on a design by metulburr from the Python forum:
    https://python-forum.io/thread-336-post-64464.html#pid64464
"""

def main():
    """
    Main entry point for the game application.

    Initializes and runs the game using a finite state machine pattern.
    Responsibilities include:
    - Initializing pygame
    - Creating the main Control instance
    - Setting up game states
    - Starting the main game loop
    - Properly quitting pygame on exit

    The state machine consists of three states:
    - menu: The main menu interface
    - game: The core gameplay state
    - end: The game over/end screen state
    - help:

    Usage:
        Called automatically when the script is run directly.
    """
    pg.init()  # Initialize all pygame modules

    # Create the main game controller with specified settings
    app = Control(SETTINGS)

    # Dictionary mapping state names to state instances
    state_dict = {
        'menu': Menu(),  # Main menu state
        'game': Game(),  # Gameplay state
        'end': End(),  # End game state
        'help': Help()
    }

    # Configure the state machine with available states and starting point
    app.setup_states(state_dict, 'menu')

    # Start the main game loop (blocks until game exits)
    app.main_game_loop()

    # Clean up pygame resources
    pg.quit()


if __name__ == "__main__":
    """
    Entry point when script is run directly.
    Calls the main() function to start the game.
    """
    main()