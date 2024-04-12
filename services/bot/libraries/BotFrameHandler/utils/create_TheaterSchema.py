# Standard Library
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
from .error_handler import check_file


def create_TheaterSchema(container_path: Path) -> TheaterSchema:
    setting_path = os.path.join(container_path, "settings.json")
    settings = {}

    try:
        check_file(setting_path)

        with open(setting_path, "r") as file_settings:
            settings = json.load(file_settings)

        # BUILDING THE THEATER
        # -- Billboard
        id: str = settings["id"]
        # -- Billboard
        billboard: str = settings["billboard"]
        # -- Container
        container = ContainerSchema(**settings["container"])
        # -- View
        view = ViewSchema(id_container_main=container.id)
        # -- Atrium
        atrium_data = settings["atrium"]
        atrium_frame = atrium_data["frame"]
        atrium_cover = os.path.join(container_path, atrium_frame["data"]["cover"])

        check_file(atrium_cover)

        atrium_frame["data"]["cover"] = atrium_cover

        atrium = GallerySchema(
            name="atrium",
            selfButtonLabel=atrium_data["selfButtonLabel"],
            frame=GalleryWrapperSchema(**atrium_data["frame"]),
        )
        # -- Galleries
        galleries = []

        for gallery in settings["galleries"]:
            gallery_frame = gallery["frame"]
            gallery_cover = os.path.join(container_path, gallery_frame["data"]["cover"])

            check_file(gallery_cover)

            gallery_frame["data"]["cover"] = gallery_cover

            galleries.append(
                GallerySchema(
                    name=gallery["name"],
                    selfButtonLabel=gallery["selfButtonLabel"],
                    frame=gallery["frame"],
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
        )

    except FileNotFoundError as err:
        print_error_message(err)
