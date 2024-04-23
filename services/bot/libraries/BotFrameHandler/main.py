# Standard Library
import os, inspect

# pyTelegramBotAPI
from telebot.async_telebot import AsyncTeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from telebot.asyncio_helper import ApiTelegramException

# aiohttp
import aiohttp

# Schemas
from .schemas import TheaterSchema, FrameWithImageSchema

# Utils - BotFrameHandler
from libraries.BotFrameHandler.utils import (
    error_handler,
    check_file,
    print_error_message,
    print_error_detail,
    print_test,
)

from libraries.BotFrameHandler.utils.exeptions import TheaterError


class TheaterHandler:
    __templates = ["with_cover"]
    __cover_path = "img/lobby.png"

    def __init__(
        self,
        bot: AsyncTeleBot,
        theaters: list[TheaterSchema],
        path: str,
        text_box: dict,
        frame_template: str = "with_cover",
        row_width=1,
    ) -> None:
        self,
        self.bot = bot
        self.theaters = theaters
        self.path = path
        self.text_box = text_box
        self.frames: dict = {}
        self.frame_template: str = self.__check_template(frame_template)
        self.__lobby_keyboardMarkup = InlineKeyboardMarkup(row_width=row_width)
        self.lobby_frame = self.__create_lobby_frame()
        self.__main_msg_id: int = 0

    def __create_lobby_frame(self):
        """Crea el Frame del Lobby

        Returns:
            frame: retorna un Frame y su Template se definió a partir del
            atributo `self.frame_template: str`
        """
        # Mensaje de error si no se crea el frame del lobby
        error_message = "Se produjo un error creando el frame del Lobby"
        # str: Path del Cover del lobby
        cover_path = os.path.join(self.path, self.__cover_path)
        # bytes: contendrá la imagen del Cover
        photo: bytes = b""

        try:
            check_file(cover_path)

            with open(cover_path, mode="rb") as img:
                photo = img.read()

            # Contendrá los `InlineKeyboardButtons` para el Keyboard
            buttons: list[InlineKeyboardButton] = []

            # * Crea los botones que erutan a cada `Theater`
            for theater in self.theaters:
                if not theater:
                    raise TheaterError(
                        message=self.__class__.__name__,
                        details=[
                            inspect.currentframe().f_code.co_name,
                            "Theater no valido",
                        ],
                    )

                theater_id: str = theater.id
                billboard: str = theater.billboard
                display_galleries: bool = theater.display_galleries

                theater_callback_data = (
                    f'@{theater_id}://{"galleries" if display_galleries else "atrium"}'
                )

                buttons.append(
                    InlineKeyboardButton(
                        text=billboard, callback_data=theater_callback_data
                    )
                )

                # Theater keyboard
                keyboard = InlineKeyboardMarkup(row_width=1)
                theater_buttons: list[InlineKeyboardButton] = []

                # atrium
                atrium = theater.atrium
                atrium_frame = atrium.frame

                # Atrium Photo
                atrium_cover_path = atrium_frame.data["cover"]
                check_file(atrium_cover_path)

                with open(atrium_cover_path, mode="rb") as img:
                    atrium_photo = img.read()

                if not display_galleries:
                    crops = [
                        {"id": 123, "name": "Jalapeño"},
                        {"id": 234, "name": "papaya"},
                    ]
                else:
                    theater_buttons.append(
                        InlineKeyboardButton(
                            text=atrium.selfButtonLabel,
                            callback_data=f"@{theater_id}://atrium",
                        )
                    )

                    # Galleries
                    galleries = theater.galleries

                    for gallery in galleries:
                        theater_buttons.append(
                            InlineKeyboardButton(
                                text=gallery.selfButtonLabel,
                                callback_data=f"@{theater_id}://{gallery.name}",
                            )
                        )

                # if atrium_frame.template == "with_cover":

                # print_test(a)
                # if self.frame_template == "with_img":
                # lobby_frame = FrameWithImageSchema(
                #     photo=photo,
                #     reply_markup=self.__lobby_keyboardMarkup,
                #     caption=caption,
                #     parse_mode=parse_mode,
                # )

            # Se añaden los botones al `Keyboard`
            self.__lobby_keyboardMarkup.add(*buttons)

            # *Se Define el `caption` del frame
            title = self.text_box["title"]
            description = self.text_box["description"]
            caption = f"<b>{title}</b>\n\n{description}"
            parse_mode = "HTML"

            # *Se crea el  Frame
            if self.frame_template == "with_cover":
                lobby_frame = FrameWithImageSchema(
                    photo=photo,
                    reply_markup=self.__lobby_keyboardMarkup,
                    caption=caption,
                    parse_mode=parse_mode,
                )

            return lobby_frame
        except FileNotFoundError as e:
            print_error_detail(
                title=e.args[0]["caller"], details=[error_message, e.args[0]["reason"]]
            )
        except TheaterError as e:
            print_error_detail(title=e, details=e.details)
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

    async def send_frame(self, frame: FrameWithImageSchema, chat_id: int):
        msg: Message | None = None
        error_title = "Se produjo un error al intentar enviar un frame"

        try:
            msg: Message | None = None

            match frame.template_name:
                case "whit_img":
                    msg = await self.bot.send_photo(
                        chat_id=chat_id,
                        photo=frame.photo,
                        reply_markup=frame.reply_markup,
                        caption=frame.caption,
                        parse_mode=frame.parse_mode,
                    )

            return msg.message_id
        except ApiTelegramException as e:
            if e.error_code == 400:
                print_error_detail(
                    title=error_title,
                    details=[e.description],
                )
            else:
                print_error_detail(
                    title=error_title,
                    details=["API Telegram error", e.description],
                )
        except Exception as e:
            print_error_detail(
                title=error_title,
                details=[e],
            )

    async def get_frame(self, route: str):
        pass
