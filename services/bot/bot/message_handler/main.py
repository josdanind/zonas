# Standard Library
import os

# Environment Variables
from config import API_CRUD_URL

# Asynchronous http requests
import aiohttp

# Commands
from .commands.main import commands, start_command

# Bot
from ..config.bot import bot
from telebot.types import Message

# >> TEST <<
from ..frame_handler.main import orchard_theater, theater_handler
from libraries.BotFrameHandler.utils import print_test


# ********************
# * Commands Handler *
# ********************
@bot.message_handler(commands=commands)
async def command_handler(message: Message):
    chat_id = message.chat.id
    username = message.chat.username
    msg_text = message.text.split()
    command = msg_text[0]
    args = msg_text[1:]

    match command:
        case "/start":
            await start_command(message)
