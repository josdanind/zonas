# Standard Library
import json

# Pydantic
from pydantic import BaseModel, ValidationError

# CRUDManager
from libraries.CRUDManager import CRUDManager

#  Utils
from utils.console_message import *

# Database - Databases lib
from config import database_bots, database_hic_cibus

# ***********
# * Schemas *
# ***********
# Hic-cibus Schemas
from schemas import (
    CompanyInDB,
    FarmInDB,
    CropInDB,
    ControlSystemInDB,
    DeviceInDB,
    WorkerInDB,
    CropWorkerInDB,
    SessionInDB,
    SessionControlSystemInDB,
)

# Bots Schemas
from schemas import BotInDB

# **********
# * Models *
# **********
# Bots
from models import botModel

# Hic-cibus
from models import (
    companyModel,
    farmModel,
    cropModel,
    controlSystemModel,
    sensorModel,
    actuatorModel,
    workerModel,
    crop_workerModel,
    sessionModel,
    sessions_control_systemModel,
)


async def sign_up_bots() -> None:
    try:
        with open("db_init/bots/activate_bots.json", "r") as file:
            bots = json.load(file)
            active_bot_list = []

            crud_manager = CRUDManager(database_bots, botModel)

            for bot in bots:
                bot_dict = BotInDB(**bot).model_dump(by_alias=True)
                bot_name = bot_dict["name"]
                is_active = bot_dict["is_active"]

                exist = await crud_manager.verify_existence(**{"name": bot_name})

                if exist is None:
                    await crud_manager.insert(bot_dict)
                    database_message(f"Bot {bot_name} was created")

                if is_active:
                    active_bot_list.append(bot_name)

            crud_message(active_bot_list)
            del crud_manager
    except TypeError as err:
        check_output()
        print_error_message(err)


