# Standard library
import re
from urllib.parse import urlparse, parse_qs

# BOT
from telebot.types import CallbackQuery
from ..config.bot import bot
from ..utils.bot_api import authenticate_user

# Frame Handler
from ..frame_handler.main import theater_handler

# Utils - BotFrameHandler
from libraries.BotFrameHandler.utils import print_test
from ..frame_handler.main import theater_handler

# Utils - Bot
from ..utils.bot_api import get_buttons
from .get_lobby_theater_queries import get_lobby_theater_queries
# pyTelegramBotAPI
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Environment Variables
from config import API_CRUD_URL

# Schemas
from libraries.BotFrameHandler.schemas import FrameSchema

# ********************
# * Button - Go Back *
# ********************
@bot.callback_query_handler(func=lambda call: "goBack" in call.data)
async def goBack_button(call: CallbackQuery):
    chat_id = call.from_user.id
    username = call.from_user.username
    user = await authenticate_user(username, chat_id)

    lobby, theater, queries = get_lobby_theater_queries(call.data)

    if (theater or lobby) and not queries:
        frame = theater_handler.lobby_frame if lobby else theater_handler.frames[theater]["frame"]
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

        user = await authenticate_user(username, chat_id)
        theater = re.search(r"@(.*?)://", theater_link).group(1)
        gallery= re.search(r"://(.*?)(\?|$)", theater_link).group(1)
        queries = parse_qs(urlparse(theater_link.replace(f"@{theater}", "http")).query)

        theater_data = theater_handler.frames[theater]
        container_url =  API_CRUD_URL + theater_data["container_path"]

        match gallery:
            case "galleries":
                await theater_handler.change_message(
                    chat_id=chat_id,
                    user=user,
                    frame=theater_data["frame"],
                    frame_route= f"/{theater}"
                )
            case "atrium":
                if not queries:
                    atrium = theater_data["galleries"]["atrium"]
                    atrium_link = atrium["link"]

                    # * COVER
                    atrium_cover = atrium["cover"]

                    # * BUTTONS
                    buttons_dict: list = await get_buttons(
                        container_url, atrium_link, atrium["query"], user["farm_id"]
                    )

                    buttons_dict.append({
                        "text": "Ir atrás",
                        "callback_data": f"goBack@{theater}",
                    })

                    # * KEYBOARD
                    atrium_keyboard = InlineKeyboardMarkup(row_width=1)
                    atrium_keyboard.add(
                        *[InlineKeyboardButton(**button) for button in buttons_dict]
                    )

                    # * CAPTION
                    atrium_caption = atrium["text_box"]
                    # --// Title
                    title = atrium_caption["title"]
                    # --// Description
                    description = atrium_caption["description"]
                    # --// Caption
                    caption = f"<b>{title}</b>\n\n{description}"

                    atrium_frame = FrameSchema(
                        cover=atrium_cover,
                        reply_markup=atrium_keyboard,
                        caption=caption,
                        parse_mode="HTML"
                    )

                    await theater_handler.change_message(
                        chat_id=chat_id,
                        user=user,
                        frame=atrium_frame,
                        frame_route=f"/{theater}/{gallery}"
                    )
                else:
                    ids = queries["id"]
                    print(ids)
            case _:
                pass

        await bot.answer_callback_query(call.id)
    except Exception as e:
        #! IMPLEMENTAR EXCEPCIÓN
        print("Ocurrrio un error", e)
