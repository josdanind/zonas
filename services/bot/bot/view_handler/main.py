# Asynchronous bot
from ..config.bot import bot

# botViewHandler
from libraries.botViewHandler import ViewHandler

# Views
from ..views.main import home_view  # Main view

view_handler = ViewHandler(bot=bot, home_view=home_view)