async def sign_up_hic_cibus() -> None:
    try:
        with open("db_init/hic-cibus/company_farm.json", "r") as file:
            crud_manager = CRUDManager(database_hic_cibus, companyModel)
            companies: dict = json.load(file)

            for company in companies:
                # Data to record
                company_data: dict = company["company"]
                farms_data: list = company["farms"]

                company_schema = CompanyInDB(
                    name=company_data["name"], data=company_data["data"]
                )

                company_schema.id = await create_record(
                    crud_manager=crud_manager,
                    schema=company_schema,
                    condition={"name": company_schema.name},
                )

                await crud_manager.change_table(farmModel)

                for farm in farms_data:
                    farm_data: dict = next(iter(farm.values()))
                    farm_data.update({"company_id": company_schema.id})

                    farm_schema = FarmInDB(**farm_data)

                    farm_schema.id = await create_record(
                        crud_manager, farm_schema, {"name": farm_schema.name}
                    )

                await crud_manager.change_table(companyModel)

        with open("db_init/hic-cibus/crops.json", "r") as file:
            crops_data = json.load(file)

            for data in crops_data:
                farm = data["farm"]
                crops = data["crops"]

                await crud_manager.change_table(farmModel)
                exist = await crud_manager.verify_existence(**{"name": farm})

                if exist:
                    farm_id = exist.id

                    for crop in crops:
                        crop["farm_id"] = farm_id
                        crop_schema = CropInDB(**crop)

                        await crud_manager.change_table(cropModel)
                        crop_schema.id = await create_record(
                            crud_manager=crud_manager,
                            schema=crop_schema,
                            condition={"crop_plot": crop_schema.crop_plot},
                        )

                        control_system = crop["data"]["control_system"]
                        control_system["crop_id"] = crop_schema.id

                        control_system_schema = ControlSystemInDB(**control_system)

                        await crud_manager.change_table(controlSystemModel)
                        control_system_schema.id = await create_record(
                            crud_manager=crud_manager,
                            schema=control_system_schema,
                            condition={"uuid": control_system_schema.uuid},
                        )

                        # Initialize sensors
                        sensors = control_system["sensors"]

                        await crud_manager.change_table(sensorModel)
                        await register_device(
                            crud_manager=crud_manager,
                            devices_data=sensors,
                            control_system_id=control_system_schema.id,
                        )

                        # Initialize actuators
                        actuators = control_system["actuators"]

                        await crud_manager.change_table(actuatorModel)
                        await register_device(
                            crud_manager=crud_manager,
                            devices_data=actuators,
                            control_system_id=control_system_schema.id,
                        )

                else:
                    crud_output(f"The {farm} farm does not exist")

        with open("db_init/hic-cibus/workers.json", "r") as file:
            workers_data = json.load(file)

            for data in workers_data:
                farm = data["farm"]
                workers = data["workers"]

                await crud_manager.change_table(farmModel)
                exist = await crud_manager.verify_existence(**{"name": farm})

                if exist:
                    farm_id = exist.id

                    for worker in workers:
                        worker["farm_id"] = farm_id
                        worker_schema = WorkerInDB(**worker)

                        #  Registra trabajador
                        await crud_manager.change_table(workerModel)
                        worker_schema.id = await create_record(
                            crud_manager=crud_manager,
                            schema=worker_schema,
                            condition={"name": worker_schema.name},
                        )

                        session_schema = SessionInDB(worker_id=worker_schema.id)
                        await crud_manager.change_table(sessionModel)

                        exist = await crud_manager.verify_existence(
                            worker_id=worker_schema.id
                        )

                        if exist is None:
                            # Crea sesión para usuario
                            session_schema.id = await crud_manager.insert(
                                session_schema.model_dump(
                                    exclude_none=True, exclude={"id"}
                                )
                            )

                            database_message(
                                f"Se creó una sesión para {worker_schema.name}"
                            )
                        else:
                            session_schema.id = exist.id
                            database_message(
                                f"Existe una sesión para {worker_schema.name}, su id es {session_schema.id}"
                            )

                        for crop in worker["crops"]:
                            await crud_manager.change_table(cropModel)
                            exist = await crud_manager.verify_existence(
                                **{"crop_plot": crop}
                            )

                            if exist:
                                crop_id = exist.id

                                # Verifica si ya existe la relación entre las dos entidades
                                await crud_manager.change_table(crop_workerModel)
                                exist = await crud_manager.select_and(
                                    crop_id=crop_id, worker_id=worker_schema.id
                                )

                                if not exist:
                                    crop_worker_schema = CropWorkerInDB(
                                        crop_id=crop_id, worker_id=worker_schema.id
                                    )

                                    #  Registra relación entre entidades crop-worker
                                    await crud_manager.insert(
                                        crop_worker_schema.model_dump(exclude={"id"})
                                    )

                                    database_message(
                                        f"La relación entre worker_id:{worker_schema.id} y crop_id: {crop_id} fue creada en la tabla crops_workers"
                                    )
                                else:
                                    database_message(
                                        f"La relación entre worker_id:{worker_schema.id} y crop_id: {crop_id} existe en la tabla crops_workers"
                                    )

                                # Registra la relación entre Session - Control System
                                await crud_manager.change_table(controlSystemModel)
                                result = await crud_manager.verify_existence(
                                    crop_id=crop_id
                                )

                                control_system_id = result.id

                                await crud_manager.change_table(
                                    sessions_control_systemModel
                                )
                                exist = await crud_manager.select_and(
                                    session_id=session_schema.id,
                                    control_system_id=control_system_id,
                                )

                                if not exist:
                                    sessions_control_system_schema = (
                                        SessionControlSystemInDB(
                                            session_id=session_schema.id,
                                            control_system_id=control_system_id,
                                        )
                                    )
                                    await crud_manager.insert(
                                        sessions_control_system_schema.model_dump(
                                            exclude={"id"}
                                        )
                                    )

                                    database_message(
                                        f"La relación entre session_id={session_schema.id} y control_system_id={control_system_id} fue creada en la tabla sessions_control_system"
                                    )
                                else:
                                    database_message(
                                        f"La relación entre session_id={session_schema.id} y control_system_id={control_system_id} existe en la tabla sessions_control_system"
                                    )
                            else:
                                crud_output(f"The {crop} crop plot does not exist")

    except KeyError as err:
        print(f"KeyError: {err}")
    except ValidationError as err:
        print(err)
        print_error_message(str(err).split("\n")[0])


async def create_record(crud_manager: CRUDManager, schema: BaseModel, condition: dict):
    key = next(iter(condition.keys()))
    exist = await crud_manager.verify_existence(**condition)

    if exist is None:
        id = await crud_manager.insert(schema.model_dump(exclude={"id"}))
        database_message(
            f"{eval(f'schema.{key}')} was registered in the {crud_manager.table_name} table with id={id}"
        )
    else:
        id = exist.id
        database_message(
            f"{eval(f'schema.{key}')} exists in the {crud_manager.table_name} table with id={id}"
        )

    return id


async def register_device(
    crud_manager: CRUDManager, devices_data: json, control_system_id: int
):
    for device_data in devices_data:
        device = devices_data[device_data]
        device["control_system_id"] = control_system_id

        for i in range(device["amount"]):
            uuid = device["uuids"][i]
            device_i = device | {"uuid": uuid}
            schema = DeviceInDB(**device_i)

            schema.id = await create_record(
                crud_manager=crud_manager, schema=schema, condition={"uuid": uuid}
            )
