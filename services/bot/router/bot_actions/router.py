# FastAPI
from fastapi import APIRouter, status

# Bot - FrameHandler
from bot import theater_handler

# TheaterHandler - Schemas
from libraries.BotFrameHandler.schemas import (
    PhysicalFrameSent_RecordSchema,
    PhysicalFrame,
    PhysicalFrameSent_DataSchema
)

from libraries.BotFrameHandler.utils.output_msg import print_test

router = APIRouter(prefix="/tlaloc/actions", tags=["Bot actions"])


# *****************************************
# * POST - Envía un frame físico a Tlaloc *
# *****************************************
@router.post(
    path="/send_physical_frame",
    status_code=status.HTTP_200_OK,
    summary="Envía un Frame",
    response_model=int
)
async def send_physical_frame(frame_data: PhysicalFrameSent_DataSchema):
    chat_id = frame_data.chat_id
    physical_frame = frame_data.physical_frame
    session_id = frame_data.shipment_record.session_id

    frame = theater_handler.build_frame_from_physical(
        physical_frame=physical_frame,
        session_id=session_id
    )

    message_id = await theater_handler.send_frame(
        frame=frame,
        chat_id=chat_id
    )

    return message_id