# Standard Library
import os, inspect


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
