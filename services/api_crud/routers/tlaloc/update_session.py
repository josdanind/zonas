# Standard Library
from datetime import datetime

# Databases
from config import database_hic_cibus

# Models
from models import sessionModel

#  CRUDManager
from libraries.CRUDManager import CRUDManager

# Schemas
from schemas import RequestToUpdateSessionSchema

async def update_session(data_session: RequestToUpdateSessionSchema):
    crud_manager = CRUDManager(database_hic_cibus, sessionModel)

    session_id = data_session.session_id
    to_update = data_session.session_table.model_dump(exclude_none=True)
    to_update["updated_at"] = datetime.now()

    result = await crud_manager.update(to_update, id=session_id)

    return result