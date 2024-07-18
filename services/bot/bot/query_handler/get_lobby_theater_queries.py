# Standard library
import re
from urllib.parse import urlparse, parse_qs

def get_lobby_theater_queries(callback_data:str) -> tuple:
    match = re.search(r"@(.*?)(\?|$)", callback_data)
    regex_match = match.group(1) if match else None

    theater = regex_match if regex_match and regex_match != "lobby" else None
    lobby = regex_match if regex_match and regex_match == "lobby" else None
    queries = None

    if theater:
        queries = parse_qs(urlparse(callback_data.replace(f"goBack@", "http://")).query)

    return (lobby, theater, queries)