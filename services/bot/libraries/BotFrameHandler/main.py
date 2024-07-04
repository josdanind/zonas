# Standard Library
import os, inspect

# pyTelegramBotAPI
from telebot.async_telebot import AsyncTeleBot
from telebot.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    Message,
    InputMediaPhoto,
)
from telebot.asyncio_helper import ApiTelegramException

# aiohttp
import aiohttp

# Schemas
from .schemas import TheaterSchema,  FrameSchema

# Utils - BotFrameHandler
from libraries.BotFrameHandler.utils import (
    error_handler,
    check_file,
    print_error_message,
    print_error_detail,
    print_test,
)

class TheaterHandler:
    __templates = ["with_cover"]
    __cover_path = "img/lobby.png"

    def __init__(
        self,
        bot: AsyncTeleBot,
        theaters: list[TheaterSchema],
        path: str,
        api_crud_url: str,
        text_box: dict,
        frame_template: str = "with_cover",
    ) -> None:
        self,
        self.bot = bot
        self.theaters = theaters
        self.path = path
        self.api_crud = api_crud_url
        self.text_box = text_box
        self.frames = {}
        self.frame_template: str = self.__check_template(frame_template)
        self.__lobby_keyboardMarkup = self.__set_keyboard(frame_template)
        self.lobby_frame = self.__create_lobby_frame()

    def __set_keyboard(self, frame_template: str) -> InlineKeyboardMarkup:
        # *Verifica si es un template válido
        template = self.__check_template(frame_template)

        match template:
            case "with_cover":
                return InlineKeyboardMarkup(row_width=1)

    def __set_theater_frames(self, theater: TheaterSchema):
        """
        Reúne la data de todos los Frames que componen a un Theater. El Frame principal
        (el "frontend" del Theater) se crea y se anexa a la key "frame" del diccionario
        que retorna este método.

        Los Frames de las Galleries no se crean, pero los botones (galleries_buttons)
        que erutan a hacia cada gallery, sí. 'text' contiene la etiqueta que describe
        su respectiva Gallery, y el 'callback_data' contiene el enlace a su respectivo Frame.

        Si el Theater se configuró para no mostrar las 'galleries' (display_galleries=false)
        el frame principal (el del Theater) no será enviado, en su lugar, se envía el frame
        del 'Atrium', en muchas ocasiones solo se desea mostrar el 'Atrium'.

        Args:
            theater (TheaterSchema): Es un objeto 'Theater'

        Returns:
            dict:
                - 'frame' (FrameSchema): es el frame del Theater.
                - 'display_galleries' (bool): 'true' para mostrar las 'galleries' en el frame del theater.
                - 'atrium' (str): enlace para obtener el 'frame' del 'atrium'
                - "galleries_buttons" (list): son botones que contienen el enlace de cada 'gallery' y del 'atrium'
        """
        # * KEYBOARD
        keyboard = self.__set_keyboard(theater.frame_template)
        buttons: list[InlineKeyboardButton] = []

        # * ATRIUM BUTTON
        atrium = theater.atrium
        atrium_frame = atrium.frame
        atrium_button: InlineKeyboardButton = InlineKeyboardButton(
            text=atrium.selfButtonLabel, callback_data=f"@{theater.id}://atrium"
        )

        # * GALLERIES BUTTONS
        gallery_buttons: list[InlineKeyboardButton] = []
        for gallery in theater.galleries:
            button = {
                "text": gallery.selfButtonLabel,
                "callback_data": f"@{theater.id}://{gallery.name}",
            }

            gallery_buttons.append(InlineKeyboardButton(**button))

        # * COVER
        atrium_cover_path = atrium_frame.data["cover"]
        check_file(atrium_cover_path)

        with open(atrium_cover_path, mode="rb") as img:
            photo = img.read()

        # * Creating the keyboard
        buttons.append(atrium_button)
        buttons += gallery_buttons

        # -- GoBack Button
        if atrium_frame.back_button:
            buttons.append(
                InlineKeyboardButton(
                    text="Ir atrás",
                    callback_data=f"goBack@lobby",
                )
            )

        keyboard.add(*buttons)

        # * CAPTION
        caption = f"<b>{theater.billboard}</b>"

        frame = FrameSchema(
            cover=photo, reply_markup=keyboard, caption=caption, parse_mode="HTML"
        )

        return {
            f"{theater.id}": {
                "frame": frame,
                "display_galleries": theater.display_galleries,
                "atrium": f"@{theater.id}://atrium",
                "galleries_buttons": gallery_buttons,
            }
        }

    def __create_lobby_frame(self):
        """Crea el Frame del Lobby, éste, es el "frontend" del 'Frame Handler'.

        El 'Lobby' expone cada 'Theater' que se incluye en el 'Frame Handler'.

        Returns:
            frame: es un Frame y su Template se definió a partir del
            atributo `self.frame_template: str`
        """
        # Mensaje de error si no se crea el frame del lobby
        error_message = "Se produjo un error creando el frame del Lobby"
        # str: Path del Cover del lobby
        cover_path = os.path.join(self.path, self.__cover_path)
        # bytes: contendrá la imagen del Cover
        cover: bytes | None = b""

        try:
            # *Lobby Cover
            check_file(cover_path)
            with open(cover_path, mode="rb") as img:
                cover = img.read()

            # *Lobby Keyboard
            # --Buttons list
            buttons: list[InlineKeyboardButton] = []

            # *Este ciclo "for" crea los botones que se exponen en el Lobby,
            # *cada botón es un enlace hacia un Theater
            for theater in self.theaters:
                # *Verifica si el elemento de la lista es un Theater
                if not isinstance(theater, TheaterSchema) :
                    print_error_detail(title=error_message, details=[
                        inspect.currentframe().f_code.co_name,
                        "Theater no valido",
                    ])

                    continue

                theater_id: str = theater.id
                billboard: str = theater.billboard

                # *Define en el callback_data de cada botón el enlace hacia theater respectivo
                # *si se va al atrium directamente o se muestran todas las galerías
                display_galleries: bool = theater.display_galleries

                # Define si se muestran todas las galerías o solo el Atrium
                theater_callback_data = (
                    f'@{theater_id}://{"galleries" if display_galleries else "atrium"}'
                )

                buttons.append(
                    InlineKeyboardButton(
                        text=billboard, callback_data=theater_callback_data
                    )
                )

                theater_frames = self.__set_theater_frames(theater)

                self.frames.update(theater_frames)

            # Se añaden los botones al `Keyboard`
            self.__lobby_keyboardMarkup.add(*buttons)

            # *Se Define el `caption` del frame
            # --// Title
            title = self.text_box["title"]
            # --// Description
            description = self.text_box["description"]
            # --// Caption
            caption = f"<b>{title}</b>\n\n{description}"

            # *Se define el parse_mode
            parse_mode = "HTML"

            # *Se crea el Frame
            if self.frame_template == "with_cover":
                lobby_frame = FrameSchema(
                    cover=cover,
                    reply_markup=self.__lobby_keyboardMarkup,
                    caption=caption,
                    parse_mode=parse_mode,
                )

            return lobby_frame

        except FileNotFoundError as e:
            print_error_detail(
                title=e.args[0]["caller"], details=[error_message, e.args[0]["reason"]]
            )
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

    async def send_frame(self, frame: FrameSchema, chat_id: int):
        msg: Message | None = None
        error_title = "Se produjo un error al intentar enviar un frame"

        try:
            match frame.frame_template:
                case "with_cover":
                    msg = await self.bot.send_photo(
                        chat_id=chat_id,
                        photo=frame.cover,
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

    async def change_message(
        self, chat_id: int, message_id: str, frame: FrameSchema
    ):
        error_title = "Se produjo un error al intentar modificar un mensaje"

        try:
            match frame.frame_template:
                case "with_cover":
                    msg = await self.bot.edit_message_media(
                        chat_id=chat_id,
                        message_id=message_id,
                        media=InputMediaPhoto(
                            media=frame.cover,
                            caption=frame.caption,
                            parse_mode=frame.parse_mode,
                        ),
                        reply_markup=frame.reply_markup,
                    )

                    return msg
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
