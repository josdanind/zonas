# Colorama
from colorama import Fore, Style

from asyncpg import Record


def print_error_message(msg: str) -> str:
    print(f"{Fore.RED}ERROR: {msg}{Style.RESET_ALL}")


def database_message(msg: str) -> str:
    print(f"{Fore.BLUE}Database: {msg}{Style.RESET_ALL}")


def crud_message(msg: str) -> str:
    print(f"{Fore.CYAN}CRUD: Bots activos {msg}{Style.RESET_ALL}")


def check_output(msg: str = "*" * 20) -> str:
    print(f"{Fore.GREEN}{msg}{Style.RESET_ALL}")


def print_Record_object(record: Record | None = None, record_list: list[Record] = []):
    if len(record_list) > 0 and record == None:
        for record in record_list:
            record_list = dict(record)
            print(record_list)
