# Bot
from ...config.bot import bot
from telebot.types import Message, InputFile, InlineKeyboardButton, InlineKeyboardMarkup

# Environment variables
from config import API_CRUD_URL

# Utils
from bot.utils import auth

home_cover = "bot/assets/views/home/home.png"

markup = InlineKeyboardMarkup(row_width=1)
markup.add(
    InlineKeyboardButton("Botón 1 Botón 1 Botón 1 Botón 1", callback_data="btn1")
)


def welcome_message(name=""):
    name = f" {name}" if name else name
    return f"<b><u>Hola{name}, bienvenido Tlaloc</u></b>"


async def start_command(message: Message, args: list = []):
    user = await auth.user_auth(message.chat.username)

    if user:
        await bot.send_photo(
            chat_id=message.chat.id,
            photo=InputFile(home_cover),
            caption="Bienvenidos a Tlaloc",
            reply_markup=markup,
        )
    else:
        print("No eres un usuario")

    # name = " ".join(args)
    # print(welcome_message())
    # await bot.send_message(message.chat.id, welcome_message(name), parse_mode="HTML")
