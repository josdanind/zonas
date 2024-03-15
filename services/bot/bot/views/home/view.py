# Standard Library
import os

# Utils
from utils.set_view_config import set_view_config

# Loading main window settings
current_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(current_dir, "config.json")
cover_path = os.path.join(current_dir, "assets/cover.png")

# *************
# * Home View *
# *************
view = set_view_config(config_path, cover_path)
