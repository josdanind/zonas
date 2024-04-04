# pyTelegramBotAPI
from telebot.async_telebot import AsyncTeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# aiohttp
import aiohttp

# Schemas
from .schemas.views import MainViewSchema, viewFrontend_Schema, homeFrontend_Schema


class ViewHandler:
    params = ["callback_data"]

    def __init__(
        self, bot: AsyncTeleBot, home_view: MainViewSchema, row_with=1
    ) -> None:
        self,
        self.bot = bot
        self.home_view = home_view
        self.__main_view_markup = InlineKeyboardMarkup(row_width=row_with)
        self.home_frontend = self.__create_main_view()
        self.__viewsFrontendList: list[viewFrontend_Schema] = [self.home_frontend]
        self.__main_msg_id: int = 0

    def __create_main_view(self) -> viewFrontend_Schema:
        buttons = []

        # Definición de los botones
        for key, value in self.home_view.buttons.items():
            params = {k: v for k, v in value.items() if k in self.params}
            buttons.append(InlineKeyboardButton(text=key, **params))

        # Teclado de la vista principal
        keyboard = self.__main_view_markup.add(*buttons)

        # Frontend de la Vista Principal: /home
        return homeFrontend_Schema(
            cover=self.home_view.cover,
            path=self.home_view.path,
            keyboard=keyboard,
        )

    async def send_frontend(
        self,
        view_name: str,
        chat_id: int,
        caption: str,
        show_buttons: bool = True,
        parse_mode: str | None = None,
    ):
        view = [view for view in self.__viewsFrontendList if view.name == view_name]

    async def auth_user(self, user):
        async with aiohttp.ClientSession() as session:
            async with session.post(url=self.db_url + f"/login/{user}") as resp:
                user = await resp.json()
