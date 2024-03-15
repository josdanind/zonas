# standard Library
import os

# Environment Variables
from config import API_CRUD_URL

#  Utils
from utils.path_operations import take_folder_names
from utils.tool_for_views import get_all_views


current_dir = os.path.dirname(os.path.abspath(__file__))
views_name = take_folder_names("bot/views")

views = get_all_views(views_name, current_dir)
