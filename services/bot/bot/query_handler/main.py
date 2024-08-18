# Standard library
import re
from urllib.parse import urlparse, parse_qs

# BOT
from telebot.types import CallbackQuery
from ..config.bot import bot

# Frame Handler
from ..frame_handler.main import theater_handler

# Utils - BotFrameHandler
from libraries.BotFrameHandler.utils import print_test
from ..frame_handler.main import theater_handler

# Utils - Bot
from .get_lobby_theater_queries import get_lobby_theater_queries

# ********************
# * Button - Go Back *
# ********************
@bot.callback_query_handler(func=lambda call: "goBack" in call.data)
async def goBack_button(call: CallbackQuery):
    chat_id = call.from_user.id
    username = call.from_user.username
    user = await theater_handler.authenticate_user(username, chat_id)

    lobby, theater, queries = get_lobby_theater_queries(call.data)

    if (theater or lobby) and not queries:
        frame = theater_handler.lobby_frame if lobby else theater_handler.theater_frame_data[theater]["frame"]
        await theater_handler.change_message(
            chat_id=chat_id,
            user=user,
            frame=frame,
            frame_route="/" if lobby else f"/{theater}"
        )

    await bot.answer_callback_query(call.id)


# ******************************
# * Button - Redirect To Frame *
# ******************************
@bot.callback_query_handler(func=lambda call: "@" in call.data)
async def redirect_to_frame_button(call: CallbackQuery):
    try:
        chat_id = call.from_user.id
        username = call.from_user.username
        theater_link = call.data

        user = await theater_handler.authenticate_user(username, chat_id)

        theater = re.search(r"@(.*?)://", theater_link).group(1)
        gallery= re.search(r"://(.*?)(\?|$)", theater_link).group(1)
        queries = parse_qs(urlparse(theater_link.replace(f"@{theater}", "http")).query)

        match gallery:
            case "galleries":
                gallery_frame = theater_handler.theater_frame_data[theater]["frame"]

                await theater_handler.change_message(
                    chat_id=chat_id,
                    user=user,
                    frame=gallery_frame,
                    frame_route= f"/{theater}"
                )
            case "atrium":
                if not queries:
                    atrium_frame = await theater_handler.get_atrium(theater, farm_id=user["farm_id"])

                    await theater_handler.change_message(
                        chat_id=chat_id,
                        user=user,
                        frame=atrium_frame,
                        frame_route=f"/{theater}/{gallery}"
                    )
                else:
                    ids = queries["id"]
                    print(ids)
                    print(theater_link)
            case _:
                pass

        await bot.answer_callback_query(call.id)
    except Exception as e:
        #! IMPLEMENTAR EXCEPCIÓN
        print("Ocurrrio un error", e)
