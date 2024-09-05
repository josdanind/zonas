# FastAPI
from fastapi import APIRouter, status, Request

# Schemas
from schemas import UserLoginSchema, RequestToUpdateSessionSchema, QueryFrameSchema

# Endpoints Implementation
from .login import login
from .update_session import update_session
from .orchard_frames import orchard_buttons
from .get_physical_frame import get_physical_frame

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
# * POST - Get Physical Frame *
# *****************************
@router.get(
    path="/ticket_office/{theater}",
    status_code=status.HTTP_200_OK,
    summary="Contenedor de Frames",
)
async def get_orchard_gallery_buttons(theater: str, id:int, session_id:int,):
    physical_frame = await get_physical_frame(theater, id, session_id)

    return physical_frame

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
