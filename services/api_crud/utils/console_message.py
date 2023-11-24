# Colorama
from colorama import Fore, Style


def print_error_message(msg: str) -> str:
    print(f"{Fore.RED}ERROR: {msg}{Style.RESET_ALL}")


def database_message(msg: str) -> str:
    print(f"{Fore.BLUE}Database: {msg}{Style.RESET_ALL}")


def check_output(msg: str = "*" * 20) -> str:
    message = f"{Fore.GREEN}{msg}{Style.RESET_ALL}"
    print(message)
