import pytest
import pygame as pg
from menu import Menu

pg.init()

def test_menu_next_state():
    menu = Menu()
    assert menu.next in ['game', 'help', 'end', 'quit']
