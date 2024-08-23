# Bot
from telebot.types import Message

# Theater Handler
from ...frame_handler.main import theater_handler


async def start_command(message: Message):
    # Extrae información del usuario
    username = message.chat.username
    chat_id = message.chat.id

    # Autentica el usuario
    user = await theater_handler.authenticate_user(username, chat_id)

    if user:
        # Envía el frame del lobby.
        msg_id = await theater_handler.send_frame(theater_handler.lobby_frame, chat_id)

        # Actualiza la sesión de usuario con la ruta del lobby
        await theater_handler.update_session(
            session_id=user["session_id"],
            to_update={
                "main_message_id": msg_id,
                "current_action": "/"
            }
        )
    else:
        # Enviar mensaje indicando que el usuario no está registrado
        error_message = f"{username} no es un usuario registrado"
        msg_id = await theater_handler.bot.send_message(chat_id=chat_id, text=error_message)

