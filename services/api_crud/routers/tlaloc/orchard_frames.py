# Standar
# Schemas
from schemas import QueryFrameSchema

# CRUDManager
from libraries.CRUDManager import CRUDManager

# Databases
from config import database_hic_cibus

# Models
from models import cropModel

async def orchard_buttons(query:QueryFrameSchema):
    match query.key:
        case "gallery":
            match query.value:
                case "atrium":
                    buttons = await get_atrium_buttons(query.link, query.farm_id)
                case "categories":
                    pass
                case _:
                    pass

    return buttons

async def get_atrium_buttons(link: str, farm_id:int):
    # Inicializa el gestor CRUD con la base de datos y el modelo de cultivo
    crud_manager = CRUDManager(database_hic_cibus, cropModel)

    # Consulta para obtener los cultivos de la granja especificada
    query = "SELECT id, crop FROM crops WHERE farm_id = :farm_id;"
    crops = await crud_manager.db.fetch_all(query, {"farm_id": farm_id})

    crops_callback_data = {}

    for crop in crops:
        link_with_id = f"{link}?id={crop.id}"

        if crop.crop not in crops_callback_data:
            crops_callback_data[crop.crop] = link_with_id
        else:
            crops_callback_data[crop.crop] += f"&id={crop.id}"

    buttons = [
        {
            "text": crop_name,
            "callback_data": callback_data
        } for crop_name, callback_data in crops_callback_data.items()
    ]

    return buttons