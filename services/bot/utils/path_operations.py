# Standard Library
import os


def take_folder_names(
    path: str, ignore: list[str] = ["__pycache__", "home"]
) -> list[str]:
    folder_names = []

    for item in os.listdir(path):
        item_path = os.path.join(path, item)

        if os.path.isdir(item_path) and item not in ignore:
            folder_names.append(item)

    return folder_names
