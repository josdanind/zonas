# Standard Library
import os


def check_file(file_path):
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        file_name = os.path.basename(file_path)

        raise FileNotFoundError(
            f'"FrameHandler" -> Se produjo un error creando la instancia "Theater". {file_name} no existe.'
        )
