# Pydantic
from pydantic import BaseModel


class FrameDataSchema(BaseModel):
    template: str
    data: dict
    query: dict


class FrameDataWrapperSchema(FrameDataSchema):
    back_button: bool = True
    gallery_button: bool = False
    home_button: bool = False


class GallerySchema(BaseModel):
    name: str
    frame: FrameDataWrapperSchema
    selfButtonLabel: str
