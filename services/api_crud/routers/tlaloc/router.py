# FastAPI
from fastapi import APIRouter, status

# CRUDManager
from libraries.CRUDManager import CRUDManager
from config import database_hic_cibus
# Models
from models import physicalFrameSentModel

# Schemas
from schemas import (
    UserLoginSchema,
    RequestToUpdateSessionSchema,
    QueryFrameSchema,
)
from schemas.hic_cibus.physical_frame_sent_record import (
    PhysicalFrameSent_DataSchema,
    PhysicalFrame
)

# Endpoints Implementation
from .login import login
from .update_session import update_session
from .orchard_frames import orchard_buttons

# .utils
from .get_physical_frame import get_physical_frame
from .register_physical_frame_shipment import (
    check_physical_frame_shipment,
    send_physical_frame,
    register_frame_shipment
)

# Utils
from utils.handler_exceptions import handler_exceptions

router = APIRouter(prefix="/tlaloc", tags=["Tlaloc"])

# ******************************
# * POST - Get Gallery Buttons *
# ******************************
@router.post(
    path="/container_frames/orchards",
    status_code=status.HTTP_200_OK,
    summary="Contenedor de Frames",
)
async def get_orchard_gallery_buttons(userRequest: QueryFrameSchema):
    buttons = await orchard_buttons(userRequest)

    return buttons

# *****************************
# * GET - Get Physical Frame *
# *****************************
@router.get(
    path="/ticket_office/{theater}",
    status_code=status.HTTP_200_OK,
    summary="Contenedor de Frames",
)
async def get_physical_frame_endpoint(theater: str, id:int):
    physical_frame = await get_physical_frame(theater, id)

    return physical_frame

# *******************************************
# * POST - Register physical frame shipment *
# *******************************************
@router.post(
    path="/physical_frames_sent",
    status_code=status.HTTP_200_OK,
    summary="Registrar envío de Physic frames",
)
async def register_physical_frame_shipment_ENDPOINT(record: PhysicalFrameSent_DataSchema):
    crud_manager = CRUDManager(database_hic_cibus, physicalFrameSentModel)

    physical_frame: PhysicalFrame = record.physical_frame

    shipment_record = await check_physical_frame_shipment(
        session_id=record.shipment_record.session_id,
        physical_frame_id=physical_frame.id,
        crud_manager=crud_manager
    )

    if shipment_record:
        return None
    else:
        message_id = await send_physical_frame(record)

        id_record = await register_frame_shipment(
            crud_manager=crud_manager,
            record = record,
            message_id= message_id
        )

        return id_record

# **************************************************
# * DELETE - Delete record of sente physical frame *
# **************************************************
@router.delete(
    path="/delete_record_frame_sent",
    status_code=status.HTTP_200_OK,
    summary="Elimina el registro del frame enviado"
)
async def delete_record_frame_sent(message_id: int):
    crud_manager = CRUDManager(database_hic_cibus, physicalFrameSentModel)

    await crud_manager.delete_by_keywords(
        c_name="message_id",
        keyword=message_id
    )

# ********************
# * POST - Bot Login *
# ********************
@router.post(
    path="/login",
    status_code=status.HTTP_200_OK,
    summary="Autenticación de Usuarios",
)
@handler_exceptions
async def bot_user_auth(
    userRequest: UserLoginSchema,
):
    user_data: dict = await login(userRequest, error_message="The user does not exist")

    return user_data


# ************************
# * PUT - Update Session *
# ************************
@router.put(
    path="/update_session",
    status_code=status.HTTP_200_OK,
    summary="Administra las sesiones de los usuarios",
)
async def update_worker_session(userRequest: RequestToUpdateSessionSchema):
    changed_records: int  = await update_session(userRequest)

    return changed_records
