# Standard Library
import os, inspect

# pyTelegramBotAPI
from telebot.async_telebot import AsyncTeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# aiohttp
import aiohttp

# Schemas
from .schemas import TheaterSchema, FrameWithImageSchema

# Utils - BotFrameHandler
from libraries.BotFrameHandler.utils import print_error_message, create_button


class TheaterHandler:
    __templates = ["with_img"]
    __cover_path = "img/cover.png"
    __params = ["callback_data"]

    def __init__(
        self,
        bot: AsyncTeleBot,
        theaters: list[TheaterSchema],
        path: str,
        text_box: dict,
        frame_template: str = "with_img",
        row_width=1,
    ) -> None:
        self,
        self.bot = bot
        self.theaters = theaters
        self.path = path
        self.text_box = text_box
        self.frame_template: str = self.__check_template(frame_template)
        self.__lobby_keyboardMarkup = InlineKeyboardMarkup(row_width=row_width)
        self.lobby_frame = self.__create_lobby_frame()
        self.__main_msg_id: int = 0

    def __create_lobby_frame(self):
        cover_path = os.path.join(self.path, self.__cover_path)
        photo: bytes = b""

        try:
            if not os.path.exists(cover_path):
                file_name = os.path.basename(cover_path)

                raise FileNotFoundError(
                    f'"FrameHandler" -> Se produjo un error creando la instancia "FrameHandler". {file_name} no existe.'
                )

            with open(cover_path, mode="rb") as img:
                photo = img.read()

            theaters = self.theaters

            buttons: list[InlineKeyboardButton] = []

            for theater in theaters:
                # *Theater
                theater_id: str = theater.id
                billboard: str = theater.billboard
                display_galleries: bool = theater.display_galleries

                # * --/Atrium
                atrium = theater.atrium
                atrium_callback_data = f"@{theater_id}://{atrium.name}"

                if not display_galleries:
                    buttons.append(
                        InlineKeyboardButton(
                            text=billboard, callback_data=atrium_callback_data
                        )
                    )
                else:
                    buttons.append(
                        InlineKeyboardButton(
                            text=atrium.selfButtonLabel,
                            callback_data=atrium_callback_data,
                        )
                    )
                    # * --/Galleries
                    galleries = theater.galleries

                    for gallery in galleries:
                        buttons.append(
                            InlineKeyboardButton(
                                text=gallery.selfButtonLabel,
                                callback_data=f"@{theater_id}://{gallery.name}",
                            )
                        )
                print(theater)

            self.__lobby_keyboardMarkup.add(*buttons)

            title = self.text_box["title"]
            description = self.text_box["description"]

            caption = f"<b>{title}</b>\n{description}"
            parse_mode = "HTML"

            if self.frame_template == "with_img":
                lobby_frame = FrameWithImageSchema(
                    photo=photo,
                    reply_markup=self.__lobby_keyboardMarkup,
                    caption=caption,
                    parse_mode=parse_mode,
                )

            return lobby_frame
        except Exception as err:
            print("ERROR: ", err)

    def __check_template(self, template: str):
        try:
            valid_template = template in self.__templates

            if valid_template:
                return template
            else:
                raise ValueError(f"Invalid frame template: {template}")
        except ValueError as err:
            print_error_message(err)
