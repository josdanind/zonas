# Bot
from telebot.types import Message

# Environment variables
from config import API_CRUD_URL

# Utils
from bot.utils.bot_api import authenticate_user, update_session

from ...frame_handler.main import theater_handler


async def start_command(message: Message):
    username = message.chat.username
    chat_id = message.chat.id

    user = await authenticate_user(username, chat_id)

    if user:
        msg_id = await theater_handler.send_frame(theater_handler.lobby_frame, chat_id)
        to_update = {"main_message_id": msg_id, "current_action": {"route": "/"}}

        await update_session(user["session_id"], to_update)
        # <TEST>
        # key_to_exclude = "frame"
        # frames = theater_handler.frames["orchards"]
        # copy = {k: v for k, v in frames.items() if k != key_to_exclude}
        # print(copy)
        # </TEST>
    else:
        msg_id = await theater_handler.bot.send_message(
            chat_id=chat_id, text=f"{username} no es un usuario registrado"
        )
