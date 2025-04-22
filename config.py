import json
import os

# Get the directory where config.py is located
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
SETTINGS_PATH = os.path.join(PROJECT_ROOT, "settings.json")

"""This serves as the config file that loads the settings.json file.
It reads all the values and makes sure things like colors,
window size, and fonts are ready to use throughout the game."""
# Load settings.json file
with open(SETTINGS_PATH, "r") as f:
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

"""Converting the color list to tuple because the JSON file
has the colors stored as a list. This makes the color values immutable,
ensuring constant color definitions throughout the game."""
# Colors (convert list to tuple)
BLACK = tuple(CONFIG["colors"]["black"])
WHITE = tuple(CONFIG["colors"]["white"])
GRAY = tuple(CONFIG["colors"]["gray"])
GREEN = tuple(CONFIG["colors"]["green"])
CYAN = tuple(CONFIG["colors"]["cyan"])
DARKGREEN = tuple(CONFIG["colors"]["darkgreen"])
PINK = tuple(CONFIG["colors"]["pink"])

IMAGE_PATHS = {
    key: os.path.join(PROJECT_ROOT, path)
    for key, path in CONFIG.get("images", {}).items()
}

# SETTINGS for game setup
SETTINGS = {
    'SIZE': (WINDOW_WIDTH, WINDOW_HEIGHT),
    'FPS': FPS
}
