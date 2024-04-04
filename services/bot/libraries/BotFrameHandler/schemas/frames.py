# Pydantic
from pydantic import BaseModel


class GalleryFrameSchema(BaseModel):
    name: str
    template: str
    data: dict
    query: dict


class GalleryFrameWrapperSchema(GalleryFrameSchema):
    back_button: bool = True
    gallery_button: bool = False
    home_button: bool = False


# ------------------


class FrameSettingsSchema(BaseModel):
    template: str
    data: dict


class FrameSchema(BaseModel):
    id: str
    selfButtonLabel: str
    frame_settings: FrameSettingsSchema


class FrameWrapperSchema(BaseModel):
    frame: FrameSchema
    back_button: bool = True
    gallery_button: bool = False
    home_button: bool = False
