# Standard Libraries
import os, re

# Commands
from .start import start_command

command_implementation = os.listdir("bot/message_handler/commands")
commands = []

ignored_names = ["main.py", "__pycache__"]

for command in command_implementation:
    if command not in ignored_names:
        commands.append(re.sub(r"\.py$", "", command))
