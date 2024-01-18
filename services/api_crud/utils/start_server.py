# Standard Library
import json

# Environments Variables
from config import administrator

#  Utils
from utils.console_message import *

# CRUDManager
from libraries.CRUDManager import CRUDManager

# Database - Databases lib
from config import database_bots, database_hic_cibus

# Recording routines
from .recording_routines import *

# **********
# * Models *
# **********
# Bots
from models import botModel

# Hic-cibus
from models import companyModel, crudUserModel


# **************
# * Admin User *
# **************
async def sign_up_crud_users() -> None:
    crud_manager = CRUDManager(database_hic_cibus, crudUserModel)

    await create_record(
        crud_manager=crud_manager,
        schema=administrator,
        condition={"username": administrator.username},
    )

    del crud_manager


async def sign_up_bots() -> None:
    try:
        crud_manager = CRUDManager(database_bots, botModel)
        with open("db_init/bots/activate_bots.json", "r") as file:
            bots = json.load(file)
            await register_bots(crud_manager, bots)

    except FileNotFoundError as err:
        crud_error_message('El fichero "' + str(err).split("'")[1] + '" no se encontró')


async def sign_up_hic_cibus() -> None:
    try:
        crud_manager = CRUDManager(database_hic_cibus, companyModel)

        # Registra las empresas con sus respectivas granjas
        with open("db_init/hic-cibus/company_farm.json", "r") as file:
            companies: dict = json.load(file)
            await register_company_farm(crud_manager, companies)

        # Registra los cultivos con sus respectivos sistemas de control
        with open("db_init/hic-cibus/crops.json", "r") as file:
            crops_data = json.load(file)
            await register_crop_control_system(crud_manager, crops_data)

        # Registra los trabajadores y crea sus respectivas sesiones
        with open("db_init/hic-cibus/workers.json", "r") as file:
            workers_data = json.load(file)
            await register_workers_sessions(crud_manager, workers_data)

        del crud_manager
    except FileNotFoundError as err:
        crud_error_message('El fichero "' + str(err).split("'")[1] + '" no se encontró')
