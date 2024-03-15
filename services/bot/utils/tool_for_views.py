# standard Library
import os, importlib.util


def get_all_views(views: list[str], views_folder_path: str):
    all_views = []

    for view in views:
        # Construye la ruta completa de cada view
        view_path = os.path.join(views_folder_path, f"{view}/view.py")

        # Crea un spec para cada módulo
        spec = importlib.util.spec_from_file_location(view, view_path)

        # Crea el modulo a partir del spec
        dub_view = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(dub_view)

        all_views.append(dub_view)

    return all_views
