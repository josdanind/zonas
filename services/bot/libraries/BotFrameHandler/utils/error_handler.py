# Standard Library
import os, inspect
from functools import wraps

# aiohttp
import aiohttp

from .output_msg import print_error_detail

def check_file(file_path: str):
    # Obtiene el nombre del fichero a partir de la ruta
    file_name = os.path.basename(file_path)

    # Identifica donde se llamo la función
    frame = inspect.currentframe()
    caller_frame = frame.f_back


    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        raise FileNotFoundError(
            {"caller": caller_frame.f_code.co_name, "reason": f"{file_name} no existe"},
        )


def http_exception_handler(func: callable) -> callable:
    @wraps(func)
    async def wrapper(*args, **kwargs) -> dict | None:
        try:
            # Intenta ejecutar la función decorada
            return await func(*args, **kwargs)
        except aiohttp.ClientResponseError as e:
            # Manejo de errores específicos de respuesta del servidor
            print_error_detail(
                title=f"HTTP error in {func.__name__}",
                details=[
                    f"Function: {inspect.currentframe().f_code.co_name}",
                    f"Status: {e.status}",
                ]
            )
        except aiohttp.ClientConnectionError as e:
            # Manejo de errores de conexión
            print_error_detail(
                title=f"Connection error in {func.__name__}",
                details=[
                    f"Function: {inspect.currentframe().f_code.co_name}",
                    "A connection error occurred",
                    str(e),
                ]
            )
        return None
    return wrapper