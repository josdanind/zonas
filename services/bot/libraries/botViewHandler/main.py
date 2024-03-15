# pyTelegramBotAPI
from telebot.async_telebot import AsyncTeleBot


# aiohttp
import aiohttp


class ViewHandler:
    def __init__(self, bot: AsyncTeleBot, db_url: str) -> None:
        self,
        self.bot = bot
        self.db_url = db_url

    async def auth_user(self, user):
        async with aiohttp.ClientSession() as session:
            async with session.post(url=self.db_url + f"/login/{user}") as resp:
                user = await resp.json()
