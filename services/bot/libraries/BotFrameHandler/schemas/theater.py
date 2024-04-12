# Standard Library
from uuid import UUID

# Pydantic
from pydantic import BaseModel

# Schemas
from .gallery import GallerySchema
from .container import ContainerSchema
from .view import ViewSchema


class TheaterSchema(BaseModel):
    id: str
    billboard: str
    container: ContainerSchema
    view: ViewSchema
    atrium: GallerySchema
    galleries: list[GallerySchema]
    display_galleries: bool = False
