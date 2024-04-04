# Coloramas
from colorama import Fore, Style


def print_error_message(msg: str) -> str:
    print(f"{Fore.RED}ERROR: {msg}{Style.RESET_ALL}")
