"""
Main module for the game application.

This module initializes and runs the game using a finite state machine pattern.
It handles pygame initialization, screen setup, and the main game loop.
"""

import pygame as pg
from config import SETTINGS
from screens import Menu, Game, End, Help  # explicit imports instead of wildcard
from state_manager.control import Control


def main():
    """
    Main entry point for the game application.

    Initializes and runs the game using a finite state machine pattern.
    Responsibilities include:
    - Initializing pygame
    - Creating the main Control instance
    - Setting up game screens
    - Starting the main game loop
    - Properly quitting pygame on exit

    The state machine consists of three screens:
    - menu: The main menu interface
    - game: The core gameplay state
    - end: The game over/end screen state
    - help: The help screen

    Usage:
        Called automatically when the script is run directly.
    """
    pg.init()  # Initialize all pygame modules
    pg.mixer.init()

    # Create the main game controller with specified settings
    app = Control(SETTINGS)

    # Dictionary mapping state names to state instances
    state_dict = {
        'menu': Menu(),
        'game': Game(),
        'end': End(),
        'help': Help()
    }

    # Configure the state machine with available screens and starting point
    app.setup_states(state_dict, 'menu')

    # Start the main game loop (blocks until game exits)
    app.main_game_loop()

    # Clean up pygame resources
    pg.quit()


if __name__ == "__main__":
    main()
