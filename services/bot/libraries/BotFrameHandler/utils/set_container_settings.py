# Standard Library
import uuid
import json, os
from pathlib import Path

# Schema
# from ..schemas.frames import FrameContainerSchema
from libraries.BotFrameHandler.schemas import (
    ContainerSchema,
    ViewSchema,
    GallerySchema,
    GalleryWrapperSchema,
    TheaterSchema,
)

# Utils - BotFrameHandler
from .output_msg import print_error_message


# def set_container_settings(container_path: Path) -> FrameContainerSchema:
def set_container_settings(container_path: Path):
    setting_path = os.path.join(container_path, "settings.json")
    cover_path = os.path.join(container_path, "cover.png")
    settings = {}

    try:
        for dir in [setting_path, cover_path]:
            # Verificando el directorio del frame
            if not os.path.exists(dir) or not os.path.isfile(dir):
                file_name = os.path.basename(dir)

                raise FileNotFoundError(
                    f'"FrameHandler" -> Se produjo un error al intentar instanciar ContainerFrame:{container_name}. {file_name} no existe.'
                )

        with open(setting_path, "r") as file_settings:
            settings = json.load(file_settings)

        # BUILDING THE THEATER
        # -- Billboard
        billboard: str = settings["billboard"]
        # -- Container
        container = ContainerSchema(**settings["container"])
        # -- View
        view = ViewSchema(id_container_main=container.id)
        # -- Atrium
        atrium_data = settings["atrium"]
        atrium = GallerySchema(
            name="atrium",
            selfButtonLabel=atrium_data["selfButtonLabel"],
            frame=GalleryWrapperSchema(**atrium_data["frame"]),
        )
        # -- Galleries
        galleries = []

        for gallery in settings["galleries"]:
            galleries.append(
                GallerySchema(
                    name=gallery["name"],
                    selfButtonLabel=gallery["selfButtonLabel"],
                    frame=gallery["frame"],
                )
            )

        # THEATER
        return TheaterSchema(
            id=uuid.uuid4(),
            billboard=billboard,
            container=container,
            view=view,
            atrium=atrium,
            galleries=galleries,
        )

    except FileNotFoundError as err:
        print_error_message(err)

    return "Hola Como estas?"
