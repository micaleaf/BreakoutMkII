import pygame as pg
import pytest
from screens.menu import Menu
"""
This tests for the Menu class in screens.menu.
Focuses on verifying correct screen state transitions.
"""
pg.init()

def test_menu_next_state():
    """
    Verifies that the Menu can transition to one of the expected states.
    """
    menu = Menu()
    assert menu.next in ['game', 'help', 'end', 'quit']
