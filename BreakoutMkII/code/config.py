import json
import os

"""This can serve as the config file that loads the settings.json file.
It reads all the values and makes sure things like colors,
window size, and fonts are ready to use throughout the game. This way the JSON file loads 
in one place instead of importing it to each .py file"""
# Load settings.json file 
with open("settings.json", "r") as f:
    CONFIG = json.load(f)

# Window Settings
WINDOW_WIDTH = CONFIG["window"]["width"]
WINDOW_HEIGHT = CONFIG["window"]["height"]
FPS = CONFIG["fps"]

# Game Settings
STARTING_LIVES = CONFIG["starting_lives"]

# Font Settings
FONT = CONFIG["font"]["name"]
FONT_SIZE = CONFIG["font"]["size"]
LINE_SPACING = int(FONT_SIZE / 2)

"""Convering the color list to tuple because the JSON file
has the colors stored as a list. This makes the color values immutable,
this way the colors cannot be changed in the code and this ensures theres
constant color definitions"""
# Colors (convert list to tuple) 
BLACK = tuple(CONFIG["colors"]["black"])
WHITE = tuple(CONFIG["colors"]["white"])
GRAY = tuple(CONFIG["colors"]["gray"])
GREEN = tuple(CONFIG["colors"]["green"])
CYAN = tuple(CONFIG["colors"]["cyan"])

# SETTINGS for game setup 
SETTINGS = {
    'SIZE': (WINDOW_WIDTH, WINDOW_HEIGHT),
    'FPS': FPS
}
