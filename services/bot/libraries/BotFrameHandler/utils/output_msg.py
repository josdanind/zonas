# Coloramas
from colorama import Fore, Style, Back


def print_error_message(msg: str) -> str:
    print(f"{Fore.RED}ERROR: {msg}{Style.RESET_ALL}")


def print_error_detail(title: str, details: list[str]):
    title: str = f"{Fore.RED}ERROR: {title}{Style.RESET_ALL}\n"
    items: str = ""

    for i in details:
        items += f"{' '*2}{Fore.RED}\u2794{Style.RESET_ALL} {i}\n"

    print(title + items.rstrip())


def print_test(msg: str | None = None) -> str:
    if msg:
        print(f"{Back.GREEN}TEST: {msg}{Style.RESET_ALL}")
    else:
        print(f"{Back.GREEN}TEST: {20*'*'}{Style.RESET_ALL}")
