# Pydantic
from pydantic import BaseModel


class GalleryFrameSchema(BaseModel):
    template: str
    data: dict
    query: dict


class GalleryWrapperSchema(GalleryFrameSchema):
    back_button: bool = True
    gallery_button: bool = False
    home_button: bool = False


class GallerySchema(BaseModel):
    name: str
    frame: GalleryWrapperSchema
    selfButtonLabel: str
