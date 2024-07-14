# Standard Library
import json, os
from pathlib import Path

# Schema
from libraries.BotFrameHandler.schemas import (
    ContainerSchema,
    ViewSchema,
    GallerySchema,
    FrameDataWrapperSchema,
    TheaterSchema,
)

# Utils - BotFrameHandler
from .output_msg import print_error_detail, print_test
from .error_handler import check_file


def create_TheaterSchema(container_path: Path) -> TheaterSchema:
    try:
        theater_name = os.path.basename(container_path)
        error_message = f"Se produjo un error creando <{theater_name} Theater>"
        setting_path = os.path.join(container_path, "settings.json")
        settings = {}

        # Comprueba la existencia del settings.json
        check_file(setting_path)

        # Deserialización del settings.json
        with open(setting_path, "r") as file_settings:
            settings = json.load(file_settings)

        # BUILDING THE THEATER
        # -- id:str Es un identificador único para Theater
        id: str = settings["id"]
        # -- Billboard
        billboard: str = settings["billboard"]
        # -- Container
        container = ContainerSchema(**settings["container"])
        # -- View
        view = ViewSchema(id_container_main=container.id)
        # -- Atrium
        atrium_data = settings["atrium"]
        atrium_frame_data = atrium_data["frame_data"]

        atrium = GallerySchema(
            name="atrium",
            selfButtonLabel=atrium_data["selfButtonLabel"],
            frame=FrameDataWrapperSchema(**atrium_frame_data),
        )
        # -- Galleries
        galleries = []

        for gallery in settings["galleries"]:
            gallery_frame_data = gallery["frame_data"]

            galleries.append(
                GallerySchema(
                    name=gallery["name"],
                    selfButtonLabel=gallery["selfButtonLabel"],
                    frame=gallery_frame_data,
                )
            )

        # THEATER
        return TheaterSchema(
            id=id,
            billboard=billboard,
            container=container,
            view=view,
            atrium=atrium,
            galleries=galleries,
            display_galleries=settings["settings"]["display_galleries"],
            frame_template=settings["settings"]["template"],
        )
    except FileNotFoundError as e:
        print_error_detail(
            title=e.args[0]["caller"], details=[error_message, e.args[0]["reason"]]
        )
