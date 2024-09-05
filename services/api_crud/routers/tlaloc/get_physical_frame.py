# Standard Library
import json

# CRUDManager
from libraries.CRUDManager import CRUDManager

# Databases
from config import database_hic_cibus

# Models
from models import cropModel

# query = """\
# SELECT
#     crops.crop,
#     control_systems.frame AS frame,
#     control_systems.id AS control_system_id
# FROM
#     crops
# INNER JOIN
#     control_systems ON control_systems.crop_id = crops.id
# INNER JOIN
#     control_systems ON control_systems.crop_id = crops.id
# WHERE
#     crops.id = :id;
# """

query = """\
SELECT
    crops.crop,
    control_systems.frame AS frame,
    control_systems.id AS control_system_id
FROM
    crops
INNER JOIN
    control_systems ON control_systems.crop_id = crops.id
WHERE
    crops.id = :id;
"""

caption = lambda title: f"""\
<b>{title}</b>\n
"""

async def get_physical_frame(theater: str, id:int):
    crud_manager = CRUDManager(database_hic_cibus, cropModel)

    data_physical_frame =  await crud_manager.db.fetch_one(query, {"id":id})
    frame_data = json.loads(data_physical_frame.frame)
    control_system_id = data_physical_frame.control_system_id

    physical_frame = {
        "id": control_system_id,
        "theater": theater,
        "cover": frame_data["cover"],
        "buttons": [],
        "caption": caption(data_physical_frame.crop),
        "template": frame_data["template"],
    }


    return physical_frame
