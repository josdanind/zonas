"""Estable los comandos (como el /start)  a partir del nombre de
los ficheros que tiene la implementación del respectivo comando.
"""
# Standard Libraries
import os, re

# Commands
from .start import start_command

# devuelve una lista con los nombres de las entradas (archivos y carpetas)
# en el directorio especificado por esa ruta
command_implementation = os.listdir("bot/message_handler/commands")
commands = []

ignored_names = ["main.py", "__pycache__"]

for command in command_implementation:
    if command not in ignored_names:
        # Elimina del string la extensión '.py'
        commands.append(re.sub(r"\.py$", "", command))
