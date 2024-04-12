# Standard Library
import os

# Commands
from .commands.main import commands, start_command

# Bot
from ..config.bot import bot
from telebot.types import Message

# TEST
# from ..views import main
from ..frame_handler.main import orchard_theater, theater_handler


# ********************
# * Commands Handler *
# ********************
@bot.message_handler(commands=commands)
async def command_handler(message: Message):
    msg_text = message.text.split()
    command = msg_text[0]
    args = msg_text[1:]

    match command:
        case "/start":
            if args:
                await start_command(message, args=args)
            else:
                # print(orchard_theater)
                theater = theater_handler.theaters[0]
                print(theater_handler.lobby_frame.reply_markup)
