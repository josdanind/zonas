# Standard Library
import os

# Commands
from .commands.main import commands, start_command

# Bot
from ..config.bot import bot
from telebot.types import Message

# TEST
from ..frame_handler.main import orchard_theater, theater_handler


# ********************
# * Commands Handler *
# ********************
@bot.message_handler(commands=commands)
async def command_handler(message: Message):
    chat_id = message.chat.id
    msg_text = message.text.split()
    command = msg_text[0]
    args = msg_text[1:]

    match command:
        case "/start":
            if args:
                await start_command(message, args=args)
            else:
                await theater_handler.send_frame(theater_handler.lobby_frame, chat_id)
                # print(theater_handler.frames)
