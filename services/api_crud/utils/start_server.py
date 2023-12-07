# Standard Library
import json

# CRUDManager
from libraries.CRUDManager import CRUDManager

#  Utils
from utils.console_message import *

# Schemas
from schemas import BotInDB

# Database - Databases lib
from config import database_bots

# Models
from models import botModel


async def sign_up_bots() -> None:
    try:
        with open("bots/activate_bots.json", "r") as file:
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
    except TypeError as err:
        print_error_message(err)
