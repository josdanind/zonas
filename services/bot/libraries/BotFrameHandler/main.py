# Standard Library
import inspect

# pyTelegramBotAPI
from telebot.async_telebot import AsyncTeleBot
from telebot.asyncio_helper import ApiTelegramException
from telebot.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    Message,
    InputMediaPhoto,
)

# aiohttp
import aiohttp

# Schemas
from .schemas import (
    ButtonSchema,
    FrameSchema,
    PhysicalFrame,
    TheaterSchema,
)

# Utils - BotFrameHandler
from libraries.BotFrameHandler.utils import (
    http_exception_handler,
    error_handler,
    check_file,
    print_error_message,
    print_error_detail,
    print_test
)

from libraries.BotFrameHandler.utils.makeHttpRequest import fetch
class TheaterHandler:
    __templates = ["with_cover"]
    # Endpoint paths
    __update_session_endpoint = "/update_session"
    __authenticate_user = "/login"
    __ticket_office = "/ticket_office"

    def __init__(
        self,
        bot: AsyncTeleBot,
        theaters: list[TheaterSchema],
        cover_url: str,
        api_crud_url: str,
        text_box: dict,
        frame_template: str = "with_cover",
    ) -> None:
        self,
        self.bot = bot
        self.theaters = self.__check_theaters(theaters)
        self.cover_url = cover_url
        self.api_crud_url = api_crud_url
        self.text_box = text_box
        self.theater_frame_data = {}
        self.frame_template: str = self.__check_template(frame_template)
        self.__lobby_keyboardMarkup = self.__set_keyboard(frame_template)
        self.lobby_frame = self.__create_lobby_frame()

    @http_exception_handler
    async def update_session(self, session_id: int, to_update: dict):
        async with aiohttp.ClientSession() as session:
            url = self.api_crud_url + self.__update_session_endpoint
            payload = {"session_id": session_id, "session_table": to_update}

            async with session.put(url=url, json=payload) as resp:
                # Raise an error if the response status is 4xx or 5xx
                resp.raise_for_status()

                # Return JSON response if the status code is 200
                return await resp.json()

    @http_exception_handler
    async def authenticate_user(self, username: str, chat_id: int):
        url = f"{self.api_crud_url}{self.__authenticate_user}"
        payload = {"username": username, "chat_id": chat_id}

        async with aiohttp.ClientSession() as session:
            async with session.post(url=url, json=payload) as resp:
                # Raise an error if the response status is 4xx or 5xx
                resp.raise_for_status()

                # Return JSON response if the status code is 200
                return await resp.json()

    @http_exception_handler
    async def get_atrium(self, theater_name:str, **condition):
        theater_data = self.theater_frame_data[theater_name]
        container_url = self.api_crud_url + theater_data["container_path"]

        # Datos del atrium
        frame_data = theater_data["galleries"]["atrium"]
        text_box = frame_data["text_box"]
        link = frame_data["link"]
        query = frame_data["query"]

        # *Cover y Caption
        cover = frame_data["cover"]
        caption =  f"<b>{text_box['title']}</b>\n\n{text_box['description']}"

        # *Buttons
        buttons: list[ButtonSchema] = []
        # *Template
        template = frame_data["template"]

        async with aiohttp.ClientSession() as session:
            payload = {**query, "link": link, **condition}

            async with session.post(url=container_url, json=payload) as resp:
                resp.raise_for_status()

                buttons =  await resp.json()

        # Añadir botón "Ir atrás"
        buttons.append(
            {
                "text": "Ir atrás",
                "callback_data": f"goBack@{theater_name}",
            }
        )

        #* Retorna el Frame del Atrium
        return TheaterHandler.create_frame_with_template(
            cover=cover,
            caption=caption,
            buttons=buttons,
            template=template
        )

    async def get_physical_frame(self, theater:str, id:int) -> PhysicalFrame:
        url = f"{self.api_crud_url}{self.__ticket_office}/{theater}"
        params = {"id": id}

        async with aiohttp.ClientSession() as session:
            physical_frame = await fetch(
                session=session,
                url=url,
                params=params
            )

        return PhysicalFrame(**physical_frame)

    @staticmethod
    def build_frame_from_physical(
        physical_frame: PhysicalFrame
    ):
        match physical_frame.template:
            case "with_cover":
                keyboard = InlineKeyboardMarkup(row_width=1)
                buttons = physical_frame.buttons
                theater = physical_frame.theater
                frame_id = physical_frame.id
                cover = physical_frame.cover
                caption = physical_frame.caption


                if  buttons:
                    keyboard.add(
                        *[InlineKeyboardButton(**button) for button in buttons]
                    )

                # Close Button
                close_button = InlineKeyboardButton(
                    text="Cerrar",
                    callback_data=f"closeFrame://{theater}?id={frame_id}"
                )

                keyboard.add(close_button)

                return FrameSchema(
                    cover=cover,
                    reply_markup=keyboard,
                    caption=caption,
                    parse_mode="HTML",
                    frame_template="with_cover"
                )



    @staticmethod
    def create_frame_with_template(
        cover: str,
        caption: str,
        buttons: list[dict],
        template: str
    ) -> FrameSchema:
        match template:
            case "with_cover":
                keyboard = InlineKeyboardMarkup(row_width=1)
                keyboard.add(
                    *[InlineKeyboardButton(**button) for button in buttons]
                )

                return FrameSchema(
                    cover=cover,
                    reply_markup=keyboard,
                    caption=caption,
                    parse_mode="HTML"
                )

    def __set_keyboard(self, frame_template: str) -> InlineKeyboardMarkup:
        """
        Define el diseño del teclado, estableciendo la cantidad de botones por fila

        Args:
            frame_template (str): plantilla del frame

        Returns:
            InlineKeyboardMarkup: Teclado del TheaterHandler
        """
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
                - 'display_galleries' (bool): 'true' para mostrar las 'galleries' en el frame del theater, 'false' para ir directamente al Atrium.
                - 'galleries' (dict): las llaves son las galerías del theater (Incluye el atrium), cada una contiene las keys: link, query, cover, text_box.
                - 'galleries_buttons' (list): Son botones que contienen el enlace hacia cada 'gallery' (se incluye el Atrium).
                - 'container_path' (str): El path del endpoint para acceder al contenedor del Theater.
        """
        # * KEYBOARD
        keyboard = self.__set_keyboard(theater.frame_template)
        buttons: list[InlineKeyboardButton] = []
        galleries = {}

        # * ATRIUM
        # * Button
        atrium = theater.atrium
        atrium_frame = atrium.frame
        atrium_link = f"@{theater.id}://atrium"

        atrium_button: InlineKeyboardButton = InlineKeyboardButton(
            text=atrium.selfButtonLabel, callback_data=atrium_link
        )

        galleries.update(
            {
                "atrium": {
                    "link": atrium_link,
                    "query": atrium_frame.query,
                    "cover": atrium_frame.data["cover"],
                    "text_box": atrium_frame.data["text_box"],
                    "template": atrium_frame.template
                }
            }
        )

        # * GALLERIES BUTTONS
        gallery_buttons: list[InlineKeyboardButton] = []

        for gallery in theater.galleries:
            gallery_link = f"@{theater.id}://{gallery.name}"
            button = {
                "text": gallery.selfButtonLabel,
                "callback_data": gallery_link,
            }

            gallery_buttons.append(InlineKeyboardButton(**button))

            galleries.update(
                {
                    gallery.name: {
                        "link": gallery_link,
                        "query": gallery.frame.query,
                        "cover": gallery.frame.data["cover"],
                        "text_box": gallery.frame.data["text_box"],
                        "template": gallery.frame.template
                    }
                }
            )

        # * Creating the keyboard
        buttons.append(atrium_button)
        buttons += gallery_buttons
        # -- GoBack Button
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
            cover=atrium_frame.data["cover"], reply_markup=keyboard, caption=caption, parse_mode="HTML"
        )


        return {
            f"{theater.id}": {
                "frame": frame,
                "display_galleries": theater.display_galleries,
                "galleries": galleries,
                "galleries_buttons": gallery_buttons,
                "container_path": theater.container.endpoint_path
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
        cover: str = self.cover_url

        try:
            # *Lobby Keyboard
            # --Buttons list
            buttons: list[InlineKeyboardButton] = []

            # *Este ciclo "for" crea los botones que se exponen en el Lobby,
            # *cada botón es un enlace hacia un Theater
            for theater in self.theaters:
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

                # self.frames.update(theater_frames)
                self.theater_frame_data.update(theater_frames)

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

    def __check_theaters(self, theaters:list[TheaterSchema]):
        ok_theaters = []

        for theater in theaters:
            if not isinstance(theater, TheaterSchema):
                print_error_detail(
                        title="Se produjo un error al incluir un Theater en el TheaterHandler",
                        details=[
                            inspect.currentframe().f_code.co_name,
                            "Theater no valido",
                        ]
                )
            else:
                ok_theaters.append(theater)

        return ok_theaters

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
        self, chat_id: int, user: dict, frame: FrameSchema, frame_route: str
    ):
        error_title = "Se produjo un error al intentar modificar un mensaje"

        try:
            match frame.frame_template:
                case "with_cover":
                    msg = await self.bot.edit_message_media(
                        chat_id=chat_id,
                        message_id=user["main_message_id"],
                        media=InputMediaPhoto(
                            media=frame.cover,
                            caption=frame.caption,
                            parse_mode=frame.parse_mode,
                        ),
                        reply_markup=frame.reply_markup,
                    )

                    await self.update_session(
                        session_id=user["session_id"],
                        to_update={"current_action": frame_route}
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
