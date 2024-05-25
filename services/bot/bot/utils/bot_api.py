# Environment Variables
from config import API_CRUD_URL

# AIOHTTP
import aiohttp

# FROM
from libraries.BotFrameHandler.utils import print_test


async def authenticate_user(username: str, chat_id: int):
    async with aiohttp.ClientSession() as session:
        url = API_CRUD_URL + "/login"

        async with session.post(
            url=url, json={"username": username, "chat_id": chat_id}
        ) as resp:
            user = await resp.json()

            if resp.status == 200:
                return user
            else:
                return None


async def update_session(session_id: int, to_update: dict):
    async with aiohttp.ClientSession() as session:
        url = API_CRUD_URL + "/update_session"

        async with session.put(
            url=url, json={"session_id": session_id, "session_table": to_update}
        ) as resp:
            user = await resp.json()

            if resp.status == 200:
                return user
            else:
                return None
