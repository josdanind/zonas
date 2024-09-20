# Pydantic
from pydantic import BaseModel, ConfigDict


class PhysicalFrame(BaseModel):
    id: int | None = None
    theater: str | None = None
    cover: bytes | str | None = None
    buttons: list | None = None
    caption: str | None = None
    template: str = "with_cover"

# ! Mejorar el nombre. 
class PhysicalFrameSent_RecordSchema(BaseModel):
    session_id: int
    physical_frame_id: int
    frame_link: str
    message_id: int | None = None

class PhysicalFrameSent_DataSchema(BaseModel):
    chat_id: int
    physical_frame: PhysicalFrame
    shipment_record: PhysicalFrameSent_RecordSchema