# Class to create an asynchronous bot
from telebot.async_telebot import AsyncTeleBot

# Bot Token
from config import BOT_TOKEN

# Instance an asynchronous bot
bot = AsyncTeleBot(BOT_TOKEN)
