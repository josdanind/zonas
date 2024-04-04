# Standard Library
import re


def take_extension(file_name: str):
    match = re.search(r"\.(\S+)$", file_name)

    if match:
        return match.group(0)
    else:
        raise ValueError(f"El fichero {file_name} no tiene extensión")


def get_penultimate_path_segment(path: str):
    pattern = r".*/([^/]+)/[^/]+$"
    match = re.search(pattern, path)

    if match:
        return match.group(1)
    else:
        raise ValueError(f"Error al extraer el penúltimo segmento del path")
