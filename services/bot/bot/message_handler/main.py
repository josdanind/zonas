# Standard Library
import os

# Commands
from .commands.main import commands, start_command

# Bot
from ..config.bot import bot
from telebot.types import Message

# TEST
from ..views import main


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
                print(main.views)
                for view in main.views:
                    print(view.view)
            print(msg_text, args)
