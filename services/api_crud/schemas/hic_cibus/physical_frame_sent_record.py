# Pydantic
from pydantic import BaseModel, ConfigDict, Field

class PhysicalFrame(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: int | None = None
    theater: str | None = None
    cover: bytes | str | None = None
    buttons: list[dict] | None = None
    caption: str | None = None
    template: str = "with_cover"


class PhysicalFrameSent_RecordSchema(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
   
    session_id: int  = Field(alias="fk_session_id")
    physical_frame_id: int = Field(alias="fk_physical_frame_id")
    frame_link: str
    message_id: int | None = None


class PhysicalFrameSent_DataSchema(BaseModel):
    chat_id: int
    physical_frame: PhysicalFrame
    shipment_record: PhysicalFrameSent_RecordSchema


