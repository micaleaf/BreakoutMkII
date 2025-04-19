import pygame as pg
import pytest
from menu import Menu

pg.init()


def test_menu_next_state():
    menu = Menu()
    assert menu.next in ['game', 'help', 'end', 'quit']
