from config import TLALOC_URL

# CRUDManager
from libraries.CRUDManager import CRUDManager

# AIOHTTP
import aiohttp

# Schemas
from schemas.hic_cibus.physical_frame_sent_record import (
    PhysicalFrameSent_DataSchema,
    PhysicalFrameSent_RecordSchema,
)


async def check_physical_frame_shipment(
    session_id: int,
    physical_frame_id: int,
    crud_manager: CRUDManager
) -> PhysicalFrameSent_RecordSchema | None:
    table_record = await crud_manager.select_and(
        fk_session_id=session_id,
        fk_physical_frame_id=physical_frame_id
    )

    if table_record:
        return PhysicalFrameSent_RecordSchema(**dict(table_record))

async def send_physical_frame(frame: PhysicalFrameSent_DataSchema):
        async with aiohttp.ClientSession() as session:
            url = f"{TLALOC_URL}/tlaloc/actions/send_physical_frame"
            payload = {"chat_id": frame.chat_id} | frame.model_dump()

            async with session.post(url=url, json=payload) as resp:

                resp.raise_for_status()

                message_id  = await resp.json()

        return message_id

async def register_frame_shipment(
    crud_manager: CRUDManager,
    record: PhysicalFrameSent_DataSchema,
    message_id: int
):
        id_record = await crud_manager.insert(
            record={
                "fk_session_id": record.shipment_record.session_id,
                "fk_physical_frame_id": record.physical_frame.id,
                "frame_link": record.shipment_record.frame_link,
                "message_id": message_id
            }
        )

        return id_record