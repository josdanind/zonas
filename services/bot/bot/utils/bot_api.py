# Environment Variables
from config import API_CRUD_URL

# AIOHTTP
import aiohttp

# FROM
from libraries.BotFrameHandler.utils import print_test

async def get_buttons(container_url:str, link:str, query: dict, farm_id:int):
    payload = query | {"link": link, "farm_id": farm_id}
    async with aiohttp.ClientSession() as session:
        async with session.post(url=container_url, json = payload) as resp:
            frame_data = await resp.json()

            if resp.status == 200:
                return frame_data
            else:
                return None


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
        payload = {"session_id": session_id, "session_table": to_update}

        async with session.put(url=url, json=payload) as resp:
            user = await resp.json()

            if resp.status == 200:
                return user
            else:
                return None
